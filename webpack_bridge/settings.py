from django.conf import settings

LOADER_SETTINGS = {
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
    LOADER_SETTINGS.update(settings.WEBPACK_MANIFEST_LOADER)
