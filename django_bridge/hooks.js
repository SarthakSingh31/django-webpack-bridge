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
}

function doneHook(bridge) {
  bridge.manifest.compiling = false;
  writeToFile(
    path.join(bridge.options.path, bridge.options.fileName),
    bridge.manifest,
  );
}

function failHook(bridge, error) {
  console.log("failHook", error);
  bridge.manifest.compiling = false;
  bridge.manifest.errors.push(error);
  writeToFile(
    path.join(bridge.options.path, bridge.options.fileName),
    bridge.manifest,
  );
}

module.exports = { compilationStart, emitHook, doneHook, failHook };