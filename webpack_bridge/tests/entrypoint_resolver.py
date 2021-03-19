# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from copy import deepcopy
from unittest.mock import patch

from .utils import MOCK_SETTINGS, get_mock_manifest, generate_mocks
from webpack_bridge.errors import WebpackManifestNotFound
from webpack_bridge.manifest import EntrypointResolver

from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings


@override_settings(**MOCK_SETTINGS)
class TestEntrypointResolver(TestCase):
    def setUp(self):
        self.mock_manifest = get_mock_manifest()

    def test_resolve(self):
        mocks = generate_mocks(self.mock_manifest)
        with mocks[0], mocks[1]:
            resolver = EntrypointResolver(settings.STATICFILES_DIRS)
            self.assertEqual(
                resolver.resolve('index'),
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

    def test_resolve_cache(self):
        mocks = generate_mocks(self.mock_manifest)
        with mocks[0], mocks[1]:
            resolver = EntrypointResolver(settings.STATICFILES_DIRS)
            # Asserts that they are the same instance
            resolved_index = resolver.resolve('index')
            self.assertIs(resolved_index, resolver.resolve('index'))
            self.assertIs(resolver.resolve('home'), resolver.resolve('home'))
            self.assertIs(resolved_index, resolver.resolve('index'))

    def test_resolve_cache_across(self):
        mocks = generate_mocks(self.mock_manifest)
        resolved_index = None
        with mocks[0], mocks[1]:
            resolver = EntrypointResolver(settings.STATICFILES_DIRS)
            resolved_index = resolver.resolve('index')

        # The manifest file is set to be empty, the assertion can only pass
        # if the cached version of WebpackManifest is used.
        mocks = generate_mocks({})
        validate_mock = patch(
            'webpack_bridge.manifest.WebpackManifest.validate',
            return_value=True
        )
        with mocks[0], mocks[1], validate_mock:
            resolver = EntrypointResolver(settings.STATICFILES_DIRS)
            self.assertEqual(resolved_index, resolver.resolve('index'))

    def test_resolve_changed(self):
        manifest_data = deepcopy(self.mock_manifest)
        mocks = generate_mocks(manifest_data)
        resolved_index = None
        with mocks[0], mocks[1]:
            resolver = EntrypointResolver(settings.STATICFILES_DIRS)
            resolved_index = resolver.resolve('index')

        self.mock_manifest['entries']['index'] = ['test.js']
        mocks = generate_mocks(self.mock_manifest)
        with mocks[0], mocks[1]:
            resolver = EntrypointResolver(settings.STATICFILES_DIRS)
            self.assertNotEqual(resolved_index, resolver.resolve('index'))

    def test_resolve_manifest_not_found(self):
        mocks = generate_mocks(self.mock_manifest, False)
        with mocks[0], mocks[1], self.assertRaises(WebpackManifestNotFound):
            EntrypointResolver(settings.STATICFILES_DIRS)
