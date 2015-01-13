function baseView() {
	//Data model
	var baseData = [];

	//Sub Views
	var detailViewInst = detailView();
	var listViewInst = listView();
	var mapViewInst = mapView();

	var utilInst = utils();

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
			headers: {"X-CSRFToken": csrftoken}
		}).done(function(data, xhr, response) {
			baseData = data;
			completeCallback();
		});
	}

	function render() {
		var base_framework = nunjucks.render('static/core/templates/main/base.html');
		$('main').html(base_framework);
	}

	function bindNavigation() {
		$('#list-view-button').click(function() {
			listViewInst.render();
		});

		$('#timeline-view-button').click(function() {

		});

		$('#map-view-button').click(function() {
			mapViewInst.renderContent(utilInst.map());
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

var baseViewInst = baseView();

$(document).ready(function() {
	baseViewInst.loadTestData(function() {
		baseViewInst.render();
		baseViewInst.bindNavigation();
	});
});
