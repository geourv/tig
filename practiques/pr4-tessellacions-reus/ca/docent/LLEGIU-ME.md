---
title: "PR4 · Guia docent de Delaunay, Voronoi i codis postals de Reus"
lang: ca
recipient: docent
content_status: approved
subject: "Tecnologies de la Informació Geogràfica"
subject_code: "21234114"
author: "Benito Zaragozí"
institution: "Universitat Rovira i Virgili"
---

# Propòsit i enunciat

L’activitat connecta els portals consultats a PR3 amb les tessel·lacions de PR4. L’encàrrec és construir i justificar una zonificació postal aproximada de Reus, comparant Delaunay i Voronoi i fent visibles preparació, efectes de vora i extrapolació. El mateix procediment es transfereix al municipi propi.

El resultat essencial combina generadors auditats, les dues estructures, zones dissoltes pel codi, mapa i controls. Les ampliacions poden estudiar sensibilitat del marge, validació per blocs o malles regulars. No substitueixen la traça entre registres originals i generadors.

# Preparació i conducció del taller

| Component | Durada orientativa |
| --- | --- |
| Aula, preparació i tessel·lacions | 120–150 min |
| Treball autònom i interpretació | 90–150 min |
| Preparació docent | 45–60 min |

Table: Estimació del taller de tessel·lacions dins de PR4.

Estimació pendent de contrast amb una classe, amb consultes de PR3 compreses i originals identificats. El còmput inclou un entorn acotat; una validació per diversos blocs o municipis requereix més dedicació. No s’afegeix aquest temps a PR4 sense ajustar-ne la planificació.

Abans de classe es comproven codis, coincidències i extensió de construcció. Convé comparar un generador aïllat amb un grup dens i demanar on s’espera una cel·la gran. Les aturades són registres versus generadors, cobertura municipal i lectura de la frontera inferida. Si es fa validació, la partició es fixa abans de construir el model; classificar els propis generadors no constitueix un contrast independent.

# Preparar Moodle

1. Incorporar el taller a la **Tasca de PR4**, amb el títol **Tessel·lacions i zonificació postal aproximada** dins de la descripció.
2. Copiar l’enunciat següent fins al final de «Qualificació». Indicar si els apartats seleccionats compten dins del 70% bàsic o si el taller és una ampliació del 20%. Si és bàsic, les extensions han d’aportar una pregunta addicional.
3. Adjuntar a **Fitxers addicionals** el PDF d’alumnat de Reus. El municipi propi i les fonts que cal obtenir queden identificats; el cas resolt de Reus, si s’ofereix, s’etiqueta com a exemple.
4. Coordinar data, forma de tramesa i mida amb PR4. Les capes s’incorporen al seu GeoPackage; el taller no crea una setena instantània ni una segona nota sobre 10 per defecte.
5. Revisar la **vista d’estudiant** i comprovar que l’encaix amb la qualificació de PR4 sigui inequívoc. Conservar el paquet docent per a la preparació i el contrast.

## Enunciat per copiar a la descripció

**Dades i objectiu.** Cal preparar portals de CartoCiudad i límit CNIG, amb un entorn de generadors, i construir Delaunay i Voronoi. Reus és la demostració; el treball propi correspon al municipi escollit. La dissolució per codi postal dona una zonificació estimada per proximitat, no una delimitació oficial.

**Treball seleccionat.** El professor indica a classe i recull en aquesta Tasca els apartats exigits i el seu encaix a PR4. El recorregut inclou preparació i correspondència d’IDs, tessel·lacions sobre els mateixos generadors, retall, dissolució, mapa i controls de cobertura i vora. La guia completa també ofereix contrastos que no són obligatoris si no s’han seleccionat.

**Ampliacions possibles.** Cal escollir una pregunta que afegeixi treball al nucli seleccionat:

- És estable la zonificació amb un entorn més ampli? Comparar dos marges declarats, mantenir les mateixes regles de preparació i mesurar on i quanta superfície canvia de categoria dins del terme.
- Com varia el contrast en reservar blocs espacials diferents? Fixar les particions abans de construir, mantenir juntes les ubicacions coincidents i informar de coincidències per codi i desacords cartografiats. Un codi poc representat exigeix una conclusió acotada.
- Com canvia un resum de portals amb la malla? Comparar quadrícules o hexàgons amb dues mides o orígens, conservar el total i explicar l’efecte del suport espacial. Una densitat per àrea no és una taxa per població.

**Documentació i lliurament.** Els generadors, correspondències, tessel·lacions i zones estimades queden al GeoPackage de PR4. Cal actualitzar els dos projectes, conservar la composició i el PDF i integrar els controls als apunts. El mapa identifica zones poc sustentades i el caràcter aproximat de les fronteres; es reobre el conjunt complet.

**Qualificació.** PR4 manté **70% treball bàsic, 20% ampliacions i 10% documentació**, fins a **7, 2 i 1 punts**. Si el taller es selecciona com a bàsic, les seves operacions es valoren al 70%; si s’ofereix com a ampliació, contribueix al 20%. No es compta dues vegades la mateixa aportació. Es valoren pregunta, controls i interpretació, amb documentació clara; cap percentatge de coincidència garanteix una nota.

# Entrades i diagnòstic de referència

La distribució CartoCiudad Tarragona 04/2026 conté `portalpk_publi` en EPSG:4258, amb els camps `id_porpk`, `tipo`, `cod_postal`, `ine_mun` i `municipio`. La consulta atributiva de portals atribuïts a Reus retorna **17.483 registres**, 17.483 IDs diferents i `ine_mun=43123`.

| Codi postal | Registres de la selecció atributiva |
| --- | ---: |
| 43110 | 1 |
| 43201 | 2.498 |
| 43202 | 1.319 |
| 43203 | 1.494 |
| 43204 | 4.169 |
| 43205 | 4.618 |
| 43206 | 3.377 |
| 43330 | 1 |
| 43470 | 1 |
| 43480 | 5 |

Table: Freqüències observades a l’entrada de referència, abans de la preparació geomètrica.

El subconjunt no presenta codis buits/nuls ni geometries SQL nul·les. S’hi han trobat 54 grups de BLOB geomètric exactament coincident, amb 388 registres i sense conflictes de codi dins d’aquells grups. Hi ha 17.149 BLOB diferents; aquest nombre no s’ha de presentar encara com el nombre definitiu de generadors després de reprojecció i control de geometries.

Els codis minoritaris no s’esborren per freqüència ni perquè no comencin per 432. Cal inspeccionar-ne la posició i la procedència. Una atribució municipal i una selecció espacial poden discrepar legítimament o revelar un problema de dades; la discrepància és un resultat per diagnosticar.

# Seqüència de demostració

## De registres a generadors

La font original es conserva. Una preparació separada filtra portals, comprova coordenades i reprojecta a EPSG:25831. La regla de coincidències ha de distingir múltiples adreces d’una mateixa ubicació, duplicats i possibles codis incompatibles.

Quan diverses files coincideixen en posició i codi, es pot construir un generador amb `id_generador` propi i una relació als `id_porpk` originals. Cal conservar nombre de registres i criteri d’agregació. No s’ha de convertir el desplaçament artificial de punts en una solució automàtica a les degeneracions.

La inspecció es repeteix sobre els generadors externs incorporats. L’absència de conflictes en el subconjunt atributiu de Reus no prova que tot l’entorn provincial tingui la mateixa propietat.

## Delaunay i Voronoi sobre el mateix conjunt

La demostració construeix les dues estructures i les superposa amb els punts. Delaunay permet discutir veïnatge, arestes llargues, triangles de vora i casos degenerats. Voronoi mostra dominis de proximitat i la necessitat d’una extensió finita de construcció.

Cal comprovar que l’extensió del Voronoi inclou tot el municipi abans de retallar-lo. Els generadors externs continuen participant en les distàncies. Es compara una preparació amb marge amb una d’entorn més ampli i es localitzen els canvis de frontera.

El codi postal es propaga com a categoria del generador. No s’interpola una mitjana de codis dins dels triangles ni s’utilitzen centroides de tots els portals d’un codi com si fossin una representació equivalent del conjunt original.

## Dissolució i lectura cartogràfica

Es manté el Voronoi retallat amb la correspondència generador/codi i es crea una segona capa dissolta. Això permet tornar a les cel·les quan una frontera o un enclavament requereixi explicació. L’agregació geomètrica no acredita una frontera postal oficial.

El mapa compara etiquetes observades, dominis inferits i densitat de suport. Un generador aïllat pot dominar una superfície gran: cal explicar el mecanisme i no presentar aquella extensió com una observació territorial directa. Una capa independent de delimitacions postals, si se’n disposa amb llicència i metadades, constitueix un contrast diferent dels mateixos portals utilitzats per generar el model.

# Controls i validació

| Control | Condició d’acceptació |
| --- | --- |
| Identitats | Relació traçable entre registres, generadors i cel·les |
| Geometria | Entrades adequades; cel·les vàlides i domini cobert sense solapaments d’àrea |
| Categories | Codis textuals, amb tractament explícit de desconeguts i conflictes |
| Dissolució | Mateixa cobertura i traça de les categories |
| Vora | Generadors externs i comparació entre extensions documentats |
| Contrast | Portals de control reservats abans de la construcció o referència independent |

Table: Controls per separar construcció correcta i validesa de la interpretació.

La classificació dels punts generadors pel seu propi Voronoi és gairebé trivial i no és una estimació honesta de rendiment predictiu. Per al contrast es reserven ubicacions completes o blocs espacials: repartir registres coincidents entre grups faria que la mateixa posició aparegués a entrenament i validació.

Cal informar de recompte i proporció de coincidències per codi, classes poc representades, punts no avaluables i distribució espacial dels desacords. Un repartiment aleatori d’adreces molt pròximes pot ser massa optimista; la validació per blocs introdueix una exigència territorial més clara. Cada resultat quantitatiu s’associa a la partició i a la preparació realment executades.

## Resultats del cas calculat

El cas de referència amplia el rectangle municipal 1.500 m i el contrasta amb una ampliació de 3.000 m. Són marges del **rectangle**, no una selecció de tots els punts a aquella distància euclidiana del terme. L’entorn ampli conté 47.862 portals, que es conserven amb la correspondència a ubicacions agrupades.

La partició utilitza blocs de 500 m en EPSG:25831: es reserva un de cada cinc segons una regla espacial determinista, abans de construir les tessel·lacions. Tots els registres coincidents comparteixen grup. El model principal utilitza 23.968 generadors d’entrenament i el contrast ampli, 37.156.

| Resultat comprovat | Valor |
| --- | ---: |
| Triangles de Delaunay | 47.918 |
| Cel·les de Voronoi retallades | 13.198 |
| Categories postals dissoltes | 14 |
| Ubicacions de validació dins de Reus | 4.092 |
| Coincidències amb el codi observat | 3.435 |
| Proporció de coincidències | 83,94% |

Table: Resultats de la partició espacial i de les fonts fixades del cas resolt.

En aquesta execució, les dues extensions donen les mateixes categories dins del terme, dins de la tolerància geomètrica declarada. Això és evidència per a aquests marges i generadors; no demostra que qualsevol conjunt exterior sigui irrellevant. El 83,94% avalua ubicacions reservades amb codi conegut, no l’exactitud de les fronteres en espais sense portals.

# Paquets, transferència i ampliacions

L’alumnat descarrega les fonts CNIG o reutilitza els originals verificats de PR3 i prepara el seu entorn de generadors amb les instruccions del PDF. El paquet docent conserva originals, generadors preparats, estructures, zonificació, incidències, controls i composició. El cas resolt compartit és un exemple; la partició de validació i el resultat s’identifiquen explícitament.

La transferència manté les preguntes sobre duplicats, entorn i suport, però no imposa els recomptes de Reus a altres municipis. Una ampliació sobre quadrícules o hexàgons pot recuperar el problema de la unitat espacial modificable: variar mida i origen mentre es manté el mateix conjunt de punts.

# Fitxers i evidències

En el treball propi, les capes i la taula de correspondència s’incorporen a la instantània PR4, amb projecte incrustat i extern coherents. El cas resolt de Reus és una demostració separada. El diari ha de permetre reconstruir la preparació i explicar almenys una frontera inferida problemàtica.

L’avaluació aplica els blocs 70/20/10 de PR4 segons l’encaix anunciat a Moodle. Cal conservar la selecció d’apartats amb què s’ha treballat i separar la correcció de la construcció, el contrast independent i la qualitat de la comunicació.

# Referències

- [Tessel·lacions i geoprocessament, manual TIG](https://geourv.github.io/tig/ca/chapters/analisi-geoprocessament-vectorial/).
- [CartoCiudad Tarragona, CNIG](https://centrodedescargas.cnig.es/CentroDescargas/detalleArchivo?sec=9092).
- [Geometria vectorial, QGIS 3.44](https://docs.qgis.org/3.44/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html).
