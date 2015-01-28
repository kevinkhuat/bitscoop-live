function utils() {
	function dataStore() {
		//Data model

		function clearData() {
			localStorage.dataData = [];
			localStorage.eventData = [];
			localStorage.messageData = [];
		}

		function loadInitialData() {
			$.ajax({
				url: '/opi/event',
				type: 'GET',
				dataType: 'json',
				headers: {
					'X-CSRFToken': sessionInst.getCsrfToken()
				}
			}).done(function(data, xhr, response) {
				localStorage.eventData = data;
			});
		}

		function loadTestData(completeCallback) {
			$.ajax({
				url: 'static/core/js/test_data/event_test_data.json',
				type: 'GET',
				dataType: 'json',
				headers: {
					'X-CSRFToken': sessionInst.getCsrfToken()
				}
			}).done(function(data, xhr, response) {
				localStorage.eventData.test = data;
				completeCallback();
			});
		}

		function updateData() {
		}

		function search() {
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
		var baseMap, geoJSON;
		initializeMap();

		//Mapbox functions
		function initializeMap() {
			baseMap = new mapbox();
			geoJSON = {
				type: 'FeatureCollection',
				features: []
			};

			L.mapbox.accessToken = 'pk.eyJ1IjoiaGVnZW1vbmJpbGwiLCJhIjoiR3NrS0JMYyJ9.NUb5mXgMOIbh-r7itnVgmg';

			map.map = L.mapbox.map('mapbox', 'liambroza.hl4bi8d0').setView([40.68, -73.59], 9);
			map.geoJSON.features = [];
		}

		function changeMapContext() {
		}

		function changeMapFocus() {
		}

		function renderDetailMap(map) {
			map.map.featureLayer = L.mapbox.featureLayer(map.geoJSON).addTo(map.map);
		}

		return {
			basemap: baseMap,
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
