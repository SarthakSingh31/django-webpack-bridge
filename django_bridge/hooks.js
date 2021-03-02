const path = require('path');
const { writeToFile } = require('./utils');

/**
 * Sets the manifest to show that the compilation has started.
 * Updates the manifest file on disk.
 * @param {DjangoWebpackBridgePlugin} bridge A instance of the bridge plugin
 */
function compilationStartHook(bridge) {
  bridge.manifest.compiling = true;
  bridge.manifest.errors = [];
  writeToFile(
    path.join(bridge.options.path, bridge.options.fileName),
    bridge.manifest,
  );
}

/**
 * Records the emited asset or the encounted error into the manifest.
 * Does not update the manifest file on disk.
 * @param {DjangoWebpackBridgePlugin} bridge A instance of the bridge plugin
 * @param {WebpackCompilationObject} compilation 
 *        https://webpack.js.org/api/compilation-object/
 */
function emitHook(bridge, compilation) {
  bridge.manifest.entries = {};
  compilation.entrypoints.forEach((entryObject, entryName) => {
    bridge.manifest.entries[entryName] = entryObject
      .getFiles()
      .map((fileName) => path.join(bridge.options.publicPath, fileName));
  });
  if (compilation.errors.length > 0) {
    bridge.manifest.errors.push(...compilation.errors)
  }
}

/**
 * Sets the manifest to show that the compilation has finshed.
 * Updates the manifest file on disk.
 * @param {DjangoWebpackBridgePlugin} bridge A instance of the bridge plugin
 */
function doneHook(bridge) {
  bridge.manifest.compiling = false;
  bridge.manifest.errors = bridge.manifest.errors
    .map(error => error.toString());
  writeToFile(
    path.join(bridge.options.path, bridge.options.fileName),
    bridge.manifest,
  );
}

module.exports = { compilationStartHook, emitHook, doneHook };