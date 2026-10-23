---
title: "PR4 · Malles, Delaunay, Voronoi postal i atlas"
lang: ca
recipient: alumnat
content_status: draft
subject: "Tecnologies de la Informació Geogràfica"
subject_code: "21234114"
author: "Benito Zaragozí"
institution: "Universitat Rovira i Virgili"
---

# Encàrrec i resultats d’aprenentatge

Els mateixos portals poden respondre preguntes diferents segons la unitat espacial que es construeixi. Una malla resumeix observacions per cel·la; Delaunay proposa parelles veïnes; Voronoi assigna dominis de proximitat. Reus permet seguir aquest ordre i acabar amb una cobertura regular de pàgines d’atlas.

Cal poder preparar generadors traçables, comprovar recomptes, estudiar agrupacions per distància i obtenir una zonificació postal estimada. El codi postal és una categoria textual: no s’interpola com una altura. L’atlas conserva un layout editable i relaciona mida de cel·la, dimensions del mapa i escala.

El professor concreta a classe i a Moodle els apartats seleccionats i si formen part del **70% bàsic de PR4** o del **20% d’ampliacions**. La guia completa no és una llista d’obligacions automàtiques. Una aportació es valora una sola vegada; el taller no crea una setena instantània.

# Fonts i preparació

El cas utilitza CartoCiudad Tarragona **04/2026**, disponible al [CNIG](https://centrodedescargas.cnig.es/CentroDescargas/detalleArchivo?sec=9092), i límits municipals CNIG **07/2026**. Es conserven originals, metadades, llicència i crèdits IGN/CNIG. El terme de Reus s’identifica amb `NATCODE=34094343123`; les capes de treball es preparen en **EPSG:25831**.

| Camp de CartoCiudad | Significat per al procediment |
| --- | --- |
| `id_porpk` | Identificador declarat pel productor |
| `tipo` | Portal o punt quilomètric |
| `cod_postal` | Categoria postal |
| `ine_mun`, `municipio` | Atribució municipal, que es contrasta amb la posició |
| `fuente_datos`, `fecha_modificacion` | Procedència i actualització |

Table: Camps de portalpk_publi dins de tarragona.gpkg.

La font original declara EPSG:4258. Canviar el CRS de la vista no transforma els punts emmagatzemats: s’exporta una còpia reprojectada. L’Explorador mostra els GeoPackage del projecte i dels originals; el WMS IGN/PNOA es carrega sota els vectors, amb contorns sense farciment per conservar-ne els colors.

## Definir el domini amb entorn

La consulta `"tipo" = 'Portal'` exclou els punts quilomètrics. Una selecció addicional per `ine_mun=43123` pot servir per inspeccionar l’atribució administrativa de Reus, però **no defineix tot l’entorn de construcció**: els portals de fora poden influir dins del terme.

El cas amplia el rectangle municipal almenys 1.500 m i arrodoneix els extrems cap enfora a múltiples de 1.000 m. Es desa com `domini` i s’hi extreuen els portals. És un marge rectangular, no un buffer euclidià. En transferir el procediment cal documentar l’extensió i provar si un entorn més ampli modifica els resultats.

## Passar de registres a generadors

Es conserva un camp ordinari `id_font` que identifiqui cada fila original abans d’exportar. Els FID de les capes noves poden canviar. Per identificar coincidències, es pot crear una clau textual de coordenada amb `geom_to_wkt($geometry, 17)` sobre la còpia puntual preparada; la precisió queda fixada i no s’arrodoneixen posicions per agrupar-les arbitràriament.

Es resumeixen les files per aquesta clau: nombre de portals, codis diferents i correspondència amb els IDs originals. Quan una ubicació conté diverses adreces del mateix codi, es conserva un únic punt generador amb `n_portals`. Si hi ha codis incompatibles o absents, es defineix una categoria explícita i es revisa la font; no es mouen els punts ni s’elimina el conflicte silenciosament.

Una còpia amb geometries duplicades eliminades permet materialitzar els punts únics, però els atributs de la fila que sobreviu no són un resum. S’hi uneix el resum per la clau de coordenada, s’assigna un `id_generador` persistent i únic i es conserva la taula de correspondència. Cada punt ha de representar una ubicació admesa i tots els registres han de continuar identificables.

La demostració té **35.190 portals** i **34.614 generadors**. Aquests generadors complets alimenten totes les estructures següents. Una partició d’entrenament/validació es prepara separadament i no substitueix el conjunt de treball sense advertir-ho.

# Malles regulars

## Construir quadrats amb origen fix

Una tessel·lació cobreix un domini sense buits ni solapaments d’interiors. La malla quadrada imposa unitats comunes per resumir punts. Des de Processament s’obre **Crea una quadrícula**, `native:creategrid`, amb aquests paràmetres:

| Paràmetre | Cas de 500 m |
| --- | --- |
| Tipus | Rectangle poligonal, `TYPE=2` |
| Extensió | La de `domini` |
| Espaiaments horitzontal i vertical | 500 m |
| Solapament horitzontal i vertical | 0 |
| CRS | EPSG:25831 |
| Sortida | `malla_500m` al GeoPackage |

Table: Quadrícula regular del cas de Reus.

![Diàleg de quadrícula amb tipus i espaiament destacats](assets/img/qgis/qgis-c06-graella-parametres.png "Extensió, CRS i espaiaments defineixen les cel·les. Igualar els dos costats produeix quadrats; el solapament zero manté interiors disjunts.")

Es repeteix a 1.000 m, conservant el mateix domini i origen, com `malla_1000m`. Cada cel·la rep `id_cella`, fila i columna. Les files i columnes es poden obtenir de la coordenada del centre respecte de l’origen: part entera de la diferència dividida pel costat. Els identificadors no depenen del FID regenerat.

## Comptar ubicacions i portals

**Compta punts en polígons** permet obtenir el nombre de generadors per cel·la; un resum espacial de `n_portals` permet obtenir el nombre de registres representats. Es conserven tots dos camps, `n_ubicacions` i `n_portals`, i les cel·les buides. Cal distingir un zero observat de l’absència de cobertura de la font.

![Malla regular sobre el terme de Reus](assets/img/qgis/qgis-c06-graella-resultat.png "Els quadrats continuen fora del municipi perquè es treballa amb un domini ampli. El retall municipal és una decisió posterior.")

Un punt sobre una frontera pot coincidir amb diverses cel·les. Abans de sumar es comprova que cada generador s’hagi assignat una sola vegada. El cas resolt utilitza intervals semioberts de coordenades, amb l’extrem exterior final inclòs a l’última cel·la. Si el resum espacial duplica fronteres, cal materialitzar la relació punt–cel·la i aplicar aquesta regla abans d’agregar.

Sobre el domini complet, la suma ha de recuperar **34.614 ubicacions** i **35.190 portals**. Retallar cel·les pel municipi crea peces parcials: comparar-ne recomptes bruts amb els d’un quadrat complet pot ser enganyós. Recompte, densitat per àrea i taxa per població o exposició són indicadors diferents.

## Comparar mida, origen i forma

Passar de 500 a 1.000 m mostra l’efecte d’escala del MAUP; desplaçar l’origen mantenint la mida mostra l’efecte de zonificació. Cal comparar patrons i totals amb els mateixos punts. Els hexàgons regulars ofereixen sis veïns laterals equidistants, però no eliminen aquests efectes. En provar-los es documenten les dimensions i l’àrea efectivament generades: el mateix valor d’espaiament no garanteix la mateixa superfície que un quadrat.

# Delaunay i distàncies entre veïns

## Construir triangles i arestes úniques

La triangulació de Delaunay connecta generadors amb triangles el cercle circumscrit dels quals no conté altres punts a l’interior. A QGIS s’executa `native:delaunaytriangulation` sobre `generadors`, amb tolerància zero i atributs dels vèrtexs activats. Es desa `triangles` i es revisen triangles perifèrics i possibles degeneracions.

![Triangulació dels generadors únics](assets/img/qgis/qgis-c06-delaunay-parametres.png "La mateixa capa de generadors alimenta la triangulació i el Voronoi posterior. Els identificadors retornats s’han de relacionar amb la capa d’entrada.")

Per estudiar distàncies es necessiten segments amb dos extrems identificables. La seqüència guiada és:

1. Convertir els polígons triangulars a línies amb `native:polygonstolines`.
2. Separar els segments amb `native:explodelines`. Una aresta interior es repeteix als dos triangles veïns.
3. Eliminar les geometries de segment duplicades i assignar una clau pròpia d’aresta. Conservar la triangulació original per comprovar la correspondència.
4. Obtenir còpies puntuals de l’inici i final de cada segment amb **Geometria per expressió**, `start_point($geometry)` i `end_point($geometry)`. Es conserva la clau d’aresta.
5. Relacionar cada extrem amb `generadors` mitjançant una unió pel més pròxim, amb distància màxima numèrica petita, per exemple 0,001 m, i comprovar que la distància és pràcticament zero. La tolerància serveix per reconèixer el mateix vèrtex, no per fusionar portals diferents.
6. Tornar els IDs dels dos extrems a les arestes per la clau. Normalitzar la parella per evitar A–B/B–A i comprovar que no hi ha autoparelles ni parelles duplicades.
7. Calcular `distancia_m` com `length($geometry)` sobre la capa EPSG:25831. Es desa `arestes` amb els IDs i la mesura recalculada.

El cas té **69.195 triangles** i **103.808 arestes úniques**. Els atributs copiats d’un triangle no identifiquen automàticament els dos extrems de cadascuna de les seves arestes; per això es fa la correspondència geomètrica anterior.

![Arestes de Delaunay en un sector del nord de Reus](assets/img/qgis/qgis-c06-delaunay-arestes.png "Les arestes proposen veïnatges euclidians. No són carrers, rutes de repartiment ni totes les parelles possibles entre portals.")

## Llindars i components connectats

Es conserva la capa completa i s’extreuen les arestes amb `"distancia_m" <= 50`, com `arestes_50m`. Es repeteix amb 25 i 100 m si la comparació està seleccionada. Els mapes mantenen enquadrament, escala i estils comparables.

Un component connectat reuneix punts units per alguna cadena d’arestes conservades. Un punt sense arestes continua essent un component d’una ubicació. Els extrems d’una cadena poden quedar més lluny del llindar: només cada pas ha de complir-lo.

Per etiquetar i contrastar els components a QGIS s’executa **DBSCAN**, `native:dbscanclustering`, sobre **tots els generadors**, amb `EPS=50`, `MIN_SIZE=1` i DBSCAN* desactivat. Es comproven pertinença, mida i aïllats. En el cas resolt aquesta configuració coincideix amb els components de les arestes de fins a 50 m. No és una equivalència amb el DBSCAN de paràmetres habituals: amb mínim superior hi intervenen nuclis, vora i soroll.

![Components i arestes de cinquanta metres](assets/img/qgis/qgis-c06-delaunay-llindar.png "El color indica mida del component, no un identificador únic: gris, aïllat; blau, 2–9 ubicacions; verd, 10–99; magenta, 100 o més. Les distàncies són geomètriques i poden travessar barreres.")

| Llindar | Arestes | Components | Aïllats |
| --- | ---: | ---: | ---: |
| 25 m | 53.237 | 6.810 | 5.074 |
| 50 m | 78.132 | 3.098 | 2.355 |
| 100 m | 92.649 | 1.323 | 916 |

Table: Resultats de referència amb els generadors complets del cas.

Augmentar el llindar pot unir components, però no els ha de dividir. Els números de clúster poden canviar entre execucions: es compara quins punts estan junts, no el número que l’algorisme assigna al grup. La interpretació ha d’explicar densitat de portals, efecte de cadena i possibles barreres.

# Voronoi i zonificació postal estimada

## Construir dominis i retallar-los

Voronoi assigna cada posició al generador més pròxim. Es calcula amb `native:voronoipolygons`, tolerància zero, còpia d’atributs activada i `BUFFER=100`. Aquí el buffer és una **ampliació percentual de l’extensió de construcció**, no una distància de 100 m. Cal comprovar que les cel·les cobreixen tot el terme; no s’afegeixen punts inventats a les cantonades.

![Paràmetres de Voronoi](assets/img/qgis/qgis-c06-reus-voronoi-parametres.png "La còpia d’atributs conserva el codi del generador. El marge dels generadors i l’ampliació percentual del diagrama són dues decisions diferents.")

Es retalla el diagrama per `municipi_reus` i es conserva `voronoi` amb `id_generador` i `cod_postal`. Els generadors externs han participat en la construcció encara que la seva posició no sigui dins del terme. En el cas hi queden **17.318 cel·les**.

![Cel·les retallades de Voronoi](assets/img/qgis/qgis-c06-reus-voronoi-resultat.png "El límit d’informe és municipal, però el conjunt de generadors inclou l’entorn. Les cel·les grans necessiten interpretar-se segons el suport de punts disponible.")

## Dissoldre pel codi textual

Es crea una segona capa amb `native:dissolve`, agrupada per `cod_postal`, sense substituir el Voronoi identificable. Els altres camps que conservi la dissolució no són estadístiques del grup. La capa final, `zones_postals`, pot tenir parts separades o enclavaments.

![Zones postals estimades de Reus](assets/img/qgis/qgis-c06-reus-codis-postals.png "Contorns i etiquetes representen categories dels generadors. El títol del mapa ha d’identificar una zonificació estimada per proximitat amb CartoCiudad 04/2026, no fronteres postals oficials.")

La demostració dona **15 categories**. Les classes minoritàries o que no comencin per 432 es diagnostiquen a la font; no s’eliminen per fer més plausible el mapa. Es comproven cobertura municipal, interiors disjunts i conservació de les categories entre cel·les i dissolució.

## Consistència i contrast independent

El codi assignat als propis generadors comprova la construcció, però no és validació independent. Per a una ampliació predictiva es reserven ubicacions o blocs abans de construir, mantenint juntes les adreces coincidents. Es recalculen les tessel·lacions amb entrenament i es comparen codis reservats, classes rares i desacords cartografiats. Aquest experiment té fitxers i recomptes propis.

Ampliar l’entorn permet estudiar sensibilitat de vora. Una coincidència sobre portals no valida automàticament fronteres en espais sense punts. Una delimitació externa amb metadades i llicència aporta un contrast diferent.

# Pràctica guiada d’atlas

## Preparar la cobertura

De `malla_1000m` s’extreuen les cel·les que comparteixen **àrea positiva** amb el terme. Es mantenen els quadrats complets; no s’utilitza un retall municipal de les cel·les. La sortida `cobertura_atlas` del cas té **82 entitats**.

Es conserven `id_cella`, fila i columna, i s’afegeix `pagina` ordenant de nord a sud i d’oest a est. Una ruta és **Afegeix un camp autoincremental**, amb inici 1 i expressió d’ordenació `-"fila" * 100000 + "columna"`, després de comprovar que hi ha menys de 100.000 columnes. Les files del cas augmenten cap al nord. Cal verificar la numeració, no donar per estable l’ordre dels FID.

![Cobertura de pàgines de Reus](assets/img/qgis/qgis-c06-atlas-cobertura.png "Els quadrats sencers d’1 km cobreixen el municipi i inclouen entorn a les vores. La numeració separa ordre de pàgina i identitat de cel·la.")

## Configurar el layout i el mapa

1. Obrir `Projecte > Dissenys` o crear un disseny d’impressió nou. Al cas resolt s’anomena **Atlas de tessel·les de Reus**.
2. Establir A4 vertical, **210 × 297 mm**. Inserir un mapa de **200 × 200 mm**, a X=5 mm i Y=40 mm, amb ID `mapa_atlas`.
3. Al panell Atlas, activar la generació i seleccionar `cobertura_atlas`. El nom de pàgina és `"id_cella"`, l’ordre ascendent és `"pagina"` i l’expressió de nom de fitxer és `'reus_' || "id_cella"`.
4. A les propietats del mapa, activar **Controlat per atlas**, escala fixa **1:5.000**, rotació zero i EPSG:25831. Fixar les capes del mapa perquè el llenç principal no les alteri accidentalment.
5. Afegir títol, fonts, CRS, escala, nord i paginació. El títol pot incloure `[% @atlas_pagename %]`; la numeració utilitza `@atlas_featurenumber` i `@atlas_totalfeatures`.

La comprovació d’enquadrament és numèrica: 200 mm a escala 1:5.000 representen 1.000 m. El marc i la cel·la són quadrats, de manera que poden coincidir. Un marge automàtic, una rotació o un marc rectangular modificarien l’extensió.

## Navegar i exportar

S’activa la previsualització i es comparen primera i última pàgina, una d’interior i una de vora. Han de variar el nom de cel·la, el número i l’extensió, mantenint-se l’escala. Si només canvia el títol, cal comprovar que l’element de mapa estigui controlat per atlas.

L’exportació es fa com a **atlas**, no com a layout estàtic. També es pot utilitzar `native:atlaslayouttopdf`, PDF únic. Si s’hi indica cobertura, es tornen a fixar filtre i ordre perquè substitueixen els del disseny; l’expressió d’ordre és `"pagina"`, ascendent.

![Configuració d’exportació de l’atlas a PDF](assets/img/qgis/qgis-c06-atlas-configuracio.png "El diàleg vincula disseny, cobertura i ordenació. La captura de paràmetres no acredita que el PDF s’hagi exportat ni revisat.")

S’obre el fitxer exportat i se’n comproven pàgines, ordre, dimensions, escala, fonts i enquadraments. Per al disseny d’una pàgina i les 82 cel·les s’espera **82 pàgines**; cal contrastar-ho amb el PDF. El WMS necessita connexió disponible. La cobertura i el layout es desen tant al projecte incrustat com al `.qgz`; desar-ne un no actualitza l’altre.

# Controls, fitxers i interpretació

| Resultat | Evidència que cal conservar |
| --- | --- |
| Preparació | Originals, CRS, regles de coincidència i correspondències |
| Malles | Mida, origen, cobertura i totals de registres/ubicacions |
| Arestes | IDs dels dos extrems, unicitat i longitud recalculada |
| Components | Llindar, aïllats, mides i efecte de cadena |
| Voronoi postal | Cel·les identificables, codis textuals i cobertura de la dissolució |
| Atlas | Cobertura, ordre, layout editable, previsualitzacions i PDF reobert |

Table: Controls del recorregut i distinció entre dades, configuració i sortides.

Les capes pròpies s’incorporen al GeoPackage de PR4 i s’actualitzen el principal `pr4`, el `.qgz` homònim, la composició i els apunts. El cas de Reus es manté separat com a demostració. Moodle concreta quins mapes i exportacions formen part del lliurament; no s’afegeix un fitxer obligatori només perquè la guia n’ofereixi un exemple.

La qualificació manté **70/20/10**, fins a **7 punts bàsics, 2 d’ampliacions i 1 de documentació**. Una ampliació pot estudiar mida/origen de malla, llindars, entorn del Voronoi, validació per blocs o relació cel·la–escala de l’atlas, sempre que afegeixi una pregunta al treball seleccionat. Es valoren controls i interpretació, no el nombre de capes ni un percentatge de coincidències aïllat.

# Referències

- [Anàlisi i geoprocessament vectorial, manual TIG](https://geourv.github.io/tig/ca/chapters/analisi-geoprocessament-vectorial/).
- [CartoCiudad Tarragona, CNIG](https://centrodedescargas.cnig.es/CentroDescargas/detalleArchivo?sec=9092).
- [Geometria vectorial, QGIS 3.44](https://docs.qgis.org/3.44/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html).
- [Generació d’atlas, QGIS 3.44](https://docs.qgis.org/3.44/en/docs/user_manual/print_layout/create_output.html#generate-an-atlas).
- [Exportació d’atlas, QGIS 3.44](https://docs.qgis.org/3.44/en/docs/user_manual/processing_algs/qgis/cartography.html#export-atlas-layout-as-pdf-single-file).
