const pluginName = 'DjangoWebpackManifestPlugin';

export default class DjangoWebpackManifestPlugin {
  apply(compiler) {
    compiler.hooks.beforeCompile.tap(pluginName, (compilationParams) => {
      console.log('DjangoWebpackManifestPlugin called in beforeCompile with: ', compilationParams);
    });

    compiler.hooks.done.tap(pluginName, (stats) => {
      console.log('DjangoWebpackManifestPlugin called in done with: ', stats);
    });
  }
}