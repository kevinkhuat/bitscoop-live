define(['embed-content', 'icons', 'moment'], function(embedContent, icons, moment) {
	var isMobile, objectContextDict;

	isMobile = (window.devicePixelRatio >= 1.5 && window.innerWidth <= 1080);

	//objectContextDict contains the mappings for generating the context for every object type for every view state,
	//as well as for rendering that object type's details panel.
	//For example, to get the render context for an event in list view, you'd call objectContext.event.LisItem(event),
	//and it would return the context object.
	//The context includes the sortable fields in the order they are displayed in.
	//The list and map contexts include an array for the columns of data to be rendered; the order of the columns is
	//the order they will be rendered on the screen.
	objectContextDict = {
			contacts: {
				grid: function objectContext$contact$gridItem(contact) {
					var gridItem, title;

					if (contact.name) {
						title = contact.name;
					}
					else if (contact.handle) {
						title = contact.handle;
					}

					gridItem = {
						objectType: 'contacts',
						object: contact,
						title: title,
						largeIcon: icons.getContactFontIcon(),
						rightIcon: icons.getProviderFontIcon(contact.events[0].provider_name.toLowerCase()),
						sortFields: objectContextDict.contacts.sort.fields
					};

					return gridItem;
				},
				list: function objectContext$contact$listItem(contact) {
					return {
						objectType: 'contacts',
						columns: [
							{
								type: 'text',
								property: 'name',
								displayMobile: true
							},
							{
								type: 'icon',
								icon: 'providerIcon',
								property: 'provider_name',
								displayMobile: true
							},
							{
								type: 'text',
								property: 'handle',
								displayMobile: true
							}
						],
						object: contact,
						isMobile: isMobile,
						sortFields: objectContextDict.contacts.sort.fields
					};
				},
				map: function objectContext$contact$mapItem(contact) {
					return {
						objectType: 'contacts',
						columns: [
							{
								type: 'text',
								property: 'name'
							},
							{
								type: 'icon',
								icon: 'providerIcon',
								property: 'provider_name'
							},
							{
								type: 'text',
								property: 'handle'
							}
						],
						object: contact,
						sortFields: objectContextDict.contacts.sort.fields
					};
				},
				details: function objectContext$contact$details(contact, isEventDetail) {
					return {
						contact:contact,
						sortFields: objectContextDict.contacts.sort.fields,
						isEventDetail: isEventDetail
					};
				},
				sort: {
					initial: 'handle:asc',
					fields: [
						{
							name: 'Name',
							property: 'name',
							attr: 'name'
						},
						{
							name: 'Provider',
							property: 'provider_name',
							attr: 'provider-name'
						},
						{
							name: 'Handle',
							property: 'handle',
							attr: 'handle'
						}
					]
				}
			},
			content: {
				grid: function objectContext$content$gridItem(content) {
					var gridItem, title, thumbnail;

					if (content.embed_thumbnail) {
						thumbnail = content.embed_thumbnail;
					}

					if (content.title) {
						title = content.title;
					}
					else if (content.text) {
						title = content.text;
					}

					gridItem = {
						objectType: 'content',
						object: content,
						leaflet_id: 0, //TODO: Fix
						thumbnail: thumbnail, //TODO: Fix
						title: title,
						rightIcon: icons.getProviderFontIcon(content.events[0].provider_name.toLowerCase()),
						sortFields: objectContextDict.content.sort.fields
					};

					if (thumbnail) {
						gridItem.leftIcon = icons.getContentFontIcon(content);
					}
					else {
						gridItem.largeIcon = icons.getContentFontIcon(content);
					}

					return gridItem;
				},
				list: function objectContext$content$listItem(content) {
					content.icon = icons.getContentFontIcon(content);

					return {
						objectType: 'content',
						columns: [
							{
								type: 'text',
								property: 'title',
								displayMobile: true
							},
							{
								type: 'icon',
								icon: 'providerIcon',
								property: 'provider_name',
								displayMobile: true
							},
							{
								type: 'icon',
								icon: 'icon',
								property: 'type',
								displayMobile: true
							},
							{
								type: 'text',
								property: 'mimetype',
								displayMobile: true
							}
						],
						object: content,
						isMobile: isMobile,
						sortFields: objectContextDict.content.sort.fields
					};
				},
				map: function objectContext$content$mapItem(content) {
					content.icon = icons.getContentFontIcon(content);
					content.formattedCreated = moment(content.created).format('M/D/YY h:mm A');

					return {
						objectType: 'content',
						columns: [
							{
								type: 'text',
								property: 'title'
							},
							{
								type: 'icon',
								icon: 'providerIcon',
								property: 'provider_name'
							},
							{
								type: 'icon',
								icon: 'icon',
								property: 'type'
							},
							{
								type: 'text',
								property: 'mimetype'
							}
						],
						object: content,
						sortFields: objectContextDict.content.sort.fields
					};
				},
				details: function objectContext$content$details(content, isEventDetail) {
					content.contentTypeIcon = icons.getContentFontIcon(content);

					if (content.embed_format) {
						content.formatted_embed_content = embedContent(content);
					}

					return {
						content: content,
						sortFields: objectContextDict.content.sort.fields,
						isEventDetail: isEventDetail
					};
				},
				sort: {
					initial: 'title:asc',
					fields: [
						{
							name: 'Title',
							property: 'title',
							attr: 'title'
						},
						{
							name: 'Provider',
							property: 'provider_name',
							attr: 'provider-name'
						},
						{
							name: 'Type',
							property: 'type',
							attr: 'type'
						},
						{
							name: 'Format',
							property: 'mimetype',
							attr: 'mimetype'
						}
					]
				}
			},
			events: {
				grid: function objectContext$event$gridItem(event) {
					var datetime, datetimeEstimated, gridItem, title, thumbnail;

					//TODO: Can we do this better?
					if (event.content.length > 0) {
						if (event.content[0].embed_thumbnail) {
							thumbnail = event.content[0].embed_thumbnail;
						}

						if (event.content[0].title) {
							title = event.content[0].title;
						}

						event.firstItemType = event.content[0].type;
					}
					else if (event.things.length) {
						if (event.things[0].embed_thumbnail) {
							thumbnail = event.things[0].embed_thumbnail;
						}

						if (event.things[0].title) {
							title = event.things[0].title;
						}

						event.firstItemType = event.things[0].type;
					}

					if (event.contacts.length > 0) {
						event.firstContactHandle = event.contacts[0].handle;
					}

					if (event.datetime) {
						event.sortDatetime = event.datetime;
						event.datetimeEstimated = false;
					}
					else {
						event.sortDatetime = event.created;
						event.datetimeEstimated = true;
					}

					if (_.has(event, 'places') && event.places.length > 0) {
						event.firstPlaceName = event.places[0].name;
					}

					gridItem = {
						objectType: 'events',
						object: event,
						thumbnail: thumbnail,
						date: moment(event.sortDatetime).format('M/D/YY'),
						time: moment(event.sortDatetime).format('h:mm A'),
						sortDatetime: event.sortDatetime,
						datetimeEstimated: event.datetimeEstimated,
						firstContactHandle: event.firstContactHandle,
						firstItemType: event.firstItemType,
						firstPlaceName: event.firsPlaceName,
						title: title,
						rightIcon: icons.getProviderFontIcon(event.provider_name.toLowerCase()),
						sortFields: objectContextDict.events.sort.fields
					};

					if (thumbnail) {
						gridItem.leftIcon = icons.getEventFontIcon(event);
					}
					else {
						gridItem.largeIcon = icons.getEventFontIcon(event);
					}

					return gridItem;
				},
				list: function objectContext$event$listItem(event) {
					var firstContent, firstThing;

					if (event.contacts.length > 0) {
						event.firstContactHandle = event.contacts[0].handle;
					}

					if (event.content.length > 0) {
						firstContent = event.content[0];

						event.title = firstContent.title;
						event.firstItemType = firstContent.type;
						event.itemIcon = icons.getContentFontIcon(firstContent);
					}
					else if (event.things.length > 0) {
						firstThing = event.things[0];

						event.title = firstThing.title;
						event.firstItemType = firstThing.type;
						event.itemIcon = icons.getThingFontIcon(firstThing);
					}

					if (_.has(event, 'places') && event.places.length > 0) {
						event.firstPlaceName = event.places[0].name;
					}

					if (event.datetime) {
						event.sortDatetime = event.datetime;
						event.datetimeEstimated = false;
					}
					else {
						event.sortDatetime = event.created;
						event.datetimeEstimated = true;
					}

					event.eventTypeIcon = icons.getEventFontIcon(event);
					event.formattedDatetime = moment(event.sortDatetime).format('M/D/YY h:mm A');
					event.providerIcon = icons.getProviderFontIcon(event.provider_name.toLowerCase());

					return {
						objectType: 'events',
						columns: [
							{
								type: 'text',
								property: 'title',
								displayMobile: true
							},
							{
								type: 'icon',
								icon: 'providerIcon',
								property: 'provider_name',
								displayMobile: true
							},
							{
								type: 'icon',
								icon: 'eventTypeIcon',
								property: 'type',
								displayMobile: true
							},
							{
								type: 'icon',
								icon: 'itemIcon',
								property: 'firstItemType',
								displayMobile: true
							},
							{
								type: 'text',
								property: 'firstContactHandle',
								displayMobile: false
							},
							{
								type: 'text',
								property: 'formattedDatetime',
								displayMobile: true
							},
							{
								type: 'text',
								property: 'firstPlaceName',
								displayMobile: false
							}
						],
						object: event,
						isMobile: isMobile,
						sortFields: objectContextDict.events.sort.fields
					};
				},
				map: function objectContext$event$mapItem(event) {
					var firstContent;

					if (event.contacts.length > 0) {
						event.firstContactHandle = event.contacts[0].handle;
					}

					if (event.content.length > 0) {
						firstContent = event.content[0];

						event.title = firstContent.title;
						event.firstItemType = firstContent.type;
						event.itemIcon = icons.getContentFontIcon(firstContent);
					}
					else if (event.things.length > 0) {
						firstThing = event.things[0];

						event.title = firstThing.title;
						event.firstItemType = firstThing.type;
						event.itemIcon = icons.getThingFontIcon(firstThing);
					}

					if (_.has(event, 'places') && event.places.length > 0) {
						event.firstPlaceName = event.places[0].name;
					}

					if (event.datetime) {
						event.sortDatetime = event.datetime;
						event.datetimeEstimated = false;
					}
					else {
						event.sortDatetime = event.created;
						event.datetimeEstimated = true;
					}

					event.eventTypeIcon = icons.getEventFontIcon(event);
					event.formattedDatetime = moment(event.sortDatetime).format('M/D/YY h:mm A');
					event.providerIcon = icons.getProviderFontIcon(event.provider_name.toLowerCase());

					return {
						objectType: 'events',
						columns: [
							{
								type: 'icon',
								icon: 'providerIcon'
							},
							{
								type: 'icon',
								icon: 'eventTypeIcon'
							},
							{
								type: 'icon',
								icon: 'itemIcon'
							},
							{
								type: 'text',
								property: 'formattedDatetime'
							}
						],
						object: event,
						sortFields: objectContextDict.events.sort.fields
					};
				},
				details: function objectContext$event$details(event) {
					event.eventTypeIcon = icons.getEventFontIcon(event);
					event.date = moment(event.sortDatetime).format('M/D/YY');
					event.time = moment(event.sortDatetime).format('h:mm A');
					event.providerIcon = icons.getProviderFontIcon(event.provider_name.toLowerCase());

					return {
						event: event,
						sortFields: objectContextDict.events.sort.fields
					};
				},
				sort: {
					initial: 'datetime:desc',
					fields: [
						{
							name: 'Title',
							property: 'title',
							attr: 'title'
						},
						{
							name: 'Provider',
							property: 'provider_name',
							attr: 'provider-name'
						},
						{
							name: 'Type',
							property: 'type',
							attr: 'type'
						},
						{
							name: 'Item Type',
							property: 'firstItemType',
							attr: 'item-type'
						},
						{
							name: 'Contact',
							property: 'firstContactHandle',
							attr: 'contact'
						},
						{
							name: 'Time',
							property: 'sortDatetime',
							attr: 'datetime'
						},
						{
							name: 'Place',
							property: 'firstPlaceName',
							attr: 'place'
						}
					]
				}
			},
			locations: {
				grid: function objectContext$location$gridItem(location) {
					var gridItem;

					gridItem = {
						objectType: 'locations',
						object: location,
						leaflet_id: 0, //TODO: Fix
						largeIcon: icons.getLocationFontIcon(),
						sortFields: objectContextDict.locations.sort.fields
					};

					return gridItem;
				},
				list: function objectContext$location$listItem(location) {
					return {
						objectType: 'locations',
						columns: [
							{
								type: 'text',
								property: 'geolocation',
								displayMobile: true
							}
						],
						object: location,
						isMobile: isMobile,
						sortFields: objectContextDict.locations.sort.fields
					};
				},
				map: function objectContext$location$mapItem(location) {
					location.formattedDatetime = moment(location.datetime ? location.datetime : location.event[0].datetime).format('M/D/YY h:mm A');

					return {
						objectType: 'locations',
						columns: [
							{
								type: 'text',
								property: 'formattedDatetime'
							}
						],
						object: location,
						sortFields: objectContextDict.locations.sort.fields
					};
				},
				details: function objectContext$location$details(location, isEventDetail) {
					location.date = moment(location.datetime).format('M/D/YY');
					location.time = moment(location.datetime).format('h:mm A');

					return {
						location: location,
						sortFields: objectContextDict.locations.sort.fields,
						isEventDetail: isEventDetail
					};
				},
				sort: {
					fields: []
				}
			},
			organizations: {
				grid: function objectContext$organization$gridItem(organization) {
					var gridItem, title, thumbnail;

					if (organization.name) {
						title = organization.name;
					}

					if (organization.embed_thumbnail) {
						thumbnail = organization.thumbnail;
					}

					gridItem = {
						objectType: 'organizations',
						object: organization,
						leaflet_id: 0, //TODO: Fix
						thumbnail: thumbnail,
						title: title,
						sortFields: objectContextDict.organizations.sort.fields
					};

					if (!thumbnail) {
						gridItem.largeIcon = icons.getOrganizationFontIcon();
					}

					return gridItem;
				},
				list: function objectContext$organization$listItem(organization) {
					organization.icon = icons.getOrganizationFontIcon(organization);

					return {
						objectType: 'organizations',
						columns: [
							{
								type: 'text',
								property: 'name',
								displayMobile: true
							},
							{
								type: 'icon',
								icon: 'icon',
								property: 'type',
								displayMobile: true
							}
						],
						object: organization,
						isMobile: isMobile,
						sortFields: objectContextDict.organizations.sort.fields
					};
				},
				map: function objectContext$organization$mapItem(organization) {
					organization.icon = icons.getOrganizationFontIcon(organization);

					return {
						objectType: 'organizations',
						columns: [
							{
								type: 'text',
								property: 'name'
							},
							{
								type: 'icon',
								icon: 'icon',
								property: 'type'
							}
						],
						object: organization,
						sortFields: objectContextDict.organizations.sort.fields
					};
				},
				details: function objectContext$organization$details(organization, isEventDetail) {
					//TODO: Fix Type Icons
					organization.organizationTypeIcon = icons.getOrganizationFontIcon();

					return {
						organization: organization,
						sortFields: objectContextDict.organizations.sort.fields,
						isEventDetail: isEventDetail
					};
				},
				sort: {
					initial: 'name:asc',
					fields: [
						{
							name: 'Name',
							property: 'name',
							attr: 'name'
						},
						{
							name: 'Type',
							property: 'type',
							attr: 'type'
						}
					]
				}
			},
			people: {
				grid: function objectContext$person$gridItem(person) {
					var gridItem, thumbnail, title;

					if (person.first_name) {
						title = person.first_name + ' ' + person.last_name;
					}

					if (person.embed_thumbnail) {
						thumbnail = person.embed_thumbnail;
					}

					gridItem = {
						objectType: 'people',
						object: person,
						thumbnail: thumbnail,
						title: title,
						largeIcon: icons.getPersonFontIcon(),
						sortFields: objectContextDict.people.sort.fields
					};

					return gridItem;
				},
				list: function objectContext$person$listItem(person) {
					return {
						objectType: 'people',
						columns: [
							{
								type: 'text',
								property: 'first_name',
								displayMobile: true
							},
							{
								type: 'text',
								property: 'last_name',
								displayMobile: true
							},
							{
								type: 'text',
								property: 'age',
								displayMobile: true
							},
							{
								type: 'text',
								property: 'gender',
								displayMobile: true
							}
						],
						object: person,
						isMobile: isMobile,
						sortFields: objectContextDict.people.sort.fields
					};
				},
				map: function objectContext$person$mapItem(person) {
					return {
						objectType: 'people',
						columns: [
							{
								type: 'text',
								property: 'first_name'
							},
							{
								type: 'text',
								property: 'last_name'
							},
							{
								type: 'text',
								property: 'age'
							},
							{
								type: 'text',
								property: 'gender'
							}
						],
						object: person,
						sortFields: objectContextDict.people.sort.fields
					};
				},
				details: function objectContext$person$details(person, isEventDetail) {
					return {
						person: person,
						sortFields:  objectContextDict.people.sort.fields,
						isEventDetail: isEventDetail
					};
				},
				sort: {
					initial: 'last_name:asc',
					fields:[
						{
							name: 'First Name',
							property: 'first_name',
							attr: 'first-name'
						},
						{
							name: 'Last Name',
							property: 'last_name',
							attr: 'last-name'
						},
						{
							name: 'Age',
							property: 'age',
							attr: 'age'
						},
						{
							name: 'Gender',
							property: 'gender',
							attr: 'gender'
						}
					]
				}
			},
			places: {
				grid: function objectContext$place$gridItem(place) {
					var gridItem, title, thumbnail;

					if (place.embed_thumbnail) {
						thumbnail = place.embed_thumbnail;
					}

					if (place.reverse_geolocation) {
						title = place.reverse_geolocation;
					}

					gridItem = {
						objectType: 'places',
						object: place,
						leaflet_id: 0, //TODO: Fix
						thumbnail: thumbnail,
						title: title,
						sortFields: objectContextDict.places.sort.fields
					};

					if (!thumbnail) {
						gridItem.largeIcon = icons.getPlaceFontIcon();
					}

					return gridItem;
				},
				list: function objectContext$place$listItem(place) {
					return {
						objectType: 'places',
						columns: [
							{
								type: 'text',
								property: 'name',
								displayMobile: true
							},
							{
								type: 'text',
								property: 'reverse_geolocation',
								displayMobile: true
							},
							{
								type: 'text',
								property: 'type',
								displayMobile: true
							}
						],
						object: place,
						isMobile: isMobile,
						sortFields: objectContextDict.places.sort.fields
					};
				},
				map: function objectContext$place$mapItem(place) {
					return {
						objectType: 'places',
						columns: [
							{
								type: 'text',
								property: 'name'
							},
							{
								type: 'text',
								property: 'type'
							}
						],
						object: place,
						sortFields: objectContextDict.places.sort.fields
					};
				},
				details: function objectContext$place$details(place, isEventDetail) {
					return {
						place: place,
						sortFields: objectContextDict.places.sort.fields,
						isEventDetail: isEventDetail
					};
				},
				sort: {
					initial: 'name:asc',
					fields: [
						{
							name: 'Name',
							property: 'name',
							attr: 'name'
						},
						{
							name: 'Location',
							property: 'reverse_geolocation',
							attr: 'reverse-geolocation'
						},
						{
							name: 'Type',
							property: 'type',
							attr: 'type'
						}
					]
				}
			},
			things: {
				grid: function objectContext$thing$gridItem(thing) {
					var gridItem, title, thumbnail;

					if (thing.embed_thumbnail) {
						thumbnail = thing.embed_thumbnail;
					}

					if (thing.title) {
						title = thing.title;
					}

					gridItem = {
						objectType: 'things',
						object: thing,
						leaflet_id: 0, //TODO: Fix
						thumbnail: thumbnail,
						title: title,
						rightIcon: icons.getProviderFontIcon(thing.events[0].provider_name.toLowerCase()),
						sortFields: objectContextDict.things.sort.fields
					};

					if (thumbnail) {
						gridItem.leftIcon = icons.getThingFontIcon(thing);
					}
					else {
						gridItem.largeIcon = icons.getThingFontIcon(thing);
					}

					return gridItem;
				},
				list: function objectContext$thing$listItem(thing) {
					thing.icon = icons.getThingFontIcon(thing);
					thing.prettyType = thing.type.replace(/_/g, ' ');

					return {
						objectType: 'things',
						columns: [
							{
								type: 'text',
								property: 'title',
								displayMobile: true
							},
							{
								type: 'icon',
								icon: 'providerIcon',
								property: 'provider_name',
								displayMobile: true
							},
							{
								type: 'icon',
								icon: 'icon',
								property: 'prettyType',
								displayMobile: true
							}
						],
						object: thing,
						isMobile: isMobile,
						sortFields: objectContextDict.things.sort.fields
					};
				},
				map: function objectContext$thing$mapItem(thing) {
					thing.icon = icons.getThingFontIcon(thing);

					return {
						objectType: 'things',
						columns: [
							{
								type: 'text',
								property: 'title'
							},
							{
								type: 'icon',
								icon: 'providerIcon',
								property: 'provider_name'
							},
							{
								type: 'icon',
								icon: 'icon',
								property: 'type'
							}
						],
						object: thing,
						sortFields: objectContextDict.things.sort.fields
					};
				},
				details: function objectContext$thing$details(thing, isEventDetail) {
					thing.thingTypeIcon = icons.getThingFontIcon(thing);
					thing.prettyType = thing.type.replace(/_/g, ' ');

					if (thing.embed_format) {
						thing.formatted_embed_content = embedContent(thing);
					}

					return {
						thing: thing,
						sortFields: objectContextDict.things.sort.fields,
						isEventDetail: isEventDetail
					};
				},
				sort: {
					initial: 'title:asc',
					fields: [
						{
							name: 'Title',
							property: 'title',
							attr: 'title'
						},
						{
							name: 'Provider',
							property: 'provider_name',
							attr: 'provider-name'
						},
						{
							name: 'Type',
							property: 'type',
							attr: 'type'
						}
					]
				}
			}
		};

	return objectContextDict;
});
