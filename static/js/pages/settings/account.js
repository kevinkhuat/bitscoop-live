define(['debounce', 'form-monitor', 'jquery', 'lodash', 'jquery-cookie', 'minimodal', 'settings-base'], function(debounce, formMonitor, $, _) {
	$(document).formMonitor('form.auto');

	$(document).on('form-monitor', 'form.auto', debounce(function(e) {
		$.ajax({
			url: $(this).attr('action'),
			method: 'POST',
			data: $.param(e.formData),
			dataType: 'json',
			headers: {
				'X-CSRFToken': $.cookie('csrftoken')
			},
			xhrFields: {
				withCredentials: true
			}
		}).always(function() {
			e.clearFormData();
		}).done(function(data) {
			var handle;

			formMonitor.done(data);

			if (handle = data.handle) {
				$('#handle-link').text(handle);
			}
		}).fail(function(response) {
			formMonitor.fail(response.responseJSON);
		});
	}, 1000));

	$('#password-update-form').on('submit', function(e) {
		var $this = $(this);

		e.preventDefault();

		$this.clearFormErrors();

		$.ajax({
			url: $this.attr('action'),
			method: $this.attr('method'),
			data: $this.serialize(),
			headers: {
				'X-CSRFToken': $.cookie('csrftoken')
			},
			xhrFields: {
				withCredentials: true
			}
		}).done(function(data) {
			formMonitor.done({
				password: true
			});

			$this.trigger('reset');
		}).fail(function(response) {
			formMonitor.fail(response.responseJSON);
		});

		return false;
	});

	$('#deactivate').on('click', function() {
		$('#deactivate-modal').modal({
			position: false,
			postOpen: function() {
				$(this).css('display', 'flex');
			}
		});
	});

	$('#deactivate-modal').on('click', 'button', function(e) {
		var action, $target;

		$target = $(e.target);
		action = $('#deactivate').data('action');

		$.modal.close();

		if ($target.is('.confirm')) {
			$.ajax({
				url: action,
				method: 'POST',
				headers: {
					'X-CSRFToken': $.cookie('csrftoken')
				},
				xhrFields: {
					withCredentials: true
				}
			}).done(function() {
				window.location.href = '/';
			});
		}
	});

	$('#delete').on('click', function() {
		$('#delete-modal').modal({
			position: false,
			postOpen: function() {
				$(this).css('display', 'flex');
			}
		});
	});

	$('#delete-modal').on('click', 'button', function(e) {
		var $target;

		$target = $(e.target);

		$.modal.close();

		if ($target.is('.confirm')) {
			$.ajax({
				url: 'https://api.bitscoop.com/v1/account',
				method: 'DELETE',
				headers: {
					'X-CSRFToken': $.cookie('csrftoken')
				},
				xhrFields: {
					withCredentials: true
				}
			}).done(function() {
				$.ajax({
					url: '/settings/account/delete',
					method: 'POST',
					headers: {
						'X-CSRFToken': $.cookie('csrftoken')
					},
					xhrFields: {
						withCredentials: true
					}
				}).done(function() {
					window.location.href = '/';
				});
			});
		}
	});
});
