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
	});
	
	// FIXME: Scope this please.
	var filters = {};
	$settings.find('input[type="checkbox"]').each(function(i, el) {
		var selector, $el = $(el);
		
		filters[$el.data('filter')] = $el.is(':checked');
	}).first().trigger('change');
});