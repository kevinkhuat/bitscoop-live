require.config({
	paths: {
		location: window.staticUrl + 'core/js/search/location.min',
		scheduleMapper: window.staticUrl + 'core/js/search/scheduleMapper.min',
		search: window.staticUrl + 'new/search.min'
	}
});

requirejs.config({
	paths: {
		bluebird: 'https://cdnjs.cloudflare.com/ajax/libs/bluebird/2.9.33/bluebird.min',  // https://github.com/petkaantonov/bluebird
		'deferred-ap': 'https://d3qxpcy62pjlsy.cloudfront.net/deferred-ap/0.0.1/deferred-ap-0.0.1.min',  // https://github.com/sjberry/deferred-ap
		jquery: 'https://code.jquery.com/jquery-2.1.4.min',  // https://github.com/jquery/jquery
		lodash: 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/3.10.1/lodash.min',  // https://github.com/lodash/lodash
		mapbox: 'https://api.tiles.mapbox.com/mapbox.js/v2.2.1/mapbox',  // https://github.com/mapbox/mapbox.js
		nunjucks: 'https://d3qxpcy62pjlsy.cloudfront.net/nunjucks/1.3.3/nunjucks-1.3.3.min',  // https://github.com/mozilla/nunjucks

		// Plugins
		'jquery-cookie': 'https://cdnjs.cloudflare.com/ajax/libs/jquery-cookie/1.4.1/jquery.cookie.min',  // https://github.com/carhartl/jquery-cookie
		'jquery-deparam': 'https://d3qxpcy62pjlsy.cloudfront.net/jquery-deparam/0.4.2/jquery-deparam-0.4.2.min',  // https://github.com/AceMetrix/jquery-deparam
		'jquery-mixitup': 'https://cdn.jsdelivr.net/jquery.mixitup/2.1.8/jquery.mixitup.min', //https://github.com/patrickkunka/mixitup
		'leaflet-draw': 'https://api.tiles.mapbox.com/mapbox.js/plugins/leaflet-draw/v0.2.2/leaflet.draw',  // https://github.com/Leaflet/Leaflet.draw
		'leaflet-draw-drag': 'https://d3qxpcy62pjlsy.cloudfront.net/leaflet-draw-drag/0.1.2/Leaflet.draw.drag-0.1.2.min',  // https://github.com/w8r/Leaflet.draw.drag
		'leaflet-fullscreen': 'https://api.tiles.mapbox.com/mapbox.js/plugins/leaflet-fullscreen/v0.0.4/Leaflet.fullscreen.min',  // https://github.com/Leaflet/Leaflet.fullscreen
		// Returns an object if using RequireJS/AMD, otherwise publishes to window as `LGeo`.
		'leaflet-geodesy': 'https://api.tiles.mapbox.com/mapbox.js/plugins/leaflet-geodesy/v0.1.0/leaflet-geodesy',  // https://github.com/mapbox/leaflet-geodesy
		'leaflet-markercluster': 'https://api.tiles.mapbox.com/mapbox.js/plugins/leaflet-markercluster/v0.4.0/leaflet.markercluster',  // https://github.com/Leaflet/Leaflet.markercluster
		'leaflet-zoomslider': 'https://api.tiles.mapbox.com/mapbox.js/plugins/leaflet-zoomslider/v0.7.0/L.Control.Zoomslider',  // https://github.com/kartena/Leaflet.zoomslider
		'mapbox-directions': 'https://api.tiles.mapbox.com/mapbox.js/plugins/mapbox-directions.js/v0.1.0/mapbox.directions' // https://github.com/mapbox/mapbox-directions.js
	},

	map: {
		'*': {
			'promises-ap': 'bluebird'
		}
	},

	shim: {
		'jquery-mixitup': {
			deps: ['jquery']
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
		}
	}
});


define('leaflet', ['mapbox'], function(mapbox) {
	return window.L;
});
