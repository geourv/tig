---
title: "PR4 · Tessel·lacions i zonificació postal aproximada de Reus"
lang: ca
recipient: alumnat
content_status: approved
subject: "Tecnologies de la Informació Geogràfica"
subject_code: "21234114"
author: "Benito Zaragozí"
institution: "Universitat Rovira i Virgili"
---

# Encàrrec i resultats d’aprenentatge

Quina zonificació es pot construir a partir dels codis postals associats als portals de CartoCiudad? L’activitat utilitza Reus per comparar la triangulació de Delaunay amb el diagrama de Voronoi i obtenir una delimitació **estimada per proximitat**, que es pugui explicar i comprovar.

El codi postal és una categoria, encara que contingui dígits. Es conserva com a text i no s’interpola com si fos una altura. Delaunay descriu veïnatges entre generadors; Voronoi assigna cada posició al generador euclidianament més pròxim. Dissoldre les cel·les pel codi permet visualitzar zones de proximitat amb la mateixa etiqueta, sense convertir-les en delimitacions postals oficials.

Cal conservar generadors, dues estructures geomètriques, zones per codi, un mapa i una explicació dels casos ambigus. És una activitat del bloc PR4; el treball propi es transfereix al municipi escollit.

El professor indica a classe i a Moodle quins apartats se seleccionen i si el taller forma part del **70% bàsic de PR4** o és una opció del **20% d’ampliacions**. La guia completa no es converteix automàticament en obligació. Una mateixa aportació es valora una sola vegada.

# Punt de partida i dades

La font del cas és CartoCiudad Tarragona, edició 04/2026, obtinguda del [Centre de Descàrregues del CNIG](https://centrodedescargas.cnig.es/CentroDescargas/detalleArchivo?sec=9092). Dins de `tarragona.gpkg`, la taula `portalpk_publi` conté portals i punts quilomètrics. Cal conservar la procedència i les condicions IGN/CNIG amb els crèdits específics del producte.

| Camp observat | Funció en l’activitat |
| --- | --- |
| `id_porpk` | Identificador del registre d’origen |
| `tipo` | Distingeix `Portal` de `PK` |
| `cod_postal` | Categoria postal, conservada com a text |
| `ine_mun`, `municipio` | Atribució municipal declarada pel productor |
| `fuente_datos`, `fecha_modificacion` | Informació de procedència i actualització |

Table: Camps de la distribució utilitzada en el cas de Reus.

La font declara EPSG:4258. Per construir distàncies planes en metres cal preparar una còpia explícitament reprojectada a **EPSG:25831**, juntament amb un límit municipal documentat. Canviar només el CRS de la vista no transforma els punts.

Cada estudiant obté CartoCiudad i els límits del CNIG per a la cobertura del seu municipi. Es poden reutilitzar els originals descarregats a PR3 quan coincideixen producte, edició i àmbit. Es conserven els ZIP i les metadades, s’extreuen els GeoPackage i el Shapefile i s’inspeccionen abans de preparar el subconjunt amb entorn. El cas resolt de Reus serveix de referència del procediment.

# Procediment

## Inspeccionar els portals i definir els generadors

La primera consulta identifica els portals atribuïts administrativament a Reus:

```sql
"tipo" = 'Portal' AND "ine_mun" = '43123'
```

Cal contrastar nom municipal, nombre de registres, IDs i freqüència de codis. Aquesta selecció atributiva no demostra que tots els punts quedin geomètricament dins del terme. Els casos discordants es documenten abans de decidir-ne el tractament.

Una ubicació amb diverses adreces coincidents no necessita diversos dominis geomètrics idèntics. Si els registres comparteixen posició i codi, es pot preparar un generador únic amb un `id_generador` i conservar la correspondència amb els `id_porpk` originals. El recompte d’adreces continua sent diferent del recompte de generadors.

Si hi ha codis diferents a una mateixa posició, el conflicte no es resol desplaçant els punts artificialment. Cal revisar font i unitat d’observació i declarar una regla. Els codis desconeguts o conflictius es poden representar com a classe no assignada; excloure’ls per fer un mapa exigeix explicar com canvia el conjunt de generadors.

## Incloure l’entorn i controlar les vores

Els portals just fora del terme poden ser els més pròxims a posicions interiors. Per això la construcció utilitza un entorn de generadors més ampli que l’àrea d’informe. Es conserva el municipi com a màscara final, però no s’eliminen prèviament tots els punts externs només per la seva atribució administrativa.

El marge es documenta i es prova ampliant-lo. Comparar dues extensions permet observar sensibilitat de vora; no demostra per si sol que qualsevol generador omès sigui irrellevant. Una comprovació amb un conjunt territorial més complet reforça el control.

## Construir Delaunay i Voronoi

Des de la caixa de Processament es construeixen la **Triangulació de Delaunay** i els **Polígons de Voronoi** amb el mateix conjunt preparat. Cal registrar la versió de QGIS, les opcions de l’eina i la destinació persistent.

A Delaunay s’inspeccionen arestes, triangles de vora i relacions entre punts amb codis iguals o diferents. Una aresta no és un carrer ni una ruta de repartiment. Els triangles grans poden reflectir poca densitat d’observacions; no són automàticament errors. Les relacions amb els generadors s’han de contrastar amb els identificadors retornats per l’eina, sense suposar que un FID nou sigui l’ID d’origen.

El Voronoi s’ha de construir amb una extensió que cobreixi tot el municipi. Si l’extensió inicial de l’eina és massa petita, es configura l’ampliació corresponent i es comprova la cobertura. No s’afegeixen portals inventats a les cantonades per fer encaixar el resultat.

En la mateixa mètrica i sense degeneracions, les estructures són duals: les cel·les veïnes de Voronoi corresponen a generadors relacionats a Delaunay. No cal convertir el codi postal en un nombre continu per obtenir cap de les dues estructures.

## Retallar i dissoldre pel codi

El Voronoi es retalla pel terme municipal i es conserva una còpia amb `id_generador` i `cod_postal`. Després es dissol pel codi, amb la política explícita per a categories no assignades. Les zones poden tenir parts separades o enclavaments; no s’han de suavitzar només perquè semblin poc plausibles.

El mapa mostra les zones amb colors categòrics, els portals i el límit municipal. Convé identificar les àrees amb poca densitat de generadors i contrastar les fronteres inferides amb el patró de punts. La llegenda i el títol indiquen que és una zonificació aproximada basada en portals de l’edició utilitzada.

# Comprovacions i interpretació

| Control | Evidència |
| --- | --- |
| Preparació | Originals preservats, CRS mètric i taula de correspondència dels generadors |
| Partició | Cel·les vàlides, sense buits ni solapaments d’àrea no explicats dins del domini |
| Dissolució | Cobertura equivalent a la de les cel·les; codis textuals conservats |
| Vora | Comparació amb generadors externs i amb una extensió més àmplia |
| Suport | Zones allunyades de portals o amb codis rars identificades |
| Contrast | Resultats separats dels controls de construcció i de la validació independent |

Table: Controls del mapa de proximitat postal.

Que cada generador quedi a la zona del seu propi codi és una comprovació de consistència, no una prova independent d’exactitud. Per contrastar la classificació es reserven abans alguns portals o blocs espacials. Les ubicacions duplicades han de quedar al mateix grup de partició, per evitar que una còpia faci de validació d’una altra.

Es comparen el codi observat dels portals reservats i l’inferit pel model, amb recompte per codi i localització dels desacords. Un bon resultat sobre adreces no valida necessàriament els límits en espais sense portals. L’edició i la cobertura de CartoCiudad continuen limitant la conclusió.

# Aplicació al municipi escollit i ampliacions

El procediment es transfereix al municipi propi, preparant també el seu entorn. Cal conservar el criteri de coincidències i codis absents i explicar l’efecte de la densitat de portals. Com a ampliació es pot comparar l’agregació de portals en malles quadrades i hexagonals, variant mida i origen sense confondre densitat amb taxa.

Altres preguntes possibles són l’estabilitat de les fronteres amb un entorn més ampli o la variació del contrast amb diferents blocs reservats. En el primer cas es mesura la superfície que canvia de categoria dins del terme; en el segon, es comparen coincidències per codi i la posició dels desacords. Les ubicacions coincidents es mantenen al mateix grup i les particions es fixen abans de construir.

L’ampliació ha d’afegir una pregunta als apartats seleccionats: repetir una comparació ja obligatòria no genera puntuació addicional. La qualificació de PR4 manté **70/20/10**, fins a **7 punts bàsics, 2 d’ampliacions i 1 de documentació**. Els controls i la interpretació sustenten l’aportació; el percentatge de coincidències no determina automàticament la nota. Apunts, captures, mapa i organització contribueixen al bloc documental.

# Fitxers i evidències

Els resultats propis s’incorporen al GeoPackage de PR4 en capes amb noms com `portals_generadors`, `delaunay_portals`, `voronoi_portals` i `zones_cp_estimades`. La correspondència entre generadors i registres d’origen es conserva en una taula. La demostració de Reus es manté identificada com a cas de classe, separada del municipi propi.

El projecte incrustat `pr4`, el `.qgz` homònim i els apunts han de resoldre les noves capes. Es conserva una composició de la zonificació estimada i se n’exporta el PDF, amb el caràcter aproximat explícit al títol i a la llegenda. Els apunts inclouen descàrrega, preparació, decisió de marge, casos ambigus, controls i interpretació. Moodle concreta l’encaix a PR4, el calendari i la forma de lliurament.

# Referències

- [Tessel·lacions i geoprocessament, manual TIG](https://geourv.github.io/tig/ca/chapters/analisi-geoprocessament-vectorial/).
- [CartoCiudad Tarragona, CNIG](https://centrodedescargas.cnig.es/CentroDescargas/detalleArchivo?sec=9092).
- [Geometria vectorial, QGIS 3.44](https://docs.qgis.org/3.44/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html).
