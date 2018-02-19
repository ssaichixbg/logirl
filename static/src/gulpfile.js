var gulp = require('gulp');
var sass = require('gulp-sass');
var minify = require('gulp-minify');
var shell = require('gulp-shell');

gulp.task('styles', function() {
    gulp.src('scss/**/*.scss')
        .pipe(sass().on('error', sass.logError))
        .pipe(gulp.dest('../css/'));
});

gulp.task('copy-js', function () {
    gulp.src('js/**/*.js')
        .pipe(gulp.dest('../js/'));
});

gulp.task('copy-minify-js', function () {
    gulp.src('js/**/*.js')
        .pipe(minify({
            ext:{
                min:'.js'
            },
            noSource: true
        }))
        .pipe(gulp.dest('../js/'));
});


gulp.task('collectstatic', shell.task([
    'python ../../manage.py collectstatic --noinput'
]));

gulp.task('default',function() {
    gulp.run('styles');
    gulp.run('copy-js');
    gulp.watch('scss/**/*.scss',['styles']);
    gulp.watch('js/**/*.js',['copy-js']);
});

gulp.task('prod', function () {
    gulp.run('styles');
    gulp.run('copy-minify-js');
    gulp.run('collectstatic');
});
