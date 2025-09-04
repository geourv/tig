require(['gitbook'], function (gitbook) {
  gitbook.events.bind('start', function () {

    function gotoLang(lang) {
      try { localStorage.setItem('preferredLang', lang); } catch (_) {}
      const path = window.location.pathname;
      const search = window.location.search || '';
      const hash = window.location.hash || '';
      // replace last segment /ca /es /en etc.
      const updated = path.replace(/\/([a-z]{2})(\/)?$/, '/' + lang);
      const target = (updated === path) ? (path.replace(/\/?$/, '/') + lang) : updated;
      window.location.href = target + search + hash;
    }

    // build dropdown dynamically from SITE_LANGS (populated in head.html)
    var langs = (window.SITE_LANGS || []).map(function (l) {
      return {
        text: l.name,
        onClick: function () { gotoLang(l.code); }
      };
    });

    gitbook.toolbar.createButton({
      id: 'lang-switcher',
      icon: 'fa fa-globe',
      label: 'Language',
      className: 'language-settings',
      position: 'left',
      dropdown: langs
    });

  });
});
