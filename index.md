---
layout: none
---

<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{{ site.title }}</title>
  <script>
    const preferred = localStorage.getItem('preferredLang') || 'ca';
    const base = "{{ site.baseurl }}";
    const target = base + '/' + (preferred === 'en' ? 'en/' : 'ca/');
    window.location.replace(target);
  </script>
</head>
<body>
  <noscript>
    <p>
      <a href="{{ site.baseurl }}/ca/">Català</a> |
      <a href="{{ site.baseurl }}/en/">English</a>
    </p>
  </noscript>
</body>
</html>

