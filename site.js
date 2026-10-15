/* Shared behaviour for the new blocks. Loaded with defer on every page. */
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Booking illustration: pick a time -> court booked -> confirmation.
     The resting HTML shows the finished frame (confirmation), so no JS, reduced
     motion or a frozen background tab still leaves a complete picture. */
  var phone = document.getElementById('sfPhone');
  if (phone && !reduce) {
    var frames = phone.querySelectorAll('.sf-frame');
    var steps = document.querySelectorAll('.sf-bs');
    var n = frames.length, i = n - 1, timer = null, paused = false, hold = [3200, 2800, 3600];

    function show(k) {
      frames.forEach(function (f, j) {
        f.classList.remove('was-on');
        if (j === i) f.classList.add('was-on');     // outgoing stays opaque underneath
        f.classList.toggle('is-on', j === k);
      });
      steps.forEach(function (s, j) { s.classList.toggle('is-on', j === k); });
      var prev = i; i = k;
      setTimeout(function () { if (frames[prev] && prev !== i) frames[prev].classList.remove('was-on'); }, 650);
    }
    function tick() {
      if (paused) { timer = setTimeout(tick, 500); return; }
      show((i + 1) % n);
      timer = setTimeout(tick, hold[i] || 3000);
    }
    function onScreen() {
      var r = phone.getBoundingClientRect();
      return r.bottom > 0 && r.top < (window.innerHeight || document.documentElement.clientHeight);
    }
    function check() { paused = document.hidden || !onScreen() || phone.matches(':hover'); }
    phone.closest('.sf-book').classList.add('sf-anim');
    window.addEventListener('scroll', check, { passive: true });
    window.addEventListener('resize', check);
    document.addEventListener('visibilitychange', check);
    phone.addEventListener('mouseenter', check);
    phone.addEventListener('mouseleave', function () { setTimeout(check, 0); });
    check();
    timer = setTimeout(tick, 1200);
  } else if (phone) {
    var last = document.querySelector('.sf-bs[data-step="3"]');
    if (last) last.classList.add('is-on');
  }
})();
