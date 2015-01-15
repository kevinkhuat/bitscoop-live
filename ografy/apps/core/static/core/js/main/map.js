function mapView() {
	//Views
	function renderBase(map, baseData, mapUtil) {
		var tempData = 'Select an Event at left to see its details.';
		var detailViewInst = detailView();
		renderContent(map, baseData, mapUtil)
		detailViewInst.renderContent(tempData, tempData, tempData, tempData, false);
	}

	function renderContent(map, baseData, mapUtil) {
		var map_framework = nunjucks.render('static/core/templates/main/map/map.html');
		$('.content').html(map_framework);

		mapboxgl.accessToken = 'pk.eyJ1IjoiaGVnZW1vbmJpbGwiLCJhIjoiR3NrS0JMYyJ9.NUb5mXgMOIbh-r7itnVgmg';

		mapboxgl.util.getJSON('https://www.mapbox.com/mapbox-gl-styles/styles/outdoors-v6.json', function (err, style) {
			if (err) throw err;

			style.layers.push({
				"id": "markers",
				"type": "symbol",
				"source": "markers",
				"layout": {
					"icon-image": "{marker-symbol}-12",
					"text-field": "{title}",
					"text-font": "Open Sans Semibold, Arial Unicode MS Bold",
					"text-offset": [0, 0.6],
					"text-anchor": "top",
					"icon-allow-overlap": true,
					"text-allow-overlap": true
				},
				"paint": {
					"text-size": 12
				}
			});

			map.geoJSON["features"] = [];

			map.map = new mapboxgl.Map({
				container: 'mapbox',
				style: style
			});

			mapUtil.calculateFitBounds(map, baseData);
			mapUtil.placeMapPoints(map, baseData);

		});

	}

	return {
		renderBase: renderBase,
		renderContent: renderContent
	}
}
