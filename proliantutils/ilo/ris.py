 # Copyright 2014 Hewlett-Packard Development Company, L.P.
 #
 # Licensed under the Apache License, Version 2.0 (the "License"); you may
 # not use this file except in compliance with the License. You may obtain
 # a copy of the License at
 #
 #      http://www.apache.org/licenses/LICENSE-2.0
 #
 # Unless required by applicable law or agreed to in writing, software
 # distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 # WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 # License for the specific language governing permissions and limitations
 # under the License.


"""
---------------------------------------------------------------------------------------------------------------------
IMPORTANT!!!
---------------------------------------------------------------------------------------------------------------------
When developing a client for the HP RESTful API, be sure to not code based upon assumptions that are not guaranteed.
Search for, and note any 'NOTE' comments in this code to read about ways to avoid incorrect assumptions.

The reason avoiding these assumptions is so important is that implementations may vary across systems and firmware
versions, and we want your code to work consistently.

---------------------------------------------------------------------------------------------------------------------
STARTING ASSUMPTIONS
---------------------------------------------------------------------------------------------------------------------

On URIs:

The HP RESTful API is a "hypermedia API" by design.  This is to avoid building in restrictive assumptions to the
data model that will make it difficult to adapt to future hardware implementations.  A hypermedia API avoids these
assumptions by making the data model discoverable via links between resources.

A URI should be treated by the client as opaque, and thus should not be attempted to be understood or deconstructed
by the client.  Only specific top level URIs (any URI in this sample code) may be assumed, and even these may be
absent based upon the implementation (e.g. there might be no /rest/v1/Systems collection on something that doesn't
have compute nodes.)

The other URIs must be discovered dynamically by following href links.  This is because the API will eventually be
implemented on a system that breaks any existing data model "shape" assumptions we may make now.  In particular,
clients should not make assumptions about the URIs for the resource members of a collection.  For instance, the URI of
a collection member will NOT always be /rest/v1/.../collection/1, or 2.  On Moonshot a System collection member might be
/rest/v1/Systems/C1N1.

This sounds very complicated, but in reality (as these examples demonstrate), if you are looking for specific items,
the traversal logic isn't too complicated.

On Resource Model Traversal:

Although the resources in the data model are linked together, because of cross link references between resources,
a client may not assume the resource model is a tree.  It is a graph instead, so any crawl of the data model should
keep track of visited resources to avoid an infinite traversal loop.

A reference to another resource is any property called "href" no matter where it occurs in a resource.

An external reference to a resource outside the data model is referred to by a property called "extref".  Any
resource referred to by extref should not be assumed to follow the conventions of the API.

On Resource Versions:

Each resource has a "Type" property with a value of the format Tyepname.x.y.z where
* x = major version - incrementing this is a breaking change to the schema
* y = minor version - incrementing this is a non-breaking additive change to the schema
* z = errata - non-breaking change

Because all resources are versioned and schema also have a version, it is possible to design rules for "nearest"
match (e.g. if you are interacting with multiple services using a common batch of schema files).  The mechanism
is not prescribed, but a client should be prepared to encounter both older and newer versions of resource types.

On HTTP POST to create:

WHen POSTing to create a resource (e.g. create an account or session) the guarantee is that a successful response
includes a "Location" HTTP header indicating the resource URI of the newly created resource.  The POST may also
include a representation of the newly created object in a JSON response body but may not.  Do not assume the response
body, but test it.  It may also be an ExtendedError object.

HTTP REDIRECT:

All clients must correctly handle HTTP redirect.  We (or Redfish) may eventually need to use redirection as a way
to alias portions of the data model.

FUTURE:  Asynchronous tasks

In the future some operations may start asynchonous tasks.  In this case, the client should recognized and handle
HTTP 202 if needed and the 'Location' header will point to a resource with task information and status.

JSON-SCHEMA:

The json-schema available at /rest/v1/Schemas governs the content of the resources, but keep in mind:
* not every property in the schema is implemented in every implementation.
* some properties are schemed to allow both null and anotehr type like string or integer.

Robust client code should check both the existence and type of interesting properties and fail gracefully if
expectations are not met.

GENERAL ADVICE:

Clients should always be prepared for:
* unimplemented properties (e.g. a property doesn't apply in a particular case)
* null values in some cases if the value of a property is not currently known due to system conditions
* HTTP status codes other than 200 OK.  Can your code handle an HTTP 500 Internal Server Error with no other info?
* URIs are case insensitive
* HTTP header names are case insensitive
* JSON Properties and Enum values are case sensitive
* A client should be tolerant of any set of HTTP headers the service returns

"""
__author__ = 'HP'

import urllib2
from urlparse import urlparse
import httplib
import base64
import json
import hashlib
import gzip
import StringIO
import sys

import operations

class RISOperations(operations.IloOperations):

    def __init__(self, host, login, password, bios_password=None):
        self.host = host
        self.login = login
        self.password = password
        self.bios_password = bios_password
        # Message registry support
        self.message_registries = {}
    
    def rest_op(self, operation, suburi, request_headers, request_body):
        """ Generic REST Operation handler"""
    
        url = urlparse('https://' + self.host + suburi)
    
        if request_headers is None:
            request_headers = dict()
    
        # Use self.login/self.password and Basic Auth
        if self.login is not None and self.password is not None:
            request_headers['Authorization'] = "BASIC " + base64.b64encode(
                                               self.login + ":" + self.password)
    
        redir_count = 4
        while redir_count:
            conn = None
            if url.scheme == 'https':
                conn = httplib.HTTPSConnection(host=url.netloc, strict=True)
            elif url.scheme == 'http':
                conn = httplib.HTTPConnection(host=url.netloc, strict=True)

            try:
                conn.request(operation, url.path, headers=request_headers, 
                             body=json.dumps(request_body))
                resp = conn.getresponse()
                body = resp.read()
            except Exception as e:
                raise iloclient.IloConnectionError(e)
    
            # NOTE:Do not assume every HTTP operation will return a JSON body.  
            # For example, ExtendedError structures are only required for
            # HTTP 400 errors and are optional elsewhere as they are mostly 
            # redundant for many of the other HTTP status code.  In particular,
            # 200 OK responses should not have to return any body.
    
            # NOTE:  this makes sure the headers names are all lower cases 
            # because HTTP says they are case insensitive
            headers = dict((x.lower(), y) for x, y in resp.getheaders())
    
            # Follow HTTP redirect
            if resp.status == 301 and 'location' in  headers:
                url = urlparse(headers['location'])
                redir_count -= 1
            else:
                break
    
        response = dict()
        try:
            if body:
                response = json.loads(body.decode('utf-8'))
        except ValueError: # if it doesn't decode as json
            # NOTE:  resources may return gzipped content
            # try to decode as gzip (we should check the headers for 
            # Content-Encoding=gzip)
            try:
                gzipper = gzip.GzipFile(fileobj=StringIO.StringIO(body))
                uncompressed_string = gzipper.read().decode('UTF-8')
                response = json.loads(uncompressed_string)
            except Exception as e:
                raise iloclient.IloError(e)
    
        return resp.status, headers, response
    
    def rest_get(self, suburi, request_headers=None):
        """REST GET operation"""
        return self.rest_op('GET', suburi, request_headers, None)
        # NOTE:  HTTP responses could be 500, 404, etc.
    
    def rest_patch(self, suburi, request_headers, request_body):
        """REST PATCH operation"""
        if not isinstance(request_headers, dict):
            request_headers = dict()
        request_headers['Content-Type'] = 'application/json'
        return self.rest_op('PATCH', suburi, request_headers, request_body)
        # NOTE:  HTTP responses could be 500, 404, 202 etc.
    
    def rest_put(self, suburi, request_headers, request_body):
        """REST PUT operation"""
        if not isinstance(request_headers, dict):
            request_headers = dict()
        request_headers['Content-Type'] = 'application/json'
        return self.rest_op('PUT', suburi, request_headers, request_body)
        # NOTE:  HTTP responses could be 500, 404, 202 etc.
    
    def rest_post(self, suburi, request_headers, request_body):
        """REST POST operation"""
        if not isinstance(request_headers, dict):
            request_headers = dict()
        request_headers['Content-Type'] = 'application/json'
        return self.rest_op('POST', suburi, request_headers, request_body)
        # NOTE:  don't assume any newly created resource is included in the
        # response. Only the Location header matters. The response body may
        # be the new resource, it may be an ExtendedError, or it may be empty.
    
    def rest_delete(self, suburi, request_headers):
        """REST DELETE operation"""
        return self.rest_op('DELETE', suburi, request_headers, None)
        # NOTE:  be prepared for various HTTP responses including 500, 404, etc.
        # NOTE:  response may be an ExtendedError or may be empty
    
    def get_type(self, obj):
        """ Return the type of an object 
        (down to the major version, skipping minor, and errata) """
        typever = obj['Type']
        typesplit = typever.split('.')
        return typesplit[0] + '.' + typesplit[1]
    
    def operation_allowed(self, headers_dict, operation):
        """ Checks HTTP response headers for specified operation 
        (e.g. 'GET' or 'PATCH') is allowed on the resource. """
        if 'allow' in headers_dict:
            if operation in headers_dict['allow']:
                return True
        return False
    
    def render_extended_error_message_list(self, extended_error):
        """ Build a list of decoded messages from the extended_error using the
            message registries. An ExtendedError JSON object is a response from
            the with its own schema.  This function knows how to parse the 
            ExtendedError object and, using any loaded message registries, render
            an array of plain language strings that represent the response."""
        messages = []
        if isinstance(extended_error, dict):
            if 'Type' in extended_error and extended_error['Type'].\
                                            startswith('ExtendedError.'):
                for msg in extended_error['Messages']:
                    message_id = msg['MessageID']
                    x = message_id.split('.')
                    registry = x[0]
                    msgkey = x[len(x) - 1]
    
                    # if the correct message registry is loaded, do string resolution
                    if registry in self.message_registries:
                        if registry in self.message_registries and \
                           msgkey in self.message_registries[registry]['Messages']:
                            msg_dict = self.message_registries[registry]['Messages'][msgkey]
                            msg_str = message_id + ':  ' + msg_dict['Message']
    
                            for argn in range(0, msg_dict['NumberOfArgs']):
                                subst = '%' + str(argn+1)
                                msg_str = msg_str.replace(subst, str(msg['MessageArgs'][argn]))
    
                            if 'Resolution' in msg_dict and msg_dict['Resolution'] != 'None':
                                msg_str += '  ' + msg_dict['Resolution']
    
                            messages.append(msg_str)
                    else: # no message registry, simply return the msg object in string form
                        messages.append(str(message_id))
    
        return messages
    
    def get_extended_error(self, extended_error):
        """ Gets the list of decoded messages from the extended_error """
        return self.render_extended_error_message_list(extended_error)

    def _get_host_details(self):
        """ Get the system details """
        # Assuming only one system present as part of collection,
        # as we are dealing with iLO's here.
        status, headers, system = self.rest_get('/rest/v1/Systems/1')
        if status < 300:
            stype = self.get_type(system)
            if not (stype == 'ComputerSystem.0' or 
                    stype(system) == 'ComputerSystem.1'):
                msg = "%s is not a valid system type " % stype
                raise iloclient.IloError(msg)
        else:
            msg = self.get_extended_error(system)
            raise iloclient.IloError(msg)
        
        return system
        
    def _get_bios_setting(self, bios_property):
        """ Retrieves bios settings of the server"""
        system = self._get_host_details()
        
        # find the BIOS URI
        if 'links' not in system['Oem']['Hp']:
            msg = '"links/BIOS" section in ComputerSystem/Oem/Hp does not exist'
            raise iloclient.IloCommandNotSupportedError(msg)

        bios_uri = system['Oem']['Hp']['links']['BIOS']['href']
        
        # get the BIOS object
        status, headers, bios_settings = self.rest_get(bios_uri)
        
        if status >= 300:
            msg = self.get_extended_error(system)
            raise iloclient.IloError(msg)
        
        # check to make sure the bios_property is supported
        if bios_property not in bios_settings:
            # not supported on this platform
            msg = '\tBIOS Property "' + bios_property + \
                  '" is not supported on this system'
            raise iloclient.IloCommandNotSupportedError(msg)
                    
        return bios_settings[bios_property]
    
    def get_secure_boot_state(self):
        """ Get the status if secure boot is enabled or not """
        system = self._get_host_details()
        
        if 'links' not in system['Oem']['Hp'] or \
           'SecureBoot' not in system['Oem']['Hp']['links']:
            msg = '"SecureBoot" resource or feature is not supported on this system'
            raise iloclient.IloCommandNotSupportedError(msg)
        
        secure_boot_uri = system['Oem']['Hp']['links']['SecureBoot']['href']
    
        # get the Secure Boot object
        status, headers, secure_boot_settings = self.rest_get(secure_boot_uri)
        
        if status >= 300:
            msg = self.get_extended_error(system)
            raise iloclient.IloError(msg)
        
        return secure_boot_settings['SecureBootCurrentState']
    
    
    def _change_bios_setting(self, bios_property, value):
        """ Change the bios setting to specified value """
        system = self._get_host_details()
        
        # find the BIOS URI
        if 'links' not in system['Oem']['Hp']:
            msg = '\t"links/BIOS" section in ComputerSystem/Oem/Hp does not exist'
            raise iloclient.IloCommandNotSupportedError(msg)
        
        bios_uri = system['Oem']['Hp']['links']['BIOS']['href']
        
        # get the BIOS object
        status, headers, bios_settings = self.rest_get(bios_uri)
        
        # check to make sure the bios_property is supported
        if bios_property not in bios_settings:
            # not supported on this platform
            msg = '\tBIOS Property "' + bios_property + '" is not supported on this system'
            raise iloclient.IloCommandNotSupportedError(msg)
        
        # if this BIOS resource doesn't support PATCH, go get the Settings, which should
        if not self.operation_allowed(headers, 'PATCH'):   # this is GET-only
            bios_uri = bios_settings['links']['Settings']['href']
            status, headers, bios_settings = self.rest_get(bios_uri)
            # this should allow PATCH, else raise error
            if not self.operation_allowed(headers, 'PATCH'):
                msg = "PATCH Operation not supported on the resource %s " %  bios_uri
                raise iloclient.IloError(msg)
    
        # we don't need to PATCH back everything, change the required one
        new_bios_settings = dict()
        new_bios_settings[bios_property] = value
        request_headers = dict()
        if self.bios_password:
            bios_password_hash = hashlib.sha256(
                                 self.bios_password.encode()).hexdigest().upper()
            request_headers['X-HPRESTFULAPI-AuthToken'] = bios_password_hash
    
        # perform the patch
        print('PATCH ' + json.dumps(new_bios_settings) + ' to ' + bios_uri)
        status, headers, response = self.rest_patch(bios_uri, 
                                    request_headers, new_bios_settings)
        print('PATCH response = ' + str(status))
        
        if status >= 300:
            msg = self.get_extended_error(response)
            raise iloclient.IloError(msg)
        
    # Experimental function included
    def _reset_to_default(self):
        """ Change to default  bios setting to default values """
        system = self._get_host_details()
        
        # find the BIOS URI
        if 'links' not in system['Oem']['Hp']:
            msg = '\t"links/BIOS" section in ComputerSystem/Oem/Hp does not exist'
            raise iloclient.IloCommandNotSupportedError(msg)
        
        bios_uri = system['Oem']['Hp']['links']['BIOS']['href']
        status, headers, bios_settings = self.rest_get(bios_uri)
        
        if status >= 300:
            msg = self.get_extended_error(response)
            raise iloclient.IloError(msg)
        
        base_config_uri = bios_settings['links']['BaseConfigs']['href']
        status, headers, config = self.rest_get(base_config_uri)
        
        if status >= 300:
            msg = self.get_extended_error(response)
            raise iloclient.IloError(msg)
        
        # if this BIOS resource doesn't support PATCH, go get the Settings, which should
        if not self.operation_allowed(headers, 'PATCH'):   # this is GET-only
            bios_uri = bios_settings['links']['Settings']['href']
            status, headers, bios_settings = self.rest_get(bios_uri)
            # this should allow PATCH, else raise error
            if not self.operation_allowed(headers, 'PATCH'):
                msg = "PATCH Operation not supported on the resource %s " %  bios_uri
                raise iloclient.IloError(msg)
     
        new_bios_settings = config['BaseConfigs'][0]['default']
        request_headers = dict()
        if self.bios_password:
            bios_password_hash = hashlib.sha256(
                                 self.bios_password.encode()).hexdigest().upper()
            request_headers['X-HPRESTFULAPI-AuthToken'] = bios_password_hash
#     
        # perform the patch
        print('PATCH ' + json.dumps(new_bios_settings) + ' to ' + bios_uri)
        status, headers, response = self.rest_patch(bios_uri, 
                                    request_headers, new_bios_settings)
        print('PATCH response = ' + str(status))
         
        if status >= 300:
            msg = self.get_extended_error(response)
            raise iloclient.IloError(msg)

    def _change_secure_boot_settings(self, property, value):
        """Change secure boot settings on the server """
        system = self._get_host_details()

        # find the BIOS URI
        if 'links' not in system['Oem']['Hp'] or \
           'SecureBoot' not in system['Oem']['Hp']['links']:
            msg = ' "SecureBoot" resource or feature is not supported on this system'
            raise iloclient.IloCommandNotSupportedError(msg)
        
        secure_boot_uri = system['Oem']['Hp']['links']['SecureBoot']['href']
    
        # Change the property required
        new_secure_boot_settings = dict()
        new_secure_boot_settings[property] = value
    
        # perform the patch
        print('PATCH ' + json.dumps(new_secure_boot_settings) + ' to ' + secure_boot_uri)
        status, headers, response = self.rest_patch(
                                    secure_boot_uri, None, new_secure_boot_settings)
        print('PATCH response = ' + str(status))
        if status >= 300:
            msg = self.get_extended_error(response)
            raise iloclient.IloError(msg)
        
        # Change the bios setting as a workaround to enable secure boot
        # Can be removed when fixed for Gen9 snap2
        val = self._get_bios_setting('CustomPostMessage')
        val = val.rstrip() if val.endswith(" ") else val+" "
        self._change_bios_setting('CustomPostMessage', val)
        
    def set_secure_boot_state(self, secure_boot_enable):
        """Enable/Disable secure boot on the server """
        #Prerequiste to enable secure boot - enable UEFIOptimizedBoot
        if secure_boot_enable:
            self._change_bios_setting('UefiOptimizedBoot', "Enabled")
        
        self._change_secure_boot_settings('SecureBootEnable', secure_boot_enable)
        
    def reset_secure_boot_keys(self):
        """ Reset secure boot keys to manufacturing defaults """
        self._change_secure_boot_settings('ResetToDefaultKeys', True)
        
    def clear_secure_boot_keys(self):
        """ Reset all keys """
        self._change_secure_boot_settings('ResetAllKeys', True)
                    
    def get_host_power_status(self):
        """Request the power state of the server.
        """
        data = self._get_host_details()
        return data['Power'].upper()

    def get_current_boot_mode(self):
        """Retrieves the current boot mode of the server."""
        boot_mode = self._get_bios_setting('BootMode')
        if boot_mode == 'LegacyBios':
            boot_mode = 'legacy'
        
        return boot_mode.upper()
    
    def set_pending_boot_mode(self, mode):
        """Configures the boot mode of the system from a specific boot mode."""
        if mode == 'bios':
            mode = 'LegacyBios'
        self._change_bios_setting('BootMode', mode)
