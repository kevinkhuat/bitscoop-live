//Render the List View on the main page
function listView(detailViewInst, dataInst, urlParserInst) {
	var contentHeight = 0;
	//Render the base framework of the List View
	function renderContent(promise) {
		//Render the list title and the container for the list elements using Nunjucks
		//and insert them into the DOM
		var list = nunjucks.render('list/list.html');
		$('.list-view').html(list);

		//Create an instance of the Detail panel and render the List View's content.
		var thisDetailViewInst = detailViewInst.renderContent(false);

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

				dataInst.state.view.sort = searchSort;
				urlParserInst.updateHash();
				//Do a search with the new sort
				//FIXME: calling the API for every new sorting request is not remotely ideal,
				//so this needs to be changed at some point
				dataInst.search('event', dataInst.state.query.event.searchString);
				urlParserInst.updateHash();
			});
		promise.resolve();
	}

	function restoreHeight() {
		return contentHeight;
	}

	function saveHeight(height) {
		contentHeight = height;
	}

	function highlight(id, eventActive) {
		var selectedItem = $('#' + id);
		if (window.window.devicePixelRatio > 1.5) {
			selectedItem.removeClass('hover');
		}

		selectedItem.siblings().removeClass('active');
		if (eventActive) {
			selectedItem.addClass('active');
			var event = dataInst.eventCache.events[selectedItem.attr('id')];
			var previousSiblings = selectedItem.prevAll();
			var scrollHeight = 0;
			for (var index = 0; index < previousSiblings.length; index++) {
				scrollHeight += $(previousSiblings[index]).height();
			}
			if ($('.sidebar').hasClass('invisible')) {
				$('.sidebar').one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend',
					function(e) {
						$('.list.content').animate({ scrollTop: scrollHeight }, 100);
						setHeight();
						$('.main-list').addClass('shrunk');
					});
			}
			else {
				$('.list.content').animate({ scrollTop: scrollHeight }, 100);
			}
			detailViewInst.updateContent(event);
		}
		else {
			selectedItem.removeClass('active');
			detailViewInst.hideContent();
			$('.list.content').height(restoreHeight());
			$('.main-list').removeClass('shrunk');
		}
	}

	//Update the List View content
	function updateContent() {
		//Iterate through json and render list items using Nunjucks templates
		var currentSort = dataInst.state.view.sort;
		var resultData = dataInst.resultCache.events;
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
				if (!(selectedItem.hasClass('active'))) {
					dataInst.state.selected = {};
					dataInst.state.selected[selectedItem.attr('id')] = true;
					dataInst.highlight(true);
				}
				else {
					dataInst.highlight(false);
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
		highlight: highlight,
		renderContent: renderContent,
		updateContent: updateContent
	};
}
