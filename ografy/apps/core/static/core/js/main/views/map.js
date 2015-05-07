//Render the Map View on the main page
function mapView(detailViewInst, dataInst, mapboxViewInst, urlParserInst) {
	var mapInst;
	var map = 'pants';
	var geoJSON = 'shorts';

	//Render the map content
	function renderContent(promise) {
		//Render the container for the map using Nunjucks and insert it into the DOM
		var map_framework = nunjucks.render('map/map.html');
		$('.map-view').html(map_framework);

		//Create a MapBox map.
		//This needs to be done after the map container has been inserted into the DOM
		//since MapBox needs a parent element specified when instantiating a map.

		mapboxViewInst.initializeMap(true);
		map = mapboxViewInst.map;
		geoJSON = mapboxViewInst.geoJSON;
		promise.resolve();
	}

	//Creates a new layer of markers on the map
	function updateContent() {
		var line = [];
		if (map.hasLayer(map.clusterGroup)) {
			map.removeLayer(map.clusterGroup);
			map.removeLayer(map.polyline);
			map.removeControl(map.layerControl);
		}
		//map.featureLayer.eachLayer(function(marker) {
		//	map.clusterGroup.removeLayer(marker);
		//});

		map.removeLayer(map.featureLayer);
		//map.removeLayer(map.clusterGroup);
		geoJSON.features = [];

		var newData = dataInst.resultCache.events;

		//Adds result data to a geoJSON layer
		geoJSON = mapboxViewInst.addData(geoJSON, newData);

		//Add the new element to the map
		map.featureLayer = L.mapbox.featureLayer(geoJSON);

		//Create a new ClusterGroup for drawing lines or directions between markers
		map.clusterGroup = new L.MarkerClusterGroup({
			maxClusterRadius: 10
		});

		var currentFocus = dataInst.state.view.map.focus.slice();
		var currentZoom = dataInst.state.view.map.zoom;

		//Logic for the focus and/or zoom being present in the URL
		if (currentFocus.length !== 0 || currentZoom !== 0) {
			//If both the focus and zoom were entered, set the map to that focus and zoom.
			if (currentFocus.length !== 0 && currentZoom !== 0) {
				map.setView(currentFocus.reverse(), currentZoom);
			}
			//If the focus was entered but not the zoom, center on the focus and set zoom to 12
			else if (currentFocus.length !== 0) {
				dataInst.state.view.map.zoom = 12;
				map.setView(currentFocus.reverse(), 12);
			}
			//If the zoom was entered but not the focus, get the user's location and center on them.
			else {
				dataInst.state.view.map.focus = [parseFloat(geoplugin_longitude()), parseFloat(geoplugin_latitude())];
				currentFocus = dataInst.state.view.map.focus;
				map.setView(currentFocus.reverse(), currentZoom);
			}
		}
		//If neither the zoom nor focus were present in the URL, fit the map around all of the elements
		//in the result data using fitBounds
		else {
			//Fit the map's view so that all of the items are visible
			map.fitBounds(map.featureLayer.getBounds());
			dataInst.state.view.map.zoom = map.getZoom();
			dataInst.state.view.map.focus = [map.getCenter().lng, map.getCenter().lat];
		}

		//Update the URL hash
		urlParserInst.updateHash();

		//Draw lines between the markers in the clusterGroup
		map.featureLayer.eachLayer(function(marker) {
			map.clusterGroup.addLayer(marker);
			line.push(marker.getLatLng());
		});

		//Add the clusterGroup to the map
		map.addLayer(map.clusterGroup);

		//Line that will be drawn between clusterGroup markers
		var polyline_options = {
			color: '#000'
		};

		//Add the clusterGroup line to the map
		map.polyline = L.polyline(line, polyline_options).addTo(map);


		//Add the layer control to the map
		map.layerControl = L.control.layers({}, { Path: map.polyline }).addTo(map);
		//FIXME: This is most of what's needed to generate walking directions once the API is working
//		var directions = L.mapbox.directions({
//			profile: 'mapbox.driving'
//		});
//
//		for (var index in geoJSON.features) {
//			if (index == 0) {
//				directions.setOrigin(geoJSON.features[index]);
//			}
//			else if (index == geoJSON.features.length-1){
//				directions.setDestination(geoJSON.features[index]);
//			}
//			else {
//				directions.addWaypoint(index-1, geoJSON.features[index]);
//			}
//		}
//
//		directions.query();
//		map.directionsLayer = L.mapbox.directions.layer(directions).addTo(map);

		//Update the zoom both locally and in the hash when the user zooms in or out
		map.on('zoomend', function() {
			dataInst.state.view.map.zoom = map.getZoom();
			urlParserInst.updateHash();
		});

		//Update the focus both locally and in the hash when the user moves the map
		map.on('moveend', function() {
			dataInst.state.view.map.focus = [map.getCenter().lng, map.getCenter().lat];
			urlParserInst.updateHash();
		});

		//When the user clicks anywhere, change all markers back to the default color
		map.on('click', function(e) {
			dataInst.highlight(false);
			//Populate the detail panel content with information from the selected item.
			detailViewInst.hideContent();
		});

		//Bind an event listener that triggers when an item on the map is selected.
		//This listener will populate the detail content with the selected item's information.
		//The selected marker will also change color.
		map.clusterGroup.on('click', function(e) {
			//Save which item was selected
			dataInst.state.selected = {};
			dataInst.state.selected[e.layer.feature.properties.id] = true;
			dataInst.highlight(true);
		});
	}

	function highlight(id, eventActive) {
		var feature;
		var layers = map.featureLayer._layers;
		var thisLayer;
		var thisMarker;
		var event;

		for (var layer in layers) {
			if (layers[layer].feature !== undefined) {
				if (layers[layer].feature.properties.id === id) {
					feature = layers[layer].feature;
					thisLayer = layer;
				}
			}
		}

		event = dataInst.eventCache.events[feature.properties.id];
		thisMarker = map.featureLayer._layers[thisLayer];

		//Reset all markers back to their original color.
		resetColors(map);

		if (eventActive) {
			//Change the color of the selected marker
			feature.properties['old-color'] = feature.properties['marker-color'];
			feature.properties['marker-color'] = '#ff8888';
			thisMarker.setIcon(L.mapbox.marker.icon(feature.properties));
			thisMarker.__parent.spiderfy();
			thisMarker.openPopup();
		}
		else {
			thisMarker.__parent.unspiderfy();
		}

		//Populate the detail panel content with information from the selected item.

		dataInst.state.view.map.focus = feature.geometry.coordinates;
		map.setView(dataInst.state.view.map.focus.slice().reverse(), dataInst.state.view.map.zoom);
		detailViewInst.updateContent(event);
	}
	//Resets the color of every marker back to default
	function resetColors(map) {
		var clusterMarkers = map.clusterGroup.getLayers();
		for (var index in clusterMarkers) {
			var thisMarker = clusterMarkers[index];

			thisMarker.feature.properties['marker-color'] = thisMarker.feature.properties['old-color'] || thisMarker.feature.properties['marker-color'];
			thisMarker.setIcon(L.mapbox.marker.icon(thisMarker.feature.properties));
			thisMarker.closePopup();
		}
	}


	return {
		highlight: highlight,
		renderContent: renderContent,
		updateContent: updateContent
	};
}
