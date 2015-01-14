function detailView() {
	//Views
	function renderContent(eventName, eventDate, eventLocation, eventData, showMap) {

		showMap = typeof showmap !== 'undefined' ? showMap : true;

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

	function updateMap(map, coordinates) {
		clearMap();
		geoJSON["features"] = {
			"type": "Feature",
			"geometry": {
				"type": "Point",
				"coordinates": coordinates
			},
			"properties": {
				"title": $(this).children('.list-item-name').html(),
				"marker-symbol": "marker"
			}
		};

		var markers = new mapboxgl.GeoJSONSource({data: geoJSON});
		map.addSource('markers', markers);

		map.flyTo([coordinates[1], coordinates[0]], 12, 0, {speed: 3.0, curve: 0.5});
	}

	function clearMap(map) {
		map.removeSource('markers');
		geoJSON["features"] = {};
	}

	return {
		renderContent: renderContent,
		updateContent: updateContent,
		clearContent: clearContent,
		updateMap: updateMap,
		clearMap: clearMap
	}
}
