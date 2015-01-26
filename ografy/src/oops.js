var _ = require('lodash');


if (typeof Object.create === 'undefined') {
	Object.create = function(proto) {
		function F() {}
		F.prototype = proto;

		return new F();
	};
}


/**
 * Instantiates a new prototype from a base constructor. Applies the constructor to the new prototype if arguments
 * are supplied. This functionality is typically used if the base constructor is intended as a base constructor and
 * the constructor itself establishes default values on the resulting prototype.
 *
 * @private
 * @param {Function|Object} constructor The base constructor
 * @param {Array} [args] An array of arguments to pass into the base constructor. If not specified then the base constructor is not called.
 * @returns {Object} The derived prototype.
 */
function construct(constructor, args) {
	var proto;

	constructor = constructor || null;

	if (constructor instanceof Function) {
		proto = Object.create(constructor.prototype);

		if (typeof args !== 'undefined') {
			constructor.apply(proto, args);
		}
	}
	else {
		proto = Object.create(constructor);
	}

	return proto;
}


/**
 * Returns the constructor of an object instance or the constructor function itself. A constructor function will
 * only be obtained for object types. e.g.:
 *
 *   >> function F() {}
 *   >> F.prototype = oops.proto(F, { num: 6 });
 *   >> function G() {}
 *   >> G.prototype = oops.proto(G, F, { test: 'george' });
 *
 *   >> oops.constructor(new F())
 *   << function F() { ... }
 *
 *   >> oops.constructor(new G())
 *   << function G() { ... }
 *
 *   >> oops.constructor(F)
 *   << function F() { ... }
 *
 *   >> oops.constructor(G)
 *   << function G() { ... }
 *
 * @param {Object|Function} obj The object instance of constructor function whose constructor will be obtained.
 * @returns {Object} The constructor if it exists else `null`.
 */
function constructor(obj) {
	var proto;

	if (!obj) {
		return null;
	}

	proto = (typeof obj === 'function') ? obj.prototype : Object.getPrototypeOf(obj);

	if (proto && proto.constructor) {
		return proto.constructor;
	}

	return null;
}


/**
 * Extends an object with new properties.
 *
 * New properties are iterated over and set on the `base` object. If a property with the same name already exists,
 * it will be overwritten with the property provided in the `ext` extension object.
 *
 * @param {Object} base The base object to extend.
 * @param {Object} ext The new object with properties that will extend or override properties on the `base` object.
 */
function extend(base, ext) {
	_.each(ext, function(d, i) {
		base[i] = d;
	});
}


/**
 * Returns the value corresponding to the nested property name on the object. Nested property names must be
 * delimited with the '.' character in accordance with standard JavaScript syntax.
 *
 * @param {Object} obj The object from which to retrieve the specified property.
 * @param {String} locator The optionally delimited nested property name.
 * @returns {*} The value in the object corresponding to the provided complex property name.
 */
function locate(obj, locator) {
	var i, start, token;

	if (locator === null || locator === '' || typeof locator === 'undefined') {
		return obj;
	}

	locator = locator.toString();
	start = -1;

	// We want to avoid using String.prototype.split to save Array instantiation overhead. We would also like to
	// avoid repeated indexOf calls to keep this method as fast as possible.
	for (i = 0; i < locator.length; i++) {
		if (locator.charAt(i) === '.') {
			token = locator.slice(start + 1, i);
			start = i;
			obj = obj[token];
		}
	}

	if (start <= locator.length) {
		token = locator.slice(start + 1, i);
		obj = obj[token];
	}

	return obj;
}


/**
 * Merges properties from N Object arguments onto a single shallow-copied object. Duplicate keys will be always be
 * overridden by subsequent argument objects.
 *
 * @returns {Object} An object with merged key/value pairs.
 */
function merge() {
	var obj;

	obj = {};

	_.each(arguments, function(d, i) {
		extend(obj, d);
	});

	return obj;
}


/**
 * Returns the parent constructor of an object instance or constructor function. A constructor function will only be
 * obtained for object types. e.g.:
 *
 *   >> function F() {}
 *   >> F.prototype = oops.proto(F, { num: 6 });
 *   >> function G() {}
 *   >> G.prototype = oops.proto(G, F, { test: 'george' });
 *
 *   >> oops.parent(new F())
 *   << function Object() { ... }
 *
 *   >> oops.parent(new G())
 *   << function F() { ... }
 *
 *   >> oops.parent(F)
 *   << function Object() { ... }
 *
 *   >> oops.parent(G)
 *   << function F() { ... }
 *
 * @param {Object|Function} inst The object instance of constructor function whose parent constructor will be obtained.
 * @returns {Function} The parent constructor if it exists else `null`.
 */
function parent(inst) {
	var constructor, proto, type;

	constructor = null;
	type = typeof inst;

	if ((type === 'object' || type === 'function') && inst) {
		proto = (inst instanceof Function) ? inst.prototype : Object.getPrototypeOf(inst);

		if (proto) {
			proto = Object.getPrototypeOf(proto);

			if (proto) {
				constructor = proto.constructor;

				if (!(constructor instanceof Function)) {
					throw new Error('Expected constructor function on object prototype');
				}

				if (constructor === inst.constructor) {
					constructor = null;
				}
			}
		}
	}

	return constructor;
}


/**
 * Returns the prototype of the parent constructor of an object instance or constructor function. A constructor
 * function will only be obtained for object types.
 *
 * @param {Object|Function} inst The object instance of constructor function whose parent constructor prototype will be obtained.
 * @returns {Object} The parent constructor prototype if it exists else `null`.
 */
function parentProto(inst) {
	var constructor;

	constructor = parent(inst);

	return (constructor === null) ? constructor : constructor.prototype;
}


/**
 * Extends a base constructor into a new prototype. Establishes and maintains a prototype chain so that
 * non-overridden properties are inherited from parent class prototypes.
 *
 * Normal `instanceof` behavior is preserved. e.g.:
 *
 *   >> function F() {}
 *   >> F.prototype = oops.proto(F, { num: 6 });
 *   >> function G() {}
 *   >> G.prototype = oops.proto(G, F, { test: 'george' });
 *
 *   >> new G() instanceof G
 *   << true
 *   >> new G() instanceof F
 *   << true
 *
 * @param {Function} base The base constructor used to set the `constructor` property on the prototype.
 * @param {Function|Object} parent The parent constructor that will be used to instantiate the new prototype.
 * @param {Object} [ext] An extension object containing key/value pairs that either override or extend the prototype of the `base` constructor.
 * @returns {Object} The derived prototype.
 */
function proto(base, parent, ext) {
	var obj;

	obj = construct(parent);
	extend(obj, ext);

	if (typeof base !== 'undefined' && base !== null) {
		obj.constructor = base;
	}

	return obj;
}


module.exports = {
	construct: construct,
	constructor: constructor,
	extend: extend,
	locate: locate,
	merge: merge,
	parent: parent,
	parentProto: parentProto,
	proto: proto
};
