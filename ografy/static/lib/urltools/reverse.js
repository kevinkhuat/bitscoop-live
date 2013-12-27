function reverse(pattern) {
	var i, ch, escaped;
	
	var ESCAPE_MAPPINGS = {
		'A': undefined,
		'b': undefined,
		'B': undefined,
		'd': '0',
		'D': 'x',
		's': ' ',
		'S': 'x',
		'w': 'x',
		'W': '!',
		'Z': undefined,
	};

	var result = [];
	var nonCapturingGroups = [];
	var consumeNext = true;
	var numArgs = 0;
	
	pattern.replace(/./g, function(ch, ind) {
		console.log(ch);
		console.log(ind);
		
		return ch;
	});
}

/*
for ch in input_iter:
	if ch != '\\':
		yield ch, False
		continue
	ch = next(input_iter)
	representative = ESCAPE_MAPPINGS.get(ch, ch)
	if representative is None:
		continue
	yield representative, True
*/