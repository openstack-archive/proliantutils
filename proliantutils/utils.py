# Copyright 2016 Hewlett Packard Enterprise Company, L.P.
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

"""
Non-iLO related utilities and helper functions.
"""

from proliantutils.ilo import firmware_controller
from proliantutils import log


LOG = log.get_logger(__name__)


def process_firmware_image(compact_firmware_file, ilo_object):
    """Processes the firmware file.

    Processing the firmware file entails extracting the firmware file from its
    compact format. Along with the raw (extracted) firmware file, this method
    also sends out information of whether or not the extracted firmware file
        a) needs to be uploaded to http store
        b) is extracted in reality or the file was already in raw format
    :param compact_firmware_file: firmware file to extract from
    :param ilo_object: ilo client object (ribcl/ris object)
    :raises: InvalidInputError, for unsupported file types or raw firmware
             file not found from compact format.
    :raises: ImageExtractionFailed, for extraction related issues
    :returns: core(raw) firmware file
    :returns: to_upload, boolean to indicate whether to upload or not
    :returns: is_extracted, boolean to indicate firmware image is actually
              extracted or not.
    """
    fw_img_extractor = firmware_controller.get_fw_extractor(
        compact_firmware_file)
    LOG.debug('Extracting firmware file: %s ...', compact_firmware_file)
    raw_fw_file_path, is_extracted = fw_img_extractor.extract()

    # Note(deray): Need to check if this processing is for RIS or RIBCL
    # based systems. For Gen9 machines (RIS based) the firmware file needs
    # to be on a http store, and hence requires the upload to happen for the
    # firmware file.
    to_upload = False
    if 'Gen9' in ilo_object.model:
        to_upload = True

    LOG.debug('Extracting firmware file: %s ... done', compact_firmware_file)
    msg = ('Firmware file %(fw_file)s is %(msg)s. Need hosting (on an http '
           'store): %(yes_or_no)s' %
           {'fw_file': compact_firmware_file,
            'msg': ('extracted. Extracted file: %s' % raw_fw_file_path
                    if is_extracted else 'already in raw format'),
            'yes_or_no': 'Yes' if to_upload else 'No'})
    LOG.info(msg)
    return raw_fw_file_path, to_upload, is_extracted
