'use strict';

const _ = require('lodash');


function initializeEndpointData(provider, connection, source, endpoint, population) {
	if (!connection.endpoint_data.hasOwnProperty(source)) {
		connection.endpoint_data[source] = {};
	}

	if (endpoint == null) {
		endpoint = provider.sources[source].mapping;
	}

	if (population == null) {
		population = provider.sources[source].population;
	}

	connection.endpoint_data[source][endpoint] = {};

	if (_.has(provider.endpoints[endpoint], 'parameters')) {
		_.each(provider.endpoints[endpoint].parameters, function(values, parameter) {
			if (values.hasOwnProperty('default')) {
				connection.endpoint_data[source][endpoint][parameter] = values.default;
			}
		});
	}

	_.forEach(provider.endpoints[endpoint].model.fields, function(values, field) {
		if (typeof values === 'object' && values.type === 'related' && (population === '*' || values.ref === population)) {
			initializeEndpointData(provider, connection, source, values.ref, '*');
		}
	});
}


module.exports = initializeEndpointData;
