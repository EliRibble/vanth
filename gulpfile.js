var htmlreplace      = require('gulp-html-replace');
var gulp             = require("gulp");
var gutil            = require("gulp-util");
var karma            = require("karma");
var minimist         = require('minimist');
var path             = require('path');
var rev              = require('gulp-rev');
var shell            = require('gulp-shell');
var sprintf          = require('sprintf');
var webpack          = require("webpack");
var webpackConfig    = require("./webpack.config.js");
var WebpackDevServer = require("webpack-dev-server");

var knownOptions = {
  string: 'env',
  string: 'region',
  string: 'bucket',
  string: 'cloudfront',
  string: 'colors',
  default: { bucket: null, cloudfront: null, colors: true, env: null, region: null }
};
var options = minimist(process.argv.slice(2), knownOptions);
if(options.env && options.env !== 'production' && options.env !== 'development') {
  throw new Error('Unknown environment config: ' + options.env);
}

if(options.colors === true || options.colors == 'true' || options.colors == 'yes') {
  options.colors = true;
} else {
  options.colors = false;
}

gulp.task('build', ['clean', 'build:webpack']);
gulp.task('clean', shell.task(['rm -rf build']));
gulp.task('default', ['webpack-dev-server']);
gulp.task('publish', ['clean', 'build', 'publish:assets', 'publish:assets:index', 'publish:index']);

gulp.task("build:webpack", ['clean'], function(callback) {
  var config = Object.create(webpackConfig);
  var SaveAssetsJson = require('assets-webpack-plugin');

  config.output = {
    filename  : "bundle.js",
    path      : path.join(__dirname, 'build'),
    publicPath: "./"
  };

  config.plugins = (config.plugins || []).concat(
    new webpack.DefinePlugin({
      "process.env": {
        "NODE_ENV": JSON.stringify(options.env)
      }
    }),
    new webpack.optimize.DedupePlugin(),
    new webpack.optimize.UglifyJsPlugin(),
    new SaveAssetsJson()
  );

  webpack(config, function(err, stats) {
    if(err) throw new gutil.PluginError("webpack:build", err);
    gutil.log("[webpack:build]", stats.toString({
      colors: options.colors
    }));
    callback();
  });
});

gulp.task("webpack-dev-server", function(callback) {
  var host = process.env.HOST || "localhost";
  var port = parseInt(process.env.PORT, 10) || 8080;
  var config = Object.create(webpackConfig);
  config.devtool = "eval";
  config.debug = true;

  new WebpackDevServer(webpack(config), {
    stats: {
      colors: true
    }
  }).listen(port, host, function(err) {
    if(err) throw new gutil.PluginError("webpack-dev-server", err);
    gutil.log("[webpack-dev-server]", sprintf("http://%s:%d/webpack-dev-server/index.html", host, port));
  });
});

gulp.task("test", function(done) {
  var server = new karma.Server({
    configFile: __dirname + "/karma.conf.js",
    singleRun: true,
  }, done);
  server.start();
});

gulp.task("tdd", function(done) {
  var server = new karma.Server({
    configFile: __dirname + "/karma.conf.js",
  }, done);
  server.start();
});
