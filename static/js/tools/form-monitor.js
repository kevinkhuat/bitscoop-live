define(['jquery', 'lodash'], function($, _) {
	var DATA_KEY = '_form-monitor-data';
	var TIMEOUT_KEY = '_form-monitor-timeout';


	function Listener$onChange(e) {
		var data, formData, name, timeoutId, $form, $icon, $target;

		$target = $(e.target);
		$form = $target.closest('form');

		if ($form.length === 0) {
			$form = $target.closest('.form-monitor-parent');
		}

		if ($form.length > 0) {
			data = {};
			name = $target.attr('name');

			$icon = $('.success-icon[data-for="' + name + '"]');
			$icon.removeClass('shown');
			timeoutId = $icon.data(TIMEOUT_KEY);

			if (timeoutId != null) {
				clearTimeout(timeoutId);
			}

			$form.serializeArray().map(function(d) {
				if (d.name === name) {
					data[d.name] = d.value;
				}
			});

			if ($target.attr('type') === 'checkbox' && $target.hasClass('flag')) {
				data[name] = $target.is(':checked');
			}

			formData = $form.data(DATA_KEY) || {};
			_.merge(formData, data);
			$form.data(DATA_KEY, formData);

			if (_.size(formData) > 0) {
				$form.trigger({
					type: 'form-monitor',
					formData: formData,
					clearFormData: function() {
						$form.removeData(DATA_KEY);
					}
				});
			}
		}
	}


	/**
	 *
	 * @param {Event} e The submit event object.
	 * @returns {boolean} Boolean `false` flag to comply with default event prevention protocol.
	 */
	function Listener$onSubmit(e) {
		var formData, $form;

		e.preventDefault();

		$form = $(e.target);
		formData = $form.data(DATA_KEY) || {};

		if (_.size(formData) > 0) {
			$form.trigger({
				type: 'form-monitor',
				formData: formData,
				clearFormData: function() {
					$form.removeData(DATA_KEY);
				}
			});
		}

		return false;
	}


	/**
	 *
	 * @param data
	 */
	function done(data, namespace) {
		if (namespace) {
			namespace = '[data-namespace="' + namespace + '"]';
		}

		$.each(data, function(name) {
			var timeoutId, $errorlist, $icon;

			$icon = $('.success-icon[data-for="' + name + '"]');
			$errorlist = $('.errorlist[data-for="' + name + '"]');

			if (namespace) {
				$icon = $icon.filter(namespace);
				$errorlist = $errorlist.filter(namespace);
			}

			$icon.addClass('shown');
			$errorlist.empty();

			timeoutId = setTimeout(function() {
				$icon.removeClass('shown');
			}, 3000);

			$icon.data(TIMEOUT_KEY, timeoutId);
		});
	}


	/**
	 * Accepts an error list object, generates an errorlist for each field, and inserts the errorlist into error
	 * containers. An error container must have the class "errorlist" and an attribute "data-for" corresponding to the
	 * field whose errors it accepts.
	 *
	 * @param {Object} data The error list object with keys equal to the input name and values equal to an array of plain-text error messages.
	 */
	function fail(data, namespace) {
		if (namespace) {
			namespace = '[data-namespace="' + namespace + '"]';
		}

		$.each(data, function(name, errors) {
			var $el, $errorlist;

			$el = $('<ul>').addClass('errorlist');

			$.each(errors, function(i, error) {
				var $li;

				$li = $('<li>').text(error);
				$el.append($li);
			});

			$errorlist = $('.errorlist[data-for="' + name + '"]');

			if (namespace) {
				$errorlist = $errorlist.filter(namespace);
			}

			$errorlist.html($el);
		});
	}


	$.fn.extend({
		clearFormErrors: function() {
			$(this).each(function(i, el) {
				var $el;

				$el = $(el);

				$el.find('input').each(function(i, input) {
					var name;

					name = $(input).attr('name');

					$('.errorlist[data-for="' + name + '"]').empty();
				});
			});

			return this;
		},

		formMonitor: function(selector) {
			if (selector != null) {
				$(this)
					.on('change', selector, Listener$onChange)
					.on('submit', selector, Listener$onSubmit);
			}
			else {
				$(this)
					.on('change', Listener$onChange)
					.on('submit', Listener$onSubmit);
			}

			return this;
		}
	});


	return {
		done: done,
		fail: fail
	};
});
