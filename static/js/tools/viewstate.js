define(['bluebird', 'jquery', 'nunjucks'], function(Promise, $, nunjucks) {
	/**
	 * Placeholder.
	 *
	 * @private
	 * @returns {boolean}
	 */
	function _returnTrue() {
		return true;
	}


	/**
	 * Placeholder.
	 *
	 * @constructor
	 * @param {String} selector
	 * @param [context]
	 */
	function Component(selector, context) {
		var element, $set;

		if (!(this instanceof Component)) {
			return new Component(selector, context);
		}

		$set = $(selector, context);

		if ($set.length === 0) {
			throw new Error('Element not found.');
		}

		element = $set.get(0);

		if (!(element instanceof HTMLElement)) {
			throw new Error('Invalid HTML element selected.');
		}

		this.element = element;
		this.view = void(0);
	}

	Component.prototype = {
		/**
		 * Placeholder.
		 *
		 * @returns {jQuery} A jQuery set of the removed children.
		 */
		clear: function Component$clear() {
			var i, listener, listeners, $element;

			$element = $(this.element);

			if (this.view) {
				listeners = this.view.listeners;

				for (i = 0; i < listeners.length; i++) {
					listener = listeners[i];
					$element.off(listener.type, listener.selector, listener.callback);
				}

				this.view = void(0);
			}

			return $element.children().detach();
		},

		/**
		 * Placeholder.
		 *
		 * @param content
		 * @returns {Component} Chainable.
		 */
		insert: function Component$insert(content) {
			var i, insertable, listener, listeners, $element;

			$element = $(this.element);

			if (content instanceof View) {
				this.view = content;

				content.component = this;

				insertable = $(content.fragment);
				listeners = this.view.listeners;

				for (i = 0; i < listeners.length; i++) {
					listener = listeners[i];
					$element.on(listener.type, listener.selector, listener.callback);
				}
			}
			else {
				insertable = $(content);
			}

			$element.append(insertable);

			return this;
		},

		/**
		 * Placeholder.
		 *
		 * @param {String} [type]
		 * @param {String} [selector]
		 * @param {Function} [callback]
		 * @returns {Component} Chainable.
		 */
		off: function Component$off(type, selector, callback) {
			$(this.element).off(type, selector, callback);

			return this;
		},

		/**
		 * Placeholder.
		 *
		 * @param {String} type
		 * @param {String} [selector]
		 * @param {Object} [data]
		 * @param {Function} callback
		 * @returns {Component} Chainable.
		 */
		on: function Component$on(type, selector, data, callback) {
			$(this.element).on(type, selector, data, callback);

			return this;
		},

		/**
		 * Placeholder.
		 *
		 * @param {String} type
		 * @param {String} [selector]
		 * @param {Object} [data]
		 * @param {Function} callback
		 * @returns {Component} Chainable.
		 */
		one: function Component$one(type, selector, data, callback) {
			$(this.element).one(type, selector, data, callback);

			return this;
		},

		/**
		 * Placeholder.
		 *
		 * @param {Component} component
		 */
		swapWith: function Component$swapWith(component) {
			return this;
		}
	};


	/**
	 * Placeholder.
	 *
	 * @param type
	 * @param selector
	 * @param data
	 * @param callback
	 * @constructor
	 */
	function Listener(type, selector, data, callback) {
		var i, namespace;

		if (/\s+/.test(type)) {
			throw new Error('Invalid event type. Whitespace not supported.');
		}

		if (/\.(?:\.|$)/.test(type)) {
			throw new Error('Invalid event type. Null classes not supported.');
		}

		if (data == null && callback == null) {
			callback = selector;
			data = selector = void(0);
		}
		else if (callback == null) {
			if (typeof selector === 'string') {
				callback = data;
				data = null;
			}
			else {
				callback = data;
				data = selector;
				selector = void(0);
			}
		}

		if (!callback) {
			throw new Error('Invalid callback function.');
		}

		this.type = type;
		this.selector = selector;
		this.data = data;
		this.callback = callback;

		if (~(i = type.indexOf('.'))) {
			namespace = type.slice(i);

			if (namespace.length > 1) {
				this.namespace = namespace;
			}

			this.baseType = type.slice(0, i);
		}
		else {
			this.namespace = void(0);
			this.baseType = type;
		}
	}

	Listener.prototype = {
		/**
		 * Placeholder.
		 *
		 * @param type
		 * @returns {boolean}
		 */
		is: function Listener$is(type) {
			var i, cls, namespace;

			if (type == null) {
				return true;
			}

			type = String(type);

			if (type[0] === '.') {
				namespace = type;
			}
			else if (~(i = type.indexOf('.', 1))) {
				namespace = type.slice(i);
				type = type.slice(0, i);

				if (this.baseType !== type) {
					return false;
				}
			}
			else {
				return this.baseType === type;
			}

			do {
				i = namespace.indexOf('.', 1);

				if (i < 0) {
					i = namespace.length;
				}

				cls = namespace.slice(0, i);
				namespace = namespace.slice(i);

				if (this.namespace.indexOf(cls) < 0) {
					return false;
				}
			}
			while (namespace.length > 0);

			return true;
		}
	};


	/**
	 * Placeholder.
	 *
	 * @param template
	 * @param url
	 * @param options
	 * @constructor
	 */
	function View(template, url, options) {
		if (!(this instanceof View)) {
			return new View(template, url);
		}

		if (typeof url === 'object') {
			options = url;
			url = void(0);
		}

		if (template instanceof HTMLElement || template instanceof $.fn.init) {
			this.fragment = template;
			this.template = this.url = void(0);
		}
		else {
			this.fragment = void(0);
			this.template = template;
			this.url = url;
		}

		options = options || {};

		this.environment = options.environment || nunjucks;
		this.component = void(0);
		this.listeners = [];
	}

	View.prototype = {
		/**
		 * Placeholder.
		 *
		 * @param type
		 * @param selector
		 * @param callback
		 * @returns {View}
		 */
		off: function View$off(type, selector, callback) {
			var i, filterCallback, filterSelector, filterType, listener, listeners, types, $target;

			// We need to split the types up here so that we can reliably generate a
			// `filterType` and flatten our loop later on.
			// FIXME: This necessitates a weird, extra regexp test. We split on whitespace and recurse, so we're guaranteed not to have whitespace on child calls, and yet we still test for it.
			if (type != null && /\s+/.test(type)) {
				types = String(type).trim().split(/\s+/);

				for (i = 0; i < types.length; i++) {
					this.off(types[i], selector, callback);
				}
			}

			filterType = (type == null) ? _returnTrue :
				function(d) {
					return d.is(type);
				};

			filterSelector = (selector == null) ? _returnTrue :
				function(d) {
					return d.selector === selector;
				};

			filterCallback = (callback == null) ? _returnTrue :
				function(d) {
					return d.callback === callback;
				};

			$target = (typeof this.component === 'undefined') ? $() : $(this.component.element);
			listeners = this.listeners;

			for (i = listeners.length - 1; i >= 0; i--) {
				listener = listeners[i];

				if (filterType(listener) && filterSelector(listener) && filterCallback(listener)) {
					listeners.splice(i, 1);
					$target.off(listener.type, listener.selector, listener.callback);
				}
			}

			return this;
		},

		/**
		 *
		 * @returns {View}
		 * @constructor
		 */
		on: function View$on(type, selector, data, callback) {
			var i, listener, types, $target;

			if (type == null) {
				throw new Error('No event type specified.');
			}

			$target = (typeof this.component === 'undefined') ? $() : $(this.component.element);
			types = String(type).trim().split(/\s+/);

			for (i = 0; i < types.length; i++) {
				listener = new Listener(types[i], selector, data, callback);
				this.listeners.push(listener);
			}

			$target.on(type, selector, data, callback);

			return this;
		},

		/**
		 * Placeholder.
		 *
		 * @param type
		 * @param selector
		 * @param data
		 * @param callback
		 * @returns {View} Chainable.
		 */
		one: function View$one(type, selector, data, callback) {
			var trigger, self = this;

			trigger = function() {
				self.off(type, selector, callback);

				return callback.apply(this, arguments);
			};

			return this.on(type, selector, data, trigger);
		},

		/**
		 * Placeholder.
		 *
		 * @param {Object|String} [context]
		 * @returns {Promise}
		 */
		render: function View$render(context) {
			var self = this;

			return render.call(this, this.template, context || this.url)
				.then(function(fragment) {
					self.fragment = fragment;

					return Promise.resolve(fragment);
				});
		},

		/**
		 * Placeholder.
		 *
		 * @param {Object|String} [context]
		 * @returns {HTMLElement|Array}
		 */
		renderSync: function View$renderSync(context) {
			return this.fragment = renderSync.call(this, this.template, context);
		}
	};

	/**
	 * Placeholder.
	 *
	 * @param {String} template
	 * @param {Object|String} context
	 * @returns {Promise}
	 */
	function render(template, context) {
		var fragment, promise, renderer;

		if (!window.hasOwnProperty('nunjucksPrecompiled')) {
			return Promise.reject(new Error('Precompiled nunjucks templates expected.'));
		}
		else if (!window.nunjucksPrecompiled.hasOwnProperty(template)) {
			return Promise.reject(new Error('Template "' + template + '" not found.'));
		}

		renderer = (this instanceof View) ? this.environment : nunjucks;

		return new Promise(function(resolve, reject) {
			if (typeof context === 'string') {
				promise = $.ajax(context, {
					method: 'GET',
					dataType: 'json'
				}).done(function(context) {
					resolve(context);
				}).fail(function(req) {
					var error;

					error = new Error(req.statusText);
					error.code = req.status;

					reject(error);
				});
			}
			else {
				resolve(context);
			}
		}).then(function(context) {
			var rendered, $el;

			rendered = renderer.render(template, context);
			$el = $(rendered);
			fragment = Array.prototype.slice.call($el);

			if (fragment.length === 1) {
				fragment = fragment[0];
			}

			return Promise.resolve(fragment);
		});
	}

	/**
	 * Placeholder.
	 *
	 * @param {String} template
	 * @param {Object|String} context
	 * @returns {HTMLElement|Array}
	 */
	function renderSync(template, context) {
		var fragment, renderer, rendered, $el;

		if (!window.hasOwnProperty('nunjucksPrecompiled')) {
			throw new Error('Precompiled nunjucks templates expected.');
		}
		else if (!window.nunjucksPrecompiled.hasOwnProperty(template)) {
			throw new Error('Template "' + template + '" not found.');
		}

		renderer = (this instanceof View) ? this.environment : nunjucks;
		rendered = renderer.render(template, context);
		$el = $(rendered);
		fragment = Array.prototype.slice.call($el);

		if (fragment.length === 1) {
			fragment = fragment[0];
		}

		return fragment;
	}

	/**
	 * Swaps the content of two components.
	 *
	 * @param {Component} a
	 * @param {Component} b
	 */
	function swap(a, b) {
		var args;

		args = Array.prototype.slice.call(arguments);

		a.clear();
		b.clear();

		return Promise.resolve(args);
	}


	return {
		Component: Component,
		View: View,

		render: render,
		renderSync: renderSync,
		swap: swap
	};
});
