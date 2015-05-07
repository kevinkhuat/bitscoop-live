//View pertaining to obtaining and searching for data
function dataStore() {
	//This is the CSRF token that is used to authenticate server requests
	var cookie = sessionsCookies().getCsrfToken();

	var eventCache = {
		events: {},
		subtypes: {
			messages: [],
			plays: []
		}
	};

	var resultCache = {
		events: {},
		page: {
			current: 1,
			start: 0,
			end: 0,
			max: 0,
			total: 0
		},
		count: 0
	}

	var state = {
		view: {
			active: {
				map: true,
				list: true,
				count: 2
			},
			instances: {
				map: null,
				list: null
			},
			map: {
				zoom: 0,
				focus: []
			},
			list: {

			},
			sort: '-datetime'
		},
		selected: {
		},
		query: {
			event: {
				enabled: true,
				searchString: ''
			},
			message: {
				enabled: false,
				searchString: ''
			},
			play: {
				enabled: false,
				searchString: ''
			}
		}
	};

	function updateResults(documentType) {
		//Check each item to see if it's been fetched already
		//If not, add it to the cache
		for (var item in resultCache.events) {
			var currentItem = resultCache.events[item];
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

	function highlight(eventActive) {
		for (item in state.view.instances) {
			for (event in state.selected) {
				state.view.instances[item].highlight(event, eventActive);
			}
		}
		if (!(eventActive)) {
			state.selected = {};
		}
	}

	function createPageBar() {
		var sortBar = nunjucks.render('search/sort.html',
			{
				sort: {
					total_results: resultCache.count,
					start_index: resultCache.count > 0 ? resultCache.page.start : 0,
					end_index: resultCache.page.end,
					mobile: (window.window.devicePixelRatio > 1.5)
				}
		});
		$('.sort').html(sortBar);

		if (state.view.sort.slice(0, 1) === '+') {
			$('.sort .menu').find('#' + state.view.sort.slice(1)).find('i').attr('class', 'icon-triangle-up');
		}
		else {
			$('.sort .menu').find('#' + state.view.sort.slice(1)).find('i').attr('class', 'icon-triangle-down');
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
				resultCache.page.current = resultCache.page.current - 1;
				if (resultCache.page.current === 1) {
					$('.previous-page').addClass('disabled');
				}
				if (resultCache.page.total !== 1) {
					$('.next-page').removeClass('disabled');
				}
				search('event', state.query.event.searchString);
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
				resultCache.page.current = resultCache.page.current + 1;
				if (resultCache.page.current === resultCache.page.total) {
					$('.next-page').addClass('disabled');
				}
				if (resultCache.page.total !== 1) {
					$('.previous-page').removeClass('disabled');
				}
				search('event', state.query.event.searchString);
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
				resultCache.page.current = 1;
				//Change the current header's sort icon
				//If it's currently sorting by something, sort by the other way
				if (state.view.sort[0] === '-') {
					searchSort = '+' + $(this)[0].id;
				}
				else if (state.view.sort[0] === '+') {
					searchSort = '-' + $(this)[0].id;
				}

				state.view.sort = searchSort;
				//Do a search with the new sort
				//FIXME: calling the API for every new sorting request is not remotely ideal,
				//so this needs to be changed at some point
				search('event', state.query.event.searchString);
			});
	}

	//Search for items in the database based on the search parameters and filters
	function search(documentType, searchString, promise) {
		var url = 'opi/' + documentType + '?page=' + resultCache.page.current + '&ordering=' + state.view.sort + '&filter=' + searchString;
		console.log(url);
		$.ajax({
			url: url,
			type: 'GET',
			dataType: 'json',
			headers: {
				'X-CSRFToken': cookie
			}
		}).done(function(data, xhr, response) {
			var results = data.results;
			resultCache.count = data.count;
			resultCache.page.max = data.page_size;
			resultCache.page.total = Math.ceil(resultCache.count / resultCache.page.max);
			resultCache.page.start = ((resultCache.page.current - 1) * resultCache.page.max) + 1;
			resultCache.page.end = (resultCache.page.current * resultCache.page.max > resultCache.count) ? (resultCache.count) : (resultCache.page.current * resultCache.page.max);
			resultCache.events = {};
			for (item in results) {
				var thisItem = results[item];
				resultCache.events[thisItem.id] = thisItem;
			}
			for (var index in resultCache.events) {
				resultCache.events[index].updated = new Date(resultCache.events[index].updated).toLocaleString();
				resultCache.events[index].created = new Date(resultCache.events[index].created).toLocaleString();
				resultCache.events[index].datetime = new Date(resultCache.events[index].datetime).toLocaleString();
			}
			updateResults(documentType);
			createPageBar();

			for (item in state.view.instances) {
				if (state.view.instances[item] !== null)
				{
					state.view.instances[item].updateContent();
				}
			}
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
		getSingleDocument: getSingleDocument,
		highlight: highlight,
		resultCache: resultCache,
		search: search,
		state: state,
		updateResults: updateResults
	};
}

