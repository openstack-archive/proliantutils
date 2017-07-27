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


def get_local_gb(system_obj):
    local_gb = max([(system_obj.smart_storage.logical_drives_maximum_size_mib
                     * 1024 * 1024),
                   system_obj.storages.volumes_maximum_size_bytes])
    if local_gb <= 0:
        local_gb = max(
            [(system_obj.smart_storage.physical_drives_maximum_size_mib
              * 1024 * 1024), system_obj.storages.drives_maximum_size_bytes,
             system_obj.simple_storages.maximum_size_bytes])
    # Convert the received size to GB
    local_gb = int(local_gb / (1024 * 1024 * 1024)) - 1
    return local_gb
