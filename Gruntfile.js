var MockBrowser = require('mock-browser').mocks.MockBrowser;
global.window = MockBrowser.createWindow();


module.exports = function(grunt) {
	grunt.initConfig({
		package: grunt.file.readJSON('package.json'),

		jscs: {
			all: {
				options: {
					config: 'config/jscs.json'
				},
				src: [
					'Gruntfile.js',
					'ografy/**/*.js',
					'!ografy/apps/demo/**/*.js',
					'!ografy/static/assets/lib/**/*.js',
					'!ografy/static/shared/js/templates.js',
					'!ografy/tests/**/*.js'
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
					'!ografy/apps/demo/**/*.js',
					'!ografy/static/assets/lib/**/*.js',
					'!ografy/static/shared/js/templates.js',
					'!ografy/tests/**/*.js'
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
				files: {
					'build/static/core/css/main-dark.css': 'ografy/apps/core/static/core/less/main-dark.less',
					'build/static/core/css/main-light.css': 'ografy/apps/core/static/core/less/main-light.less',
					'build/static/shared/css/site-dark.css': 'ografy/static/shared/less/site-dark.less',
					'build/static/shared/css/site-light.css': 'ografy/static/shared/less/site-light.less'
				}
			}
		},

		nunjucks: {
			precompile: {
				baseDir: 'ografy/apps/core/nunjucks/**/',
				src: 'ografy/apps/core/nunjucks/**/*',
				dest: 'build/static/shared/js/templates.js',
				options: {
					//env: require('./nunjucks-environment'),
					name: function(filename) {
						return filename.replace('ografy/apps/core/nunjucks/', '');
					}
				}
			}
		},

		watch: {
			nunjucks: {
				files: 'ografy/apps/core/nunjucks/**/*',
				tasks: ['nunjucks']
			},
			less: {
				files: [
					'ografy/apps/core/static/core/less/main.less',
					'ografy/apps/core/static/core/less/main-dark.less',
					'ografy/apps/core/static/core/less/main-light.less',
					'ografy/static/shared/less/site.less',
					'ografy/static/shared/less/site-dark.less',
					'ografy/static/shared/less/site-light.less'
				],
				tasks: ['less']
			}
		}
	});

	// Load grunt tasks from NPM packages
	require('load-grunt-tasks')(grunt);

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
