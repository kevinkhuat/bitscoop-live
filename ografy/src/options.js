/*!
 * options v0.1.0
 *
 * Generates and manipulates options objects.
 *
 * Copyright 2014 Ografy, LLC
 *
 * Authors:
 *     Steven Berry
 */
var _ = require('lodash');

var oops = require('./oops');


/**
 * Placeholder.
 *
 * @param {Object} opts
 * @constructor
 */
function Options(opts) {
	this.update(opts);
}

Options.prototype = oops.proto(Options, {
	has: function Options$has(name) {
		return this.hasOwnProperty(name);
	},

	pop: function Options$pop(name) {
		var prop;

		if (this.hasOwnProperty(name)) {
			prop = this[name];
			delete this[name];

			return prop;
		}
	},

	update: function Options$update(ext) {
		oops.extend(this, ext);

		return this;
	}
});


/**
 * Creates an options object from a plain object.
 *
 * @param {Object} [obj] A plain object with key/values to map to the options object.
 * @returns {Object} An options object corresponding to the supplied plain object.
 */
function create(obj) {
	return (obj instanceof Options) ? obj : new Options(obj);
}


/**
 * Placeholder.
 *
 * @param opts
 * @param name
 */
function has(opts, name) {
	return Options.prototype.has.call(opts, name);
}


/**
 * Removes and returns the indicated property from an options object.
 *
 * @param {Object} opts The options object whose property will be stripped.
 * @param {String} name The name of the property to return and remove from the options object.
 * @returns {*} The value in the options object corresponding to the provided name key.
 */
function pop(opts, name) {
	return Options.prototype.pop.call(opts, name);
}


/**
 * Extends an object with new properties.
 *
 * New properties are iterated over and set on the `base` object. If a property with the same name already exists,
 * it will be overwritten with the property provided in the `ext` extension object.
 *
 * @param {Object} base The base object to extend.
 * @param {Object} opts The new object with properties that will extend or override properties on the `base` object.
 */
function popExtend(base, opts) {
	if (!(opts instanceof Options)) {
		opts = new Options(opts);
	}

	_.each(opts, function(d, name) {
		base[name] = pop(opts, name);
	});

	return base;
}


/**
 * Merges an options object onto another object. Freezes properties on the new object so that modifications to the
 * options object do not manifest onto the other object.
 *
 * @param {Object} opts The options object used for mapping.
 * @param {Object} obj The object on which to map options properties.
 */
function update(opts, obj) {
	return Options.prototype.update.call(opts, obj);
}


module.exports = {
	Options: Options,

	create: create,
	has: has,
	pop: pop,
	popExtend: popExtend,
	update: update
};
