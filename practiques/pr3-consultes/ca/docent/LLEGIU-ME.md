---
title: "PR3 · Guia docent de consultes, expressions i fonts cadastrals"
lang: ca
recipient: docent
content_status: approved
subject: "Tecnologies de la Informació Geogràfica"
subject_code: "21234114"
author: "Benito Zaragozí"
institution: "Universitat Rovira i Virgili"
---

# Finalitat i resultats d’aprenentatge

La pràctica ha de fer recognoscible l’estat de les dades en cada pas. Filtrar una capa, mostrar unes files, seleccionar entitats i exportar-les poden semblar equivalents en una captura, però tenen efectes diferents sobre el mapa, les eines i els fitxers conservats.

El recorregut progressiu del capítol 5 ja proporciona el cas principal: selecció manual de Vila-seca, filtre provincial, modes de taula, selecció per expressió, selecció espacial i calculadora. La pràctica en concentra les decisions i hi connecta un mapa municipal més elaborat i la descoberta ATOM del Cadastre.

# Preparació i conducció de la sessió

| Component | Durada orientativa |
| --- | --- |
| Aula, consultes i descoberta de fonts | 150–180 min |
| Treball autònom i apunts | 120–180 min |
| Preparació docent | 45–60 min |

Table: Estimació de PR3 amb PR2 validada i cobertura provincial identificada.

Són temps orientatius pendents de contrast amb una classe. Les descàrregues formen part de l’activitat; les esperes del CNIG o del Cadastre poden requerir treball previ. Les consultes i la descoberta ATOM es poden repartir en dues sessions.

Cal comprovar les fitxes, el contingut real dels ZIP i el feed cadastral abans de la demostració. A classe es registra l’estat de filtre, taula i selecció abans de cada exportació. Es fan aturades després d’obtenir el municipi, en el contrast de predicats i després de reobrir les capes. La pregunta «què passaria si ara es netegés la selecció?» ajuda a separar estat transitori i resultat persistent. Davant d’un recompte diferent, es revisen edició, IDs i criteri.

# Preparar Moodle

1. Crear una **Tasca** amb el nom **PR3 · Consultes, expressions i mapa municipal**.
2. Copiar a **Descripció** el bloc següent fins al final de «Qualificació». Enumerar els apartats obligatoris acordats a classe, incloent l’abast concret de la descoberta cadastral.
3. Adjuntar a **Fitxers addicionals** el PDF d’alumnat. Les fitxes CNIG i el feed del Cadastre s’enllacen des de la lectura; cada estudiant obté la cobertura del seu municipi.
4. Fixar dates, forma de tramesa, límit de mida i màxim de 10 amb blocs 7/2/1. Si un servei falla, indicar com es documenta la incidència i quan es reprèn la descàrrega.
5. Comprovar la **vista d’estudiant**, els enllaços i els fitxers. Un cas resolt compartit es presenta com a exemple; el paquet docent complet serveix per preparar la sessió.

## Enunciat per copiar a la descripció

**Dades i objectiu.** Cal conservar la PR2 pròpia, obtenir CartoCiudad i transport del CNIG i preparar consultes sobre el municipi escollit. Els límits conserven la traça de PR1; la descoberta ATOM del Cadastre identifica una font diferenciada amb els seus codis i metadades.

**Treball bàsic —70%.** El professor selecciona a classe els apartats obligatoris i els recull en aquesta Tasca: estats de consulta, expressions, selecció espacial, exportació, mesures, mapa i descoberta cadastral. Cal conservar els resultats locals i les tres capes de PR2, distingir files d’IDs de tram i documentar predicats i unitats. La guia ofereix més comparacions que les necessàriament avaluades.

**Ampliacions —20%.** Es pot resoldre una d’aquestes preguntes més enllà del mínim seleccionat:

- Quins objectes expliquen la diferència entre dos predicats de frontera? Comparar conjunts d’IDs, preparar una taula de casos exclusius i inspeccionar-ne una mostra al mapa amb la mateixa font i límit.
- Com canvia una suma viària en comptar registres o trams únics? Auditar els `id_tramo` repetits i les seves geometries, justificar la unitat de resum i contrastar els totals. No eliminar files només perquè comparteixen etiqueta.
- Quina consulta es pot reutilitzar sobre un segon municipi? Conservar expressió, paràmetres i recomptes, provar casos amb resultat i sense resultat i explicar com es detecta un codi o camp inadequat.

**Documentació i lliurament —10%.** La base és `pr3-consultes-cognom`: GeoPackage amb principal `pr3`, `.qgz`, mapa i apunts PDF. Els apunts documenten descàrregues, estats de consulta, expressions, recomptes, unitats, traça cadastral i interpretació. Les captures mostren configuració i resultat persistent; cal reobrir el conjunt en una altra carpeta.

**Qualificació.** Fins a **7 punts** pels obligatoris seleccionats i comprovats; **2 punts** per una ampliació amb pregunta, controls i interpretació; **1 punt** per claredat dels apunts, captures, mapa i organització. Els 7 punts són el màxim del bloc bàsic. Ni una consulta vàlida ni un mapa elaborat garanteixen una nota; les ampliacions no substitueixen els obligatoris i la documentació aporta puntuació pròpia.

# Punt de partida i dades

Cal partir d’una PR2 validada i copiar-ne el GeoPackage complet a `pr3-consultes-cognom.gpkg`. El nou principal `pr3` i el `.qgz` homònim han d’apuntar al contenidor nou. `fanals`, `carrils_bici` i `plaques_solars` continuen físicament presents, encara que no siguin capes actives durant la consulta CNIG.

Les edicions del cas resolt són límits CNIG de 28/07/2026, CartoCiudad Tarragona de 04/2026 i transport Tarragona de 07/2026. Els noms físics són `recintos_municipales_inspire_peninbal_etrs89`, `portalpk_publi`, `manzana` i `rt_tramo_vial`. Cal conservar originals, metadades i atribució IGN/CNIG, amb els crèdits específics de CartoCiudad.

El terme de consulta es desa com `municipi_consulta` a partir del CNIG. Es conserva `municipi_treball`, heretat de PR1, i se’n contrasten edició, codi i geometria. Els recomptes següents pertanyen a les edicions i al límit CNIG documentats; no s’exigeixen a un altre municipi ni a una descàrrega posterior.

# Procediment de demostració

## Progressió de les consultes

La preparació comença amb la cerca i descàrrega al CNIG per part de l’alumnat. Cal mostrar les fitxes provincials de CartoCiudad i transport, conservar els ZIP i les metadades i inspeccionar els GeoPackage extrets. El suport docent reté aquests originals i el cas preparat per poder repetir i diagnosticar la demostració.

1. Localització i selecció manual de Vila-seca, contrastant `NAMEUNIT` i `NATCODE`.
2. Filtre de capa pel codi provincial ES514, mostrant l’accés des del menú contextual i el proveïdor de la consulta.
3. Modes de taula: tots, seleccionats, visibles i expressió, amb selecció neta quan es vulgui demostrar només el filtre de taula.
4. Eines i modificadors de selecció, contrastats per separat al mapa, per àrea i a les capçaleres de fila.
5. Selecció per expressió amb el mateix codi municipal, exportació de `municipi_consulta` i de context administratiu.
6. Selecció espacial de portals, illes i viari; vista municipal completa, exportació nativa i reobertura.
7. Calculadora: creació/actualització, tipus, abast, camp virtual/emmagatzemat, ajuda d’una funció i agregat.

La consulta provincial es conserva literalment:

```sql
"CODNUT3" = 'ES514'
```

La seqüència manté el mateix territori i evita presentar un catàleg de funcions sense necessitat. Una captura del diàleg acredita la configuració; el resultat reobert acredita l’exportació. Si es reutilitza una figura del manual, s’identifica la seva edició i no s’atribueix a una execució nova.

## Controls quantitatius del cas de referència

| Pas o font | Resultat documentat | Lectura correcta |
| --- | --- | --- |
| Recintes originals | 8.132 | Distribució ETRS89 del cas, amb unitats singulars |
| Filtre provincial | 184 | Subconjunt `CODNUT3=ES514` |
| Punts CartoCiudad | 368.290 | 364.921 portals i 3.369 PK |
| Portals de Vila-seca | 3.584 | Coincidència de recompte entre els dos predicats provats, no equivalència universal |
| Illes originals | 28.459 | Geometria poligonal de `manzana` |
| Illes contingudes/intersectants | 285 / 318 | 33 casos de diferència a inspeccionar |
| Transport original | 233.982 files | Registres, no nombre de carreteres |
| Autovies/autopistes provincials | 3.663 files | Dues classes documentades de `clased` |
| Selecció viària municipal | 265 files, 185 `id_tramo` diferents | Geometries completes i relacions amb itineraris |

Table: Referències retingudes per diagnosticar la reproducció del cas.

Els predicats es van avaluar sobre les fonts originals abans d’exportar a EPSG:25831. Un canvi de font, límit o ordre de transformació pot afectar casos de frontera. Davant d’un recompte diferent, cal comparar les entrades i els IDs, no ajustar el criteri fins a obtenir el nombre esperat.

La suma el·lipsoidal dels 265 registres viaris del cas és 79,337036 km. Inclou geometries senceres i representacions de trams en diversos itineraris; no és una estimació de longitud d’eixos únics dins del municipi. El retall i la decisió d’unitat analítica es reprendran a PR4.

## Expressions i mesura

Cal mostrar les cometes de camps i literals, la combinació lògica, els parèntesis i el tractament de nuls. El filtre de capa OGR SQL i les expressions de QGIS no s’intercanvien sense comprovar funcions i tipus.

La calculadora crea un camp numèric, l’actualitza amb una precisió declarada i contrasta un camp virtual. El cas municipal diferencia `area($geometry)` de `$area`: amb la mateixa geometria CNIG en EPSG:25831, les referències són aproximadament 21.704.046,0248 m² plans i 21.708.436,9802 m² amb GRS80. No s’explica aquesta diferència com si fos un canvi de límit.

Un agregat permet relacionar cada municipi amb el total provincial. Cal comprovar el denominador, l’efecte dels filtres i la suma de les proporcions. Una mesura emmagatzemada s’haurà de recalcular si una operació geomètrica posterior en modifica la forma.

## Criteri cartogràfic del viari

El filtre principal del cas selecciona aquestes dues classes:

```sql
"clased" IN ('Autopista libre / autovía', 'Autopista de peaje')
```

Per construir el mapa amb vies secundàries cal inspeccionar el domini real, definir les classes admeses i conservar el criteri. Els termes primari/secundari no es traslladen automàticament entre CNIG, OSM o una classificació funcional local.

El cas resolt utilitza com a segon grup cartogràfic les classes següents, amb 388 i 150 registres municipals seleccionats, respectivament:

```sql
"clased" IN ('Carretera convencional', 'Carretera multicarril')
```

És una decisió de representació del cas: el grup no inclou automàticament camins, sendes o viari urbà. Els resultats conserven `id_font` i `id_tramo` per poder distingir cada registre original dels identificadors de tram repetits en itineraris.

La demostració combina les vies amb illes de farciment visible, portals i límit municipal. La llegenda i la jerarquia gràfica han d’explicar la selecció. Els trams seleccionats que sobresurten del municipi són una oportunitat per distingir consulta i retall, no un error que s’hagi d’ocultar amb l’enquadrament.

## ATOM del Cadastre

Es mostra el [portal INSPIRE](https://www.catastro.hacienda.gob.es/webinspire/index.html), el feed general del producte, l’oficina territorial i l’entrada municipal amb metadades i descàrrega. Cal distingir WMS, WFS i conjunt predefinit ATOM abans d’obrir el complement.

El cas documentat el 15 de setembre de 2026 identifica Vila-seca amb `43173` al feed cadastral, mentre `43171` correspon a Vilaplana en aquell feed. La codificació CNIG de Vila-seca acaba en `43171`. Aquesta comparació ensenya a seguir el contracte de cada productor, no a aplicar una conversió numèrica universal.

La demostració ha de conservar el paquet retornat, comprovar que realment sigui el producte anunciat i registrar `updated`, llicència, extensió i CRS. Una descàrrega només aparent pot ser HTML desat amb extensió ZIP. Si s’utilitza Spanish Inspire Catastral Downloader, la font continua sent el Cadastre i la traça manual ha de permetre diagnosticar un error del servei o del complement.

# Comprovacions i interpretació

La revisió compara criteri i resultat persistent: conjunt d’IDs, recomptes, geometria completa de les seleccions i fonts locals reobertes. La validesa de l’expressió al constructor no acredita que el seu significat sigui l’adequat.

Cal comprovar per separat la preservació de PR2. El paquet resolt de la guia de consultes és una referència del cas CNIG; només una comparació de l’inventari heretat pot acreditar que una nova cadena completa conserva els fanals, carrils i plaques.

L’accés cadastral s’avalua com a descoberta i preparació de dades. No es dedueixen titularitat, drets edificatoris ni conclusions jurídiques d’una capa geomètrica descarregada.

# Aplicació al municipi escollit

Cada estudiant documenta el seu municipi, les fonts, la classificació viària i els casos de frontera. Les comparacions útils són entre mètodes sobre les mateixes entrades: una selecció manual i per expressió del mateix objecte, o dos predicats espacials amb el mateix límit.

La correcció demana una explicació de per què una capa està filtrada, seleccionada o exportada. Un mapa visualment elaborat ha de continuar sent traçable a les consultes desades.

# Fitxers i evidències

El resultat inclou `pr3-consultes-cognom.gpkg`, principal `pr3`, `.qgz` homònim, apunts PDF, composició guardada i mapa exportat. Les lectures distribuïdes i els apunts de l’estudiant tenen funcions diferents.

El PDF de l’alumnat explica l’obtenció i la preparació de fonts sobre la seva PR2. El paquet docent conserva originals, base acumulativa, resultats, controls i mapa de referència. Un cas resolt compartit s’identifica com a exemple de consulta i persistència; el treball propi documenta les seves descàrregues i decisions.

# Referències

- [Consultes i dades relacionals, manual TIG](https://geourv.github.io/tig/ca/chapters/consultes-dades-relacionals/).
- [Centre de Descàrregues del CNIG](https://centrodedescargas.cnig.es/CentroDescargas/).
- [Feed ATOM de parcel·les cadastrals](https://www.catastro.hacienda.gob.es/INSPIRE/CadastralParcels/ES.SDGC.CP.atom.xml).
