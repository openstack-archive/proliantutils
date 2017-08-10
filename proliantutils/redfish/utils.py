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

import collections

import six

from proliantutils import exception
from proliantutils.redfish.resources.system import constants as sys_cons


# Representation of supported boot modes
SupportedBootModes = collections.namedtuple(
    'SupportedBootModes', ['boot_mode_bios', 'boot_mode_uefi'])


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


def get_supported_boot_mode(supported_boot_mode):
        """Return bios and uefi support.

        :param supported_boot_mode: Supported boot modes
        :return: A tuple of 'true'/'false' based on bios and uefi
            support respectively.
        """
        boot_mode_bios = 'false'
        boot_mode_uefi = 'false'
        if (supported_boot_mode ==
                sys_cons.SUPPORTED_LEGACY_BIOS_ONLY):
            boot_mode_bios = 'true'
        elif (supported_boot_mode ==
                sys_cons.SUPPORTED_UEFI_ONLY):
            boot_mode_uefi = 'true'
        elif (supported_boot_mode ==
                sys_cons.SUPPORTED_LEGACY_BIOS_AND_UEFI):
            boot_mode_bios = 'true'
            boot_mode_uefi = 'true'

        return SupportedBootModes(boot_mode_bios=boot_mode_bios,
                                  boot_mode_uefi=boot_mode_uefi)


def get_allowed_operations(resource, subresouce_path):
    """Helper function to get the HTTP allowed methods.

    :param resource: ResourceBase instance from which the path is loaded.
    :param subresource_path: JSON field to fetch the value from.
            Either a string, or a list of strings in case of a nested field.
    :returns: A list of allowed HTTP methods.
    """
    uri = get_subresource_path_by(resource, subresouce_path)
    response = resource._conn.get(path=uri)
    return response.headers['Allow']


def is_operation_allowed(method, resource, subresouce_path):
    """Checks whether the operation is allowed for the resource.

    This method checks whether a HTTP method is allowed to be
    performed on the given sub resource path.
    :param method: A HTTP method. example: GET, PATCH, POST
    :param resource: ResourceBase instance from which the path is loaded.
    :param subresource_path: JSON field to fetch the value from.
            Either a string, or a list of strings in case of a nested field.
    :returns: True if the operation is allowed else False
    """
    return method in get_allowed_operations(resource, subresouce_path)


def max_safe(iterable):
    """Creates a wrapper over python max() function.

    This function is just a wrapper over pthon max().
    It catches the exceptions and let max() return without any error.
    """

    try:
        return max(iterable)
    except ValueError:
        # The TypeError is not caught here as that should be thrown.
        return 0


def lazy_load_and_cache(attribute_name, should_set_attribute=True):
    """Utility decorator to load the attribute value lazily and cache.

    This decorator is to be used to evaluate the attribute lazily.
    It expects the decorated method to contain its own logic of evaluation.
    When the attribute is not set, then it sets the resultant value on the
    attribute. If the ``should_set_attribute`` value is True then the attribute
    value is set to the result returned by the decorated method or otherwise
    it doesn't attempt to set.
    :param attribute_name: attribute name of the instance
    :param should_set_attribute: If True, then sets the attribute value to
        the result returned by the decorated method. Default is True.
    :returns: the value of attribute
    :raises: AttributeError, if the named attribute does not exist on
        the instance (the first parameter of decorated method)
    """
    if not isinstance(attribute_name, six.string_types):
        raise TypeError(
            ("'attribute_name' must be of type string. Invalid argument "
             "type provided: %(attribute_name_type)s") %
            {'attribute_name_type': type(attribute_name)})

    def func_decorator(func):

        @six.wraps(func)
        def func_wrapper(the_instance):

            instance_attr_val = getattr(the_instance, attribute_name)
            if instance_attr_val is None:

                result = func(the_instance)
                if should_set_attribute:
                    setattr(the_instance, attribute_name, result)
                return getattr(the_instance, attribute_name)

            return instance_attr_val

        return func_wrapper
    return func_decorator


def lazy_load_and_cache_resource(attribute_name, should_set_attribute=True):
    """Decorator to load the attribute value lazily for resource.

    Same as ``lazy_load_and_cache`` but only applicable for resource
    based initialization and caching.
    :param attribute_name: attribute name of the resource
    :param should_set_attribute: If True, then sets the attribute value to
        the result returned by the decorated method. Default value: True
    :returns: the value of attribute
    """
    def func_decorator(func):

        @six.wraps(func)
        @lazy_load_and_cache(attribute_name, should_set_attribute)
        def func_wrapper(the_resource_instance):

            cached_resource_instance = func(the_resource_instance)
            # Note(deray): Will invoke cache resource instance's ``refresh()``
            # method if the resource is stale. This logic is futuristic.
            return cached_resource_instance

        return func_wrapper
    return func_decorator
