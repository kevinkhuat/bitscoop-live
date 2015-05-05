//Render the List View on the main page
function listView(detailViewInst, dataInst, mapboxViewInst, urlParserInst) {
	var contentHeight = 0;
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
				var searchSort;

				if (window.window.devicePixelRatio > 1.5) {
					$(this).removeClass('hover');
				}
				dataInst.setResultCurrentPage(1);
				//Remove the sort icons from every other header, as we're only sorting by one field at a time for now
				$(this).siblings().children().removeClass('icon-triangle-up').removeClass('icon-triangle-down');
				var childIcon = $(this).children();
				//Change the current header's sort icon
				//If it's currently sorting by something, sort by the other way
				if ($(childIcon).hasClass('icon-triangle-up')) {
					$(childIcon).attr('class', 'icon-triangle-down');
					searchSort = '-' + $(this)[0].id;
				}
				else if ($(childIcon).hasClass('icon-triangle-down')) {
					$(childIcon).attr('class', 'icon-triangle-up');
					searchSort = '+' + $(this)[0].id;
				}
				//If it's not sorting by anything, sort up.
				else {
					$(childIcon).attr('class', 'icon-triangle-up');
					searchSort = '+' + $(this)[0].id;
				}

				urlParserInst.setSort(searchSort);
				urlParserInst.updateHash();
				//Do a search with the new sort
				//FIXME: calling the API for every new sorting request is not remotely ideal,
				//so this needs to be changed at some point
				dataInst.search('event', urlParserInst.getSearchFilters(), searchSort);
			});
		renderContent(map, geoJSON);
		callback();
	}

	function renderContent(map, geoJSON) {
		map.removeLayer(map.featureLayer);
	}

	function restoreHeight() {
		return contentHeight;
	}

	function saveHeight(height) {
		contentHeight = height;
	}

	//Update the List View content
	function updateContent() {
		//Iterate through json and render list items using Nunjucks templates
		var currentSort = urlParserInst.getSort();
		var resultData = dataInst.getResultList();
		var listItems = nunjucks.render('list/list_elements.html',
			{
			resultData: resultData
		});
		$('.list.content').html(listItems);

		$('.list.title').find('i').attr('class', '');
		if (currentSort.slice(0, 1) === '+') {
			$('.list.title').find('#' + currentSort.slice(1)).find('i').attr('class', 'icon-triangle-up');
		}
		else {
			$('.list.title').find('#' + currentSort.slice(1)).find('i').attr('class', 'icon-triangle-down');
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
					var event = dataInst.getResultListSingle(selectedItem.attr('id'));
					var previousSiblings = selectedItem.prevAll();
					var scrollHeight = 0;
					if ($('.sidebar').hasClass('invisible')) {
						$('.sidebar').one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend',
							function(e) {
								scrollHeight = previousSiblings.height() * previousSiblings.length;
								$('.list.content').animate({ scrollTop: scrollHeight }, 100);
								map.invalidateSize();
								setHeight();
								$('.main-list').addClass('shrunk');
							});
					}
					else {
						scrollHeight = previousSiblings.height() * previousSiblings.length;
						$('.list.content').animate({ scrollTop: scrollHeight }, 100);
					}
					detailViewInst.updateContent(event);
				}
				//If the clicked item is now inactive (occurs when you click an active item),
				//clear the detail panel content and map
				else {
					detailViewInst.hideContent();
					detailViewInst.clearMap(map);
					$('.list.content').height(restoreHeight());
					$('.main-list').removeClass('shrunk');
				}
			});
		setHeight();
		saveHeight($('.list.content').height());
	}

	//This is used to set the height of the div containing the list content.
	//It gets the height of the main-list div, then subtracts the 30-pixel height of the header
	//and sets the list content div to this figure.
	//This allows for making the content scrollable while leaving the header alone.
	function setHeight() {
		var parentHeight = $('.main-list').height();
		var headerHeight = $('.list.title').height();
		var sortHeight = $('.sort').outerHeight();
		if (window.innerHeight < window.innerWidth) {
			$('.list.content').height(parentHeight - headerHeight - sortHeight);
		}
		else {
			$('.list.content').height($('.main-list').height() - sortHeight);
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
