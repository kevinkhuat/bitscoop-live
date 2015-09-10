var path = require('path');

var MockBrowser = require('mock-browser').mocks.MockBrowser;


global.window = MockBrowser.createWindow();


module.exports = function(grunt) {
	grunt.initConfig({
		package: grunt.file.readJSON('package.json'),
		banner: '/**\n * @license\n * Copyright (c) <%= grunt.template.today("yyyy") %> BitScoop Labs, Inc.\n * All rights reserved.\n */',

		clean: {
			artifacts: 'artifacts',
			build: 'build',
			predeploy: [
				'artifacts/**/*.{css,js,less}',
				'artifacts/lib/icomoon/selection.json',
				'!artifacts/**/*.min.{css,js}'
			]
		},

		cleanempty: {
			target: {
				options: {
					files: false
				},
				src: 'artifacts/**/*'
			}
		},

		copy: {
			collectstatic: {
				files: [
					{
						expand: true,
						cwd: 'ografy/static/',
						src: '**',
						dest: 'artifacts/'
					},
					{
						expand: true,
						cwd: 'ografy/core/static/',
						src: '**',
						dest: 'artifacts/'
					},
					{
						expand: true,
						cwd: 'ografy/apps/explorer/static/',
						src: '**',
						dest: 'artifacts/'
					}
				]
			},
			deploy: {
				files: [
					{
						expand: true,
						cwd: 'artifacts/',
						src: '**',
						dest: 'build/' + new Date().getTime()
					}
				]
			},
			minify: {
				files: [
					'<%= cssmin.target.files %>',
					'<%= uglify.target.files %>'
				]
			}
		},

		cssmin: {
			target: {
				files: [
					{
						expand: true,
						cwd: 'artifacts/',
						src: '**/*.css',
						dest: 'artifacts/',
						ext: '.min.css'
					}
				]
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
			target: {
				options: {
					paths: ['artifacts/']
				},
				files: {
					'artifacts/core/css/site.css': 'artifacts/core/less/site.less'
				}
			}
		},

		nunjucks: {
			target: {
				src: [
					'ografy/nunjucks/**/*.html',
					'ografy/core/nunjucks/**/*.html',
					'ografy/{apps,contrib,lib}/*/nunjucks/**/*.html'
				],
				dest: 'artifacts/core/js/templates.js',
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

		uglify: {
			target: {
				files: [
					{
						expand: true,
						cwd: 'artifacts/',
						src: '**/*.js',
						dest: 'artifacts/',
						ext: '.min.js'
					}
				]
			}
		},

		usebanner: {
			target: {
				options: {
					position: 'top',
					banner: '<%= banner %>'
				},
				files: {
					src: [
						'artifacts/**/*.{css,js}',
						'!artifacts/lib/**/*',
						'artifacts/lib/{cartano,jutsu}/**/*.{css,js}',
						'artifacts/lib/requirejs/config/*.js'
					]
				}
			}
		},

		watch: {
			nunjucks: {
				files: '<%= nunjucks.precompile.src %>',
				tasks: ['nunjucks', 'copy:minify']
			},
			static: {
				files: '<%= copy.collectstatic.files %>',
				tasks: ['copy:collecstatic', 'less', 'copy:minify']
			}
		}
	});

	// Load grunt tasks from NPM packages
	require('load-grunt-tasks')(grunt);

	grunt.registerTask('build', [
		'copy:collectstatic',
		'less',
		'nunjucks',
		'cssmin',
		'uglify',
		'clean:predeploy',
		'cleanempty',
		'usebanner',
		'copy:deploy'
	]);

	grunt.registerTask('devel', [
		'copy:collectstatic',
		'less',
		'nunjucks',
		'copy:minify'
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
