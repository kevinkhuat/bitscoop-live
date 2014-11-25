function smokesignal() {
	'use strict';

	var clean_cache = {};

	function map(api_json, schema_mapping){
		//console.log(api_json);
		//console.log(schema_mapping);

		_.forIn(schema_mapping, function(val, key){

			switch (key) {
				case "Event":
					_mapEvents(api_json, schema_mapping[key]);
					break;
				case "Message":
					_mapMessages(api_json, schema_mapping[key]);
					break;
			}

		});

	}


	function _mapEvents(api_json, schema_mapping) {
		//console.log(api_json);
		//console.log(schema_mapping);

		var location = schema_mapping.data.split(/./);


	};

	function _mapMessages(api_json, schema_mapping){
		console.log(api_json);
		console.log(schema_mapping);


	};

	return {
		map: map
	};
}
