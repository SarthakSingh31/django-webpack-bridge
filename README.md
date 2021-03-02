# Django Webpack Bridge

Creates a bridge from webpack to django.

## How to Use

1. Add the packages to `setup.py` and `package.json`.
   1. Both are named `django-webpack-bridge`.
   2. To install from git
    python: `'django-webpack-bridge @ https://github.com/SarthakSingh31/django-webpack-bridge/tarball/master'`
    nodejs: `"django-webpack-bridge": "https://github.com/SarthakSingh31/django-webpack-bridge.git"`
2. Add the plugin to `webpack.config.js`

    ```js
    const DjangoBridgePlugin = require('django-webpack-bridge');
    module.exports = {
        ...,
        plugins: [
            ...,
            new DjangoBridgePlugin(),
        ],
    }
    ```

    `django-webpack-bridge` will use the variables from `module.exports.output`
3. Add the following to `settings.py`

    ```python
    INSTALLED_APPS += [
        ...
        'webpack_bridge',
    ]
    STATICFILES_DIRS = [
        '{same as module.exports.output.path from webpack.config.js}',
    ]
    ```

4. In the `template.html`
    ```jsx
    {% load webpack_bridge %}
    {% render_webpack_entry 'entry point name' js='defer' %}
    ```

## Settings

```python
BRIDGE_SETTINGS = {
   'manifest_file': Name of the manifest file (Defaults to 'manifest.json'),
   'cache': Boolean to turn caching on and off (Defaults to not DEBUG),
   'cache_timeout': Timeout duration for the cache (Defaults to 1 Day),
   'cache_prefix': Namespace for the cache (Defaults to 'webpack_manifest'),
   'group_to_extensions': Maps a tag group to a group of tags
       (Defaults to 'script' -> ('js',), 'style' -> ('css', )),
   'group_to_html_tag': Maps a tag group to a html tag
       (Defaults to 'script': '<script src="{path}" {attributes}></script>',
                    'style': '<link rel="stylesheet" type="text/css"'
                             + ' href="{path}" {attributes}>',
       ),
   'compiling_poll_duration': Time between updaing the manifest from the file
                              while compiling in sec (Defaults to 0.5 sec),
}
```

`group_to_extensions` and `group_to_html_tag` combine to create a multi-key map from a group of file extensions to a html tag. Eg.
```(js, jsx) -> <script src="{path}" {attributes}></script>```

`path`: Will be replaced with the bundle path
`attributes`: Will be replaced with any attributes specfied when when calling 'render_webpack_entry'. Attributes are grouped by file extension
