var cache = {};


/**
 * Creates an extended regular expression object for matching text with a pattern. Differs from a
 * native regular expression in that additional syntax and flags are supported.
 *
 * @constructor
 * @param {String|RegExp} pattern Regex pattern string, or an existing regex object to copy.
 * @param {String} [flags] Any combination of flags.
 */
function XRegExp(pattern, flags) {
	var compiled, nativ;

	if (!(this instanceof XRegExp)) {
		return new XRegExp(pattern, flags);
	}

	if (pattern instanceof RegExp || pattern instanceof XRegExp) {
		return new XRegExp(pattern.source, flags);
	}

	pattern = pattern.replace(/\\\//g, '/');
	flags = (typeof flags === 'undefined') ? '' : String(flags);
	compiled = compile(pattern);

	this.captureNames = compiled.captureNames;
	this.nativ = nativ = new RegExp(compiled.pattern, flags);
	this.source = pattern;
	this.global = nativ.global;
	this.ignoreCase = nativ.ignoreCase;
	this.lastIndex = nativ.lastIndex;
	this.multiline = nativ.multiline;
}

/*
 * FIXME: We'd like this to be a "subclass" of the native RegExp for `instanceof` checks.
 * However, this prevents us from assigning a custom value to `this.source` as it's a readonly property that would be in the prototype.
 * We can't even assign an own property `this.source` to new instances of XRegExp to override the prototype chain property.
*/
XRegExp.prototype = {
	/**
	 * Adds named capture support (with backreferences returned as `result.name`), and fixes browser
	 * bugs in the native `RegExp.prototype.exec`.
	 *
	 * @private
	 * @param {String} str String to search.
	 * @returns {Array} Match array with named back-reference properties, or `null`.
	 */
	exec: function XRegExp$exec(str) {
		var i, match, name, lastIndex;

		lastIndex = this.lastIndex;

		if (match = this.nativ.exec(str)) {
			if (this.captureNames) {
				for (i = 1; i < match.length; ++i) {
					if (name = this.captureNames[i - 1]) {
						match[name] = match[i];
					}
				}
			}

			// Fix browsers that increment `lastIndex` after zero-length matches
			if (this.global && !match[0].length && this.nativ.lastIndex > match.index) {
				this.nativ.lastIndex = match.index;
			}
		}

		if (!this.global) {
			// Fixes IE, Opera bug (last tested IE 9, Opera 11.6)
			this.lastIndex = lastIndex;
		}
		else {
			this.lastIndex = this.nativ.lastIndex;
		}

		return match;
	},

	/**
	 * Fixes browser bugs in the native `RegExp.prototype.test`. Calling `XRegExp.install('natives')`
	 * uses this to override the native method.
	 *
	 * @private
	 * @param {String} str String to search.
	 * @returns {Boolean} Whether the regex matched the provided value.
	 */
	test: function XRegExp$test(str) {
		return !!this.nativ.test(str);
	}
};


/**
 * Compiles an XRegExp pattern to a native RegExp pattern.
 *
 * @param pattern The pattern that should be compiled to a native RegExp pattern.
 * @returns {Object} A plain object containing the compiled pattern and captureNames.
 */
function compile(pattern) {
	var cached, captures, compiled, pos;

	// Copy the argument behavior of `RegExp`
	pattern = (typeof pattern === 'undefined') ? '(?:)' : String(pattern);

	cached = cache[pattern];

	if (!cached) {
		captures = [];
		pos = 0;

		compiled = pattern.replace(/\((?!\?[!:=<])(?:(?:\?P|:)<(\w+)>)?/g, function(match, name) {
			if (name) {
				captures.push(name);
			}
			else {
				captures.push('$' + pos++);
			}

			return '(';
		});

		cached = cache[pattern] = {
			pattern: compiled,
			captureNames: (captures.length > 0) ? captures : null
		};
	}

	return {
		pattern: cached.pattern,
		captureNames: cached.captureNames
	};
}


/**
 * Escapes any regular expression meta-characters, for use when matching literal strings. The result can safely be
 * used at any point within a regex that uses any flags.
 *
 * @param {String} str String to escape.
 * @returns {String} String with regex characters escaped.
 */
function escape(str) {
	if (typeof str === 'undefined' || str === null) {
		throw new TypeError('Cannot convert null or undefined to object');
	}

	return str.replace(/[-[\]{}()*+?.,\\^$|#\s]/g, '\\$&');
}


/**
 * Empties the compiled XRegExp pattern cache.
 */
function flush() {
	cache = {};
}


module.exports = {
	XRegExp: XRegExp,

	compile: compile,
	escape: escape,
	flush: flush
};
