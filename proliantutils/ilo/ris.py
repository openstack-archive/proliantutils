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

__author__ = 'HP'

import base64
import gzip
import hashlib
import json

import six
from six.moves import http_client
from six.moves.urllib import parse as urlparse

from proliantutils import exception
from proliantutils.ilo import common
from proliantutils.ilo import operations

""" Currently this class supports only secure boot and firmware settings
related API's .

TODO : Add rest of the API's that exists in RIBCL. """


class RISOperations(operations.IloOperations):

    def __init__(self, host, login, password, bios_password=None):
        self.host = host
        self.login = login
        self.password = password
        self.bios_password = bios_password
        # Message registry support
        self.message_registries = {}

    def _rest_op(self, operation, suburi, request_headers, request_body):
        """Generic REST Operation handler."""

        url = urlparse.urlparse('https://' + self.host + suburi)
        # Used for logging on redirection error.
        start_url = url.geturl()

        if request_headers is None:
            request_headers = dict()

        # Use self.login/self.password and Basic Auth
        if self.login is not None and self.password is not None:
            auth_data = self.login + ":" + self.password
            hr = "BASIC " + base64.b64encode(
                auth_data.encode('ascii')).decode("utf-8")
            request_headers['Authorization'] = hr

        redir_count = 5
        while redir_count:
            conn = None
            if url.scheme == 'https':
                conn = http_client.HTTPSConnection(host=url.netloc,
                                                   strict=True)
            elif url.scheme == 'http':
                conn = http_client.HTTPConnection(host=url.netloc,
                                                  strict=True)

            try:
                conn.request(operation, url.path, headers=request_headers,
                             body=json.dumps(request_body))
                resp = conn.getresponse()
                body = resp.read()
            except Exception as e:
                raise exception.IloConnectionError(e)

            # NOTE:Do not assume every HTTP operation will return a JSON body.
            # For example, ExtendedError structures are only required for
            # HTTP 400 errors and are optional elsewhere as they are mostly
            # redundant for many of the other HTTP status code. In particular,
            # 200 OK responses should not have to return any body.

            # NOTE:  this makes sure the headers names are all lower cases
            # because HTTP says they are case insensitive
            headers = dict((x.lower(), y) for x, y in resp.getheaders())

            # Follow HTTP redirect
            if resp.status == 301 and 'location' in headers:
                url = urlparse.urlparse(headers['location'])
                redir_count -= 1
            else:
                break
        else:
            # Redirected for 5th time. Throw error
            msg = ("URL Redirected 5 times continuously. "
                   "URL incorrect: %s" % start_url)
            raise exception.IloConnectionError(msg)

        response = dict()
        try:
            if body:
                response = json.loads(body)
        except (ValueError, TypeError):
            # if it doesn't decode as json
            # NOTE:  resources may return gzipped content
            # try to decode as gzip (we should check the headers for
            # Content-Encoding=gzip)
            try:
                gzipper = gzip.GzipFile(fileobj=six.BytesIO(body))
                uncompressed_string = gzipper.read().decode('UTF-8')
                response = json.loads(uncompressed_string)
            except Exception as e:
                raise exception.IloError(e)

        return resp.status, headers, response

    def _rest_get(self, suburi, request_headers=None):
        """REST GET operation.

        HTTP response codes could be 500, 404 etc.
        """
        return self._rest_op('GET', suburi, request_headers, None)

    def _rest_patch(self, suburi, request_headers, request_body):
        """REST PATCH operation.

        HTTP response codes could be 500, 404, 202 etc.
        """
        if not isinstance(request_headers, dict):
            request_headers = dict()
        request_headers['Content-Type'] = 'application/json'
        return self._rest_op('PATCH', suburi, request_headers, request_body)

    def _rest_put(self, suburi, request_headers, request_body):
        """REST PUT operation.

        HTTP response codes could be 500, 404, 202 etc.
        """
        if not isinstance(request_headers, dict):
            request_headers = dict()
        request_headers['Content-Type'] = 'application/json'
        return self._rest_op('PUT', suburi, request_headers, request_body)

    def _rest_post(self, suburi, request_headers, request_body):
        """REST POST operation.

        The response body after the operation could be the new resource, or
        ExtendedError, or it could be empty.
        """
        if not isinstance(request_headers, dict):
            request_headers = dict()
        request_headers['Content-Type'] = 'application/json'
        return self._rest_op('POST', suburi, request_headers, request_body)

    def _rest_delete(self, suburi, request_headers):
        """REST DELETE operation.

        HTTP response codes could be 500, 404 etc.
        """
        return self._rest_op('DELETE', suburi, request_headers, None)

    def _get_collection(self, collection_uri, request_headers=None):
        """Generator function that returns collection members."""

        # get the collection
        status, headers, thecollection = self._rest_get(collection_uri)

        if status != 200:
            msg = self._get_extended_error(thecollection)
            raise exception.IloError(msg)

        while status < 300:
            # verify expected type
            # Don't limit to version 0 here as we will rev to 1.0 at some
            # point hopefully with minimal changes
            ctype = self._get_type(thecollection)
            if (ctype not in ['Collection.0', 'Collection.1']):
                raise exception.IloError("collection not found")

            # if this collection has inline items, return those
            # NOTE:  Collections are very flexible in how the represent
            # members.  They can be inline in the collection as members
            # of the 'Items' array, or they may be href links in the
            # links/Members array.  The could actually be both. Typically,
            # iLO implements the inline (Items) for only when the collection
            # is read only.  We have to render it with the href links when an
            # array contains PATCHable items because its complex to PATCH
            # inline collection members.

            if 'Items' in thecollection:
                # iterate items
                for item in thecollection['Items']:
                    # if the item has a self uri pointer,
                    # supply that for convenience.
                    memberuri = None
                    if 'links' in item and 'self' in item['links']:
                        memberuri = item['links']['self']['href']
                    yield 200, None, item, memberuri

            # else walk the member links
            elif ('links' in thecollection and
                  'Member' in thecollection['links']):
                # iterate members
                for memberuri in thecollection['links']['Member']:
                    # for each member return the resource indicated by the
                    # member link
                    status, headers, member = self._rest_get(memberuri['href'])
                    yield status, headers, member, memberuri['href']

            # page forward if there are more pages in the collection
            if ('links' in thecollection and
                    'NextPage' in thecollection['links']):
                next_link_uri = (collection_uri + '?page=' + str(
                                 thecollection['links']['NextPage']['page']))
                status, headers, thecollection = self._rest_get(next_link_uri)

            # else we are finished iterating the collection
            else:
                break

    def _get_type(self, obj):
        """Return the type of an object."""
        typever = obj['Type']
        typesplit = typever.split('.')
        return typesplit[0] + '.' + typesplit[1]

    def _operation_allowed(self, headers_dict, operation):
        """Checks if specified operation is allowed on the resource."""

        if 'allow' in headers_dict:
            if operation in headers_dict['allow']:
                return True
        return False

    def _render_extended_error_message_list(self, extended_error):
        """Parse the ExtendedError object and retruns the message.

        Build a list of decoded messages from the extended_error using the
        message registries. An ExtendedError JSON object is a response from
        the with its own schema.  This function knows how to parse the
        ExtendedError object and, using any loaded message registries,
        render an array of plain language strings that represent
        the response.
        """
        messages = []
        if isinstance(extended_error, dict):
            if ('Type' in extended_error and
                    extended_error['Type'].startswith('ExtendedError.')):
                for msg in extended_error['Messages']:
                    message_id = msg['MessageID']
                    x = message_id.split('.')
                    registry = x[0]
                    msgkey = x[len(x) - 1]

                    # if the correct message registry is loaded,
                    # do string resolution
                    if (registry in self.message_registries and msgkey in
                            self.message_registries[registry]['Messages']):
                        rmsgs = self.message_registries[registry]['Messages']
                        msg_dict = rmsgs[msgkey]
                        msg_str = message_id + ':  ' + msg_dict['Message']

                        for argn in range(0, msg_dict['NumberOfArgs']):
                            subst = '%' + str(argn+1)
                            m = str(msg['MessageArgs'][argn])
                            msg_str = msg_str.replace(subst, m)

                        if ('Resolution' in msg_dict and
                                msg_dict['Resolution'] != 'None'):
                            msg_str += '  ' + msg_dict['Resolution']

                        messages.append(msg_str)
                    else:
                        # no message registry, simply return the msg object
                        # in string form
                        messages.append(str(message_id))

        return messages

    def _get_extended_error(self, extended_error):
        """Gets the list of decoded messages from the extended_error."""
        return self._render_extended_error_message_list(extended_error)

    def _get_host_details(self):
        """Get the system details."""
        # Assuming only one system present as part of collection,
        # as we are dealing with iLO's here.
        status, headers, system = self._rest_get('/rest/v1/Systems/1')
        if status < 300:
            stype = self._get_type(system)
            if stype not in ['ComputerSystem.0', 'ComputerSystem.1']:
                msg = "%s is not a valid system type " % stype
                raise exception.IloError(msg)
        else:
            msg = self._get_extended_error(system)
            raise exception.IloError(msg)

        return system

    def _check_bios_resource(self, properties=[]):
        """Check if the bios resource exists."""

        system = self._get_host_details()
        if ('links' in system['Oem']['Hp'] and
                'BIOS' in system['Oem']['Hp']['links']):
            # Get the BIOS URI and Settings
            bios_uri = system['Oem']['Hp']['links']['BIOS']['href']
            status, headers, bios_settings = self._rest_get(bios_uri)

            if status >= 300:
                msg = self._get_extended_error(bios_settings)
                raise exception.IloError(msg)

            # If property is not None, check if the bios_property is supported
            for property in properties:
                if property not in bios_settings:
                    # not supported on this platform
                    msg = ('BIOS Property "' + property + '" is not'
                           ' supported on this system.')
                    raise exception.IloCommandNotSupportedError(msg)

            return headers, bios_uri, bios_settings

        else:
            msg = ('"links/BIOS" section in ComputerSystem/Oem/Hp'
                   ' does not exist')
            raise exception.IloCommandNotSupportedError(msg)

    def _get_bios_settings_resource(self, data):
        """Get the BIOS settings resource."""
        try:
            bios_settings_uri = data['links']['Settings']['href']
        except KeyError:
            msg = ('BIOS Settings resource not found.')
            raise exception.IloError(msg)

        status, headers, bios_settings = self._rest_get(bios_settings_uri)
        if status != 200:
            msg = self._get_extended_error(bios_settings)
            raise exception.IloError(msg)

        return headers, bios_settings_uri, bios_settings

    def _validate_if_patch_supported(self, headers, uri):
        """Check if the PATCH Operation is allowed on the resource."""
        if not self._operation_allowed(headers, 'PATCH'):
                msg = ('PATCH Operation not supported on the resource '
                       '"%s"' % uri)
                raise exception.IloError(msg)

    def _get_bios_setting(self, bios_property):
        """Retrieves bios settings of the server."""
        headers, bios_uri, bios_settings = self._check_bios_resource([
            bios_property])
        return bios_settings[bios_property]

    def _get_bios_hash_password(self, bios_password):
        """Get the hashed BIOS password."""
        request_headers = dict()
        if bios_password:
            bios_password_hash = hashlib.sha256((bios_password.encode()).
                                                hexdigest().upper())
            request_headers['X-HPRESTFULAPI-AuthToken'] = bios_password_hash
        return request_headers

    def _change_bios_setting(self, properties):
        """Change the bios settings to specified values."""
        keys = properties.keys()
        # Check if the BIOS resource/property exists.
        headers, bios_uri, settings = self._check_bios_resource(keys)
        if not self._operation_allowed(headers, 'PATCH'):
            headers, bios_uri, _ = self._get_bios_settings_resource(settings)
            self._validate_if_patch_supported(headers, bios_uri)

        request_headers = self._get_bios_hash_password(self.bios_password)
        status, headers, response = self._rest_patch(bios_uri, request_headers,
                                                     properties)
        if status >= 300:
            msg = self._get_extended_error(response)
            raise exception.IloError(msg)

    def _get_iscsi_settings_resource(self, data):
        """Get the iscsi settings resoure.

        :param data: Existing iscsi settings of the server.
        :returns: headers, iscsi_settings url and
                 iscsi settings as a dictionary.
        :raises: IloCommandNotSupportedError, if resource is not found.
        :raises: IloError, on an error from iLO.
        """
        try:
            iscsi_settings_uri = data['links']['Settings']['href']
        except KeyError:
            msg = ('iscsi settings resource not found.')
            raise exception.IloCommandNotSupportedError(msg)

        status, headers, iscsi_settings = self._rest_get(iscsi_settings_uri)

        if status != 200:
            msg = self._get_extended_error(iscsi_settings)
            raise exception.IloError(msg)

        return headers, iscsi_settings_uri, iscsi_settings

    def _get_bios_boot_resource(self, data):
        """Get the Boot resource like BootSources.

        :param data: Existing Bios settings of the server.
        :returns: boot settings.
        :raises: IloCommandNotSupportedError, if resource is not found.
        :raises: IloError, on an error from iLO.
        """
        try:
            boot_uri = data['links']['Boot']['href']
        except KeyError:
            msg = ('Boot resource not found.')
            raise exception.IloCommandNotSupportedError(msg)

        status, headers, boot_settings = self._rest_get(boot_uri)

        if status != 200:
            msg = self._get_extended_error(boot_settings)
            raise exception.IloError(msg)

        return boot_settings

    def _get_bios_mappings_resource(self, data):
        """Get the Mappings resource.

        :param data: Existing Bios settings of the server.
        :returns: mappings settings.
        :raises: IloCommandNotSupportedError, if resource is not found.
        :raises: IloError, on an error from iLO.
        """
        try:
            map_uri = data['links']['Mappings']['href']
        except KeyError:
            msg = ('Mappings resource not found.')
            raise exception.IloCommandNotSupportedError(msg)

        status, headers, map_settings = self._rest_get(map_uri)
        if status != 200:
            msg = self._get_extended_error(map_settings)
            raise exception.IloError(msg)

        return map_settings

    def _check_iscsi_rest_patch_allowed(self):
        """Checks if patch is supported on iscsi.

        :returns: iscsi url.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """

        headers, bios_uri, bios_settings = self._check_bios_resource()
        # Check if the bios resource exists.

        if('links' in bios_settings and 'iScsi' in bios_settings['links']):
            iscsi_uri = bios_settings['links']['iScsi']['href']
            status, headers, settings = self._rest_get(iscsi_uri)

            if status != 200:
                msg = self._get_extended_error(settings)
                raise exception.IloError(msg)

            if not self._operation_allowed(headers, 'PATCH'):
                headers, iscsi_uri, settings = (
                    self._get_iscsi_settings_resource(settings))
                self._validate_if_patch_supported(headers, iscsi_uri)

            return iscsi_uri

        else:
            msg = ('"links/iScsi" section in bios'
                   ' does not exist')
            raise exception.IloCommandNotSupportedError(msg)

    def _change_iscsi_settings(self, mac, iscsi_info):
        """Change iscsi settings.

        :param mac: MAC address of the initiator.
        :param iscsi_info: A dictionary that contains information of iscsi
                           target like target_name, lun, ip_address, port etc.
        :raises: IloInvalidInputError, if mac provided is invalid.
        :raises: IloError, on an error from iLO.
        """
        headers, bios_uri, bios_settings = self._check_bios_resource()
        # Get the Boot resource and Mappings resource.
        map_settings = self._get_bios_mappings_resource(bios_settings)
        boot_settings = self._get_bios_boot_resource(bios_settings)
        correlatable_id = None
        for boot_setting in boot_settings['BootSources']:
            if(mac in boot_setting['UEFIDevicePath']):
                correlatable_id = boot_setting['CorrelatableID']
                break

        if not correlatable_id:
            msg = ('MAC provided is Invalid')
            raise exception.IloInvalidInputError(msg)

        nic = None
        # Get the NIC for the particular mac provided.
        for map_setting in map_settings['BiosPciSettingsMappings']:
            sub_instances = map_setting['Subinstances']
            if sub_instances:
                for sub_instance in sub_instances:
                    if(sub_instance['CorrelatableID'] ==
                       correlatable_id):
                        # The nic is in the format 'NicBoot1' or 'NicBoot2'
                        nic = sub_instance['Associations'][0]
                        break
                if nic is not None:
                    break

        if not nic:
            msg = ('MAC does not have any corresponding mapping')
            raise exception.IloError(msg)

        iscsi_uri = self._check_iscsi_rest_patch_allowed()
        iscsi_info['iSCSIBootAttemptName'] = nic
        iscsi_info['iSCSINicSource'] = nic
        iscsi_info['iSCSIBootAttemptInstance'] = 1
        iscsi_info['iSCSIBootEnable'] = 'Enabled'
        patch_data = {'iSCSIBootSources': [iscsi_info]}
        status, headers, response = self._rest_patch(iscsi_uri,
                                                     None, patch_data)
        if status >= 300:
            msg = self._get_extended_error(response)
            raise exception.IloError(msg)

    def _change_secure_boot_settings(self, property, value):
        """Change secure boot settings on the server."""
        system = self._get_host_details()
        # find the BIOS URI
        if ('links' not in system['Oem']['Hp'] or
           'SecureBoot' not in system['Oem']['Hp']['links']):
            msg = (' "SecureBoot" resource or feature is not '
                   'supported on this system')
            raise exception.IloCommandNotSupportedError(msg)

        secure_boot_uri = system['Oem']['Hp']['links']['SecureBoot']['href']

        # Change the property required
        new_secure_boot_settings = dict()
        new_secure_boot_settings[property] = value

        # perform the patch
        status, headers, response = self._rest_patch(
            secure_boot_uri, None, new_secure_boot_settings)

        if status >= 300:
            msg = self._get_extended_error(response)
            raise exception.IloError(msg)

        # Change the bios setting as a workaround to enable secure boot
        # Can be removed when fixed for Gen9 snap2
        val = self._get_bios_setting('CustomPostMessage')
        val = val.rstrip() if val.endswith(" ") else val+" "
        self._change_bios_setting({'CustomPostMessage': val})

    def _validate_uefi_boot_mode(self):
        """Checks if the system is in uefi boot mode.

        :return: 'True' if the boot mode is uefi else 'False'
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        boot_mode = self.get_current_boot_mode()
        if boot_mode == 'UEFI':
            return True
        else:
            return False

    def get_product_name(self):
        """Gets the product name of the server.

        :returns: server model name.
        :raises: IloError, on an error from iLO.
        """
        system = self._get_host_details()
        return system['Model']

    def get_secure_boot_mode(self):
        """Get the status of secure boot.

        :returns: True, if enabled, else False
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        system = self._get_host_details()

        if ('links' not in system['Oem']['Hp'] or
           'SecureBoot' not in system['Oem']['Hp']['links']):
            msg = ('"SecureBoot" resource or feature is not supported'
                   ' on this system')
            raise exception.IloCommandNotSupportedError(msg)

        secure_boot_uri = system['Oem']['Hp']['links']['SecureBoot']['href']

        # get the Secure Boot object
        status, headers, secure_boot_settings = self._rest_get(secure_boot_uri)

        if status >= 300:
            msg = self._get_extended_error(secure_boot_settings)
            raise exception.IloError(msg)

        return secure_boot_settings['SecureBootCurrentState']

    def set_secure_boot_mode(self, secure_boot_enable):
        """Enable/Disable secure boot on the server.

        :param secure_boot_enable: True, if secure boot needs to be
               enabled for next boot, else False.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        self._change_secure_boot_settings('SecureBootEnable',
                                          secure_boot_enable)

    def reset_secure_boot_keys(self):
        """Reset secure boot keys to manufacturing defaults.

        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        self._change_secure_boot_settings('ResetToDefaultKeys', True)

    def clear_secure_boot_keys(self):
        """Reset all keys.

        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        self._change_secure_boot_settings('ResetAllKeys', True)

    def get_host_power_status(self):
        """Request the power state of the server.

        :returns: Power State of the server, 'ON' or 'OFF'
        :raises: IloError, on an error from iLO.
        """

        data = self._get_host_details()
        return data['Power'].upper()

    def get_http_boot_url(self):
        """Request the http boot url from system in uefi boot mode.

        :returns: URL for http boot
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedInBiosError, if the system is
                 in the bios boot mode.
        """
        if(self._validate_uefi_boot_mode() is True):
            return self._get_bios_setting('UefiShellStartupUrl')
        else:
            msg = 'get_http_boot_url is not supported in the BIOS boot mode'
            raise exception.IloCommandNotSupportedInBiosError(msg)

    def set_http_boot_url(self, url):
        """Set url to the UefiShellStartupUrl to the system in uefi boot mode.

        :param url: URL for http boot
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedInBiosError, if the system is
                 in the bios boot mode.
        """
        if(self._validate_uefi_boot_mode() is True):
            self._change_bios_setting({'UefiShellStartupUrl': url})
        else:
            msg = 'set_http_boot_url is not supported in the BIOS boot mode'
            raise exception.IloCommandNotSupportedInBiosError(msg)

    def set_iscsi_boot_info(self, mac, target_name, lun, ip_address,
                            port='3260', auth_method=None, username=None,
                            password=None):
        """Set iscsi details of the system in uefi boot mode.

        The iSCSI initiator is identified by the MAC provided.
        The initiator system is set with the target details like
        IQN, LUN, IP, Port etc.
        :param mac: MAC address of initiator.
        :param target_name: Target Name for iscsi.
        :param lun: logical unit number.
        :param ip_address: IP address of the target.
        :param port: port of the target.
        :param auth_method : either None or CHAP.
        :param username: CHAP Username for authentication.
        :param password: CHAP secret.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedInBiosError, if the system is
                 in the bios boot mode.
        """
        if(self._validate_uefi_boot_mode() is True):
            iscsi_info = dict()
            iscsi_info['iSCSITargetName'] = target_name
            iscsi_info['iSCSIBootLUN'] = lun
            iscsi_info['iSCSITargetIpAddress'] = ip_address
            iscsi_info['iSCSITargetTcpPort'] = int(port)
            if (auth_method == 'CHAP'):
                iscsi_info['iSCSIAuthenticationMethod'] = 'Chap'
                iscsi_info['iSCSIChapUsername'] = username
                iscsi_info['iSCSIChapSecret'] = password
            self._change_iscsi_settings(mac.upper(), iscsi_info)
        else:
            msg = 'iscsi boot is not supported in the BIOS boot mode'
            raise exception.IloCommandNotSupportedInBiosError(msg)

    def get_current_boot_mode(self):
        """Retrieves the current boot mode of the server.

        :returns: Current boot mode, LEGACY or UEFI.
        :raises: IloError, on an error from iLO.
        """
        boot_mode = self._get_bios_setting('BootMode')
        if boot_mode == 'LegacyBios':
            boot_mode = 'legacy'

        return boot_mode.upper()

    def get_pending_boot_mode(self):
        """Retrieves the pending boot mode of the server.

        Gets the boot mode to be set on next reset.
        :returns: either LEGACY or UEFI.
        :raises: IloError, on an error from iLO.
        """
        headers, uri, bios_settings = self._check_bios_resource(['BootMode'])
        _, _, settings = self._get_bios_settings_resource(bios_settings)
        boot_mode = settings.get('BootMode')
        if boot_mode == 'LegacyBios':
            boot_mode = 'legacy'
        return boot_mode.upper()

    def set_pending_boot_mode(self, boot_mode):
        """Sets the boot mode of the system for next boot.

        :param boot_mode: either 'uefi' or 'legacy'.
        :raises: IloInvalidInputError, on an invalid input.
        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        boot_mode = boot_mode.lower()
        if boot_mode not in ['uefi', 'legacy']:
            msg = 'Invalid Boot mode specified'
            raise exception.IloInvalidInputError(msg)

        boot_properties = {'BootMode': boot_mode}

        if boot_mode == 'legacy':
            boot_properties['BootMode'] = 'LegacyBios'
        else:
            # If Boot Mode is 'Uefi' set the UEFIOptimizedBoot first.
            boot_properties['UefiOptimizedBoot'] = "Enabled"

        # Change the Boot Mode
        self._change_bios_setting(boot_properties)

    def reset_ilo_credential(self, password):
        """Resets the iLO password.

        :param password: The password to be set.
        :raises: IloError, if account not found or on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        acc_uri = '/rest/v1/AccountService/Accounts'

        for status, hds, account, memberuri in self._get_collection(acc_uri):
            if account['UserName'] == self.login:
                mod_user = {}
                mod_user['Password'] = password
                status, headers, response = self._rest_patch(memberuri,
                                                             None, mod_user)
                if status != 200:
                    msg = self._get_extended_error(response)
                    raise exception.IloError(msg)
                return

        msg = "iLO Account with specified username is not found."
        raise exception.IloError(msg)

    def _get_ilo_details(self):
        """Gets iLO details

        :raises: IloError, on an error from iLO.
        :raises: IloConnectionError, if iLO is not up after reset.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        reset_uri = '/rest/v1/Managers/1'
        status, headers, manager = self._rest_get(reset_uri)

        if status != 200:
            msg = self._get_extended_error(manager)
            raise exception.IloError(msg)

        # verify expected type
        mtype = self._get_type(manager)
        if (mtype not in ['Manager.0', 'Manager.1']):
            msg = "%s is not a valid Manager type " % mtype
            raise exception.IloError(msg)

        return manager, reset_uri

    def reset_ilo(self):
        """Resets the iLO.

        :raises: IloError, on an error from iLO.
        :raises: IloConnectionError, if iLO is not up after reset.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        manager, reset_uri = self._get_ilo_details()
        action = {'Action': 'Reset'}

        # perform the POST
        status, headers, response = self._rest_post(reset_uri, None, action)

        if(status != 200):
            msg = self._get_extended_error(response)
            raise exception.IloError(msg)

        # Check if the iLO is up again.
        common.wait_for_ilo_after_reset(self)

    def reset_bios_to_default(self):
        """Resets the BIOS settings to default values.

        :raises: IloError, on an error from iLO.
        :raises: IloCommandNotSupportedError, if the command is not supported
                 on the server.
        """
        # Check if the BIOS resource if exists.
        headers_bios, bios_uri, bios_settings = self._check_bios_resource()
        # Get the BaseConfig resource.
        try:
            base_config_uri = bios_settings['links']['BaseConfigs']['href']
        except KeyError:
            msg = ("BaseConfigs resource not found. Couldn't apply the BIOS "
                   "Settings.")
            raise exception.IloCommandNotSupportedError(msg)

        # Check if BIOS resource supports patch, else get the settings
        if not self._operation_allowed(headers_bios, 'PATCH'):
            headers, bios_uri, _ = self._get_bios_settings_resource(
                bios_settings)
            self._validate_if_patch_supported(headers, bios_uri)

        status, headers, config = self._rest_get(base_config_uri)
        if status != 200:
            msg = self._get_extended_error(config)
            raise exception.IloError(msg)

        new_bios_settings = {}
        for cfg in config['BaseConfigs']:
            default_settings = cfg.get('default', None)
            if default_settings is not None:
                new_bios_settings = default_settings
                break
        else:
            msg = ("Default Settings not found in 'BaseConfigs' resource.")
            raise exception.IloCommandNotSupportedError(msg)
        request_headers = self._get_bios_hash_password(self.bios_password)
        status, headers, response = self._rest_patch(bios_uri, request_headers,
                                                     new_bios_settings)
        if status >= 300:
            msg = self._get_extended_error(response)
            raise exception.IloError(msg)

    def _get_ilo_firmware_version(self):
        """Gets the ilo firmware version for server capabilities

        :returns: a dictionary of iLO firmware version.

        """

        manager, reset_uri = self._get_ilo_details()
        ilo_firmware_version = manager['Firmware']['Current']['VersionString']
        return {'ilo_firmware_version': ilo_firmware_version}

    def get_server_capabilities(self):
        """Gets server properties which can be used for scheduling

        :returns: a dictionary of hardware properties like firmware
                  versions, server model.
        :raises: IloError, if iLO returns an error in command execution.

        """
        capabilities = {}
        system = self._get_host_details()
        capabilities['server_model'] = system['Model']
        rom_firmware_version = (
            system['Oem']['Hp']['Bios']['Current']['VersionString'])
        capabilities['rom_firmware_version'] = rom_firmware_version
        capabilities.update(self._get_ilo_firmware_version())
        try:
            self.get_secure_boot_mode()
            capabilities['secure_boot'] = 'true'
        except exception.IloCommandNotSupportedError:
            # If an error is raised dont populate the capability
            # secure_boot
            pass
        return capabilities
