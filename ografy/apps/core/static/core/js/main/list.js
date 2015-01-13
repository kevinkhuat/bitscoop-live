//TEST_REMOVE
function getCoordinatesHack () {
	var trimmed = $.trim($(this).children('.list-item-location').html());
	var numberArray = trimmed.split(',').map(function(trimmed){return Number(trimmed);});
	return numberArray;
}

//Views
function renderListContent() {
	//Iterate through json and render list items using Nunjucks templates
	var list = nunjucks.render('static/core/templates/main/list/list.html');
	$('#content').html(list);

	var list_items = nunjucks.render('static/core/templates/main/list/list_elements.html', {event_data: data});
	$('#list-items').html(list_items);
}

$('.list-item').click(function() {
	$(this).siblings().removeClass('active');
	$(this).toggleClass('active');

	if ($(this).hasClass('active')) {
		var eventName = $(this).children('.list-item-name').html();
		var eventDate = $(this).children('.list-item-date').html();
		var eventLocation = $(this).children('.list-item-location').html();
		var eventData = $(this).children('.list-item-data').html();

		renderDetailContent(eventName, eventDate, eventLocation, eventData, true);
		updateDetailMap (getCoordinatesHack());

		//	var objectId = $(this).attr('id');
		//	$.ajax({
		//		url: '/opi/event/' + objectId,
		//		type: 'GET',
		//		dataType: 'json',
		//		headers: {"X-CSRFToken": csrftoken}
		//	}).done(function(data, xhr, response) {
		//
		//		$('.information-date-location .data').html(data.data);
		//		$('.information-date-location .location').html(data.location);
		//		$('.information-date-location .date').html(data.created);
		//		console.log(data);
		//		jsonMarkers["features"].push(
		//			{
		//				"geometry": {
		//					"coordinates": data.location,
		//					"type": "Point"
		//				},
		//				"properties": {
		//					"description": data.provider_name,
		//					"id": "marker-htbzzpcz1",
		//					"marker-color": "#1087bf",
		//					"marker-size": "large",
		//					"marker-symbol": "telephone",
		//					"title": "Call from Lisa",
		//					"data-type": "Call",
		//					"data-time": "5:31 pm",
		//					"data-image-uri": "{% static 'demo/img/lisa-portrait.jpg' %}"
		//				},
		//				"type": "Feature"
		//			});
		//			var map = L.mapbox.map('map', 'liambroza.hl4bi8d0', {
		//				zoomControl: false
		//				}).setView(data.location, 16);
		//			map.featureLayer = L.mapbox.featureLayer(jsonMarkers).addTo(map);
		//
		//	// find and store a variable reference to the list of filters
		//			var filters = document.getElementById('filters');
		//
		//			var typesObj = {}, types = [];
		//			var features = map.featureLayer.getGeoJSON().features;
		//			for (var i = 0; i < features.length; i++) {
		//				typesObj[features[i].properties['data-type']] = true;
		//}
		//	});
	}
	else {
		clearDetailContent();
		clearDetailMap();
	}
});