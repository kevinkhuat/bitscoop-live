define(['ga', 'jquery', 'lodash', 'moment', 'nunjucks'], function(ga, $, _, moment, nunjucks) {
	var TEMPLATES = {
		defaults: {
			url: 'https://bitscoop.com',  // the url you'd like to share.
			title: 'Shared via BitScoop',  // title to be shared alongside your link
			description: 'Search & Explore the Internet of You',  // text to be shared alongside your link
			imageURL: 'https://d1j1f384sln5mu.cloudfront.net/1443324625/assets/images/logo_240.png',  // image to be shared
			hashtags: 'BitScoop'
			//via: 'BitScoopLabs'
		},
		urls: {
			share: {
				facebook: {
					href: 'http://www.facebook.com/sharer.php?s=100&p[title]={{ title }}&p[summary]={{ description }}&p[url]={{ url }}&p[images][0]={{ imageURL }}',
					app_id: '',  // Facebook app id for tracking shares. if provided, will use the facebook API
					caption: '',  // caption to be shared alongside your link to Facebook
					after: function() {
						ga('send', {
							hitType: 'social',
							socialNetwork: 'facebook',
							socialAction: 'share',
							socialTarget: url
						});
					}
				},
				twitter: {
					href: 'https://twitter.com/intent/tweet?text={{ title }}&url={{ url }}',
					after: function() {
						ga('send', {
							hitType: 'social',
							socialNetwork: 'twitter',
							socialAction: 'share',
							socialTarget: url
						});
					}
				},
				googlePlus: {
					href: 'https://plus.google.com/share?url={{ url }}',
					after: function() {
						ga('send', {
							hitType: 'social',
							socialNetwork: 'Google+',
							socialAction: 'share',
							socialTarget: url
						});
					}
				},
				tumblr: {
					href: 'http://www.tumblr.com/share/link?url={{ url }}&name={{ title }}&description={{ description }}&tags={{ hashtags }}&show-via=true',
					after: function() {
						ga('send', {
							hitType: 'social',
							socialNetwork: 'tumblr',
							socialAction: 'share',
							socialTarget: url
						});
					}
				},
				pinterest: {
					href: 'http://pinterest.com/pin/create/button/?url={{ url }}&media={{ imageURL }}&description={{ title }}%20-%20{{ description }}',
					after: function() {
						ga('send', {
							hitType: 'social',
							socialNetwork: 'Pinterest',
							socialAction: 'share',
							socialTarget: url
						});
					}
				},
				reddit: {
					href: 'http://www.reddit.com/submit?url={{ url }}&title={{ title }}',
					href_text: 'https://www.reddit.com/submit?title={{ title }}&text={{ description }}',
					after: function() {
						ga('send', {
							hitType: 'social',
							socialNetwork: 'reddit',
							socialAction: 'share',
							socialTarget: url
						});
					}
				},
				linkedin: {
					href: 'http://www.linkedin.com/shareArticle?mini=true&url={{ url }}&title={{ title }}&summary={{ description }}&source={{ url }}',
					after: function() {
						ga('send', {
							hitType: 'social',
							socialNetwork: 'Linked In',
							socialAction: 'share',
							socialTarget: url
						});
					}
				},
				email: {
					href: 'mailto:%20?subject={{ title }}&body={{ url }}%20-%20{{ description }}',
					after: function() {
						ga('send', {
							hitType: 'social',
							socialNetwork: 'Email',
							socialAction: 'share',
							socialTarget: url
						});
					}
				},
				sms: {
					href: 'sms:%20&body={{ title }}%20-%20{{ url }}%20-%20{{ description }}',
					after: function() {
						ga('send', {
							hitType: 'sms',
							socialNetwork: 'Email',
							socialAction: 'share',
							socialTarget: url
						});
					}
				}
			},
			actions: {
				wolfram_calc: {
					href: 'http://www.wolframalpha.com/input/?i={{ term }}'
				},
				cisi: {
					href: 'http://www.canistream.it/search/movie/{{ term }}'
				},
				amazon: {
					href: 'https://www.amazon.com/s/field-keywords={{ term }}'
				},
				wikipedia: {
					href: 'https://en.wikipedia.org/w/index.php?search={{ term }}'
				}
			},
			location: {
				googleMaps_show: {
					// https://www.google.com/maps?q=33.514671899999996,-117.7216579
					href: 'https://www.google.com/maps?q={{ lat }},{{ lng }}'
				},
				googleMaps_nav: {
					// https://www.google.com/maps/dir/Current+Location/43.12345,-76.12345
					href: 'https://www.google.com/maps/dir/Current+Location/{{ lat }},{{ lng }}'
				},
				wolfram: {
					// http://www.wolframalpha.com/input/?i=48.8567+lat+2.3508+long
					href: 'http://www.wolframalpha.com/input/?i={{ lat }}%20latitude,%20{{ lng }}%20longitude'
				},
				weather: {
					// http://forecast.weather.gov/MapClick.php?lat=40.781581302919285&lon=-73.96648406982422
					href: 'http://forecast.weather.gov/MapClick.php?lat={{ lat }}&lon={{ lng }}'
				}
			}
		}
	};

	// Google social interactions
	// https://developers.google.com/analytics/devguides/collection/analyticsjs/social-interactions

	function _fixedEncodeURIComponent(str) {
		return encodeURIComponent(str).replace(/[!'()*]/g, function(c) {
			return '%' + c.charCodeAt(0).toString(16);
		});
	}

	function _hydrateShareURL(URLString, url, title, description, imageURL) {
		return URLString.replace('{{ url }}', _fixedEncodeURIComponent(url === null ? TEMPLATES.defaults.url : url))
			.replace('{{ title }}', _fixedEncodeURIComponent(title === '' ? TEMPLATES.defaults.title : title))
			.replace('{{ description }}', _fixedEncodeURIComponent(description === '' ? TEMPLATES.defaults.description : description))
			.replace('{{ imageURL }}', _fixedEncodeURIComponent(imageURL === '' ? TEMPLATES.defaults.imageURL : imageURL))
			.replace('{{ hashtags }}', _fixedEncodeURIComponent(TEMPLATES.defaults.hashtags));
			//.replace('{{ via }}', _fixedEncodeURIComponent(TEMPLATES.defaults.via));
	}

	function _hydrateLocationURL(URLString, lat, lng) {
		return URLString.replace('{{ lat }}', _fixedEncodeURIComponent(lat))
			.replace('{{ lng }}', _fixedEncodeURIComponent(lng));
	}

	function _hydrateActionURL(URLString, term) {
		return URLString.replace('{{ term }}', _fixedEncodeURIComponent(term));
	}

	function _prettyConcat(stringArray) {
		var result = '';
		_.forEach(stringArray, function(value) {
			if (value) {
				if (result.length > 0) {
					result += ' - ' + value;
				}
				else {
					result += value;
				}
			}
		});
		return result;
	}

	var renderActions = {
		objects: {
			contacts: {
				render: function renderActions$objects$contact(contact) {
					var result =
						//nunjucks.render('explorer/components/action/bar.html', {
						//	share: true,
						//	location: false,
						//	action: contact.name || false
						//}) +
						renderActions.actions.share(
							null,
							TEMPLATES.defaults.title,
							_prettyConcat([contact.source, contact.name, contact.handle]),
							''
						);

					//if (contact.name) {
					//	result += renderActions.actions.actions({
					//		wolfram_calc_href: _hydrateActionURL(TEMPLATES.urls.actions.wolfram_calc.href, contact.name),
					//		wikipedia_href: _hydrateActionURL(TEMPLATES.urls.actions.wikipedia.href, contact.name)
					//	});
					//}
					return result;
				}
			},
			content: {
				render: function renderActions$objects$content(content) {
					var addActionBar, result;
					//addActionBar = _.includes(['audio', 'video', 'game'], content.type);
					result = nunjucks.render('explorer/components/action/bar.html', {
							share: true,
							location: false,
							action: false //addActionBar
						}) +
						renderActions.actions.share(
							content.url || null,
							_prettyConcat([content.title, TEMPLATES.defaults.title]),
							_prettyConcat([content.text || TEMPLATES.defaults.description]),
							content.embed_thumbnail || ''
						);

					//if (addActionBar) {
					//	result += renderActions.actions.actions({
					//		wolfram_calc_href: _hydrateActionURL(TEMPLATES.urls.actions.wolfram_calc.href, content.title),
					//		cisi_href: _hydrateActionURL(TEMPLATES.urls.actions.cisi.href, content.title),
					//		amazon_href: _hydrateActionURL(TEMPLATES.urls.actions.amazon.href, content.title),
					//		wikipedia_href: _hydrateActionURL(TEMPLATES.urls.actions.wikipedia.href, content.title)
					//	});
					//}
					return result;
				}
			},
			events: {
				render: function renderActions$objects$event(event) {
					var result = '';
						//nunjucks.render('explorer/components/action/bar.html', {
						//	share: true,
						//	location: false,
						//	action: event.datetime || true
						//}) + renderActions.actions.share(
						//	null,
						//	_prettyConcat([event.type, TEMPLATES.defaults.title, TEMPLATES.defaults.description]),
						//	_prettyConcat([event.provider_name, event.type, moment(event.datetime).format('MMMM Do, YYYY HH:mm:ss a zz')]),
						//	''
						//);

					//if (event.datetime) {
					//	var formattedDateTime = moment(event.datetime).format('MMMM Do, YYYY HH:mm:ss a zz');
					//	result += renderActions.actions.actions({
					//		wolfram_calc_href: _hydrateActionURL(TEMPLATES.urls.actions.wolfram_calc.href, formattedDateTime),
					//		wikipedia_href: _hydrateActionURL(TEMPLATES.urls.actions.wikipedia.href, formattedDateTime)
					//	});
					//}
					return result;
				}
			},
			locations: {
				render: function renderActions$objects$location(location) {
					return renderActions.actions.location(
						location.geolocation[1],
						location.geolocation[0]
					);
						//nunjucks.render('explorer/components/action/bar.html', {
						//		share: true,
						//		location: false,
						//		action: false
						//	}) + renderActions.actions.share(
						//	_hydrateLocationURL(TEMPLATES.urls.location.googleMaps_show.href, location.geolocation[1], location.geolocation[0]),
						//	'',
						//	'',
						//	''
						//)+
				}
			},
			organizations: {
				render: function renderActions$objects$place(organization) {
					var result = '';
					//nunjucks.render('explorer/components/action/bar.html', {
					//	share: (typeof (organization.url) === 'undefined'),
					//	location: false,
					//	action: true
					//}) + renderActions.actions.actions({
					//		wolfram_calc_href: _hydrateActionURL(TEMPLATES.urls.actions.wolfram_calc.href, organization.title),
					//		wikipedia_href: _hydrateActionURL(TEMPLATES.urls.actions.wikipedia.href, organization.title)
					//	});
                    //
					//if (typeof (organization.url) === 'undefined') {
					//	result += renderActions.actions.share(organization.title || organization.text);
					//}
					return result;
				}
			},
			places: {
				render: function renderActions$objects$place(place) {
					return renderActions.actions.share(
							_hydrateLocationURL(TEMPLATES.urls.location.googleMaps_show.href, place.location.geolocation[1], place.location.geolocation[0]),
							'',
							'',
							''
						) + renderActions.actions.location(
							place.location.geolocation[1],
							place.location.geolocation[0]
						) + renderActions.actions.actions({
							wolfram_calc_href: _hydrateActionURL(TEMPLATES.urls.actions.wolfram_calc.href, place.name || place.reverse_geolocation),
							wikipedia_href: _hydrateActionURL(TEMPLATES.urls.actions.wikipedia.href, place.name || place.reverse_geolocation)
						});
					//nunjucks.render('explorer/components/action/bar.html', {
					//		share: false, //true
					//		location: true,
					//		action: true
					//	}) +
				}
			},
			things: {
				render: function renderActions$objects$thing(thing) {
					return nunjucks.render('explorer/components/action/bar.html', {
								share: true,
								location: false,
								action: false //true
							}) + renderActions.actions.share(
								thing.url || null,
								_prettyConcat([thing.title, TEMPLATES.defaults.title]),
								_prettyConcat([thing.text || TEMPLATES.defaults.description]),
								thing.embed_thumbnail || ''
						);
						//) + renderActions.actions.actions({
						//	wolfram_calc_href: _hydrateActionURL(TEMPLATES.urls.actions.wolfram_calc.href, thing.title),
						//	cisi_href: _hydrateActionURL(TEMPLATES.urls.actions.cisi.href, thing.title),
						//	amazon_href: _hydrateActionURL(TEMPLATES.urls.actions.amazon.href, thing.title),
						//	wikipedia_href: _hydrateActionURL(TEMPLATES.urls.actions.wikipedia.href, thing.title)
						//}
						//
				}
			}
		},
		actions: {
			share: function renderActions$actions$share(url, title, description, imageURL) {
				var facebookHref, googlePlusHref, redditHref;
				if (url !== null) {
					facebookHref = _hydrateShareURL(TEMPLATES.urls.share.facebook.href, url, title, description, imageURL);
					googlePlusHref = _hydrateShareURL(TEMPLATES.urls.share.googlePlus.href, url, title, description, imageURL);
					redditHref = _hydrateShareURL(TEMPLATES.urls.share.reddit.href, url, title, description, imageURL);
				}
				else {
					redditHref = _hydrateShareURL(TEMPLATES.urls.share.reddit.href_text, url, title, description, imageURL);
				}
				return nunjucks.render('explorer/components/action/share.html', {
					facebook_href: facebookHref,
					twitter_href: _hydrateShareURL(TEMPLATES.urls.share.twitter.href, url, title.replace(' - Shared with BitScoop', '').slice(0, 60) + ' - via @BitScoopLabs', description, imageURL),
					googlePlus_href: googlePlusHref,
					tumblr_href: _hydrateShareURL(TEMPLATES.urls.share.tumblr.href, url, title, description, imageURL),
					pinterest_href: _hydrateShareURL(TEMPLATES.urls.share.pinterest.href, url, title, description, imageURL),
					reddit_href: redditHref,
					linkedin_href: _hydrateShareURL(TEMPLATES.urls.share.linkedin.href, url, title, description, imageURL),
					email_href: _hydrateShareURL(TEMPLATES.urls.share.email.href, url, title, description, imageURL),
					sms_href: _hydrateShareURL(TEMPLATES.urls.share.sms.href, url, title, description, imageURL)
				});
			},
			location: function renderActions$actions$location(lat, lng) {
				return nunjucks.render('explorer/components/action/location.html', {
					googleMaps_show_href: _hydrateLocationURL(TEMPLATES.urls.location.googleMaps_show.href, lat, lng),
					googleMaps_nav_href: _hydrateLocationURL(TEMPLATES.urls.location.googleMaps_nav.href, lat, lng),
					weather_href: _hydrateLocationURL(TEMPLATES.urls.location.weather.href, lat, lng),
					wolfram_href: _hydrateLocationURL(TEMPLATES.urls.location.wolfram.href, lat, lng)
				});
			},
			actions: function renderActions$actions$location(context) {
				return nunjucks.render('explorer/components/action/actions.html', context);
			}
		}
	};

	return renderActions;
});
