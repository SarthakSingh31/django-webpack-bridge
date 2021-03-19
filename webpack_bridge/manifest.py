# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import json
import hashlib
from os import path
import time

from django.core.cache import cache
from django.templatetags.static import static
from django.utils.html import format_html

from webpack_bridge.errors import WebpackError, WebpackManifestNotFound,\
    WebpackEntryNotFound, FileExtensionHasNoMapping
from webpack_bridge.settings import BRIDGE_SETTINGS

MANIFEST_CACHE_TAG = 'manifest'


def hash_bytes(bytes):
    """Creates a MD5 hash of the 'bytes'"""
    md5 = hashlib.md5()
    md5.update(bytes)
    return md5.hexdigest()


class TagTranslater:
    """
    A helper class to generate html tags from an array of bundles.
    """

    def __init__(self):
        self.__group_to_extensions = BRIDGE_SETTINGS['group_to_extensions']
        self.__group_to_html_tag = BRIDGE_SETTINGS['group_to_html_tag']

    def translate(self, bundles):
        """
        Extracts the file extension from bundle paths and generates a html
        tag to import the bundles.
        """
        translated_bundles = []
        for bundle_path in bundles:
            bundle_ext = path.splitext(bundle_path)[1][1:]
            html_tag = None
            for group in self.__group_to_extensions:
                if bundle_ext in self.__group_to_extensions[group]:
                    html_tag = format_html(
                        self.__group_to_html_tag[group],
                        path=static(bundle_path),
                        attributes='{attributes}'
                    )

            if html_tag is None:
                raise FileExtensionHasNoMapping(
                    bundle_ext,
                    self.__group_to_extensions[group]
                )
            else:
                translated_bundles.append({
                    'ext': bundle_ext,
                    'tag': html_tag
                })

        return translated_bundles


class WebpackManifest:
    """
    Wrapper for webpack manifest data. Provides flags to help with caching
    and helper methods to resolve 'entries'.
    """

    def __init__(self, manifest_data, path):
        """
        manifest_data: The data from a manifest.json file.
        path: The path to the manifest.json file the 'manifest_data' is from.
        """
        self.__dirty = True  # True means that the cache needs to be updated
        self.__manifest = json.loads(manifest_data)
        self.__manifest_hash = hash_bytes(manifest_data)
        self.manifest_path = path
        self.__translated_entries = {}

    def validate(self, manifest_data):
        # Returns true if the manifest is up to date with 'manifest_data'
        return hash_bytes(manifest_data) == self.__manifest_hash

    def is_dirty(self):
        return self.__dirty

    def set_clean(self):
        self.__dirty = False

    def resolve(self, entry):
        """
        Resolves a 'entry' to the html tags required to render it.
        Will wait for the webpack compilation to finish by blocking this
        thread.
        """
        while 'compiling' in self.__manifest and self.__manifest['compiling']:
            time.sleep(BRIDGE_SETTINGS['compiling_poll_duration'])
            if path.isfile(self.manifest_path):
                with open(self.manifest_path, 'rb') as current_manifest:
                    current_manifest = current_manifest.read()
                    if not self.validate(current_manifest):
                        try:
                            self.__manifest = json.loads(current_manifest)
                            self.__manifest_hash = hash_bytes(current_manifest)
                        except json.JSONDecodeError:
                            pass

        if 'errors' in self.__manifest and len(self.__manifest['errors']) > 0:
            raise WebpackError(self.__manifest['errors'])

        if entry in self.__translated_entries:
            return self.__translated_entries[entry]
        else:
            if entry not in self.__manifest['entries']:
                raise WebpackEntryNotFound(entry)

            self.__translated_entries[entry] = \
                TagTranslater().translate(self.__manifest['entries'][entry])
            self.__dirty = True
            return self.__translated_entries[entry]


class EntrypointResolver:
    """
    Resolves a entrypoint to the associated bundles and generates html to
    import them. Also caches the manifest.json and the generated html tags.
    """

    @staticmethod
    def __get_manifest_path(dirs):
        for dir in dirs:
            manifest_path = path.join(dir, BRIDGE_SETTINGS['manifest_file'])
            if path.isfile(manifest_path):
                return manifest_path

        raise WebpackManifestNotFound(BRIDGE_SETTINGS['manifest_file'], dirs)

    def __update_cache(self):
        if BRIDGE_SETTINGS['cache'] and self.__manifest.is_dirty():
            self.__manifest.set_clean()
            cache.set(
                self.__cache_tag,
                self.__manifest,
                BRIDGE_SETTINGS['cache_timeout']
            )

    def __init__(self, dirs):
        """
        dirs: The directories in which to look for the manifest.json file.
        """
        self.__manifest = None
        if BRIDGE_SETTINGS['cache']:
            self.__cache_tag = '{}.{}'.format(
                BRIDGE_SETTINGS['cache_prefix'],
                MANIFEST_CACHE_TAG
            )
            cached_manifest = cache.get(self.__cache_tag)
            if cached_manifest:
                try:
                    opened_file = open(cached_manifest.manifest_path, 'rb')
                    with opened_file as current_manifest:
                        if cached_manifest.validate(current_manifest.read()):
                            self.__manifest = cached_manifest
                except FileNotFoundError:
                    pass

        if self.__manifest is None:
            manifest_path = EntrypointResolver.__get_manifest_path(dirs)
            with open(manifest_path, 'rb') as manifest_data:
                self.__manifest = WebpackManifest(
                    manifest_data.read(),
                    manifest_path
                )
                self.__update_cache()

    def resolve(self, entry):
        """
        Wrapper around WebpackManifest.resolve. Adds caching.
        """
        bundles = self.__manifest.resolve(entry)
        self.__update_cache()
        return bundles
