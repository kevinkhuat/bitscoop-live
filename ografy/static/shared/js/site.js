define ('site', ['cookies'], function(cookies) {
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

	function bindSignalSettings() {
		$('.signal-settings-block').on('change', 'input[type=checkbox]', function() {
			var $this = $(this);
			var enabled = this.checked;
			var $parent = $this.parents('.endpoint-checkbox');
			var endpoint_id = $parent.attr('data-endpoint-id');
			var permission_id = $parent.attr('data-permission-id');
			var signal_id = $parent.attr('data-signal-id');

			var data = {
				enabled: enabled,
				endpoint_id: endpoint_id,
				permission_id: permission_id,
				signal_id: signal_id
			};
			$.ajax({
				url: '/settings/signals',
				type: 'POST',
				dataType: 'html',
				data: data,
				headers: {
					'X-CSRFToken': cookies.getCsrfToken()
				}
			}).done(function(data, xhr, response) {
				var permission_id = data;
				$parent.attr('data-permission-id', permission_id);
			}).fail(function(data, xhr, response) {
				console.log('Endpoint patch failed');
			});
		});

		$('body')
			.on('click', '.delete-cancel', function() {
				$(this).parents('.delete-check').addClass('hidden');
			})
			.on('click', '.delete-signal', function() {
				$(this).parent().siblings('.delete-check').toggleClass('hidden');
			})
			.on('click', '.delete-confirm', function() {
				var $this = $(this);
				var $thisSignalContainer = $this.closest('.drawer-container');
				var $thisSignalId = $thisSignalContainer.data('signal-id');
				$.ajax({
					url: '/opi/signal/' + $thisSignalId,
					type: 'DELETE',
					dataType: 'json',
					data: {},
					headers: {
						'X-CSRFToken': cookies.getCsrfToken()
					}
				}).done(function() {
					$($thisSignalContainer).remove();
				});
			})
			.on('click', '.content-drawer-trigger', function() {
				var $this = $(this);
				$this.siblings('.content-drawer').slideToggle(200).end();
				$this.toggleClass('drawer-open');
			});

		$('.content-list').on('change', 'input[name=name]', function(event) {
			var $target = $(event.target);
			var newName = $target.val();
			$target.closest('.drawer-container').find('.signal-name').html(newName);
		});
	}


	function bindVerifiedSignal(selector) {
		$('body').on('click', selector, function() {
			var data = {};
			var signalId = $(this).parents('.content-list').data('signal-id');
			data.updateFrequency = $('input:radio:checked').attr('updateFrequency');
			data.endpointsDict = {};
			data.name = $('input[name=signal-name]')[0].value;

			$('input:checkbox').each(function() {
				var parent = $(this).parents('.endpoint-checkbox');
				var def_id = parent.attr('data-endpoint-id');
				var auth_id = parent.attr('data-permission-id');
				data.endpointsDict[def_id] = {};
				data.endpointsDict[def_id][auth_id] = $(this).prop('checked');
			});

			data.endpointsDict = JSON.stringify(data.endpointsDict);
			$.ajax({
				url: '/verify/' + signalId,
				type: 'POST',
				'content-type': 'application/json',
				dataType: 'text',
				data: data,
				headers: {
					'X-CSRFToken': cookies.getCsrfToken()
				}
			}).done(function(data, xhr, response) {
				window.location.pathname = data;
			}).fail(function(data, xhr, response) {
				console.log('fail');
			});
		});
	}

	function bindToggleSignal(selector) {
		$('body').on('click', selector, function() {
			var signalId = $(this).parents('.drawer-container').data('signal-id');
			var data = {};
			data.enabled = !($('#onoffswitch-' + signalId)[0].checked);
			$.ajax({
				url: '/opi/signal/' + signalId,
				type: 'PATCH',
				dataType: 'json',
				data: data,
				headers: {
					'X-CSRFToken': cookies.getCsrfToken()
				}
			}).done(function(data, xhr, response) {
				//console.log('succeeded');
			}).fail(function(data, xhr, response) {
				//console.log('failed');
			});
		});
	}

	function bindProviderUtilities() {
		var filter = window.location.hash.substring(1);
		var filterTypes = [
			'collaboration',
			'development',
			'fitness',
			'gaming',
			'health',
			'media',
			'music',
			'productivity',
			'social',
			'video'
		];

		for (var index in filterTypes) {
			var filterType = filterTypes[index];
			$('.grid-filters').append('<div class="filter" data-filter=".' + filterType + '"><div class="filter-text">' + filterType.charAt(0).toUpperCase() + filterType.slice(1) + '</div></div>');
		}

		$('#provider-grid').mixItUp();

		if (filterTypes.indexOf(filter) > -1) {
			$('.filter[data-filter="all"]').removeClass('active');
			$('.filter[data-filter=".' + filter + '"]').trigger('click');
		}
		else {
			$('.filter[data-filter="all"]').addClass('active');
			window.location.hash = 'all';
		}

		$('.grid-filters')
			.on('click', '.grid-filter-placeholder', function() {
				$('.filter').toggleClass('is-visible');
				$('.grid-filters').toggleClass('open');
			})
			.on('click', '.filter', function() {
				var dataFilter, $placeholder, $this = $(this);
				$placeholder = $('.grid-filter-placeholder');
				dataFilter = $this.data('filter');
				if (dataFilter.charAt(0) === '.') {
					dataFilter = dataFilter.slice(1);
				}
				window.location.hash = dataFilter;
				if ($placeholder.css('display') !== 'none') {
					$placeholder.children('.placeholder-text').html($this.children('.filter-text').html());
					$('.filter').toggleClass('is-visible');
					$('.grid-filters').toggleClass('open');
				}
			});

		$('.grid.container').on('click', '.provider-button', function() {
			$this = $(this);
			if (!($this.hasClass('provider-associated'))) {
				window.location = $this.data('link');
			}
			else {
				$('.modal').addClass('visible');
			}
		});

		$('.btn-close').on('click', function() {
			$('.modal').removeClass('visible');
		});
	}

	function scrollToContent() {
		if (window.matchMedia(window.matchMedia('(max-width: 1000px)').matches)) {
			$('main').animate({ scrollTop: $('#content').position().top });
		}
	}

	return {
		bindMainAppUtilities: bindMainAppUtilities,
		bindProviderUtilities: bindProviderUtilities,
		bindSignalSettings: bindSignalSettings,
		bindToggleSignal: bindToggleSignal,
		bindVerifiedSignal: bindVerifiedSignal,
		scrollToContent: scrollToContent
	};
});
