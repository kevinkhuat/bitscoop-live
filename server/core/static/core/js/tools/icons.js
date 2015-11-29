define([], function() {
	/**
	 * Gets icon classes for mapped events and schema objects
	 *
	 * @param {String} library Icon library
	 * @param {String} name Object name with an optional namespace
	 * @returns {String} Icon classname
	 */
	var IconTranslation = {
		fontAwesome: {
			contact: 'fa fa-user',

			'content.achievement': 'fa fa-trophy',
			'content.audio': 'fa fa-headphones',
			'content.code': 'fa fa-code',
			'content.file': 'fa fa-file-o',
			'content.game': 'fa fa-gamepad',
			'content.image': 'fa fa-picture-o',
			'content.receipt': 'fa fa-dollar',
			'content.software': 'fa fa-floppy-o',
			'content.text': 'fa fa-file-text-o',
			'content.video': 'fa fa-video-camera',

			'event.called': 'fa fa-phone',
			'event.commented': 'fa fa-comment',
			'event.created': 'fa fa-pencil-square-o',
			'event.ate': 'fa fa-cutlery',
			'event.edited': 'fa fa-pencil-square-o',
			'event.exercised': 'fa fa-heartbeat',
			'event.messaged': 'fa fa-comment',
			'event.played': 'fa fa-play',
			'event.purchased': 'fa fa-credit-card',
			'event.slept': 'fa fa-bed',
			'event.traveled': 'fa fa-plane',
			'event.viewed': 'fa fa-eye',
			'event.visited': 'fa fa-crosshairs',

			location: 'fa fa-map-marker',
			organization: 'fa fa-building-o',
			person: 'fa fa-user',
			place: 'fa fa-map-pin',

			'thing.apparel_&_accessories': 'fa fa-cube',
			'thing.appliances': 'fa fa-cube',
			'thing.automotive': 'fa fa-car',
			'thing.baby': 'fa fa-cube',
			'thing.books_&_magazines': 'fa fa-book',
			'thing.electronics': 'fa fa-bolt',
			'thing.food': 'fa fa-cutlery',
			'thing.gifts': 'fa fa-gift',
			'thing.health_&_beauty': 'fa fa-plus-circle',
			'thing.home_&_kitchen': 'fa fa-home',
			'thing.movies_&_tv': 'fa fa-television',
			'thing.music': 'fa fa-music',
			'thing.office': 'fa fa-briefcase',
			'thing.pet': 'fa fa-paw',
			'thing.products': 'fa fa-shopping-bag',
			'thing.shoes': 'fa fa-cube',
			'thing.sports_&_outdoors': 'fa fa-futbol-o',
			'thing.tools_&_home_improvement': 'fa fa-gamepad',
			'thing.toys_&_games': 'fa fa-gamepad',
			'thing.other': 'fa fa-pencil-square-o',

			'provider.dropbox': 'fa fa-dropbox',
			'provider.fitbit': 'fa fa-fitbit',
			'provider.github': 'fa fa-github',
			'provider.google': 'fa fa-google',
			'provider.instagram': 'fa fa-instagram',
			'provider.reddit': 'fa fa-reddit-alien',
			'provider.slice': 'fa fa-slice',
			'provider.spotify': 'fa fa-spotify',
			'provider.steam': 'fa fa-steam',
			'provider.twitter': 'fa fa-twitter'
		}
	};

	function getIcon(library, name) {
		return IconTranslation[library][name];
	}

	/**
	 * Tries to get the icon that should represent the first content item associated with an event.
	 * If there are no matches, or there are no pieces of content, return the default icon, which is a map icon.
	 *
	 * @param {Array} content A list of content items
	 * @returns {String} An icon class name
	 */
	getIcon.getContentFontIcon = function(content) {
		var content_type;

		if (content == null) {
			return 'fa fa-map-marker';
		}

		// TODO: Make this a little more robust, how do we determine the content type if there is more than one.
		content_type = content.type;

		return getIcon('fontAwesome', 'content.' + [content_type]) || 'fa fa-map-marker';
	};

	/**
	 * Tries to get the icon that should represent an event.
	 * If there are no matches, return the default icon, which is an exclamation mark.
	 *
	 * @param {Object} event An event
	 * @return {String} An icon name
	 */
	getIcon.getEventFontIcon = function(event) {
		var event_type;

		event_type = event.type;

		return getIcon('fontAwesome', 'event.' + [event_type]) || 'fa fa-exclamation';
	};

	getIcon.getContactFontIcon = function() {
		return getIcon('fontAwesome', 'contact');
	};

	getIcon.getLocationFontIcon = function() {
		return getIcon('fontAwesome', 'location');
	};

	getIcon.getOrganizationFontIcon = function() {
		return getIcon('fontAwesome', 'organization');
	};

	getIcon.getPersonFontIcon = function() {
		return getIcon('fontAwesome', 'person');
	};

	getIcon.getPlaceFontIcon = function() {
		return getIcon('fontAwesome', 'place');
	};

	getIcon.getProviderFontIcon = function(providerName) {
		return getIcon('fontAwesome', 'provider.' + providerName || 'fa fa-plug');
	};

	getIcon.getThingFontIcon = function(thing) {
		return getIcon('fontAwesome', 'thing.' + thing.type) || 'fa fa-cube';
	};

	return getIcon;
});
