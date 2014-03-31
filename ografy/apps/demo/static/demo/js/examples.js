$(document).ready(function() {
	var svg, svg2, svg4, svg5;
	var data, data2, data4, data5;

	svg = dimple.newSvg('#chartContainer', 600, 400);
	data = $('#chartContainer').data('source');
	d3.tsv(data, function(data) {
		var chart = new dimple.chart(svg, data);
		chart.setBounds(70, 30, 510, 330)
		chart.addMeasureAxis('x', 'Total');
		chart.addMeasureAxis('y', 'Number of Items Purchased');
		chart.addMeasureAxis('z', 'Hours Spent Shopping');
		chart.addSeries(['Month', 'Merchant'], dimple.plot.bubble);
		chart.addLegend(240, 10, 360, 20, 'right');
		chart.draw(4000);
	});

	svg2 = dimple.newSvg('#chartContainer2', 600, 400);
	data2 = $('#chartContainer2').data('source');
	d3.tsv(data2, function(data) {
		var chart, y;
		chart = new dimple.chart(svg2, data);
		chart.setBounds(75, 30, 500, 330)
		chart.addPctAxis('x', 'Messages');
		y = chart.addCategoryAxis('y', 'Date');
		y.addOrderRule('Date');
		chart.addSeries('Person', dimple.plot.bar);
		chart.addLegend(100, 10, 510, 20, 'right');
		chart.draw(4000);
	});

	svg4 = dimple.newSvg('#chartContainer4', 600, 400);
	data4 = $('#chartContainer4').data('source');
	d3.tsv(data4, function(data) {
		var chart, x;
		chart = new dimple.chart(svg4, data);
		chart.setBounds(60, 30, 520, 320);
		x = chart.addCategoryAxis('x', 'Day');
		x.addOrderRule('Date');
		chart.addPctAxis('y', 'Percentage');
		chart.addSeries('Action', dimple.plot.bar);
		chart.addLegend(10, 10, 600, 20, 'right');
		chart.draw(4000);
	});

	svg5 = dimple.newSvg('#chartContainer5', 600, 400);
	data5 = $('#chartContainer5').data('source');
	d3.tsv(data5, function(data) {
		var chart, x;
		chart = new dimple.chart(svg5, data);
		chart.setBounds(60, 30, 520, 305);
		x = chart.addTimeAxis('x', 'Date', '%m/%d/%Y', '%m/%y');
		x.addOrderRule('Date');
		x.timePeriod = d3.time.months;
		chart.addMeasureAxis('y', 'Mentions and Likes');
		chart.addSeries('Service', dimple.plot.line);
		chart.addLegend(90, 10, 500, 20, 'right');
		chart.draw(4000);
	});
});
