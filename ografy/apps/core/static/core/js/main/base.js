function baseView() {
	//Data model
	var baseData = [];
	var baseMap = new mapbox();

	//View components
	var detailViewInst = detailView();
	var utilsInst = utils();
	var mapInst = utilsInst.mapbox();
	var sessionInst = utilsInst.session();

	//Sub Views
	var listViewInst = listView(detailViewInst, mapInst, sessionInst);
	var mapViewInst = mapView(detailViewInst, utilsInst);

	function mapbox() {
		this.map;
		this.geoJSON = {
			"type": "FeatureCollection",
			"features": []
		};
	}

	function clearData() {

	}

	function updateData() {

	}

	function search() {

	}

	function loadTestData(completeCallback) {
		$.ajax({
			url: 'static/core/js/test_data/event_test_data.json',
			type: 'GET',
			dataType: 'json',
			headers: {
				"X-CSRFToken": sessionInst.getCsrfToken()
			}
		}).done(function(data, xhr, response) {
			baseData = data;
			completeCallback();
		});
	}

	function render() {
		var base_framework = nunjucks.render('static/core/templates/main/base.html');
		$('main').html(base_framework);

		mapViewInst.renderBase(baseMap, baseData, mapInst);
	}

	function bindNavigation() {
		$('.list-view-button').click(function() {
			listViewInst.renderBase(baseMap, baseData);
		});

		$('.timeline-view-button').click(function() {

		});

		$('.map-view-button').click(function() {
			mapViewInst.renderBase(baseMap, baseData, mapInst);
		});
	}

	function loadInitialData() {
		$.ajax({
			url: '/opi/event',
			type: 'GET',
			dataType: 'json',
			headers: {
				"X-CSRFToken": sessionInst.getCsrfToken()
			}
		}).done(function(data, xhr, response) {
			baseData = data;
		});
	}

	function insertInitialData() {
		for (i=0; i<8; i++){
			var data = {
				"created": "2014-12-01 19:54:06.860Z",
				"updated": "2014-12-01 19:54:06.860Z",
				"user_id": 1,
				"data_blob": {"cool": "pants", "hammer": "time"}
			};
			$.ajax({
				url: '/opi/data',
				type: 'POST',
				dataType: 'json',
				headers: {
					"X-CSRFToken": sessionInst.getCsrfToken()
				},
				data: data
			}).done(function(data, xhr, response) {
				baseData = data;
				console.log(baseData);
			});
		}

	}

	return {
		render: render,
		bindNavigation: bindNavigation,
		insertInitialData: insertInitialData,
		loadInitialData: loadInitialData,
		loadTestData: loadTestData
	}
}