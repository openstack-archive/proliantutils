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
import hashlib

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


def _get_hash_object(hash_algo_name):
    """Create a hash object based on given algorithm.

    :param hash_algo_name: name of the hashing algorithm.
    :raises: InvalidParameterValue, on unsupported or invalid input.
    :returns: a hash object based on the given named algorithm.
    """
    algorithms = (hashlib.algorithms_guaranteed if six.PY3
                  else hashlib.algorithms)
    if hash_algo_name not in algorithms:
        msg = (_("Unsupported/Invalid hash name '%s' provided.")
               % hash_algo_name)
        LOG.error(msg)
        raise exception.InvalidParameterValue(msg)

    return getattr(hashlib, hash_algo_name)()


def hash_file(file_like_object, hash_algo='md5'):
    """Generate a hash for the contents of a file.

    It returns a hash of the file object as a string of double length,
    containing only hexadecimal digits. It supports all the algorithms
    hashlib does.
    :param file_like_object: file like object whose hash to be calculated.
    :param hash_algo: name of the hashing strategy, default being 'md5'.
    :raises: InvalidParameterValue, on unsupported or invalid input.
    :returns: a condensed digest of the bytes of contents.
    """
    checksum = _get_hash_object(hash_algo)
    for chunk in iter(lambda: file_like_object.read(32768), b''):
        checksum.update(chunk)
    return checksum.hexdigest()


def verify_image_checksum(image_location, expected_checksum):
    """Verifies checksum (md5) of image file against the expected one.

    This method generates the checksum of the image file on the fly and
    verifies it against the expected checksum provided as argument.

    :param image_location: location of image file whose checksum is verified.
    :param expected_checksum: checksum to be checked against
    :raises: ImageRefValidationFailed, if invalid file path or
             verification fails.
    """
    try:
        with open(image_location, 'rb') as fd:
            actual_checksum = utils.hash_file(fd)
    except IOError as e:
        LOG.error(_LE("Error opening file: %(file)s"),
                  {'file': image_location})
        raise exception.ImageRefValidationFailed(image_href=image_location,
                                                 reason=e)

    if actual_checksum != expected_checksum:
        msg = (_('Error verifying image checksum. Image %(image)s failed to '
                 'verify against checksum %(checksum)s. Actual checksum is: '
                 '%(actual_checksum)s') %
               {'image': image_location, 'checksum': expected_checksum,
                'actual_checksum': actual_checksum})
        LOG.error(msg)
        raise exception.ImageRefValidationFailed(image_href=image_location,
                                                 reason=msg)
