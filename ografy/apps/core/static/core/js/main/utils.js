function utils() {

	function mapbox() {
		//Mapbox functions
		function initializeMap() {

		}

		function changeMapContext() {

		}

		function changeMapFocus() {

		}

		function calculateFitBounds(map, dataList) {
			var maxLong = dataList[0].location[0];
			var minLong = dataList[0].location[0];
			var maxLat = dataList[0].location[1];
			var minLat = dataList[0].location[1];

			for (index in dataList) {
				if (dataList[index].location[0] > maxLong) {
					maxLong = dataList[index].location[0];
				}
				if (dataList[index].location[0] < minLong) {
					minLong = dataList[index].location[0];
				}
				if (dataList[index].location[1] > maxLat) {
					maxLat = dataList[index].location[1];
				}
				if (dataList[index].location[1] < minLat) {
					minLat = dataList[index].location[1];
				}
			}

			map.map.fitBounds([[minLat, minLong], [maxLat, maxLong]], {'padding': 15});
		}

		function placeMapPoints(map, dataList) {
			for (index in dataList) {
				map.geoJSON["features"].push({
					"type": "Feature",
					"geometry": {
						"type": "Point",
						"coordinates": dataList[index].location
					},
					"properties": {
						"title": dataList[index].provider_name + " " + dataList[index].name,
						"marker-symbol": "marker"
					}
				})
			}

			var markers = new mapboxgl.GeoJSONSource({data: map.geoJSON});
			map.map.addSource('markers', markers);
		}

		function renderDetailMap(map) {
			mapboxgl.accessToken = 'pk.eyJ1IjoiaGVnZW1vbmJpbGwiLCJhIjoiR3NrS0JMYyJ9.NUb5mXgMOIbh-r7itnVgmg';

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
						"text-allow-overlap": true
					},
					"paint": {
						"text-size": 12
					}
				});

				map.geoJSON["features"] = [];

				map.map = new mapboxgl.Map({
					center: [40.82, -73.59],
					zoom: 9,
					container: 'mapbox',
					style: style
				});

				var markers = new mapboxgl.GeoJSONSource({data: map.geoJSON});
				map.map.addSource('markers', markers);
			});
		}

		return {
			calculateFitBounds: calculateFitBounds,
			placeMapPoints: placeMapPoints,
			renderDetailMap: renderDetailMap
		}
	}

	function session() {
		//Django cookie management
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

		return {
			getCookie: getCookie
		}
	}

	return {
		mapbox: mapbox,
		session: session
	}
}
