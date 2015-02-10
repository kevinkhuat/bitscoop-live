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

