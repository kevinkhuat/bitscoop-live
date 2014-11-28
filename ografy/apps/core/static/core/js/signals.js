function modalDialog(modalId, modalLinkName, submitHandler, openHandler) {
	var $modal;

	$modal = $(modalId).modal({show: false});

	$modal.on('click', '.btn-primary', submitHandler || function(event) {
		event.preventDefault();
		$modal.find('form').submit();
	});

	if (modalLinkName) {
		$('a[name="' + modalLinkName + '"]').on('click', function(event) {
			event.preventDefault();
			$modal.modal('toggle');

			if (openHandler) {
				openHandler($modal);
			}
		});
	}

	return $modal;
};

$(function() {
	modalDialog('#ajax-call-modal', 'ajax-call', function(event) {
			var $backend, $result, $form;
			event.preventDefault();
			$modaldialog = $(this).closest('.modal');
			$form = $modaldialog.find('form');
			$backend = $modaldialog.find('[name="logged-in-backend"]');
			$call_url = $modaldialog.find('[name="api_call_url"]');
			$result = $modaldialog.find('.login-result');

			$.get('/auth/call/' + $backend.text().trim() + '/', {
				backend_id: $backend.val(),
				api_call_url: $call_url.val()
			}).done(function(data, xhr, response) {
				$result.find('.user-id').html(data.user_id);
				$result.find('.user-username').html(data.username);
				$result.find('.ajax-API-result-data').html(data);
				$form.hide();
				$result.show();
				setTimeout(function() {
					window.location = '/';
				}, 10000);
			});
		},
		function($modal) {
			$.get('/auth/signals/', {}).done(
				function(data, xhr, response) {
					$logged_in_backend = $modal.find('[name="logged-in-backend"]');
					$.each(data, function(index, item) {
						$logged_in_backend.append(
							$('<option></option>').val(item.id).html(item.provider)
						);
					});
				});
		}
	);

	modalDialog('#ajax-login-modal', 'ajax-login', function(event) {
		var $backend, $accessToken, $accessTokenSecret, $result, $form;
		event.preventDefault();

		$modal = $(this).closest('.modal');
		$form = $modal.find('form');
		$backend = $modal.find('[name="backend"]');
		$accessToken = $modal.find('[name="access_token"]');
		$accessTokenSecret = $modal.find('[name="access_token_secret"]');
		$result = $modal.find('.login-result');

		$.get('/auth/associate/' + $backend.val() + '/', {
			access_token: $accessToken.val(),
			access_token_secret: $accessTokenSecret.val()
		}, function(data, xhr, response) {
			$result.find('.user-id').html(data.id);
			$result.find('.user-username').html(data.username);
			$form.hide();
			$result.show();
			setTimeout(function() {
				window.location = '/';
			}, 10000);
		}, 'json')
	});
});
