//Render the List View on the main page
function listView(detailViewInst, dataInst, cacheInst, mapboxViewInst, sessionInst) {
	//Render the base framework of the List View
	function renderBase() {
		//Render the list title and the container for the list elements using Nunjucks
		//and insert them into the DOM
		var list = nunjucks.render('list/list.html');
		$('.data-view').html(list);

		//Create an instance of the Detail panel, get the map and geoJSON properties it created,
		//then render the List View's content.
		var thisDetailViewInst = detailViewInst.renderContent(true);
		var map = mapboxViewInst.map;
		var geoJSON = mapboxViewInst.geoJSON;
		renderContent(map, geoJSON);
	}

	//Render the List View content
	function renderContent(map, geoJSON) {
		//Iterate through json and render list items using Nunjucks templates
		var eventData = dataInst.getResultData();
		var listItems = nunjucks.render('list/list_elements.html',
			{
			eventData: eventData
		});
		$('.list.content').html(listItems);

		//Bind an event listener that triggers when any list item is clicked
		$('.list.item').click(function() {
			//Remove 'active' from items other than the one that was clicked on
			//Then toggle 'active' on the clicked item
			var selectedItem = $(this);
			selectedItem.siblings().removeClass('active');
			selectedItem.toggleClass('active');

			//If the clicked item is now active, get the item's information from the database
			if (selectedItem.hasClass('active')) {
				$.ajax({
					url: 'opi/event/' + selectedItem.attr('id'),
					type: 'GET',
					dataType: 'json',
					headers: {
						'X-CSRFToken': sessionInst.getCsrfToken()
					}
				}).done(function(data, xhr, response) {
					//When the data has been acquired, update the detail content and detail map
					//with the new data
					var single_data = data;
					detailViewInst.updateContent(single_data.provider_name, single_data.datetime, String(single_data.location.coordinates), String(single_data.data));
					detailViewInst.updateMap(single_data.provider_name, map, single_data.location.coordinates);
				});
			}
			//If the clicked item is now inactive (occurs when you click an active item),
			//clear the detail panel content and map
			else {
				detailViewInst.clearContent();
				detailViewInst.clearMap(map);
			}
		});
	}


	function updateContent() {

	}

	return{
		renderContent: renderContent,
		renderBase: renderBase,
		updateContent: updateContent
	};
}
