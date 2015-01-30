function utils() {
	function dataStore() {
		//Data model

		function clearData() {
			localStorage.setItem('dataData', '');
			localStorage.setItem('eventData', '');
			localStorage.setItem('messageData', '');
		}

		function loadInitialData() {
			$.ajax({
				url: '/opi/event',
				type: 'GET',
				dataType: 'json',
				headers: {
					'X-CSRFToken': sessionsCookies().getCsrfToken()
				}
			}).done(function(data, xhr, response) {
				localStorage.setItem('eventData', JSON.stringify(data));
			});
		}

		function loadTestData() {
			var cookie = sessionsCookies().getCsrfToken();
			$.ajax({
				url: 'static/core/js/test_data/event_test_data.json',
				type: 'GET',
				dataType: 'json',
				headers: {
					'X-CSRFToken': cookie
				}
			}).done(function(data, xhr, response) {
				localStorage.setItem('eventData', JSON.stringify(data));
			});
		}

		function updateData() {
		}

		function search(searchString) {
			var cookie = sessionsCookies().getCsrfToken();
			var url = 'opi/event?$filter=' + searchString;
			$.ajax({
				url: url,
				type: 'GET',
				dataType: 'json',
				headers: {
					'X-CSRFToken': cookie
				}
			}).done(function(data, xhr, response) {
				localStorage.eventData = JSON.stringify(data);
			});
		}

		return {
			clearData: clearData,
			loadInitialData: loadInitialData,
			loadTestData: loadTestData,
			updateData: updateData,
			search: search
		};
	}

	function mapboxManager() {
		var map, geoJSON;
		initializeMap();

		//Mapbox functions
		function initializeMap() {
			geoJSON = {
				type: 'FeatureCollection',
				features: []
			};

			L.mapbox.accessToken = 'pk.eyJ1IjoiaGVnZW1vbmJpbGwiLCJhIjoiR3NrS0JMYyJ9.NUb5mXgMOIbh-r7itnVgmg';

			map = L.mapbox.map('mapbox', 'liambroza.hl4bi8d0');
		}

		function changeMapContext() {
		}

		function changeMapFocus() {
		}

		function renderDetailMap(map) {
			map.featureLayer = L.mapbox.featureLayer(geoJSON).addTo(map);
		}

		return {
			map: map,
			geoJSON: geoJSON,
			initializeMap: initializeMap,
			changeMapContext: changeMapContext,
			changeMapFocus: changeMapFocus,
			renderDetailMap: renderDetailMap
		};
	}

	function sessionsCookies() {
		var csrfToken = '';

		//Django cookie management
		function getCookie(name) {
			var cookieValue = null;
			if (document.cookie && document.cookie !== '') {
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
			if (csrfToken === '') {
				csrfToken = getCookie('csrftoken');
			}

			return csrfToken;
		}

		return {
			getCsrfToken: getCsrfToken,
			getCookie: getCookie
		};
	}

	return {
		dataStore: dataStore,
		mapboxManager: mapboxManager,
		sessionsCookies: sessionsCookies
	};
}
