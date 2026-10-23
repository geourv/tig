---
title: "PR4 · Guia docent de malles, proximitat postal i atlas"
lang: ca
recipient: docent
content_status: draft
subject: "Tecnologies de la Informació Geogràfica"
subject_code: "21234114"
author: "Benito Zaragozí"
institution: "Universitat Rovira i Virgili"
---

# Propòsit i seqüència docent

El taller segueix els mateixos portals a través de **malles regulars → Delaunay i arestes → Voronoi postal → atlas**. Cada estructura respon una pregunta: recompte per unitat, veïnatge, domini de proximitat o cobertura de pàgines. Les captures s’utilitzen al pas que expliquen, amb el resultat i la comprovació corresponents.

Reus és el cas de demostració; la transferència correspon al municipi propi. El codi postal es tracta com a categoria textual i la zonificació es descriu com a estimació per proximitat. Les agrupacions per llindar no es presenten com barris ni com connexions funcionals, i l’atlas no és només una successió d’imatges: conserva cobertura, ordre i layout editable.

# Preparació i conducció

| Component | Dedicació orientativa |
| --- | --- |
| Aula, malla i Delaunay amb llindars | 90–120 min |
| Aula, Voronoi postal i atlas | 90–120 min |
| Treball autònom i comprovacions | 150–210 min |
| Preparació docent | 60–90 min |

Table: Estimació del recorregut complet, pendent de contrast amb una classe.

L’estimació pressuposa PR3 validada, fonts descarregades i nocions de selecció i agregació. La reconstrucció manual d’arestes i correspondències necessita més temps que obrir el resultat resolt. Es poden repartir els blocs en dues sessions o seleccionar-ne una part, ajustant la càrrega total de PR4. Una validació per diversos marges o blocs afegeix treball.

Abans de la sessió es comproven els originals, el projecte, les connexions GeoPackage, el WMS i un cas de cada diagnòstic: ubicacions coincidents, punt aïllat, aresta llarga, codi minoritari i cel·la de vora. Les aturades demanen predir el resultat abans de veure’l. La primera distinció és registres versus ubicacions; l’última és configuració de l’atlas versus exportació revisada.

# Preparar Moodle

1. Incorporar el taller a la **Tasca de PR4**, amb el títol **Malles, proximitat postal i atlas**.
2. Copiar l’enunciat següent fins al final de «Qualificació» i concretar els apartats seleccionats. Indicar si són bàsics del 70% o una via d’ampliació del 20%.
3. Adjuntar el PDF d’alumnat a **Fitxers addicionals**. El cas resolt de Reus, si es comparteix, s’identifica com a exemple i inclou les dependències verificades.
4. Coordinar amb PR4 dates, tramesa i mida. Indicar si es demana atlas complet, mostra de pàgines o només una altra composició; la guia no imposa automàticament totes les exportacions.
5. Revisar la **vista d’estudiant**. El taller continua a la instantània PR4, sense setena fase ni segona nota sobre 10. El paquet docent es conserva per preparar i contrastar la sessió.

## Enunciat per copiar a la descripció

**Dades i objectiu.** Cal preparar portals de CartoCiudad i el límit CNIG del municipi, amb entorn exterior i un CRS mètric adequat. Reus és la demostració. El recorregut compara malles, veïnatges de Delaunay, zones postals estimades amb Voronoi i una cobertura regular per a atlas.

**Treball seleccionat.** El professor indica a classe i enumera en aquesta Tasca els apartats exigits i el seu encaix a PR4. Es conserven generadors, correspondències, paràmetres, resultats persistents i controls. Una malla requereix totals i regla de fronteres; les arestes, IDs i longituds; el Voronoi, cobertura i categories; l’atlas, cobertura, layout, ordre i exportació comprovada quan se seleccioni aquest bloc.

**Ampliacions possibles.** Cal desenvolupar una pregunta addicional al nucli seleccionat:

- Com canvia el patró en variar mida o origen de la malla? Mantenir els mateixos punts, conservar totals i separar escala de zonificació.
- Com canvien components i aïllats en variar la distància? Conservar el graf complet i contrastar efecte de cadena i barreres.
- És estable la zonificació postal amb un entorn més ampli? Mesurar superfície que canvia de categoria i localitzar-ne les causes.
- Com varia el contrast en reservar blocs espacials? Fixar la partició abans, mantenir juntes les ubicacions coincidents i informar de classes rares i desacords.
- Quina mida de cel·la és adequada per a un format i escala d’atlas? Justificar dimensions, nombre de pàgines i llegibilitat, amb una prova interior i una de vora.

**Documentació i lliurament.** Les capes pròpies s’incorporen al GeoPackage de PR4 i als seus projectes incrustat i extern. Es conserven la composició editable, els PDF seleccionats i els controls als apunts. Les conclusions diferencien proximitat geomètrica, delimitació oficial, accessibilitat i representació cartogràfica. El conjunt es reobre des d’una ubicació neta.

**Qualificació.** PR4 manté **70% treball bàsic, 20% ampliacions i 10% documentació**, fins a **7, 2 i 1 punts**. El taller es valora al bloc anunciat i cap evidència es compta dues vegades. Les ampliacions no substitueixen els obligatoris. Es valoren pregunta, correcció, controls i interpretació; un percentatge de coincidències o un nombre elevat de capes no garanteix una nota.

# Fonts i diagnòstic d’entrada

El cas complet utilitza CartoCiudad Tarragona 04/2026, `portalpk_publi`, i límits CNIG 07/2026. La font puntual és EPSG:4258 i la preparació es reprojecta a EPSG:25831. Reus té `NATCODE=34094343123`. El domini és el rectangle municipal ampliat almenys 1.500 m i arrodonit cap enfora a múltiples de 1.000 m.

La selecció atributiva `tipo=Portal` i `ine_mun=43123`, útil com a diagnòstic, retorna **17.483 registres** en l’original fixat. No és l’entrada completa del model: el domini ampli incorpora portals de l’entorn, amb independència de l’atribució municipal.

| Codi | Registres | Codi | Registres |
| --- | ---: | --- | ---: |
| 43110 | 1 | 43205 | 4.618 |
| 43201 | 2.498 | 43206 | 3.377 |
| 43202 | 1.319 | 43330 | 1 |
| 43203 | 1.494 | 43470 | 1 |
| 43204 | 4.169 | 43480 | 5 |

Table: Diagnòstic atributiu de la font; no és el recompte del domini de construcció.

En aquest subconjunt hi havia 54 grups de BLOB geomètric coincident, amb 388 registres i sense conflictes de codi, i 17.149 BLOB diferents. La igualtat binària prèvia no es presenta com el recompte definitiu de generadors després de reprojecció. El cas complet agrupa coordenades preparades exactes i obté **35.190 registres i 34.614 ubicacions**.

La taula `correspondencia` conserva `id_font`, `id_porpk`, `id_generador` i el codi original. El generador conserva `n_portals` i un codi textual o una categoria explícita de manca/conflicte. Eliminar geometries duplicades no agrega atributs: s’ha de recuperar el resum de tots els registres associats. Les categories minoritàries es diagnostiquen, no s’esborren per fer quadrar un mapa.

# Demostració de malles regulars

## Construcció i totals

S’obre `native:creategrid`: rectangle poligonal, domini fix, EPSG:25831, espaiaments iguals de 500 m i solapament zero. Es repeteix a 1.000 m amb el mateix origen. Les capes conserven cel·les buides, fila, columna i `id_cella`.

![Quadrícula regular sobre Reus](assets/img/qgis/qgis-c06-graella-resultat.png "La malla completa precedeix tant l’agregació com la selecció de pàgines d’atlas. El terme magenta no retalla automàticament les cel·les.")

El recompte de generadors dona `n_ubicacions`; la suma de `n_portals` dona registres. Les dues malles recuperen els totals respectius del domini. La pregunta d’aturada és què passa amb un punt sobre una aresta de cel·la: una unió per intersecció pot generar diverses parelles.

El cas resolt assigna cada punt amb índexs i intervals semioberts, amb el límit exterior final a l’última cel·la. Aquest control s’ha de conservar si es reconstrueix el procediment amb eines de recompte espacial. Les cel·les parcials d’un retall municipal no es comparen ingènuament amb les completes.

## MAUP i hexàgons

Comparar 500/1.000 m permet parlar d’escala; desplaçar un origen fix a igual mida permet parlar de zonificació. Els hexàgons són una alternativa regular amb sis veïns laterals equidistants, no una solució automàtica al MAUP. La comparació ha de controlar àrea de cel·la i origen. Els recomptes calculats d’aquesta fita corresponen a quadrícules; no s’hi atribueix una execució hexagonal.

# Demostració de Delaunay i agrupacions

## Arestes amb traça

La triangulació utilitza tots els generadors, tolerància zero i informació dels vèrtexs. La ruta manual transforma triangles a línies, explota segments i elimina duplicats. Una aresta interior participa habitualment en dos triangles; conservar totes dues còpies duplicaria la parella.

Els IDs dels extrems es reconstrueixen contra els generadors, amb una clau d’aresta que uneixi les còpies puntuals d’inici/final. Una unió pel més pròxim ha de retornar distància pràcticament zero. Els atributs d’un triangle no identifiquen directament cada segment. Es normalitzen parelles no dirigides i es recalcula `distancia_m`.

![Arestes del sector de comparació](assets/img/qgis/qgis-c06-delaunay-arestes.png "La inspecció manté punts, arestes i WMS. Una connexió geomètrica pot travessar una barrera que el model no representa.")

El cas resolt té **69.195 triangles** i **103.808 arestes úniques**. Els controls comparen IDs, multiplicitat 1/2 dels costats triangulars i longituds reconstruïdes a partir de coordenades. Un arrodoniment excessiu dels camps de distància pot fer fallar el contrast; la precisió d’emmagatzematge no és l’exactitud de CartoCiudad.

## Llindar, cadena i aïllats

S’extreuen arestes de fins a 25, 50 i 100 m sense perdre la capa completa. Un component és un conjunt connectat per cadenes; no exigeix que totes les parelles del grup quedin dins del llindar. Els punts sense arestes són components d’una ubicació i han de continuar al recompte.

| Llindar | Arestes | Components | Aïllats |
| --- | ---: | ---: | ---: |
| 25 m | 53.237 | 6.810 | 5.074 |
| 50 m | 78.132 | 3.098 | 2.355 |
| 100 m | 92.649 | 1.323 | 916 |

Table: Comparació sobre un conjunt de generadors constant.

![Components a cinquanta metres](assets/img/qgis/qgis-c06-delaunay-llindar.png "Els colors agrupen mides de components, no identitats de clúster. Cal mostrar una cadena llarga i un punt aïllat abans d’interpretar el patró.")

La comprovació independent calcula el graf de totes les parelles dins de cada radi amb un índex de proximitat i compara pertinença als components, sense reutilitzar la llista d’arestes de Delaunay. Les tres particions coincideixen en aquest cas. Aquest control no converteix Delaunay en una matriu exhaustiva de distàncies.

Com a ruta GUI, `native:dbscanclustering` amb `MIN_SIZE=1`, `EPS=50` i DBSCAN* desactivat coincideix amb els components de 50 m. Totes les ubicacions poden ser nucli i els aïllats es conserven. Amb un mínim superior cal explicar densitat, vora i soroll; no es manté la mateixa interpretació. Les etiquetes es comparen per membres, no pels IDs numèrics.

# Demostració de Voronoi postal

## Extensió, atributs i dissolució

El diagrama utilitza els mateixos generadors complets. A `native:voronoipolygons`, `BUFFER=100` amplia percentualment l’extensió, no 100 metres. Es conserven atributs, es comprova cobertura i es retalla pel terme. El cas obté **17.318 cel·les retallades**.

![Voronoi al sector de comparació](assets/img/qgis/qgis-c06-reus-voronoi-resultat.png "La posició dels generadors externs pot condicionar cel·les interiors. El retall municipal es fa després de construir el diagrama.")

Es dissol per `cod_postal`, conservat com a text. La capa de cel·les identificables es manté per diagnosticar zones i enclavaments. Hi ha **15 categories**: 43006, 43110, 43120, 43201–43206, 43330, 43381, 43392, 43393, 43470 i 43480.

![Zonificació postal estimada](assets/img/qgis/qgis-c06-reus-codis-postals.png "El mapa és una estimació de proximitat derivada dels portals. Els codis rars requereixen rastrejar la font i el suport territorial, no eliminar la categoria.")

Els controls de la fita comproven validesa, cobertura municipal i disjunció d’interiors de cel·les i zones. Cal afegir a la lectura docent la relació generador–codi, els efectes de vora i la distinció entre consistència de construcció i validació postal independent. Les fronteres no són oficials i no s’infereixen rutes de repartiment.

## Contrast amb blocs reservats: antecedent separat

El cas anterior de Reus, conservat com a experiment de validació, amplia el rectangle 1.500 m i el contrasta amb 3.000 m. L’entorn ampli conté 47.862 portals. La partició reserva un de cada cinc blocs de 500 m, mantenint juntes les ubicacions coincidents; el model principal utilitza 23.968 generadors d’entrenament i el contrast ampli, 37.156.

| Resultat de l’experiment anterior | Valor |
| --- | ---: |
| Triangles | 47.918 |
| Cel·les retallades | 13.198 |
| Categories dissoltes | 14 |
| Ubicacions reservades dins de Reus | 4.092 |
| Coincidències amb el codi observat | 3.435 |
| Proporció de coincidències | 83,94% |

Table: Resultats de la partició de validació anterior, diferents del model complet actual.

En aquell experiment els dos marges donaven les mateixes categories dins del terme, amb la tolerància declarada. El **83,94% no és una validació del mapa complet de 15 categories** ni una mesura d’exactitud de fronteres en espais sense portals. Cada experiment conserva preparació, partició i sortides pròpies. Una nova validació fixa els blocs abans de construir i informa de classes rares, punts no avaluables i desacords cartografiats.

# Pràctica guiada d’atlas

## Cobertura, identitats i ordre

La malla d’1 km es filtra per intersecció d’àrea positiva amb Reus i conserva quadrats sencers. `cobertura_atlas` té **82 entitats**. `id_cella` identifica; `pagina` ordena. L’ordre és de nord a sud i d’oest a est, amb numeració consecutiva i sense dependre dels FID.

![Cobertura numerada de l’atlas](assets/img/qgis/qgis-c06-atlas-cobertura.png "Les cel·les perifèriques mantenen la forma quadrada i inclouen entorn exterior. Retallar-les canviaria la relació entre cobertura i enquadrament.")

La reconstrucció pot afegir un camp autoincremental ordenant amb `-"fila" * 100000 + "columna"`, inici 1, després de comprovar el domini de columnes i que la fila augmenta cap al nord. Es revisen primer i últim ID i la cobertura de tot el municipi.

## Relació cel·la–marc–escala

El layout **Atlas de tessel·les de Reus** utilitza A4 vertical, 210 × 297 mm. El mapa `mapa_atlas` té 200 × 200 mm, a X=5 i Y=40 mm, EPSG:25831, rotació zero i escala fixa 1:5.000. El producte de 200 mm per 5.000 equival a 1.000 m sobre el terreny.

Al panell Atlas s’activa la generació, s’escull la cobertura, el nom de pàgina `id_cella`, l’ordre ascendent `pagina` i el nom de fitxer `'reus_' || "id_cella"`. A les propietats del **mapa** s’activa separadament **Controlat per atlas** i l’escala fixa. Aquesta doble vinculació és el punt de diagnòstic principal si les pàgines canvien de títol però mostren sempre el mateix mapa.

La composició inclou títol amb `@atlas_pagename`, paginació amb `@atlas_featurenumber` i `@atlas_totalfeatures`, CRS, escala, nord i fonts. Les capes del mapa es fixen i es comprova una pàgina interior i una de vora. El WMS de l’escena online necessita servei disponible; el projecte científic reobert utilitza dependències locals.

## Previsualització i exportació

La previsualització ha de canviar entitat, títol i extensió mantenint escala i dimensions. Cal observar primera, última, interior i vora. Es desa la composició i es tornen a obrir projecte incrustat i extern per verificar-ne la persistència.

![Algorisme d’exportació d’atlas a PDF](assets/img/qgis/qgis-c06-atlas-configuracio.png "El diàleg mostra paràmetres d’exportació. No és una captura del compositor ni una prova d’un PDF multipàgina ja generat.")

Des del compositor o amb `native:atlaslayouttopdf` s’exporta un atlas, no un layout estàtic. Si s’indica una cobertura al diàleg de Processament, cal tornar a fixar l’ordre i qualsevol filtre, perquè substitueixen els del layout. Amb una pàgina de disseny i 82 cel·les s’espera un PDF de 82 pàgines: es comprova al fitxer reobert, juntament amb noms, extents, escala i fonts.

El cas retingut acredita la configuració i la iteració nativa de les **82 entitats**, amb noms únics, ordre i coincidència d’enquadrament amb cada quadrat. Aquesta evidència no substitueix la inspecció del PDF final ni la navegació visual del compositor que es demostra a classe.

# Controls, transferència i paquets

El cas complet té **80 controls** de fonts, geometries, CRS, identitats, malles, graf, Voronoi i atlas. Els originals mantenen els hashes i els projectes s’han reobert. Les fonts d’autoria, els inputs preparats i els bundles es retenen; el paquet resolt de demostració no substitueix la cadena pròpia PR1–PR6.

| Bloc | Diagnòstic que cal demanar |
| --- | --- |
| Generadors | Distingir adreça, fila original i ubicació |
| Malla | Reconstruir totals i explicar una frontera de cel·la |
| Graf | Identificar una parella, una cadena i un aïllat |
| Postal | Rastrejar un codi minoritari i una zona poc sustentada |
| Atlas | Justificar escala i comprovar una pàgina de vora |
| Lliurament | Reobrir dades, projectes, layout i PDF seleccionats |

Table: Punts de comprovació de la sessió.

La transferència manté preguntes i controls, sense imposar els recomptes de Reus. Les capes pròpies s’incorporen a PR4, amb projecte incrustat, `.qgz`, composició i apunts coherents. La correcció tècnica i la persistència es valoren al bloc de treball seleccionat; la claredat del mapa i la documentació, al 10%, sense doble recompte.

# Referències

El [manual TIG](https://geourv.github.io/tig/ca/chapters/analisi-geoprocessament-vectorial/) desenvolupa els conceptes i el [CNIG](https://centrodedescargas.cnig.es/CentroDescargas/detalleArchivo?sec=9092) proporciona CartoCiudad Tarragona. La documentació QGIS 3.44 descriu la [geometria vectorial](https://docs.qgis.org/3.44/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html), la [generació d’atlas](https://docs.qgis.org/3.44/en/docs/user_manual/print_layout/create_output.html#generate-an-atlas) i l’[exportació a PDF](https://docs.qgis.org/3.44/en/docs/user_manual/processing_algs/qgis/cartography.html#export-atlas-layout-as-pdf-single-file).
