import json
import hashlib
from os import path

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.cache import cache

from webpack_bridge.errors import WebpackError, WebpackManifestNotFound,\
    WebpackEntryNotFound, FileExtensionHasNoMapping
from webpack_bridge.settings import LOADER_SETTINGS

MANIFEST_CACHE_TAG = 'manifest'

def hash_bytes(bytes):
    md5 = hashlib.md5()
    md5.update(bytes)
    return md5.hexdigest()

class TagTranslater:
    def __init__(self):
        self.__group_to_extensions = LOADER_SETTINGS['group_to_extensions']
        self.__group_to_html_tag = LOADER_SETTINGS['group_to_html_tag']

    def translate(self, bundle_data_array):
        translated_bundles = []
        for bundle_data in bundle_data_array:
            html_tag = None
            for group in self.__group_to_extensions:
                if bundle_data['ext'] in self.__group_to_extensions[group]:
                    html_tag = self.__group_to_html_tag[group].format(
                        path=static(bundle_data['path']),
                        attributes='{attributes}'
                    )
            
            if html_tag is None:
                raise FileExtensionHasNoMapping(bundle_data['ext'])
            else:
                translated_bundles.push({
                    'ext': bundle_data['ext'],
                    'tag': html_tag
                })
        
        return translated_bundles



class WebpackManifest:
    def __init__(self, manifest_data, path):
        # Keeps track whether it is cached
        self.__dirty = True
        self.__manifest = json.loads(manifest_data)
        self.__manifest_hash = hash_bytes(manifest_data)
        self.manifest_path = path
        self.__translated_entries = {}

    def validate(self, manifest_data):
        return hash_bytes(manifest_data) == self.__manifest_hash

    def is_dirty(self):
        return self.__dirty

    def set_clean(self):
        self.__dirty = False

    def resolve(self, entry):
        # TODO: Add waiting for compilation here

        if 'error' in self.__manifest:
            raise WebpackError(self.__manifest['error'])

        if entry in self.__translated_entries:
            return self.__translated_entries[entry]
        else:
            if entry not in self.__manifest['entries']:
                raise WebpackEntryNotFound(entry)
            
            bundle_data_array = []
            for bundle_name in self.__manifest['entries'][entry]:
                bundle_path = self.__manifest['bundles'][bundle_name]
                bundle_ext = path.splitext(bundle_path)[1][1:]
                bundle_data_array.push({
                    'ext': bundle_ext,
                    'path': bundle_path,
                })
            
            self.__translated_entries[entry] = \
                TagTranslater().translate(bundle_data_array)
            self.__dirty = True
            return self.__translated_entries[entry]


class EntrypointResolver:
    @staticmethod
    def __get_manifest_path(dirs):
        for dir in dirs:
            manifest_path = path.join(dir, LOADER_SETTINGS['manifest_file'])
            if path.isfile(manifest_path):
                return manifest_path

        raise WebpackManifestNotFound(dirs, LOADER_SETTINGS['manifest_file'])

    def __update_cache(self):
        if LOADER_SETTINGS['cache'] and self.__manifest.is_dirty():
            cache.set(
                self.__manifest,
                self.__cache_tag,
                LOADER_SETTINGS['cache_timeout']
            )
            self.__manifest.set_clean()

    def __init__(self, dirs):
        self.__manifest = None
        if LOADER_SETTINGS['cache']:
            self.__cache_tag = '{}.{}'.format(
                LOADER_SETTINGS['cache_prefix'],
                MANIFEST_CACHE_TAG
            )
            cached_manifest = cache.get(self.__cache_tag)
            try:
                with open(cached_manifest.manifest_path, 'rb') as current_manifest:
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
        bundles = self.__manifest.resolve(entry)
        self.__update_cache()
        return bundles