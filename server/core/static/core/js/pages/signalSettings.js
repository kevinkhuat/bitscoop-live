define(['jquery', 'jutsu', 'jquery-cookie'], function($, jutsu) {
	$(document).ready(function() {
		$('.signal-settings-block').on('change', 'input[type=checkbox]', function() {
			var $this = $(this);
			var enabled = this.checked;
			var $parent = $this.parents('.event-source-checkbox');
			var event_source_name = $parent.attr('data-event-source-name');
			var permission_name = $parent.attr('data-permission-name');
			var signal_id = $parent.attr('data-signal-id');

			var data = {
				enabled: enabled,
				event_source_name: event_source_name,
				permission_name: permission_name,
				signal_id: signal_id
			};

			$.ajax({
				url: '/settings/signals',
				type: 'POST',
				dataType: 'html',
				data: data,
				headers: {
					'X-CSRFToken': $.cookie('csrftoken')
				}
			}).done(function(data, xhr, response) {
				$parent.attr('data-permission-name', data);
			}).fail(function(data, xhr, response) {
				console.log('EventSource patch failed');
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
						'X-CSRFToken': $.cookie('csrftoken')
					}
				}).done(function() {
					$($thisSignalContainer).remove();
				});
			})
			.on('click', '.content-drawer-trigger', function() {
				var $this = $(this);
				$this.siblings('.content-drawer').slideToggle(200).end();
				$this.toggleClass('drawer-open');
			})
			.on('click', '.onoffswitch', function() {
				var signalId = $(this).parents('.drawer-container').data('signal-id');
				var data = {};
				data.enabled = ($('#onoffswitch-' + signalId)[0].checked);
				$.ajax({
					url: '/opi/signal/' + signalId,
					type: 'PATCH',
					dataType: 'json',
					data: data,
					headers: {
						'X-CSRFToken': $.cookie('csrftoken')
					}
				}).done(function(data, xhr, response) {
					//console.log('succeeded');
				}).fail(function(data, xhr, response) {
					//console.log('failed');
				});
			})
			.autoform('.autoformEnabled', {
				'X-CSRFToken': $.cookie('csrftoken')
			});

		$('.content-item').on('change', 'input[name=name]', function(event) {
			var $target = $(event.target);
			var newName = $target.val();
			$target.closest('.drawer-container').find('.signal-name').html(newName);
		});
	});
});