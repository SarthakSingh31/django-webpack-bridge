from webpack_bridge.settings import LOADER_SETTINGS

class WebpackManifestNotFound(Exception):
    def __init__(name, path):
        message = 'Manifest file with name ({}) not found in {}'
        super().__init__(message.format(name, path))


class WebpackEntryNotFound(Exception):
    def __init__(entry):
        message = 'Webpack entry with name {} not found in manifest.'
        super().__init__(message.format(entry))


class WebpackError(Exception):
    def __init__(error):
        message = 'There was an error in webpack: {}'
        super().__init__(message.format(error))


class FileExtensionHasNoMapping(Exception):
    def __init__(ext):
        message = 'File extension \'{}\' has no mapping, available mappings {}'
        super().__init__(message.format(ext, LOADER_SETTINGS.group_to_extensions))