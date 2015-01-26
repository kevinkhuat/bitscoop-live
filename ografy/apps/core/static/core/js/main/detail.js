function detailView() {
	//Views
	function renderContent(eventName, eventDate, eventLocation, eventData, showMap) {
		showMap = typeof showMap !== 'undefined' ? showMap : true;

		var list_detail = nunjucks.render('static/core/templates/main/detail.html', {
			showMap: showMap
		});
		$('.base_detail').html(list_detail);

		//Populate content
		$('.detail-main-label').html(eventName);
		$('.detail-time-content').html(eventDate);
		$('.detail-location-content').html(eventLocation);
		$('.detail-body-content').html(eventData);
	}

	function updateContent(eventName, eventDate, eventLocation, eventData) {
		$('.detail-main-label').html(eventName);
		$('.detail-time-content').html(eventDate);
		$('.detail-location-content').html(eventLocation);
		$('.detail-body-content').html(eventData);
	}

	function clearContent() {
		$('.detail-main-label').html('Select an Event at left to see its details.');
		$('.detail-time-content').html('Select an Event at left to see its details.');
		$('.detail-location-content').html('Select an Event at left to see its details.');
		$('.detail-body-content').html('Select an Event at left to see its details.');
	}

	function updateMap(eventName, map, coordinates) {
		var geoJSON = {
			// this feature is in the GeoJSON format: see geojson.org
			// for the full specification
			type: 'Feature',
			geometry: {
				type: 'Point',
				// coordinates here are in longitude, latitude order because
				// x, y is the standard for GeoJSON and many formats
				coordinates: coordinates
			},
			properties: {
				title: eventName,
				description: 'pants',
				// one can customize markers by adding simplestyle properties
				// https://www.mapbox.com/guides/an-open-platform/#simplestyle
				'marker-size': 'large',
				'marker-color': '#BE9A6B',
				'marker-symbol': 'post'
			}
		};

		map.map.featureLayer.setGeoJSON(geoJSON);

		map.map.setView([coordinates[1], coordinates[0]], 13, {
			pan: {
				animate: true
			}
		});
	}

	function clearMap(map) {
		map.map.featureLayer.setGeoJSON([]);
	}

	return {
		renderContent: renderContent,
		updateContent: updateContent,
		clearContent: clearContent,
		updateMap: updateMap,
		clearMap: clearMap
	}
}
