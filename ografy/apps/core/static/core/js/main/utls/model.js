//View pertaining to obtaining and searching for data
function dataStore(urlParserInst) {
	//This is the array of events that is returned from a search
	var resultData = [];

	//Number of results from the search
	var resultCount = 0;

	//Number of pages from the search
	var resultPages = 0;

	//Current page of results
	var resultCurrentPage = 1;

	var resultPageSize = 0;

	var resultCurrentStartIndex = 0;
	var resultCurrentEndIndex = 0;

	//This is a dictionary of the IDs of events that have been obtained in previous searches
	var eventIndex = {};

	//This is the master list of events that have been obtained in previous searches
	var eventData = [];

	//This is the list of events in the current search that have not been obtained in previous searches
	var newData = [];

	//This is the collection of HTML elements that are rendered from eventData
	//Most of them will be set to invisible since only ones from the current search
	//should be displayed.
	var eventHTML = '';

	var currentOrder = '-datetime';

	var currentViewInst = '';

	//Data model
	function getEventData() {
		return eventData;
	}

	function getResultData() {
		return resultData;
	}

	function getResultCount() {
		return resultCount;
	}

	function getResultCurrentPage() {
		return resultCurrentPage;
	}

	function getResultTotalPages() {
		return resultPages;
	}

	function getResultCurrentStartIndex() {
		return resultCurrentStartIndex;
	}

	function getResultCurrentEndIndex() {
		return resultCurrentEndIndex;
	}

	function setResultCurrentPage(page_num) {
		resultCurrentPage = page_num;
	}

	function getCurrentOrder() {
		return currentOrder;
	}

	function setCurrentOrder(new_order) {
		currentOrder = new_order;
	}

	function setCurrentView(inst) {
		currentViewInst = inst;
	}

	function getCurrentView() {
		return currentViewInst;
	}

	function updateData() {
		newData = [];
		for (var item in resultData) {
			var currentId = resultData[item].id;

			var removed = false;
			var keys = Object.keys(eventIndex);
			for (var index in keys) {
				if (currentId === keys[index]) {
					removed = true;
				}
			}
			if (removed === false) {
				newData.push(resultData[item]);
				eventIndex[currentId] = true;
				eventData.push(resultData[item]);
			}
		}

		var listItems = nunjucks.render('list/event_list.html',
			{
				eventData: newData
			});
		$('#event-list').append(listItems);

		currentEvents = $('#event-list *');
		for (var index in eventData) {
			var found = false;
			var thisEvent = eventData[index];
			var id = thisEvent.id;
			for (var item in resultData) {
				var thisItem = resultData[item];
				if (id === thisItem.id) {
					found = true;
				}
			}

			if (found === true) {
				$('div[event-id=' + id + ']').addClass('active');
			}
			else if (found === false) {
				$('div[event-id=' + id + ']').removeClass('active');
			}
		}
	}

	function createPageBar() {

		var orderBar = nunjucks.render('search/order.html',
			{
				order: {
					total_results: resultCount,
					start_index: resultCurrentStartIndex,
					end_index: resultCurrentEndIndex,
					mobile: (window.window.devicePixelRatio > 1.5)
				}
		});
		$('.order').html(orderBar);
		if (currentOrder.slice(0,1) === '+') {
			$('.menu.sort').find('#' + currentOrder.slice(1)).find('i').attr('class', 'icon-triangle-up');
		}
		else {

			$('.menu.sort').find('#' + currentOrder.slice(1)).find('i').attr('class', 'icon-triangle-down');
		}
		$('.previous-page').not('.disabled')
			.mouseenter(function() {
				$(this).addClass('hover');
			})
			.mouseleave(function() {
				$(this).removeClass('hover');
			})
			.click(function() {
				if (window.window.devicePixelRatio > 1.5) {
					$(this).removeClass('hover');
				}
				setResultCurrentPage(getResultCurrentPage() - 1);
				if(getResultCurrentPage === 1) {
					$('.previous-page').addClass('disabled');
				}
				if (getResultTotalPages() !== 1) {
					$('.next-page').removeClass('disabled');
				}
				search('event', urlParserInst.getSearchFilters(), getCurrentOrder());
			});

		$('.next-page').not('.disabled')
			.mouseenter(function() {
				$(this).addClass('hover');
			})
			.mouseleave(function() {
				$(this).removeClass('hover');
			})
			.click(function() {
				if (window.window.devicePixelRatio > 1.5) {
					$(this).removeClass('hover');
				}
				setResultCurrentPage(getResultCurrentPage() + 1);
				if (getResultCurrentPage() === getResultTotalPages()) {
					$('.next-page').addClass('disabled');
				}
				if (getResultTotalPages !== 1) {
					$('.previous-page').removeClass('disabled');
				}
				search('event', urlParserInst.getSearchFilters(), getCurrentOrder());
			});

		$('.sort-button')
			.mouseenter(function() {
				$(this).addClass('hover');
			})
			.mouseleave(function() {
				$(this).removeClass('hover');
			})
			.click(function() {
				if (window.window.devicePixelRatio > 1.5) {
					$(this).removeClass('hover');
				}
				$('.menu.sort').toggleClass('hidden');
			});

			$(document.body).click(function(e) {
				if (!e.target.closest('.order')) {
					$('.menu.sort').addClass('hidden');
				}
			});

		$('.menu.sort .item')
			.mouseenter(function() {
				$(this).addClass('hover');
			})
			.mouseleave(function() {
				$(this).removeClass('hover');
			})
			.click(function() {
				if (window.window.devicePixelRatio > 1.5) {
					$(this).removeClass('hover');
				}
				setResultCurrentPage(1);
				//Change the current header's order icon
				//If it's currently ordering by something, order by the other way
				if (currentOrder[0] === '-') {
					searchOrder = '+' + $(this)[0].id;
				}
				else if (currentOrder[0] === '+') {
					searchOrder = '-' + $(this)[0].id;
				}

				setCurrentOrder(searchOrder);
				//Do a search with the new order
				//FIXME: calling the API for every new ordering request is not remotely ideal,
				//so this needs to be changed at some point
				search('event', urlParserInst.getSearchFilters(), searchOrder);
			});
	}

	//Search for items in the database based on the search parameters and filters
	function search(eventType, searchString, orderString) {
		var cookie = sessionsCookies().getCsrfToken();
		var url = 'opi/' + eventType + '?page=' + resultCurrentPage + '&ordering='+ orderString + '&filter=' + searchString;
		console.log(url);
		$.ajax({
			url: url,
			type: 'GET',
			dataType: 'json',
			headers: {
				'X-CSRFToken': cookie
			}
		}).done(function(data, xhr, response) {
			if (data.count > 0) {
				resultCount = data.count;
				resultPageSize = data.page_size;
				resultPages = Math.ceil(resultCount/resultPageSize);
				resultCurrentStartIndex = ((resultCurrentPage - 1) * resultPageSize) + 1;
				resultCurrentEndIndex = (resultCurrentPage*resultPageSize > resultCount) ? (resultCount) : (resultCurrentPage*resultPageSize);
				results = data.results;
				for (var index in results) {
					results[index].updated = new Date(results[index].updated).toLocaleString();
					results[index].created = new Date(results[index].created).toLocaleString();
					results[index].datetime = new Date(results[index].datetime).toLocaleString();
				}
				resultData = results;
				updateData();
				createPageBar();
				currentViewInst.updateContent();
			}
			else if (data.count === 0) {
			}
		});
	}

	return {
		createPageBar: createPageBar,
		getEventData: getEventData,
		getResultCount: getResultCount,
		getResultData: getResultData,
		getResultCurrentPage: getResultCurrentPage,
		setResultCurrentPage: setResultCurrentPage,
		getResultCurrentStartIndex: getResultCurrentStartIndex,
		getResultCurrentEndIndex: getResultCurrentEndIndex,
		getResultTotalPages: getResultTotalPages,
		getCurrentOrder: getCurrentOrder,
		setCurrentOrder: setCurrentOrder,
		getCurrentView: getCurrentView,
		setCurrentView: setCurrentView,
		updateData: updateData,
		search: search
	};
}

