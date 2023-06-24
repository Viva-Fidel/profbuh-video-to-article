const { src, dest, watch, parallel, series } = require("gulp");
const sass = require("gulp-sass")(require("sass"));
const concat = require("gulp-concat");
const clean = require("gulp-clean");
const fileinclude = require("gulp-file-include");
const autoprefixer = require("gulp-autoprefixer");
const sourcemaps = require("gulp-sourcemaps");
const cssnano = require("gulp-cssnano");
const gulpif = require("gulp-if");
const imagemin = require("gulp-imagemin");
const TerserPlugin = require("terser-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const webpack = require("webpack-stream");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");

const isProd = process.argv.includes("--production");

const isDev = !isProd;

/* Paths */
const frontendPath = "./";
const templatesPath = "../templates/";
const staticPath = "../static/";

const paths = {
  frontend: {
    indexHtml: frontendPath + "index.html",
    partials: frontendPath + "html/partials/**/*.html",
    scss: frontendPath + "styles/style.scss",
    fonts: frontendPath + "fonts/**/*.{woff2,woff}",
    images: frontendPath + "images/**/*.{jpeg,png,svg,jpg,webp,ico,gif}",
    assets: frontendPath + "assets/**/*",
    js: frontendPath + "js/**/*.js",

  },
  dist: {
    html: templatesPath + "core/",
    css: staticPath + "css/",
    fonts: staticPath + "fonts/",
    images: staticPath + "images/",
    assets: staticPath + "assets/",
    js: staticPath + "js/",

  },
};

/* index.html task */
const html = () => {
  return src([paths.frontend.indexHtml])
    .pipe(
      fileinclude({
        prefix: "@@",
        basepath: "@file",
      })
    )
    .pipe(dest(paths.dist.html))
};

/* styles task */
const styles = () => {
  return src(paths.frontend.scss)
    .pipe(gulpif(isDev, sourcemaps.init()))
    .pipe(sass(gulpif(isProd, { outputStyle: "compressed" })))
    .pipe(
      cssnano(
        gulpif(isProd, {
          zindex: false,
          discardComments: {
            removeAll: true,
          },
        })
      )
    )
    .pipe(gulpif(isProd, autoprefixer({cascade: false})))
    .pipe(concat("style.min.css"))
    .pipe(dest(paths.dist.css))
    .pipe(gulpif(isDev,sourcemaps.write("./")))
    .pipe(dest(paths.dist.css))
};

/* fonts task */
const fonts = () => {
  return src(paths.frontend.fonts).pipe(dest(paths.dist.fonts));
};

/* images task */

const images = () => {
  return src(paths.frontend.images)
    .pipe(
      imagemin({
        progressive: true,
        svgoPlugins: [{ removeViewBox: false }],
        interlaced: true,
        optimizationLevel: 3,
      })
    )
    .pipe(dest(paths.dist.images))
};
/* assets task */

const assetsInclude = () => {
  return src(paths.frontend.assets).pipe(dest(paths.dist.assets));
};
/* scripts task */
const scripts = () => {
  return src(paths.frontend.js)
    .pipe(
      webpack({
        mode: isProd ? "production" : "development",
        output: {
          filename: "main.js",
        },
        module: {
          rules: [
            {
              test: /\.js$/,
              exclude: /node_modules/,
              use: {
                loader: "babel-loader",
                options: {
                  presets: ["@babel/preset-env"],
                },
              },
            },
            {
              test: /\.css$/,
              use: [{ loader: MiniCssExtractPlugin.loader }, "css-loader"],
            },
          ],
        },
        optimization: {
          minimize: true,
          minimizer: [
            new TerserPlugin({
              terserOptions: {
                format: {
                  comments: false,
                },
              },
              extractComments: false,
            }),
            new CssMinimizerPlugin({
              minimizerOptions: {
                preset: [
                  "default",
                  {
                    discardComments: { removeAll: true },
                  },
                ],
              },
            }),
          ],
        },
        plugins: [
          new MiniCssExtractPlugin({
            filename: "../css/libs.css",
          }),
        ],
      })
    )
    .pipe(dest(paths.dist.js))
};
const cleanFolders = () => {
  return src(["../templates/core/*", "../static/*"], { read: false }).pipe(
    clean({ force: true })
  );
};

function watching() {
  watch(frontendPath + "styles/**/*.scss", styles);
  watch(frontendPath + "**/*.html", html);
  watch(paths.frontend.partials, html);
  watch(frontendPath + "fonts/**/*.{woff2,woff}", fonts);
  watch(frontendPath + "images/**/*.{jpeg,png,svg,jpg,webp,ico,gif}", images);
  watch(frontendPath + "js/**/*.js", scripts);

}

exports.html = html;
exports.styles = styles;
exports.images = images;
exports.watching = watching;
exports.cleanFolders = cleanFolders;
exports.fonts = fonts;
exports.scripts = scripts;
exports.assetsInclude = assetsInclude;
const build = series(
  cleanFolders,
  parallel(fonts, html,scripts, styles,images,assetsInclude)
);
const dev = series(
  cleanFolders,
  parallel(fonts, html, styles,scripts, watching,images,assetsInclude)
);

exports.default = isProd ? build : dev;
