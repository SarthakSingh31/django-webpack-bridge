const path = require('path');
const { writeToFile } = require('./utils');

function compilationStart(bridge) {
  bridge.compiling = true;
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

  bridge.manifest.errors = compilation.errors;
}

function doneHook(bridge) {
  bridge.compiling = false;
  writeToFile(
    path.join(bridge.options.path, bridge.options.fileName),
    bridge.manifest,
  );
}

module.exports = { compilationStart, emitHook, doneHook };