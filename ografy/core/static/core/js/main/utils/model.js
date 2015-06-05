//View pertaining to obtaining and searching for data
function dataStore() {
	//This is the CSRF token that is used to authenticate server requests
	var cookie = sessionsCookies().getCsrfToken();

	//This is the definition of whether the device on which the page is rendered is a mobile device
	var isMobile = ((window.innerWidth < 1080 && window.devicePixelRatio >= 1.5) || (window.devicePixelRatio >= 3));

	//This caches all of the events that have been retrieved from searches.
	//The subtypes lists store the IDs of events that have been retrieved using subtype-specific APIs.
	//For example, a Message can be retrieved through the Event API, and it will contain all of the fields
	//except for those exclusive to Messages.  Once it's retrieved using the Message API, the event stored
	//in the events dictionary will be overwritten to contain the Message-specific fields as well as the common
	//Event fields.  The message subtype list would have the ID of that event added to indicate that that Event
	//has the Message fields present.
	var eventCache = {
		events: {},
		subtypes: {
			messages: [],
			plays: []
		}
	};

	//This stores all of the results from the most recent search, including all of the pagination information.
	var resultCache = {
		events: {},
		page: {
			current: 1,
			start: 0,
			end: 0,
			max: 0,
			total: 0
		},
		count: 0,
		query_id: ''
	};

	//This stores the state for the front-end.
	var state = {
		view: {
			//Active keeps track of whether each view is active or not.
			active: {
				map: true,
				list: true,
				count: 2
			},
			//Instances stores the instantiation of each view so that this module can reference them without
			//being passed them during its own instantiation, which would create a circular dependency.
			instances: {
				map: null,
				list: null
			},
			//Detail stores the instance of the detail sidebar.  It's separate from instances so that
			//all of the regular views can be iterated over without including the sidebar.
			detail: null,
			//Map and list store information particular to those views.
			map: {
				zoom: 0,
				focus: []
			},
			list: {

			},
			//This stores the current sort.
			sort: '-datetime'
		},
		//This stores which event(s) are currently selected and which will be showing more detailed information.
		//For now there will only be one event selected at a time, but that could change.
		selected: {
		},
		//This stores the filters (searchString) for each event type and whether it is enabled.
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
		//Check each item to see if it's been fetched already.  If not, add it to the cache.
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

	//When an event is selected or deselected, update the page's state to reflect this and
	//trigger each view's highlight function so that it is active in each view.
	function highlight(eventActive) {
		var events = [];
		//Get the events associated with the selected event IDs.
		for (var event_id in state.selected) {
			events.push(eventCache.events[event_id]);
			//Call each view's highlight function.
			for (var item in state.view.instances) {
				state.view.instances[item].highlight(event_id, eventActive);
			}
		}
		//Update the detail sidebar with the information of the selected events.
		for (var event in events) {
			state.view.detail.updateContent(events[event]);
		}
		//If the selected event is active and this is a mobile device, all views but one need to be
		//deactivated so that there's enough room for the detail sidebar.
		if (eventActive) {
			if (state.view.active.count > 1 && isMobile) {
				var activeViews = $('.view-button.active');
				for (var i = activeViews.length - 1; i > 0; i--) {
					var viewName = activeViews[i].id.slice(12);
					state.view.active[viewName] = false;
					state.view.active.count -= 1;
					$(activeViews[i]).removeClass('active');
					$('.' + viewName + '-view').addClass('hidden');
				}
			}
		}
		//If the selected event is not active, update the front-end state to reflect that and hide the detail sidebar.
		else if (!(eventActive)) {
			state.selected = {};
			state.view.detail.hideContent();
		}
	}

	//Creates and manages the pagination control bar.
	function createPageBar() {
		//Render the page bar and insert it into the DOM.
		var sortBar = nunjucks.render('search/sort.html',
			{
				sort: {
					total_results: resultCache.count,
					start_index: resultCache.count > 0 ? resultCache.page.start : 0,
					end_index: resultCache.page.end,
					mobile: (isMobile)
				}
		});
		$('.sort').html(sortBar);

		//Add a triangle up or down next to the sort field that is in use depending on which direction it is sorting.
		if (state.view.sort.slice(0, 1) === '+') {
			$('.sort .menu').find('#' + state.view.sort.slice(1)).find('i').attr('class', 'icon-triangle-up');
		}
		else {
			$('.sort .menu').find('#' + state.view.sort.slice(1)).find('i').attr('class', 'icon-triangle-down');
		}
		//Add event listeners to the previous page button for mouse-in/mouse-out and click.
		$('.previous-page').not('.disabled')
			.mouseenter(function() {
				$(this).addClass('hover');
			})
			.mouseleave(function() {
				$(this).removeClass('hover');
			})
			.click(function() {
				//Remove the hover class if the device is mobile so that it doesn't stay there
				//indefinitely on touch devices.
				if (isMobile) {
					$(this).removeClass('hover');
				}
				//Decrement the page number.
				resultCache.page.current = resultCache.page.current - 1;
				//If going to the first page, hide the previous page button.
				if (resultCache.page.current === 1) {
					$('.previous-page').addClass('disabled');
				}
				//If there is more than one page, the next page button will need to be visible
				//after going to a previous page no matter what.
				if (resultCache.page.total !== 1) {
					$('.next-page').removeClass('disabled');
				}
				//Run a search to get the new page.
				search('event', state.query.event.searchString);
			});

		//Add event listeners to the next page button for mouse-in/mouse-out and click.
		$('.next-page').not('.disabled')
			.mouseenter(function() {
				$(this).addClass('hover');
			})
			.mouseleave(function() {
				$(this).removeClass('hover');
			})
			.click(function() {
				//Remove the hover class if the device is mobile so that it doesn't stay there
				//indefinitely on touch devices.
				if (isMobile) {
					$(this).removeClass('hover');
				}
				//Increment the page number.
				resultCache.page.current = resultCache.page.current + 1;
				//If going to the last page, hide the next page button.
				if (resultCache.page.current === resultCache.page.total) {
					$('.next-page').addClass('disabled');
				}
				//If there is more than one page, the previous page button will need to be visible
				//after going to a next page no matter what.
				if (resultCache.page.total !== 1) {
					$('.previous-page').removeClass('disabled');
				}
				//Run a search to get the new page.
				search('event', state.query.event.searchString);
			});

		//Add event listeners to the sort menu button for mouse-in/mouse-out and click.
		$('.sort-button')
			.mouseenter(function() {
				$(this).addClass('hover');
			})
			.mouseleave(function() {
				$(this).removeClass('hover');
			})
			//Remove the hover class if the device is mobile so that it doesn't stay there
			//indefinitely on touch devices.
			.click(function() {
				if (isMobile) {
					$(this).removeClass('hover');
				}
				//Show or hide the sort menu on click.
				$('.sort .menu').toggleClass('hidden');
			});

		//Hide the sort menu if the user clicks outside of it.
		$(document.body).click(function(e) {
			if (!e.target.closest('.sort')) {
				$('.sort .menu').addClass('hidden');
			}
		});

		//Add event listeners to each sort menu entry for mouse-in/mouse-out and click.
		$('.sort .menu .item')
			.mouseenter(function() {
				$(this).addClass('hover');
			})
			.mouseleave(function() {
				$(this).removeClass('hover');
			})
			.click(function() {
				var searchSort;

				//Remove the hover class if the device is mobile so that it doesn't stay there
				//indefinitely on touch devices.
				if (isMobile) {
					$(this).removeClass('hover');
				}
				//On a new sort, always start on the first page of results.
				resultCache.page.current = 1;
				//Change the current header's sort icon.
				//If it's currently sorting by something, sort by the other way.
				if (state.view.sort[0] === '-') {
					searchSort = '+' + $(this)[0].id;
				}
				else if (state.view.sort[0] === '+') {
					searchSort = '-' + $(this)[0].id;
				}

				state.view.sort = searchSort;
				//Do a search with the new sort.
				//FIXME: calling the API for every new sorting request is not remotely ideal,
				//so this needs to be changed at some point
				search('event', state.query.event.searchString);
			});
	}

	//Search for items in the database based on the search parameters and filters
	function search(documentType, searchString, promise) {
		var url = 'opi/' + documentType + '?page=' + resultCache.page.current + '&ordering=' + state.view.sort;
		if (searchString.length > 0) {
			url += '&filter=' + searchString;
		}
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

			//Save all of the pagination information.
			resultCache.count = data.count;
			resultCache.page.max = data.page_size;
			resultCache.page.total = Math.ceil(resultCache.count / resultCache.page.max);
			resultCache.page.start = ((resultCache.page.current - 1) * resultCache.page.max) + 1;
			resultCache.page.end = (resultCache.page.current * resultCache.page.max > resultCache.count) ? (resultCache.count) : (resultCache.page.current * resultCache.page.max);

			//Clear the result cache and then save the new results to it.
			resultCache.events = {};
			for (var item in results) {
				var thisItem = results[item];
				resultCache.events[thisItem.id] = thisItem;
			}

			//Convert the datetimes to a more user-readable format.
			for (var index in resultCache.events) {
				resultCache.events[index].updated = new Date(resultCache.events[index].updated).toLocaleString();
				resultCache.events[index].created = new Date(resultCache.events[index].created).toLocaleString();
				resultCache.events[index].datetime = new Date(resultCache.events[index].datetime).toLocaleString();
			}

			//Update the event cache with any new information from this sort.
			updateResults(documentType);

			//Re-render the pagination bar with the new information.
			createPageBar();

			//Update each view with the results of the search.
			for (var item in state.view.instances) {
				if (state.view.instances[item] !== null)
				{
					state.view.instances[item].updateContent();
				}
			}
		});
	}

	//Gets a single event's information from the database.
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
			var eventId = newDocument.event.id;
			//If the event type is something other than Event, save the fact that it was
			//retrieved from the higher-level API and has the type-specific fields.
			if (documentType === 'message') {
				eventCache.subtypes.messages.push(thisId);
			}
			else if (documentType === 'play') {
				eventCache.subtypes.plays.push(thisId);
			}
			//Save the event to the cache and convert the datetimes to a more user-readable format.
			//FIXME: Populate extra Message/Play/etc. data better, i.e. don't just stick it on Event like we do here
			for (var index in newDocument) {
				if (index !== 'id') {
					eventCache.events[eventId][index] = newDocument[index];
				}
			}
			eventCache.events[eventId].created = new Date(eventCache.events[eventId].created).toLocaleString();
			eventCache.events[eventId].datetime = new Date(eventCache.events[eventId].datetime).toLocaleString();
			eventCache.events[eventId].updated = new Date(eventCache.events[eventId].updated).toLocaleString();
			//Resolve the input promise to indicate the function has completed.
			return promise.resolve();
		});
	}

	return {
		createPageBar: createPageBar,
		eventCache: eventCache,
		getSingleDocument: getSingleDocument,
		highlight: highlight,
		isMobile: isMobile,
		resultCache: resultCache,
		search: search,
		state: state,
		updateResults: updateResults
	};
}

