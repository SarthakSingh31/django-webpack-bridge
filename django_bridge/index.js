const { compilationStart, emitHook, doneHook } = require('./hooks');

const pluginName = 'DjangoWebpackBridgePlugin';

const defaults = {
  path: null,
  publicPath: null,
  fileName: 'manifest.json',
}

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
      compilationStart(this);
    });

    compiler.hooks.thisCompilation.tap(pluginName, (compilation) => {
      compilation.hooks.processAssets.tap({
        name: pluginName,
        stage: Infinity
      }, () => {
        emitHook(this, compilation);
      });
    });

    compiler.hooks.done.tap(pluginName, (_) => {
      doneHook(this);
    });
  }
}

module.exports = DjangoWebpackBridgePlugin;