function utils() {
	function mapbox() {
		//Mapbox functions
		function initializeMap() {
		}

		function changeMapContext() {
		}

		function changeMapFocus() {
		}

		function renderDetailMap(map) {
			L.mapbox.accessToken = 'pk.eyJ1IjoiaGVnZW1vbmJpbGwiLCJhIjoiR3NrS0JMYyJ9.NUb5mXgMOIbh-r7itnVgmg';
			map.map = L.mapbox.map('mapbox', 'liambroza.hl4bi8d0').setView([40.68, -73.59], 9);

			map.geoJSON['features'] = [];
			map.map.featureLayer = L.mapbox.featureLayer(map.geoJSON).addTo(map.map);
		}

		return {
			renderDetailMap: renderDetailMap
		}
	}

	function session() {
		var csrfToken = '';

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

		function getCsrfToken() {
			if (csrfToken == '') {
				csrfToken = getCookie('csrftoken');
			}

			return csrfToken;
		}

		return {
			getCsrfToken: getCsrfToken,
			getCookie: getCookie
		}
	}

	return {
		mapbox: mapbox,
		session: session
	}
}
