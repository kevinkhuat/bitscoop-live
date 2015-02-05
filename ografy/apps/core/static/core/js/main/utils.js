//Utilities used in rendering and using the main page
function utils() {
	//View pertaining to obtaining and searching for data
	function dataStore() {

		//This is the array of events that is returned from a search
		var resultData = [];

		//This is a dictionary of the IDs of events that have been obtained in previous searches
		var eventIndex = {};

		//This is the master list of events that have been obtained in previous searches
		var eventData = [];
		
		//This is the list of events in the current search that have not been obtained in previous searches
		var newData = [];

		//This is the collection of HTML elements that are rendered from eventData
		//Most of them will be set to invisible since only ones from the current search
		//should be displayed.
		var eventHTML = '';

		var currentViewInst = '';

		//Data model
		function getEventData() {
			return eventData;
		}


		function setCurrentView(inst) {
			currentViewInst = inst;
		}

		function updateData() {
			newData = [];
			for (var item in resultData) {
				var currentId = resultData[item].id;
				eventIndex[currentId] = true;

				var removed = false;
				var keys = Object.keys(eventIndex);
				for (var index in keys) {
					if (currentId === keys[index]) {
						removed = true;
					}
				}
				if (removed === false) {
					newData.push(resultData[item]);
					eventData.push(resultData[item]);
				}
			}

			var listItems = nunjucks.render('event_list.html',
				{
					eventData: newData
				});
			$('#event-list').append(listItems);

			currentEvents = $('#event-list *');
			for (var index in currentEvents) {
				var found = false;
				var thisEvent = currentEvents[index];
				var id = $(thisEvent).attr('data-id');
				for (var item in resultData) {
					var thisItem = resultData[item];
					if (id === thisItem.id) {
						found = true;
					}
				}

				if (found === false) {
					$(thisEvent).addClass('invisible');
				}
				else if (found === true) {
					$(thisEvent.removeClass('invisible'));
				}
			}
		}

		//Search for items in the database based on the search parameters and filters
		function search(searchString, callbackFunction) {
			var cookie = sessionsCookies().getCsrfToken();
			var url = 'opi/event?filter=' + searchString;
			$.ajax({
				url: url,
				type: 'GET',
				dataType: 'json',
				headers: {
					'X-CSRFToken': cookie
				}
			}).done(function(data, xhr, response) {
				resultData = data;
				updateData();
				currentViewInst.renderContent();
			});
		}

		return {
			getEventData: getEventData,
			setCurrentView: setCurrentView,
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
