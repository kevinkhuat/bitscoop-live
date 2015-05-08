//Render the Map View on the main page.
function mapView(dataInst, mapboxViewInst, urlParserInst) {
	var mapInst;
	var map = 'pants';
	var geoJSON = 'shorts';

	//Render the map content.
	function renderContent(promise) {
		//Render the container for the map using Nunjucks and insert it into the DOM
		var map_framework = nunjucks.render('map/map.html');
		$('.map-view').html(map_framework);

		//Create a MapBox map.
		//This needs to be done after the map container has been inserted into the DOM
		//since MapBox needs a parent element specified when instantiating a map.
		mapboxViewInst.initializeMainMap();
		map = mapboxViewInst.map.main;
		geoJSON = mapboxViewInst.geoJSON;
		//Resolve the input promise to indicate that the map view has finished rendering.
		promise.resolve();
	}

	//Create a new layer of markers on the map.
	function updateContent() {
		var line = [];
		var newData = dataInst.resultCache.events;
		var currentFocus = dataInst.state.view.map.focus.slice();
		var currentZoom = dataInst.state.view.map.zoom;

		if (map.hasLayer(map.clusterGroup)) {
			map.removeLayer(map.clusterGroup);
			map.removeLayer(map.polyline);
			map.removeControl(map.layerControl);
		}

		//Remove all markers from the map
		map.removeLayer(map.featureLayer);
		geoJSON.features = [];

		//Add the result data to a geoJSON layer
		geoJSON = mapboxViewInst.addData(geoJSON, newData);

		//Add the new geoJSON layer to the map
		map.featureLayer = L.mapbox.featureLayer(geoJSON);

		//Create a new ClusterGroup for drawing lines or directions between markers
		map.clusterGroup = new L.MarkerClusterGroup({
			maxClusterRadius: 20
		});

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
			if (map.featureLayer.getGeoJSON().features.length > 0) {
				map.fitBounds(map.featureLayer.getBounds());
				dataInst.state.view.map.zoom = map.getZoom();
				dataInst.state.view.map.focus = [map.getCenter().lng, map.getCenter().lat];
			}
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

		//Update the zoom both in the data model and in the hash when the user zooms in or out.
		map.on('zoomend', function() {
			dataInst.state.view.map.zoom = map.getZoom();
			urlParserInst.updateHash();
		});

		//Update the focus both in the data model and in the hash when the user moves the map.
		map.on('moveend', function() {
			dataInst.state.view.map.focus = [map.getCenter().lng, map.getCenter().lat];
			urlParserInst.updateHash();
		});

		//When the user clicks anywhere, change all markers back to the default color.
		map.on('click', function(e) {
			dataInst.highlight(false);
		});

		//Bind an event listener that triggers when an item on the map is selected.
		//This will clear the data model's selected field, add the clicked event to the selected field,
		//and call the data model's highlight function.
		//Note that this doesn't directly call this module's highlight function, as the data model's highlight
		//function calls each view's highlight function.
		map.clusterGroup.on('click', function(e) {
			//Save which item was selected
			dataInst.state.selected = {};
			dataInst.state.selected[e.layer.feature.properties.id] = true;
			dataInst.highlight(true);
		});
	}

	//Highlight a selected event on the map.
	function highlight(id, eventActive) {
		var feature;
		var layers = map.featureLayer._layers;
		var thisLayer;
		var thisMarker;
		var event;

		//Find the layer, feature, and marker associated with the selected event.
		for (var layer in layers) {
			if (layers[layer].feature !== undefined) {
				if (layers[layer].feature.properties.id === id) {
					feature = layers[layer].feature;
					thisLayer = layer;
					thisMarker = map.featureLayer._layers[thisLayer];
				}
			}
		}

		//Reset all markers back to their original color.
		resetColors(map);

		//If the given event is active, highlight it.
		if (eventActive) {
			//Change the color of the selected marker
			feature.properties['old-color'] = feature.properties['marker-color'];
			feature.properties['marker-color'] = '#ff8888';
			thisMarker.setIcon(L.mapbox.marker.icon(feature.properties));
			//Open the popup.  Note that if the marker is in a cluster, this won't show up.
			//An attempt was made to spiderfy the selected cluster before opening the popup,
			//but that caused more problems than it solved since markers that weren't normally spiderfied
			//were being spiderfied anyway.
			thisMarker.openPopup();
		}

		//Set the focus to the event's coordinates and then center the map over the event and zoom in.
		dataInst.state.view.map.focus = feature.geometry.coordinates;
		map.setView(dataInst.state.view.map.focus.slice().reverse(), dataInst.state.view.map.zoom, {
			pan: {
				animate: true,
				duration: 0.25
			}
		});
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
