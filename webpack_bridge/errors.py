# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from webpack_bridge.settings import BRIDGE_SETTINGS


class WebpackManifestNotFound(Exception):
    def __init__(_, name, paths):
        message = 'Manifest file with name ({}) not found in {}'
        super().__init__(message.format(name, paths))


class WebpackEntryNotFound(Exception):
    """
    The requsted 'entry' was not found in the manifest file
    It is probably not defined in webpack.config.js
    """

    def __init__(_, entry):
        message = 'Webpack entry with name {} not found in manifest.'
        super().__init__(message.format(entry))


class WebpackError(Exception):
    """Passes through any errors raised by webpack"""

    def __init__(_, errors):
        error_msg = ""
        for error in errors:
            error_msg += error + '\n'
        message = 'There was an error in webpack:\n{}'
        super().__init__(message.format(error_msg))


class FileExtensionHasNoMapping(Exception):
    """
    Could not find the file extension in 'BRIDGE_SETTINGS.group_to_html_tag'
    """

    def __init__(_, ext, group_to_extensions):
        message = 'File extension \'{}\' has no mapping, available mappings {}'
        super().__init__(message.format(ext, group_to_extensions))
