'use strict'
const path = require('path');
const DjangoBridgePlugin = require('django-webpack-bridge');

module.exports = {
  optimization: {
    splitChunks: {
      chunks: 'all',
    },
  },
  entry: {
    index: "./src/index.js",
  },
  output: {
    path: path.resolve('./dist'),
    filename: "[name]-[fullhash].js",
    chunkFilename: '[id]-[chunkhash].js',
    publicPath: '/',
  },
  plugins: [
    new DjangoBridgePlugin(),
  ],
}