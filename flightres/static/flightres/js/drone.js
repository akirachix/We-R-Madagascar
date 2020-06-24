
(function ($) {

  "use strict";

  $(document).ready(function () {

    var winwidth = $(window).width();
    if (winwidth <= 1024) {
      $('.drone-admin-wrapper').addClass('sidebar-collapse');
    }else{
      $('.drone-admin-wrapper').removeClass('sidebar-collapse');
    }
    $(window).resize(function(){
      if (winwidth <= 1024) {
        $('.drone-admin-wrapper').addClass('sidebar-collapse');
      }else{
        $('.drone-admin-wrapper').removeClass('sidebar-collapse');
      }
    })

    function popUp() {
      $('.common-button').on('click', function (e) {
        e.preventDefault();
        var targetId = $(this).attr('popup-link');
        $('#' + targetId).addClass('open');
      });
    }
    popUp();
    function formModal() {
      $('.modal-link').on('click', function () {
        var targetId = $(this).attr('modal-link');
        $('#' + targetId).addClass('open');
      });
    }
    formModal();
    function closePopup() {
      $('.popup-footer .common-button, .close-icon').on('click', function (e) {
        e.preventDefault();
        $(this).closest('.popup').removeClass('open');
      });
    }
    closePopup();
    function accMenu() {

      $('.acc-list').find('.acc-header').on('click', function () {
        // Adds Active Class
        $(this).toggleClass('active');
        // Expand or Collapse This Panel
        $(this).next().slideToggle('fast');
        // Hide The Other Panels
        $('.acc-body').not($(this).next()).slideUp('200');
        // Removes Active Class From Other Titles
        $('.acc-header').not($(this)).removeClass('active');
      });
    }
    accMenu();

    // for li a active
    // function filterDropdown() {
    //   $('.admin-aside-menu > li.is-submenu > a').on('click', function(e) {
    //     e.preventDefault();
    //     if($(this).next('ul.submenu').is(':visible')) {
    //         $(this).removeClass('active');
    //         $(this).next('ul.submenu').slideUp();
    //     } else {
    //         $('.admin-aside-menu > li.is-submenu > a').removeClass('active');
    //         $(this).addClass('active');
    //         $('.admin-aside-menu > li.is-submenu > a').next('ul.submenu').slideUp();
    //         $(this).next('ul.submenu').slideToggle();
    //     }
    //   });
    // }
    // filterDropdown();

    // for li active
    // function sidebarMenu() {
    // var $emenu = $('.admin-aside-menu');
    //   $emenu.find('li.is-submenu > a').on('click', function(e) {
    //     e.preventDefault();
    //     if($(this).next('ul.submenu').is(':visible')) {
    //         $(this).parent().removeClass('active');
    //         $(this).next('ul.submenu').slideUp();
    //     } else {
    //         $emenu.find('li.is-submenu').removeClass('active');
    //         $(this).parent().addClass('active');
    //         $emenu.find('li.is-submenu').children('ul.submenu').slideUp();
    //         $(this).next('ul.submenu').slideToggle();
    //     }
    //   });
    // }
    // sidebarMenu();

    function multipleMenu() {
      $(".admin-aside-menu > .is-submenu > a").click(function () {
        var e = $(this).next(".submenu")
          , a = ".admin-aside-menu > li.is-submenu > .submenu";
        0 === $(".minified-menu").length && ($(a).not(e).slideUp(function () {
          $(this).closest("li").removeClass("active")
        }),
          $(e).slideToggle(function () {
            var e = $(this).closest("li");
            $(e).hasClass("active") ? $(e).removeClass("active") : $(e).addClass("active")
          }))
      }),
        $(".admin-aside-menu > .is-submenu .submenu li.is-submenu > a").click(function () {
          if (0 === $(".minified-menu").length) {
            var e = $(this).next(".submenu");
            $(e).slideToggle()
          }
        });
    }
    multipleMenu();


    function toggleSidebar() {
      $('.admin-sidebar .toggle-sidebar').on('click', function (e) {
        e.preventDefault();
        $('.drone-admin-wrapper').toggleClass('sidebar-collapse');
      })
    }
    toggleSidebar();



    function selectToggle() {
      $('.custom-select .selected-item').on('click', function () {
        $(this).closest('.custom-select').toggleClass('show-dropdown');
      });
      $(document).on("click", function (event) {
        var $trigger = $(".custom-select");
        if ($trigger !== event.target && !$trigger.has(event.target).length) {
          $(".custom-select").removeClass("show-dropdown");
        }
      });
    }
    selectToggle();

    function customDropdown() {
      $('.custom-dropdown').on('click', function (e) {
        e.preventDefault();
        $(this).children('ul.custom-dropdown-menu').slideToggle(300);
      });

      $(document).mouseup(function (e) {
        var container = $(".custom-dropdown-menu");
        // If the target of the click isn't the container
        if (!container.is(e.target) && container.has(e.target).length === 0) {
          container.hide(300);
        }
      });

    }
    customDropdown();

    function moreOption() {
      $('.more-option a.more-vert').on('click', function (e) {
        e.preventDefault();
        $(this).closest('.more-option').find('ul.option-list').slideToggle(300);
      });

      $(document).mouseup(function (e) {
        var container = $(".option-list");
        // If the target of the click isn't the container
        if (!container.is(e.target) && container.has(e.target).length === 0) {
          container.hide(300);
        }
      });

    }
    moreOption();


    function customTab() {
      $('.sidebar-tab ul.custom-tab a').click(function () {
        var tab_id = $(this).attr('data-tab');

        $('.sidebar-tab ul.custom-tab li a').removeClass('current');
        $('.custom-tab-content .tab-item').removeClass('current');

        $(this).addClass('current');
        $("#" + tab_id).addClass('current');
      })
    }
    customTab();


    $('.tr-header').click(function () {
      $(this).toggleClass('active');
      $(this).nextUntil('.tr-header').css('display', function (i, v) {
        return this.style.display === 'table-row' ? 'none' : 'table-row';
      });
    });

    // FAQ Accordion
	$(function() {
		$('.accordion').find('.accordion-title').on('click', function(){
			// Adds Active Class
			$(this).toggleClass('active');
			// Expand or Collapse This Panel
			$(this).next().slideToggle('fast');
			// Hide The Other Panels
			$('.accordion-content').not($(this).next()).slideUp('fast');
			// Removes Active Class From Other Titles
			$('.accordion-title').not($(this)).removeClass('active');		
		});
	});

	// Tabs
	(function ($) {
		$('.tab ul.tabs').addClass('active').find('> li:eq(0)').addClass('current');
		$('.tab ul.tabs li a').on('click', function (g) {
			var tab = $(this).closest('.tab'), 
			index = $(this).closest('li').index();
			tab.find('ul.tabs > li').removeClass('current');
			$(this).closest('li').addClass('current');
			tab.find('.tab-content').find('div.tabs-item').not('div.tabs-item:eq(' + index + ')').slideUp();
			tab.find('.tab-content').find('div.tabs-item:eq(' + index + ')').slideDown();
			g.preventDefault();
		});
	})(jQuery);



    $("#upload").change(function (event) {
      readURL(this);
    });

    function readURL(input) {
      if (input.files && input.files[0]) {
        var reader = new FileReader();
        var filename = $("#upload").val();
        filename = filename.substring(filename.lastIndexOf('\\') + 1);
        reader.onload = function (e) {
          debugger;
          $('#preview').attr('src', e.target.result);
          $('#preview').hide();
          $('#preview').fadeIn(500);
          $('.custom-file-label').text(filename);
        }
        reader.readAsDataURL(input.files[0]);
      }
    }
  });
})(window.jQuery);

