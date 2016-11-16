var path = require("path")
var webpack = require('webpack')

module.exports = {
  context: __dirname,

  entry: {
    AuthApp: ['./drf_auth/reactjs/AuthApp', ],
    vendors: ['react', ],
  },

  output: {
      path: path.resolve('./drf_auth/static/bundles/'),
      filename: "[name].js"
  },

  externals: [
  ], // add all vendor libs

  plugins: [
    new webpack.optimize.CommonsChunkPlugin({
      names: ['vendors', ],
      minChunks: 2,
    })
  ], // add all common plugins here

  module: {
    loaders: [] // add all common loaders here
  },

  resolve: {
    modulesDirectories: ['node_modules', 'bower_components'],
    extensions: ['', '.js', '.jsx']
  },
}
