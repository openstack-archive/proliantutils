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

import six

from proliantutils import exception


def get_subresource_path_by(resource, subresource_path):
    """Helper function to find the resource path

    :param resource: ResourceBase instance from which the path is loaded.
    :param subresource_path: JSON field to fetch the value from.
            Either a string, or a list of strings in case of a nested field.
            It should also include the '@odata.id'
    :raises: MissingAttributeError, if required path is missing.
    :raises: ValueError, if path is empty.
    :raises: AttributeError, if json attr not found in resource
    """
    if isinstance(subresource_path, six.string_types):
        subresource_path = [subresource_path]
    elif not subresource_path:
        raise ValueError('"subresource_path" cannot be empty')

    body = resource.json
    for path_item in subresource_path:
        body = body.get(path_item, {})

    if not body:
        raise exception.MissingAttributeError(
            attribute='/'.join(subresource_path), resource=resource.path)

    if '@odata.id' not in body:
        raise exception.MissingAttributeError(
            attribute='/'.join(subresource_path)+'/@odata.id',
            resource=resource.path)

    return body['@odata.id']
