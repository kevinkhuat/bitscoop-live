$(document).ready(function() {
	$('.waypoint').waypoint(function(e) {
		var sectionId, $active, $link, $this = $(this);
		
		sectionId = $this.attr('id');
		$link = $('a[href="#' + sectionId + '"]');
		$active = $('.steps > a.active').first();
		
		if ($active[0] !== $link[0]) {
			$active.removeClass('active');
			$link.addClass('active');
		}
	});
	
	$(document).delegate('.steps > a', 'click', function(e) {
		var href, $this = $(this);
		
		e.preventDefault();
		
		$('.steps > a.active').removeClass('active');
		$this.addClass('active');
		
		href = $this.attr('href');
		$.waypoints('disable');
		$(document.body).scrollTo(href, {
			offset: -65,
			duration: 150,
			onAfter: function() {
				$.waypoints('enable');
			}
		});
	});
});