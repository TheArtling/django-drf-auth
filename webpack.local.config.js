var path = require("path")
var webpack = require('webpack')

var config = require('./webpack.base.config.js')

config.ip = 'localhost'
config.devtool = '#eval-source-map'

// Use webpack dev server
config.entry = {
  AuthApp: [
    'webpack-dev-server/client?http://localhost:3000',
    'webpack/hot/only-dev-server',
    './drf_auth/reactjs/AuthApp',
  ],
  vendors: [
    'webpack-dev-server/client?http://localhost:3000',
    'webpack/hot/only-dev-server',
    'react',
  ],
}

// override django's STATIC_URL for webpack bundles
config.output.publicPath = 'http://localhost:3000' + '/assets/bundles/'

// Add HotModuleReplacementPlugin and BundleTracker plugins
config.plugins = config.plugins.concat([
  new webpack.HotModuleReplacementPlugin(),
  new webpack.NoErrorsPlugin(),
  new webpack.DefinePlugin({
    'process.env': {
      'NODE_ENV': JSON.stringify('development'),
  }}),
])

// Add a loader for JSX files with react-hot enabled
config.module.loaders.push(
  { test: /\.jsx?$/, exclude: /node_modules/, loaders: ['react-hot', 'babel'] }
)

module.exports = config
