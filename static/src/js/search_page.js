function getBootstrapBreakpoint(){
  var w = $(document).innerWidth();
  return (w < 768) ? 'xs' : ((w < 992) ? 'sm' : ((w < 1200) ? 'md' : 'lg'));
}

function createNewSearch() {
  searchPage = 0;
  $('.load-more-btn').hide();
  $('.no-more').hide();
}

function loadMore(callback) {
  // prevent loading at same time or destroyed
  var $loadMoreBtn = $('.load-more-btn');
  if ($loadMoreBtn.hidden || $loadMoreBtn.data('loading')) {
    return;
  }
  $loadMoreBtn.data('loading', true);

  // start loading
  var l = Ladda.create(document.querySelector('.load-more-btn'));
  l.start();
  $.ajax({
    url: replaceCurrentURLParam('page', searchPage + 1, '/search'),
    success: function (result) {
      if (result === '') {
        $loadMoreBtn.fadeOut();
        $('.no-more').fadeIn();
      }
      else {
        searchPage += 1;
        $(result).appendTo($('#search-result')).hide().fadeIn();
        Waypoint.refreshAll();
      }
    },
    error: function (xhr,status,error) {
      $('.net-error').fadeIn().delay(2000).fadeOut();
    },
    complete: function (xhr,status){
      l.stop();
      l.remove();
      $loadMoreBtn.data('loading', false);
    }
  })
}

function initLoadMoreButton() {
  $('.load-more-btn')
    .waypoint(
      function (direction) {
        if (searchPage > 0 && direction === 'down') {
          loadMore();
        }
      }, {
        offset: 'bottom-in-view'
      });
}

var searchPage = 0;

$(function() {
  // search bar slick
  (function () {
    if (getBootstrapBreakpoint() === 'xs' ) {
      var elements = $('.search-bar');
      Stickyfill.add(elements);
    }
  })();

  // enable tooltip
  (function () {
     $('[data-tooltip="true"]').tooltip({
       trigger: 'hover'
     });
  })();

  // bind events
  // order options click
  (function () {
    $('.order-option').on(clickEvent, function (e) {
      e.preventDefault();

      var order = $(this).data('type');
      location.href = replaceCurrentURLParam('order', order);
    })
  })();

  // load more
  (function () {
    var $moreBtn = $('.load-more-btn');
    $moreBtn.on(clickEvent, function (e) {
      e.preventDefault();

      loadMore();
    });

    initLoadMoreButton();
  })();
});