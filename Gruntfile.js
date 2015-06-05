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
				files: {
					'artifacts/core/css/main-dark.css': 'ografy/core/static/core/less/main-dark.less',
					'artifacts/core/css/main-light.css': 'ografy/core/static/core/less/main-light.less',
					'artifacts/shared/css/site-dark.css': 'ografy/static/shared/less/site-dark.less',
					'artifacts/shared/css/site-light.css': 'ografy/static/shared/less/site-light.less'
				}
			}
		},

		nunjucks: {
			precompile: {
				baseDir: 'ografy/core/nunjucks/core/**/',
				src: 'ografy/core/nunjucks/core/**/*',
				dest: 'artifacts/shared/js/templates.js',
				options: {
					//env: require('./nunjucks-environment'),
					name: function(filename) {
						return filename.replace('ografy/core/nunjucks/core/', '');
					}
				}
			}
		},

		watch: {
			nunjucks: {
				files: 'ografy/core/nunjucks/**/*',
				tasks: [
					'nunjucks'
				]
			},
			less: {
				files: [
					'ografy/core/static/core/less/main-dark.less',
					'ografy/core/static/core/less/main-light.less',
					'ografy/core/static/core/less/main.less',
					'ografy/static/shared/less/site-dark.less',
					'ografy/static/shared/less/site-light.less',
					'ografy/static/shared/less/site.less'
				],
				tasks: [
					'less'
				]
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
