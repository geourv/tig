---
layout: manual-chapter
title: Consultes i dades relacionals
description: Un recorregut amb dades del CNIG des de la selecció manual de Vila-seca fins als filtres, les consultes espacials i la calculadora de camps.
lang: ca
ref: manual-queries-relational-data
profiles: [unaltremanual]
content_status: approved
permalink: /ca/chapters/consultes-dades-relacionals/
weight: 60
part: Continguts
manual_references: true
---

Trobar Vila-seca en un mapa i seleccionar-ne el terme és una primera manera d'interrogar les dades. Quan la pregunta passa a ser «quins municipis pertanyen a Tarragona?» o «quins portals es troben dins del terme?», el reconeixement visual deixa pas a un criteri que el SIG pot avaluar i repetir. El resultat pot ser una selecció temporal, una vista filtrada o una capa nova; saber distingir-los és necessari per continuar treballant amb el conjunt correcte.

El capítol segueix aquest canvi d'escala amb un mateix cas. Primer es localitza i se selecciona Vila-seca manualment. Després s'exploren els filtres de capa i de taula, es comparen les eines de selecció i es formalitza el criteri amb una expressió. La posició dels portals, les illes i les vies introdueix les seleccions espacials. Finalment, la calculadora de camps permet mesurar, classificar i relacionar el valor d'una entitat amb el conjunt.

>>>>> En acabar el recorregut, cal poder conservar consultes i càlculs territorials que es puguin reconstruir.
>>>>>
>>>>> - Distingir la capa activa, les entitats seleccionades i les files que mostra una taula.
>>>>> - Aplicar filtres i seleccions manuals, per expressió i per ubicació, comprovant-ne l'abast.
>>>>> - Exportar els subconjunts al GeoPackage amb identificadors i geometries comprovables.
>>>>> - Crear i actualitzar camps del tipus adequat, interpretar l'ajuda de les funcions i verificar un agregat.

## Les dades i el projecte del cas {#dades-cas-consultes}

Les dades vectorials es descarreguen de la secció **Información Geográfica de Referencia** del [Centre de Descàrregues del CNIG](https://centrodedescargas.cnig.es/CentroDescargas/). El recorregut utilitza límits administratius, CartoCiudad i xarxes de transport de Tarragona. Obtenir els paquets, descomprimir-los i identificar-ne les capes forma part del treball; no s'ha de començar amb un subconjunt preparat sense saber d'on prové.

::: table "Edicions i capes utilitzades en el recorregut de Vila-seca"
| Producte | Edició del cas | Capa i contingut que s'inspeccionen |
| --- | --- | --- |
| [Línies límit](https://centrodedescargas.cnig.es/CentroDescargas/detalleArchivo?sec=9000029) | 28/07/2026 | Recintes municipals, provincials i autonòmics del paquet Shapefile peninsular/balear |
| [CartoCiudad Tarragona](https://centrodedescargas.cnig.es/CentroDescargas/detalleArchivo?sec=9092) | 04/2026 | `portalpk_publi` i `manzana`, dins de `tarragona.gpkg` |
| [Xarxes de transport de Tarragona](https://centrodedescargas.cnig.es/CentroDescargas/detalleArchivo?sec=11655613) | 07/2026 | `rt_tramo_vial`, dins de `red_viaria.gpkg` |
:::

`recintos_municipales_inspire_peninbal_etrs89` és la capa municipal d'aquesta distribució. Conté **8.132 entitats** i declara `EPSG:4258`. Els noms de les capes provincial i autonòmica indiquen el nivell equivalent. Aquesta font no té necessàriament el mateix esquema que una distribució GML. De la mateixa manera, el nom genèric `rt_viales` d'altres materials no substitueix el nom físic `rt_tramo_vial` observat en aquest paquet.

Els originals es conserven a `data/raw/`. Amb QGIS tancat, el GeoPackage validat de `pr2` es copia de `dist/` a `sandbox/` amb el nom `pr3-consultes-cognom.gpkg`. La nova vista principal es desa com a `pr3` i les fonts locals es reorienten al contenidor nou. Les capes heretades continuen disponibles. En aquest capítol, el terme del CNIG que es seleccionarà al primer pas es desarà com a `municipi_consulta` i serà la referència de totes les consultes espacials del cas.

Les captures corresponen a **QGIS 3.44.11** amb la interfície configurada en català; algunes cadenes encara apareixen en anglès. L'ortofoto WMS ICGC del projecte inicial serveix per orientar-se. Les consultes s'apliquen a les capes vectorials del CNIG, no als píxels de l'ortofoto.

## Localitzar i seleccionar Vila-seca al mapa {#seleccio-manual-vila-seca}

Es carrega la capa municipal completa, es deixa damunt del WMS i es representa sense farciment, amb el contorn visible. Per trobar Vila-seca cal navegar cap al litoral de Tarragona i acostar el mapa amb la roda del ratolí i l'eina de desplaçament. Reus, Tarragona i Salou ajuden a situar el terme. Les etiquetes basades en `NAMEUNIT` faciliten el reconeixement; encara no s'ha aplicat cap filtre provincial.

Al panell **Capes** es fa clic sobre **Municipis CNIG** per convertir-la en la capa activa. Després s'activa **Selecciona objectes** i es fa un clic a l'interior de Vila-seca. També es pot arrossegar un rectangle petit que intersecti el terme. La selecció ressaltada pertany a aquesta capa: tenir el WMS visible no el converteix en una font d'entitats seleccionables.

![QGIS amb Vila-seca seleccionat dins de la capa municipal del CNIG, la capa activa emmarcada i un glif de clic al mapa]({{ site.baseurl }}/assets/img/qgis/qgis-c05-manual-selection.annotations.svg "La primera selecció és manual: s'activa Municipis CNIG i es fa clic a l'interior de Vila-seca. El glif identifica el clic i el ressaltat mostra l'entitat seleccionada dins de la font completa."){: data-figure-width-web="58rem" data-figure-width-pdf="100%"}

La comprovació consisteix a obrir la taula d'atributs i llegir l'entitat seleccionada: `NAMEUNIT` és **Vila-seca** i `NATCODE` és **34094343171**. Hi ha una entitat seleccionada, però la font encara en conté 8.132. El codi és text identificador, no una magnitud. El rectangle de cerca tampoc no s'ha convertit en una geometria nova: s'ha marcat el polígon municipal complet.

El reconeixement visual és útil per explorar, però el codi permetrà reconstruir la selecció sense repetir el mateix clic. Abans de continuar es neteja la selecció, de manera que el resultat del filtre següent no es confongui amb aquest estat temporal.

## Limitar la capa als municipis de Tarragona {#filtre-municipis-tarragona}

La pregunta següent és administrativa: quins municipis pertanyen a la província de Tarragona? A la capa carregada, el camp textual `CODNUT3` conté la codificació que permet formular aquest criteri. S'activa **Municipis CNIG** al panell, es fa **clic amb el botó dret sobre aquella fila** i, al menú contextual que s'obre, s'escull **Filtre…**.

![Capa Municipis CNIG activa, glif de botó dret sobre la seva fila i opció Filtre ressaltada al menú contextual]({{ site.baseurl }}/assets/img/qgis/qgis-c05-layer-filter-menu.annotations.svg "El menú s'obté amb el botó dret sobre la capa activa. L'anotació assenyala la fila d'origen del clic i el requadre ressalta Filtre, l'acció que obre el constructor de la consulta."){: data-figure-width-web="58rem" data-figure-width-pdf="100%"}

Al constructor se selecciona `CODNUT3`, es consulten els valors disponibles i s'escriu la condició que mostra la captura: el codi provincial ha de coincidir amb **ES514**. Les cometes dobles identifiquen el camp i les simples delimiten el literal de text. El mateix diàleg informa que la consulta s'avalua al proveïdor **OGR SQL**. Després de provar-la, s'accepta amb **D'acord**.

![Constructor del filtre de capa amb CODNUT3 i la consulta provincial completa emmarcada]({{ site.baseurl }}/assets/img/qgis/qgis-c05-layer-filter-dialog.annotations.svg "La consulta del proveïdor limita la capa a CODNUT3 igual a ES514. El quadre d'expressió conté el criteri complet que s'ha d'aplicar a aquesta distribució del CNIG."){: data-figure-width-web="54rem" data-figure-width-pdf="100%"}

La capa exposa ara **184 municipis**. El fitxer original continua contenint-ne 8.132: no s'han esborrat els altres. El filtre modifica el conjunt disponible per al mapa, les consultes i els processos que rebin aquesta capa. La icona de filtre del panell permet reconèixer l'estat; reobrir **Filtre…** permet consultar o retirar la condició.

Desar el projecte pot conservar aquest filtre, però no crea una còpia provincial dins del GeoPackage de la pràctica. Aquesta distinció serà important quan es vulgui conservar un resultat que no depengui de la configuració temporal de la capa.

## Inspeccionar subconjunts a la taula d'atributs {#filtres-taula}

Es manté el filtre provincial i s'obre la taula amb el botó dret sobre la capa, **Obre la taula d'atributs**. Al desplegable **inferior esquerre** es decideix quines files mostra el panell. Canviar aquest mode no és aplicar un altre filtre de capa: el mapa i les eines continuen disposant dels 184 municipis del subconjunt provincial.

### Totes les files o només les seleccionades

**Mostrar tots els objectes** mostra les 184 files exposades per la capa. Per contrastar-ho, es marquen tres municipis a la taula, Reus, Salou i Vila-seca, fent clic a les capçaleres de fila i afegint les files separades amb Ctrl. Després s'escull **Mostra els objectes seleccionats** al desplegable inferior esquerre.

![Taula amb tres municipis seleccionats i el desplegable inferior esquerre, amb el mode de seleccionats emmarcat]({{ site.baseurl }}/assets/img/qgis/qgis-c05-table-filter.annotations.svg "El filtre de taula deixa visibles Reus, Salou i Vila-seca perquè estan seleccionats. La capa continua exposant 184 entitats; tornar a Mostrar tots els objectes recupera les seves files al panell."){: data-figure-width-web="45rem" data-figure-width-pdf="90%"}

El recompte s'ha de llegir en el context correcte: **8.132** a la font, **184** a la capa filtrada i **3** a la selecció i a la taula. La selecció es comparteix entre mapa i taula. Una cel·la activa, en canvi, no demostra per si sola que la seva entitat estigui seleccionada.

### Les entitats visibles al mapa

El mode **Show Features Visible on Map** limita les files a les entitats visibles a l'extensió actual del llenç. A la vista local del cas apareixen **nou municipis**. Si es canvia el zoom o es desplaça el mapa, pot canviar la llista: aquest mode respon «què hi ha a la vista?», no «què pertany a la província?».

![Taula d'atributs amb el mode d'entitats visibles al mapa i el control inferior assenyalat]({{ site.baseurl }}/assets/img/qgis/qgis-c05-table-visible-filter.annotations.svg "El filtre d'entitats visibles depèn de l'extensió del mapa. Els nou registres d'aquesta vista són una finestra d'inspecció sobre la mateixa capa provincial de 184 municipis."){: data-figure-width-web="48rem" data-figure-width-pdf="95%"}

### Filtrar per camp o per expressió

**Filtre per camp** permet escollir una columna i introduir un criteri de cerca adequat al seu tipus. **Filtre avançat (Expressió)** obre el constructor de QGIS i permet combinar camps i funcions. En el cas s'hi demanen els tres noms anteriors amb `IN`, que comprova la pertinença a una llista. La captura mostra la consulta aplicada i la taula resultant després de netejar la selecció.

![Taula amb tres files, el filtre avançat per NAMEUNIT visible i cap entitat seleccionada]({{ site.baseurl }}/assets/img/qgis/qgis-c05-table-expression-filter.annotations.svg "La mateixa llista de tres municipis pot provenir d'una expressió de la taula, amb zero entitats seleccionades. El camp de consulta i el selector de mode permeten distingir aquest estat de Mostra els objectes seleccionats."){: data-figure-width-web="48rem" data-figure-width-pdf="95%"}

El desplegable també permet inspeccionar entitats noves o editades i entitats amb restriccions incomplertes. Són modes de diagnòstic: no signifiquen que els altres registres s'hagin eliminat. Abans de calcular o exportar, cal comprovar separadament **filtre de capa**, **mode de la taula** i **selecció activa** {% cite qgisUserGuide344 %}.

## Construir una selecció reproduïble {#seleccions-expressions}

Fins ara s'ha distingit allò que la capa ofereix d'allò que el panell mostra. Ara es torna al mapa per comparar les maneres de marcar entitats. Es tanca el filtre d'inspecció de la taula, es deixa activa **Municipis CNIG** i es manté el subconjunt provincial de 184 municipis.

### Eines de selecció i modificadors

El menú **Edita > Selecciona** i el desplegable de la barra de selecció donen accés a les eines. Cadascuna defineix una cerca; el resultat continua sent un conjunt d'entitats marcades, no una capa geomètrica nova.

![Menú real de selecció de QGIS amb l'eina de clic o rectangle ressaltada i les alternatives visibles]({{ site.baseurl }}/assets/img/qgis/qgis-c05-selection-tools.annotations.svg "Selecciona objectes admet un clic o un rectangle. Les eines de polígon, mà alçada i radi canvien la forma de la cerca; totes actuen sobre la capa activa."){: data-figure-width-web="45rem" data-figure-width-pdf="90%"}

::: table "Gestos de cerca al mapa"
| Eina | Gest | Què es conserva en seleccionar |
| --- | --- | --- |
| Clic o rectangle | Clic a l'interior o arrossegament del rectangle | L'entitat completa que coincideix amb la cerca |
| Polígon | Clics per als vèrtexs; clic dret per acabar | Les entitats que compleixen la relació amb l'àrea dibuixada |
| Mà alçada | Clic per començar, moviment i un altre clic per acabar | Les entitats trobades pel traç tancat |
| Radi | Clic al centre, moviment o radi numèric i clic final | Les entitats trobades pel cercle; no es desa una zona d'influència |
:::

Amb **un sol clic**, Shift o Ctrl commuten la pertinença de l'entitat: l'afegeixen si no estava seleccionada i la retiren si ho estava. Es pot comprovar fent clic a Vila-seca, Shift+clic a Salou i Ctrl+clic a Vila-seca. Els resultats successius són una entitat, dues i només Salou.

En una **selecció per àrea**, Shift afegeix coincidències i Ctrl les retira. Ctrl+Shift conserva només les coincidències que ja formaven part de la selecció. Amb Vila-seca i Salou marcats, un rectangle petit a l'interior de Vila-seca amb Ctrl+Shift deixa només Vila-seca. Alt exigeix que l'entitat quedi completament continguda en l'àrea dibuixada: aquell rectangle petit no conté cap municipi sencer i deixa la selecció buida {% cite qgisUserGuide344 %}.

Sobre les **capçaleres de fila** de la taula, Ctrl permet afegir o retirar files separades i Shift selecciona un interval contigu. Per això marcar les files primera i tercera amb Ctrl produeix dues entitats, mentre que Shift des de la primera inclou també la segona. No s'ha d'aplicar una única regla de modificadors a clics de mapa, cerques per àrea i intervals de files.

**Selecciona tots els objectes** marca les 184 entitats de la capa filtrada. **Inverteix la selecció** canvia seleccionades per no seleccionades dins d'aquest conjunt: si només hi havia Vila-seca, en queden 183. **Desselecciona els objectes de la capa actual** deixa zero; l'opció de totes les capes té un abast més ampli. **Resselecciona objectes** permet recuperar la selecció anterior després de deseleccionar-la. Aquestes accions modifiquen l'estat de treball i convé comprovar-ne el recompte.

### Seleccionar pel valor d'un atribut o amb una expressió

**Selecciona objectes a partir d'un valor…** obre un formulari de cerca, adequat per a una consulta senzilla. Quan cal conservar el criteri exacte o combinar condicions, es tria **Edita > Selecciona > Selecciona objectes segons una expressió…**. A la versió mostrada, la drecera és **Ctrl+F3**.

![Ruta Edita i Selecciona amb l'acció de selecció per expressió ressaltada i la drecera Ctrl F3 a la mateixa fila]({{ site.baseurl }}/assets/img/qgis/qgis-c05-selection-expression-menu.annotations.svg "La selecció per expressió s'obre des d'Edita > Selecciona. El requadre identifica l'acció concreta; Ctrl+F3 apareix a la mateixa fila del menú."){: data-figure-width-web="56rem" data-figure-width-pdf="100%"}

El constructor s'assembla al del filtre avançat de la taula: permet escollir camps, consultar valors i construir expressions amb funcions. Aquí, però, el botó final és **Selecciona objectes**. S'hi expressa el mateix identificador que s'havia comprovat després del clic manual, `NATCODE` igual al codi de Vila-seca.

![Diàleg natiu de selecció per expressió amb el criteri NATCODE de Vila-seca i el botó Selecciona objectes emmarcats]({{ site.baseurl }}/assets/img/qgis/qgis-c05-selection-expression-dialog.annotations.svg "La condició identifica Vila-seca pel seu codi i el botó Selecciona objectes la converteix en una selecció. La previsualització avalua la fila indicada pel selector, no el recompte de totes les coincidències."){: data-figure-width-web="54rem" data-figure-width-pdf="100%"}

En prémer el botó queda **una entitat seleccionada**, la mateixa que amb el clic inicial. La capa continua tenint 184 municipis disponibles i no s'ha creat cap fitxer. El desplegable del botó també permet afegir coincidències, retirar-les o limitar la selecció actual. Abans d'acceptar un resultat cal comprovar quin mètode s'ha utilitzat.

La selecció i el filtre avançat de taula utilitzen el motor d'expressions de QGIS. El filtre de capa anterior es delegava a OGR SQL. Que una igualtat senzilla sigui vàlida en tots dos contextos no garanteix que totes les funcions o conversions tinguin la mateixa sintaxi.

### Llegir una expressió: tipus, condicions i valors absents

Una expressió relaciona una **entrada**, una **operació** i un **resultat**. A la consulta anterior, l'entrada és el valor textual de `NATCODE`; l'operació compara amb un literal; el resultat és cert o fals per a cada fila amb codi conegut. Escriure el nom del camp entre cometes simples el convertiria en un text constant i no llegiria la columna.

`AND` exigeix que es compleixin dues condicions, `OR` n'admet almenys una i `NOT` les nega. Els parèntesis fan explícita l'agrupació quan es combinen. Per exemple, el criteri de vies principals que s'utilitzarà més endavant és una llista de classes admeses; `IN` evita repetir moltes igualtats unides amb `OR`. Una consulta que afegeix un criteri espacial al criteri de classe exigeix que es compleixin tots dos.

`NULL` indica un valor absent o desconegut; no és zero, cadena buida ni el text `'NULL'`. Es comprova amb `IS NULL`, no amb `= NULL`. Comparar un nul amb un valor ordinari produeix un resultat desconegut, i `NOT` no el converteix en cert. Una selecció només marca les files on el predicat és cert. Cal comptar les absències quan podrien canviar la interpretació del subconjunt.

Les funcions s'introdueixen segons la necessitat: `trim()` retira espais perifèrics d'un text, `round()` arrodoneix una mesura i `CASE` tria un resultat segons condicions. No s'han de normalitzar noms ni convertir codis a nombres només per fer coincidir dues taules. Convé conservar l'atribut rebut i calcular la preparació en un camp nou.

### Desar la selecció i el context administratiu

Amb Vila-seca seleccionat es fa clic dret a la capa i es tria **Exporta > Desa els objectes seleccionats com a…**. La destinació és el GeoPackage de `pr3`, el nom intern és `municipi_consulta` i el CRS de sortida, `EPSG:25831`. Aquest pas reprojecta i desa el municipi complet. En carregar-lo es comproven la font local, una entitat i el mateix `NATCODE`.

Per conservar també el conjunt provincial es torna a la capa filtrada i s'exporten **totes les entitats**, amb l'opció de només seleccionades desmarcada, com a `municipis_tarragona`. La sortida conté 184 municipis sense necessitar el filtre original. El mode d'inspecció de la taula no determina què exporta aquesta operació.

![Relació entre la font municipal, la capa filtrada, una selecció de tres, la taula i una exportació de totes les entitats]({{ site.baseurl }}/assets/diagrams/ca/05-consultes-dades-relacionals/filter-selection-flow.puml "Cada estat té un recompte propi. Mostrar tres files o marcar tres entitats no canvia una exportació configurada per desar tots els 184 municipis de la capa provincial."){: data-figure-width-web="30.5rem" data-figure-width-pdf="72%"}

Les altres escales administratives es poden conservar amb el mateix procediment. Sobre els recintes provincials, `"NATCODE" LIKE '3409%'` selecciona les quatre províncies catalanes de l'edició. Sobre els autonòmics, `"CODNUT2" IN ('ES24','ES51','ES52')` identifica Aragó, Catalunya i la Comunitat Valenciana. S'exporten només les seleccionades com a `provincies_catalunya` i `ccaa_context`. Els codis NUTS i `NATCODE` són codificacions diferents: cal consultar els camps reals de cada nivell.

## Seleccionar per ubicació sobre el mateix municipi {#cas-consultes-vila-seca}

El codi ha permès trobar Vila-seca; ara la pregunta es refereix a objectes d'altres capes que hi tenen una relació espacial. La referència serà **municipi_consulta**, el terme CNIG que s'acaba de desar. Mantenir aquesta mateixa geometria durant totes les consultes permet atribuir una diferència de resultat al criteri aplicat i no a un canvi inadvertit de límit.

### Seleccionar i exportar els portals de CartoCiudad {#portals-seleccio-exportacio}

Es carrega `portalpk_publi` des de `tarragona.gpkg`. Abans de preguntar per la posició cal comprovar què representa cada punt. El camp `tipo` té dos valors: **364.921 `Portal`** i **3.369 `PK`**, fins al total de 368.290 entitats. Els punts quilomètrics no són portals; per això s'obre el filtre de capa i s'hi aplica el criteri mostrat.

![Filtre de la capa de CartoCiudad amb la condició tipo igual a Portal emmarcada]({{ site.baseurl }}/assets/img/qgis/qgis-c05-portals-filter.annotations.svg "El filtre atributiu conserva els portals i exclou els punts quilomètrics. La selecció espacial següent només rebrà aquesta unitat d'observació."){: data-figure-width-web="54rem" data-figure-width-pdf="100%"}

A la caixa d'eines de Processament es cerca **Selecciona per la ubicació**, identificat com `native:selectbylocation`. L'entrada és **Portals CartoCiudad**; el predicat, **intersecta**; la capa de comparació, **Vila-seca · municipi CNIG**; i el mètode crea una **selecció nova**. En executar, QGIS compara les geometries en una referència compatible sense haver de canviar artificialment el CRS declarat dels originals.

![Diàleg de selecció per ubicació amb el predicat, el municipi CNIG de comparació i el botó Executa ressaltats]({{ site.baseurl }}/assets/img/qgis/qgis-c05-spatial-selection.annotations.svg "La configuració relaciona els portals filtrats amb el municipi CNIG seleccionat al començament. Executa produeix una selecció nova de 3.584 portals en aquestes edicions."){: data-figure-width-web="54rem" data-figure-width-pdf="100%"}

En prémer **Executa**, el diàleg selecciona **3.584 portals** a la capa d'entrada. Es tanca el diàleg i s'enquadra **tot el terme de Vila-seca**, amb el contorn municipal visible. Els punts grocs són els seleccionats; els grisos continuen a la font però no formen part de la selecció. La vista municipal permet comprovar-ne la distribució respecte del polígon complet i reconèixer els punts exteriors que han quedat sense seleccionar.

![Terme municipal complet de Vila-seca amb els portals seleccionats en groc i altres punts de la font sense seleccionar]({{ site.baseurl }}/assets/img/qgis/qgis-c05-portals-selected.annotations.svg "La vista del terme complet permet contrastar els portals seleccionats amb el límit municipal. Els punts grocs són candidats a exportar; encara es treballa amb la capa original i una selecció temporal."){: data-figure-width-web="58rem" data-figure-width-pdf="100%"}

Per conservar-la, es fa **clic dret sobre Portals CartoCiudad**, la capa que té la selecció, i s'obre **Exporta > Desa els objectes seleccionats com a…**. L'opció que es refereix als seleccionats evita confondre aquest resultat amb una exportació de tots els portals de la província.

![Menú contextual de Portals CartoCiudad amb el clic dret i l'acció Desa els objectes seleccionats com a ressaltats]({{ site.baseurl }}/assets/img/qgis/qgis-c05-selected-export-menu.annotations.svg "La selecció es converteix en una sortida persistent des del menú de la mateixa capa. El ressaltat identifica Desa els objectes seleccionats com a, no l'exportació general de tots els objectes."){: data-figure-width-web="58rem" data-figure-width-pdf="100%"}

Al diàleg es tria **GeoPackage** i, amb el botó de cerca del **Nom del fitxer**, s'escull el fitxer existent de `pr3` a `sandbox/`. **Nom de la capa** serà `portals_vilaseca`; el CRS de sortida, `EPSG:25831`; i **Desa només els objectes seleccionats** ha de quedar marcat. També es manté **Afegeix el fitxer desat al mapa**. Es crea una taula nova dins del contenidor: no se sobreescriuen les capes que ja conté.

![Diàleg d'exportació dels portals amb el GeoPackage existent, el nom portals_vilaseca, EPSG 25831 i només seleccionats ressaltats]({{ site.baseurl }}/assets/img/qgis/qgis-c05-portals-export-dialog.annotations.svg "El diàleg configura l'exportació dels 3.584 portals seleccionats al GeoPackage de treball. El fitxer identifica el contenidor; portals_vilaseca identifica la capa nova que s'hi afegeix."){: data-figure-width-web="55rem" data-figure-width-pdf="100%"}

Després de prémer **D'acord**, es comprova la capa local afegida al projecte: **3.584 registres**, geometria de punt, CRS de sortida, identificadors d'origen i només valors `Portal` a `tipo`. La seva font ha d'apuntar al GeoPackage de `pr3`. Es pot netejar la selecció i retirar la capa provincial del projecte sense perdre el subconjunt exportat; el resultat es mostrarà junt amb les illes desades en el pas següent.

Amb `estan dins` també se seleccionen 3.584 portals en el cas, però els predicats no són equivalents. Un punt exactament a la frontera pot intersectar el municipi sense estar dins del seu interior. La coincidència dels recomptes s'ha de llegir com un resultat d'aquestes dades, no com una propietat universal {% cite ogcSimpleFeatures2011 %}.

>> Un recompte ràpid del proveïdor pot conservar temporalment el total anterior a un filtre. Els controls del cas recorren les entitats realment exposades i contrasten les capes desades amb SQLite. Si el recompte sembla incoherent, cal revisar consulta, valors i sortida persistent abans d'interpretar-lo.

### Seleccionar illes completament dins del terme {#illes-seleccio-exportacio}

Es carrega `manzana`, que conté **28.459 illes**. A **Propietats > Informació** es comprova que la geometria és **Polygon**. Cal representar-les amb farciment i contorn, mantenint la vista de tot el municipi per comprovar la selecció. Dibuixar només els contorns pot fer que semblin línies de viari. El filtre `tipo` anterior pertanyia als portals i no s'ha de traslladar a aquesta capa.

La pregunta d'aquest pas és més restrictiva: quines illes queden **completament dins** de Vila-seca? A **Selecciona per la ubicació**, l'entrada és **Illes CartoCiudad**, el predicat és **estan dins**, la referència és **Vila-seca · municipi CNIG** i el mètode crea una selecció nova.

![Diàleg de selecció espacial d'Illes CartoCiudad amb el predicat estan dins i el municipi de referència destacats]({{ site.baseurl }}/assets/img/qgis/qgis-c05-blocks-spatial-selection.annotations.svg "Estan dins selecciona les illes contingudes en el terme. Aquest és el criteri del resultat principal que es desarà; intersecta es reserva per comparar els casos de frontera."){: data-figure-width-web="54rem" data-figure-width-pdf="100%"}

L'execució selecciona **285 polígons**. Amb el terme complet enquadrat, el farciment groc permet reconèixer les illes seleccionades i comprovar que queden dins del contorn municipal. Els polígons grisos de l'altra banda del límit, o els que el travessen i no compleixen el predicat, romanen a la font però no s'exportaran.

![Terme complet de Vila-seca amb illes de CartoCiudad seleccionades en groc i altres polígons sense seleccionar]({{ site.baseurl }}/assets/img/qgis/qgis-c05-blocks-selected.annotations.svg "El mateix enquadrament municipal permet comprovar les illes respecte de tot el límit. El farciment groc identifica les superfícies seleccionades; les entitats no seleccionades només aporten context de la font."){: data-figure-width-web="58rem" data-figure-width-pdf="100%"}

Es repeteix **Exporta > Desa els objectes seleccionats com a…**, ara des d'**Illes CartoCiudad**. S'escull el mateix GeoPackage i un nom nou, `illes_vilaseca`, amb `EPSG:25831` i només seleccionats. En acceptar es comproven les 285 entitats locals i que cap polígon desat no ultrapassi el terme.

![Exportació nativa de la selecció d'illes al GeoPackage amb el nom illes_vilaseca i només seleccionats activat]({{ site.baseurl }}/assets/img/qgis/qgis-c05-blocks-export-dialog.annotations.svg "illes_vilaseca s'afegeix al mateix contenidor que els portals. L'exportació conserva els 285 polígons seleccionats, no els 28.459 de la font provincial."){: data-figure-width-web="55rem" data-figure-width-pdf="100%"}

Per entendre el paper de la frontera es pot tornar a la capa original i repetir la selecció amb **intersecta**, sense substituir la sortida anterior. Els recomptes següents corresponen a les consultes sobre la font original i el mateix límit CNIG:

::: table "Comparació de predicats sobre les illes i el límit CNIG de Vila-seca"
| Criteri | Entitats seleccionades | Què s'ha de comprovar |
| --- | ---: | --- |
| `estan dins` | 285 | Contenció segons el predicat topològic |
| `intersecta` | 318 | Qualsevol punt compartit amb el terme |
| Intersecten però no queden contingudes | 33 | Entitats de frontera, incloses les que travessen el límit |
:::

Les 33 diferències s'han d'inspeccionar al mapa: una illa que travessa el terme compleix `intersecta` i, si s'exportés aquesta selecció, es conservaria **sencera**, inclosa la part exterior. El resultat principal `illes_vilaseca` continua sent el de **285 illes contingudes**. Escollir un predicat i retallar una geometria són operacions diferents.

![Vista del municipi complet amb portals locals taronja i illes locals amb farciment blau dins del límit magenta]({{ site.baseurl }}/assets/img/qgis/qgis-c05-exported-selections.annotations.svg "Resultats reoberts del GeoPackage amb tot Vila-seca enquadrat: 3.584 portals i 285 illes contingudes. El blau dels polígons i el taronja dels punts són simbologia de les capes desades, no el groc de la selecció temporal."){: data-figure-width-web="58rem" data-figure-width-pdf="100%"}

### Seleccionar i exportar autovies i autopistes {#autovies-seleccio-exportacio}

Es carrega `rt_tramo_vial` des de `red_viaria.gpkg`. La capa conté **233.982 registres** i el camp `clased` en descriu la classe. La pregunta es concreta en les **autovies i autopistes que passen per Vila-seca**, on es reconeixen l'A-7 i l'AP-7. El filtre de capa conserva les dues classes d'autovia/autopista de la captura; no inclou totes les carreteres convencionals de la província.

![Filtre del viari amb les classes Autopista libre / autovía i Autopista de peaje al quadre de consulta ressaltat]({{ site.baseurl }}/assets/img/qgis/qgis-c05-roads-filter.annotations.svg "El criteri atributiu conserva les dues classes d'autovia/autopista i deixa 3.663 registres provincials. La selecció municipal s'executarà després sobre aquest subconjunt."){: data-figure-width-web="54rem" data-figure-width-pdf="100%"}

S'obre **Selecciona per la ubicació** amb **Vials RT** com a entrada, **intersecta** com a predicat i **Vila-seca · municipi CNIG** com a referència. Cal crear una selecció nova. Aquí no s'utilitza `estan dins`, perquè una autovia pot travessar el terme i tenir part d'un tram fora del municipi.

![Selecció espacial del viari filtrat amb intersecta, el límit de Vila-seca i Executa assenyalats]({{ site.baseurl }}/assets/img/qgis/qgis-c05-roads-spatial-selection.annotations.svg "La selecció espacial s'aplica als 3.663 registres del filtre d'autovies i autopistes. Intersecta permet conservar també els trams que travessen el límit municipal."){: data-figure-width-web="54rem" data-figure-width-pdf="100%"}

En executar queden **265 registres seleccionats**. El mapa mostra els trams grocs i el límit magenta. Els extrems grocs que ultrapassen aquest contorn formen part de trams sencers que sí que intersecten Vila-seca: no són altres vies incorporades sense criteri. El retall dels extrems correspondrà al geoprocessament del capítol 6.

![Autovies i autopistes seleccionades en groc respecte del límit municipal magenta]({{ site.baseurl }}/assets/img/qgis/qgis-c05-roads-selected.annotations.svg "La selecció identifica les entitats viàries que intersecten el terme. El ressaltat groc encara és temporal i pot continuar fora del límit quan el tram seleccionat el travessa."){: data-figure-width-web="58rem" data-figure-width-pdf="100%"}

Amb aquesta selecció activa, es fa clic dret a **Vials RT** i s'exporten només els seleccionats al GeoPackage existent, com a `transport_candidats_c06`, en `EPSG:25831`. El nom indica que és l'entrada preparada per al capítol següent. La captura mostra el mateix patró d'exportació que s'ha comprovat amb punts i polígons.

![Diàleg d'exportació dels trams seleccionats al GeoPackage amb transport_candidats_c06, EPSG 25831 i només seleccionats]({{ site.baseurl }}/assets/img/qgis/qgis-c05-roads-export-dialog.annotations.svg "L'exportació desa els 265 registres seleccionats com una capa nova del contenidor. Es conserven els atributs, els identificadors i les geometries lineals completes."){: data-figure-width-web="55rem" data-figure-width-pdf="100%"}

Després de l'exportació es comprova la capa afegida i se'n neteja la selecció. Les etiquetes A-7 i AP-7 identifiquen dues vies del resultat. El recompte de **265 files** correspon a **185 valors diferents d'`id_tramo`**: la font associa alguns trams a més d'un itinerari, com AP-7, E-15 o el corredor TEN-T. No s'ha d'interpretar el nombre de files com un nombre de carreteres, ni eliminar-ne repeticions sense entendre aquesta relació.

![Capa d'autovies i autopistes reoberta del GeoPackage, dibuixada en blau, amb A-7 i AP-7 etiquetades]({{ site.baseurl }}/assets/img/qgis/qgis-c05-roads-result.annotations.svg "Resultat persistent, amb l'A-7 i l'AP-7 recognoscibles. El blau representa la capa local i no una selecció activa. Les parts exteriors continuen presents perquè l'exportació no ha retallat els trams."){: data-figure-width-web="58rem" data-figure-width-pdf="100%"}

### Què canvia quan es relacionen atributs

Les operacions anteriors decideixen quines entitats es conserven. Una **unió** respon una pregunta diferent: quina informació d'una altra taula correspon a cada entitat? Una unió per clau compara codis; una unió espacial compara geometries. En tots dos casos cal distingir zero, una o diverses correspondències abans d'afegir atributs {% cite longleyGeographicInformationScience2015 %}.

Per exemple, molts portals poden correspondre a un municipi: és una relació **N:1** des dels portals i **1:N** des del municipi. Afegir a cada portal una fitxa municipal única pot ser una unió directa. Consultar tots els portals des del municipi demana conservar el detall com una relació, o resumir-lo expressament. Unir el detall com si fos una sola fila per municipi podria duplicar el polígon o prendre una coincidència arbitrària.

![Cardinalitats entre territoris i taules relacionades, amb casos 1:1, N:1, 1:N i N:M]({{ site.baseurl }}/assets/quarto/05-consultes-dades-relacionals/join-cardinality.qmd "La cardinalitat indica quantes correspondències s'esperen per fila. El detall de molts objectes associats a un municipi no es converteix automàticament en una fitxa municipal única."){: data-figure-width-web="56rem" data-figure-width-pdf="100%"}

La clau ha de ser estable, única a la banda corresponent i no nul·la. Els noms municipals ajuden a inspeccionar, però poden tenir variants i homònims. En observacions repetides, la unitat pot ser municipi i any, i la clau ha d'incloure totes dues dimensions. Abans d'una unió es compten nuls, duplicats i codis sense parella; després es comproven el nombre de files conservades i una mostra de correspondències. Els punts fronterers amb diverses coincidències no s'han d'assignar sempre a la primera candidata.

## Calcular atributs i interpretar les funcions {#mesures-municipis}

Ara el GeoPackage conserva subconjunts identificats i reobribles. La pregunta passa de **quines entitats** a **quin valor correspon a cada una**: superfície municipal, longitud d'un tram o pes d'un municipi dins del conjunt provincial. La calculadora de camps avalua una expressió per fila i escriu el resultat en un atribut compatible.

El [disseny de la taula d'atributs del capítol de digitalització](../model-vectorial-digitalitzacio/#disseny-taula-atributs) ja relacionava tipus, unitats i dominis. La mateixa decisió reapareix aquí: un codi amb zeros inicials necessita text; una àrea amb fraccions necessita un nombre decimal; una classe com `mitja` necessita text. Convertir una mesura a enter o afegir-hi literalment `km²` canviaria el tipus de resultat i en limitaria l'ús posterior.

### Crear un camp numèric nou

S'activa **municipis_tarragona**, la capa local de 184 polígons. Es comprova que la capa està realment en `EPSG:25831` i que el projecte utilitza **GRS80**, metres per a distàncies i metres quadrats per a àrees. El CRS del llenç no substitueix el de la font. Es neteja la selecció i s'obre la calculadora des de la taula d'atributs.

Es marca **Crea un camp nou**, s'escriu `area_km2` i es tria **Nombre decimal (real)**. L'expressió de la captura converteix l'àrea el·lipsoidal del projecte a quilòmetres quadrats. **Crea un camp virtual** queda desmarcat perquè el resultat s'ha de conservar al GeoPackage. En acceptar, QGIS pot activar el mode d'edició; després cal desar els canvis.

![Calculadora de camps amb el nom area_km2, el tipus decimal i l'expressió ressaltats]({{ site.baseurl }}/assets/img/qgis/qgis-c05-field-calculator.annotations.svg "Crear un camp exigeix decidir-ne el nom, el tipus i l'expressió. El càlcul s'aplica als 184 municipis perquè no hi ha una selecció que en limiti l'abast."){: data-figure-width-web="56rem" data-figure-width-pdf="100%"}

La previsualització correspon a l'entitat indicada pel selector. Un valor plausible no comprova tota la columna: cal revisar nuls, valors no positius, extrems i una mostra coneguda. En aquest cas s'han contrastat els 184 resultats amb el càlcul de QGIS i les mesures geomètriques corresponents.

### Actualitzar un camp existent

Per actualitzar no es torna a crear el mateix nom. Es marca **Actualitza un camp existent**, es tria el camp i es defineix la nova expressió. El cas arrodoneix `area_km2` a sis decimals: la captura mostra tant el camp de destinació com la fórmula. Aquesta decisió fixa els decimals emmagatzemats; no augmenta l'exactitud de la geometria.

![Calculadora en mode d'actualització d'area_km2 amb l'expressió d'arrodoniment i el selector de camp ressaltats]({{ site.baseurl }}/assets/img/qgis/qgis-c05-field-update.annotations.svg "Actualitzar substitueix els valors del camp escollit. El mode de creació queda desactivat i l'expressió recalcula area_km2 amb sis decimals."){: data-figure-width-web="56rem" data-figure-width-pdf="100%"}

Després de l'actualització, Vila-seca conserva **21,708437 km²**. S'han comprovat totes les files, no només la previsualització. Si estigués activada l'opció d'actualitzar només les seleccionades, les altres mantindrien el valor anterior; aquesta barreja exigeix una justificació. Crear un camp conserva la comparació amb l'entrada; actualitzar-lo la substitueix i cal registrar la fórmula als apunts.

Un **camp emmagatzemat** escriu el valor a la font i queda congelat fins que es recalcula. Un **camp virtual** conserva l'expressió al projecte i la reavalua. És útil per explorar, però pot dependre del context de QGIS i no és necessàriament visible en un altre programa. Una edició de la geometria pot deixar obsoleta una mesura emmagatzemada encara que el camp continuï tenint nombres vàlids.

### Llegir l'ajuda d'una funció i calcular un agregat {#ajuda-funcions-agregats}

La llista central del constructor agrupa les funcions per famílies. **Seleccionar una funció** mostra a la dreta la seva ajuda; si el panell està plegat, s'utilitza **Mostra l'ajuda**. Cal llegir què retorna, la sintaxi, els arguments obligatoris i opcionals i els exemples. La barra de desplaçament permet continuar fins als arguments i exemples que no caben a la primera vista. Aquesta ajuda correspon a la versió de QGIS que està executant el càlcul.

Un agregat resumeix diverses files. Per saber quin percentatge de la superfície provincial correspon a cada municipi, el numerador és la seva `area_km2` i el denominador és la suma de les 184 àrees. Es crea un altre camp decimal, `quota_area_pct`, i s'escull **Agregats > aggregate** per llegir-ne l'ajuda mentre es construeix l'expressió.

![Calculadora amb quota_area_pct, la funció aggregate seleccionada i els panells d'expressió i ajuda emmarcats]({{ site.baseurl }}/assets/img/qgis/qgis-c05-aggregate-help.annotations.svg "L'ajuda nativa mostra la funció aggregate i la seva signatura. L'expressió divideix l'àrea de la fila per la suma d'àrees de la capa i la converteix en percentatge."){: data-figure-width-web="60rem" data-figure-width-pdf="100%"}

En aquesta expressió, **`@layer`** identifica la capa actual, **`'sum'`** tria la suma i **`"area_km2"`** indica què s'avalua a les files que s'agreguen. L'argument opcional `filter` permetria restringir-les. La funció retorna un únic total; la divisió exterior el compara amb l'àrea de cada municipi i la multiplicació per cent expressa la quota. Els arguments tenen funcions diferents: el nom d'un camp no s'ha de confondre amb el literal que tria l'operació.

El total dels valors emmagatzemats és **6.306,697054 km²**. Vila-seca representa aproximadament **0,344212%**, i la suma de les 184 quotes és **100%**, dins de la tolerància numèrica del càlcul. Aquests controls comproven el denominador i l'abast. Un filtre de capa addicional canviaria el conjunt disponible i, per tant, el significat del percentatge.

El resultat agregat pot repetir-se a cada fila sense canviar la unitat d'observació. Si es desés només el total provincial als 184 municipis i després se sumés aquella columna, es multiplicaria el total per 184. Una taula resum amb una fila per província és una representació diferent. Igualment, la mitjana de densitats municipals no equival necessàriament a dividir la suma de població per la suma de superfície. Els nuls i la cobertura han d'acompanyar qualsevol resum.

### Àrea, perímetre i longitud: funció, CRS i unitat

L'ajuda també permet distingir funcions de mesura semblants. `$area`, `$perimeter` i `$length` respecten la configuració de mesura del projecte. `area($geometry)`, `perimeter($geometry)` i `length($geometry)` calculen planarment sobre les coordenades de la geometria. Si aquestes coordenades són geogràfiques, el resultat pla no s'expressa en metres o metres quadrats {% cite qgisUserGuide344 %}.

::: table "Mesures contrastades del polígon CNIG de Vila-seca"
| Expressió | Mètode i unitat | Resultat |
| --- | --- | ---: |
| `area($geometry)` | Pla, sobre EPSG:25831, m² | 21.704.046,0248 |
| `$area` | El·lipsoidal GRS80, m² | 21.708.436,9802 |
| `perimeter($geometry)` | Pla, m | 38.438,1327 |
| `$perimeter / 1000` | El·lipsoidal, km | 38,442087 |
:::

La diferència entre les dues àrees prové del mètode de mesura sobre **la mateixa geometria**, no d'un canvi de font municipal. El cas conserva camps separats per comparar-les. Canviar l'el·lipsoide del projecte posteriorment no actualitza per si sol una columna ja emmagatzemada.

Sobre `transport_candidats_c06`, els camps decimals `long_plana_m`, `long_ellipsoide_m` i `long_km` conserven, respectivament, la longitud plana, l'el·lipsoidal i la conversió a quilòmetres. La suma dels **265 registres** és **79,337036 km**. Inclou les parts exteriors al terme, les calçades diferenciades i les representacions d'un mateix tram en diversos itineraris. Per tant, no és la longitud d'eixos únics exclusivament dins de Vila-seca. En canvi, `length("NAMEUNIT")` sobre els municipis comptaria caràcters: el tipus de l'argument també determina què fa una funció.

### Classificacions i etiquetes amb camps del tipus adequat

Una classificació es desa en un camp textual. Per a `classe_area`, el cas defineix tres intervals didàctics de superfície el·lipsoidal: menys de 10 km², de 10 a menys de 50 i 50 o més. La branca de nuls és explícita i l'ordre de les condicions determina on entren els límits:

```text
CASE
  WHEN $geometry IS NULL OR is_empty($geometry) THEN NULL
  WHEN $area / 1000000 < 10 THEN 'petit'
  WHEN $area / 1000000 < 50 THEN 'mitja'
  ELSE 'gran'
END
```

El resultat és **37** municipis `petit`, **105** `mitja` i **42** `gran`. La suma reconstrueix els 184 registres i Vila-seca queda a `mitja`. Els llindars són una decisió de l'exercici, no una classificació oficial. Si hi hagués geometries buides, caldria comptar els nuls separadament.

Per a les etiquetes, el camp textual `nom_etiqueta` conserva el nom de presentació sense substituir `NAMEUNIT`. L'expressió següent retira espais perifèrics, tracta la cadena buida com a absent i ofereix un text de presentació quan falta el nom:

```text
coalesce(nullif(trim("NAMEUNIT"), ''), 'Sense nom')
```

A `area_km2` es pot assignar l'àlies **Àrea (km²)**. El camp continua sent numèric i les expressions continuen referint-se al seu nom físic. La unitat s'afegeix en construir el text de l'etiqueta, no dins de la columna numèrica. A **Etiquetes > Etiquetes simples**, es combina el nom, un salt de línia, el valor formatat en català i el sufix de la unitat:

```text
"nom_etiqueta" || '\n' ||
format_number("area_km2", 2, 'ca_ES') || ' km²'
```

![Municipis de l'entorn de Vila-seca etiquetats amb nom i superfície en km², amb la capa de mesures identificada]({{ site.baseurl }}/assets/img/qgis/qgis-c05-label-expression.annotations.svg "L'etiqueta presenta Vila-seca amb 21,71 km². La presentació amb dos decimals i el sufix de la unitat no transformen el camp numèric en text ni n'alteren el valor emmagatzemat."){: data-figure-width-web="58rem" data-figure-width-pdf="100%"}

## Conservar i comprovar el recorregut

En acabar, el GeoPackage conté les capes heretades i les noves capes de consulta, context administratiu, portals, illes i transport. Es desen les edicions, el projecte principal incrustat `pr3` i un `.qgz` extern nou, amb camins relatius al contenidor homònim. Amb QGIS tancat es prepara la parella a `dist/` i es prova des d'una ubicació neta.

La comprovació ha de recuperar els resultats, no els clics: municipi CNIG identificat, 184 municipis provincials, quatre províncies, tres comunitats de context, 3.584 portals, 285 illes contingudes i 265 registres d'autovies/autopistes en aquestes edicions. Es comproven també els camps persistents, les quotes, els identificadors i les geometries completes. Els apunts conserven els criteris i les captures que mostren accés, selecció, exportació i resultat reobert. El WMS continua requerint xarxa; la seva imatge no queda incrustada al GeoPackage.

## Activitats

### Reconstruir els estats d'una consulta

Sobre la capa provincial, cal trobar Vila-seca manualment i recuperar-lo després per expressió. Es contrastaran totes les files, seleccionades, visibles al mapa i filtrades per expressió. Per a cada estat s'anotaran recompte de font, capa, taula i selecció. La comprovació ha d'explicar com una taula de tres files pot coexistir amb zero entitats seleccionades i una capa de 184 municipis.

### Interpretar les fronteres i els agregats

Cal localitzar, a la font original, una de les 33 illes que entren a la selecció per intersecció però no a la de contenció, i explicar per què no forma part d'`illes_vilaseca`. Després s'ha de justificar per què els 79,337036 km calculats sobre els registres viaris no equivalen a quilòmetres d'eixos únics interiors al terme. La comparació de 265 files amb 185 identificadors de tram diferents ha d'acompanyar aquesta interpretació. A la capa municipal es contrastarà una quota de superfície amb el seu numerador i denominador, utilitzant l'ajuda d'`aggregate` per explicar els arguments.

### Relacionar el detall amb els municipis

Es poden relacionar els portals provincials amb els municipis CNIG. Cal declarar el predicat i diagnosticar zero, una i diverses coincidències per portal. Només les correspondències resoltes alimentaran una taula resum amb una fila per clau municipal; el detall es conservarà com a relació 1:N. Abans d'unir el resum als polígons cal comprovar-ne la unicitat i les claus sense parella. Els casos ambigus són part del diagnòstic, no files que s'hagin d'amagar.

### Micropràctica 3: del municipi escollit als resultats comprovats

::: table "Resultats que cal conservar a la instantània pr3"
| Component | Resultat observable |
| --- | --- |
| Entrades | GeoPackage validat de `pr2` i originals documentats de límits, CartoCiudad i transport de l'àmbit escollit |
| Consultes | Selecció manual contrastada amb una expressió; filtres de capa i taula diferenciats; predicats espacials justificats |
| Dades desades | Municipi de consulta i context administratiu; portals, illes i candidats de transport, amb identificadors i geometries comprovats |
| Camps | Mesures decimals amb CRS i unitats; una actualització documentada; classe textual; agregat contrastat i etiquetes |
| Apunts | Fonts, edicions, criteris, recomptes, ajuda consultada, captures significatives, incidències i interpretació |
| Transport | Projecte incrustat `pr3` i `.qgz` homònim reoberts amb les fonts locals resoltes |
:::

Els recomptes del cas serveixen per comprovar Vila-seca en les edicions indicades, no com a xifres que s'hagin d'imitar en un altre municipi. Moodle concreta l'abast avaluat. La parella validada es conserva amb el nom base `pr3-consultes-cognom` i es tracta com a fita de només lectura mentre el capítol següent en prepara la còpia de geoprocessament.
