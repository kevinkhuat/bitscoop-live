requirejs.config({
	baseUrl: '',
	paths: {
		lib: 'static/lib',
		staticjs: 'static/shared/js',
		main: 'static/core/js/main'
	},
	shim: {
		'main/base': {
			deps: [
				'main/detail',
				'main/views/list',
				'main/views/map',
				'main/utls/model',
				'main/utls/mapUtil',
				'main/utls/session',
				'main/utls/sortBar',
				'main/views/list',
				'main/filter/search'
			]
		},
		'main/detail': {
			deps: [
				'main/utls/mapUtil',
				'main/utls/model',
				'main/utls/session'
			]
		},
		'main/list': {
			deps: [
				'main/utls/mapUtil',
				'main/utls/model',
				'main/utls/session'
			]
		},
		'main/map': {
			deps: [
				'main/utls/mapUtil',
				'main/utls/model',
				'main/utls/session'
			]
		}
	}
});

// Start the main app logic.
requirejs([
		'main/utls/mapUtil',
		'main/utls/model',
		'main/utls/session',
		'main/utls/sortBar',
		'main/utls/url',
		'main/detail',
		'main/views/list',
		'main/views/map',
		'main/filter/search',
		'main/filter/objects/data/metadata',
		'main/filter/objects/event/metadata',
		'main/filter/objects/message/metadata',
		'main/base',
		'static/shared/js/templates.js'
	],

	function() {
		$(document).ready(function() {
			var base = baseView();

			base.render();
		});
	});
