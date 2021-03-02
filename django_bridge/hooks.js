const path = require('path');
const { writeToFile } = require('./utils');

function compilationStart(bridge) {
  bridge.manifest.compiling = true;
  bridge.manifest.errors = [];
  writeToFile(
    path.join(bridge.options.path, bridge.options.fileName),
    bridge.manifest,
  );
}

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

function doneHook(bridge) {
  bridge.manifest.compiling = false;
  bridge.manifest.errors = bridge.manifest.errors
    .map(error => error.toString());
  writeToFile(
    path.join(bridge.options.path, bridge.options.fileName),
    bridge.manifest,
  );
}

module.exports = { compilationStart, emitHook, doneHook };