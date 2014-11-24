$(document).ready(function() {
	// using jQuery
	function getCookie(name) {
	    var cookieValue = null;
	    if (document.cookie && document.cookie != '') {
	        var cookies = document.cookie.split(';');
	        for (var i = 0; i < cookies.length; i++) {
	            var cookie = jQuery.trim(cookies[i]);
	            // Does this cookie string begin with the name we want?
	            if (cookie.substring(0, name.length + 1) == (name + '=')) {
	                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                break;
	            }
	        }
	    }
	    return cookieValue;
	}

	var csrftoken = getCookie('csrftoken');

	$('#event-form')
		.data('fields', ['signal-id', 'user-id', 'provider-id', 'provider-name'])
		.data('post-data-cb', function() {
			var data, fields, that = this;

			data = {};
			fields = this.data('fields');

			$.each(fields, function(i, name) {
				var num, val;

				val = that.find('input[name="event-' + name + '"]').val();
				num = parseInt(val);

				data[name] = isNaN(num) ? val : num;
			});

			return data;
		})
		.data('put-data-cb', function() {
			var data, id, postdataCallback;

			postdataCallback = this.data('post-data-cb');
			data = postdataCallback.call(this);

			id = parseInt(this.find('input[name="event-db-id"]').val());

			if (isNaN(id)) {
				throw new Error('PUTing requires an ID');
			}

			data['id'] = id;

			return data;
		});

	$(document).on('click', 'form.action input[type="submit"]', function(e) {
		var datacb, formData, method, $form, $this = $(this);

		e.preventDefault();

		method = $this.data('method').toLowerCase();
		$form = $this.closest('form');
		datacb = $form.data(method + '-data-cb');
		formData = datacb.call($form);

		console.log(formData);

		$.ajax({
			url: '/obase/event',
			type: method.toUpperCase(),
			data: JSON.stringify(formData),
			dataType: 'json',
			headers: {"X-CSRFToken": csrftoken}
		}).done(function(data, xhr, response) {
			$('#event-result').html(JSON.stringify(data));
		}).fail(function() {
			console.log('FAILED');
		});
	});
});