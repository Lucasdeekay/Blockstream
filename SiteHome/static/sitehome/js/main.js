$(document).ready(function () {
	"use strict"; // start of use strict

	/*==============================
	Header
	==============================*/
	$(window).on('scroll', function () {
		if ($(this).scrollTop() > 0){
			$('.header').addClass('header--active');
		} else {
			$('.header').removeClass('header--active');
		}
	});
	$(window).trigger('scroll');

	/*==============================
	Mobile navigation
	==============================*/
	$('.header__menu').on('click', function() {
		$(this).toggleClass('header__menu--active');
		$('.header__nav').toggleClass('header__nav--active');
	});

	/*==============================
	Partners slider
	==============================*/
	$('.partners__slider').owlCarousel({
		mouseDrag: false,
		touchDrag: true,
		dots: false,
		loop: true,
		autoplay: true,
		autoplayTimeout: 5000,
		smartSpeed: 800,
		autoplayHoverPause: true,
		responsive: {
			0: {
				items: 2,
				margin: 20
			},
			576: {
				items: 3,
				margin: 20
			},
			768: {
				items: 4,
				margin: 20
			},
			992: {
				items: 5,
				margin: 25
			},
			1200: {
				items: 6,
				margin: 30
			}
		}
	});

	/*==============================
	Testimonial slider
	==============================*/
	$('.testimonial-slider').owlCarousel({
		mouseDrag: true,
		touchDrag: true,
		dots: true,
		loop: true,
		autoplay: true,
		autoplayTimeout: 6000,
		smartSpeed: 800,
		autoplayHoverPause: true,
		margin: 30,
		items: 1,
		autoWidth: true,
		autoHeight: true,
		center: true,
		responsive: {
			1200: {
				autoHeight: false,
				mouseDrag: false,
			},
			1440: {
				autoHeight: false,
				mouseDrag: false,
				margin: 60,
			}
		}
	});

	/*==============================
	Section background img
	==============================*/
	$('.section--bg').each(function(){
		if ($(this).attr('data-bg')){
			$(this).css({
				'background': 'url(' + $(this).data('bg') + ')',
				'background-position': 'center center',
				'background-repeat': 'no-repeat',
				'background-size': 'cover'
			});
		}
	});

	/*==============================
	Modal
	==============================*/
	$('.section__video').magnificPopup({
		disableOn: 0,
		type: 'iframe',
		mainClass: 'mfp-fade',
		removalDelay: 200,
		preloader: false,
		callbacks: {
			open: function() {
				if ($(window).width() > 1199) {
					$('.header').css('margin-right',  getScrollBarWidth() + "px");
				}
			},
			close: function() {
				if ($(window).width() > 1199) {
					$('.header').css('margin-right', 0);
				}
			},
		}
	});

	function getScrollBarWidth () {
		var $outer = $('<div>').css({visibility: 'hidden', width: 100, overflow: 'scroll'}).appendTo('body'),
			widthWithScroll = $('<div>').css({width: '100%'}).appendTo($outer).outerWidth();
		$outer.remove();
		return 100 - widthWithScroll;
	};

	/*==============================
	Canvas
	==============================*/
	if ($('.home__particles').length) {
		VANTA.NET({
			el: "#canvas",
			mouseControls: false,
			touchControls: false,
			gyroControls: false,
			minHeight: 200.00,
			minWidth: 200.00,
			scale: 1.00,
			scaleMobile: 1.00,
			color: 0xCDDCED,
			backgroundColor: 0xffffff,
			points: 13.00,
			maxDistance: 25.00,
			spacing: 21.00
		})
	}

	if ($('.sign__particles').length) {
		VANTA.NET({
			el: "#canvas",
			mouseControls: false,
			touchControls: false,
			gyroControls: false,
			minHeight: 200.00,
			minWidth: 200.00,
			scale: 1.00,
			scaleMobile: 1.00,
			color: 0xCDDCED,
			backgroundColor: 0xf4f9fe,
			points: 13.00,
			maxDistance: 25.00,
			spacing: 21.00
		})
	}

	if ($('.section__particles').length) {
		VANTA.NET({
			el: "#canvas",
			mouseControls: false,
			touchControls: false,
			gyroControls: false,
			minHeight: 200.00,
			minWidth: 200.00,
			scale: 1.00,
			scaleMobile: 1.00,
			color: 0xCDDCED,
			backgroundColor: 0xf4f9fe,
			points: 17.00,
			maxDistance: 25.00,
			spacing: 21.00,
		})
	}

	/*============= Message Tab =============*/
	$('.delete').click(function(){
	    $('#suc-sec').hide();
	    $('#err-sec').hide();
	});

	$('#suc-sec').slideToggle();
	$('#err-sec').slideToggle();
});