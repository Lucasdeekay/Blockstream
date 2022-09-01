$(function(){

	/*============= Transaction Tab =============*/
	$('#withdrawal-table').hide();
	$('#others-table').hide();

	$('#wdr-btn').click(function(){
	    $('#withdrawal-table').show();
	    $('#wdr-btn').addClass('is-active');
	    $('#deposit-table').hide();
	    $('#dep-btn').removeClass('is-active');
	    $('#others-table').hide();
	    $('#oth-btn').removeClass('is-active');
	});
	$('#oth-btn').click(function(){
	    $('#others-table').show();
	    $('#oth-btn').addClass('is-active');
	    $('#withdrawal-table').hide();
	    $('#wdr-btn').removeClass('is-active');
	    $('#deposit-table').hide();
	    $('#dep-btn').removeClass('is-active');
	});
	$('#dep-btn').click(function(){
	    $('#deposit-table').show();
	    $('#dep-btn').addClass('is-active');
	    $('#withdrawal-table').hide();
	    $('#wdr-btn').removeClass('is-active');
	    $('#others-table').hide();
	    $('#oth-btn').removeClass('is-active');
	});
	/*============= Settings Tab =============*/
	$('#security-sec').hide();
	$('#others-sec').hide();

	$('#security-btn').click(function(){
	    $('#security-sec').show();
	    $('#security-btn').addClass('is-active');
	    $('#personal-sec').hide();
	    $('#personal-btn').removeClass('is-active');
	    $('#others-sec').hide();
	    $('#other-btn').removeClass('is-active');
	});
	$('#other-btn').click(function(){
	    $('#others-sec').show();
	    $('#other-btn').addClass('is-active');
	    $('#security-sec').hide();
	    $('#security-btn').removeClass('is-active');
	    $('#personal-sec').hide();
	    $('#personal-btn').removeClass('is-active');
	});
	$('#personal-btn').click(function(){
	    $('#personal-sec').show();
	    $('#personal-btn').addClass('is-active');
	    $('#security-sec').hide();
	    $('#security-btn').removeClass('is-active');
	    $('#others-sec').hide();
	    $('#other-btn').removeClass('is-active');
	});

	/*============= Admin Tab =============*/
	$('#withTable').hide();
	$('#cliTable').hide();
	$('#depoTable').hide();

	$('#withBtn').click(function(){
	    $('#withTable').show();
	    $('#withBtn').addClass('is-active');
	    $('#depoTable').hide();
	    $('#depoBtn').removeClass('is-active');
	    $('#cliTable').hide();
	    $('#cliBtn').removeClass('is-active');
	    $('#clientTable').hide();
	    $('#clientBtn').removeClass('is-active');
	});
	$('#depoBtn').click(function(){
	    $('#depoTable').show();
	    $('#depoBtn').addClass('is-active');
	    $('#withTable').hide();
	    $('#withBtn').removeClass('is-active');
	    $('#cliTable').hide();
	    $('#cliBtn').removeClass('is-active');
	    $('#clientTable').hide();
	    $('#clientBtn').removeClass('is-active');
	});
	$('#cliBtn').click(function(){
	    $('#cliTable').show();
	    $('#cliBtn').addClass('is-active');
	    $('#depoTable').hide();
	    $('#depoBtn').removeClass('is-active');
	    $('#withTable').hide();
	    $('#withBtn').removeClass('is-active');
	    $('#clientTable').hide();
	    $('#clientBtn').removeClass('is-active');
	});
	$('#clientBtn').click(function(){
	    $('#clientTable').show();
	    $('#clientBtn').addClass('is-active');
	    $('#depoTable').hide();
	    $('#depoBtn').removeClass('is-active');
	    $('#withTable').hide();
	    $('#withBtn').removeClass('is-active');
	    $('#cliTable').hide();
	    $('#cliBtn').removeClass('is-active');
	});

	/*============= Message Tab =============*/
	$('.delete').click(function(){
	    $('#suc-sec').hide();
	    $('#err-sec').hide();
	});

	/*============= Image Lazy Loading =============*/
	new LazyLoad({
	    elements_selector: ".lazy", // class to apply to
	    threshold: 300 // pixel threshold
	});
});