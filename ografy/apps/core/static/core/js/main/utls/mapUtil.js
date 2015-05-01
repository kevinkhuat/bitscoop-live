//View pertaining to the MapBox map
function mapboxManager() {
	var map, geoJSON;

	//The map needs to be created for the functions associated with this view to work
//	initializeMap();

	//Create the MapBox map
	//Note that this must be run after the map container has been inserted into the DOM
	//in order to run right
	function initializeMap(enableExtraControls) {
		this.geoJSON = {
			type: 'FeatureCollection',
			features: []
		};

		//The instantiation of a map takes the DOM element where the map will be stored
		//as a parameter, hence why the DOM element must exist before this function is called.
		this.map = L.mapbox.map('mapbox', 'liambroza.hl4bi8d0',  {
			zoomControl: true,
			//FIXME: This was added as a hack to work around a bug in Leaflet's clusterGroup.
			//When reloading the map, at the highest zoom level (19), markers would no longer cluster.
			//This would cause all markers at the same location to stack on top of each other.
			//My solution was to restrict the zoom level to 18, where the bug does not appear.
			//Should revisit if and when ClusterGroup is fixed.
			maxZoom: 18,
			tileLayer: {
				// This map option disables world wrapping. by default, it is false.
				continuousWorld: false,
				// This option disables loading tiles outside of the world bounds.
				noWrap: true
			}
		});

		if (enableExtraControls) {
			L.mapbox.geocoderControl('mapbox.places', {
				autocomplete: true
			}).addTo(this.map);
			L.control.fullscreen().addTo(this.map);
		}

		var mobileDisplay = ((window.innerWidth < 1080 && window.devicePixelRatio >= 1.5) || (window.devicePixelRatio >= 3));
		if (!mobileDisplay) {
			var map = this.map;
			map.featureGroup = L.featureGroup().addTo(map);

			map.markerDrawControl = new L.Control.Draw({
				edit: {
					featureGroup: map.featureGroup
				},
				draw: {
					polygon: false,
					polyline: false,
					rectangle: false,
					circle: false,
					marker: true
				}
			});

			map.on('draw:created', showMarkerDrawing);
			map.on('draw:edited', showMarkerDrawingEdited);

			map.polygonDrawControl = new L.Control.Draw({
				edit: {
					featureGroup: map.featureGroup
				},
				draw: {
					polygon: true,
					polyline: false,
					rectangle: false,
					circle: false,
					marker: false
				}
			});

			map.on('draw:created', showPolygonDrawing);
			map.on('draw:edited', showPolygonDrawingEdited);
		}
	}

	//These functions are used for drawing polygons and markers
	function showMarkerDrawingEdited(e) {
		e.layers.eachLayer(function(layer) {
			showMarkerDrawingArea({ layer: layer });
		});
	}
	function showMarkerDrawing(e) {
		var map = e.target;
		map.featureGroup.clearLayers();
		map.featureGroup.addLayer(e.layer);
		map.markerSelect = e.layer._latlng;
		e.layer.bindPopup((LGeo.area(e.layer) / 1000000).toFixed(2) + ' km<sup>2</sup>');
		e.layer.openPopup();
	}

	function showPolygonDrawingEdited(e) {
		e.layers.eachLayer(function(layer) {
			showPolygonDrawingArea({ layer: layer });
		});
	}
	function showPolygonDrawing(e) {
		var map = e.target;
		map.featureGroup.clearLayers();
		map.featureGroup.addLayer(e.layer);
		map.polySelect = e.layer._latlngs;
		e.layer.bindPopup((LGeo.area(e.layer) / 1000000).toFixed(2) + ' km<sup>2</sup>');
		e.layer.openPopup();
	}

	//Render a detail panel map
	function renderDetailMap(map) {
		map.featureLayer = L.mapbox.featureLayer(geoJSON).addTo(map);
	}

	function addData(geoJSON, newData) {
		//Create a MapBox GeoJSON element with the new information
		for (var index in newData) {
			var thisEvent = newData[index];
			var markerSymbol;
			var markerColor;

			if (thisEvent['_cls'] === 'Event') {
				markerColor = '#0052CE';
				markerSymbol = 'star-stroked';
			}
			else if (thisEvent['_cls'] === 'Event.Message') {
				markerColor = '#E6B800';
				markerSymbol = 'post';
			}
			else if (thisEvent['_cls'] === 'Event.Play') {
				markerColor = '#33CC33';
				markerSymbol = 'music';
			}

			geoJSON.features.push({
				// this feature is in the GeoJSON format: see geojson.org
				// for the full specification
				type: 'Feature',
				geometry: {
					type: 'Point',
					// coordinates here are in longitude, latitude order because
					// x, y is the standard for GeoJSON and many formats
					coordinates: thisEvent.location.coordinates
				},
				properties: {
					title: thisEvent.name,
					description: thisEvent.provider_name,
					// one can customize markers by adding simplestyle properties
					// https://www.mapbox.com/guides/an-open-platform/#simplestyle
					'marker-size': 'large',
					'marker-color': markerColor,
					'marker-symbol': markerSymbol,
					datetime: thisEvent.datetime,
					data: thisEvent.data,
					id: thisEvent.id
				}
			});
		}

		return geoJSON;
	}

	return {
		addData: addData,
		geoJSON: geoJSON,
		initializeMap: initializeMap,
		map: map,
		renderDetailMap: renderDetailMap
	};
}

