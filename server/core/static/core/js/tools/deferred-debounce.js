define([], function() {
	function deferredDebounce(fn) {
		var flag, promise;

		return function(e) {
			var args, self;

			self = this;
			args = arguments;

			if (!flag) {
				if (promise = fn.apply(self, args)) {
					flag = true;
					promise.then(function() {
						flag = false;
					});
				}
			}
		};
	}

	return deferredDebounce;
});
