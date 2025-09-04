---
layout: none
---

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{{ site.title }}</title>

  {%- assign langs = site.data.languages -%}
  {%- assign first_lang = langs | first -%}
  <script>
    (function () {
      // data from Jekyll
      var BASE = "{{ site.baseurl }}";
      var LANGS = {{ langs | jsonify }};
      var CODES = LANGS.map(function (x) { return x.code; });
      var DEFAULT = "{{ first_lang.code | default: 'ca' }}";

      function pickPreferred() {
        // 1) stored choice
        try {
          var stored = localStorage.getItem('preferredLang');
          if (stored && CODES.indexOf(stored) !== -1) return stored;
        } catch (e) {}

        // 2) browser language (e.g., "es-ES" -> "es")
        var nav = (navigator.language || navigator.userLanguage || "").toLowerCase();
        if (nav && nav.length >= 2) {
          var two = nav.slice(0,2);
          if (CODES.indexOf(two) !== -1) return two;
        }

        // 3) fallback to the first language in _data
        return DEFAULT;
      }

      function ensureSlash(s) { return s.endsWith('/') ? s.slice(0,-1) : s; }

      var base = ensureSlash(BASE);
      var lang = pickPreferred();
      var langEntry = LANGS.find(function (x){ return x.code === lang; }) || LANGS[0];

      // prefer path_prefix if provided; else construct "/<code>/"
      var prefix = (langEntry && langEntry.path_prefix) ? langEntry.path_prefix : ("/" + lang + "/");

      var target = base + prefix;
      // avoid double slashes (when base = "" and prefix starts with "/")
      target = target.replace(/\/{2,}/g, "/");

      window.location.replace(target);
    })();
  </script>

  <!-- no-JS fallback: immediate refresh to default language -->
  <meta http-equiv="refresh" content="0; url={{ site.baseurl }}{{ first_lang.path_prefix | default: '/' | append: first_lang.code | append: '/' }}">
</head>
<body>
  <noscript>
    <p>
      {%- for l in langs -%}
        <a href="{{ site.baseurl }}{{ l.path_prefix | default: '/' | append: l.code | append: '/' }}">{{ l.name }}</a>{% unless forloop.last %} |
        {% endunless %}
      {%- endfor -%}
    </p>
  </noscript>
</body>
</html>
