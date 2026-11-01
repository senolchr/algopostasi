// Algoritma Postası — gönderileri yayın saatine göre aç/kapat, videoyu tıklayınca yükle.
(function () {
  var preview = /[?&]onizleme=1/.test(location.search);
  var now = Date.now();
  var isOpen = function (el) { return preview || Date.parse(el.getAttribute('data-publish')) <= now; };

  document.querySelectorAll('[data-publish]').forEach(function (el) {
    el.classList.add(isOpen(el) ? 'is-open' : 'is-sealed');
  });

  // Ana sayfa: yalnızca en son açılmış gönderiyi öne çıkar
  var box = document.querySelector('[data-latest]');
  if (box) {
    var open = [].slice.call(box.querySelectorAll('.feature.is-open'));
    var last = open[open.length - 1];
    box.querySelectorAll('.feature').forEach(function (f) { f.hidden = f !== last; });
    var empty = box.querySelector('.empty-feature');
    if (empty) empty.hidden = !!last;
  }

  // Videolar: kapak görseli, tıklanınca YouTube oynatıcısı
  document.addEventListener('click', function (ev) {
    var btn = ev.target.closest('.yt .play');
    if (!btn) return;
    var wrap = btn.closest('.yt');
    var f = document.createElement('iframe');
    f.src = 'https://www.youtube-nocookie.com/embed/' + wrap.getAttribute('data-id') + '?autoplay=1&rel=0';
    f.title = 'YouTube video oynatıcısı';
    f.allow = 'autoplay; encrypted-media; picture-in-picture';
    f.allowFullscreen = true;
    wrap.innerHTML = '';
    wrap.appendChild(f);
  });
})();
