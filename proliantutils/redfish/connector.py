# Copyright 2017 Hewlett Packard Enterprise Development LP
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

__author__ = 'HPE'

import retrying
from sushy import connector
from sushy import exceptions
from urlparse import urlparse


class HPEConnector(connector.Connector):
    """Class that extends base Sushy Connector class

    This class extends the Sushy's Connector class to override certain methods
    required to customize the functionality of the http operations.
    """

    MAX_RETRY_ATTEMPTS = 3  # Maximum number of attempts to be retried
    MAX_TIME_BEFORE_RETRY = 2 * 1000  # wait time in milliseconds before retry

    @retrying.retry(
        retry_on_exception=(
            lambda e: isinstance(e, exceptions.ConnectionError)),
        stop_max_attempt_number=MAX_RETRY_ATTEMPTS,
        wait_fixed=MAX_TIME_BEFORE_RETRY)
    def _op(self, method, path='', **session_kwargs):
        """Overrides the base method to support retrying the operation.

        :param method: The HTTP method to be used, e.g: GET, POST,
            PUT, PATCH, etc...
        :param path: The sub-URI path to the resource.
        :param session_kwargs: Optional requests session keyword arguments.
        :returns: The response from the connector.Connector's _op method.
        """
        session_kwargs['allow_redirects'] = False
        resp = super(HPEConnector, self)._op(method, path, **session_kwargs)
        if resp.status_code == 308:
            path = urlparse(resp.headers['Location']).path
            resp = super(HPEConnector, self)._op(method, path, **session_kwargs)
        return resp
