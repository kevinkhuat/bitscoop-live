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

		nunjucks: {
			precompile: {
				baseDir: 'ografy/apps/core/static/core/templates/main/**/',
				src: 'ografy/apps/core/static/core/templates/main/**/*',
				dest: 'ografy/static/shared/js/templates.js',
				options: {
					//env: require('./nunjucks-environment'),
					name: function(filename) {
						return filename.replace('ografy/apps/core/static/core/templates/main/', '');
					}
				}
			}
		},

		watch: {
			nunjucks: {
	            files: 'ografy/apps/core/static/core/templates/main/**/*',
	            tasks: ['nunjucks']
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
