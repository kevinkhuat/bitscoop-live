function stream_layers(n, m, o) {
	if (arguments.length < 3) {
		o = 0;
	}

	function bump(a) {
		var i, w, x, y, z;

		x = 1 / (0.1 + Math.random());
		y = 2 * Math.random() - 0.5;
		z = 10 / (0.1 + Math.random());

		for (i = 0; i < m; i++) {
			w = (i / m - y) * z;
			a[i] += x * Math.exp(-w * w);
		}
	}

	return d3.range(n).map(function() {
		var i, a = [];

		for (i = 0; i < m; i++) {
			a[i] = o + o * Math.random();
		}

		for (i = 0; i < 5; i++) {
			bump(a);
		}

		return a.map(stream_index);
	});
}

function stream_waves(n, m) {
	return d3.range(n).map(function(i) {
		return d3.range(m).map(function(j) {
			var x;

			x = 20 * j / m - i / 3;

			return 2 * x * Math.exp(-0.5 * x);
		}).map(stream_index);
	});
}

function stream_index(d, i) {
	return {
		x: i,
		y: Math.max(0, d)
	};
}

function exampleData() {
	return stream_layers(3, 10 + Math.random() * 100, 0.1).map(function(data, i) {
		return {
			key: 'Dataset ' + i,
			values: data
		};
	});
}

function exampleData2() {
	return {"title":"Revenue","subtitle":"US$, in thousands","ranges":[150,225,300],"measures":[220],"markers":[250]};
}

function exampleData3() {
	return [
		{
			"key" : "Quantity" ,
			"bar": true,
			"values" : [ [ 1136005200000 , 1271000.0] , [ 1138683600000 , 1271000.0] , [ 1141102800000 , 1271000.0] , [ 1143781200000 , 0] , [ 1146369600000 , 0] , [ 1149048000000 , 0] , [ 1151640000000 , 0] , [ 1154318400000 , 0] , [ 1156996800000 , 0] , [ 1159588800000 , 3899486.0] , [ 1162270800000 , 3899486.0] , [ 1164862800000 , 3899486.0] , [ 1167541200000 , 3564700.0] , [ 1170219600000 , 3564700.0] , [ 1172638800000 , 3564700.0] , [ 1175313600000 , 2648493.0] , [ 1177905600000 , 2648493.0] , [ 1180584000000 , 2648493.0] , [ 1183176000000 , 2522993.0] , [ 1185854400000 , 2522993.0] , [ 1188532800000 , 2522993.0] , [ 1191124800000 , 2906501.0] , [ 1193803200000 , 2906501.0] , [ 1196398800000 , 2906501.0] , [ 1199077200000 , 2206761.0] , [ 1201755600000 , 2206761.0] , [ 1204261200000 , 2206761.0] , [ 1206936000000 , 2287726.0] , [ 1209528000000 , 2287726.0] , [ 1212206400000 , 2287726.0] , [ 1214798400000 , 2732646.0] , [ 1217476800000 , 2732646.0] , [ 1220155200000 , 2732646.0] , [ 1222747200000 , 2599196.0] , [ 1225425600000 , 2599196.0] , [ 1228021200000 , 2599196.0] , [ 1230699600000 , 1924387.0] , [ 1233378000000 , 1924387.0] , [ 1235797200000 , 1924387.0] , [ 1238472000000 , 1756311.0] , [ 1241064000000 , 1756311.0] , [ 1243742400000 , 1756311.0] , [ 1246334400000 , 1743470.0] , [ 1249012800000 , 1743470.0] , [ 1251691200000 , 1743470.0] , [ 1254283200000 , 1519010.0] , [ 1256961600000 , 1519010.0] , [ 1259557200000 , 1519010.0] , [ 1262235600000 , 1591444.0] , [ 1264914000000 , 1591444.0] , [ 1267333200000 , 1591444.0] , [ 1270008000000 , 1543784.0] , [ 1272600000000 , 1543784.0] , [ 1275278400000 , 1543784.0] , [ 1277870400000 , 1309915.0] , [ 1280548800000 , 1309915.0] , [ 1283227200000 , 1309915.0] , [ 1285819200000 , 1331875.0] , [ 1288497600000 , 1331875.0] , [ 1291093200000 , 1331875.0] , [ 1293771600000 , 1331875.0] , [ 1296450000000 , 1154695.0] , [ 1298869200000 , 1154695.0] , [ 1301544000000 , 1194025.0] , [ 1304136000000 , 1194025.0] , [ 1306814400000 , 1194025.0] , [ 1309406400000 , 1194025.0] , [ 1312084800000 , 1194025.0] , [ 1314763200000 , 1244525.0] , [ 1317355200000 , 475000.0] , [ 1320033600000 , 475000.0] , [ 1322629200000 , 475000.0] , [ 1325307600000 , 690033.0] , [ 1327986000000 , 690033.0] , [ 1330491600000 , 690033.0] , [ 1333166400000 , 514733.0] , [ 1335758400000 , 514733.0]]
		},
		{
			"key" : "Price" ,
			"values" : [ [ 1136005200000 , 71.89] , [ 1138683600000 , 75.51] , [ 1141102800000 , 68.49] , [ 1143781200000 , 62.72] , [ 1146369600000 , 70.39] , [ 1149048000000 , 59.77] , [ 1151640000000 , 57.27] , [ 1154318400000 , 67.96] , [ 1156996800000 , 67.85] , [ 1159588800000 , 76.98] , [ 1162270800000 , 81.08] , [ 1164862800000 , 91.66] , [ 1167541200000 , 84.84] , [ 1170219600000 , 85.73] , [ 1172638800000 , 84.61] , [ 1175313600000 , 92.91] , [ 1177905600000 , 99.8] , [ 1180584000000 , 121.191] , [ 1183176000000 , 122.04] , [ 1185854400000 , 131.76] , [ 1188532800000 , 138.48] , [ 1191124800000 , 153.47] , [ 1193803200000 , 189.95] , [ 1196398800000 , 182.22] , [ 1199077200000 , 198.08] , [ 1201755600000 , 135.36] , [ 1204261200000 , 125.02] , [ 1206936000000 , 143.5] , [ 1209528000000 , 173.95] , [ 1212206400000 , 188.75] , [ 1214798400000 , 167.44] , [ 1217476800000 , 158.95] , [ 1220155200000 , 169.53] , [ 1222747200000 , 113.66] , [ 1225425600000 , 107.59] , [ 1228021200000 , 92.67] , [ 1230699600000 , 85.35] , [ 1233378000000 , 90.13] , [ 1235797200000 , 89.31] , [ 1238472000000 , 105.12] , [ 1241064000000 , 125.83] , [ 1243742400000 , 135.81] , [ 1246334400000 , 142.43] , [ 1249012800000 , 163.39] , [ 1251691200000 , 168.21] , [ 1254283200000 , 185.35] , [ 1256961600000 , 188.5] , [ 1259557200000 , 199.91] , [ 1262235600000 , 210.732] , [ 1264914000000 , 192.063] , [ 1267333200000 , 204.62] , [ 1270008000000 , 235.0] , [ 1272600000000 , 261.09] , [ 1275278400000 , 256.88] , [ 1277870400000 , 251.53] , [ 1280548800000 , 257.25] , [ 1283227200000 , 243.1] , [ 1285819200000 , 283.75] , [ 1288497600000 , 300.98] , [ 1291093200000 , 311.15] , [ 1293771600000 , 322.56] , [ 1296450000000 , 339.32] , [ 1298869200000 , 353.21] , [ 1301544000000 , 348.5075] , [ 1304136000000 , 350.13] , [ 1306814400000 , 347.83] , [ 1309406400000 , 335.67] , [ 1312084800000 , 390.48] , [ 1314763200000 , 384.83] , [ 1317355200000 , 381.32] , [ 1320033600000 , 404.78] , [ 1322629200000 , 382.2] , [ 1325307600000 , 405.0] , [ 1327986000000 , 456.48] , [ 1330491600000 , 542.44] , [ 1333166400000 , 599.55] , [ 1335758400000 , 583.98]]
		}
	].map(function(series) {
		series.values = series.values.map(function(d) {
			return {
				x: d[0],
				y: d[1]
			};
		});

		return series;
	});
}

function exampleData4() {
	return [
		{
			"label": "Cash",
			"value": 29.765957771107
		},
		{
			"label": "Corporate Bonds",
			"value": 32.807804682612
		},
		{
			"label": "Equity",
			"value": 196.45946739256
		},
		{
			"label": "Index Futures",
			"value": 0.19434030906893
		},
		{
			"label": "Options",
			"value": 98.079782601442
		},
		{
			"label": "Preferred",
			"value": 13.925743130903
		},
		{
			"label": "Not Available",
			"value": 5.1387322875705
		}
	];
}

function exampleData5() {
	return [
		{
			"label": "Microsoft",
			"value": 23
		},
		{
			"label": "LinkedIn",
			"value": 15
		},
		{
			"label": "Facebook",
			"value": 16
		},
		{
			"label": "Twitter",
			"value": 8
		},
		{
			"label": "Other",
			"value": 38
		}
	];
}

function randomData(groups, points) {
	var i, j;

	var data = [];
	var shapes = ['circle', 'cross', 'triangle-up', 'triangle-down', 'diamond', 'square'];
	var random = d3.random.normal();

	for (i = 0; i < groups; i++) {
		data.push({
			key: 'Group ' + i,
			values: []
		});

		for (j = 0; j < points; j++) {
			data[i].values.push({
				x: random(),
				y: random(),
				size: Math.random()
			});
		}
	}

	return data;
}

function testData() {
	return stream_layers(3,128,.1).map(function(data, i) {
		return {
			key: 'Stream' + i,
			values: data
		};
	});
}



$(document).ready(function() {
	// Multibar
	nv.addGraph(function() {
		var chart = nv.models.multiBarChart();

		chart.xAxis.tickFormat(d3.format(',f'));
		chart.yAxis.tickFormat(d3.format(',.1f'));

		d3.select('#chart1').datum(exampleData()).transition().duration(275).call(chart);
		nv.utils.windowResize(chart.update);

		$('#chart1 text').attr('fill', '#FFF');

		return chart;
	});

	nv.addGraph(function() {
		var chart = nv.models.lineWithFocusChart();

		chart.xAxis.tickFormat(d3.format(',f'));
		chart.yAxis.tickFormat(d3.format(',.2f'));
		chart.y2Axis.tickFormat(d3.format(',.2f'));

		d3.select('#chart3')
			.datum(testData())
			.transition().duration(500)
			.call(chart);

		nv.utils.windowResize(chart.update);

		$('#chart3 text').attr('fill', '#FFF');

		return chart;
	});

	d3.json('/static/demo/data/stackedAreaData.json', function(data) {
		nv.addGraph(function() {
			var chart = nv.models.stackedAreaChart()
				.x(function(d) { return d[0]; })
				.y(function(d) { return d[1]; })
				.clipEdge(true);

			chart.xAxis.tickFormat(function(d) { return d3.time.format('%x')(new Date(d)) });
			chart.yAxis.tickFormat(d3.format(',.2f'));

			d3.select('#chart2').datum(data).transition().duration(500).call(chart);

			nv.utils.windowResize(chart.update);

			$('#chart2 text').attr('fill', '#FFF');

			return chart;
		});
	});


	nv.addGraph(function() {
		var testdata = exampleData3();
		var chart = nv.models.linePlusBarChart()
			.margin({
				top: 30,
				right: 60,
				bottom: 50,
				left: 70
			})
			.x(function(d,i) { return i; })
			.color(d3.scale.category10().range());

		chart.xAxis.tickFormat(function(d) {
			var dx = testdata[0].values[d] && testdata[0].values[d].x || 0;

			return d3.time.format('%x')(new Date(dx))
		});

		chart.y1Axis.tickFormat(d3.format(',f'));

		chart.y2Axis.tickFormat(function(d) {
			return '$' + d3.format(',f')(d);
		});

		chart.bars.forceY([0]);
		//chart.lines.forceY([0]);

		d3.select('#chart4')
			.datum(exampleData())
			.transition()
			.duration(500)
			.call(chart);

		nv.utils.windowResize(chart.update);

		$('#chart4 text').attr('fill', '#FFF');

		return chart;
	});

	nv.addGraph(function() {
		var chart = nv.models.scatterChart()
			.showDistX(true)
			.showDistY(true)
			.color(d3.scale.category10().range());

		chart.xAxis.tickFormat(d3.format('.02f'));
		chart.yAxis.tickFormat(d3.format('.02f'));

		d3.select('#chart5').datum(randomData(3,40)).transition().duration(500).call(chart);

		nv.utils.windowResize(chart.update);

		$('#chart5 text').attr('fill', '#FFF');

		return chart;
	});

	nv.addGraph(function() {
		var chart = nv.models.pieChart()
			.x(function(d) { return d.label; })
			.y(function(d) { return d.value; })
			.showLabels(true);

		d3.select("#chart6")
			.datum(exampleData5())
			.transition()
			.duration(1200)
			.call(chart);

		$('#chart6 text').attr('fill', '#FFF');

		return chart;
	});

	nv.addGraph(function() {
		var chart = nv.models.pieChart()
			.x(function(d) { return d.label; })
			.y(function(d) { return d.value; })
			.showLabels(true)
			.labelThreshold(0.05)
			.donut(true);

		d3.select("#chart7")
			.datum(exampleData4())
			.transition()
			.duration(1200)
			.call(chart);

		$('#chart7 text').attr('fill', '#FFF');

		return chart;
	});
});


$(document).ready(function() {
	var $content = $('#content');
	var $settings = $('#settings');

	$content.isotope({
		itemSelector: '.item',

		getSortData: {
			name: '.name',
			category: '[data-category]'
		},
	});

	$(window).on('keydown', function(e) {
		if (e.which === 192) {
			$(document.body).toggleClass('settings');
		}
	});

	$(document).on('click', '#menu-toggle', function(e) {
		$(document.body).toggleClass('settings');
	});

	$settings.on('change', 'input[type="checkbox"]', function(e) {
		var active, key, $this = $(this);

		e.stopPropagation();

		filters[$this.data('filter')] = $this.is(':checked');

		active = [];
		for (key in filters) {
			if (filters[key]) {
				active.push('.item' + key);
			}
		}

		console.log(active.join(','));

		$content.isotope({
			filter: (active.length === 0) ? ':not(*)' : active.join(',')
		});

		$('svg text').attr('fill', '#FFF');
	});

	// FIXME: Scope this please.
	var filters = {};
	$settings.find('input[type="checkbox"]').each(function(i, el) {
		var selector, $el = $(el);

		filters[$el.data('filter')] = $el.is(':checked');
	}).first().trigger('change');
});
