var path    = require('path');
var webpack = require('webpack');

module.exports = {
  devtool: 'inline-source-map',
  entry: './lib/app.js',
  output: {
    path: __dirname,
    filename: 'bundle.js'
  },
  module: {
    loaders: [{
      test: /^((?!\.config\.).)*\.(js|jsx)$/,
      loader: 'babel',
      exclude: /(node_modules|bower_components)/,
      query: {
        cacheDirectory: true,
        presets: ['es2015', 'react'],
      }
    },
      { test: /bootstrap\/js\//,                loader: 'imports?jQuery=jquery' },
      { test: /\.less$/,                        loader: "style-loader!css-loader!less-loader" },
      { test: /\.(png|jpg)$/,                   loader: "url-loader?prefix=images/&limit=5000" },
      { test: /\.woff(\?v=\d+\.\d+\.\d+)?$/,    loader: "url?limit=10000&minetype=application/font-woff" },
      { test: /\.woff2(\?v=\d+\.\d+\.\d+)?$/,   loader: "url?limit=10000&minetype=application/font-woff" },
      { test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/,     loader: "url?limit=10000&minetype=application/octet-stream" },
      { test: /\.eot(\?v=\d+\.\d+\.\d+)?$/,     loader: "file" },
      { test: /\.svg(\?v=\d+\.\d+\.\d+)?$/,     loader: "url?limit=10000&minetype=image/svg+xml" },
      { test: /\.otf$/,                         loader: "file-loader?prefix=font/" },
    ]
  },
  externals: {
  },
  resolve: {
    alias: {
      styles: __dirname + '/styles',
      images: __dirname + '/images',
      vanth : __dirname + '/lib',
      widget: __dirname + '/lib/widget',
      tests : __dirname + '/tests',
    },
    extensions: ['', '.js', '.jsx', '.less', '.png', '.jpg']
  },
  plugins: [
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery",
      "window.jQuery": "jquery",
      "root.jQuery": "jquery",
    })
  ]
};
