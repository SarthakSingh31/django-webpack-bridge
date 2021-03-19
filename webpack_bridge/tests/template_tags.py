# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from .utils import MOCK_SETTINGS, get_mock_manifest, generate_mocks
from webpack_bridge.templatetags.webpack_bridge import render_webpack_entry

from django.test import TestCase
from django.test.utils import override_settings


@override_settings(**MOCK_SETTINGS)
class TestRenderWebpackEntry(TestCase):
    def setUp(self):
        self.mock_manifest = get_mock_manifest()

    def test_render(self):
        mocks = generate_mocks(self.mock_manifest)
        with mocks[0], mocks[1]:
            self.assertEqual(
                render_webpack_entry(
                    'home',
                    js='async',
                    css='crossorigin'
                ),
                '<script src="/static/home-234xz0jk.js" async></script>\n'
                '<script src="/static/vendor-4t4g534y.js" async></script>\n'
                '<link rel="stylesheet" type="text/css"'
                ' href="/static/other-home-89m07yfg.css" crossorigin>\n'
            )
