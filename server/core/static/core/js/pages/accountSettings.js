define(['jutsu', 'location', 'jquery-cookie'], function(jutsu, location) {
	$(document).ready(function() {
		$('body').autoform('.autoformEnabled', {
			'X-CSRFToken': $.cookie('csrftoken')
		});

		$('[name="update_password"]').click(function() {
			var $this = $(this);
			var $form = $this.closest('form');

			if ($('[name="new_password"]').val() === $('[name="new_password_repeated"]').val()) {
				$.ajax({
					url: $form.attr('action'),
					type: 'POST',
					dataType: 'html',
					data: $form.serialize(),
					headers: {
						'X-CSRFToken': $.cookie('csrftoken')
					}
				}).done(function(data, xhr, response) {
					var errorString;
					var errors = JSON.parse(data);

					if (Object.keys(errors).length > 0) {
						if (_.has(errors, 'new_password')) {
							errorString = '';

							_.forEach(errors.new_password, function(error) {
								errorString += error;
							});

							$('[name="password_errors"]').html(errorString);
						}
						else {
							$('[name="password_errors"]').html('');
						}

						if (_.has(errors, 'password')) {
							errorString = '';

							_.forEach(errors.password, function(error) {
								errorString += error;
							});

							$('[name="password_update"]').html(errorString);
						}
						else {
							$('[name="password_update"]').html('');
						}
					}
					else {
						$('[name="password_update"]').html('Password updated successfully');
						$('[name="password_errors"]').html('');
					}
				});
			}
			else {
				$('[name="password_errors"]').html('This field does not match the first new password field');
			}
		});
	});
});
