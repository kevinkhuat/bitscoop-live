define(['ga', 'jquery', 'moment', 'nunjucks'], function(ga, $, moment, nunjucks) {
	var TEMPLATES = {
		defaults: {
			url: 'https://bitscoop.com',            // the url you'd like to share.
			title: 'Shared with BitScoop',          // title to be shared alongside your link
			description: 'Shared with BitScoop',    // text to be shared alongside your link
			imageURL: 'https://d1j1f384sln5mu.cloudfront.net/1443324625/assets/images/logo_240.png',       // image to be shared
			hashtags: '@BitScoop',
			via: '@BitScoopLabs'
		},
		urls: {
			share: {
				facebook: {
					href: 'http://www.facebook.com/sharer.php?s=100&p[title]={{ title }}&p[summary]={{ description }}&p[url]={{ url }}&p[images][0]={{ imageURL }}',
					app_id: '',       // Facebook app id for tracking shares. if provided, will use the facebook API
					caption: '',      // caption to be shared alongside your link to Facebook
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
					href: 'https://twitter.com/intent/tweet?text={{ title }}+{{ description }}&url={{ url }}&hashtags={{ hashtags }}&via={{ via }}',
					after: function() {
						ga('send', {
							hitType: 'social',
							socialNetwork: 'tumblr',
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
					href: 'http://www.tumblr.com/share/link?url={{ url }}&name={{ title }}&description={{ description }}',
					after: function() {
						ga('send', {
							hitType: 'social',
							socialNetwork: 'Twitter',
							socialAction: 'share',
							socialTarget: url
						});
					}
				},
				pinterest: {
					href: 'http://pinterest.com/pin/create/button/?url={{ url }}&media={{ imageURL }}&description={{ description }}',
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
					href: 'mailto:?subject={{ url }}&body={{ description }}: {{ url }}',
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
					href: 'sms:&body={{ title }}+{{ url }}',
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
					// http://www.wolframalpha.com/input/?i=December+15+2014+4%3A15+am+PT
					// http://www.wolframalpha.com/input/?i=France
					// http://www.wolframalpha.com/input/?i=December+15+2014+4%3A15+am+PT+weather+Paris
					// http://www.wolframalpha.com/input/?i=capricorn+one
					href: 'http://www.wolframalpha.com/input/?i={{ title }}'
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
					href: 'http://www.wolframalpha.com/input/?i={{ lat }}+latitude,+{{ lng }}+longitude'
				},
				weather: {
					// http://forecast.weather.gov/MapClick.php?lat=40.781581302919285&lon=-73.96648406982422
					href: 'http://forecast.weather.gov/MapClick.php?lat={{ lat }}&lon={{ lng }}'
				}
			}
		}
	};

	function _fixedEncodeURIComponent(str) {
		return encodeURIComponent(str).replace(/[!'()*]/g, function(c) {
			return '%' + c.charCodeAt(0).toString(16);
		});
	}

	// Google social interactions
	// https://developers.google.com/analytics/devguides/collection/analyticsjs/social-interactions

	function _hydrateLocationURL(URLString, lat, lng) {
		return URLString.replace('{{ lat }}', _fixedEncodeURIComponent(lat))
			.replace('{{ lng }}', _fixedEncodeURIComponent(lng));
	}

	function _hydrateShareURL(URLString, url, title, description, imageURL) {
		return URLString.replace('{{ url }}', _fixedEncodeURIComponent(url === '' ? TEMPLATES.defaults.url : url))
			.replace('{{ title }}', _fixedEncodeURIComponent(title === '' ? TEMPLATES.defaults.title : title))
			.replace('{{ description }}', _fixedEncodeURIComponent(description === '' ? TEMPLATES.defaults.description : description))
			.replace('{{ imageURL }}', _fixedEncodeURIComponent(imageURL === '' ? TEMPLATES.defaults.imageURL : imageURL))
			.replace('{{ hashtags }}', _fixedEncodeURIComponent(TEMPLATES.defaults.hashtags))
			.replace('{{ via }}', _fixedEncodeURIComponent(TEMPLATES.defaults.via));
	}

	var renderActions = {
		objects: {
			contacts: {
				render: function renderActions$objects$contact(contact) {
					return nunjucks.render('explorer/components/action/bar.html', {
							share: true,
							action: true
						}) + renderActions.actions.share(
							'',
							contact.source + ' - ' + contact.name + ' - ' + contact.handle + ' - ' + TEMPLATES.defaults.title,
							contact.source + ' - ' + contact.name + ' - ' + contact.handle + ' - ' + TEMPLATES.defaults.description,
							''
						) + renderActions.actions.actions(
							'',
							contact.name,
							contact.name,
							''
						);
				}
			},
			content: {
				render: function renderActions$objects$content(content) {
					return nunjucks.render('explorer/components/action/bar.html', {
							share: true,
							action: true
						}) + renderActions.actions.share(
							content.url === null ? '' : content.url,
							content.title + ' - ' + TEMPLATES.defaults.title,
							content.text + ' - ' + TEMPLATES.defaults.description,
							content.embed_thumbnail === null ? '' : content.embed_thumbnail
						) + renderActions.actions.actions(
							content.url === null ? '' : content.url,
							content.title,
							content.text,
							content.embed_thumbnail === null ? '' : content.embed_thumbnail
						);
				}
			},
			events: {
				render: function renderActions$objects$event(event) {
					return nunjucks.render('explorer/components/action/bar.html', {
							share: true,
							action: true
						}) + renderActions.actions.share(
							'',
							event.provider_name + ' - ' + event.type + ' - ' + moment(event.datetime).format('MMMM Do, YYYY HH:mm:ss a zz') + ' - ' + TEMPLATES.defaults.description,
							event.provider_name + ' - ' + event.type + ' - ' + moment(event.datetime).format('MMMM Do, YYYY HH:mm:ss a zz') + ' - ' + TEMPLATES.defaults.description,
							''
						) + renderActions.actions.actions(
							'',
							moment(event.datetime).format('MMMM Do, YYYY HH:mm:ss a zz'),
							moment(event.datetime).format('MMMM Do, YYYY HH:mm:ss a zz'),
							''
						);
				}
			},
			locations: {
				render: function renderActions$objects$location(location) {
					return nunjucks.render('explorer/components/action/bar.html', {
							share: true,
							location: true,
							action: true
						}) + renderActions.actions.share(
							_hydrateLocationURL(TEMPLATES.urls.location.googleMaps_show.href, location.geolocation[1], location.geolocation[0]),
							'',
							'',
							''
						) + renderActions.actions.location(
							location.geolocation[1],
							location.geolocation[0]
						) + renderActions.actions.actions(
							'',
							location.geolocation[1] + ' latitude, ' + location.geolocation[0] + ' longitude ',
							location.geolocation[1] + ' latitude, ' + location.geolocation[0] + ' longitude ',
							''
						);
				}
			},
			organizations: {
				render: function renderActions$objects$place(organization) {
					return nunjucks.render('explorer/components/action/bar.html', {
							share: true,
							location: false,
							action: true
						}) + renderActions.actions.share(
							organization.url === null ? '' : organization.thumbnail,
							organization.title + ' - ' + TEMPLATES.defaults.title,
							organization.text + ' - ' + TEMPLATES.defaults.description,
							organization.thumbnail === null ? '' : organization.thumbnail
						) + renderActions.actions.actions(
							organization.url === null ? '' : organization.thumbnail,
							organization.title + ' - ' + TEMPLATES.defaults.title,
							organization.text + ' - ' + TEMPLATES.defaults.description,
							organization.thumbnail === null ? '' : organization.thumbnail
						);
				}
			},
			places: {
				render: function renderActions$objects$place(place) {
					return nunjucks.render('explorer/components/action/bar.html', {
							share: true,
							location: true,
							action: true
						}) + renderActions.actions.share(
							_hydrateLocationURL(TEMPLATES.urls.location.googleMaps_show.href, place.location.geolocation[1], place.location.geolocation[0]),
							'',
							'',
							''
						) + renderActions.actions.location(
							place.location.geolocation[1],
							place.location.geolocation[0]
						) + renderActions.actions.actions(
							'',
							place.location.geolocation[1] + ' latitude, ' + place.location.geolocation[0] + ' longitude ',
							place.location.geolocation[1] + ' latitude, ' + place.location.geolocation[0] + ' longitude ',
							''
						);
				}
			},
			things: {
				render: function renderActions$objects$thing(thing) {
					return nunjucks.render('explorer/components/action/bar.html', {
							share: true,
							action: true
						}) + renderActions.actions.share(
							'',
							thing.source + ' - ' + thing.name + ' - ' + thing.handle + ' - ' + TEMPLATES.defaults.title,
							thing.source + ' - ' + thing.name + ' - ' + thing.handle + ' - ' + TEMPLATES.defaults.description,
							''
						) + renderActions.actions.actions(
							'',
							thing.name,
							thing.name,
							''
						);
				}
			}
		},
		actions: {
			share: function renderActions$actions$share(url, title, description, imageURL) {
				return nunjucks.render('explorer/components/action/share.html', {
					facebook_href: _hydrateShareURL(TEMPLATES.urls.share.facebook.href, url, title, description, imageURL),
					twitter_href: _hydrateShareURL(TEMPLATES.urls.share.twitter.href, url, title, description, imageURL),
					googlePlus_href: _hydrateShareURL(TEMPLATES.urls.share.googlePlus.href, url, title, description, imageURL),
					tumblr_href: _hydrateShareURL(TEMPLATES.urls.share.tumblr.href, url, title, description, imageURL),
					pinterest_href: _hydrateShareURL(TEMPLATES.urls.share.pinterest.href, url, title, description, imageURL),
					reddit_href: _hydrateShareURL(TEMPLATES.urls.share.reddit.href, url, title, description, imageURL),
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
			actions: function renderActions$actions$location(url, title, description, imageURL, lat, lng, dateTime) {
				return nunjucks.render('explorer/components/action/actions.html', {
					wolfram_calc_href: _hydrateShareURL(TEMPLATES.urls.actions.wolfram_calc.href, url, title, description, imageURL)
				});
			}
		}
	};

	return renderActions;
});
