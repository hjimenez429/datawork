$(document).ready(function() {
	$('.step-btn').click(function() {
		$('.step-active').removeClass('step-active');
		$(this).addClass('step-active');
		const id = $(this).data('step');
		
		$('.active').fadeOut('slow', function() {
			$(this).removeClass('active');
			$('.step-' + id).fadeIn('slow', function() {
				$(this).addClass('active');
			});			
		});
	});
	$('.upd').change(function() {
      $.ajax({
        url: 'http://127.0.0.1:8000/update/' + $('#pt').val() + '/' + $('#ag').val() + '/',
        success: function(result){
          $('#dv').html(result.udD);
          $("head").append(result.udS);
      }});
    });

    $('.upd').change();
});

