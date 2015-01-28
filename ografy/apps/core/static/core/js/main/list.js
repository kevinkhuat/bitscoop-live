function listView(detailViewInst, dataInst, utilsInst, sessionInst) {
	function renderBase() {
		var tempData = 'Select an Event at left to see its details.';

		var list = nunjucks.render('list/list.html');
		$('.data-view').html(list);

		var thisDetailViewInst = detailViewInst.renderContent(tempData, tempData, tempData, tempData, true);
		var map = thisDetailViewInst.map;
		var geoJSON = thisDetailViewInst.geoJSON;
		renderContent(map, geoJSON);
	}

	//Views
	function renderContent(map, geoJSON) {
		//Iterate through json and render list items using Nunjucks templates
		var eventData = JSON.parse(localStorage.eventData);

		var listItems = nunjucks.render('list/list_elements.html',
			{
			eventData: eventData
		});

		$('.list-content').html(listItems);

		$('.list-item').click(function() {
			var selectedItem = $(this);
			selectedItem.siblings().removeClass('active');
			selectedItem.toggleClass('active');

			if (selectedItem.hasClass('active')) {
				$.ajax({
					url: 'static/core/js/test_data/event_single_test_data.json',
					type: 'GET',
					dataType: 'json',
					headers: {
						'X-CSRFToken': sessionInst.getCsrfToken()
					}
				}).done(function(data, xhr, response) {
					var single_data = data;
					detailViewInst.updateContent(single_data.provider_name, single_data.created, String(single_data.location), String(single_data.data));
					detailViewInst.updateMap(single_data.provider_name, map, single_data.location);
				});
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
	};
}
