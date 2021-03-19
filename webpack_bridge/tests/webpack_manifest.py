# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from copy import deepcopy
import json
from os import path
from webpack_bridge.settings import BRIDGE_SETTINGS

from .utils import MOCK_SETTINGS, get_mock_manifest, generate_mocks
from webpack_bridge.errors import WebpackError, WebpackEntryNotFound
from webpack_bridge.manifest import WebpackManifest

from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings


@override_settings(**MOCK_SETTINGS)
class TestWebpackManifest(TestCase):
    def setUp(self):
        self.mock_manifest_data = get_mock_manifest()
        self.mock_manifest_path = path.join(
            settings.STATIC_URL,
            BRIDGE_SETTINGS['manifest_file']
        )

    def test_validate(self):
        manifest_data = self.mock_manifest_data
        webpack_manifest = WebpackManifest(
            json.dumps(manifest_data).encode(),
            self.mock_manifest_path
        )

        mock_entries = manifest_data['entries']
        manifest_data['entries'] = {}
        self.assertFalse(
            webpack_manifest.validate(json.dumps(manifest_data).encode())
        )

        manifest_data['entries'] = mock_entries
        self.assertTrue(
            webpack_manifest.validate(json.dumps(manifest_data).encode())
        )

    def test_resolve(self):
        webpack_manifest = WebpackManifest(
            json.dumps(self.mock_manifest_data).encode(),
            self.mock_manifest_path
        )
        resolved_index = webpack_manifest.resolve('index')
        self.assertTrue(webpack_manifest.is_dirty())
        self.assertEqual(
            resolved_index,
            [
                {
                    'ext': 'js',
                    'tag': '<script src="/static/index-m876t9o8.js"'
                    + ' {attributes}></script>'
                },
                {
                    'ext': 'js',
                    'tag': '<script src="/static/vendor-4t4g534y.js"'
                    + ' {attributes}></script>'
                }
            ]
        )

    def test_resolve_compiling(self):
        manifest_data = deepcopy(self.mock_manifest_data)
        manifest_data['compiling'] = True
        mocks = generate_mocks(self.mock_manifest_data)
        with mocks[0], mocks[1]:
            webpack_manifest = WebpackManifest(
                json.dumps(manifest_data).encode(),
                self.mock_manifest_path
            )
            resolved_index = webpack_manifest.resolve('index')
            self.assertTrue(webpack_manifest.is_dirty())
            self.assertEqual(
                resolved_index,
                [
                    {
                        'ext': 'js',
                        'tag': '<script src="/static/index-m876t9o8.js"'
                        + ' {attributes}></script>'
                    },
                    {
                        'ext': 'js',
                        'tag': '<script src="/static/vendor-4t4g534y.js"'
                        + ' {attributes}></script>'
                    }
                ]
            )

    def test_resolve_webpack_errors(self):
        self.mock_manifest_data['errors'] = ['error1', 'error2']
        webpack_manifest = WebpackManifest(
            json.dumps(self.mock_manifest_data).encode(),
            self.mock_manifest_path
        )
        with self.assertRaises(WebpackError):
            webpack_manifest.resolve('index')

    def test_resolve_entry_not_found(self):
        webpack_manifest = WebpackManifest(
            json.dumps(self.mock_manifest_data).encode(),
            self.mock_manifest_path
        )
        with self.assertRaises(WebpackEntryNotFound):
            webpack_manifest.resolve('notentry')

    def test_resolve_cache(self):
        webpack_manifest = WebpackManifest(
            json.dumps(self.mock_manifest_data).encode(),
            self.mock_manifest_path
        )
        # Asserts that they are the same instance
        resolved_index = webpack_manifest.resolve('index')
        self.assertIs(webpack_manifest.resolve('index'), resolved_index)
        self.assertIs(
            webpack_manifest.resolve('home'),
            webpack_manifest.resolve('home')
        )
        self.assertIs(webpack_manifest.resolve('index'), resolved_index)
