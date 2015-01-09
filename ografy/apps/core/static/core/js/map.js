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

$(document).ready(function(){
mapboxgl.accessToken = 'pk.eyJ1IjoiaGVnZW1vbmJpbGwiLCJhIjoiR3NrS0JMYyJ9.NUb5mXgMOIbh-r7itnVgmg';

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
    "name": "hamburger",
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
    "name": "cheeseburger",
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
    "name": "hot dog",
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
    "name": "french fry",
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
    "name": "taco",
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
    "name": "milkshake",
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
    "name": "donut",
    "location" : [ -73.87, 40.78 ]
  }
]

mapboxgl.util.getJSON('https://www.mapbox.com/mapbox-gl-styles/styles/outdoors-v6.json', function (err, style) {
  if (err) throw err;

  style.layers.push({
    "id": "markers",
    "type": "symbol",
    "source": "markers",
    "layout": {
        "icon-image": "{marker-symbol}-12",
        "text-field": "{title}",
        "text-font": "Open Sans Semibold, Arial Unicode MS Bold",
        "text-offset": [0, 0.6],
        "text-anchor": "top",
        "icon-allow-overlap": true,
        "icon-ignore-placement": true
    },
    "paint": {
      "text-size": 12
    }
  });

    var max_X = data[0].location[0];
    var min_X = data[0].location[0];
    var max_Y = data[0].location[1];
    var min_Y = data[0].location[1];

    for (x in data){
        if (data[x].location[0] > max_X){

        }
    }
  var map = new mapboxgl.Map({
    container: 'map',
    style: style,
    center: [40.78, -73.90],
    zoom: 15
  });

  var geoJSON = {
    "type": "FeatureCollection",
    "features": [

    ]
  };

    for (x in data) {
        geoJSON["features"].push({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": data[x].location
                },
                "properties": {
                    "title": data[x].provider_name + " " + data[x].name,
                    "marker-symbol": "harbor"
                }
        })
    }
  var markers = new mapboxgl.GeoJSONSource({ data: geoJSON });
  map.addSource('markers', markers);
});

    //
	//// find and store a variable reference to the list of filters
	//		var filters = document.getElementById('filters');
    //
	//		var typesObj = {}, types = [];
	//		var features = map.featureLayer.getGeoJSON().features;
	//		for (var i = 0; i < features.length; i++) {
	//			typesObj[features[i].properties['data-type']] = true;
		//}
	//}).fail(function() {
	//	console.log('FAILED');
	//});
});