requirejs.config({
	baseUrl: '',
	paths: {
		lib: 'static/lib',
		main: 'static/core/js/main'
	},
	shim: {
		'main/base': {
			deps: ['main/detail', 'main/list', 'main/map', 'main/utils']
		},
		'main/detail': {
			deps: ['main/utils']
		},
		'main/list': {
			deps: ['main/utils']
		},
		'main/map': {
			deps: ['main/utils']
		},
		'main/utils': {
			deps: []
		}
	}
});

// Start the main app logic.
requirejs(['main/utils', 'main/detail', 'main/list', 'main/map', 'main/search', 'main/base'],
	function () {
		$(document).ready(function() {
			var base = baseView();
			var search = searchView();

			base.loadTestData(function() {
				base.render();
				base.bindNavigation();
			});

			search.bindEvents()
			//base.insertInitialData();
		});
	});