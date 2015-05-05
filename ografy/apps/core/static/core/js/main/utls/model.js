//View pertaining to obtaining and searching for data
function dataStore(urlParserInst) {
	//This is the CSRF token that is used to authenticate server requests
	var cookie = sessionsCookies().getCsrfToken();

	var eventCache = {
		events: {},
		subtypes: {
			messages: [],
			plays: []
		},
		resultList: []
	};

	//Number of results from the search
	var resultCount = 0;

	//Number of pages from the search
	var resultPages = 0;

	//Current page of results
	var resultCurrentPage = 1;

	var resultPageSize = 0;

	var resultCurrentStartIndex = 0;
	var resultCurrentEndIndex = 0;

	var currentSort = '-datetime';

	var currentViewInst = '';

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
		//Check each item to see if it's been fetched already
		//If not, add it to the cache
		for (var item in eventCache.resultList) {
			var currentItem = eventCache.resultList[item];
			var currentId = currentItem.id;
			var tempIndex;

			//If the search was for an event, just check if it's in the event cache and add it if it's not
			if (documentType === 'event') {
				if (!(currentId in eventCache.events)) {
					eventCache.events[currentId] = currentItem;
				}
			}
			//If the search was for a subtype, check if it was fetched as that subtype
			//If not, then even if it was fetched as an Event, it needs to be overwritten to include the fields not
			//present on its Event.
			else {
				//Check the subtype list to see if it was fetched as that subtype
				if (documentType === 'message') {
					tempIndex = eventCache.subtypes.messages;
				}
				else if (documentType === 'play') {
					tempIndex = eventCache.subtypes.plays;
				}

				//If it wasn't fetched as that subtype, add it to the Event cache, overwriting anything that may be there
				if (!(currentId in tempIndex)) {
					tempIndex.push(currentId);
					eventCache.events[currentId] = currentItem;
				}
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
			eventCache.resultList = data.results;
			for (var index in eventCache.resultList) {
				eventCache.resultList[index].updated = new Date(eventCache.resultList[index].updated).toLocaleString();
				eventCache.resultList[index].created = new Date(eventCache.resultList[index].created).toLocaleString();
				eventCache.resultList[index].datetime = new Date(eventCache.resultList[index].datetime).toLocaleString();
			}
			updateResults(documentType);
			createPageBar();
			currentViewInst.updateContent();
		});
	}

	function getSingleDocument(documentType, id, promise) {
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
			var thisId = newDocument.id;
			if (documentType === 'message') {
				eventCache.subtypes.messages.push(thisId);
			}
			else if (documentType === 'play') {
				eventCache.subtypes.plays.push(thisId);
			}
			eventCache.events[thisId] = newDocument;
			eventCache.events[thisId].created = new Date(eventCache.events[thisId].created).toLocaleString();
			eventCache.events[thisId].datetime = new Date(eventCache.events[thisId].datetime).toLocaleString();
			eventCache.events[thisId].updated = new Date(eventCache.events[thisId].updated).toLocaleString();
			return promise.resolve();
		});
	}

	return {
		createPageBar: createPageBar,
		eventCache: eventCache,
		getCurrentView: getCurrentView,
		getResultCount: getResultCount,
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

