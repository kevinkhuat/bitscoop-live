var querystring = require('./querystring');
var url = require('./url');
var uuid = require('./uuid');
var xregexp = require('./xregexp');


// Keep a global id handy for pattern caching.
var gid = 0;
// Keep a pattern cache storage with keys taking the format [root.id]-[name search] for quick reversing.
var patternCache = {};
// Keep a required query variable cache storage with keys taking the format [root.id]-[name search] for quick reversing.
var queryCache = {};
// Scan for group names to generate a reverse URL template string.
var re_group_replace = /\((?:(?:\?P|:)<(\w+)>)?([^\)]*)\)/g;
// Scan for template names to build a reverse URL from template string.
var re_process_template = /{{([^}]+)}}/g;


/**
 * Placeholder.
 *
 * @constructor
 */
function Bundle() {}

Bundle.prototype = {
	initialized: false,

	exec: function Bundle$exec() {
		// If there is no view to execute, then throw.
		if (!this.route.view) {
			throw new Error('No view function bound to route');
		}

		// Execute the view with the arguments and parameters obtained from the trace.
		return this.route.view(this.vars, this.query);
	},

	obj: function Bundle$export() {
		var i, named, positioned;

		named = this.named;
		positioned = this.positioned;

		for (i = 0; i < positioned.length; i++) {
			named['$' + i] = positioned[i];
		}

		return {
			exec: this.exec,
			route: this.route,
			vars: named
		};
	},

	/**
	 * Merges named parameters and positional parameters captured along a Route path. Positional parameters are tracked
	 * and re-indexed in an array so that there are no inherent overlaps. Overlaps in named parameters are not
	 * considered because there is no way to reliably rename conflicts.
	 *
	 * @param {Route} route The matched route at the current position in the trace.
	 * @param {Array} match The XRegExp match object.
	 * @returns {Bundle} Chainable bundle object.
	 */
	push: function Bundle$push(route, match) {
		var i, name, names;

		if (!this.initialized) {
			this.route = route;
			this.named = {};
			this.positioned = [];

			this.initialized = true;
		}

		if (match && (names = route.re.captureNames)) {
			for (i = names.length - 1; i >= 0; i--) {
				name = names[i];

				if (/^\$\d+$/.test(name)) {
					this.positioned.unshift(match[name]);
				}
				else {
					this.named[name] = match[name];
				}
			}
		}

		return this;
	}
};


/**
 * A Route object that serves as a container for an XRegExp match pattern, a name, and a view function.
 *
 * Route instances can be included as sub-routes which are included in any path searching and name finding.
 *
 * @constructor
 * @param {String|Object} pattern The string RegExp pattern used to create an internal XRegExp object.
 * @param {String|Object} [name] The name of the Route. If no name is provided, the Route cannot be searched for by name.
 * @param {Object} [args] A configuration object.
 * @config {Array} [params] An array of required query string parameters that will propagate to the route instance and every sub-route.
 */
function Route(pattern, name, args) {
	if (!(this instanceof Route)) {
		return new Route(pattern, name, args);
	}

	if (typeof pattern === 'object') {
		args = pattern;
		name = pattern.name;
		pattern = pattern.pattern;
	}
	else if (typeof name === 'object') {
		args = name;
		name = name.name;
	}

	if (name && ~name.indexOf('.')) {
		throw new SyntaxError('Invalid character \'.\' in name "' + name + '"');
	}

	this.id = ++gid;
	this.re = new xregexp.XRegExp(pattern);
	this.name = name;
	this.included = [];

	if (args) {
		this.params = args.params || null;
	}
}

Route.prototype = {
	/**
	 * Binds a view function to the Route. The view function is automatically parameterized.
	 *
	 * @param {Array} parameters The parameters to qualify when the view function is executed; automatically passed to `parameterize`.
	 * @param {Function} view The view function to bind to the Route.
	 * @returns {Route} The chainable Route instance.
	 */
	bind: function(parameters, view) {
		this.view = parameterize(parameters, view);

		return this;
	},

	/**
	 * Proxy call for `exec` function using the instance as the parameter `root`.
	 *
	 * @param href
	 * @returns {Object}
	 */
	exec: function Route$exec(href) {
		return exec(this, href);
	},

	/**
	 * Proxy call for `find` function using the instance as the parameter `root`.
	 *
	 * @param name
	 * @returns {Route}
	 */
	find: function Route$find(name) {
		return find(this, name);
	},

	/**
	 * Proxy call for `include` using the instance as the parameter `root`.
	 *
	 * @param pattern
	 * @param name
	 * @param args
	 * @returns {Route} The chainable Route instance.
	 */
	include: function Route$include(pattern, name, args) {
		include(this, pattern, name, args);

		return this;
	},

	/**
	 * Proxy call for `match` using the instance as the parameter `root`.
	 *
	 * @param {String|RegExp|XRegExp} pattern
	 * @returns {Route}
	 */
	match: function Route$match(pattern) {
		return match(this, pattern);
	},

	/**
	 * Proxy call for `trace` using the instance as the parameter `root`.
	 *
	 * @param {String} name
	 * @returns {Array}
	 */
	trace: function Route$trace(name) {
		return trace(this, name);
	}
};


function _includeRoute(root, route) {
	root.included.push(route);
}


/**
 * Recursive helper function that finds a Route in a tree by name.
 *
 * @private
 * @param {Route} route The root Route instance.
 * @param {string} name The name of the Route to find.
 * @returns {Route} The found route starting from the root of the search.
 */
function _routeByName(route, name) {
	var i, included, subroute;

	// Base case. If we hit a route with the provided name, return it.
	if (route.name === name) {
		return route;
	}

	// We didn't hit a URL with the provided name, so branch into each included URL.
	included = route.included;
	for (i = 0; i < included.length; i++) {
		if (subroute = _routeByName(included[i], name)) {
			return subroute;
		}
	}

	return null;
}


/**
 * Recursive helper function that matches a Route path against a provided path string.
 *
 * The bottommost Route instance is returned IFF there is no more path remaining. Otherwise the path is stripped
 * according to the provided `route` XRegExp pattern and the resulting path string is passed to every sub-route.
 *
 * If the end of the path is reached (i.e. length is 0) and there are no matches in the list of included sub-routes,
 * then `null` is returned since there is no match.
 *
 * Similarly if the path length is greater than zero and doesn't match the route or any sub-routes `null` is
 * returned for the no match case.
 *
 * @private
 * @param {Route} route The Route instance passed explicitly to avoid the `this` overhead of .call().
 * @param {String} path The current string path to match against.
 * @returns {Object} A plain JavaScript object with key-values for the matched route, captured parameters, and a tracking index to re-index positioned parameters.
 */
function _routeByPath(route, path) {
	var i, bundle, match, remaining;

	if (match = route.re.exec(path)) {
		remaining = path.slice(match.index + match[0].length);

		if (remaining[0] === '/') {
			remaining = remaining.slice(1);
		}
	}
	else {
		return null;
	}

	if (remaining.length === 0) {
		return new Bundle().push(route, match);
	}
	else {
		for (i = 0; i < route.included.length; i++) {
			if (bundle = _routeByPath(route.included[i], remaining)) {
				return bundle.push(route, match);
			}
		}
	}

	return null;
}


/**
 * Recursive helper function that matches a Route path against a provided path string.
 *
 * @param {Route} route The Route instance passed explicitly to avoid the `this` overhead of .call().
 * @param {String} pattern The current string pattern to match against.
 */
function _routeByPattern(route, pattern) {
	var i, included, match, source;

	pattern = _stripPattern(pattern);
	source = _stripPattern(route.re.source);

	if (pattern === source) {
		return route;
	}

	if (pattern.indexOf(source) === 0) {
		included = route.included;
		pattern = pattern.slice(source.length);

		for (i = 0; i < included.length; i++) {
			if (match = _routeByPattern(included[i], pattern)) {
				return match;
			}
		}
	}

	return null;
}


/**
 * Placeholder.
 *
 * @private
 * @param pattern
 */
function _stripPattern(pattern) {
	// Strip leading "^/" or "^" sequences.
	pattern = pattern.replace(/^(\^?\/?)/, '');
	// Strip trailing "/?$", "/$", or "$" sequences.
	pattern = pattern.replace(/((?:\/|\/\?)?\$?)$/, '');

	return pattern;
}


/**
 * Placeholder.
 *
 * @private
 * @param {Array} traced The trace of the URL search starting with the root of the search and ending with the matching route.
 */
function _template(traced) {
	var i, reversed;

	reversed = '';

	for (i = 0; i < traced.length; i++) {
		// TODO: Make adding this slash dependent on the regex (e.g. ending with "$" results in no trailing slash whereas ending with "/$" or "/?$" does).
		if (reversed.length > 0) {
			reversed += '/';
		}

		reversed += _stripPattern(traced[i].re.source);
	}

	i = 0;
	reversed = reversed.replace(re_group_replace, function(match, name, pattern) {
		if (!name) {
			name = '$' + i++;
		}

		return '{{' + name + '}}';
	});

	return reversed;
}


/**
 * Returns a trace array of Routes matching the provided name. The trace array contains a Route for each included
 * level provided matches are found all the way through starting with the Route instance itself and ending with the
 * found Route.
 *
 * @param {Route} route The root Route from which to start the trace search.
 * @param {String} name The name of the route to locate, passed directly to the `trace` instance function.
 * @returns {Array} The trace array of the route path leading to and including the Route matching the provided `name`.
 */
function _traceRoute(route, name) {
	var i, trace;

	// Base case. If we hit a route with the provided name, return it.
	if (route.name === name) {
		return [route];
	}

	// We didn't hit a URL with the provided name, so branch into each included URL.
	for (i = 0; i < route.included.length; i++) {
		if (trace = _traceRoute(route.included[i], name)) {
			trace.unshift(route);

			return trace;
		}
	}

	// Return `null` so the trace recursion knows where to break.
	// We don't want to add nulls to the end of our trace.
	return null;
}


/**
 * Matches a provided path against the Route instance and its sub-routes.
 *
 * A leading '/' character will be stripped from the provided path. Matches against sub-routes will preserve
 * this behavior. So a Route group will NEVER match something like:
 *
 *   >> new Route('^/example');
 *
 * There should be no leading slash.
 *
 * @param {Route} root The of the route search tree.
 * @param {String} href The URL to match against a Route structure.
 * @returns {Object} A plain JavaScript object with a key-value for the matched route and a key-value for the captured parameters.
 */
function exec(root, href) {
	var bundle, parsed;

	if (parsed = url.parse(href, true)) {
		if (bundle = _routeByPath(root, parsed.location)) {
			bundle = bundle.obj();
			bundle.query = parsed.vars;

			return bundle;
		}
	}

	// No valid match found.
	throw new Error('No route path matches `' + href + '`');
}


/**
 * Returns the final Route from the trace array matching the provided name.
 *
 * Namespacing syntax can be used to direct a search and distinguish between two routes with the same name.
 * Example:
 *
 *   >> route.find('profile');
 *
 * Might match two different routes. A namespace can be applied by using something like:
 *
 *   >> route.find('myapp:profile');
 *
 * Where a route with a unique name of "myapp" has been included in the route tree of the variable "route".
 * Dot-notation can be used to start deeper in the route tree. Example:
 *
 *   >> route.find('myapp.profile:details');
 *
 * Here the search for a URL with the name "details" will start with the Route included with the name "profile"
 * which was in turn included under the Route "myapp" under the Route "route". If no search name is included
 * after the colon, then the URL located with the dot notation directly will be the terminating route. Example:
 *
 *   >> route.find('myapp.profile:');
 *
 * @param {Route} root The anchor of the route tree search.
 * @param {String} name The name of the route to locate, passed directly to the `trace` instance function.
 * @returns {Route} The route matching the provided `name`.
 */
function find(root, name) {
	var i, j, included, locator, locators, route, subroute;

	if (~(i = name.indexOf(':'))) {
		locators = name.slice(0, i);
		name = name.slice(i + 1);
	}

	if (locators) {
		locators = locators.split('.');

		for (i = 0; i < locators.length; i++) {
			if (root === null) {
				return null;
			}

			locator = locators[i];
			included = root.included;

			for (j = 0; j < included.length; j++) {
				subroute = included[j];

				if (subroute.name === locator) {
					root = subroute;

					break;
				}
			}
		}
	}

	if (!name) {
		return root;
	}

	if (route = _routeByName(root, name)) {
		return route;
	}

	// No matching Route found in the tree.
	throw new Error('No route name matches `' + name + '`');
}


/**
 * Accepts N Route instances as individual arguments that will be included as sub-routes for route instance.
 *
 * When matching a parent Route against a string path, included Routes will be checked so long as the stripped
 * path has a non-zero length.
 *
 * @param {Route} root The root Route under which additional provided Routes should be included.
 * @param {String|Route|Array} pattern String pattern that will be used to instantiate a new Route to include, a single Route instance or array of Route instances to include in the route tree.
 * @param {String} [name] The name for the included Route instance if a new Route instance will be created.
 * @param {Object} [args] A configuration object.
 * @config {Array} [params] An array of required query string parameters that will propagate to the route instance and every sub-route.
 * @returns {Route} The chainable Route instance.
 */
function include(root, pattern, name, args) {
	var i, route;

	if (pattern instanceof Array) {
		for (i = 0; i < pattern.length; i++) {
			route = (pattern[i] instanceof Route) ? pattern[i] : new Route(pattern[i]);
			_includeRoute(root, route);
		}
	}
	else {
		route = (pattern instanceof Route) ? pattern : new Route(pattern, name, args);
		_includeRoute(root, route);
	}

	// We can't reliably use these caches anymore if a new URL has been included because it may have been inserted
	// within a cached search path. Thus the only thing we can reliably (and easily) do is flush the cache.
	patternCache = {};
	queryCache = {};
}


/**
 * Matches a provided pattern against the match tree of a Route and its sub-routes.
 *
 * @param {Route} root The root Route from which to start the trace search.
 * @param {String|RegExp|XRegExp} pattern The regex pattern to test against the route tree.
 * @returns {Route} The Route instance that matches the supplied pattern.
 */
function match(root, pattern) {
	var match;

	pattern = new xregexp.XRegExp(pattern).source;

	if (pattern.length === 0) {
		throw new Error('Pattern length must be greater than 0');
	}

	if (match = _routeByPattern(root, pattern)) {
		return match;
	}

	throw new Error('No route pattern matches `' + pattern + '`');
}


/**
 * Generates a proxy function that resolves a list of provided parameters and
 * executes a provided callback with the resolved values.
 *
 * The proxy function accepts a plain JavaScript object with named parameter key-value pairs. The
 * resolved values are recalculated whenever the proxy function is called.
 *
 * @param {Array} parameters An array of parameter names that should be resolved from `args` passed to the returned function.
 * @param {Function} callback The callback function to execute with resolved parameters.
 * @returns {Function} A function that accepts a plain JavaScript object with named parameter key-value pairs.
 */
function parameterize(parameters, callback) {
	if (!(parameters instanceof Array)) {
		throw new TypeError('Parameter `parameters` must be an array');
	}

	if (!(callback instanceof Function)) {
		throw new TypeError('Parameter `callback` must be a function');
	}

	return function parameterized(args, params) {
		var i, resolved;

		resolved = new Array(parameters.length + 1);

		for (i = 0; i < parameters.length; i++) {
			resolved[i] = args[parameters[i]];
		}

		resolved[parameters.length] = params;

		return callback.apply(this, resolved);
	};
}


/**
 * Builds a string URL of the Route matching the provided `name`.
 *
 * @param {Route} root The of the route search tree.
 * @param {String} name The name of the URL to reverse; passed directly to `trace`.
 * @param {Object} [vars] An object with capture group key/value pairs required to reverse the URL pattern into a string.
 * @param {Object} [params] An object with key/value pairs corresponding to query string parameters.
 * @returns {String} The reversed URL string.
 */
function reverse(root, name, vars, params) {
	var i, key, qs, query, reversed, route, traced;

	vars = vars || {};
	params = params || {};

	key = root.id + '-' + name;

	if (!patternCache.hasOwnProperty(key)) {
		traced = trace(root, name);
		reversed = patternCache[key] = _template(traced);

		query = [];

		for (i = 0; i < traced.length; i++) {
			route = traced[i];

			if (route.params) {
				Array.prototype.push.apply(query, route.params);
			}
		}

		queryCache[key] = query.join('***');
	}
	else {
		reversed = patternCache[key];
		query = queryCache[key] ? queryCache[key].split('***') : [];
	}

	reversed = reversed.replace(re_process_template, function(match, name) {
		if (typeof vars[name] === 'undefined') {
			throw new Error('Required path variable \'' + name + '\' not specified');
		}

		return vars[name];
	});

	for (i = 0; i < query.length; i++) {
		if (!params.hasOwnProperty(query[i])) {
			throw new Error('Required parameter \'' + query[i] + '\' not specified');
		}
	}

	// We do have to double loop through params here, but the first loop only checks for required query parameters.
	// Having this increases maintainability by using QueryString functionality supports optional query parameters.
	// We don't necessarily want to build in required parameters into QueryString itself (yet?).
	if (qs = querystring.format(params)) {
		reversed += '?' + qs;
	}

	return reversed;
}


/**
 * Returns a trace array of Routes matching the provided name. The trace array contains a Route for each included
 * level provided matches are found all the way through starting with the Route instance itself and ending with the
 * found Route.
 *
 * @param {Route} root
 * @param {String} name The name of the route to locate, passed directly to the `trace` instance function.
 * @returns {Array} The trace array of the route path leading to and including the Route matching the provided `name`.
 */
function trace(root, name) {
	var i, j, included, locator, locators, match, route, subroute, trace;

	trace = [root];

	if (~(i = name.indexOf(':'))) {
		locators = name.slice(0, i);
		name = name.slice(i + 1);
	}

	if (locators) {
		locators = locators.split('.');

		for (i = 0; i < locators.length; i++) {
			if (root === null) {
				return null;
			}

			locator = locators[i];
			included = root.included;

			for (j = 0; j < included.length; j++) {
				subroute = included[j];

				if (subroute.name === locator) {
					root = subroute;
					trace.push(root);

					break;
				}
			}
		}
	}

	if (!name) {
		return trace;
	}

	if (match = _traceRoute(root, name)) {
		trace.pop();
		Array.prototype.push.apply(trace, match);

		return trace;
	}

	// No valid trace found.
	throw new Error('No route name matches `' + name + '`');
}


module.exports = {
	Route: Route,

	exec: exec,
	find: find,
	include: include,
	match: match,
	parameterize: parameterize,
	reverse: reverse,
	trace: trace
};
