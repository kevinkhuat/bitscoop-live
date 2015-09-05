define('search', ['jquery', 'jquery-deparam', 'lodash', 'nunjucks', 'jquery-cookie'], function($, deparam, _, nunjucks) {
	// https://ografy.io/map?s=Location:within([1,2],[3,4],[5,6])&limit=16&offset=32
	//
	// {
	//     "limit": 16,
	//     "offset": 32,
	//     "next": "https://ografy.io/map?slkjsdflkfsdjlkjfsd&limit=16&offset=48
	//

	//A list of the fields that can be searched by the query text
	var MAPPED_SEARCH_TEXT_FIELDS = [
		'contacts_list.handle',
		'contacts_list.name',
		'content_list.content_type',
		'content_list.file_extension',
		'content_list.owner',
		'content_list.text',
		'content_list.title',
		'content_list.url',
		'event_type',
		'provider_name'
	];
	var mainMap, instance;

	//This converts datetimes into a stringified form that we like.  All of the built-in functions are too verbose
	//or don't look the way we want.
	var stringifyDate = function(date) {
		var hours, minutes, ampm, datetime;

		hours = date.getHours()%12;
		hours = hours ? hours : 12;
		minutes = date.getMinutes();
		minutes = minutes < 10 ? '0' + minutes : minutes;
		ampm = date.getHours() >= 12 ? 'PM' : 'AM';

		datetime = date.toLocaleDateString() + ' ' + hours + ':' + minutes + ' ' + ampm;

		return datetime;
	};

	/**
	 * An abstract representation of a search filter.
	 *
	 * @constructor
	 */
	function Filter(id) {
		this.id = id;
	}

	Filter.prototype = {

		/**
		 * The functions that should be present in all filter types that inherit from this base filter.
		 */
		addToDSL: function Filter$addToDSL() {},
		retrieveValues: function Filter$retrieveValues() {},
		updateValues: function Filter$updateValues() {}
	};


	/**
	 * A filter for people/entities, and how they interacted with the user.
	 *
	 * The person/entity is saved in this.name, and that name is compared against each Contact's
	 * name or handle; this field does double-duty rather than having separate fields for each one
	 *
	 * The Contact Interaction Type is saved in this.contactInteractionType, and can be 'to', 'from', or 'with'.
	 *
	 *
	 * @param id The ID of the filter to be constructed
	 * @param context Any information to be used in constructing the filter
	 * @constructor
	 */
	function WhoFilter(id, context) {
		this.id = id;
		this.type = 'who';

		if (_.has(context, 'name')) {
			this.name = context.name;
		}

		if (_.has(context, 'contactInteractionType')) {
			this.contactInteractionType = context.contactInteractionType;
		}
	}

	WhoFilter.prototype = new Filter();
	WhoFilter.prototype.constructor = Filter;

	/**
	 * This adds a Who filter to the query DSL
	 *
	 * @param query The query DSL
	 */
	WhoFilter.prototype.addToDSL = function(query) {
		var newTerm;

		//If the user has specified a name to filter on
		if (this.name !== '') {
			//If the user has specified a Contact Interaction Type
			if (this.hasOwnProperty('contactInteractionType')) {
				newTerm = {
					and: [
						{
							or: [
								{
									term: {
										'contacts_list.name': this.name
									}
								},
								{
									term: {
										'contacts_list.handle': this.name
									}
								}
							]
						},
						{
							term: {
								contact_interaction_type: this.contactInteractionType.toLowerCase()
							}
						}
					]
				};
			}
			//If the user has not specified a Contact Interaction Type, in which case the name is the only
			//thing being filtered on in this filter
			else {
				newTerm = {
					and: [
						{
							or: [
								{
									term: {
										'contacts_list.name': this.name
									}
								},
								{
									term: {
										'contacts_list.handle': this.name
									}
								}
							]
						}
					]
				};
			}
		}
		//If the user has not specified a name to filter on
		else {
			//If the user has specified a Contact Interaction Type, in which case it is the only thing being filtered
			//on in this filter
			if (this.hasOwnProperty('contactInteractionType')) {
				newTerm = {
					and: [
						{
							term: {
								contact_interaction_type: this.contactInteractionType.toLowerCase()
							}
						}
					]
				};
			}
		}

		//Add the filter to the query DSL
		query.query.filtered.filter.and[0].bool.should.push(newTerm);
	};

	/**
	 * Get the values from this filter and return them in a dictionary called context
	 *
	 * @returns object The dictionary of values for this filter
	 */
	WhoFilter.prototype.retrieveValues = function() {
		var context = {};

		context.name = this.name;
		context.contactInteractionType = this.contactInteractionType;

		return context;
	};

	/**
	 * Get the values from the filter content DOM element and update this filter with them
	 */
	WhoFilter.prototype.updateValues = function() {
		var contactInteractionType =  $('.contactInteractionType').val();
		this.name = $('.namehandle').val();

		if (contactInteractionType !== 'Any') {
			this.contactInteractionType = contactInteractionType;
		}
	};


	/**
	 * A filter for content type
	 *
	 * The Content Type that the user is filtering on is saved as this.contentType
	 *
	 * @param id The ID of the filter to be constructed
	 * @param context Any information to be used in constructing the filter
	 * @constructor
	 */
	function WhatFilter(id, context) {
		this.id = id;
		this.type = 'what';

		if (_.has(context, 'contentType')) {
			this.contentType = context.contentType;
		}
	}

	WhatFilter.prototype = new Filter();
	WhatFilter.prototype.constructor = Filter;

	/**
	 * This adds a What filter to the query DSL
	 *
	 * @param query The query DSL
	 */
	WhatFilter.prototype.addToDSL = function(query) {
		var newTerm;

		newTerm = {
			term: {
				'content_list.content_type': this.contentType.toLowerCase()
			}
		};

		query.query.filtered.filter.and[0].bool.should.push(newTerm);
	};

	/**
	 * Get the values from this filter and return them in a dictionary called context
	 *
	 * @returns object The dictionary of values for this filter
	 */
	WhatFilter.prototype.retrieveValues = function() {
		var context = {};

		context.contentType = this.contentType;

		return context;
	};

	/**
	 * Get the values from the filter content DOM element and update this filter with them
	 */
	WhatFilter.prototype.updateValues = function() {
		this.contentType = $('.contentType').val();
	};


	/**
	 * A filter for where events took place
	 *
	 * A Where filter can either be inside/outside a polygon that the user draws manually (whereType 'area')
	 * or within/outside a user-defined radius from a marker the user placed on the map (whereType 'radius').
	 *
	 * For an area filter:
	 * The filter is for either inside or outside the polygon the user drew, so this.modifier will either be 'Inside' or 'Outside'.
	 * The coordinates of the polygon will be in a list saved to this.coordinates.
	 * this.mapId is the leaflet ID of the corresponding polygon.
	 * this.whereType is 'area'
	 *
	 * For a radius filter:
	 * this.radius is the user-specified radius from the marker.
	 * this.unit is either Miles or Kilometers, as selected by the user
	 * The filter is for either within or outside the radius from the marker, so this.Modifier will either be 'Within' or 'Outside'
	 * The coordinates of the marker will be saved to this.coordinates
	 * this.MapId is the leaflet ID of the corresponding marker
	 * this.whereType is 'radius'
	 *
	 *
	 * @param id The ID of the filter to be constructed
	 * @param context Any information to be used in constructing the filter
	 * @constructor
	 */
	function WhereFilter(id, context) {
		this.id = id;
		this.type = 'where';
		var leafletReturn, filterCoordinates;
		var leafletCoordinates = [];
		var featureGroup = mainMap.controls.draw.options.edit.featureGroup;

		if (_.has(context, 'radius')) {
			this.radius = context.radius;
		}

		if (_.has(context, 'unit')) {
			this.unit = context.unit;
		}

		this.modifier = context.modifier;
		this.coordinates = context.coordinates;
		this.mapId = context.mapId;
		this.whereType = context.whereType;


		//When a Where filter is being automatically constructed, its corresponding polygon/marker must be created on the map.
		if (Object.keys(context).length > 0) {
			var newFilter;

			//For radius Where filters
			if (context.whereType === 'radius') {
				//Construct the coordinate list for the leaflet marker
				leafletCoordinates.push(context.coordinates.lat, context.coordinates.lon);

				//In Cartano, coordinates are saved in a dictionary with keys 'lat' and 'lng'
				filterCoordinates = {
					lat: parseFloat(context.coordinates.lat),
					lng: parseFloat(context.coordinates.lon)
				};

				//Construct a Leaflet marker and add it to the map
				leafletReturn = L.marker(leafletCoordinates).addTo(featureGroup);

				//Save the Leaflet ID on the filter
				this.mapId = leafletReturn._leaflet_id;

				//Set up a filter to be saved in Cartano
				newFilter = {
					id: this.mapId,
					type: 'marker',
					element: mainMap.element,
					coordinates: [filterCoordinates],
					area: 0
				};
			}
			//For area Where filters
			else if (context.whereType === 'area') {
				//Push each of the polygon's coordinates onto a list
				filterCoordinates = [];
				_.forEach(context.coordinates, function(coordinateSet) {
					leafletCoordinates.push([parseFloat(coordinateSet.lat), parseFloat(coordinateSet.lon)]);

					//In Cartano, coordinates are saved in a dictionary with keys 'lat' and 'lng'
					filterCoordinates.push({
						lat: parseFloat(coordinateSet.lat),
						lng: parseFloat(coordinateSet.lon)
					});
				});

				//Construct a Leaflet polygon and add it to the map
				leafletReturn = L.polygon(leafletCoordinates).addTo(featureGroup);

				//Save the Leaflet ID on the filter
				this.mapId = leafletReturn._leaflet_id;

				//Set up a filter to be saved in Cartano
				newFilter = {
					id: this.mapId,
					type: 'polygon',
					element: mainMap.element,
					coordinates: [filterCoordinates],
					area: 0
				};
			}

			//Add the new filter to Cartano
			mainMap.geofilters[this.mapId] = newFilter;
		}
	}

	WhereFilter.prototype = new Filter();
	WhereFilter.prototype.constructor = Filter;

	/**
	 * This adds a Where filter to the query DSL
	 *
	 * @param query The query DSL
	 */
	WhereFilter.prototype.addToDSL = function(query) {
		var newTerm;

		//If the filter is a polygon
		if (this.whereType === 'area') {
			//If the filter is for events outside the polygon
			if (this.modifier === 'Outside') {
				newTerm = {
					not: {
						geo_polygon: {
							'location.geolocation': {
								points: this.coordinates
							}
						}
					}
				};
			}
			//If the filter is for events inside the polygon
			else if (this.modifier === 'Inside') {
				newTerm = {
					geo_polygon: {
						'location.geolocation': {
							points: this.coordinates
						}
					}
				};
			}
		}
		//If the filter is a radius surrounding a point
		else if (this.whereType === 'radius') {
			//If the filter is within the radius surrounding a point
			if (this.modifier === 'Within') {
				newTerm = {
					geo_distance: {
						distance: this.radius + this.unit.toLowerCase(),
						'location.geolocation': this.coordinates
					}
				};
			}
			//If the filter is outside the radius surrounding a point
			else if (this.modifier === 'Outside') {
				newTerm = {
					not: {
						geo_distance: {
							distance: this.radius + this.unit.toLowerCase(),
							'location.geolocation': this.coordinates
						}
					}
				};
			}
		}

		//Add the filter to the query
		query.query.filtered.filter.and[0].bool.should.push(newTerm);
	};

	/**
	 * Get the values from this filter and return them in a dictionary called context
	 *
	 * @returns object The dictionary of values for this filter
	 */
	WhereFilter.prototype.retrieveValues = function() {
		var context = {};

		context.coordinates = this.coordinates;
		context.mapId = this.mapId;

		if (this.whereType === 'area') {
			context.modifier = this.modifier;
			context.whereType = 'area';
		}
		else if (this.whereType === 'radius') {
			context.modifier = this.modifier;
			context.radius = this.radius;
			context.unit = this.unit;
			context.whereType = 'radius';
		}

		return context;
	};

	/**
	 * Get the values from the filter content DOM element and update this filter with them
	 */
	WhereFilter.prototype.updateValues = function() {
		var self = this;
		var $filterContent = $('[data-where-id][data-map-id]');

		this.modifier = $('.modifier').val();
		this.radius = $('.radius').val();
		this.unit = $('.distanceUnit').val();
		this.mapId = $filterContent.data('map-id');
		this.whereType = $filterContent.data('where-type');

		this.updateCoordinates();
	};

	/**
	 * Update the coordinates for this Where filter based on the coordinates of the filter on the map
	 */
	WhereFilter.prototype.updateCoordinates = function() {
		var self = this;

		//Get the Cartano filter that matches this filter
		var matchingGeofilter = _.find(mainMap.geofilters, function(geofilter) {
			return geofilter.id === self.mapId;
		});

		//Update the coordinates of this filter
		this.coordinates = matchingGeofilter.coordinates;
		//Mapbox abbreviates longitude as 'lng', but ElasticSearch expects it as 'lon', so make that conversion
		_.forEach(this.coordinates, function(coordinateSet) {
			coordinateSet.lon = coordinateSet.lng;
			delete coordinateSet.lng;
		});

		//A radius filter only has one set of coordinates, and ElasticSearch does not expect it to be in a list,
		//so set this.coordinates to just the coordinate set
		if (this.whereType === 'radius') {
			this.coordinates = this.coordinates[0];
		}
	};

	/**
	 * A filter for when an event took place
	 *
	 * The start and end datetimes are saved as this.startDate and this.endDate
	 *
	 * @param id The ID of the filter to be constructed
	 * @param context Any information to be used in constructing the filter
	 * @constructor
	 */
	function WhenFilter(id, context) {
		this.id = id;
		this.type = 'when';
		//this.startDate;
		//this.endDate;

		if (_.has(context, 'startDate')) {
			this.startDate = context.startDate;
		}

		if (_.has(context, 'endDate')) {
			this.endDate = context.endDate;
		}
	}

	WhenFilter.prototype = new Filter();
	WhenFilter.prototype.constructor = Filter;

	/**
	 * This adds a When filter to the query DSL
	 *
	 * @param query The query DSL
	 */
	WhenFilter.prototype.addToDSL = function(query) {
		var newTerm = {
			range: {
				datetime: {
					format: 'yyyy-MM-dd\'T\'HH:mm'
				}
			}
		};

		//If the filter contains a start date
		if (this.startDate !== undefined) {
			_.set(newTerm, 'range.datetime.gte', this.startDate);
		}

		//If the filter contains an end date
		if (this.endDate !== undefined) {
			_.set(newTerm, 'range.datetime.lte', this.endDate);
		}

		//Add the filter to the query
		query.query.filtered.filter.and[0].bool.should.push(newTerm);
	};

	/**
	 * Get the values from this filter and return them in a dictionary called context
	 *
	 * @returns object The dictionary of values for this filter
	 */
	WhenFilter.prototype.retrieveValues = function() {
		var context = {};

		context.startDate = this.startDate;
		context.endDate = this.endDate;

		return context;
	};

	/**
	 * Get the values from the filter content DOM element and update this filter with them
	 */
	WhenFilter.prototype.updateValues = function() {
		this.startDate = $('.startDate').val();
		this.endDate = $('.endDate').val();
	};


	/**
	 * A filter for which Provider an event came from
	 *
	 * The Provider Name is saved as this.providerName
	 *
	 * Once Python Social Auth is replaced with something that allows for connecting multiple accounts
	 * from the same Provider, this will probably be expanded so the user can search by Signal in addition
	 * to Provider.
	 *
	 * @param id The ID of the filter to be constructed
	 * @param context Any information to be used in constructing the filter
	 * @constructor
	 */
	function HowFilter(id, context) {
		this.id = id;
		this.type = 'how';
		//this.providerName;

		if (_.has(context, 'providerName')) {
			this.providerName = context.providerName;
		}
	}

	HowFilter.prototype = new Filter();
	HowFilter.prototype.constructor = Filter;


	/**
	 * This adds a How filter to the query DSL
	 *
	 * @param query The query DSL
	 */
	HowFilter.prototype.addToDSL = function(query) {
		var newTerm;

		newTerm = {
			term: {
				provider_name: this.providerName.toLowerCase()
			}
		};

		//Add the filter to the query
		query.query.filtered.filter.and[0].bool.should.push(newTerm);
	};

	/**
	 * Get the values from this filter and return them in a dictionary called context
	 *
	 * @returns object The dictionary of values for this filter
	 */
	HowFilter.prototype.retrieveValues = function() {
		var context = {};

		context.providerName = this.providerName;

		return context;
	};

	/**
	 * Get the values from the filter content DOM element and update this filter with them
	 */
	HowFilter.prototype.updateValues = function() {
		this.providerName = $('.providerName').val();
	};


	/**
	 * An abstract representation of a search. Contains the DOM representation and instance methods to convert the
	 * search to a DSL query before it's sent to the server.
	 *
	 * @constructor
	 */
	function Search() {
		this.searchDSL = {};
		//Each filter type has its own list and nextId.  Whenever a new filter of that type is created,
		//nextId is incremented
		this.filters = {
			who: {
				nextId: 0,
				list: []
			},
			what: {
				nextId: 0,
				list: []
			},
			where: {
				nextId: 0,
				list: []
			},
			when: {
				nextId: 0,
				list: []
			},
			how: {
				nextId: 0,
				list: []
			}
		};
	}

	Search.prototype = {
		/**
		 * Adds a new filter to the list of its type in this.filters, then calls for a new DOM representation to be added.
		 *
		 * @param filter The filter that has been constructed
		 * @constructor
		 */
		addFilter: function Search$addFilter(filter) {
			var type = filter.type;

			// Add filter of specified type to the internal list of filters.
			this.filters[type].nextId++;

			this.filters[type].list.push(filter);
			this.DOM.addFilter(this.filters[type].list[filter.id]);
		},

		/**
		 * This binds event listeners to a number of actions and defines the callback functions that should be run
		 * when those actions occur.
		 *
		 * @constructor
		 */
		_bind: function Search$_bind() {
			var self = this;

			/**
			 * This is called when a filter type is selected for a new filter.
			 * It un-highlights the other filter types and highlights the one selected.
			 * If then calls the DOM renderFilterContent function so that the user can select filter options.
			 *
			 * @param e The event that occurred
			 */
			var addFilterCallback = function(e) {
				var $this = $(e.target);
				var filterType = $this.data('filter-type');
				var context = {};

				//The How filters need to be rendered with the list of signals
				if (filterType === 'how') {
					context.signals = self.signals;
				}

				//Un-highlight the other filter types and highlight the one selected.
				$this.siblings().removeClass('active');
				$this.addClass('active');

				//Hide the cancel button next to the filter types, as a new one will be shown
				//in the Filter Content area, and having two is unnecessary and possibly confusing.
				$('.close.type').addClass('hidden');

				//Render the Filter Content for the filter type selected.
				self.DOM.renderFilterContent(filterType, self.filters[filterType].nextId, context);
			};

			/**
			 * Hide the filter types and the Filter Content area.
			 */
			var clearTypesCallback = function() {
				self.DOM.hideTypes();
				self.DOM.removeFilterContent();
			};

			/**
			 * This closes the Filter Content area and un-highlights all of the markers and polygons on the map
			 *
			 * @param e The event that occurred
			 */
			var closeContentCallback = function(e) {
				var $thisFilter = $(e.target).closest('[data-filter-type]');

				//If a Where filter had been open, un-highlight it.  If that filter hadn't been created yet,
				//then delete that shape, as the user has canceled the creation of that filter.
				if ($thisFilter.data('filter-type') === 'where') {
					var mapId = $thisFilter.data('map-id');
					var filterId = $thisFilter.data('where-id');

					var matchingFilter = _.find(self.filters.where.list, function(filter) {
						return filter.id === filterId;
					});

					//If the filter being edited in the Filter Content area hadn't been created yet, then
					//delete the polygon or marker from the map.
					if (matchingFilter === undefined) {
						self.DOM.removeGeofilter(mapId);
					}

					//Trying to highlight a geofilter with ID 0 will deselect all of them, as Leaflet starts
					//its count at 1.
					self.highlightCurrentGeofilter(0);
				}

				//Hide the Filter Content area and the filter types
				self.DOM.removeFilterContent();
				self.DOM.hideTypes();
			};

			/**
			 * This calls for the selected filter to be delted from both the internal store and the map
			 *
			 * @param e The event that occurred
			 */
			var removeFilterCallback = function(e) {
				var $this = $(e.target);
				var $parent = $this.parent();
				var filterType = $parent.data('filter-type');
				var filterId = $parent.data(filterType + '-id');

				self.removeFilter(filterId, filterType);
			};

			/**
			 * This populates the Filter Content area with the information from an existing filter
			 *
			 * @param e The event that occurred
			 */
			var renderFilterCallback = function(e) {
				var $this = $(e.target);

				//Highlight the filter that was selected and un-highlight the others
				$this.addClass('active');
				$this.siblings('.filter').removeClass('active');

				//Only populate the Filter Content area if the user didn't click on the remove button
				if (!($this.is('.remove'))) {
					var context;
					var $parent = $this.parent();
					var filterType = $parent.data('filter-type');
					var filterId = $parent.data(filterType + '-id');
					var thisFilter = _.find(self.filters[filterType].list, function(filter) {
						return filter.id === filterId;
					});

					//Get the filter's values
					context = thisFilter.retrieveValues();

					//If it's a Where filter, then highlight the corresponding marker or polygon on the map.
					if (filterType === 'where') {
						var mapId = thisFilter.mapId;

						self.highlightCurrentGeofilter(mapId);
					}

					//If it's a How filter, it needs the user's Signals in its context.
					if (filterType === 'how') {
						context.signals = self.signals;
					}

					//Render the Filter Content for this filter.
					self.DOM.renderFilterContent(filterType, filterId, context);
				}
			};

			/**
			 * Save the information in the Filter Content.  If it's an existing filter, then overwrite what's there.
			 * If it's a new filter, then create a new filter and save the values.
			 *
			 * @param e The event that occurred
			 */
			var saveFilterCallback = function(e) {
				var $this = $(e.target);
				var $parent = $this.parent();
				var filterType = $parent.data('filter-type');
				var filterId = $parent.data(filterType + '-id');
				var thisFilter = _.find(self.filters[filterType].list, function(filter) {
					return filter.id === filterId;
				});

				//If this is a new filter, create an instance of that filter type.
				if (thisFilter === undefined) {
					if (filterType === 'who') {
						thisFilter = new WhoFilter(self.filters[filterType].nextId, {});
					}
					else if (filterType === 'what') {
						thisFilter = new WhatFilter(self.filters[filterType].nextId, {});
					}
					else if (filterType === 'where') {
						thisFilter = new WhereFilter(self.filters[filterType].nextId, {});
					}
					else if (filterType === 'when') {
						thisFilter = new WhenFilter(self.filters[filterType].nextId, {});
					}
					else if (filterType === 'how') {
						thisFilter = new HowFilter(self.filters[filterType].nextId, {});
					}

					//Add the filter to the list of that filter type
					self.addFilter(thisFilter);
				}

				//Whether or not it was new, save the values in the Filter Content to the filter.
				thisFilter.updateValues();

				//Un-highlight all markers and polygons on the map.
				self.highlightCurrentGeofilter(0);

				//Hide the Filter Content and type areas
				self.DOM.removeFilterContent();
				self.DOM.hideTypes();

				//Update the text in the DOM representation of the filter.
				self.DOM.updateFilter(thisFilter);
			};

			//Show the types of filters in the DOM.
			var showTypesCallback = function() {
				self.DOM.showTypes();
			};

			//Create event listeners and indicate the callback functions they call.
			this.element
				.on('click', '.add.button.show', showTypesCallback)
				.on('click', '.add.button.type', addFilterCallback)
				.on('click', '.close.type', clearTypesCallback)
				.on('click', '.close.content', closeContentCallback)
				.on('click', '.remove', removeFilterCallback)
				.on('click', '.filter', renderFilterCallback)
				.on('click', '.save', saveFilterCallback);
		},

		/**
		 * Functions that manage the addition, removal, and updating of search DOM elements
		 */
		DOM: {
			/**
			 * Adds a new filter to the DOM.
			 *
			 * @param filter The filter being added
			 * @constructor
			 */
			addFilter: function Search$DOM$addFilter(filter) {
				var $filterContainer = $('#filters');

				//Render the new filter
				var filterDOM = nunjucks.render('templates/filter.html', {
					filter: filter
				});

				//Add the new filter right before the new filter button; the new filter button will always be at the
				//very end of the filter set
				$(filterDOM).insertBefore($filterContainer.children().last());
			},

			/**
			 * //Hide the filter types area
			 *
			 * @constructor
			 */
			hideTypes: function Search$DOM$hideTypes() {
				$('.add.button.type').removeClass('active');
				$('#filterTypes').addClass('hidden');
			},

			/**
			 * Remove a filter from the DOM
			 *
			 * @param filterId The ID of the filter being removed
			 * @param type The type of filter being removed
			 * @constructor
			 */
			removeFilter: function Search$DOM$removeFilter(filterId, type) {
				var $this = $('[data-' + type + '-id=' + filterId + ']');
				$this.remove();
			},

			/**
			 * Hide the Filter Content area (basically just set its HTML content to nothing)
			 *
			 * @constructor
			 */
			removeFilterContent: function Search$DOM$removeFilter() {
				$('.filter-content').html('');
			},

			/**
			 * Remove a map element corresponding to given Where filter from the map.
			 *
			 * @param mapId The ID of the map element to be removed
			 * @constructor
			 */
			removeGeofilter: function Search$DOM$removeGeofilter(mapId) {
				mainMap.controls.draw.options.edit.featureGroup.removeLayer(mapId);
				delete mainMap.geofilters[mapId];
			},

			/**
			 * This populates the Filter Content area with the tools for editing a specified filter type.
			 *
			 * @param type The type of filter being created or edited
			 * @param id The ID of the filter being created or edited
			 * @param context The context of the filter being created or edited
			 * @constructor
			 */
			renderFilterContent: function Search$DOM$renderFilterContent(type, id, context) {
				var filterContentDOM = nunjucks.render('templates/filter_content.html', {
					context: context,
					id: id,
					type: type
				});

				$('.filter-content').html(filterContentDOM);
			},

			/**
			 * Un-hide the filter types area.
			 *
			 * @constructor
			 */
			showTypes: function Search$DOM$showTypes() {
				$('.close.type').removeClass('hidden');
				$('#filterTypes').removeClass('hidden');
			},

			/**
			 * This updates the text in the DOM filter to reflect that filter's content.
			 *
			 * @param filter The filter being updated
			 * @constructor
			 */
			updateFilter: function Search$DOM$updateFilter(filter) {
				var filterDOM;

				//If it's a When filter, its Start Date and/or End Date need to be properly stringified before
				//nunjucks renders the filter DOM element.
				if (filter.type === 'when') {
					var startDate = new Date(filter.startDate);
					var endDate = new Date(filter.endDate);
					filterDOM = nunjucks.render('templates/filter.html', {
						filter: filter,
						update: true,
						startDate: stringifyDate(new Date(startDate.getTime() + startDate.getTimezoneOffset() * 60 * 1000)),
						endDate: stringifyDate(new Date(endDate.getTime() + endDate.getTimezoneOffset() * 60 * 1000))
					});
				}
				//All other filter types need no special parsing
				else {
					filterDOM = nunjucks.render('templates/filter.html', {
						filter: filter,
						update: true
					});
				}

				//Replace the filter DOM element currently there with the new one.
				$('[data-' + filter.type + '-id=' + filter.id + ']').replaceWith(filterDOM);
			}
		},


		/**
		 * Converts a Search instance to an ElasticSearch DSL query that can be passed to the search endpoint.
		 */
		getQuery: function Search$getQuery() {
			self.queryText = $('[name="search"]').val();

			self.searchDSL = {
				query: {
					filtered: {
						filter: {
							and: [
								{
									bool: {
										should: []
									}
								}
							]
						}
					}
				},
				//This is the pagination size, and can be changed to whatever we want.
				size: '50'
			};

			//Only add the query text portions if there is query text to be searched on.
			if (self.queryText.length > 0) {
				self.searchDSL.query.filtered.query = {
					multi_match: {
						query: self.queryText,
							type: 'most_fields',
							fields: MAPPED_SEARCH_TEXT_FIELDS
					}
				};
			}

			// This essentially "serializes" the Search instance's "form."
			_.forEach(this.filters, function(filterType) {
				_.forEach(filterType.list, function(filter) {
					filter.addToDSL(self.searchDSL);
				});
			});

			return self.searchDSL;
		},

		/**
		 * This highlights a given map element and un-highlights all the others.
		 *
		 * @param mapId The ID of the map element to be highlighted.
		 * @constructor
		 */
		highlightCurrentGeofilter: function Search$hydrateCurrentGeofilter(mapId) {
			_.forEach(mainMap.controls.draw.options.edit.featureGroup._layers, function(layer) {
				//If this map element is the one to be highlighted:
				if (layer._leaflet_id === mapId) {
					//If it's a marker, replace its icon with the highlighted image
					if (layer.hasOwnProperty('_icon')) {
						layer._icon.src = window.staticUrl + 'assets/img/marker-red.png';
					}
					//If it's a polygon, set its fill color to the highlighted color
					else {
						layer.setStyle({
							fillColor: '#62e910'
						});
					}
				}
				//If this map element is not the one to be highlighted:
				else {
					//If it's a marker, set its icon to the default, un-highlighted image
					if (layer.hasOwnProperty('_icon')) {
						layer._icon.src = 'https://api.tiles.mapbox.com/mapbox.js/v2.2.1/images/marker-icon.png';
					}
					//If it's a polygon, set its fill color to the default, un-highlighted color
					else {
						layer.setStyle({
							fillColor: '#0033ff'
						});
					}
				}
			});
		},

		/**
		 * This converts an existing DSL query back into individual filters.  It pushes those filters
		 * onto the internal list, creates their DOM representations, and adds the map polygons and/or markers
		 * for Where filters.
		 *
		 * @param dsl The existing DSL query from which new filters will be constructed
		 * @constructor
		 */
		hydrateFilters: function Search$hydrateFilters(dsl) {
			var radiusString, re;
			this.searchDSL = dsl;
			var self = this;
			var filterList;

			//Pull off the text query and filters, but only if they exist on the DSL query
			if (_.has(this.searchDSL.query, 'filtered')) {
				//The text query can be inserted directly into the search box.
				if (_.has(this.searchDSL.query.filtered, 'query')) {
					$('[name="search"]').val(this.searchDSL.query.filtered.query.multi_match.query);
				}

				//Pull off the list of filters
				if (_.has(this.searchDSL.query.filtered, 'filter')) {
					filterList = this.searchDSL.query.filtered.filter.and[0].bool.should;
				}
			}

			//Create a new filter for each one in the list
			_.forEach(filterList, function(thisFilter) {
				var context = {};
				var newFilter;

				//Filters that start with 'and', which are Who filters
				if (_.has(thisFilter, 'and')) {
					//If the Who filter has an 'or' term, then it contains a name/handle to filter on
					if (_.has(thisFilter.and[0], 'or')) {
						context.name = thisFilter.and[0].or[0].term['contacts_list.name'];

						//If there is more than one term in the 'and', then the Who filter contains both a name
						//to filter on and a Contact Interaction Type
						if (thisFilter.and.length > 1) {
							context.contactInteractionType = thisFilter.and[1].term.contact_interaction_type[0].toUpperCase() + thisFilter.and[1].term.contact_interaction_type.slice(1);
						}
					}
					//If the Who filter does not have an 'or' term, then it just has a Contact Interaction Type
					else {
						context.contactInteractionType = thisFilter.and[0].term.contact_interaction_type[0].toUpperCase() + thisFilter.and[0].term.contact_interaction_type.slice(1);
					}

					//Create the new filter and add it
					newFilter = new WhoFilter(self.filters.who.nextId, context);
					self.addFilter(newFilter);
				}
				//Filters that start with 'term'
				else if (_.has(thisFilter, 'term')) {
					//Filters that have 'content_list.content_type' are What filters
					if (_.has(thisFilter.term, 'content_list.content_type')) {
						context.contentType = thisFilter.term['content_list.content_type'][0].toUpperCase() + thisFilter.term['content_list.content_type'].slice(1);

						//Create the new filter and add it
						newFilter = new WhatFilter(self.filters.what.nextId, context);
						self.addFilter(newFilter);
					}
					//Filters that have 'provider_name' are How filters
					else if (_.has(thisFilter.term, 'provider_name')) {
						context.providerName = thisFilter.term.provider_name;

						//Create the new filter and add it
						newFilter = new HowFilter(self.filters.how.nextId, context);
						self.addFilter(newFilter);
					}
				}
				//Filters that start with term 'not'
				else if (_.has(thisFilter, 'not')) {
					//Filters that have 'geo_polygon' are area Where filters; inside a 'not', they are for outside the polygon
					if (_.has(thisFilter.not, 'geo_polygon')) {
						context.coordinates = thisFilter.not.geo_polygon['location.geolocation'].points;
						context.whereType = 'area';
						context.modifier = 'Outside';

						//Create the new filter and add it
						newFilter = new WhereFilter(self.filters.where.nextId, context);
						self.addFilter(newFilter);
					}
					//Filters that have 'geo_distance' are radius Where filters; inside a 'not', they are for outside the radius
					else if (_.has(thisFilter.not, 'geo_distance')) {
						radiusString = thisFilter.not.geo_distance.distance;
						re = /[0-9.]+/;

						context.modifier = 'Outside';
						context.radius = radiusString.match(re)[0];
						context.unit = radiusString.replace(re, '');
						context.unit = context.unit[0].toUpperCase() + context.unit.slice(1);
						context.coordinates = thisFilter.not.geo_distance['location.geolocation'];
						context.whereType = 'radius';

						//Create the new filter and add it
						newFilter = new WhereFilter(self.filters.where.nextId, context);
						self.addFilter(newFilter);
					}
				}
				//Filters that have 'geo_polygon' are area Where filters; without a 'not', they are for inside the polygon
				else if (_.has(thisFilter, 'geo_polygon')) {
					context.coordinates = thisFilter.geo_polygon['location.geolocation'].points;
					context.whereType = 'area';
					context.modifier = 'Inside';

					//Create the new filter and add it
					newFilter = new WhereFilter(self.filters.where.nextId, context);
					self.addFilter(newFilter);
				}
				//Filters that have 'geo_distance' are radius Where filters; without a 'not', they are for within that radius
				else if (_.has(thisFilter, 'geo_distance')) {
					radiusString = thisFilter.geo_distance.distance;

					//ElasticSearch does geo_distance based on a mashup of the radius and units, e.g. '24.1kilometers'
					//This matches the radius portion
					re = /[0-9.]+/;

					context.modifier = 'Within';
					context.radius = radiusString.match(re)[0];

					//Strip out the radius to get the units
					context.unit = radiusString.replace(re, '');
					context.unit = context.unit[0].toUpperCase() + context.unit.slice(1);
					context.coordinates = thisFilter.geo_distance['location.geolocation'];
					context.whereType = 'radius';

					//Create the new filter and add it
					newFilter = new WhereFilter(self.filters.where.nextId, context);
					self.addFilter(newFilter);
				}
				//Filters that start with 'range' are When filters
				else if (_.has(thisFilter, 'range')) {
					//If there is a start datetime, save it
					if (_.has(thisFilter, 'range.datetime.gte')) {
						context.startDate = thisFilter.range.datetime.gte;
					}

					//If there is an end datetime, save it
					if (_.has(thisFilter, 'range.datetime.lte')) {
						context.endDate = thisFilter.range.datetime.lte;
					}

					//Create the new filter and add it
					newFilter = new WhenFilter(self.filters.when.nextId, context);
					self.addFilter(newFilter);
				}

				//Update the DOM representation of the new filter with the filter's values
				self.DOM.updateFilter(newFilter);
			});
		},

		/**
		 * Initializes the Search object
		 *
		 * @param dsl The query DSL that was saved in the URL
		 * @param searchElementSelector The top-level DOM element that contains all of the Search and filter controls
		 * @param map The Cartano Map element
		 * @returns {*} A promise that is resolved when the user's signals have been successfully retrieved
		 * @constructor
		 */
		init: function Search$init(dsl, searchElementSelector, map) {
			var self = this;

			mainMap = map;

			//Create event delgation for a geofilter event, which Cartano will fire when one or more polygons or markers
			//are created, updated, or deleted.
			$(document).bind('geofilter', function(e) {
				//There might be more than one filter in a geofilter event
				_.forEach(e.filters, function(filter) {
					var mapId = filter.id;
					var context = {};

					//If the event was not a deletion:
					if (e.action !== 'delete') {
						context.mapId = mapId;
						context.coordinates = filter.coordinates[0];

						//Set the Where type
						if (filter.type === 'marker') {
							context.whereType = 'radius';
						}
						else if (filter.type === 'polygon') {
							context.whereType = 'area';
						}

						//If this filter was created, highlight it and populate the Filter Content area
						//with its information
						if (e.action === 'create') {
							self.highlightCurrentGeofilter(mapId);
							self.DOM.renderFilterContent('where', self.filters.where.nextId, context);
						}
						//If this filter was updated, try to get the filter from the internal store
						//and update it if it has been previously created
						else if (e.action === 'update') {
							var updateFilter = _.find(self.filters.where.list, function(filter) {
								return filter.mapId === mapId;
							});

							if (updateFilter !== undefined) {
								updateFilter.updateCoordinates();
							}
						}
					}
					//If the event was a deletion, try to get the filter from the internal store
					//and remove it if it has been previously created.
					//Also empty the Filter Content area.
					else {
						var deleteFilter = _.find(self.filters.where.list, function(filter) {
							return filter.mapId === mapId;
						});

						if (deleteFilter !== undefined) {
							self.removeFilter(deleteFilter.id, 'where');
						}

						self.DOM.removeFilterContent();
					}
				});
			});

			//How filters need the Providers of the user's signals, so retrieve the Signals
			//and return the ajax request so that its promise can be used to determine when this has been finished.
			return $.ajax({
				url: '/opi/signal',
				type: 'GET',
				dataType: 'json',
				headers: {
					'X-CSRFToken': $.cookie('csrftoken')
				}
			}).done(function(data, xhr, response) {
				self.signals = data;

				//Currently, How filters only run on the Provider level, so get the Provider for each Signal
				_.forEach(self.signals, function(signal) {
					$.ajax({
						url: '/opi/provider/' + signal.provider,
						type: 'GET',
						dataType: 'json',
						headers: {
							'X-CSRFToken': $.cookie('csrftoken')
						}
					}).done(function(data, xhr, response) {
						signal.provider = data;
					});
				});

				//Save a reference to the Search/filter container
				self.element = $(searchElementSelector);

				//Bind needed event listeners
				self._bind();

				//If there was a DSL query saved in the URL hash, create filters for each one that was present
				if (dsl.length > 0) {
					//window.location.hash keeps the '#' from the hash, so strip it off
					dsl = deparam(decodeURIComponent(dsl).slice(1));
					self.hydrateFilters(dsl);
				}
			});
		},

		/**
		 * Remove a filter
		 *
		 * @param filterId The ID of the filter being removed
		 * @param type The type of filter being removed
		 * @constructor
		 */
		removeFilter: function Search$removeFilter(filterId, type) {
			//Return the filter that has the specified ID
			var matchFilter = function(filter) {
				return filter.id === filterId;
			};

			var removeFilter = _.find(this.filters[type].list, matchFilter);
			var mapId = removeFilter.mapId;

			//Remove the filter from the internal store
			_.remove(this.filters[type].list, matchFilter);

			//Remove a Where filter's map object (if not a map object, nothing happens)
			this.DOM.removeGeofilter(mapId);

			//Remove the DOM representation of the filter
			this.DOM.removeFilter(filterId, type);
		}
	};

	//Create a reference to the Search object
	instance = new Search();


	return {
		element: instance.element,
		filters: instance.filters,
		signals: instance.signals,

		addFilter: instance.addFilter,
		_bind: instance._bind,
		DOM: instance.DOM,
		getQuery: instance.getQuery,
		highlightCurrentGeofilter: instance.highlightCurrentGeofilter,
		hydrateFilters: instance.hydrateFilters,
		init: instance.init,
		removeFilter: instance.removeFilter,
		stringifyDate: stringifyDate
	};
});
