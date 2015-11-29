define(['ga', 'jquery', 'moment', 'nunjucks', 'share-button'], function(ga, $, moment, nunjucks) {
	var SHARE_DESC_DEFAULT = 'Shared with BitScoop';

	var URL_WOLFRAM_DOMAIN_ROUTE = 'http://www.wolframalpha.com/input/?i=';
	var URL_WOLFRAM_LOC_PARAMS = '{{ LAT }}+lat+{{ LONG }}+long+';

	var URL_GOOGLE_DOMAIN = 'https://www.google.com';
	var URL_GOOGLE_MAPS_LOCATION_ROUTE_PARAMS = '/maps?q={{ LAT }},{{ LONG }}';
	var URL_GOOGLE_MAPS_LOCATION_NAV_ROUTE_PARAMS = '/maps/dir/Current+Location/{{ LAT }},{{ LONG }}';

	var URL_WEATHER_FORECAST_DOMAIN_ROUTE_PARAMS = 'http://forecast.weather.gov/MapClick.php?lat={{ LAT }}&lon={{ LONG }}';

	function _replaceLocation(URLString, location) {
		URLString.replace('{{ LAT }}', location.LAT).replace('{{ LONG }}', location.LONG);
	}

	function createActionBar(url, title, description, imageURL, location, datetime) {
		var actionBar = nunjucks.render('explorer/grid_view_item.html', {
			// https://gearside.com/easily-link-to-locations-and-directions-using-the-new-google-maps/
			// https://www.google.com/maps?q=33.514671899999996,-117.7216579
			GoogleMapsURL: URL_GOOGLE_DOMAIN + _replaceLocation(URL_GOOGLE_MAPS_LOCATION_ROUTE_PARAMS, location),
			// https://www.google.com/maps/dir/Current+Location/43.12345,-76.12345
			GoogleMapsNavURL: URL_GOOGLE_DOMAIN + _replaceLocation(URL_GOOGLE_MAPS_LOCATION_NAV_ROUTE_PARAMS, location),
			// http://www.wolframalpha.com/input/?i=48.8567+lat+2.3508+long+ =
			WolframLocSearchURL: URL_WOLFRAM_DOMAIN_ROUTE + _replaceLocation(URL_WOLFRAM_LOC_PARAMS, location),
			// http://www.wolframalpha.com/input/?i=December+15+2014+4%3A15+am+PT
			WolframClockURL: URL_WOLFRAM_DOMAIN_ROUTE + moment(datetime).format('MMMM Do, YYYY HH:mm:ss a zz'),
			// http://www.wolframalpha.com/input/?i=France
			// http://www.wolframalpha.com/input/?i=December+15+2014+4%3A15+am+PT+weather+Paris
			// http://www.wolframalpha.com/input/?i=capricorn+one
			WolframCalcURL: URL_WOLFRAM_DOMAIN_ROUTE + title,
			// http://forecast.weather.gov/MapClick.php?lat=40.781581302919285&lon=-73.96648406982422
			WeatherURL: _replaceLocation(URL_WEATHER_FORECAST_DOMAIN_ROUTE_PARAMS, location)
		});

		var $actionBar = $(actionBar);

		// Google social interactions
		// https://developers.google.com/analytics/devguides/collection/analyticsjs/social-interactions

		var config = {
			//protocol:     // the protocol you'd prefer to use. [Default: your current protocol]
			url: url,          // the url you'd like to share. [Default: `window.location.href`]
			title: title,        // title to be shared alongside your link [Default: See below in defaults section]
			description: description,  // text to be shared alongside your link, [Default: See below in defaults section]
			image: imageURL,        // image to be shared [Default: See below in defaults section]
			//ui: {
			//  flyout:       // change the flyout direction of the shares. chose from `top left`, `top center`, `top right`, `bottom left`, `bottom right`, `bottom center`, `middle left`, or `middle right` [Default: `top center`]
			//  button_font:  // include the Lato font set from the Google Fonts API. [Default: `true`]
			//  buttonText:  // change the text of the button, [Default: `Share`]
			//  icon_font:    // include the minified Entypo font set. [Default: `true`]
			//},
			networks: {
				googlePlus: {
					//enabled: // Enable Google+. [Default: true]
					//url:     // the url you'd like to share to Google+ [Default: config.url]
					//before: function(element) {
					//	this.url = element.getAttribute('data-url');
					//	this.text = 'Changing the Facebook Share Configurations';
					//},
					after: function() {
						console.log('User Google+ shared: ', this.url);
						ga('send', {
							hitType: 'social',
							socialNetwork: 'Google+',
							socialAction: 'share',
							socialTarget: url
						});
					}
				},
				twitter: {
					//enabled:      // Enable Twitter. [Default: true]
					//url:          // the url you'd like to share to Twitter [Default: config.url]
					//description:  // text to be shared alongside your link to Twitter [Default: config.description]
					after: function() {
						console.log('User Twitter shared: ', this.url);
						ga('send', {
							hitType: 'social',
							socialNetwork: 'Twitter',
							socialAction: 'share',
							socialTarget: url
						});
					}
				},
				facebook: {
					//enabled:      // Enable Facebook. [Default: true]
					//load_sdk:     // Load the FB SDK. If false, it will default to Facebook's sharer.php implementation.
					//              // NOTE: This will disable the ability to dynamically set values and rely directly on applicable Open Graph tags.
					//              // [Default: true]
					//url:          // the url you'd like to share to Facebook [Default: config.url]
					//app_id:       // Facebook app id for tracking shares. if provided, will use the facebook API
					//title:        // title to be shared alongside your link to Facebook [Default: config.title]
					caption: SHARE_DESC_DEFAULT,      // caption to be shared alongside your link to Facebook [Default: null]
					//description:  // text to be shared alongside your link to Facebook [Default: config.description]
					//image:        // image to be shared to Facebook [Default: config.image]
					after: function() {
						console.log('User facebook shared: ', this.url);
						ga('send', {
							hitType: 'social',
							socialNetwork: 'facebook',
							socialAction: 'share',
							socialTarget: url
						});
					}
				},
				pinterest: {
					//enabled:      // Enable Pinterest. [Default: true]
					//url:          // the url you'd like to share to Pinterest [Default: config.url]
					//image:        // image to be shared to Pinterest [Default: config.image]
					//description:  // text to be shared alongside your link to Pinterest [Default: config.description]
					after: function() {
						console.log('User Pinterest shared: ', this.url);
						ga('send', {
							hitType: 'social',
							socialNetwork: 'Pinterest',
							socialAction: 'share',
							socialTarget: url
						});
					}
				},
				reddit: {
					//enabled:  // Enable Reddit. [Default: true]
					//url:      // the url you'd like to share to Reddit [Default: config.url]
					//title:    // title to be shared alongside your link to Reddit [Default: config.title]
					after: function() {
						console.log('User reddit shared: ', this.url);
						ga('send', {
							hitType: 'social',
							socialNetwork: 'reddit',
							socialAction: 'share',
							socialTarget: url
						});
					}
				},
				linkedin: {
					//enabled:      // Enable LinkedIn. [Default: true]
					//url:          // the url you'd like to share to LinkedIn [Default: config.url]
					//title:        // title to be shared alongside your link to LinkedIn [Default: config.title],
					//description:  // text to be shared alongside your link to LinkedIn [Default: config.description]
					after: function() {
						console.log('User Linked In shared: ', this.url);
						ga('send', {
							hitType: 'social',
							socialNetwork: 'Linked In',
							socialAction: 'share',
							socialTarget: url
						});
					}
				},
				whatsapp: {
					//enabled:      // Enable WhatsApp. [Default: true]
					//description:  // text to be shared alongside your link to WhatsApp [Default: config.description],
					//url:          // the url you'd like to share to WhatsApp [Default: config.url]
					after: function() {
						console.log('User WhatsApp shared: ', this.url);
						ga('send', {
							hitType: 'social',
							socialNetwork: 'WhatsApp',
							socialAction: 'share',
							socialTarget: url
						});
					}
				},
				email: {
					//enabled:      // Enable Email. [Default: true]
					//title:        // the subject of the email [Default: config.title]
					//description:  // The body of the email [Default: config.description]
					after: function() {
						console.log('User Email shared: ', this.url);
						ga('send', {
							hitType: 'social',
							socialNetwork: 'Email',
							socialAction: 'share',
							socialTarget: url
						});
					}
				}
			}
		};

		var share = new ShareButton('.share-button', config);
		share.open();

		return share;
	}

	return createActionBar;
});
