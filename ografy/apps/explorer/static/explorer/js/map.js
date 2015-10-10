define(['cartano', 'jquery', 'jquery-cookie'], function(cartano, $) {
	var map;

	$.ajax({
		url: '/tokens/mapbox',
		type: 'GET',
		dataType: 'json',
		headers: {
			'X-CSRFToken': $.cookie('csrftoken')
		}
	}).done(function(data) {
		map = new cartano.Map('liambroza.hl4bi8d0', {
			accessToken: data.MAPBOX_ACCESS_TOKEN,

			className: 'flex-grow',

			zoomControl: true,
			drawControl: true,
			layerControl: true
		});

		$('#background').append(map.element);
		map.resize();
	});
});
