define(['debounce', 'form-monitor', 'jquery', 'moment', 'bootstrap-transition', 'bootstrap-collapse', 'datetimepicker', 'jquery-cookie', 'minimodal', 'settings-base'], function(debounce, formMonitor, $, moment) {
	$(document).ready(function() {
		$(document).formMonitor('form.auto');

		$('#birthday').datetimepicker({
			format: 'YYYY-MM-DD',
			icons: {
				up: 'fa fa-chevron-up',
				down: 'fa fa-chevron-down',
				previous: 'fa fa-chevron-left',
				next: 'fa fa-chevron-right',
				time: 'fa fa-clock-o',
				date: 'fa fa-calendar'
			}
		});

		// The datetimepicker has a stopImmediatePropagation on its input change. This manually triggers a change
		// on the input in such a way that it will properly bubble up to form-monitor.
		$('#birthday').on('dp.change', function(e) {
			var event;

			if (e.date && e.oldDate && (e.oldDate !== e.date)) {
				event = $.Event('change');
				event.target = $('.form-control').get(0);

				$('form.auto').trigger(event);
			}
		});

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
});
