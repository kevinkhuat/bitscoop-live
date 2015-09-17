var path = require('path');

var MockBrowser = require('mock-browser').mocks.MockBrowser;


global.window = MockBrowser.createWindow();


module.exports = function(grunt) {
	grunt.initConfig({
		package: grunt.file.readJSON('package.json'),
		banner: '/**\n * @license\n * Copyright (c) <%= grunt.template.today("yyyy") %> Ografy, LLC.\n * All rights reserved.\n */',

		clean: {
			artifacts: 'artifacts',
			build: 'build',
			predeploy: [
				'build/static/**/*.less',
				'build/static/**/*.js',
				'build/static/lib/icomoon/selection.json',
				'!build/static/rest_framework/**/*',
				'!build/static/**/*.min.js'
			]
		},

		cleanempty: {
			build: {
				options: {
					files: false
				},
				src: 'build/**/*'
			}
		},

		copy: {
			js: {
				files: {
					'artifacts/core/js/search/location.min.js': 'ografy/core/static/core/js/search/location.js',
					'artifacts/new/new.min.js': 'ografy/apps/new/static/new/new.js',
					'artifacts/shared/js/paths.min.js': 'ografy/static/shared/js/paths.js',
					'artifacts/core/js/search/scheduleMapper.min.js': 'ografy/core/static/core/js/search/scheduleMapper.js',
					'artifacts/new/search.min.js': 'ografy/apps/new/static/new/search.js',
					'artifacts/shared/js/site.min.js': 'ografy/static/shared/js/site.js',
					'artifacts/shared/js/tooltip.min.js': 'ografy/static/shared/js/tooltip.js',
					'artifacts/lib/cartano/cartano.min.js': 'ografy/static/lib/cartano/cartano.js',
					'artifacts/lib/jutsu/jutsu.min.js': 'ografy/static/lib/jutsu/jutsu.js'
				}
			},
			nunjucks: {
				files: {
					'artifacts/shared/js/templates.min.js': 'artifacts/shared/js/templates.js'
				}
			}
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

		rename: {
			deploy: {
				src: 'build/static',
				dest: 'build/' + new Date().getTime()
			}
		},

		uglify: {
			dist: {
				files: [
					'<%= copy.js.files %>',
					'<%= copy.nunjucks.files %>'
				]
			}
		},

		usebanner: {
			dist: {
				options: {
					position: 'top',
					banner: '<%= banner %>'
				},
				files: {
					src: [
						'build/**/*.{css,js}',
						'!build/static/lib/**/*',
						'build/static/lib/{cartano,jutsu}/**/*.{css,js}',
						'!build/static/rest_framework/**/*'
					]
				}
			}
		},

		watch: {
			nunjucks: {
				files: '<%= nunjucks.precompile.src %>',
				tasks: ['nunjucks', 'copy:nunjucks']
			},
			less: {
				files: '<%= less.development.src %>',
				tasks: 'less'
			},
			js: {
				files: [
					'ografy/{apps,core,lib,static}/**/*.js',
					'!ografy/{apps,core,lib,static}/**/*.min.js'
				],
				tasks: 'copy:js'
			}
		}
	});

	// Load grunt tasks from NPM packages
	require('load-grunt-tasks')(grunt);

	grunt.registerTask('build', [
		'less',
		'nunjucks',
		'uglify'
	]);

	grunt.registerTask('deploy', [
		'clean:predeploy',
		'cleanempty:build',
		'usebanner:dist',
		'rename:deploy'
	]);

	grunt.registerTask('devel', [
		'less',
		'nunjucks',
		'copy'
	]);

	grunt.registerTask('lint', [
		'jsonlint:jshint',
		'jshint',
		'jsonlint:jscs',
		'jscs'
	]);

	grunt.registerTask('default', [
		'jsonlint:package',
		'lint',
		'build'
	]);
};
