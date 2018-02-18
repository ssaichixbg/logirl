$(function() {
    (function () {
        var elements = $('.position-sticky');
        Stickyfill.add(elements);
    })();
});

var clickEvent = (function() {
  if ('ontouchstart' in document.documentElement === true)
    return 'touchstart';
  else
    return 'click';
})();

function replaceParam(key, value) {
  var params = window.location.search.substr(1).split('&');
  var found = false;
  for (var i = 0; i < params.length; i++) {
      if (params[i].indexOf(key) >= 0) {
          params[i] = key + '=' + value;
          found = true;
          break;
      }
  }
  if (!found) {
      params.push(key + '=' + value);
  }
  return window.location.pathname + '?' + params.join('&')
}