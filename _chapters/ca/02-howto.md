---
lang: ca
permalink: /:title/ca/
title: 2. Com Començar
author: Tao He
date: 2019-04-28
category: Jekyll
weight: 2
layout: chapter
---

El tema jekyll-gitbook es pot utilitzar igual que altres [temes de Jekyll][3] i admet [tema remot][2] a [Github Pages][1], consulta també [la guia oficial][4].

Pots incorporar aquest tema de Jekyll al teu lloc web de dues maneres:

- Fer un [fork][5] d'aquest repositori i afegir les teves publicacions en markdown a la carpeta `_posts`, després pujar-les al teu propi repositori de Github.
- Utilitzar-lo com a tema remot al teu fitxer [`_config.yml`][6] (tal com fem nosaltres mateixos per a aquest lloc),

```yaml
# Configuracions
title:            Jekyll Gitbook
longtitle:        Jekyll Gitbook
remote_theme:     sighingnow/jekyll-gitbook
```

##### CONSELL
No cal pujar el paquet HTML generat.
{: .block-tip }

[1]: https://pages.github.com
[2]: https://github.com/sighingnow/jekyll-gitbook/fork
[3]: https://pages.github.com/themes
[4]: https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/adding-a-theme-to-your-github-pages-site-using-jekyll
[5]: https://github.com/sighingnow/jekyll-gitbook/fork
[6]: https://github.com/sighingnow/jekyll-gitbook/blob/master/_config.yml
