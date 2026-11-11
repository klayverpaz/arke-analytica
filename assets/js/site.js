(function () {
  'use strict';
  var doc = document.documentElement;
  doc.classList.add('js');

  // Menu mobile
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.getElementById('site-nav');
  if (toggle && nav) {
    var setOpen = function (open) {
      nav.classList.toggle('is-open', open);
      toggle.setAttribute('aria-expanded', String(open));
    };
    toggle.addEventListener('click', function () {
      setOpen(!nav.classList.contains('is-open'));
    });
    nav.addEventListener('click', function (ev) {
      if (ev.target.closest('a')) setOpen(false);
    });
    document.addEventListener('keydown', function (ev) {
      if (ev.key === 'Escape') setOpen(false);
    });
  }

  // Idioma: guarda a escolha para o redirecionamento da raiz
  var remember = function (lang) {
    try { localStorage.setItem('arke-lang', lang); } catch (err) { /* sem storage */ }
  };
  var pageLang = (doc.lang || 'pt').slice(0, 2).toLowerCase();
  remember(pageLang);
  document.querySelectorAll('[data-lang]').forEach(function (a) {
    a.addEventListener('click', function () { remember(a.getAttribute('data-lang')); });
  });

  // Entrada discreta das seções
  var items = document.querySelectorAll('[data-reveal]');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('is-in'); });
  }

  // Formulário: monta a mensagem e abre o WhatsApp. Nada é enviado a servidor.
  var form = document.getElementById('contact-form');
  if (form) {
    var status = form.querySelector('.form-status');
    var cfg = JSON.parse(form.getAttribute('data-msg'));
    form.addEventListener('submit', function (ev) {
      ev.preventDefault();
      if (form.elements.website.value) return; // honeypot
      form.classList.add('was-validated');
      if (!form.checkValidity()) {
        status.textContent = status.getAttribute('data-error');
        status.className = 'form-status is-error';
        var bad = form.querySelector(':invalid');
        if (bad) bad.focus();
        return;
      }
      var lines = [cfg.intro, ''];
      ['name', 'company', 'email', 'phone', 'challenge', 'timeline', 'budget'].forEach(function (key) {
        var value = (form.elements[key].value || '').trim();
        if (!value || (key === 'budget' && value === cfg.skip)) return;
        lines.push(cfg.labels[key] + ': ' + value);
      });
      var url = 'https://wa.me/' + form.getAttribute('data-wa-number') + '?text=' + encodeURIComponent(lines.join('\n'));
      status.textContent = status.getAttribute('data-sent');
      status.className = 'form-status is-ok';
      window.open(url, '_blank', 'noopener');
    });
  }
})();
