define(['debounce', 'form-monitor', 'jquery', 'lodash', 'jquery-cookie', 'jquery-deparam', 'minimodal', 'settings-base'], function(debounce, formMonitor, $, _) {
	$(document).ready(function() {
		var params;

		params = $.deparam(window.location.search.slice(1));

		if (params.provider) {
			$('.connection[data-provider-id="' + params.provider + '"]').addClass('active');
		}

		$(document).on('click', '.connection .title', function(e) {
			var $connection;

			$connection = $(this).closest('.connection');

			if (e.shiftKey) {
				$connection.toggleClass('active');
			}
			else if ($connection.hasClass('active')) {
				$connection.removeClass('active');
			}
			else {
				$connection.addClass('active')
					.siblings('.active').removeClass('active');
			}
		});

		$(document).formMonitor('form.auto');

		$(document).on('form-monitor', 'form.auto', debounce(function(e) {
			var sources, formData, id, serialized, $this = $(this);

			formData = e.formData;

			serialized = _.pick(formData, ['name', 'enabled']);
			id = $this.closest('.connection').data('id');
			serialized.connection_id = id;
			sources = {};

			$.each(formData, function(key, value) {
				if (!serialized.hasOwnProperty(key)) {
					sources[key] = value;
				}
			});

			serialized.sources = sources;

			$.ajax({
				url: $this.attr('action'),
				method: 'PATCH',
				data: JSON.stringify(serialized),
				contentType: 'application/json',
				headers: {
					'X-CSRFToken': $.cookie('csrftoken')
				},
				xhrFields: {
					withCredentials: true
				}
			}).always(function() {
				e.clearFormData();
			}).done(function(data) {
				formMonitor.done(formData, id);

				if (formData.hasOwnProperty('name')) {
					$this.closest('.connection').find('div.name').text(formData.name);
				}
			});
		}, 1000));

		$(document).on('click', 'button.disable,button.delete,button.enable', function(e) {
			var id, name, $connection, $modal, $this = $(this);

			$connection = $this.closest('.connection');
			id = $connection.data('id');
			name = $connection.find('.title .name').text();

			if ($this.is('.enable')) {
				$.ajax({
					url: '/settings/connections',
					method: 'PATCH',
					data: JSON.stringify({
						connection_id: id,
						enabled: true
					}),
					contentType: 'application/json',
					headers: {
						'X-CSRFToken': $.cookie('csrftoken')
					},
					xhrFields: {
						withCredentials: true
					}
				}).done(function() {
					$connection.removeClass('disabled');
					$this.addClass('danger disable')
						.removeClass('primary enable')
						.text('Disable');
				});
			}
			else {
				$modal = $($this.is('.disable') ? '#disable-modal' : '#delete-modal');

				$modal.data('connection-id', id).find('span.name').text(name);
				$modal.modal({
					position: false,
					postOpen: function() {
						$(this).css('display', 'flex');
					}
				});
			}
		});

		$('#disable-modal').on('click', 'button', function(e) {
			var data, id, $modal;

			if ($(this).is('.confirm')) {
				$modal = $.modal.obj;
				id = $modal.data('connection-id');

				data = {
					connection_id: id,
					enabled: false
				};

				$.ajax({
					url: '/settings/connections',
					method: 'PATCH',
					data: JSON.stringify(data),
					contentType: 'application/json',
					headers: {
						'X-CSRFToken': $.cookie('csrftoken')
					},
					xhrFields: {
						withCredentials: true
					}
				}).done(function() {
					$('.connection[data-id="' + id + '"]')
						.addClass('disabled')
						.find('button.disable')
						.removeClass('danger disable')
						.addClass('primary enable')
						.text('Enable');

					$.modal.close();
				});
			}
			else {
				$.modal.close();
			}
		});

		$('#delete-modal').on('click', 'button', function(e) {
			var id, $modal;

			if ($(this).is('.confirm')) {
				$modal = $.modal.obj;
				id = $modal.data('connection-id');

				$.ajax({
					url: 'https://api.bitscoop.com/v1/connections/' + id,
					method: 'DELETE',
					headers: {
						'X-CSRFToken': $.cookie('csrftoken')
					},
					xhrFields: {
						withCredentials: true
					}
				}).done(function() {
					$('.connection[data-id="' + id + '"]').remove();
					$.modal.close();
				});
			}
			else {
				$.modal.close();
			}
		});
	});
});
