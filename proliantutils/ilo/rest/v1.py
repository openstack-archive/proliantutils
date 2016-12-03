# Copyright 2016 Hewlett Packard Enterprise Development Company, L.P.
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

"""Helper module for working with REST technology."""

__author__ = 'HPE'

import base64
import gzip
import hashlib
import json
import time

import requests
from requests.packages import urllib3
from requests.packages.urllib3 import exceptions as urllib3_exceptions
import six
from six.moves import urllib
from six.moves.urllib import parse as urlparse

from proliantutils import exception
from proliantutils import log

LOG = log.get_logger(__name__)


class RestRequest(object):
    """Holder for Request information."""

    def __init__(self, path, method='GET', body=''):
        """Initialize RestRequest

        :param path: path within tree
        :type path: str
        :param method: method to be implemented
        :type method: str
        :param body: body payload for the rest call
        :type body: dict
        """
        self._method = method
        self._path = path
        self._body = body

    def _get_method(self):
        """Return object method."""
        return self._method

    method = property(_get_method, None)

    def _get_path(self):
        """Return object path."""
        return self._path

    path = property(_get_path, None)

    def _get_body(self):
        """Return object body."""
        return self._body

    body = property(_get_body, None)

    def __str__(self):
        """Format string."""
        strvars = dict(method=self.method, path=self.path, body=self.body)

        # set None to '' for strings
        if not strvars['body']:
            strvars['body'] = ''

        try:
            strvars['body'] = str(str(self._body))
        except BaseException:
            strvars['body'] = ''

        return u"%(method)s %(path)s\n\n%(body)s" % strvars


class RestClientBase(object):
    """Base class for RestClients."""

    MAX_RETRY = 5

    def __init__(self, host, username=None, password=None,
                 default_prefix='/rest/v1/', sessionkey=None,
                 biospassword=None, cacert=None):
        """Initialization of the base class RestClientBase

        :param host: The ip of the remote iLO system
        :type host: str
        :param username: The user name used for authentication
        :type username: str
        :param password: The password used for authentication
        :type password: str
        :param default_prefix: The default root point
        :type default_prefix: str
        :param sessionkey: session key for the current login
        :type sessionkey: str
        :param biospassword: biospassword, if needed
        :type biospassword: str
        :param cacert: SSL certificate
        :type biospassword: str
        """

        self.__host = host
        self.__username = username
        self.__password = password
        self.__biospassword = biospassword
        self.__base_url = urlparse.urlparse('https://' + host)

        self.__session_key = sessionkey
        self.__authorization_key = None
        self.__session_location = None

        self._conn = None
        self._conn_count = 0

        self.login_url = None
        self.default_prefix = default_prefix
        self.bios_password = biospassword
        # Message registry support
        self.message_registries = {}
        self.cacert = cacert

        # By default, requests logs following message if verify=False
        #   InsecureRequestWarning: Unverified HTTPS request is
        #   being made. Adding certificate verification is strongly advised.
        # Just disable the warning if user intentionally did this.
        if self.cacert is None:
            urllib3.disable_warnings(urllib3_exceptions.InsecureRequestWarning)

    def _LiLO(self, msg):
        """Prepends host information if available to msg and returns it."""
        try:
            return "[iLO %s] %s" % (self.__host, msg)
        except AttributeError:
            return "[iLO <unknown>] %s" % msg

    @property
    def host(self):
        """Returns host (iLO ip)."""
        return self.__host

    @host.setter
    def host(self, value):
        """Sets host (iLO ip)

        :param value: The host (iLO ip) to be set.
        :type value: str
        """
        self.__host = value

    @property
    def username(self):
        """Returns user name."""
        return self.__username

    @username.setter
    def username(self, value):
        """Sets user name

        :param value: The user name to be set.
        :type value: str
        """
        self.__username = value

    @property
    def login(self):
        """Returns user name."""
        return self.__username

    @property
    def password(self):
        """Returns password."""
        return self.__password

    @password.setter
    def password(self, password):
        """Sets password

        :param password: The password to be set.
        :type password: str
        """
        self.__password = password

    def get_biospassword(self):
        """Return BIOS password."""
        return self.__biospassword

    def set_biospassword(self, biospassword):
        """Set BIOS password

        :param biospassword: The bios password to be set.
        :type biospassword: str
        """
        self.__biospassword = biospassword

    def get_base_url(self):
        """Return used URL."""
        return self.__base_url

#     def set_base_url(self, url):
#         """Set based URL
#         :param url: The URL to be set.
#         :type url: str
#         """
#         self.__base_url = url

    def get_session_key(self):
        """Return session key."""
        return self.__session_key

    def set_session_key(self, session_key):
        """Set session key

        :param session_key: The session_key to be set.
        :type session_key: str
        """
        self.__session_key = session_key

    def get_session_location(self):
        """Return session location."""
        return self.__session_location

    def set_session_location(self, session_location):
        """Set session location

        :param session_location: The session_location to be set.
        :type session_location: str
        """
        self.__session_location = session_location

    def get_authorization_key(self):
        """Return authorization key."""
        return self.__authorization_key

    def set_authorization_key(self, authorization_key):
        """Set authorization key

        :param session_location: The session_location to be set.
        :type session_location: str
        """
        self.__authorization_key = authorization_key

    def _rest_get(self, path, headers=None, args=None):
        """REST GET operation.

        HTTP response codes could be 500, 404 etc.
        :param path: the URL path.
        :param path: str.
        :params headers: the header arguments
        :params args: dict.
        :params args: the arguments to get
        :params args: dict.
        """
        return self._rest_request(
            path, method='GET', args=args, headers=headers)

    def _rest_head(self, path, headers=None, args=None):
        """REST HEAD operation.

        :param path: the URL path.
        :param path: str.
        :params headers: the header arguments
        :params args: dict.
        :params args: the arguments to get
        :params args: dict.
        """
        return self._rest_request(
            path, method='HEAD', args=args, headers=headers)

    def _rest_post(self, path, headers=None, body=None, args=None,
                   providerheader=None):
        """REST POST operation.

        The response body after the operation could be the new resource, or
        ExtendedError, or it could be empty.
        :param path: the URL path.
        :param path: str.
        :param headers: list of headers to be appended.
        :type headers: list.
        :param body: the body to be sent.
        :type body: str.
        :params args: the arguments to post.
        :params args: dict.
        :param optionalpassword: provide password for authentication.
        :type optionalpassword: str.
        :param provideheader: provider id for the header.
        :type providerheader: str.
        """
        return self._rest_request(
            path, method='POST', args=args, body=body, headers=headers,
            providerheader=providerheader)

    def _rest_put(self, path, headers=None, body=None, args=None,
                  optionalpassword=None, providerheader=None):
        """REST PUT operation.

        HTTP response codes could be 500, 404, 202 etc.
        :param path: the URL path.
        :param path: str.
        :param headers: list of headers to be appended.
        :type headers: list.
        :param body: the body to be sent.
        :type body: str.
        :params args: the arguments to put.
        :params args: dict.
        :param optionalpassword: provide password for authentication.
        :type optionalpassword: str.
        :param provideheader: provider id for the header.
        :type providerheader: str.
        """
        return self._rest_request(
            path, method='PUT', args=args, body=body, headers=headers,
            optionalpassword=optionalpassword, providerheader=providerheader)

    def _rest_patch(self, path, headers=None, body=None, args=None,
                    optionalpassword=None, providerheader=None):
        """REST PATCH operation.

        HTTP response codes could be 500, 404, 202 etc.
        :param path: the URL path.
        :param path: str.
        :param headers: list of headers to be appended.
        :type headers: list.
        :param body: the body to be sent.
        :type body: str.
        :params args: the arguments to patch.
        :params args: dict.
        :param optionalpassword: provide password for authentication.
        :type optionalpassword: str.
        :param provideheader: provider id for the header.
        :type providerheader: str.
        """
        return self._rest_request(
            path, method='PATCH', args=args, body=body, headers=headers,
            optionalpassword=optionalpassword, providerheader=providerheader)

    def _rest_delete(self, path, headers=None, args=None,
                     optionalpassword=None, providerheader=None):
        """REST DELETE operation.

        HTTP response codes could be 500, 404 etc.
        :param path: the URL path.
        :type path: str.
        :param headers: list of headers to be appended.
        :type headers: list.
        :param args: the arguments to delete.
        :type args: dict.
        :param optionalpassword: provide password for authentication.
        :type optionalpassword: str.
        :param provideheader: provider id for the header.
        :type providerheader: str.
        """
        return self._rest_request(
            path, method='DELETE', args=args, headers=headers,
            optionalpassword=optionalpassword, providerheader=providerheader)

    def _get_req_headers(self, headers=None, providerheader=None,
                         optionalpassword=None):
        """Get the request headers

        :param headers: additional headers to be utilized
        :type headers: str
        :param provideheader: provider id for the header.
        :type providerheader: str.
        :param optionalpassword: provide password for authentication.
        :type optionalpassword: str.
        :returns: returns headers
        """
        headers = headers if isinstance(headers, dict) else {}

        if providerheader:
            headers['X-CHRP-RIS-Provider-ID'] = providerheader

        if self.__biospassword:
            hash_object = hashlib.sha256(self.__biospassword)
            headers['X-HPRESTFULAPI-AuthToken'] = (hash_object.hexdigest().
                                                   upper())
        elif optionalpassword:
            hash_object = hashlib.sha256(optionalpassword)
            headers['X-HPRESTFULAPI-AuthToken'] = (hash_object.hexdigest().
                                                   upper())

        if self.__session_key:
            headers['X-Auth-Token'] = self.__session_key
        elif self.__authorization_key:
            headers['Authorization'] = self.__authorization_key
        elif (self.__username is not None and self.__password is not None):
            # Use self.__username / self.__password for Basic Auth
            auth_data = self.__username + ":" + self.__password
            hr = "BASIC " + (base64.b64encode(auth_data.encode('ascii')).
                             decode("utf-8"))
            headers['Authorization'] = hr

        headers['Accept'] = '*/*'
        headers['Connection'] = 'Keep-Alive'

        return headers

    def _get_response_body_from_gzipped_content(self, url, response):
        """Get the response body from gzipped content

        :param url: the url for which response was sent
        :type url: str
        :param response: response content object, probably gzipped
        :type response: object
        :returns: returns response body
        :raiises IloError: if the content is **not** gzipped
        """
        # if it doesn't decode as json
        # NOTE:  resources may return gzipped content
        # try to decode as gzip (we should check the headers
        # for Content-Encoding=gzip)
        #
        # if response.headers['content-encoding'] == "gzip":
        #   ...
        #
        # NOTE: json.loads on python3 raises TypeError when
        # response.text is gzipped one.
        try:

            gzipper = gzip.GzipFile(
                fileobj=six.BytesIO(response.text))

            LOG.debug(
                self._LiLO("Received compressed response for "
                           "url %(url)s."), {'url': url})

            uncompressed_string = (gzipper.read().
                                   decode('UTF-8'))
            response_body = json.loads(uncompressed_string)

        except Exception as e:

            LOG.debug(
                self._LiLO("Error occur while decompressing "
                           "body. Got invalid response "
                           "'%(response)s' for url %(url)s: "
                           "%(error)s"),
                {'url': url, 'response': response.text,
                 'error': e})
            raise exception.IloError(e)

        return response_body

    def _rest_request(self, path, method='GET', args=None, headers=None,
                      body=None, optionalpassword=None, providerheader=None):
        """Generic REST Operation handler.

        :param path: path within tree
        :type path: str
        :param method: method to be implemented
        :type method: str
        :param args: the arguments for method
        :type args: dict
        :param body: body payload for the rest call
        :type body: dict
        :param headers: provide additional headers
        :type headers: dict
        :param optionalpassword: provide password for authentication
        :type optionalpassword: str
        :param provideheader: provider id for the header
        :type providerheader: str
        :returns: returns a RestResponse object
        """
        headers = self._get_req_headers(headers, providerheader,
                                        optionalpassword)
        if self.default_prefix not in path:
            reqpath = (self.default_prefix + path).replace('//', '/')
        else:
            reqpath = path.replace('//', '/')

        if body is not None:
            if isinstance(body, dict) or isinstance(body, list):
                headers['Content-Type'] = u'application/json'
                body = json.dumps(body)
            else:
                headers['Content-Type'] = u'application/x-www-form-urlencoded'
                body = urllib.urlencode(body)

            headers['Content-Length'] = len(body)

        if args:
            if method == 'GET':
                reqpath += '?' + urllib.urlencode(args)
            elif method == 'PUT' or method == 'POST' or method == 'PATCH':
                headers['Content-Type'] = u'application/x-www-form-urlencoded'
                body = urllib.urlencode(args)

        restreq = RestRequest(reqpath, method=method, body=body)

        attempts = 0
        while attempts < self.MAX_RETRY:
            LOG.debug(self._LiLO('\n\tHTTP REQUEST: %(restreq_method)s'
                                 '\n\tPATH: %(restreq_path)s'
                                 '\n\tBODY: %(restreq_body)s'
                                 '\n'),
                      {'restreq_method': restreq.method,
                       'restreq_path': restreq.path,
                       'restreq_body': restreq.body})
            attempts = attempts + 1
            LOG.info(self._LiLO('Attempt %s of %s'), attempts, restreq.path)

            url = self.__base_url.geturl() + restreq.path
            try:
                response = self._rest_request_core(restreq, headers)

                response_body = {}
                if response.text:
                    try:
                        response_body = json.loads(response.text)
                    except (TypeError, ValueError):
                        response_body = (
                            self._get_response_body_from_gzipped_content(
                                url, response))

            except Exception as excp:
                if isinstance(excp, exception.IloError):
                    raise

                LOG.debug(self._LiLO("Unable to connect to iLO (%s). %s"),
                          self.__host, excp)

                LOG.info(self._LiLO('Retrying %s') % path)
                time.sleep(1)
                continue
            else:
                break

        if attempts < self.MAX_RETRY:
            LOG.debug(self._LiLO('HTTP RESPONSE for %(restreq_path)s:'
                                 '\n\tCode: %(status_code)s'
                                 '\n\tResponse Body: %(response_body)s'
                                 '\n'),
                      {'restreq_path': restreq.path,
                       'status_code': response.status_code,
                       'response_body': response_body})

            return response.status_code, response.headers, response_body
        # else:
            # raise RetriesExhaustedError()

    def _rest_request_core(self, restreq, headers):
        """Core REST request initiator.

        :param restreq: RestRequest instance
        :type path: RestRequest
        :param headers: headers
        :type headers: dict
        :returns: returns a RestResponse object
        """
        while True:

            kwargs = {'headers': headers,
                      'data': restreq.body}

            if self.cacert is not None:
                kwargs['verify'] = self.cacert
            else:
                kwargs['verify'] = False

            url = self.__base_url.geturl() + restreq.path
            request_method = getattr(requests, restreq.method.lower())

            inittime = time.clock()
            response = request_method(url, **kwargs)
            endtime = time.clock()

            LOG.info(self._LiLO('Response Time to %s: %s seconds.') %
                     (restreq.path, str(endtime - inittime)))

            if (response.status_code not in range(300, 399)
                    or response.status_code == 304):
                break

            # NOTE:Do not assume every HTTP operation will return a
            # JSON body. For example, ExtendedError structures are only
            # required for HTTP 400 errors and are optional elsewhere
            # as they are mostly redundant for many of the other HTTP
            # status code. In particular, 200 OK responses should not
            # have to return any body.

            # NOTE:  this makes sure the headers names are all lower
            # cases because HTTP says they are case insensitive.
            # Follow HTTP redirect
            if (response.status_code == 301
                    and 'location' in response.headers):
                url = urlparse.urlparse(response.headers['location'])
                # redir_count -= 1
                LOG.debug(self._LiLO("Request redirected to %s."),
                          url.geturl())
            else:
                break

        return response
