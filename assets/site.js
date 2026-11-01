// Algoritma Postası — videoyu tıklayınca YouTube oynatıcısını yükle.
// (Yayın saati gelmemiş postalar siteye hiç konmaz; ayıklama derleme sırasında yapılır.)
(function () {
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
