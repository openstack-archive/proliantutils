#!/bin/bash
#
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


# The names for parameters in driver_info of a bare metal node.
IRONIC_DEPLOY_KERNEL_KEY=deploy_kernel
IRONIC_DEPLOY_RAMDISK_KEY=deploy_ramdisk
IRONIC_DEPLOY_ISO_KEY=ilo_deploy_iso

# Absolute path of the user image may be specified in this variable.
# If this is partition image, the user image kernel and user image ramdisk
# may also be specified.
IRONIC_USER_IMAGE=${IRONIC_USER_IMAGE:-}
IRONIC_USER_IMAGE_KERNEL=${IRONIC_USER_IMAGE_KERNEL:-}
IRONIC_USER_IMAGE_RAMDISK=${IRONIC_USER_IMAGE_RAMDISK:-}

# Preferred distro for the user image. If absolute path of the user image
# is specified, this should be specified to convey the instance user to
# tempest.
IRONIC_USER_IMAGE_PREFERRED_DISTRO=${IRONIC_USER_IMAGE_PREFERRED_DISTRO:-}

# This variable conveys if whole disk user image is to be used.
IRONIC_WHOLE_DISK_USER_IMAGE=$(trueorfalse False IRONIC_WHOLE_DISK_USER_IMAGE)

# The information about ProLiant hardware to be registered as Ironic node.
# This is of the following format:
#   <ip-address of ilo> <mac address> <ilo username> <ilo password> <size of root disk>
IRONIC_ILO_HWINFO=${IRONIC_ILO_HWINFO-}

# Returns 0 if whole disk image, 1 otherwise.
function is_whole_disk_image_required {
    is_deployed_by_agent || [[ "$IRONIC_WHOLE_DISK_USER_IMAGE" == "True" ]] && return 0
    return 1
}

function prepare_deploy_image {

    local output_file_prefix
    local cloud_image
    local cloud_image_kernel
    local cloud_image_ramdisk

    sudo apt-get -y purge python-requests

    if [ -z "$IRONIC_USER_IMAGE" ]; then
        output_file_prefix="${TOP_DIR}/files/${IRONIC_USER_IMAGE_PREFERRED_DISTRO}-cloud-image"
        if is_whole_disk_image_required; then
            cloud_image="${output_file_prefix}-disk.qcow2"
        else
            cloud_image="${output_file_prefix}.qcow2"
            cloud_image_kernel="${output_file_prefix}.vmlinuz"
            cloud_image_ramdisk="${output_file_prefix}.initrd"
        fi
        DEFAULT_IMAGE_NAME=$(basename $output_file_prefix)
    else
        cloud_image=$IRONIC_USER_IMAGE
        cloud_image_kernel=$IRONIC_USER_IMAGE_KERNEL
        cloud_image_ramdisk=$IRONIC_USER_IMAGE_RAMDISK
        DEFAULT_IMAGE_NAME=$(basename $cloud_image)
    fi

    iniset $TEMPEST_CONFIG compute ssh_user $IRONIC_USER_IMAGE_PREFERRED_DISTRO
    iniset $TEMPEST_CONFIG scenario ssh_user $IRONIC_USER_IMAGE_PREFERRED_DISTRO
    iniset $TEMPEST_CONFIG baremetal active_timeout 1800

    if [ ! -e "$cloud_image" ] || \
            ( ! is_whole_disk_image_required &&  \
              [ ! -e "$cloud_image_kernel" ] && \
              [ ! -e "$cloud_image_ramdisk" ] ); then

        DISK_IMAGE_CREATE_ELEMENTS="$IRONIC_USER_IMAGE_PREFERRED_DISTRO"
        if is_whole_disk_image_required; then
            DISK_IMAGE_CREATE_ELEMENTS+=" vm"
        else
            DISK_IMAGE_CREATE_ELEMENTS+=" baremetal grub2"
        fi

        DIB_CLOUD_INIT_DATASOURCES="ConfigDrive, OpenStack" disk-image-create \
            -o "$output_file_prefix" "$DISK_IMAGE_CREATE_ELEMENTS"
    fi

    local token
    token=$(openstack token issue -c id -f value)
    die_if_not_set $LINENO token "Keystone fail to get token"

    IMAGE_META=""
    if ! is_whole_disk_image_required; then
        local cloud_image_kernel_uuid=$(openstack \
            --os-token "$token" \
            --os-url "http://$GLANCE_HOSTPORT" \
            image create \
            $(basename $cloud_image_kernel) \
            --public --disk-format=aki \
            --container-format=aki \
            < "$cloud_image_kernel" | grep ' id ' | get_field 2)

        local cloud_image_ramdisk_uuid=$(openstack \
            --os-token "$token" \
            --os-url "http://$GLANCE_HOSTPORT" \
            image create \
            $(basename $cloud_image_ramdisk) \
            --public --disk-format=ari \
            --container-format=ari \
            < "$cloud_image_ramdisk" | grep ' id ' | get_field 2)

        IMAGE_META+=" --property ramdisk_id=$cloud_image_ramdisk_uuid "
        IMAGE_META+=" --property kernel_id=$cloud_image_kernel_uuid "
    fi

    openstack \
        --os-token "$token" \
        --os-url "http://$GLANCE_HOSTPORT" \
        image create \
        $DEFAULT_IMAGE_NAME \
        --public --disk-format=qcow2 \
        --container-format=bare \
        $IMAGE_META \
        < "$cloud_image"
}

function enroll_ilo_hardware {

    if [ -z "$IRONIC_ILO_HWINFO" ]; then
        return
    fi

    local ironic_node_cpu=$IRONIC_HW_NODE_CPU
    local ironic_node_ram=$IRONIC_HW_NODE_RAM
    local ironic_node_disk=$IRONIC_HW_NODE_DISK

    local hardware_info=${IRONIC_ILO_HWINFO}
    local ilo_address=$(echo $hardware_info |awk  '{print $1}')
    local mac_address=$(echo $hardware_info |awk '{print $2}')
    local ilo_username=$(echo $hardware_info |awk '{print $3}')
    local ilo_passwd=$(echo $hardware_info |awk '{print $4}')
    local root_device_hint=$(echo $hardware_info |awk '{print $5}')

    local node_options="-i ilo_address=$ilo_address "
    node_options+="-i ilo_password=$ilo_passwd "
    node_options+="-i ilo_username=$ilo_username "

    if [ "$IRONIC_DEPLOY_DRIVER" = "pxe_ilo" ]; then
        node_options+=" -i $IRONIC_DEPLOY_KERNEL_KEY=$IRONIC_DEPLOY_KERNEL_ID"
        node_options+=" -i $IRONIC_DEPLOY_RAMDISK_KEY=$IRONIC_DEPLOY_RAMDISK_ID"
    else
        node_options+=" -i $IRONIC_DEPLOY_ISO_KEY=$IRONIC_DEPLOY_ISO_ID"
    fi

    if [ -n "$root_device_hint" ]; then
        node_options+=' -p root_device="{\"size\": \"$root_device_hint\"}"'
    fi

    local node_id=$(ironic node-create \
                    -d $IRONIC_DEPLOY_DRIVER \
                    -p cpus=$ironic_node_cpu \
                    -p memory_mb=$ironic_node_ram \
                    -p local_gb=$ironic_node_disk \
                    -p cpu_arch=x86_64 \
                    $node_options \
                    | grep " uuid " | get_field 2)

    ironic port-create --address $mac_address --node $node_id
}

if [[ "$1" == "stack" && "$2" == "extra" ]]; then
    echo_summary "Configuring for iLO hardware"
    prepare_deploy_image
    enroll_ilo_hardware
fi
