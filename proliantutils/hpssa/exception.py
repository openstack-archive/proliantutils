# Copyright 2015 Hewlett-Packard Development Company, L.P.
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


class HPSSAException(Exception):

    message = "An exception occured in hpssa module"

    def __init__(self, message=None, **kwargs):

        if not message:
            message = self.message

        message = message % kwargs
        super(HPSSAException, self).__init__(message)


class InvalidInputError(HPSSAException):

    message = "Invalid Input: %(reason)s"


class PhysicalDisksNotFoundError(HPSSAException):

    message = ("Not enough physical disks were found to create logical disk "
               "of size %(size_gb)s GiB and raid level %(raid_level)s")


class HPSSAOperationError(HPSSAException):

    message = ("An error was encountered while doing hpssa configuration: "
               "%(reason)s.")
