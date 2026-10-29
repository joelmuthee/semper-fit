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

  /* Bidirectional reveal (.sf-rv): comes in when it enters the screen, from below on
     the way down and from above on the way up, and resets once it has fully left.
     Geometry on a passive scroll listener, no IntersectionObserver. */
  var rv = [].slice.call(document.querySelectorAll('.sf-rv'));
  if (rv.length) {
    var lastY = window.scrollY;
    var tick = function () {
      var vh = window.innerHeight, down = window.scrollY >= lastY;
      lastY = window.scrollY;
      rv.forEach(function (el) {
        var r = el.getBoundingClientRect();
        var inView = r.top < vh * 0.92 && r.bottom > vh * 0.06;
        var gone = r.bottom < 0 || r.top > vh;
        if (inView && !el.classList.contains('in')) { el.classList.toggle('from-top', !down); el.classList.add('in'); }
        else if (gone && el.classList.contains('in')) el.classList.remove('in');
      });
    };
    window.addEventListener('scroll', tick, { passive: true });
    window.addEventListener('resize', tick);
    tick();
    // Anything still hidden after 3s (a frozen tab, a missed event) is shown anyway.
    setTimeout(function () { rv.forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < window.innerHeight && r.bottom > 0) el.classList.add('in');
    }); }, 3000);
  }

  /* Gym hours chart: a "now" line at the current Nairobi time, today's row marked, and
     the hero chip says whether the gym is open right now. All from the bars' own data,
     so the chart and the chip can never disagree. Static text above stays true without JS. */
  var week = document.getElementById('gyWeek');
  if (week) {
    var paint = function () {
      var eat = new Date(Date.now() + 3 * 3600 * 1000);
      var dow = eat.getUTCDay(), h = eat.getUTCHours() + eat.getUTCMinutes() / 60, x = h - 5;
      var rows = week.querySelectorAll('.gy-row'), today = null;
      rows.forEach(function (r) { var t = Number(r.dataset.dow) === dow; r.classList.toggle('is-today', t); if (t) today = r; });
      var line = week.querySelector('.gy-nowline');
      if (!line) { line = document.createElement('span'); line.className = 'gy-nowline'; week.appendChild(line); }
      if (today && x >= 0 && x <= 16) {
        var tr = today.querySelector('.gy-track').getBoundingClientRect(), wr = week.getBoundingClientRect();
        line.style.display = ''; line.style.left = (tr.left - wr.left + tr.width * x / 16) + 'px';
      } else line.style.display = 'none';
      var label = function (v) { var hh = Math.floor(v + 5), m = Math.round((v + 5 - hh) * 60); var ap = hh < 12 ? 'am' : 'pm'; var h12 = hh % 12 || 12; return h12 + (m ? ':' + String(m).padStart(2, '0') : '') + ap; };
      var open = null, next = null;
      if (today) today.querySelectorAll('.gy-gym').forEach(function (b) {
        var s = Number(b.style.getPropertyValue('--s')), e = Number(b.style.getPropertyValue('--e'));
        if (x >= s && x < e) open = e; else if (x < s && next === null) next = s;
      });
      var chip = document.getElementById('gyChip');
      if (chip) {
        chip.classList.toggle('is-open', open !== null);
        document.getElementById('gyChipT').textContent = open !== null ? 'Gym open now' : 'Gym closed now';
        document.getElementById('gyChipS').textContent = open !== null ? 'Until ' + label(open) + ' today' : (next !== null ? 'Opens ' + label(next) + ' today' : 'Opens again tomorrow');
      }
    };
    paint();
    window.addEventListener('resize', paint);
    setInterval(paint, 60000);
  }

  /* Padel rally: the SVG ball rests on its last point; the rally plays only while the
     court is on screen and the tab is visible, never under reduced motion. */
  var court = document.getElementById('pdCourt'), rally = document.getElementById('pdRally');
  if (court && rally && !reduce && court.pauseAnimations) {
    var started = false;
    var check = function () {
      var r = court.getBoundingClientRect();
      var on = !document.hidden && r.bottom > 0 && r.top < window.innerHeight;
      if (on && !started) { started = true; court.classList.add('pd-live'); rally.beginElement(); }
      if (started) { if (on) court.unpauseAnimations(); else court.pauseAnimations(); }
    };
    window.addEventListener('scroll', check, { passive: true });
    document.addEventListener('visibilitychange', check);
    check();
  }
})();
