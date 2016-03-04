define([], function() {
	var exports;

	var qs = {
		/**
		 *
		 * @returns {Object}
		 */
		parse: function() {
			var i, key, token, tokens, value, values;

			values = {};
			tokens = location.search.slice(1).split('&');

			if (tokens.length === 1 && tokens[0] === '') {
				return values;
			}

			for (i = 0; i < tokens.length; i++) {
				token = tokens[i].split('=');
				key = decodeURIComponent(token[0]);
				value = decodeURIComponent(token[1]);

				values[key] = value;
			}

			return values;
		},

		/**
		 *
		 * @param obj
		 * @returns {String}
		 */
		format: function(obj) {
			var formatted, prop;

			formatted = '';

			if (obj) {
				for (prop in obj) {
					if (!obj.hasOwnProperty(prop)) {
						break;
					}

					formatted += fixedEncodeURIComponent(prop) + '=' + fixedEncodeURIComponent(obj[prop]) + '&';
				}

				formatted = formatted.slice(0, -1);
			}

			return (formatted.length > 0) ? '?' + formatted : formatted;
		}
	};

	function extendFactory(obj, update) {
		/**
		 * Removes a query parameter or set of query parameters from the query string and pushes the supplied state
		 * onto the history stack.
		 *
		 * @param {String|Array} name
		 * @param {*} [state] The state to push onto the history stack.
		 */
		function delParam(name, state) {
			var i, params, search;

			params = qs.parse();

			if (Array.isArray(name)) {
				for (i = 0; i < name.length; i++) {
					delete params[name[i]];
				}
			}
			else {
				delete params[name];
			}

			search = qs.format(params);

			if (state || search !== location.search) {
				return update(location.origin + location.pathname + search + location.hash, state);
			}
		}

		/**
		 * Sets the hash on the location and pushes the supplied state onto the history stack.
		 *
		 * @param {String} hash
		 * @param {*} [state] The state to push onto the history stack.
		 */
		function hash(hash, state) {
			if (hash == null) {
				hash = '';
			}

			if (hash[0] === '#') {
				hash = hash.slice(1);
			}

			if (state || hash !== location.hash.slice(1)) {
				hash = (hash.length > 0) ? '#' + hash : hash;

				return update(location.origin + location.pathname + location.search + hash, state);
			}
		}

		/**
		 * Sets the path on the location and pushes the supplied state onto the history stack.
		 *
		 * @param {String} path
		 * @param {*} [state] The state to push onto the history stack.
		 */
		function path(path, state) {
			var pathname;

			pathname = location.pathname;

			if (!path || path[0] === '/') {
				pathname = path;
			}
			else {
				pathname = pathname.replace(/\/$/, '') + '/' + path;
			}

			if (state || location.pathname.replace(/\/$/, '') !== pathname.replace(/\/$/, '')) {
				return update(location.origin + pathname + location.search + location.hash, state);
			}
		}

		/**
		 * Sets a query parameter or set of query parameters on the location and pushes the supplied state onto the
		 * history stack.
		 *
		 * @param {String|Object} name
		 * @param {String} [value]
		 * @param {*} [state] The state to push onto the history stack.
		 */
		function setParam(name, value, state) {
			var key, params, search;

			params = qs.parse();

			if (typeof name === 'object') {
				state = value;

				for (key in name) {
					if (!name.hasOwnProperty(key)) {
						break;
					}

					params[key] = name[key];
				}
			}
			else {
				params[name] = value;
			}

			search = qs.format(params);

			if (state || search !== location.search) {
				return update(location.origin + location.pathname + search + location.hash, state);
			}
		}

		obj.delParam = delParam;
		obj.hash = hash;
		obj.setParam = obj.param = setParam;
		obj.path = path;
	}

	/**
	 *
	 *
	 * @param {String} str
	 * @returns {String}
	 */
	function fixedEncodeURIComponent(str) {
		if (str == null) {
			return '';
		}

		return encodeURIComponent(str).replace(/[!'()*]/g, function(c) {
			return '%' + c.charCodeAt(0).toString(16);
		});
	}

	/**
	 *
	 * @param {String} url
	 * @param {*} [state] The state to push onto the history stack.
	 */
	function push(url, state) {
		return history.pushState(state, null, url);
	}

	/**
	 *
	 * @param {String} url
	 * @param {*} [state] The state to push onto the history stack.
	 */
	function replace(url, state) {
		return history.replaceState(state, null, url);
	}


	exports = {
		back: history.back,
		go: history.go,
		push: push,
		replace: replace
	};

	Object.defineProperties(exports, {
		length: {
			enumerable: true,
			get: function() {
				return window.history.length;
			}
		},

		state: {
			enumerable: true,
			get: function() {
				return window.history.state;
			}
		}
	});

	extendFactory(exports, push);
	extendFactory(replace, replace);

	return exports;
});
