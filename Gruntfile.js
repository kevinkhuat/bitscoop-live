var path = require('path');

var MockBrowser = require('mock-browser').mocks.MockBrowser;


global.window = MockBrowser.createWindow();


module.exports = function(grunt) {
	grunt.initConfig({
		package: grunt.file.readJSON('package.json'),

		clean: {
			artifacts: 'artifacts',
			build: 'build'
		},

		jscs: {
			all: {
				options: {
					config: 'config/jscs.json'
				},
				src: [
					'Gruntfile.js',
					'ografy/**/*.js',
					'!ografy/static/lib/**/*.js'
				],
				gruntfile: 'Gruntfile.js'
			}
		},

		jshint: {
			all: {
				options: {
					jshintrc: 'config/jshint.json',
					reporter: require('jshint-stylish')
				},
				src: [
					'Gruntfile.js',
					'ografy/**/*.js',
					'!ografy/static/lib/**/*.js'
				]
			}
		},

		jsonlint: {
			amdsync: {
				src: 'config/amdsync.exports.json'
			},
			jscs: {
				src: 'config/jscs.json'
			},
			jshint: {
				src: 'config/jslint.json'
			},
			package: {
				src: 'package.json'
			}
		},

		less: {
			development: {
				expand: true,
				src: 'ografy/**/*.less',
				dest: 'artifacts',
				ext: '.css',
				rename: (function() {
					var delimiter, names;

					delimiter = 'static' + path.sep;
					names = {};

					return function(dest, less) {
						var i, components, filename, src;

						src = less.replace(/\.css$/, '.less');

						if (~(i = less.indexOf(delimiter))) {
							filename = path.join(dest, less.slice(i + delimiter.length));
						}
						else {
							filename = path.join(dest, less);
						}

						filename = filename.split(path.sep).map(function(d, i) {
							return (d === 'less') ? 'css' : d;
						}).join(path.sep);

						if (names.hasOwnProperty(filename)) {
							grunt.log.warn('Name collison on less file "' + filename + '":\n\tOld: ' + names[filename] + '\n\tNew: ' + src);
						}

						names[filename] = src;

						return filename;
					};
				})()
			}
		},

		nunjucks: {
			precompile: {
				src: [
					'ografy/nunjucks/**/*.html',
					'ografy/core/nunjucks/**/*.html',
					'ografy/{apps,contrib,lib}/*/nunjucks/**/*.html'
				],
				dest: 'artifacts/shared/js/templates.js',
				options: {
					name: (function() {
						var delimiter, names;

						delimiter = 'nunjucks' + path.sep;
						names = {};

						return function(filename) {
							var i, template;

							if (~(i = filename.indexOf(delimiter))) {
								template = filename.slice(i + delimiter.length);
							}

							template = template.replace(new RegExp(path.sep, 'g'), '/');

							if (names.hasOwnProperty(template)) {
								grunt.log.warn('Name collison on nunjucks template "' + template + '":\n\tOld: ' + names[template] + '\n\tNew: ' + filename);
							}

							names[template] = filename;

							return template;
						};
					})()
				}
			}
		},

		watch: {
			nunjucks: {
				files: '<%= nunjucks.precompile.src %>',
				tasks: 'nunjucks'
			},
			less: {
				files: '<%= less.development.src %>',
				tasks: 'less'
			}
		}
	});

	// Load grunt tasks from NPM packages
	require('load-grunt-tasks')(grunt);

	grunt.registerTask('build', [
		'less',
		'nunjucks'
	]);

	grunt.registerTask('lint', [
		'jsonlint:jshint',
		'jshint',
		'jsonlint:jscs',
		'jscs'
	]);

	// Default grunt
	grunt.registerTask('default', [
		'jsonlint:package',
		'lint'
	]);
};
