# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from .utils import MOCK_SETTINGS, get_mock_manifest
from webpack_bridge.errors import FileExtensionHasNoMapping
from webpack_bridge.manifest import TagTranslater

from django.test import TestCase
from django.test.utils import override_settings


@override_settings(**MOCK_SETTINGS)
class TestTagTranslater(TestCase):
    def setUp(self):
        self.tag_translater = TagTranslater()
        self.mock_manifest = get_mock_manifest()

    def test_translate(self):
        bundles = self.mock_manifest['entries']['home']
        self.assertEqual(
            self.tag_translater.translate(bundles),
            [
                {
                    'ext': 'js',
                    'tag': '<script src="/static/home-234xz0jk.js"'
                    + ' {attributes}></script>'
                },
                {
                    'ext': 'js',
                    'tag': '<script src="/static/vendor-4t4g534y.js"'
                    + ' {attributes}></script>'
                },
                {
                    'ext': 'css',
                    'tag': '<link rel="stylesheet" type="text/css" '
                    + 'href="/static/other-home-89m07yfg.css" {attributes}>'
                }
            ]
        )

    def test_translate_error(self):
        # Extension with no mapping
        with self.assertRaises(FileExtensionHasNoMapping):
            bundles = self.mock_manifest['entries']['home']
            bundles.append('test.test')
            self.tag_translater.translate(bundles)

        # No Extension
        with self.assertRaises(FileExtensionHasNoMapping):
            bundles = self.mock_manifest['entries']['home']
            bundles.append('test')
            self.tag_translater.translate(bundles)
