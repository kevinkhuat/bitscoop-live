/**
 * Creates a random generator which will memoize generated keys to ensure uniqueness.
 *
 * If no generator function is supplied, `rand` will default to the built-in `uuid4` function.
 *
 * The supplied generator function should have a reasonably high entropy to minimize the chance for collision. If
 * the generator does NOT have enough entropy, there is a reasonable chance that an infinite loop will be
 * encountered.
 *
 * @param {Function} [rand] A generator function that produces random strings.
 * @returns {Function} The new generator function enhanced with memoization.
 */
function unique(rand) {
	var cache;

	rand = rand || uuid4;
	cache = {};

	return function() {
		var uid;

		do {
			uid = rand();
		}
		while (cache.hasOwnProperty(uid));

		cache[uid] = true;

		return uid;
	};
}


/**
 * Generates a UUID4-compliant random string.
 *
 * @returns {String} A UUID4-compliant random string.
 */
function uuid4() {
	return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(ch) {
		var rand, result;

		rand = (Math.random() * 16) | 0;
		result = (ch === 'x') ? rand : (rand & 0x3 | 0x8);

		return result.toString(16);
	});
}


module.exports = {
	unique: unique,
	uuid4: uuid4
};
