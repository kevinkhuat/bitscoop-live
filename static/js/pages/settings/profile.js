define(['debounce', 'form-monitor', 'jquery', 'jquery-cookie', 'settings-base'], function(debounce, formMonitor, $) {
	$(document).formMonitor('form.auto');

	$(document).on('change', 'input[name="gender"]', function(e) {
		var $otherGender, $this = $(this);

		$otherGender = $('input[name="other_gender"]');

		if ($this.val() === 'other') {
			$otherGender.val('').closest('div.text-box').show();
		}
		else {
			$otherGender.val('').closest('div.text-box').hide();
		}
	});

	$(document).on('form-monitor', 'form.auto', debounce(function(e) {
		var formData;

		formData = e.formData;

		if (formData.gender === 'other') {
			delete formData.gender;
		}

		if (formData.hasOwnProperty('other_gender')) {
			formData.gender = formData.other_gender;
			delete formData.other_gender;
		}

		$.ajax({
			url: window.location.href,
			method: 'PATCH',
			data: $.param(formData),
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
			formMonitor.done(data);
		}).fail(function(response) {
			formMonitor.fail(response.responseJSON);
		});
	}, 1000));
});
