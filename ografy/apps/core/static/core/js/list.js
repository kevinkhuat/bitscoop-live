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

$(document).ready(function() {
	var csrftoken = getCookie('csrftoken');

	// filter items on button click
	$('.list-item').click(function() {
		$(this).siblings().removeClass('active');
		$(this).toggleClass('active');

		if ($(this).hasClass('active')) {
			$('.information').removeClass('invisible');

			var objectId = $(this).attr('id');
			$.ajax({
				url: '/opi/event/' + objectId,
				type: 'GET',
				dataType: 'json',
				headers: {"X-CSRFToken": csrftoken}
			}).done(function(data, xhr, response) {

				$('.information-date-location .data').html(data.data);
				$('.information-date-location .location').html(data.location);
				$('.information-date-location .date').html(data.created);
				console.log(data);
				jsonMarkers["features"].push(
					{
						"geometry": {
							"coordinates": data.location,
							"type": "Point"
						},
						"properties": {
							"description": data.provider_name,
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
					});
					var map = L.mapbox.map('map', 'liambroza.hl4bi8d0', {
						zoomControl: false
						}).setView(data.location, 16);
					map.featureLayer = L.mapbox.featureLayer(jsonMarkers).addTo(map);

			// find and store a variable reference to the list of filters
					var filters = document.getElementById('filters');

					var typesObj = {}, types = [];
					var features = map.featureLayer.getGeoJSON().features;
					for (var i = 0; i < features.length; i++) {
						typesObj[features[i].properties['data-type']] = true;
		}
			});
		}
		else {
			$('.information').addClass('invisible');
		}
	});

});