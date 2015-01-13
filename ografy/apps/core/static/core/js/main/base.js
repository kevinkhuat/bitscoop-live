$(document).ready(function() {
	loadTestData(function() {
		renderBase();
		bindNavigation();
	});

});

function renderBase () {
	var base_framework = nunjucks.render('static/core/templates/main/base.html');
	$('main').html(base_framework);
}

function bindNavigation() {
	$('#list-view-button').click(function () {
		detailPaneDefaultMode();
	});

	$('#timeline-view-button').click(function () {
		detailPaneDefaultMode();
	});

	$('#map-view-button').click(function () {
		detailPaneMapMode();
		renderMapContent();
	});
}

//Data model
var baseData = [];
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

function clearData() {

}

function updateData() {

}

function search () {

}

function loadTestData(completeCallback) {
	baseData = DANGEROUS_TEST_DATA;
	completeCallback();
}

