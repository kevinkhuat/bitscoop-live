function listView() {

	var detailViewInst = detailView();
	var utilsViewInst = utils();

	function renderBase(map, baseData) {
		var tempData = 'Select an Event at left to see its details.';

		var list = nunjucks.render('static/core/templates/main/list/list.html');
		$('.content').html(list);

		renderContent(map, baseData);
		detailViewInst.renderContent(tempData, tempData, tempData, tempData, true);
		utilsViewInst.mapbox().renderDetailMap(map);
	}

	//Views
	function renderContent(map, event_data) {
		//Iterate through json and render list items using Nunjucks templates
		var listItems = nunjucks.render('static/core/templates/main/list/list_elements.html', {event_data: event_data});
		$('.list-content').html(listItems);

		$('.list-item').click(function() {
			var selectedItem = $(this);
			selectedItem.siblings().removeClass('active');
			selectedItem.toggleClass('active');


			if (selectedItem.hasClass('active')) {
				var csrftoken = utilsViewInst.session().getCookie('csrftoken');
				$.ajax({
					url: 'static/core/js/test_data/event_single_test_data.json',
					type: 'GET',
					dataType: 'json',
					headers: {"X-CSRFToken": csrftoken}
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
	}
}
