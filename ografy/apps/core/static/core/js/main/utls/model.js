//View pertaining to obtaining and searching for data
function dataStore(urlParserInst) {
	//This is the array of events that is returned from a search
	var resultList = [];

	//Number of results from the search
	var resultCount = 0;

	//Number of pages from the search
	var resultPages = 0;

	//Current page of results
	var resultCurrentPage = 1;

	var resultPageSize = 0;

	var resultCurrentStartIndex = 0;
	var resultCurrentEndIndex = 0;

	//This are dictionaries of the IDs of document types that have been obtained in previous searches
	var dataIndex = {};
	var eventIndex = {};
	var messageIndex = {};
	var playIndex = {};

	//This are master lists of document types that have been obtained in previous searches
	var eventList = [];

	//This is the list of results in the current search that have not been obtained in previous searches
	var newResults = [];

	//This is the collection of HTML elements that are rendered from eventList
	//Most of them will be set to invisible since only ones from the current search
	//should be displayed.
	var eventHTML = '';

	var currentSort = '-datetime';

	var currentViewInst = '';

	//Data model
	function getEventList() {
		return eventList ;
	}

	function getDataIndex() {
		return dataIndex;
	}

	function getEventIndex() {
		return eventIndex;
	}

	function getMessageIndex() {
		return messageIndex;
	}

	function getPlayIndex() {
		return playIndex;
	}

	function getResultListSingle(id) {
		for (var i in eventList) {
			if (eventList[i].id === id) {
				return eventList[i];
			}
		}
	}

	function getResultList() {
		return resultList;
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

	function setCurrentView(inst) {
		currentViewInst = inst;
	}

	function getCurrentView() {
		return currentViewInst;
	}

	function updateResults(documentType) {
		newResults = [];
		for (var item in resultList) {
			var currentId = resultList[item].id;
			var tempList;
			var tempIndex;

			if (documentType === 'data') {
				tempList = dataList;
				tempIndex = dataIndex;
			}
			else if (documentType === 'event') {
				tempList = eventList;
				tempIndex = eventIndex;
			}
			else if (documentType === 'message') {
				tempList = messageList;
				tempIndex = messageIndex;
			}
			else if (documentType === 'play') {
				tempList = playList;
				tempIndex = playIndex;
			}

			if (!(currentId in tempIndex)) {
				newResults.push(resultList[item]);
				tempIndex[currentId] = tempList.length;
				tempList.push(resultList[item]);
			}
		}

		var listItems = nunjucks.render('list/event_list.html',
			{
				eventList: newResults
			});
		$('#event-list').append(listItems);

		currentEvents = $('#event-list *');
		for (var index in eventList) {
			var found = false;
			var thisEvent = eventList[index];
			var id = thisEvent.id;
			for (var item in resultList) {
				var thisItem = resultList[item];
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
		var currentSort = urlParserInst.getSort();
		var sortBar = nunjucks.render('search/sort.html',
			{
				sort: {
					total_results: resultCount,
					start_index: resultCount > 0 ? resultCurrentStartIndex : 0,
					end_index: resultCurrentEndIndex,
					mobile: (window.window.devicePixelRatio > 1.5)
				}
		});
		$('.sort').html(sortBar);

		if (currentSort.slice(0, 1) === '+') {
			$('.sort .menu').find('#' + currentSort.slice(1)).find('i').attr('class', 'icon-triangle-up');
		}
		else {
			$('.sort .menu').find('#' + currentSort.slice(1)).find('i').attr('class', 'icon-triangle-down');
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
				if (getResultCurrentPage === 1) {
					$('.previous-page').addClass('disabled');
				}
				if (getResultTotalPages() !== 1) {
					$('.next-page').removeClass('disabled');
				}
				search('event', urlParserInst.getSearchFilters(), currentSort);
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
				search('event', urlParserInst.getSearchFilters(), currentSort);
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
				$('.sort .menu').toggleClass('hidden');
			});

		$(document.body).click(function(e) {
			if (!e.target.closest('.sort')) {
				$('.sort .menu').addClass('hidden');
			}
		});

		$('.sort .menu .item')
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
				setResultCurrentPage(1);
				//Change the current header's sort icon
				//If it's currently sorting by something, sort by the other way
				if (currentSort[0] === '-') {
					searchSort = '+' + $(this)[0].id;
				}
				else if (currentSort[0] === '+') {
					searchSort = '-' + $(this)[0].id;
				}

				urlParserInst.setSort(searchSort);
				urlParserInst.updateHash();
				//Do a search with the new sort
				//FIXME: calling the API for every new sorting request is not remotely ideal,
				//so this needs to be changed at some point
				search('event', urlParserInst.getSearchFilters(), urlParserInst.getSort());
			});
	}

	//Search for items in the database based on the search parameters and filters
	function search(documentType, searchString, sortString) {
		var cookie = sessionsCookies().getCsrfToken();
		var url = 'opi/' + documentType + '?page=' + resultCurrentPage + '&ordering=' + sortString + '&filter=' + searchString;
		console.log(url);
		$.ajax({
			url: url,
			type: 'GET',
			dataType: 'json',
			headers: {
				'X-CSRFToken': cookie
			}
		}).done(function(data, xhr, response) {
			resultCount = data.count;
			resultPageSize = data.page_size;
			resultPages = Math.ceil(resultCount / resultPageSize);
			resultCurrentStartIndex = ((resultCurrentPage - 1) * resultPageSize) + 1;
			resultCurrentEndIndex = (resultCurrentPage * resultPageSize > resultCount) ? (resultCount) : (resultCurrentPage * resultPageSize);
			results = data.results;
			if (documentType === 'event') {
				for (var index in results) {
					results[index].updated = new Date(results[index].updated).toLocaleString();
					results[index].created = new Date(results[index].created).toLocaleString();
					results[index].datetime = new Date(results[index].datetime).toLocaleString();
				}
			}
			else if (documentType === 'message') {
			}
			resultList = results;
			updateResults(documentType);
			createPageBar();
			if (documentType === 'event') {
				currentViewInst.updateContent();
			}
		});
	}

	function getSingleDocument(documentType, id, promise) {
		var cookie = sessionsCookies().getCsrfToken();
		var url = 'opi/' + documentType + '/' + id;
		$.ajax({
			url: url,
			type: 'GET',
			dataType: 'json',
			headers: {
				'X-CSRFToken': cookie
			}
		}).done(function(data, xhr, response) {
			var newDocument = data;
			if (documentType === 'data') {
				dataIndex[newDocument.id] = newDocument.event_id;
				eventList[eventIndex[newDocument.event.id]].subtypeInstance = newDocument;
			}
			else if (documentType === 'message') {
				messageIndex[newDocument.id] = newDocument.event;
				eventList[eventIndex[newDocument.event.id]].subtypeInstance = newDocument;
			}
			else if (documentType === 'play') {
				playIndex[newDocument.id] = newDocument.event;
				eventList[eventIndex[newDocument.event.id]].subtypeInstance = newDocument;
			}
			return promise.resolve();
		});
	}

	return {
		createPageBar: createPageBar,
		getCurrentView: getCurrentView,
		getDataIndex: getDataIndex,
		getEventIndex: getEventIndex,
		getEventList: getEventList,
		getMessageIndex: getMessageIndex,
		getPlayIndex: getPlayIndex,
		getResultListSingle: getResultListSingle,
		getResultCount: getResultCount,
		getResultList: getResultList,
		getResultCurrentPage: getResultCurrentPage,
		getResultCurrentStartIndex: getResultCurrentStartIndex,
		getResultCurrentEndIndex: getResultCurrentEndIndex,
		getResultTotalPages: getResultTotalPages,
		getSingleDocument: getSingleDocument,
		search: search,
		setCurrentView: setCurrentView,
		setResultCurrentPage: setResultCurrentPage,
		updateResults: updateResults
	};
}

