function baseView() {
	//Data model
	var baseData = [];

	//Sub Views
	var detailViewInst = detailView();
	var listViewInst = listView();
	var mapViewInst = mapView();

	var utilsViewInst = utils();

	function clearData() {

	}

	function updateData() {

	}

	function search() {

	}

	function loadTestData(completeCallback) {
		var csrftoken = utilsViewInst.session().getCookie('csrftoken');
		$.ajax({
			url: 'static/core/js/test_data/event_test_data.json',
			type: 'GET',
			dataType: 'json',
			headers: {"X-CSRFToken": csrftoken}
		}).done(function(data, xhr, response) {
			baseData = data;
			completeCallback();
		});
	}

	function render() {
		var map;
		var geoJSON = {
			"type": "FeatureCollection",
			"features": []
		};

		var base_framework = nunjucks.render('static/core/templates/main/base.html');
		$('main').html(base_framework);

		var tempData = 'Select an Event at left to see its details.';
		listViewInst.renderContent(map, baseData);
		detailViewInst.renderContent(tempData, tempData, tempData, tempData, true);

		var detailMap = utilsViewInst.mapbox().renderDetailMap(map);
		$('.map').html(detailMap);
	}

	function bindNavigation() {
		$('#list-view-button').click(function() {
			listViewInst.renderContent(baseData);
		});

		$('#timeline-view-button').click(function() {

		});

		$('#map-view-button').click(function() {
			mapViewInst.renderContent(utilsViewInst.map());
		});
	}

	function loadInitialData() {
		$.ajax({
			url: '/opi/event',
			type: 'GET',
			dataType: 'json',
			headers: {"X-CSRFToken": csrftoken}
		}).done(function(data, xhr, response) {
			baseData = data;
			console.log(baseData);
		});
	}

	return {
		render: render,
		bindNavigation: bindNavigation,
		loadInitialData: loadInitialData,
		loadTestData: loadTestData
	}
}