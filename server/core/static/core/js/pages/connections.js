define(['jquery', 'jquery-cookie'], function($) {
	$(document).on('submit', function(e) {
		var data, permissions, serialized, $form;

		e.preventDefault();

		$form = $(e.target).closest('form');

		serialized = {};
		$form.serializeArray().map(function(d) {
			serialized[d.name] = d.value;
		});

		if (!serialized['signal-name']) {
			serialized['signal-name'] = $form.find('input[name="signal-name"]').attr('placeholder');
		}

		data = {};
		permissions = data.permissions = [];
		data.updateFrequency = parseInt(serialized['update-frequency']);
		data.name = serialized['signal-name'];

		delete serialized['update-frequency'];
		delete serialized['signal-name'];

		$.each(serialized, function(d) {
			permissions.push(d);
		});

		data.permissions = JSON.stringify(data.permissions);

		$.ajax({
			url: $form.attr('action'),
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

		return false;
	});
});
