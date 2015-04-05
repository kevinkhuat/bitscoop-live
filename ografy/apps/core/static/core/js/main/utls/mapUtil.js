//View pertaining to the MapBox map
function mapboxManager(dataInst) {
	var map, geoJSON;

	//The map needs to be created for the functions associated with this view to work
//	initializeMap();

	//Create the MapBox map
	//Note that this must be run after the map container has been inserted into the DOM
	//in order to run right
	function initializeMap() {
		this.geoJSON = {
			type: 'FeatureCollection',
			features: []
		};

		L.mapbox.accessToken = 'pk.eyJ1IjoiaGVnZW1vbmJpbGwiLCJhIjoiR3NrS0JMYyJ9.NUb5mXgMOIbh-r7itnVgmg';

		//The instantiation of a map takes the DOM element where the map will be stored
		//as a parameter, hence why the DOM element must exist before this function is called.
		this.map = L.mapbox.map('mapbox', 'liambroza.hl4bi8d0',  {
			zoomControl: false,
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
		}).addControl(L.mapbox.geocoderControl('mapbox.places', {
			autocomplete: true
		}));

		L.control.fullscreen().addTo(this.map);
		if (window.devicePixelRatio < 1.5) {
			L.control.zoomslider().addTo(this.map);
			var map = this.map;
			map.featureGroup = L.featureGroup().addTo(this.map);
			var drawControl = new L.Control.Draw({
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
			}).addTo(this.map);

			this.map.on('draw:created', showPolygonArea);
			this.map.on('draw:edited', showPolygonAreaEdited);

			function showPolygonAreaEdited(e) {
				e.layers.eachLayer(function(layer) {
					showPolygonArea({ layer: layer });
				});
			}
			function showPolygonArea(e) {
				map.featureGroup.clearLayers();
				map.featureGroup.addLayer(e.layer);
				map.polySelect = e.layer._latlngs;
				e.layer.bindPopup((LGeo.area(e.layer) / 1000000).toFixed(2) + ' km<sup>2</sup>');
				e.layer.openPopup();
			}
		}


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

	function addData(geoJSON) {
		var newData = dataInst.getResultData().reverse();

		//Create a MapBox GeoJSON element with the new information
		for (var index in newData) {
			geoJSON.features.push({
				// this feature is in the GeoJSON format: see geojson.org
				// for the full specification
				type: 'Feature',
				geometry: {
					type: 'Point',
					// coordinates here are in longitude, latitude order because
					// x, y is the standard for GeoJSON and many formats
					coordinates: newData[index].location.coordinates
				},
				properties: {
					title: newData[index].name,
					description: newData[index].provider_name,
					// one can customize markers by adding simplestyle properties
					// https://www.mapbox.com/guides/an-open-platform/#simplestyle
					'marker-size': 'large',
					'marker-color': '#BE9A6B',
					'marker-symbol': 'post',
					datetime: newData[index].datetime,
					data: newData[index].data,
					id: newData[index].id
				}
			});
		}

		return geoJSON;
	}

	return {
		addData: addData,
		map: map,
		geoJSON: geoJSON,
		initializeMap: initializeMap,
		changeMapContext: changeMapContext,
		changeMapFocus: changeMapFocus,
		renderDetailMap: renderDetailMap
	};
}

