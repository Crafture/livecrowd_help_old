'use strict';
// INCLUDE GULP AND MODULES
var gulp = require('gulp'), 
	concat = require('gulp-concat'),
	minify = require('gulp-minify'),
	rename = require('gulp-rename'),
	sass = require('gulp-sass'),
	cleanCSS = require('gulp-clean-css'),
	autoPrefixer = require('gulp-autoprefixer');

// MINIFY GULP TASK :: gulp minify
gulp.task("minify", function() {
	return gulp.src("development/js/**/*.js")
		.pipe(concat("bundle.js"))
		.pipe(minify())
		.pipe(rename("scripts.min.js"))
		.pipe(gulp.dest("js"));
});	

// SASS to CSS COMPILE AND MINIFY GULP TASK :: gulp sass
gulp.task("sass", function() {
	return gulp.src("development/scss/styles.scss")
		.pipe(sass())
		.pipe(cleanCSS({compatibility:"ie8"}))
		.pipe(autoPrefixer())
		.pipe(gulp.dest("css"));
});

// DEFAULT GULP TASK :: gulp
gulp.task("default", ["minify", "sass"]);

// WATCH GULP TASK :: gulp watch
gulp.task("watch", function() {
	gulp.watch('development/scss/**/*.scss', ['sass']);
	gulp.watch('development/js/**/*.js', ['minify']);
});