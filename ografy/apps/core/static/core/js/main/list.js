function listView() {

	var detailViewInst = detailView();
	var utilsViewInst = utils();

	//TEST_REMOVE
	function getCoordinatesHack(selectedItem) {
		var trimmed = $.trim(selectedItem.children('.list-item-location').html());
		var numberArray = trimmed.split(',').map(function(trimmed) {
			return Number(trimmed);
		});
		return numberArray;
	}

	function renderBase(map, baseData) {
		var tempData = 'Select an Event at left to see its details.';

		var list = nunjucks.render('static/core/templates/main/list/list.html');
		$('.content').html(list);

		renderContent(map, baseData);
		detailViewInst.renderContent(tempData, tempData, tempData, tempData, true);
		utilsViewInst.mapbox().renderDetailMap(map);
	}

	//Views
	function renderContent(map, data) {
		//Iterate through json and render list items using Nunjucks templates
		var listItems = nunjucks.render('static/core/templates/main/list/list_elements.html', {event_data: data});
		$('.list-content').html(listItems);

		$('.list-item').click(function() {
			var selectedItem = $(this);
			selectedItem.siblings().removeClass('active');
			selectedItem.toggleClass('active');


			if (selectedItem.hasClass('active')) {
				var eventName =selectedItem.children('.list-item-name').html();
				var eventDate = selectedItem.children('.list-item-date').html();
				var eventLocation = selectedItem.children('.list-item-location').html();
				var eventData = selectedItem.children('.list-item-data').html();

				detailViewInst.updateContent(eventName, eventDate, eventLocation, eventData);
				detailViewInst.updateMap(eventName, map, getCoordinatesHack(selectedItem));

			}
			else {
				detailViewInst.clearContent();
				detailViewInst.clearMap(map);
			}
		});
	}

	return{
		renderContent: renderContent,
		renderBase: renderBase
	}
}
