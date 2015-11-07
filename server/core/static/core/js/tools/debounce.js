define([], function() {
	function debounce(fn, delay) {
		var delayed;

		return function(e) {
			var args, self;

			self = this;
			args = arguments;

			clearTimeout(delayed);

			delayed = setTimeout(function() {
				fn.apply(self, args);
			}, delay);
		};
	}


	return debounce;
});
