//Render the List View on the main page
function listView(dataInst, urlParserInst) {
	//This saves the height of the list content before it's compressed due to the detail sidebar appearing.
	var contentHeight = 0;

	//Render the base framework of the List View
	function renderContent(promise) {
		//Render the list title and the container for the list elements using Nunjucks
		//and insert them into the DOM
		var list = nunjucks.render('list/list.html');
		$('.list-view').html(list);

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
				dataInst.resultCache.page.current = 1;
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

				//Save the new sort to the data model and update the URL.
				dataInst.state.view.sort = searchSort;
				urlParserInst.updateHash();
				//Do a search with the new sort
				//FIXME: calling the API for every new sorting request is not remotely ideal,
				//so this needs to be changed at some point
				dataInst.search('event', dataInst.state.query.event.searchString);
			});
		//Resolve the input promise to indicate that the list view has finished rendering.
		promise.resolve();
	}

	//Restore the saved height of the list content.
	function restoreHeight() {
		return contentHeight;
	}

	//Save the current height of the list content.
	function saveHeight(height) {
		contentHeight = height;
	}

	//Highlight a selected event on the map.
	function highlight(id, eventActive) {
		var selectedItem = $('#' + id);
		//Remove the hover class on mobile so that it doesn't stay there permanently.
		if (dataInst.isMobile) {
			selectedItem.removeClass('hover');
		}

		//Remove the active class from any other list elements.
		selectedItem.siblings().removeClass('active');
		//If the given event has been selected (i.e. has not been de-selected), set it to 'active'
		//and scroll down to it.
		if (eventActive) {
			var event = dataInst.eventCache.events[selectedItem.attr('id')];
			var previousSiblings = selectedItem.prevAll();
			var scrollHeight = 0;

			selectedItem.addClass('active');
			//Sum the heights of all the list elements above the selected one so that they can be scrolled past.
			for (var index = 0; index < previousSiblings.length; index++) {
				scrollHeight += $(previousSiblings[index]).height();
			}
			//If the sidebar is going to be popping out, wait until it is finished.
			if ($('.sidebar').hasClass('invisible')) {
				$('.sidebar').one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend',
					function(e) {
						//Scroll to the selected event and set the height of the list content to account for
						//the sidebar potentially taking up vertical space.
						$('.list.content').animate({ scrollTop: scrollHeight }, 100);
						setHeight();
						$('.main-list').addClass('shrunk');
					});
			}
			else {
				//If the sidebar is already present, just scroll to the selected event.
				$('.list.content').animate({ scrollTop: scrollHeight }, 100);
			}
		}
		//If the given event has been de-selected, remove the 'active' class and restore the list to its full height.
		else {
			selectedItem.removeClass('active');
			$('.list.content').height(restoreHeight());
			$('.main-list').removeClass('shrunk');
		}
	}

	//Update the List View content
	function updateContent() {
		//Iterate through json and render list items using Nunjucks templates, then insert it into the DOM.
		var currentSort = dataInst.state.view.sort;
		var resultData = dataInst.resultCache.events;
		var listItems = nunjucks.render('list/list_elements.html',
			{
			resultData: resultData
		});
		$('.list.content').html(listItems);

		//Place an up or down triangle in the title of the column that is being sorted on.
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
				//Bind an event listener that triggers when an item on the map is selected.
				//This will clear the data model's selected field, add the clicked event to the selected field,
				//and call the data model's highlight function.
				//Note that this doesn't directly call this module's highlight function, as the data model's highlight
				//function calls each view's highlight function.
				var selectedItem = $(this);
				if (!(selectedItem.hasClass('active'))) {
					dataInst.state.selected = {};
					dataInst.state.selected[selectedItem.attr('id')] = true;
					dataInst.highlight(true);
				}
				else {
					dataInst.highlight(false);
				}
			});
		//If the list view is now active, set and save its full height.
		if (dataInst.state.view.active.list) {
			setHeight();
			saveHeight($('.list.content').height());
		}
	}

	//This is used to set the height of the div containing the list content.
	//This allows for making the content scrollable while leaving the header alone.
	function setHeight() {
		var parentHeight = $('.main-list').height();
		var headerHeight = $('.list.title').height();
		var sortHeight = $('.sort').outerHeight();
		//In landscape view, there will be a header on the list.
		//The height will be the full height of the list container minus the height of the header and the sort bar.
		if (window.innerHeight < window.innerWidth) {
			$('.list.content').height(parentHeight - headerHeight - sortHeight);
		}
		//In portrait view, the height will be the full height of the list container minus the height of the sort bar.
		//There is no header in this case.
		else {
			$('.list.content').height($('.list-view').height() - sortHeight);
		}
	}

	//Create an event listener to set a new height when the window is re-sized.
	$(window).resize(function() {
		setHeight();
	});

	return {
		highlight: highlight,
		renderContent: renderContent,
		setHeight: setHeight,
		updateContent: updateContent
	};
}
