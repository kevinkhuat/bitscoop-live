/**
 * The base functionality and interface for a Filter. Not intended to be instantiated directly. Used for instanceof
 * checks on prototype chains to make sure that a Filter instance is actually a BaseFilter sub-class.
 *
 * @constructor
 */
function BaseFilter() {}

BaseFilter.prototype = {
	/**
	 * Placholder.
	 *
	 * @param {BaseModel|*} model The BaseModel constructor that is used to determine the filter statements based on the inherent field types.
	 * @returns {Function} A function that can be used in iteration over a set of Model instances to determine which should be filtered.
	 */
	toFunction: function BaseFilter$toFunction(model) {
		return new Function('return true;');
	},

	/**
	 * Placeholder.
	 *
	 * @returns {String}
	 */
	toString: function BaseFilter$toString() {
		return '';
	}
};


/**
 * Determines whether a test object is an instance of `BaseFilter` or any sub-class.
 *
 * @param {*} obj The object whose type to check.
 * @returns {Boolean} True if `obj` is an instance of `BaseFilter` or any sub-class thereof else false.
 */
function isFilter(obj) {
	return obj instanceof BaseFilter;
}


module.exports = {
	BaseFilter: BaseFilter,

	isFilter: isFilter
};
