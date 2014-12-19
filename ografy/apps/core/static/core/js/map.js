function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


	var jsonMarkers = {
		"features": [

		],
		"id": "liambroza.hl46f2ok",
		"type": "FeatureCollection"
	};

	var csrftoken = getCookie('csrftoken');
	$.ajax({
		url: '/opi/event',
		type: 'GET',
		dataType: 'json',
		headers: {"X-CSRFToken": csrftoken}
	}).done(function(data, xhr, response) {
		for (var i=0; i < data.length; i++) {
			jsonMarkers["features"].push(
				{
					"geometry": {
						"coordinates": data[i].location,
						"type": "Point"
					},
					"properties": {
						"description": data[i].provider_name,
						"id": "marker-htbzzpcz1",
						"marker-color": "#1087bf",
						"marker-size": "large",
						"marker-symbol": "telephone",
						"title": "Call from Lisa",
						"data-type": "Call",
						"data-time": "5:31 pm",
						"data-image-uri": "{% static 'demo/img/lisa-portrait.jpg' %}"
					},
					"type": "Feature"
				}
			);
		}
		var map = L.mapbox.map('map', 'liambroza.hl4bi8d0', {
			zoomControl: false
		}).setView([40.78, -73.88], 16);
		map.featureLayer = L.mapbox.featureLayer(jsonMarkers).addTo(map);

	// find and store a variable reference to the list of filters
			var filters = document.getElementById('filters');

			var typesObj = {}, types = [];
			var features = map.featureLayer.getGeoJSON().features;
			for (var i = 0; i < features.length; i++) {
				typesObj[features[i].properties['data-type']] = true;
		}
	}).fail(function() {
		console.log('FAILED');
	});