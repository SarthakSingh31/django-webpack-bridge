# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
from unittest.mock import patch, mock_open

MOCK_SETTINGS = {
    'STATICFILES_DIRS': [
        '/static/',
    ],
}


def generate_mocks(manifest_data, isfile_return=True):
    open_mock = patch(
        'builtins.open',
        mock_open(read_data=json.dumps(manifest_data).encode())
    )
    is_file_mock = patch('os.path.isfile', return_value=isfile_return)
    return (open_mock, is_file_mock)


def get_mock_manifest():
    with open('test_files/manifest.json') as mock_manifest_data:
        return json.load(mock_manifest_data)
