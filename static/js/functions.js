(function ($) {
    "use strict";
    $(window).on('load', function () {
        $('.preloader').fadeOut(1000);
        
        // lightcase 
        $('a[data-rel^=lightcase]').lightcase();
        
        //Member Filter Isotop
        // init Isotope
        var $grid = $('.grid').isotope({
            itemSelector: '.project__item',
            layoutMode: 'fitRows',
        });

        // filter functions
        var filterFns = {
            // show if name ends with -ium
            ium: function () {
                var name = $(this).find('.name').text();
                return name.match(/ium$/);
            }
        };
        // bind filter button click
        $('.button-group').on('click', '.filter-btn', function () {
            var filterValue = $(this).attr('data-filter');
            // use filterFn if matches value
            filterValue = filterFns[filterValue] || filterValue;
            $grid.isotope({
                filter: filterValue
            });
        });
        // change is-checked class on buttons
        $('.button-group').each(function (i, buttonGroup) {
            var $buttonGroup = $(buttonGroup);
            $buttonGroup.on('click', '.filter-btn', function () {
                $buttonGroup.find('.is-checked').removeClass('is-checked');
                $(this).addClass('is-checked');
            });
        });
    })

    //progressbar
    window.addEventListener('DOMContentLoaded', function () {
        const circle = new CircularProgressBar('pie');
        setInterval(() => {
            const options = {
                index: 0,
                percent: Math.floor((Math.random() * 100) + 1)
            }
            circle.animationTo(options);
        }, 2000);
    });

    $(document).ready(function () {

        /*==== header Section Start here =====*/
        $("ul>li>ul").parent("li").addClass("menu-item-has-children");
        // drop down menu width overflow problem fix
        $('ul').parent('li').on('hover', function () {
            var menu = $(this).find("ul");
            var menupos = $(menu).offset();
            if (menupos.left + menu.width() > $(window).width()) {
                var newpos = -$(menu).width();
                menu.css({
                    left: newpos
                });
            }
        });
        $('.menu li a').on('click', function (e) {
            var element = $(this).parent('li');
            if (screen.width < 1200) {
                if (element.hasClass('open')) {
                    element.removeClass('open');
                    element.find('li').removeClass('open');
                    element.find('ul').slideUp(300, "swing");
                } else {
                    element.addClass('open');
                    element.children('ul').slideDown(300, "swing");
                    element.siblings('li').children('ul').slideUp(300, "swing");
                    element.siblings('li').removeClass('open');
                    element.siblings('li').find('li').removeClass('open');
                    element.siblings('li').find('ul').slideUp(300, "swing");
                }
            }
        })

        $('.header__ellepsis').on('click', function (e) {
            var element = $('.header__top');
            if (element.hasClass('open')) {
                element.removeClass('open');
                element.slideUp(300, "swing");
                $('.overlayTwo').removeClass('active');
            } else {
                element.addClass('open');
                element.slideDown(300, "swing");
                $('.overlayTwo').addClass('active');
            }
        });
        $('.header__bar').on('click', function () {
            $(this).toggleClass('active');
            $('.menu').toggleClass('active');
        })
        

        //Header
        var fixed_top = $("header");
        $(window).on('scroll', function () {
            if ($(this).scrollTop() > 100) {
                fixed_top.addClass("header-fixed");
            } else {
                fixed_top.removeClass("header-fixed");
            }
        });

        /*==== header Section End here =====*/

        // scroll up start here
        $(function () {
            $(window).on('scroll', function () {
                if ($(this).scrollTop() > 300) {
                    $('.scrollToTop').css({
                        'bottom': '2%',
                        'opacity': '1',
                        'transition': 'all .5s ease'
                    });
                } else {
                    $('.scrollToTop').css({
                        'bottom': '-30%',
                        'opacity': '0',
                        'transition': 'all .5s ease'
                    })
                }
            });

            //Click event to scroll to top
            $('a.scrollToTop').on('click', function () {
                $('html, body').animate({
                    scrollTop: 0
                }, 500);
                return false;
            });
        });

        
        //Odometer
        $(".odometer").each(function () {
            $(this).isInViewport(function (status) {
            if (status === "entered") {
                for (var i = 0; i < document.querySelectorAll(".odometer").length; i++) {
                var el = document.querySelectorAll('.odometer')[i];
                el.innerHTML = el.getAttribute("data-odometer-final");
                }
            }
            });
        });


        // Banner slider start here
        var swiper = new Swiper('.banner__slider', {
            slidesPerView: 1,
            spaceBetween: 50,
            speed: 1200,
            effect: "fade",
            autoplay: {
                delay: 5000,
                disableOnInteraction: false,
            },
            loop: true
        });
        var swiper = new Swiper('.banner__slider__one', {
            slidesPerView: 1,
            speed: 1200,
            autoplay: {
                delay: 5000,
                disableOnInteraction: false,
            },
            loop: true
        });
        var swiper = new Swiper('.banner__slider__two', {
            slidesPerView: 1,
            speed: 1200,
            autoplay: {
                delay: 5000,
                disableOnInteraction: false,
            },
            loop: true
        });

        // Testimonial slider start here
        var swiper = new Swiper('.testimonial__slider', {
            slidesPerView: 1,
            spaceBetween: 50,
            speed: 1200,
            navigation: {
                nextEl: '.testimonial__prev',
                prevEl: '.testimonial__next',
            },
            autoplay: {
                delay: 5000,
                disableOnInteraction: false,
            },
            loop: true
        });
        var swiper = new Swiper('.testimonial__slider__two', {
            slidesPerView: 2,
            spaceBetween: 80,
            speed: 1500,
            autoplay: {
                delay: 5000,
                disableOnInteraction: false,
            },
            breakpoints: {
				991: {
					slidesPerView: 1,
				},
			},
            loop: true,
        });
        var swiper = new Swiper('.testimonial__slider__three', {
            slidesPerView: 2,
            spaceBetween: 30,
            speed: 1500,
            direction: "vertical",
            autoplay: {
                delay: 5000,
                disableOnInteraction: false,
            },
            breakpoints: {
				480: {
					slidesPerView: 1,
				},
			},
            loop: true,
        });
        var swiper = new Swiper('.testimonial__slider__four', {
            slidesPerView: 2,
            spaceBetween: 30,
            speed: 1500,
            autoplay: {
                delay: 5000,
                disableOnInteraction: false,
            },
            breakpoints: {
				991: {
					slidesPerView: 1,
				},
			},
            loop: true,
        });


        // feature
        var swiper = new Swiper('.feature__slider', {
            slidesPerView: 6,
            spaceBetween: 30,
            speed: 1500,
            autoplay: {
                delay: 5000,
                disableOnInteraction: false,
            },
            breakpoints: {
				991: {
					slidesPerView: 2,
                    spaceBetween: 15,
				},
				1199: {
					slidesPerView: 3,
				},
				1440: {
					slidesPerView: 4,
				},
			},
            loop: true,
        });

        // Project slider start here
        var swiper = new Swiper('.project__slider', {
            slidesPerView: 5,
            spaceBetween: 20,
            speed: 1200,
            autoplay: {
                delay: 2500,
                disableOnInteraction: false,
            },
            loop: true,
            breakpoints: {
				480: {
					slidesPerView: 1,
				},
				992: {
					slidesPerView: 2,
				},
				1440: {
					slidesPerView: 4,
				},
			},
        });


        // sponsor slider start here
        var swiper = new Swiper('.sponsor__slider', {
            slidesPerView: 5,
            spaceBetween: 20,
            speed: 1200,
            autoplay: {
                delay: 3500,
                disableOnInteraction: false,
            },
            loop: true,
            breakpoints: {
				480: {
					slidesPerView: 2,
				},
				992: {
					slidesPerView: 3,
				},
				1440: {
					slidesPerView: 4,
				},
			},
        });


        // sponsor slider start here
        var swiper = new Swiper('.service__slider', {
            slidesPerView: 3,
            spaceBetween: 20,
            speed: 1200,
            autoplay: {
                delay: 3500,
                disableOnInteraction: false,
            },
            loop: true,
            breakpoints: {
				480: {
					slidesPerView: 1,
				},
				992: {
					slidesPerView: 2,
				},
			},
            pagination: {
                el: ".service__pagination",
                clickable: true,
            },
        });


        


        // shop cart + - start here
        var CartPlusMinus = $('.cart-plus-minus');
        $(".qtybutton").on("click", function() {
            var $button = $(this);
            var oldValue = $button.parent().find("input").val();
            if ($button.text() === "+") {
                var newVal = parseFloat(oldValue) + 1;
            } else {
                if (oldValue > 0) {
                    var newVal = parseFloat(oldValue) - 1;
                } else {
                    newVal = 1;
                }
            }
            $button.parent().find("input").val(newVal);
        });

        // shop sidebar menu
        $(".shop-menu>li>ul").parent("li").addClass("catmenu-item-has-children");
        $('.shop-menu li a').on('click', function (e) {
            var element = $(this).parent('li');
            if (element.hasClass('open')) {
                element.removeClass('open');
                element.find('li').removeClass('open');
                element.find('ul').slideUp(300, "swing");
            } else {
                element.addClass('open');
                element.children('ul').slideDown(300, "swing");
                element.siblings('li').children('ul').slideUp(300, "swing");
                element.siblings('li').removeClass('open');
                element.siblings('li').find('li').removeClass('open');
                element.siblings('li').find('ul').slideUp(300, "swing");
            }
        })

        // product view mode change js
        $(function() {
            $('.product-view-mode').on('click', 'a', function (e) {
                e.preventDefault();
                var shopProductWrap = $('.shop-product-wrap');
                var viewMode = $(this).data('target');
                $('.product-view-mode a').removeClass('active');
                $(this).addClass('active');
                shopProductWrap.removeClass('grid list').addClass(viewMode);
            });
        });

        // model option start here
        $(function() {
            $('.view-modal').on('click', function () {
                $('.modal').addClass('show');
            });
            $('.close').on('click', function () {
                $('.modal').removeClass('show');
            });
        });
        // product single thumb slider
        $(function() {
            var galleryThumbs = new Swiper('.pro-single-thumbs', {
                spaceBetween: 10,
                slidesPerView: 3,
                loop: true,
                freeMode: true,
                loopedSlides: 1,
                watchSlidesVisibility: true,
                watchSlidesProgress: true,
                navigation: {
                nextEl: '.pro-single-next',
                prevEl: '.pro-single-prev',
                },
            });
            var galleryTop = new Swiper('.pro-single-top', {
                spaceBetween: 10,
                loop:true,
                loopedSlides: 1,
                thumbs: {
                    swiper: galleryThumbs,
                },
            });
        });
        
        //Review Tabs
        $('ul.review-nav').on('click', 'li', function (e) {
            e.preventDefault();
            var reviewContent = $('.review-content');
            var viewRev = $(this).data('target');
            $('ul.review-nav li').removeClass('active');
            $(this).addClass('active');
            reviewContent.removeClass('review-content-show description-show').addClass(viewRev);
        });


    });
    
    //Odometer
    $(".app__content ul li").each(function () {
        $(this).isInViewport(function (status) {
        if (status === "entered") {
            for (var i = 0; i < document.querySelectorAll(".odometer").length; i++) {
            var el = document.querySelectorAll('.odometer')[i];
            el.innerHTML = el.getAttribute("data-odometer-final");
            }
        }
        });
    });

    //contact form js
    $(function () {
        var form = $('#contact-form');
        var formMessages = $('.form-message');
        $(form).submit(function (e) {
            e.preventDefault();
            var formData = $(form).serialize();
            $.ajax({
                type: 'POST',
                url: $(form).attr('action'),
                data: formData
            })
            .done(function (response) {
                $(formMessages).removeClass('error');
                $(formMessages).addClass('success');
                $(formMessages).text(response);
                $('#contact-form input, #contact-form textarea').val('');
            })
            .fail(function (data) {
                $(formMessages).removeClass('success');
                $(formMessages).addClass('error');
                if (data.responseText !== '') {
                    $(formMessages).text(data.responseText);
                } else {
                    $(formMessages).text('Oops! An error occured and your message could not be sent.');
                }
            });
        });
    });

    

}(jQuery));