define([], function() {
	function throttle(fn, delay) {
		var disabled, throttler;

		if (typeof fn !== 'function') {
			throw new Error('Invalid callback function specified');
		}

		if (arguments.length < 2) {
			throttler = function(e) {
				var cb, promise;

				if (!disabled) {
					promise = fn.apply(this, arguments);

					if (promise && (typeof promise.always === 'function' || typeof promise.finally === 'function')) {
						disabled = true;

						cb = function() {
							disabled = false;
						};

						if (typeof promise.always === 'function') {
							promise.always(cb);
						}
						else if (typeof promise.finally === 'function') {
							promise.finally(cb);
						}
					}

					return promise;
				}
			};
		}
		else {
			throttler = function(e) {
				if (!disabled) {
					disabled = true;

					setTimeout(function() {
						disabled = false;
					}, delay);

					return fn.apply(this, arguments);
				}
			};
		}

		return throttler;
	}


	return throttle;
});
