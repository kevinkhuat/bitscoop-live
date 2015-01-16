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

		L.mapbox.accessToken = 'pk.eyJ1IjoiaGVnZW1vbmJpbGwiLCJhIjoiR3NrS0JMYyJ9.NUb5mXgMOIbh-r7itnVgmg';
		map.map = L.mapbox.map('mapbox', 'liambroza.hl4bi8d0').setView([40.82, -73.59], 9);

		map.geoJSON["features"] = [];

		for (index in baseData) {
			map.geoJSON["features"].push({
				// this feature is in the GeoJSON format: see geojson.org
				// for the full specification
				type: 'Feature',
				geometry: {
					type: 'Point',
					// coordinates here are in longitude, latitude order because
					// x, y is the standard for GeoJSON and many formats
					coordinates: baseData[index].location
				},
				properties: {
					title: baseData[index].name,
					description: baseData[index].provider_name,
					// one can customize markers by adding simplestyle properties
					// https://www.mapbox.com/guides/an-open-platform/#simplestyle
					'marker-size': 'large',
					'marker-color': '#BE9A6B',
					'marker-symbol': 'post',
					'datetime': baseData[index].datetime,
					'data': baseData[index].data
				}
			})
		}

		map.map.featureLayer = L.mapbox.featureLayer(map.geoJSON).addTo(map.map);

		map.map.fitBounds(map.map.featureLayer.getBounds());

		map.map.featureLayer.on('click', function(e) {
			var feature = e.layer.feature;
			console.log(feature.geometry.coordinates);
			$('.detail-main-label').html(feature.properties.description);
			$('.detail-time-content').html(feature.properties.datetime);
			$('.detail-location-content').html(String(feature.geometry.coordinates));
			$('.detail-body-content').html(String(feature.properties.data));

		});
	}

	return {
		renderBase: renderBase,
		renderContent: renderContent
	}
}
