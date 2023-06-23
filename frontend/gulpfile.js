const { src, dest, watch, parallel, series } = require("gulp");
const sass = require("gulp-sass")(require("sass"));
const concat = require("gulp-concat");
const clean = require("gulp-clean");
const fileinclude = require("gulp-file-include");
const autoprefixer = require("gulp-autoprefixer");
const sourcemaps = require("gulp-sourcemaps");
const cssnano = require("gulp-cssnano");
const gulpif = require("gulp-if");
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
  },
  dist: {
    html: templatesPath + "core/",
    css: staticPath + "css/",
    fonts: staticPath + "fonts/",
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

}

exports.html = html;
exports.styles = styles;
exports.watching = watching;
exports.cleanFolders = cleanFolders;
exports.fonts = fonts;
const build = series(
  cleanFolders,
  parallel(fonts, html, styles,)
);
const dev = series(
  cleanFolders,
  parallel(fonts, html, styles, watching)
);

exports.default = isProd ? build : dev;
