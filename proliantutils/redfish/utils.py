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
from sushy.resources import base

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


def init_and_set_resource_if_not_already(resource_class, resource_id):
    """Creates the resource instance and sets on attribute.

    This decorator is to be used to create the resource instance from
    ``resource_class`` if the attribute returned by the decorated method
    is not already set. It expects the decorated method to have its first
    parameter as the resource instance on which it checks the attribute.
    The attribute name is to be returned from the decorated method.
    :param resource_class: The class of the resource
    :param resource_id: The identity of the resource.
        Either a string, or a callable (will be bound to resource instance
        while calling)
    :returns: the value of attribute returned by the wrapped method
    :raises: AttributeError, if the named attribute does not exist on
        resource instance (the first parameter of decorated method)
    """
    if ((not issubclass(resource_class, base.ResourceBase)) or
        (not (isinstance(resource_id, six.string_types) or
              callable(resource_id)))):
        raise TypeError(
            ("'resource_class' and 'resource_id' must be a ResourceBase "
             "instance and string/callable respectively. Invalid argument "
             "type/s provided: %(res_class_type)s, %(res_id_type)s") %
            {'res_class_type': type(resource_class),
             'res_id_type': type(resource_id)})

    def func_decorator(func):
        @six.wraps(func)
        def func_wrapper(this_resource_instance):
            instance_attr_name = func(this_resource_instance)

            instance_attr_val = getattr(
                this_resource_instance, instance_attr_name)
            if instance_attr_val is None:

                res_instance = resource_class(
                    this_resource_instance._conn,
                    (resource_id(this_resource_instance)
                     if callable(resource_id) else resource_id),
                    redfish_version=this_resource_instance.redfish_version)
                setattr(this_resource_instance, instance_attr_name,
                        res_instance)
                return getattr(this_resource_instance, instance_attr_name)

            return instance_attr_val

        return func_wrapper
    return func_decorator
