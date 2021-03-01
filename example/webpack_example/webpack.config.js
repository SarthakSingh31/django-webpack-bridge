'use strict'
const path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const DjangoBridgePlugin = require('django-webpack-bridge');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin');

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
  module: {
    rules: [
      {
        test: /\.vue$/,
        use: 'vue-loader'
      },
      {
        test: /\.css$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader'
        ],
      },
    ]
  },
  plugins: [
    new CleanWebpackPlugin(),
    new DjangoBridgePlugin(),
    new MiniCssExtractPlugin({
      filename: '[name]-[fullhash].css',
      chunkFilename: '[id]-[chunkhash].css',
    }),
    new VueLoaderPlugin(),
  ],
  resolve: {
    alias: {
      'vue$': 'vue/dist/vue.esm.js',
    },
  }
}