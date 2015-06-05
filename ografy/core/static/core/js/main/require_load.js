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
				'main/utils/model',
				'main/utils/mapUtil',
				'main/utils/session',
				'main/views/list',
				'main/filter/search'
			]
		},
		'main/detail': {
			deps: [
				'main/utils/mapUtil',
				'main/utils/model',
				'main/utils/session'
			]
		},
		'main/list': {
			deps: [
				'main/utils/mapUtil',
				'main/utils/model',
				'main/utils/session'
			]
		},
		'main/map': {
			deps: [
				'main/utils/mapUtil',
				'main/utils/model',
				'main/utils/session'
			]
		}
	}
});

// Start the main app logic.
requirejs([
		'main/utils/mapUtil',
		'main/utils/model',
		'main/utils/session',
		'main/utils/url',
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
