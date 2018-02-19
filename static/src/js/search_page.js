function getBootstrapBreakpoint(){
  var w = $(document).innerWidth();
  return (w < 768) ? 'xs' : ((w < 992) ? 'sm' : ((w < 1200) ? 'md' : 'lg'));
}

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
      location.href = replaceParam('order', order)
    })
  })();
});