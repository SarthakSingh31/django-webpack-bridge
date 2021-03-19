// Copyright 2021 UW-IT, University of Washington
// SPDX-License-Identifier: Apache-2.0

const webpack = require('webpack');

const { compilationStartHook, emitHook, doneHook } = require('./hooks');

const pluginName = 'DjangoWebpackBridgePlugin';

const defaults = {
  path: null,
  publicPath: null,
  fileName: 'manifest.json',
}

/**
 * A plguin for Webpack that generates a manifest file intended to
 * be consumed by django-webpack-bridge.
 */
class DjangoWebpackBridgePlugin {
  constructor(options) {
    this.manifest = {};
    this.options = Object.assign({}, defaults, options);
  }

  apply(compiler) {
    if (!this.options.path) {
      this.options.path = compiler.options.output.path;
    }

    if (!this.options.publicPath) {
      this.options.publicPath = compiler.options.output.publicPath;
    }

    compiler.hooks.thisCompilation.tap(pluginName, (_) => {
      compilationStartHook(this);
    });

    if (webpack.version.startsWith('4')) {
      compiler.hooks.emit.tap(pluginName, (compilation) => emitHook(this, compilation));
    } else {
      compiler.hooks.thisCompilation.tap(pluginName, (compilation) => {
        compilation.hooks.processAssets.tap({
          name: pluginName,
          stage: Infinity
        }, () => {
          emitHook(this, compilation);
        });
      });
    }

    compiler.hooks.done.tap(pluginName, (_) => {
      doneHook(this);
    });
  }
}

module.exports = DjangoWebpackBridgePlugin;