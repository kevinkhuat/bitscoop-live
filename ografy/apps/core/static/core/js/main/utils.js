//Utilities used in rendering and using the main page
function utils() {
	//View pertaining to obtaining and searching for data
	function dataStore() {
		//Data model

		function clearData() {
			localStorage.setItem('dataData', '');
			localStorage.setItem('eventData', '');
			localStorage.setItem('messageData', '');
		}

		//Load all items from the database
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

		//Search for items in the database based on the search parameters and filters
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

	//View pertaining to the MapBox map
	function mapboxManager() {
		var map, geoJSON;

		//The map needs to be created for the functions associated with this view to work
		initializeMap();

		//Create the MapBox map
		//Note that this must be run after the map container has been inserted into the DOM
		//in order to run right
		function initializeMap() {
			geoJSON = {
				type: 'FeatureCollection',
				features: []
			};

			L.mapbox.accessToken = 'pk.eyJ1IjoiaGVnZW1vbmJpbGwiLCJhIjoiR3NrS0JMYyJ9.NUb5mXgMOIbh-r7itnVgmg';

			//The instantiation of a map takes the DOM element where the map will be stored
			//as a parameter, hence why the DOM element must exist before this function is called.
			map = L.mapbox.map('mapbox', 'liambroza.hl4bi8d0');
		}

		//Change the map's context
		function changeMapContext() {
		}

		//Change the map's focus
		function changeMapFocus() {
		}

		//Render a detail panel map
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

	//View pertaining to session cookies
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

		//Gets a CSRF token
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
