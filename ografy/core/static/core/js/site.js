define ('site', ['lodash', 'jquery-cookie'], function(_) {
	//Many of these event bindings may become unnecessary after the front-end revamp.
	function bindMainAppUtilities() {
		$('.user-button').click(function() {
			$('.menu.main').toggleClass('hidden');
		});

		$(document.body).click(function(e) {
			if (!e.target.classList.contains('item')) {
				$('.menu.main').addClass('hidden');
			}
		});

		$('.drawer-toggle').click(function() {
			$('.left.drawer').toggleClass('hidden');
			$('.drawer-toggle').toggleClass('hidden');
		});

		$(document.body).click(function(e) {
			if (!e.target.classList.contains('drawer-toggle') && !e.target.classList.contains('link')) {
				$('.left.drawer').addClass('hidden');
				$('.drawer-toggle').not('.map').addClass('hidden');
			}
		});

		$('.fullscreen').click(function() {
			if (document.webkitFullscreenEnabled) {
				if (document.webkitIsFullScreen) {
					document.webkitCancelFullScreen();
				}
				else {
					document.documentElement.webkitRequestFullscreen();
				}
			}
			else if (document.mozFullScreenEnabled) {
				if (document.mozFullScreen) {
					document.mozCancelFullScreen();
				}
				else {
					document.documentElement.mozRequestFullScreen();
				}
			}
			else if (document.msFullscreenEnabled) {
				if (document.msIsFullScreen) {
					document.msCancelFullScreen();
				}
				else {
					document.documentElement.msRequestFullscreen();
				}
			}
			else {
				if (document.isFullScreen) {
					document.cancelFullScreen();
				}
				else {
					document.documentElement.requestFullscreen();
				}
			}
		});

		$('header nav .item')
			.add('.menu .add-filter')
			.add('.signal-button')
			.add('ul.links > li > *')
			.add('.filter-button')
			.add('.dropdown span')
			.add('.list.item')
			.add('.selector')
			.add('.delete-signal')
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
			});

		$('.menu .add-filter').click(function() {
			$('.filter-button').addClass('active');
		});

		$('.selector').click(function() {
			$(this).toggleClass('active');
			$(this).siblings('.item').toggleClass('active');
			if ($(this).hasClass('active') && $(this).closest('.flex').siblings().children().length === 0) {
				var eventType = $(this).parents('.type-grouping').attr('id');
				eventType = eventType.charAt(0).toUpperCase() + eventType.slice(1) + 's';
				$(this).siblings('.item').html('All ' + eventType);
			}
			else {
				var eventType = $(this).parents('.type-grouping').attr('id');
				eventType = eventType.charAt(0).toUpperCase() + eventType.slice(1) + 's';
				$(this).siblings('.item').html(eventType);
			}
			if ($('#event .selector').not('.active').length === 1 || $('.selector.active').length > 1) {
				$('.filter-button').addClass('active');
			}
			else {
				$('.filter-button').removeClass('active');
			}
		});
	}

	function bindConnectSignal(selector) {
		$('body').on('click', selector, function() {
			var data = {};
			var providerName = $('[data-provider-name]').data('provider-name');
			data.updateFrequency = $('input:radio:checked').attr('updateFrequency');
			data.permissions = [];
			data.name = $('input[name=signal-name]')[0].value;

			$('input:checkbox:checked').each(function() {
				var parent = $(this).parents('.event-source-checkbox');
				var eventSourceName = parent.attr('data-event-source-name');
				data.permissions.push(eventSourceName);
			});

			data.permissions = JSON.stringify(data.permissions);
			$.ajax({
				url: '/connections/connect/' + providerName.toLowerCase(),
				type: 'POST',
				'content-type': 'application/json',
				dataType: 'text',
				data: data,
				headers: {
					'X-CSRFToken': $.cookie('csrftoken')
				}
			}).done(function(data, xhr, response) {
				window.location.pathname = data;
			}).fail(function(data, xhr, response) {
				console.log('fail');
			});
		});
	}

	function bindHelpUtilities() {
		$('.help-categories')
			.on('click', '.grid-help-placeholder', function() {
				$('.help-type').toggleClass('is-visible');
				$('.help-categories').toggleClass('open');
			})
			.on('click', '.help-type', function() {
				var dataFilter, $placeholder, $this = $(this);
				$placeholder = $('.grid-help-placeholder');
				dataFilter = $this.data('help-type');
			});
	}

	function scrollToContent() {
		if (window.matchMedia(window.matchMedia('(max-width: 1000px)').matches)) {
			$('main').animate({ scrollTop: $('#content').position().top });
		}
	}

	function bindFAQUtilities() {
		$('body').on('click', '.content-drawer-trigger', function() {
			var $this = $(this);
			$this.siblings('.content-drawer').slideToggle(200).end();
			$this.toggleClass('drawer-open');
		});
	}

	return {
		bindConnectSignal: bindConnectSignal,
		bindFAQUtilities: bindFAQUtilities,
		bindHelpUtilities: bindHelpUtilities,
		bindMainAppUtilities: bindMainAppUtilities,
		scrollToContent: scrollToContent
	};
});
