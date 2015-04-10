//Render the List View on the main page
function listView(detailViewInst, dataInst, cacheInst, mapboxViewInst, sessionInst, urlParserInst) {
	//Render the base framework of the List View
	function renderBase(callback) {
		//Render the list title and the container for the list elements using Nunjucks
		//and insert them into the DOM
		var list = nunjucks.render('list/list.html');
		$('.data-view').html(list);

		//Create an instance of the Detail panel, get the map and geoJSON properties it created,
		//then render the List View's content.
		var thisDetailViewInst = detailViewInst.renderContent(true);
		var map = mapboxViewInst.map;
		var geoJSON = mapboxViewInst.geoJSON;

		//Bind event listeners for the headers
		//Mouse enter or leave adds and removes the active highlighting
		//Click also removes the highlighting so that mobile users don't have
		//a permanently highlighted field when clicked.
		//Other click functionality detailed below
		$('.list.title > .list')
			.mouseenter(function() {
			$(this).addClass('hover');
			})
			.mouseleave(function() {
				$(this).removeClass('hover');
			})
			.click(function() {
				var searchOrder;

				if (window.window.devicePixelRatio > 1.5) {
					$(this).removeClass('hover');
				}
				dataInst.setResultCurrentPage(1);
				//Remove the order icons from every other header, as we're only ordering by one field at a time for now
				$(this).siblings().children().removeClass('icon-triangle-up').removeClass('icon-triangle-down');
				var childIcon = $(this).children();
				//Change the current header's order icon
				//If it's currently ordering by something, order by the other way
				if ($(childIcon).hasClass('icon-triangle-up')) {
					$(childIcon).attr('class', 'icon-triangle-down');
					searchOrder = '-' + $(this)[0].id;
				}
				else if ($(childIcon).hasClass('icon-triangle-down')) {
					$(childIcon).attr('class', 'icon-triangle-up');
					searchOrder = '+' + $(this)[0].id;
				}
				//If it's not ordering by anything, order up.
				else {
					$(childIcon).attr('class', 'icon-triangle-up');
					searchOrder = '+' + $(this)[0].id;
				}

				dataInst.setCurrentOrder(searchOrder);
				//Do a search with the new order
				//FIXME: calling the API for every new ordering request is not remotely ideal,
				//so this needs to be changed at some point
				dataInst.search('event', urlParserInst.getSearchFilters(), searchOrder);
			});
		renderContent(map, geoJSON);
		callback();
	}

	function renderContent(map, geoJSON) {
		map.removeLayer(map.featureLayer);
	}
	//Update the List View content
	function updateContent() {
		//Iterate through json and render list items using Nunjucks templates
		var currentOrder = dataInst.getCurrentOrder();
		var resultData = dataInst.getResultData();
		var listItems = nunjucks.render('list/list_elements.html',
			{
			resultData: resultData
		});
		$('.list.content').html(listItems);

		if (currentOrder.slice(0,1) === '+') {
			$('.list.title').find('#' + currentOrder.slice(1)).find('i').attr('class', 'icon-triangle-up');
		}
		else {
			$('.list.title').find('#' + currentOrder.slice(1)).find('i').attr('class', 'icon-triangle-down');
		}
		//Bind an event listener that triggers when any list item is clicked or moused over/off
		$('.list.item')
			.mouseenter(function() {
				$(this).addClass('hover');
			})
			.mouseleave(function() {
				$(this).removeClass('hover');
			})
			.click(function() {
				//Remove 'active' from items other than the one that was clicked on
				//Then toggle 'active' on the clicked item
				var selectedItem = $(this);

				if (window.window.devicePixelRatio > 1.5) {
					selectedItem.removeClass('hover');
				}
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
					detailViewInst.hideContent();
					detailViewInst.clearMap(map);
				}
			});

		setHeight();
	}

	//This is used to set the height of the div containing the list content.
	//It gets the height of the main-list div, then subtracts the 30-pixel height of the header
	//and sets the list content div to this figure.
	//This allows for making the content scrollable while leaving the header alone.
	function setHeight() {
		var parentHeight = $('.main-list').height();
		var headerHeight = $('.list.title').height();
		if (window.innerHeight < window.innerWidth) {
			$('.list.content').height(parentHeight - headerHeight);
		}
		else {
			$('.list.content').height(parentHeight);
		}
	}

	$(window).resize(function() {
		setHeight();
	});

	return{
		renderContent: renderContent,
		renderBase: renderBase,
		updateContent: updateContent
	};
}
