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
    itemSelector: '.iso-item',
	masonry: {
		columnWidth: 500
	}
	});

	// filter items on button click
	$('#filters').on( 'click', 'span', function() {
		$(this).toggleClass('active');
		var filterValue = getFilter();

		$container.isotope({ filter: filterValue });
	});

	$('.iso-item').on('click', function(){
	    $(this).toggleClass('big');
	    $container.isotope( 'layout' );
    });
});