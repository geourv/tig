/* This file is intentionally provided empty in the jekyll-gitbook theme.
 * It is loaded after the core scripts (theme.js, gitbook.js, etc.)
 * Its purpose is to let users extend or override behavior with their own JavaScript.
 *
 * In this project it has been customized to:
 *   - Add automatic numbering to headings (chapters/sections/subsections)
 *   - Synchronize that numbering with both the in-page TOC and the sidebar summary
 *   - Filter and number chapters by language, based on _data/languages.yml
 */


// --- automatic numbering for chapters and sections (0-based) ---
(function () {
  function addNumbering(root) {
    if (!root) return;

    var chap = parseInt(root.getAttribute('data-chapter'), 10);
    if (isNaN(chap)) chap = 0;

    var section = root.querySelector('.markdown-section') || root;
    var sec = 0; // h2
    var sub = 0; // h3

    function alreadyPrefixed(el) {
      if (!el) return false;
      if (el.firstElementChild && el.firstElementChild.classList.contains('hd-num')) return true;
      return /^\s*\d+(\.\d+)*\s/.test(el.textContent || '');
    }

    function setPrefix(el, prefix) {
      if (!el || alreadyPrefixed(el)) return;
      var span = document.createElement('span');
      span.className = 'hd-num';
      span.textContent = prefix; // spacing via CSS
      el.insertBefore(span, el.firstChild);
    }

    var walker = document.createTreeWalker(section, NodeFilter.SHOW_ELEMENT, {
      acceptNode: function (node) {
        var t = node.tagName ? node.tagName.toLowerCase() : '';
        return (t === 'h1' || t === 'h2' || t === 'h3') ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_SKIP;
      }
    });

    var seenFirstH1 = false, node;
    while ((node = walker.nextNode())) {
      var tag = node.tagName.toLowerCase();
      if (tag === 'h1') {
        if (!seenFirstH1) {
          setPrefix(node, String(chap));
          seenFirstH1 = true;
        } else {
          setPrefix(node, String(chap));
        }
      } else if (tag === 'h2') {
        sec += 1; sub = 0;
        setPrefix(node, chap + '.' + sec);
      } else if (tag === 'h3') {
        if (sec === 0) sec = 1;
        sub += 1;
        setPrefix(node, chap + '.' + sec + '.' + sub);
      }
    }
  }

  function run() {
    var root = document.querySelector('.chapter-content') || document.querySelector('.page-inner') || document.body;
    if (!root) return;
    root.querySelectorAll('.hd-num').forEach(function (n) { n.parentNode && n.parentNode.removeChild(n); });
    addNumbering(root);
  }

  if (document.readyState !== 'loading') run();
  else document.addEventListener('DOMContentLoaded', run);

  if (window.gitbook && gitbook.events && gitbook.events.bind) {
    gitbook.events.bind('page.change', run);
  }
})();


// --- synchronize numbering to TOC (in-page and sidebar) ---
(function () {
  function langsArray() {
    return (window.SITE_LANGS || []).map(function (x) { return x.code; });
  }
  function langFromPath(pathname) {
    var langs = langsArray();
    for (var i = 0; i < langs.length; i++) {
      var code = langs[i];
      if (pathname.indexOf('/' + code + '/') !== -1 || pathname.endsWith('/' + code) || pathname.endsWith('/' + code + '/')) {
        return code;
      }
    }
    return null;
  }
  function currentLang() {
    var fromData = document.querySelector('.chapter-content')?.getAttribute('data-lang');
    if (fromData) return fromData;
    var hl = (document.documentElement.getAttribute('lang') || '').toLowerCase();
    if (hl) return hl;
    return langFromPath(location.pathname) || (langsArray()[0] || 'ca');
  }

  function getPrefixFromHeading(h) {
    if (!h) return null;
    var s = h.querySelector('.hd-num');
    return s ? (s.textContent || '').trim() : null;
  }

  function setTOCNum(a, num) {
    if (!a || (!num && num !== 0)) return;
    var old = a.querySelector('.toc-num');
    if (old && old.parentNode) old.parentNode.removeChild(old);
    var fc = a.firstChild;
    if (fc && fc.nodeType === Node.TEXT_NODE && fc.nodeValue) {
      fc.nodeValue = fc.nodeValue.replace(/^\s+/, '');
    }
    a.setAttribute('data-num', String(num));
  }

  // in-page TOC (#id)
  function updateInPageTOC(scope) {
    var tocLinks = (scope || document).querySelectorAll('#toc a, nav#toc a, .table-of-contents a, .toc a');
    tocLinks.forEach(function (a) {
      var href = a.getAttribute('href') || '';
      if (!href || href.charAt(0) !== '#') return;
      var id = href.slice(1);
      var h = document.getElementById(id);
      var pref = getPrefixFromHeading(h);
      setTOCNum(a, pref);
    });
  }

// sidebar chapters
function updateSidebarChapters() {
  var lang = currentLang();
  var langs = new Set(langsArray());

  // seleccionem tots els <a> top-level de la TOC
  var links = Array.prototype.slice.call(
    document.querySelectorAll('.book-summary .summary > li > a')
  );

  // neteja
  links.forEach(function (a) { a.removeAttribute('data-num'); });

  var idx = 0;
  links.forEach(function (a) {
    // SALTAR la portada (no numerar però sí que ha de fer clic)
    var li = a.closest('li');
    if (li && (li.getAttribute('data-home') === '1' || li.classList.contains('home-item'))) {
      return; // no posem data-num a la portada
    }

    var href = a.getAttribute('href') || '';
    var path; try { path = new URL(href, location.href).pathname; } catch (_) { path = href; }
    var itemLang = langFromPath(path);
    if (!itemLang || !langs.has(itemLang) || itemLang !== lang) return;

    a.setAttribute('data-num', String(idx++));
  });
}



  // sidebar in-page (#id)
  function updateSidebarInPage() {
    var links = document.querySelectorAll('.book-summary a[href^="#"], .summary a[href^="#"]');
    links.forEach(function (a) {
      var id = a.getAttribute('href').slice(1);
      var h = document.getElementById(id);
      var pref = getPrefixFromHeading(h);
      setTOCNum(a, pref);
    });
  }

  function runTOC() {
    document.querySelectorAll('.book-summary .summary a[data-num], #toc a[data-num], .toc a[data-num], .table-of-contents a[data-num]')
      .forEach(function (a) { a.removeAttribute('data-num'); });

    setTimeout(function () {
      updateInPageTOC(document);
      updateSidebarChapters();
      updateSidebarInPage();
    }, 0);
  }

  if (document.readyState !== 'loading') runTOC();
  else document.addEventListener('DOMContentLoaded', runTOC);

  if (window.gitbook && gitbook.events && gitbook.events.bind) {
    gitbook.events.bind('page.change', runTOC);
  }

  var sum = document.querySelector('.book-summary .summary');
  if (sum && window.MutationObserver) {
    var mo = new MutationObserver(function () { runTOC(); });
    mo.observe(sum, { childList: true, subtree: true });
  }
})();


document.addEventListener("DOMContentLoaded", function() {
  mediumZoom('figure.md-figure img', {
    margin: 24,
    background: 'rgba(0,0,0,0.8)'
  });
});
