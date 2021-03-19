# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings

# BRIDGE_SETTINGS
#
# 'group_to_extensions' and 'group_to_html_tag' combine to create a
# multi-key map from a group of file extensions to a html tag. Eg.
# (js, jsx) -> <script src="{path}" {attributes}></script>
#
# {path}: Will be replaced with the bundle path
# {attributes}: Will be replaced with any attributes specfied when
#               when calling 'render_webpack_entry'. Attributes are grouped
#               by file extension

BRIDGE_SETTINGS = {
    # Name of the manifest file
    'manifest_file': 'manifest.json',
    # Boolean to turn caching on and off
    'cache': not settings.DEBUG,
    # Timeout duration for the cache
    'cache_timeout': 86400,  # 1 Day
    # Namespace for the cache
    'cache_prefix': 'webpack_manifest',
    # Maps a tag group to a group of tags
    'group_to_extensions': {
        'script': ('js', ),
        'style': ('css', ),
    },
    # Maps a tag group to a html tag
    'group_to_html_tag': {
        'script': '<script src="{path}" {attributes}></script>',
        'style':
            '<link rel="stylesheet" type="text/css"'
            + ' href="{path}" {attributes}>',
    },
    # Time between updaing the manifest from the file while compiling
    'compiling_poll_duration': 0.5,
}

if hasattr(settings, 'WEBPACK_MANIFEST_LOADER'):
    BRIDGE_SETTINGS.update(settings.WEBPACK_MANIFEST_LOADER)
