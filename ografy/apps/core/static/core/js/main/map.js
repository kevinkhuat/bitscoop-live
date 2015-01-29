function mapView(detailViewInst, dataInst, utilsInst, sessionInst, geocoder) {
	//Views
	function renderBase() {
		var tempData = 'Select an Event at left to see its details.';
		dataInst.loadTestData();
		renderContent();
		detailViewInst.renderContent(tempData, tempData, tempData, tempData, false);
	}

	function renderContent() {
		var map_framework = nunjucks.render('map/map.html');
		$('.data-view').html(map_framework);

		var mapInst = utilsInst.mapboxManager();
		var map = mapInst.map;
		var geoJSON = mapInst.geoJSON;

		geoJSON.features = [];

		var testData = JSON.parse(localStorage.eventData);
		console.log(testData);
		for (var index in testData) {
			geoJSON.features.push({
				// this feature is in the GeoJSON format: see geojson.org
				// for the full specification
				type: 'Feature',
				geometry: {
					type: 'Point',
					// coordinates here are in longitude, latitude order because
					// x, y is the standard for GeoJSON and many formats
					coordinates: testData[index].location
				},
				properties: {
					title: testData[index].name,
					description: testData[index].provider_name,
					// one can customize markers by adding simplestyle properties
					// https://www.mapbox.com/guides/an-open-platform/#simplestyle
					'marker-size': 'large',
					'marker-color': '#BE9A6B',
					'marker-symbol': 'post',
					datetime: testData[index].datetime,
					data: testData[index].data
				}
			});
		}

		map.featureLayer = L.mapbox.featureLayer(geoJSON).addTo(map);

		map.fitBounds(map.featureLayer.getBounds());

		map.featureLayer.on('click', function(e) {
			var feature = e.layer.feature;
			$('.detail-main-label').html(feature.properties.description);
			$('.detail-time-content').html(feature.properties.datetime);
			$('.detail-location-content').html(String(feature.geometry.coordinates));
			$('.detail-body-content').html(String(feature.properties.data));
		});
	}

	return {
		renderBase: renderBase,
		renderContent: renderContent
	};
}
