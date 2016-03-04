define(['debounce', 'form-monitor', 'jquery', 'jquery-cookie'], function(debounce, formMonitor, $) {
	$(document).formMonitor('form.auto');

	$(document).on('form-monitor', 'form.auto', debounce(function(e) {
		$.ajax({
			url: $(this).attr('action'),
			method: 'PATCH',
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
			formMonitor.done(data);
		}).fail(function(response) {
			formMonitor.fail(response.responseJSON);
		});
	}, 1000));
});
