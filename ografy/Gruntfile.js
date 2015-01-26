var MockBrowser = require('mock-browser').mocks.MockBrowser;
global.window = MockBrowser.createWindow();


module.exports = function(grunt) {
	grunt.initConfig({
		package: grunt.file.readJSON('package.json'),

		amdsync: {
			all: {
				options: {
					baseUrl: '.',
					name: '<%= package.name %>',
					exports: grunt.file.readJSON('config/amdsync.exports.json')
				},
				src: 'src/**/*.js',
				dest: 'artifacts/amdsync/<%= package.name %>.js'
			}
		},

		jscs: {
			all: {
				options: {
					config: 'config/jscs.json'
				},
				src: [
					'Gruntfile.js',
					'src/**/*.js',
					'apps/**/*.js',
					'!apps/demo/**/*.js',
					'static/**/*.js',
					'!static/lib/**/*.js'
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
					'src/**/*.js',
					'apps/**/*.js',
					'!apps/demo/**/*.js',
					'static/**/*.js',
					'!static/lib/**/*.js'
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

		watch: {
			files: 'src/**/*.js',
			tasks: 'build'
		}
	});

	// Load grunt tasks from NPM packages
	require('load-grunt-tasks')(grunt);

	grunt.registerTask('build', [
		'jsonlint:amdsync',
		'amdsync'
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
		'lint',
		'build'
	]);
};
