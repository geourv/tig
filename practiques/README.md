---
title: "Pràctiques municipals de TIG"
lang: ca
content_status: draft
---

# Pràctiques de TIG

**16 lectures PDF vigents per a revisió local, 172 pàgines i 10 paquets GIS verificats**: els vuit casos del recorregut i els dos complementaris de ROI/Reus. Dotze lectures corresponen a `2026-10-v1`, aprovada per l’autor el 18/10/2026; les quatre de PR4/Reus corresponen a `2026-10-vector-r2` i continuen en esborrany. Les guies docents inclouen preparació de la sessió, enunciats per copiar a Moodle i criteris 70–20–10.

L'autor ha aprovat publicar el manual actual a `latest` i ha confirmat mantenir
les quatre guies noves en esborrany. Les captures de la sèrie d'atles continuen
a [#37](https://github.com/geourv/tig/issues/37), primera tasca després de
l'actualització del capturador.

El recorregut ampliat incorpora descàrrega d’originals CNIG, metadades, preparació pròpia i composicions. Els paquets serveixen al professorat i es poden compartir com a exemples identificats. Vila-seca és el cas principal i Reus aporta les tessel·lacions de PR4. La [micropràctica PR1 confirmada a Moodle](pr1-project-setup/revisio/moodle-confirmed-2026-10-18/README.md) té un abast propi, explicat a les dues lectures PR1: composicions opcionals i requisits independents de la font CNIG, l’EPSG o un segon PDF.

## Índex vigent dels materials locals · 22/10/2026

| Activitat | PDF d’alumnat | PDF docent | Versió i estat |
| --- | --- | --- | --- |
| PR1 · Projecte municipal | [8 pàgines](../sandbox/practiques/pr1-project-setup/lectura-2026-10-v1-ca-alumnat-primera-01/outputs/LLEGIU-ME.pdf) | [9 pàgines](../sandbox/practiques/pr1-project-setup/lectura-2026-10-v1-ca-docent-primera-01/outputs/LLEGIU-ME.pdf) | v1 · aprovada |
| PR2 · Digitalització | [6 pàgines](../sandbox/practiques/pr2-digitalitzacio/lectura-2026-10-v1-ca-alumnat-primera-01/outputs/LLEGIU-ME.pdf) | [6 pàgines](../sandbox/practiques/pr2-digitalitzacio/lectura-2026-10-v1-ca-docent-primera-01/outputs/LLEGIU-ME.pdf) | v1 · aprovada |
| PR3 · Consultes | [7 pàgines](../sandbox/practiques/pr3-consultes/lectura-2026-10-v1-ca-alumnat-primera-01/outputs/LLEGIU-ME.pdf) | [8 pàgines](../sandbox/practiques/pr3-consultes/lectura-2026-10-v1-ca-docent-primera-01/outputs/LLEGIU-ME.pdf) | v1 · aprovada |
| PR4 · Envolupants i geoprocessament | [27 pàgines](../sandbox/practiques/pr4-geoprocessament/lectura-2026-10-vector-r2-ca-alumnat-revisio-02/outputs/LLEGIU-ME.pdf) | [23 pàgines](../sandbox/practiques/pr4-geoprocessament/lectura-2026-10-vector-r2-ca-docent-revisio-02/outputs/LLEGIU-ME.pdf) | vector-r2 · esborrany |
| Reus · Malles, proximitat postal i atles | [23 pàgines](../sandbox/practiques/pr4-tessellacions-reus/lectura-2026-10-vector-r2-ca-alumnat-revisio-01/outputs/LLEGIU-ME.pdf) | [18 pàgines](../sandbox/practiques/pr4-tessellacions-reus/lectura-2026-10-vector-r2-ca-docent-revisio-02/outputs/LLEGIU-ME.pdf) | vector-r2 · esborrany |
| PR5 · Ràster | [7 pàgines](../sandbox/practiques/pr5-raster/lectura-2026-10-v1-ca-alumnat-primera-01/outputs/LLEGIU-ME.pdf) | [7 pàgines](../sandbox/practiques/pr5-raster/lectura-2026-10-v1-ca-docent-primera-01/outputs/LLEGIU-ME.pdf) | v1 · aprovada |
| PR6 · Model i síntesi | [6 pàgines](../sandbox/practiques/pr6-sintesi/lectura-2026-10-v1-ca-alumnat-primera-01/outputs/LLEGIU-ME.pdf) | [7 pàgines](../sandbox/practiques/pr6-sintesi/lectura-2026-10-v1-ca-docent-primera-01/outputs/LLEGIU-ME.pdf) | v1 · aprovada |
| Bonus · PyQGIS/SQL | [5 pàgines](../sandbox/practiques/bonus-pyqgis-sql/lectura-2026-10-v1-ca-alumnat-primera-01/outputs/LLEGIU-ME.pdf) | [5 pàgines](../sandbox/practiques/bonus-pyqgis-sql/lectura-2026-10-v1-ca-docent-primera-01/outputs/LLEGIU-ME.pdf) | v1 · aprovada |

Table: Selecció local que coincideix amb les fonts editables actuals; 81 pàgines aprovades i 91 en esborrany.

La [verificació del 22/10](../sandbox/practiques/materials-readiness-20261022-01.json)
comprova els 16 PDF, snapshots i artefactes dels rebuts, dimensions A4 horitzontals,
estat editorial, recomptes i límits de text. El verificador públic QGIS 0.6.1
accepta els deu arbres GIS complets i les seleccions de projecte resolt.
Els set imports de la micropràctica PR1 confirmada conserven els hashes.
Les dades i els projectes són als [casos docents](#dades-projectes-i-mapes-docents)
i als [complementaris ROI/Reus](#revisió-de-pr4-i-reus--esborrany-2026-10-vector-r2).

La composició d’una nova edició de distribució PDF/ZIP requereix les lectures
aprovades i les seleccions GIS explícites del compositor compartit. Aquest índex
permet revisar els materials retinguts i identificar-ne la versió exacta.

La integració de les instruccions i definicions de correcció amb Unaltramesa
es completa en la [tasca #35](https://github.com/geourv/tig/issues/35), respectant
l’edició PR1 congelada. L’inventari actual cobreix les lectures i els casos GIS.

La reparació de l’atles té [acceptació local al proveïdor](https://github.com/dosquartsdedocs/unaltracaptura-qgis/issues/27#issuecomment-6329069144),
però encara falta la release i l’adopció de família per completar les captures
de Reus. La [migració del web](https://github.com/geourv/tig/issues/36) està preparada
amb els conflictes i la coherència dels pins pendents de resoldre.

## Revisió de PR4 i Reus · esborrany `2026-10-vector-r2`

El capítol 6 i les quatre guies s'han reordenat en envolupants, distàncies,
buffer/ROI, superposicions, punts, malles, Delaunay, Voronoi postal i atlas.
Les captures acompanyen cada concepte; els contorns conserven els colors del
WMS i els punters tenen caixes visibles. Les fonts continuen en `draft`.

| Lectura de revisió | Alumnat | Professorat |
| --- | --- | --- |
| PR4 · Envolupants i geoprocessament | [PDF · 27 p.](../sandbox/practiques/pr4-geoprocessament/lectura-2026-10-vector-r2-ca-alumnat-revisio-02/outputs/LLEGIU-ME.pdf) | [PDF · 23 p.](../sandbox/practiques/pr4-geoprocessament/lectura-2026-10-vector-r2-ca-docent-revisio-02/outputs/LLEGIU-ME.pdf) |
| Reus · Malles, proximitat postal i atlas | [PDF · 23 p.](../sandbox/practiques/pr4-tessellacions-reus/lectura-2026-10-vector-r2-ca-alumnat-revisio-01/outputs/LLEGIU-ME.pdf) | [PDF · 18 p.](../sandbox/practiques/pr4-tessellacions-reus/lectura-2026-10-vector-r2-ca-docent-revisio-02/outputs/LLEGIU-ME.pdf) |

Table: Quatre PDF locals de revisió, 91 pàgines, A4 horitzontal i marca ESBORRANY.

- [Cas ROI amb envolupants](pr4-geoprocessament/roi/README.md):
  [carpeta completa](../sandbox/practiques/pr4-geoprocessament/roi-run-20261020-04/),
  [projecte resolt](../sandbox/practiques/pr4-geoprocessament/roi-run-20261020-04/payload/projects/pr4-roi-exemple.qgz), 143 controls.
- [Cas Reus complet](pr4-tessellacions-reus/cas/README.md):
  [carpeta completa](../sandbox/practiques/pr4-tessellacions-reus/tesselles-run-20261020-04/),
  [projecte resolt](../sandbox/practiques/pr4-tessellacions-reus/tesselles-run-20261020-04/payload/projects/reus-tesselles.qgz), 80 controls.

Hi ha 33 conjunts de captura. El projecte d'atlas conserva 82 cel·les,
ordre i enquadraments comprovats. La captura del compositor i l'exportació
PDF multipàgina encara requereixen suport comprovat del proveïdor; el diàleg
d'exportació no es presenta com a prova d'un fitxer produït.

### Revisió r1 rebutjada editorialment i retinguda

La revisió `2026-10-roi-r1` desenvolupa la ROI CNIG, la preparació de punts,
línies i polígons, les diferències, les parts i els punts derivats. Reutilitza
les captures del capítol 6, amb les connexions GeoPackage visibles i el WMS
IGN/PNOA sota els vectors. L'autor la va rebutjar per l'ordre i la inserció
de les captures; els resultats es conserven com a antecedent.

- [Lectura d'alumnat · 21 pàgines](../sandbox/practiques/pr4-geoprocessament/lectura-2026-10-roi-r1-ca-alumnat-revisio-01/outputs/LLEGIU-ME.pdf).
- [Guia docent · 18 pàgines](../sandbox/practiques/pr4-geoprocessament/lectura-2026-10-roi-r1-ca-docent-revisio-02/outputs/LLEGIU-ME.pdf).
- [Fonts i reproducció del cas complementari](pr4-geoprocessament/roi/README.md).
- [Projecte QGIS resolt](../sandbox/practiques/pr4-geoprocessament/roi-run-20261019-03/payload/projects/pr4-roi-exemple.qgz), amb [carpeta completa](../sandbox/practiques/pr4-geoprocessament/roi-run-20261019-03/) i 131 controls.

Els PDF de la primera versió continuen aprovats i retenen les fonts exactes
d'aquella fita. Les fonts editables PR4 i Reus enllaçades a continuació
corresponen ara a l'esborrany nou, no als snapshots aprovats dels PDF v1.

## Lectures aprovades de la primera versió

| Pràctica | Alumnat | Professorat |
| --- | --- | --- |
| PR1 · Projecte municipal i recorregut CNIG | [PDF · 8 p.](../sandbox/practiques/pr1-project-setup/lectura-2026-10-v1-ca-alumnat-primera-01/outputs/LLEGIU-ME.pdf) · [Font](pr1-project-setup/ca/alumnat/LLEGIU-ME.md) | [PDF · 9 p.](../sandbox/practiques/pr1-project-setup/lectura-2026-10-v1-ca-docent-primera-01/outputs/LLEGIU-ME.pdf) · [Font](pr1-project-setup/ca/docent/LLEGIU-ME.md) |
| PR2 · Digitalització | [PDF · 6 p.](../sandbox/practiques/pr2-digitalitzacio/lectura-2026-10-v1-ca-alumnat-primera-01/outputs/LLEGIU-ME.pdf) · [Font](pr2-digitalitzacio/ca/alumnat/LLEGIU-ME.md) | [PDF · 6 p.](../sandbox/practiques/pr2-digitalitzacio/lectura-2026-10-v1-ca-docent-primera-01/outputs/LLEGIU-ME.pdf) · [Font](pr2-digitalitzacio/ca/docent/LLEGIU-ME.md) |
| PR3 · Consultes i expressions | [PDF · 7 p.](../sandbox/practiques/pr3-consultes/lectura-2026-10-v1-ca-alumnat-primera-01/outputs/LLEGIU-ME.pdf) · [Font](pr3-consultes/ca/alumnat/LLEGIU-ME.md) | [PDF · 8 p.](../sandbox/practiques/pr3-consultes/lectura-2026-10-v1-ca-docent-primera-01/outputs/LLEGIU-ME.pdf) · [Font](pr3-consultes/ca/docent/LLEGIU-ME.md) |
| PR4 · Buffers, superposicions i ROI | [PDF · 7 p.](../sandbox/practiques/pr4-geoprocessament/lectura-2026-10-v1-ca-alumnat-primera-01/outputs/LLEGIU-ME.pdf) · [Font](pr4-geoprocessament/ca/alumnat/LLEGIU-ME.md) | [PDF · 7 p.](../sandbox/practiques/pr4-geoprocessament/lectura-2026-10-v1-ca-docent-primera-01/outputs/LLEGIU-ME.pdf) · [Font](pr4-geoprocessament/ca/docent/LLEGIU-ME.md) |
| Reus · Delaunay, Voronoi i codis postals | [PDF · 6 p.](../sandbox/practiques/pr4-tessellacions-reus/lectura-2026-10-v1-ca-alumnat-primera-01/outputs/LLEGIU-ME.pdf) · [Font](pr4-tessellacions-reus/ca/alumnat/LLEGIU-ME.md) | [PDF · 7 p.](../sandbox/practiques/pr4-tessellacions-reus/lectura-2026-10-v1-ca-docent-primera-01/outputs/LLEGIU-ME.pdf) · [Font](pr4-tessellacions-reus/ca/docent/LLEGIU-ME.md) |
| PR5 · Ràster i relleu | [PDF · 7 p.](../sandbox/practiques/pr5-raster/lectura-2026-10-v1-ca-alumnat-primera-01/outputs/LLEGIU-ME.pdf) · [Font](pr5-raster/ca/alumnat/LLEGIU-ME.md) | [PDF · 7 p.](../sandbox/practiques/pr5-raster/lectura-2026-10-v1-ca-docent-primera-01/outputs/LLEGIU-ME.pdf) · [Font](pr5-raster/ca/docent/LLEGIU-ME.md) |
| PR6 · Model i síntesi | [PDF · 6 p.](../sandbox/practiques/pr6-sintesi/lectura-2026-10-v1-ca-alumnat-primera-01/outputs/LLEGIU-ME.pdf) · [Font](pr6-sintesi/ca/alumnat/LLEGIU-ME.md) | [PDF · 7 p.](../sandbox/practiques/pr6-sintesi/lectura-2026-10-v1-ca-docent-primera-01/outputs/LLEGIU-ME.pdf) · [Font](pr6-sintesi/ca/docent/LLEGIU-ME.md) |
| Bonus · PyQGIS i SQL | [PDF · 5 p.](../sandbox/practiques/bonus-pyqgis-sql/lectura-2026-10-v1-ca-alumnat-primera-01/outputs/LLEGIU-ME.pdf) · [Font](bonus-pyqgis-sql/ca/alumnat/LLEGIU-ME.md) | [PDF · 5 p.](../sandbox/practiques/bonus-pyqgis-sql/lectura-2026-10-v1-ca-docent-primera-01/outputs/LLEGIU-ME.pdf) · [Font](bonus-pyqgis-sql/ca/docent/LLEGIU-ME.md) |

Table: Primera versió aprovada de les lectures, 108 pàgines en total.

## Conducció, Moodle i qualificació

Cada guia docent inclou temps orientatius d’aula, treball autònom i preparació, punts de comprovació i una secció **Preparar Moodle**. El bloc **Enunciat per copiar a la descripció** va de dades i objectiu fins a qualificació. El professor hi concreta l’abast comunicat a classe; PR1 respecta els requisits de l’edició confirmada. L’adjunt ordinari és el PDF d’alumnat; calendari i tramesa es concreten a la Tasca.

La qualificació té màxims de **7 punts pel treball bàsic, 2 per ampliacions i 1 per documentació**. Les propostes d’ampliació inclouen pregunta, comparació i controls: escales cartogràfiques, qualitat de captura, casos de frontera, cobertura zero, sensibilitat del marge, llindars ràster o parametrització del model. Reus es vincula a PR4 i el bonus al 20% de la pràctica indicada, sense doble recompte. La documentació també pot augmentar la nota sobre el bloc bàsic.

## Dades, projectes i mapes docents

Els paquets són **carpetes completes segellades pel productor**, preparades per a revisió local. Cal conservar-ne l’estructura; el `.qgz` sol no conté les dades. Per modificar un projecte es treballa sobre una còpia completa nova del paquet, mantenint intacta la referència verificada.

| Cas | Paquet complet | Projecte resolt | Mapa de revisió | Controls |
| --- | --- | --- | --- | ---: |
| PR1 | [Carpeta](../sandbox/practiques/pr1-project-setup/run-cnig-01/) | [QGIS](../sandbox/practiques/pr1-project-setup/run-cnig-01/payload/projects/pr1-project-setup-exemple.qgz) | [PDF](../sandbox/practiques/pr1-project-setup/run-cnig-01/payload/figures/mapa-revisio.pdf) | 20 |
| PR2 · sintètica | [Carpeta](../sandbox/practiques/pr2-digitalitzacio/run-cnig-01/) | [QGIS](../sandbox/practiques/pr2-digitalitzacio/run-cnig-01/payload/projects/pr2-digitalitzacio-exemple.qgz) | [PDF](../sandbox/practiques/pr2-digitalitzacio/run-cnig-01/payload/figures/mapa-revisio.pdf) | 27 |
| PR3 | [Carpeta](../sandbox/practiques/pr3-consultes/run-cnig-02/) | [QGIS](../sandbox/practiques/pr3-consultes/run-cnig-02/payload/projects/pr3-consultes-exemple.qgz) | [PDF](../sandbox/practiques/pr3-consultes/run-cnig-02/payload/figures/mapa-revisio.pdf) | 46 |
| PR4 | [Carpeta](../sandbox/practiques/pr4-geoprocessament/run-cnig-03/) | [QGIS](../sandbox/practiques/pr4-geoprocessament/run-cnig-03/payload/projects/pr4-geoprocessament-exemple.qgz) | [PDF](../sandbox/practiques/pr4-geoprocessament/run-cnig-03/payload/figures/mapa-revisio.pdf) | 71 |
| Reus | [Carpeta](../sandbox/practiques/pr4-tessellacions-reus/run-cnig-04/) | [QGIS](../sandbox/practiques/pr4-tessellacions-reus/run-cnig-04/payload/projects/pr4-tessellacions-reus-exemple.qgz) | [PDF](../sandbox/practiques/pr4-tessellacions-reus/run-cnig-04/payload/figures/mapa-revisio.pdf) | 31 |
| PR5 | [Carpeta](../sandbox/practiques/pr5-raster/run-cnig-02/) | [QGIS](../sandbox/practiques/pr5-raster/run-cnig-02/payload/projects/pr5-raster-exemple.qgz) | [PDF](../sandbox/practiques/pr5-raster/run-cnig-02/payload/figures/mapa-revisio.pdf) | 125 |
| PR6 | [Carpeta](../sandbox/practiques/pr6-sintesi/run-cnig-01/) | [QGIS](../sandbox/practiques/pr6-sintesi/run-cnig-01/payload/projects/pr6-sintesi-exemple.qgz) | [PDF](../sandbox/practiques/pr6-sintesi/run-cnig-01/payload/figures/mapa-revisio.pdf) | 127 |
| Bonus | [Carpeta](../sandbox/practiques/bonus-pyqgis-sql/run-cnig-02/) | [QGIS](../sandbox/practiques/bonus-pyqgis-sql/run-cnig-02/payload/projects/bonus-pyqgis-sql-exemple.qgz) | [PDF](../sandbox/practiques/bonus-pyqgis-sql/run-cnig-02/payload/figures/mapa-revisio.pdf) | 144 |

Table: Vuit casos executats amb el productor QGIS, amb 591 controls i reobertures sense xarxa.

Cada carpeta conserva els GeoPackage i ràsters a `payload/data/`, originals i fonts executades a `payload/sources/`, captures i controls, i el manifest `bundle.json`. Els ZIP CNIG originals formen part dels inputs retinguts. El [procediment de reproducció](recorregut-municipal/README.md) identifica els requests, els hashes i els límits dels casos.

Fonts d’exemple: [model PR6](recorregut-municipal/pr6_roi_municipal.model3), [PyQGIS](recorregut-municipal/bonus_roi.py), [SQLite](recorregut-municipal/bonus_portals.sql) i [PostGIS](recorregut-municipal/bonus_postgis.sql). Els snapshots exactes utilitzats en cada execució es conserven també al seu paquet.

## Límits dels casos docents

- **PR2:** el cas disponible és sintètic —3 punts, 3 línies i 2 polígons— i conserva `no_apte_per_analisi`. Calen observacions revisades per disposar d’un inventari territorial real. El context PNOA local és de 6,59 m/píxel i no serveix per a captura fina.
- **Composicions:** hi ha mapes editables i PDF de revisió. El perfil del productor encara limita la composició a mapes i text; la llegenda nativa i l’escala gràfica queden per completar amb suport verificat. Reus incorpora una clau de colors i PR5, dos marcs comparables.
- **PR6:** el model extern s’ha executat sobre Vila-seca i Reus. El desament del model dins de les representacions del projecte continua sent una comprovació separada.
- **Fonts i ampliacions:** les instruccions d’ATOM cadastral i de contrast amb inundabilitat són a les lectures; aquests paquets no incorporen una nova descàrrega cadastral ni una capa específica d’inundabilitat. El bonus executa PyQGIS i SQLite; PostGIS és un exemple de codi sense execució de servidor acreditada.

## Continuïtat i retenció

La successió manté sis instantànies principals; Reus és una activitat de PR4 i el bonus és opcional. Les fases conserven físicament les capes heretades i PR6 manté els deu GeoTIFF de PR5 byte per byte. El projecte incrustat i l’extern es desen i comproven separadament.

Markdown, codi, models d’autoria i requests són versionables. Les tres carpetes d’inputs del pilot, PR1 històrica i recorregut municipal s’ignoren per carpeta; `sandbox/` i `dist/practiques/` cobreixen jobs i productes. La reserva exacta dels paths d’edició continua als plans. Les dades i els artefactes es retenen encara que Git els ignori.

L’[inventari de retenció](../context/practiques/lliuraments.md) recull versions, hashes, seleccions, incidències i proves. L’edició PR1 `2026-10-review-r1`, basada en ICGC, queda superada i es conserva com a antecedent. També es mantenen els primers PDF, els intents refusats i el [pilot de buffer de 500 m](tig-buffer-municipal-500m/README.md).

L’autor ha aprovat aquesta primera versió de les activitats. Els enllaços a PDF i dades són locals i requereixen conservar els jobs; la distribució efectiva per Moodle utilitza una selecció explícita dels materials pertinents. Les carpetes de pràctiques i d’execució estan excloses del web públic del manual.
