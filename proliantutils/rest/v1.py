# Copyright 2017 Hewlett Packard Enterprise Development Company, L.P.
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

"""Helper module to work with REST APIs"""

__author__ = 'HPE'

import base64
import gzip
import json

import requests
from requests.packages import urllib3
from requests.packages.urllib3 import exceptions as urllib3_exceptions
import retrying
import six
from six.moves.urllib import parse as urlparse

from proliantutils import exception
from proliantutils import log


REDIRECTION_ATTEMPTS = 5

LOG = log.get_logger(__name__)


class RestClientBase(object):

    def __init__(self, host, login, password, bios_password=None,
                 cacert=None):
        self.host = host
        self.login = login
        self.password = password
        self.bios_password = bios_password
        # Message registry support
        self.message_registries = {}
        self.cacert = cacert

        # By default, requests logs following message if verify=False
        #   InsecureRequestWarning: Unverified HTTPS request is
        #   being made. Adding certificate verification is strongly advised.
        # Just disable the warning if user intentionally did this.
        if self.cacert is None:
            urllib3.disable_warnings(urllib3_exceptions.InsecureRequestWarning)

    def _(self, msg):
        """Prepends host information to msg and returns it."""
        return "[iLO %s] %s" % (self.host, msg)

    def _get_response_body_from_gzipped_content(self, url, response):
        """Get the response body from gzipped content

        Try to decode as gzip (we should check the headers for
        Content-Encoding=gzip)

          if response.headers['content-encoding'] == "gzip":
            ...

        :param url: the url for which response was sent
        :type url: str
        :param response: response content object, probably gzipped
        :type response: object
        :returns: returns response body
        :raiises IloError: if the content is **not** gzipped
        """
        try:
            gzipper = gzip.GzipFile(fileobj=six.BytesIO(response.text))

            LOG.debug(self._("Received compressed response for "
                             "url %(url)s."), {'url': url})
            uncompressed_string = (gzipper.read().decode('UTF-8'))
            response_body = json.loads(uncompressed_string)

        except Exception as e:
            LOG.debug(
                self._("Error occurred while decompressing body. "
                       "Got invalid response '%(response)s' for "
                       "url %(url)s: %(error)s"),
                {'url': url, 'response': response.text, 'error': e})
            raise exception.IloError(e)

        return response_body

    def _rest_op(self, operation, suburi, request_headers, request_body):
        """Generic REST Operation handler."""

        url = urlparse.urlparse('https://' + self.host + suburi)
        # Used for logging on redirection error.
        start_url = url.geturl()

        LOG.debug(self._("%(operation)s %(url)s"),
                  {'operation': operation, 'url': start_url})

        if request_headers is None or not isinstance(request_headers, dict):
            request_headers = {}

        # Use self.login/self.password and Basic Auth
        if self.login is not None and self.password is not None:
            auth_data = self.login + ":" + self.password
            hr = "BASIC " + base64.b64encode(
                auth_data.encode('ascii')).decode("utf-8")
            request_headers['Authorization'] = hr

        if request_body is not None:
            if (isinstance(request_body, dict)
                    or isinstance(request_body, list)):
                request_headers['Content-Type'] = 'application/json'
            else:
                request_headers['Content-Type'] = ('application/'
                                                   'x-www-form-urlencoded')

        """Helper methods to retry and keep retrying on redirection - START"""

        def retry_if_response_asks_for_redirection(response):
            # NOTE:Do not assume every HTTP operation will return a JSON
            # request_body. For example, ExtendedError structures are only
            # required for HTTP 400 errors and are optional elsewhere as they
            # are mostly redundant for many of the other HTTP status code.
            # In particular, 200 OK responses should not have to return any
            # request_body.

            # NOTE:  this makes sure the headers names are all lower cases
            # because HTTP says they are case insensitive
            # Follow HTTP redirect
            if response.status_code == 301 and 'location' in response.headers:
                retry_if_response_asks_for_redirection.url = (
                    urlparse.urlparse(response.headers['location']))
                LOG.debug(self._("Request redirected to %s."),
                          retry_if_response_asks_for_redirection.url.geturl())
                return True
            return False

        @retrying.retry(
            # Note(deray): Return True if we should retry, False otherwise.
            # In our case, when the url response we receive asks for
            # redirection then we retry.
            retry_on_result=retry_if_response_asks_for_redirection,
            # Note(deray): Return True if we should retry, False otherwise.
            # In our case, when it's an IloConnectionError we don't retry.
            # ``requests`` already takes care of issuing max number of
            # retries if the URL service is unavailable.
            retry_on_exception=(
                lambda e: not isinstance(e, exception.IloConnectionError)),
            stop_max_attempt_number=REDIRECTION_ATTEMPTS)
        def _fetch_response():

            url = retry_if_response_asks_for_redirection.url

            kwargs = {'headers': request_headers,
                      'data': json.dumps(request_body)}
            if self.cacert is not None:
                kwargs['verify'] = self.cacert
            else:
                kwargs['verify'] = False

            LOG.debug(self._('\n\tHTTP REQUEST: %(restreq_method)s'
                             '\n\tPATH: %(restreq_path)s'
                             '\n\tBODY: %(restreq_body)s'
                             '\n'),
                      {'restreq_method': operation,
                       'restreq_path': url.geturl(),
                       'restreq_body': request_body})

            request_method = getattr(requests, operation.lower())
            try:
                response = request_method(url.geturl(), **kwargs)
            except Exception as e:
                LOG.debug(self._("Unable to connect to iLO. %s"), e)
                raise exception.IloConnectionError(e)

            return response

        """Helper methods to retry and keep retrying on redirection - END"""

        try:
            # Note(deray): This is a trick to use the function attributes
            # to overwrite variable/s (in our case ``url``) and use the
            # modified one in nested functions, i.e. :func:`_fetch_response`
            # and :func:`retry_if_response_asks_for_redirection`
            retry_if_response_asks_for_redirection.url = url

            response = _fetch_response()
        except retrying.RetryError as e:
            # Redirected for REDIRECTION_ATTEMPTS - th time. Throw error
            msg = (self._("URL Redirected %(times)s times continuously. "
                          "URL used: %(start_url)s More info: %(error)s") %
                   {'start_url': start_url, 'times': REDIRECTION_ATTEMPTS,
                    'error': str(e)})
            LOG.debug(msg)
            raise exception.IloConnectionError(msg)

        response_body = {}
        if response.text:
            try:
                response_body = json.loads(response.text)
            except (TypeError, ValueError):
                # Note(deray): If it doesn't decode as json, then
                # resources may return gzipped content.
                # ``json.loads`` on python3 raises TypeError when
                # ``response.text`` is gzipped one.
                response_body = (
                    self._get_response_body_from_gzipped_content(url,
                                                                 response))

        LOG.debug(self._('\n\tHTTP RESPONSE for %(restreq_path)s:'
                         '\n\tCode: %(status_code)s'
                         '\n\tResponse Body: %(response_body)s'
                         '\n'),
                  {'restreq_path': url.geturl(),
                   'status_code': response.status_code,
                   'response_body': response_body})
        return response.status_code, response.headers, response_body

    def _rest_get(self, suburi, request_headers=None):
        """REST GET operation.

        HTTP response codes could be 500, 404 etc.
        """
        return self._rest_op('GET', suburi, request_headers, None)

    def _rest_patch(self, suburi, request_headers, request_body):
        """REST PATCH operation.

        HTTP response codes could be 500, 404, 202 etc.
        """
        return self._rest_op('PATCH', suburi, request_headers, request_body)

    def _rest_put(self, suburi, request_headers, request_body):
        """REST PUT operation.

        HTTP response codes could be 500, 404, 202 etc.
        """
        return self._rest_op('PUT', suburi, request_headers, request_body)

    def _rest_post(self, suburi, request_headers, request_body):
        """REST POST operation.

        The response body after the operation could be the new resource, or
        ExtendedError, or it could be empty.
        """
        return self._rest_op('POST', suburi, request_headers, request_body)

    def _rest_delete(self, suburi, request_headers):
        """REST DELETE operation.

        HTTP response codes could be 500, 404 etc.
        """
        return self._rest_op('DELETE', suburi, request_headers, None)
