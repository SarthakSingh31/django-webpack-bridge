from django.conf import settings

# BRIDGE_SETTINGS
# {
#   'manifest_file': Name of the manifest file (Defaults to 'manifest.json'),
#   'cache': Boolean to turn caching on and off (Defaults to not DEBUG),
#   'cache_timeout': Timeout duration for the cache (Defaults to 1 Day),
#   'cache_prefix': Namespace for the cache (Defaults to 'webpack_manifest'),
#   'group_to_extensions': Maps a tag group to a group of tags
#       (Defaults to 'script' -> ('js',), 'style' -> ('css', )),
#   'group_to_html_tag': Maps a tag group to a html tag
#       (Defaults to 'script': '<script src="{path}" {attributes}></script>',
#                    'style': '<link rel="stylesheet" type="text/css"'
#                             + ' href="{path}" {attributes}>',
#       ),
#   'compiling_poll_duration': Time between updaing the manifest from the file
#                              while compiling in sec (Defaults to 0.5 sec),
# }
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
    'manifest_file': 'manifest.json',
    'cache': not settings.DEBUG,
    'cache_timeout': 86400,  # 1 Day
    'cache_prefix': 'webpack_manifest',
    'group_to_extensions': {
        'script': ('js', ),
        'style': ('css', ),
    },
    'group_to_html_tag': {
        'script': '<script src="{path}" {attributes}></script>',
        'style':
            '<link rel="stylesheet" type="text/css"'
            + ' href="{path}" {attributes}>',
    },
    'compiling_poll_duration': 0.5,
}

if hasattr(settings, 'WEBPACK_MANIFEST_LOADER'):
    BRIDGE_SETTINGS.update(settings.WEBPACK_MANIFEST_LOADER)
