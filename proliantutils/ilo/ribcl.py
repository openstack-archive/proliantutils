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


"""Provides iLO management interface. Talks to the iLO management engine
over RIBCL scripting language
"""

import re
import six
import urllib2
import xml.etree.ElementTree as etree


POWER_STATE = {
    'ON': 'Yes',
    'OFF': 'No',
}


class IloError(Exception):
    """This exception is used when a problem is encountered in
    executing an operation on the iLO
    """
    def __init__(self, message, errorcode=None):
        super(IloError, self).__init__(message)


class IloClientInternalError(IloError):
    """This exception is raised when iLO client library fails to
    communicate properly with the iLO
    """
    def __init__(self, message, errorcode=None):
        super(IloError, self).__init__(message)


class IloLoginFailError(IloError):
    """This exception is used to communicate a login failure to
    the caller.
    """
    messages = ['User login name was not found',
                    'Login failed', 'Login credentials rejected']
    statuses = [0x005f, 0x000a]


class IloConnectionError(IloError):
    """This exception is used to communicate an HTTP connection
    error from the iLO to the caller.
    """
    def __init__(self, message):
        super(IloConnectionError, self).__init__(message)


class IloInvalidInputError(IloError):
    """This exception is used when invalid inputs are passed to
    the APIs exposed by this module.
    """
    def __init__(self, message):
        super(IloInvalidInputError, self).__init__(message)


class IloClient:
    """iLO class for RIBCL interface for iLO.

    This class provides an OO interface for retrieving information
    and managing iLO. This class currently uses RIBCL scripting
    language to talk to the iLO. It implements the same interface in
    python as described in HP iLO 4 Scripting and Command Line Guide.
    """
    def __init__(self, host, login, password, timeout=60, port=443):
        self.host = host
        self.login = login
        self.password = password
        self.timeout = timeout
        self.port = port

    def _request_ilo(self, root):
        """This function sends the XML request to the ILO and
        receives the output from ILO.

        :raises: IloConnectionError() if
        unable to send the request.
        """
        if self.port:
            urlstr = 'https://%s:%d/ribcl' % (self.host, self.port)
        else:
            urlstr = 'https://%s/ribcl' % (self.host)
        xml = self._serialize_xml(root)
        try:
            req = urllib2.Request(url=urlstr, data=xml)
            req.add_header("Content-length", len(xml))
            data = urllib2.urlopen(req).read()
        except (ValueError, urllib2.URLError, urllib2.HTTPError) as e:
            raise IloConnectionError(e)
        return data

    def _create_dynamic_xml(self, cmdname, tag_name, mode, subelements=None):
        """This function creates the dynamic xml required to be sent
        to the ILO for all the APIs.

        :param cmdname: the API which needs to be implemented.
        :param tag_name: the tag info under which ILO has defined
                         the particular API.
        :param mode: 'read' or 'write'
        :param subelements: dictionary containing subelements of the
                            particular API tree.
        :returns: the etree.Element for the root of the RIBCL XML

        """
        root = etree.Element('RIBCL', VERSION="2.0")
        login = etree.SubElement(
            root, 'LOGIN', USER_LOGIN=self.login, PASSWORD=self.password)
        tagname = etree.SubElement(login, tag_name, MODE=mode)
        subelements = subelements or {}

        etree.SubElement(tagname, cmdname)

        if six.PY2:
            root_iterator = root.getiterator(cmdname)
        else:
            root_iterator = root.iter(cmdname)

        for cmd in root_iterator:
            for key, value in subelements.items():
                cmd.set(key, value)

        return root

    def _serialize_xml(self, root):
        """It serializes the dynamic xml created and converts
        it to a string. This is done before sending the
        xml to the ILO.

        :param root: root of the dynamic xml.
        """
        if hasattr(etree, 'tostringlist'):
            xml = '\r\n'.join(etree.tostringlist(root)) + '\r\n'
        else:
            xml = etree.tostring(root) + '\r\n'
        return xml

    def _parse_output(self, xml_response):
        """This function parses the output received from ILO.
        As the output contains multiple XMLs, it extracts
        one xml at a time and loops over till all the xmls
        in the response are exhausted.

        It returns the data to APIs either in dictionary
        format or as the string.
        It creates the dictionary only if the Ilo response
        contains the data under the requested RIBCL command.
        If the Ilo response contains only the string,
        then the string is returned back.

        """
        count = 0
        xml_dict = {}
        resp_message = None
        xml_start_pos = []
        for m in re.finditer(r"\<\?xml", xml_response):
            xml_start_pos.append(m.start())
        while count < len(xml_start_pos):
            if (count == len(xml_start_pos) - 1):
                result = xml_response[xml_start_pos[count]:]
            else:
                result = \
                    xml_response[xml_start_pos[count]:
                        xml_start_pos[count + 1]]
            result = result.strip()
            message = etree.fromstring(result)
            resp = self._validate_message(message)
            if hasattr(resp, 'tag'):
                xml_dict = self._elementtree_to_dict(resp)
            elif resp is not None:
                resp_message = resp
            count = count + 1

        if xml_dict:
            return xml_dict
        elif resp_message is not None:
            return resp_message

    def _elementtree_to_dict(self, element):
        """Converts the actual response from the ILO for an API
        to the dictionary.
        """
        node = dict()
        text = getattr(element, 'text')
        if text is not None:
            text = text.strip()
            if len(text) != 0:
                node['text'] = text
        node.update(element.items())  # element's attributes
        child_nodes = {}
        for child in element:  # element's children
            child_nodes.setdefault(child.tag, []).append(
                self._elementtree_to_dict(child))
        # convert all single-element lists into non-lists
        for key, value in child_nodes.items():
            if len(value) == 1:
                child_nodes[key] = value[0]
        node.update(child_nodes.items())
        return node

    def _validate_message(self, message):
        """This function validates the XML response to see
        if the exit status is 0 or not in the response.
        If the status is non-zero it raises exception.
        """
        if message.tag != 'RIBCL':
            # the true case shall be unreachable for response
            # XML from Ilo as all messages are tagged with RIBCL
            # but still raise an exception if any invalid
            # XML response is returned by Ilo. Set status to some
            # arbitary non-zero value.
            status = -1
            raise IloClientInternalError(message, status)

        for child in message:
            if child.tag != 'RESPONSE':
                return message
            status = int(child.get('STATUS'), 16)
            msg = child.get('MESSAGE')
            if status == 0 and msg != 'No error':
                return msg
            if status != 0:
                if 'syntax error' in msg:
                    raise IloClientInternalError(msg, status)
                if status in IloLoginFailError.statuses or \
                        msg in IloLoginFailError.messages:
                    raise IloLoginFailError(msg, status)
                raise IloError(msg, status)

    def _execute_command(self, create_command, tag_info, mode, dic={}):
        """Common infrastructure used by all APIs to send/get
        response from ILO.
        """
        xml = self._create_dynamic_xml(
            create_command, tag_info, mode, dic)
        d = self._request_ilo(xml)
        data = self._parse_output(d)
        return data

    def get_all_licenses(self):
        """Retrieve license type, key, installation date, etc."""
        data = self._execute_command('GET_ALL_LICENSES', 'RIB_INFO', 'read')
        d = {}
        for key, val in data['GET_ALL_LICENSES']['LICENSE'].items():
            if isinstance(val, dict):
                d[key] = data['GET_ALL_LICENSES']['LICENSE'][key]['VALUE']
        return d

    def get_host_power_status(self):
        """Request the power state of the server.
        """
        data = self._execute_command(
            'GET_HOST_POWER_STATUS', 'SERVER_INFO', 'read')
        return data['GET_HOST_POWER']['HOST_POWER']

    def get_one_time_boot(self):
        """Retrieves the current setting for the one time boot."""
        data = self._execute_command(
            'GET_ONE_TIME_BOOT', 'SERVER_INFO', 'read')
        return data['ONE_TIME_BOOT']['BOOT_TYPE']['VALUE']

    def get_vm_status(self, device='FLOPPY'):
        """Returns the virtual media drive status like url, is connected, etc.
        """
        dic = {'DEVICE': device.upper()}
        data = self._execute_command(
            'GET_VM_STATUS', 'RIB_INFO', 'read', dic)
        return data['GET_VM_STATUS']

    def reset_server(self):
        """Resets the server."""
        data = self._execute_command('RESET_SERVER', 'SERVER_INFO', 'write')
        return data

    def press_pwr_btn(self):
        """Simulates a physical press of the server power button."""
        data = self._execute_command('PRESS_PWR_BTN', 'SERVER_INFO', 'write')
        return data

    def hold_pwr_btn(self):
        """Simulate a physical press and hold of the server power button."""
        dic = {'TOGGLE': 'NO'}
        data = self._execute_command(
            'HOLD_PWR_BTN', 'SERVER_INFO', 'write', dic)
        return data

    def set_host_power(self, power):
        """Toggle the power button of server.
        : param power : 'ON' or 'OFF'
        """
        if power.upper() in POWER_STATE:
            dic = {'HOST_POWER': POWER_STATE[power.upper()]}
            data = self._execute_command(
                'SET_HOST_POWER', 'SERVER_INFO', 'write', dic)
            return data
        else:
            raise IloInvalidInputError(
                "Invalid input. The expected input is ON or OFF.")

    def set_one_time_boot(self, value):
        """Configures a single boot from a specific device."""
        dic = {'value': value}
        data = self._execute_command(
            'SET_ONE_TIME_BOOT', 'SERVER_INFO', 'write', dic)
        return data

    def insert_virtual_media(self, url, device='FLOPPY'):
        """Notifies iLO of the location of a virtual media diskette image."""
        dic = {
            'DEVICE': device.upper(),
            'IMAGE_URL': url,
        }
        data = self._execute_command(
            'INSERT_VIRTUAL_MEDIA', 'RIB_INFO', 'write', dic)
        return data

    def eject_virtual_media(self, device='FLOPPY'):
        """Ejects the Virtual Media image if one is inserted."""
        dic = {'DEVICE': device.upper()}
        data = self._execute_command(
            'EJECT_VIRTUAL_MEDIA', 'RIB_INFO', 'write', dic)
        return data

    def set_vm_status(self, device='FLOPPY',
                      boot_option='BOOT_ONCE', write_protect='YES'):
        """Sets the Virtual Media drive status and allows the
        boot options for booting from the virtual media.
        """
        dic = {'DEVICE': device.upper()}
        xml = self._create_dynamic_xml(
            'SET_VM_STATUS', 'RIB_INFO', 'write', dic)

        if six.PY2:
            child_iterator = xml.getiterator()
        else:
            child_iterator = xml.iter()

        for child in child_iterator:
            if child.tag == 'SET_VM_STATUS':
                etree.SubElement(
                   child, 'VM_BOOT_OPTION', VALUE=boot_option.upper())
                etree.SubElement(
                   child, 'VM_WRITE_PROTECT', VALUE=write_protect.upper())

        d = self._request_ilo(xml)
        data = self._parse_output(d)
        return data
