
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
/* 
    function popUp() {
      $('.common-button').on('click', function (e) {
        e.preventDefault();
        var targetId = $(this).attr('popup-link');
        $('#' + targetId).addClass('open');
      });
    }
    popUp(); */
    function popUp_escalate() {
      $('.escalate-button').on('click', function (e) {
        e.preventDefault();
        var targetId = $(this).attr('popup-link');
        $('#' + targetId).addClass('open');
      });
    }
    popUp_escalate();

    function formModal() {
      $('.modal-link').on('click', function () {
        var targetId = $(this).attr('modal-link');
        $('#' + targetId).addClass('open');
        // $('.body-container').addClass('blur-bg');
      });
    }
    formModal();

    function closePopup() {
      $('.buttons .cancel-button, .close-icon').on('click', function (e) {
        e.preventDefault();
        $(this).closest('.popup').removeClass('open');
        // $('.body-container').removeClass('blur-bg');
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


    $(document).ready(function () {
      $('#admin-datatable').DataTable();
      $('.dataTables_length').addClass('bs-select');
    });
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

    function customTab1() {
      $('ul.tab-list li a').click(function () {
        var tab_id = $(this).attr('data-target');
  
        $('ul.tab-list li a').removeClass('current');
        $('.tab-content-holder').removeClass('current');
  
        $(this).addClass('current');
        $("#" + tab_id).addClass('current');
      })
    }
    customTab1();

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

  function tab_list_nav(){
    $('.tab-list li').on('click', 'a', function(){
      if($(this).closest('a').next().hasClass('current')){
        $('.tab-list a').removeClass('current');
    }
    else{
      $('.tab-list a').removeClass('current');
    }
    $(this).closest('a').addClass('current');
    })
  }
  tab_list_nav();

  function header_li(){
    $('.menu ul li').on('click', 'a', function(){
      if($(this).closest('a').next().hasClass('active')){
        $('.menu ul li a').removeClass('active');
    }
    else{
      $('.menu ul li a').removeClass('active');
    }
    $(this).closest('a').addClass('active');
    })
  }
  header_li();

/*   function tab_li(){
    $('#flight').hide();
    $('#img-gallery').hide();
    $(document).ready(function(){
        $('.tab-list li').on('click', 'a', function(e){
          e.preventDefault();
          $('#flight').hide();
          $('#img-gallery').hide();
          $('#location').hide();
          $($(this).attr("href")).show();
        })
    });
  }
  tab_li(); */

  function guidelines_li(){
    $('.nav-wrap').on('click', 'li', function(){
      if($(this).closest('li').next().hasClass('active')){
        $('.nav-wrap li').removeClass('active');
    }
    else{
      $('.nav-wrap li').removeClass('active');
    }
    $(this).closest('li').addClass('active');
    })
  }
  guidelines_li();

  function guideline_tab(){
    $('#categoryB').hide();
    $('#categoryC').hide();
    $('#categoryD').hide();
    $(document).ready(function(){
        $('.nav-wrap li').on('click', 'a', function(e){
          e.preventDefault();
          $('#categoryA').hide();
          $('#categoryB').hide();
          $('#categoryC').hide();
          $('#categoryD').hide();
          $($(this).attr("href")).show();
        })
    });
  }
  guideline_tab();

  function popup_info(){
    $('.guideline-popup').on('click','a.popup-info', function(e){
      e.preventDefault();
      $('.guideline-popup').addClass('open');
    });
    $('.guideline-popup').on('click','a.icon-close', function(e){
      e.preventDefault();
      $('.guideline-popup').removeClass('open');
    });

  }
  popup_info();
  //pie-chart
  var options = {
    series: [60, 30, 90],
    colors:['#00BCFF', '#FCBA15', '#3346D1'],
    chart: {
      width: '100%',
    type: 'donut',
  },
  labels: ['Recieved', 'Solved', 'Pending'],
 /*  responsive: [{
    breakpoint: 480,
    options: {
      chart: {
        height: 200,
      },
      legend: {
        position: 'right center'
      },
    }
  }] */
  };

  var chart = new ApexCharts(document.querySelector("#pie-chart"), options);
  chart.render();

// line-chart
var options = {
  series: [
    {
      name: "Total Requests",
      data: [200, 100, 200, 150, 150, 100, 100, 150, 200, 150, 200, 150]
    },
    {
      name: "Approved Requests",
      data: [300, 200, 300, 280, 200, 205, 150, 300, 400, 300, 500, 400]
    }
],
colors: ['#3346D1', '#00BCFF'],
  chart: {
  height: 370,
  type: 'line',
  zoom: {
    enabled: false
  }
},
responsive: [{
  breakpoint: 480,
  options: {
    chart: {
      height: 200,
    },
  },
}],
dataLabels: {
  enabled: false
},
stroke: {
  width: 2,
  curve: 'straight'
},
markers: {
  size: 5
},
grid: {
  row: {
    colors: ['transparent', 'transparent'], // takes an array which will be repeated on columns
    opacity: 0.5
  },
},
xaxis: {
  categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
}
};

var chart = new ApexCharts(document.querySelector("#line-chart"), options);
chart.render();

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

