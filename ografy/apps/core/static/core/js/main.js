$(document).ready(function() {
	function getFilter() {
		var filters = [];
		$('#filters .active').each(function(i, el) {
			filters.push($(el).data('filter'));
		})

		return filters.join(',');
	}

	var $container = $('#isotope-container').isotope({
	  // options
	});

	// filter items on button click
	$('#filters').on( 'click', 'span', function() {
		$(this).toggleClass('active');
		var filterValue = getFilter();

		$container.isotope({ filter: filterValue });
	});
});
