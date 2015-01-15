function detailView() {
	//Views
	function renderContent(eventName, eventDate, eventLocation, eventData, showMap) {

		showMap = typeof showMap !== 'undefined' ? showMap : true;

		var list_detail = nunjucks.render('static/core/templates/main/detail.html', {showMap: showMap});
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
		clearMap(map);
		map.geoJSON["features"].push({
			"type": "Feature",
			"geometry": {
				"type": "Point",
				"coordinates": coordinates
			},
			"properties": {
				"title": eventName,
				"marker-symbol": "marker"
			}
		});

		var markers = new mapboxgl.GeoJSONSource({data: map.geoJSON});
		map.map.addSource('markers', markers);

		map.map.flyTo([coordinates[1], coordinates[0]], 14, 0, {speed: 3.0, curve: 0.5});
	}

	function clearMap(map) {
		if (typeof map.map.style.sources.markers !== 'undefined') {
			map.map.removeSource('markers');
		}

		map.geoJSON["features"] = [];

	}

	return {
		renderContent: renderContent,
		updateContent: updateContent,
		clearContent: clearContent,
		updateMap: updateMap,
		clearMap: clearMap
	}
}
