require.config({
	paths: {
		site: window.staticUrl + 'core/js/site.min',
		templates: window.staticUrl + 'core/js/templates.min',

		// Tools
		autoblur: window.staticUrl + 'core/js/tools/autoblur.min',
		debounce: window.staticUrl + 'core/js/tools/debounce.min',
		'deferred-debounce': window.staticUrl + 'core/js/tools/deferred-debounce.min',
		'main-menu': window.staticUrl + 'core/js/tools/main-menu.min',
		filters: window.staticUrl + 'core/js/tools/filters.min',
		'form-monitor': window.staticUrl + 'core/js/tools/form-monitor.min',
		icons: window.staticUrl + 'core/js/tools/icons.min',
		location: window.staticUrl + 'core/js/tools/location.min',
		type: window.staticUrl + 'core/js/tools/type.min',
		viewstate: window.staticUrl + 'core/js/tools/viewstate.min',

		// Components
		tooltip: window.staticUrl + 'core/js/components/tooltip.min',
		search: window.staticUrl + 'core/js/components/search.min',

		// Pages
		'account-settings': window.staticUrl + 'core/js/pages/settings/account.min',
		connections: window.staticUrl + 'core/js/pages/connections.min',
		'connection-settings': window.staticUrl + 'core/js/pages/settings/connections.min',
		explorer: window.staticUrl + 'explorer/js/pages/explorer.min',
		'location-settings': window.staticUrl + 'core/js/pages/settings/location.min',
		'profile-settings': window.staticUrl + 'core/js/pages/settings/profile.min',
		providers: window.staticUrl + 'core/js/pages/providers.min',
		'user-home': window.staticUrl + 'core/js/pages/user-home.min',

		// Explorer Utils
		'embed-content': window.staticUrl + 'explorer/js/embed-content.min',
		'external-actions': window.staticUrl + 'explorer/js/external-actions.min',

		// Explorer Components
		details: window.staticUrl + 'explorer/js/components/details.min',
		drawer: window.staticUrl + 'explorer/js/components/drawer.min',
		'grid-item': window.staticUrl + 'explorer/js/components/grid-item.min',
		'list-item': window.staticUrl + 'explorer/js/components/list-item.min',
		'map-list-item': window.staticUrl + 'explorer/js/components/map-list-item.min',

		// Explorer Object Context
		'object-context': window.staticUrl + 'explorer/js/objects/object-context.min',

		// Extensions
		'jquery-regexp-selector': window.staticUrl + 'lib/jquery/plugins/regexp-selector.min'
	}
});

requirejs.config({
	paths: {
		cartano: window.staticUrl + 'lib/cartano/cartano.min',  // Custom BitScoop external library.
		jutsu: window.staticUrl + 'lib/jutsu/jutsu.min',  // Custom BitScoop external library.

		bluebird: 'https://cdnjs.cloudflare.com/ajax/libs/bluebird/2.9.33/bluebird.min',  // https://github.com/petkaantonov/bluebird
		'deferred-ap': 'https://d1m45eggqhap5f.cloudfront.net/deferred-ap/0.0.1/deferred-ap-0.0.1.min',  // https://github.com/sjberry/deferred-ap
		jquery: 'https://code.jquery.com/jquery-2.1.4.min',  // https://github.com/jquery/jquery
		lodash: 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/3.10.1/lodash.min',  // https://github.com/lodash/lodash
		mapbox: 'https://api.tiles.mapbox.com/mapbox.js/v2.2.1/mapbox',  // https://github.com/mapbox/mapbox.js
		moment: 'https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.10.6/moment.min', //http://momentjs.com/
		nunjucks: 'https://d1m45eggqhap5f.cloudfront.net/nunjucks/1.3.3/nunjucks-1.3.3.min',  // https://github.com/mozilla/nunjucks
		twemoji: 'https://twemoji.maxcdn.com/twemoji.min',  // https://github.com/twitter/twemoji

		// Google Analytics Shim
		ga: 'https://www.google-analytics.com/analytics',

		// Plugins
		'jquery-cookie': 'https://cdnjs.cloudflare.com/ajax/libs/jquery-cookie/1.4.1/jquery.cookie.min',  // https://github.com/carhartl/jquery-cookie
		'jquery-deparam': 'https://d1m45eggqhap5f.cloudfront.net/jquery-deparam/0.4.2/jquery-deparam-0.4.2.min',  // https://github.com/AceMetrix/jquery-deparam
		'jquery-deserialize': 'https://d1m45eggqhap5f.cloudfront.net/jquery-deserialize/1.3.2/jquery.deserialize-1.3.2.min',  // https://github.com/kflorence/jquery-deserialize
		'jquery-mixitup': 'https://cdn.jsdelivr.net/jquery.mixitup/2.1.8/jquery.mixitup.min', //https://github.com/patrickkunka/mixitup
		'leaflet-awesome-markers': 'https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.min',  // https://github.com/lvoogdt/Leaflet.awesome-markers
		'leaflet-draw': 'https://api.tiles.mapbox.com/mapbox.js/plugins/leaflet-draw/v0.2.2/leaflet.draw',  // https://github.com/Leaflet/Leaflet.draw
		'leaflet-draw-drag': 'https://d1m45eggqhap5f.cloudfront.net/leaflet-draw-drag/0.1.2/Leaflet.draw.drag-0.1.2.min',  // https://github.com/w8r/Leaflet.draw.drag
		'leaflet-featuregroup-subgroup': 'https://cdn.rawgit.com/ghybs/Leaflet.FeatureGroup.SubGroup/master/leaflet.featuregroup.subgroup-src',  //https://github.com/ghybs/Leaflet.FeatureGroup.SubGroup
		'leaflet-fullscreen': 'https://api.tiles.mapbox.com/mapbox.js/plugins/leaflet-fullscreen/v0.0.4/Leaflet.fullscreen.min',  // https://github.com/Leaflet/Leaflet.fullscreen
		'leaflet-markercluster': 'https://api.tiles.mapbox.com/mapbox.js/plugins/leaflet-markercluster/v0.4.0/leaflet.markercluster',  // https://github.com/Leaflet/Leaflet.markercluster
		'leaflet-zoomslider': 'https://api.tiles.mapbox.com/mapbox.js/plugins/leaflet-zoomslider/v0.7.0/L.Control.Zoomslider',  // https://github.com/kartena/Leaflet.zoomslider
		minimodal: 'https://d3buhrktqnvzt8.cloudfront.net/minimodal/0.1.2/minimodal-0.1.2.min',  // https://github.com/sjberry/minimodal
		'mapbox-directions': 'https://api.tiles.mapbox.com/mapbox.js/plugins/mapbox-directions.js/v0.1.0/mapbox.directions' // https://github.com/mapbox/mapbox-directions.js
	},

	map: {
		'*': {
			'promises-ap': 'bluebird'
		}
	},

	shim: {
		ga: {
			exports: 'ga'
		},

		'jquery-deserialize': {
			deps: ['jquery']
		},

		'jquery-mixitup': {
			deps: ['jquery']
		},

		'leaflet-awesome-markers': {
			deps: ['leaflet']
		},

		'leaflet-draw': {
			deps: ['leaflet']
		},

		'leaflet-draw-drag': {
			deps: ['leaflet-draw']
		},

		'leaflet-fullscreen': {
			deps: ['leaflet']
		},

		'leaflet-markercluster': {
			deps: ['leaflet']
		},

		mapbox: {
			exports: 'L.mapbox'
		},

		'mapbox-directions': {
			deps: ['mapbox']
		},

		twemoji: {
			exports: 'twemoji'
		}

	}
});

define('leaflet', ['mapbox'], function(mapbox) {
	return window.L;
});
