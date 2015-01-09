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
	//Perform an ajax get call to grab event_test_json and store it to a local variable
    var event_data;

    var data = [
  {
    "created": "2014-12-01 19:54:06.860Z",
    "updated": "2014-12-01 19:54:06.860Z",
    "user_id": 1,
    "signal_id": 2,
    "provider_id": 3,
    "provider_name": "steam",
    "datetime": "2014-12-01 19:54:06.860Z",
    "data": {},
    "name": "pizza",
    "location" : [ -73.88, 40.78 ]
  },
  {
    "created": "2013-02-01 11:23:06.220Z",
    "updated": "2013-04-01 13:02:06.830Z",
    "user_id": 1,
    "signal_id": 2,
    "provider_id": 3,
    "provider_name": "steam",
    "datetime": "2013-04-01 13:02:06.830Z",
    "data": {},
    "name": "pizza",
    "location" : [ -73.887, 40.68 ]
  },
  {
    "created": "2014-12-02 19:54:06.860Z",
    "updated": "2014-12-02 19:54:06.860Z",
    "user_id": 1,
    "signal_id": 1,
    "provider_id": 1,
    "provider_name": "facebook",
    "datetime": "2014-12-02 19:54:06.860Z",
    "data": {},
    "name": "pizza",
    "location" : [ -73.88, 40.58 ]
  },
  {
    "created": "2014-12-03 19:54:06.860Z",
    "updated": "2014-12-03 19:54:06.860Z",
    "user_id": 1,
    "signal_id": 1,
    "provider_id": 1,
    "provider_name": "facebook",
    "datetime": "2014-12-03 19:54:06.860Z",
    "data": {},
    "name": "pizza",
    "location" : [ -73.88, 40.38 ]
  },
  {
    "created": "2014-12-08 19:54:06.860Z",
    "updated": "2014-12-08 19:54:06.860Z",
    "user_id": 1,
    "signal_id": 3,
    "provider_id": 8,
    "provider_name": "github",
    "datetime": "2014-12-08 19:54:06.860Z",
    "data": {},
    "name": "pizza",
    "location" : [ -73.883, 40.28 ]
  },
  {
    "created": "2014-11-03 19:54:06.860Z",
    "updated": "2014-11-03 19:54:06.860Z",
    "user_id": 1,
    "signal_id": 1,
    "provider_id": 1,
    "provider_name": "facebook",
    "datetime": "2014-11-03 19:54:06.860Z",
    "data": {},
    "name": "pizza",
    "location" : [ -73.88, 40.98 ]
  },
  {
    "created": "2014-03-02 19:54:06.860Z",
    "updated": "2014-03-02 19:54:06.860Z",
    "user_id": 1,
    "signal_id": 4,
    "provider_id": 2,
    "provider_name": "twitter",
    "datetime": "2014-03-02 19:54:06.860Z",
    "data": {},
    "name": "pizza",
    "location" : [ -73.882, 40.88 ]
  },
  {
    "created": "2014-12-14 19:54:06.860Z",
    "updated": "2014-12-14 19:54:06.860Z",
    "user_id": 1,
    "signal_id": 2,
    "provider_id": 3,
    "provider_name": "steam",
    "datetime": "2014-12-14 19:54:06.860Z",
    "data": {},
    "name": "pizza",
    "location" : [ -73.87, 40.78 ]
  }
]

    //for (x in data)
    //$.ajax({
	//	url: '/opi/event',
	//	type: 'POST',
	//	dataType: 'json',
	//	headers: {"X-CSRFToken": csrftoken},
     //   data: data[x]
	//}).done(function(data, xhr, response) {
	//	event_data = data;
	//});

	//$.ajax({
	//	url: '/opi/event',
	//	type: 'GET',
	//	dataType: 'json',
	//	headers: {"X-CSRFToken": csrftoken}
	//}).done(function(data, xhr, response) {
	//	var event_data = data;
	//});
//	var event_data = [
//  {
//    "created": "2014-12-01 19:54:06.860Z",
//    "updated": "2014-12-01 19:54:06.860Z",
//    "id": "9dan39daje0",
//    "user_id": 1,
//    "signal_id": 2,
//    "provider_id": 3,
//    "provider_name": "steam",
//    "datetime": "2014-12-01 19:54:06.860Z",
//    "data": {},
//    "name": "pizza",
//    "location" : [ -73.88, 40.78 ],
//  },
//  {
//    "created": "2013-02-01 11:23:06.220Z",
//    "updated": "2013-04-01 13:02:06.830Z",
//    "id": "9dan39daje1",
//    "user_id": 1,
//    "signal_id": 2,
//    "provider_id": 3,
//    "provider_name": "steam",
//    "datetime": "2013-04-01 13:02:06.830Z",
//    "data": {},
//    "name": "pizza",
//    "location" : [ -73.887, 40.68 ]
//  },
//  {
//    "created": "2014-12-02 19:54:06.860Z",
//    "updated": "2014-12-02 19:54:06.860Z",
//    "id": "9dan39daje2",
//    "user_id": 1,
//    "signal_id": 1,
//    "provider_id": 1,
//    "provider_name": "facebook",
//    "datetime": "2014-12-02 19:54:06.860Z",
//    "data": {},
//    "name": "pizza",
//    "location" : [ -73.88, 40.58 ]
//  },
//  {
//    "created": "2014-12-03 19:54:06.860Z",
//    "updated": "2014-12-03 19:54:06.860Z",
//    "id": "9dan39daje3",
//    "user_id": 1,
//    "signal_id": 1,
//    "provider_id": 1,
//    "provider_name": "facebook",
//    "datetime": "2014-12-03 19:54:06.860Z",
//    "data": {},
//    "name": "pizza",
//    "location" : [ -73.88, 40.38 ]
//  },
//  {
//    "created": "2014-12-08 19:54:06.860Z",
//    "updated": "2014-12-08 19:54:06.860Z",
//    "id": "9dan39daje4",
//    "user_id": 1,
//    "signal_id": 3,
//    "provider_id": 8,
//    "provider_name": "github",
//    "datetime": "2014-12-08 19:54:06.860Z",
//    "data": {},
//    "name": "pizza",
//    "location" : [ -73.883, 40.28 ]
//  },
//  {
//    "created": "2014-11-03 19:54:06.860Z",
//    "updated": "2014-11-03 19:54:06.860Z",
//    "id": "9dan39daje5",
//    "user_id": 1,
//    "signal_id": 1,
//    "provider_id": 1,
//    "provider_name": "facebook",
//    "datetime": "2014-11-03 19:54:06.860Z",
//    "data": {},
//    "name": "pizza",
//    "location" : [ -73.88, 40.98 ]
//  },
//  {
//    "created": "2014-03-02 19:54:06.860Z",
//    "updated": "2014-03-02 19:54:06.860Z",
//    "id": "9dan39daje6",
//    "user_id": 1,
//    "signal_id": 4,
//    "provider_id": 2,
//    "provider_name": "twitter",
//    "datetime": "2014-03-02 19:54:06.860Z",
//    "data": {},
//    "name": "pizza",
//    "location" : [ -73.882, 40.88 ]
//  },
//  {
//    "created": "2014-12-14 19:54:06.860Z",
//    "updated": "2014-12-14 19:54:06.860Z",
//    "id": "9dan39daje7",
//    "user_id": 1,
//    "signal_id": 2,
//    "provider_id": 3,
//    "provider_name": "steam",
//    "datetime": "2014-12-14 19:54:06.860Z",
//    "data": {},
//    "name": "pizza",
//    "location" : [ -73.87, 40.78 ]
//  }
//]

	//Iterate through json and render list items using Nunjucks templates
    var list = nunjucks.render('static/core/templates/main/list/list.html');
    $('#content').html(list);

    var insertion = nunjucks.render('static/core/templates/main/list/list_elements.html', {event_data: data});
    $('.list-content').html(insertion);

	//Add a hidden field to each list item for the item ID

    //nunjucks.configure('/ografy/ografy/apps/core/static/core/templates');
    list_detail = nunjucks.render('static/core/templates/main/detail.html');
    //var list_detail = nunjucks.render("/ografy/apps/core/static/core/templates/list_detail.html");
    $('.list-detail').html(list_detail);


	//Make sure that the sidebar is driven by Nunjucks templates
	//When a click event happens on a list item, it updates the sidebar
	//with the corresponding json data
	// filter items on button click
	$('.list-item').click(function() {
		$(this).siblings().removeClass('active');
		$(this).toggleClass('active');

		if ($(this).hasClass('active')) {
			$('.information').removeClass('invisible');

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
			$('.information').addClass('invisible');
		}
	});

});
