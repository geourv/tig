---
title: "PR4 · Buffers, superposicions i regió d’interès"
lang: ca
recipient: alumnat
content_status: approved
subject: "Tecnologies de la Informació Geogràfica"
subject_code: "21234114"
author: "Benito Zaragozí"
institution: "Universitat Rovira i Virgili"
---

# Finalitat i resultats d’aprenentatge

Què canvia quan una consulta deixa de seleccionar entitats senceres i comença a construir geometries noves? La pràctica compara àrees d’influència, retalls, interseccions i unions, i acaba delimitant una regió d’interès rectangular que es podrà reutilitzar en el treball ràster.

En acabar, cal poder predir l’efecte dels paràmetres d’un buffer, diferenciar les geometries i els atributs d’una superposició, identificar cobertura d’un o més generadors i justificar l’envolupant escollida. Cada operació ha de deixar una sortida persistent i una comprovació interpretable.

El professor selecciona a classe les comparacions obligatòries del **70% bàsic** i les recull a Moodle, preservant la ROI de continuïtat. La lectura no exigeix totes les combinacions possibles. Si s’hi incorpora el taller de Reus, Moodle indica si és treball bàsic o una opció d’ampliació.

# Punt de partida i dades

Amb QGIS tancat, es copia la instantània validada de PR3 a `sandbox/pr4-geoprocessament-cognom.gpkg`. Es comproven les capes municipals, els portals, les illes, els candidats viaris i la digitalització heretada. El principal serà `pr4`; el `.qgz` extern es crea de nou amb fonts relatives al contenidor homònim.

Les operacions de distància es fan en **EPSG:25831**, amb geometries locals vàlides i no buides. Cal identificar l’edició CNIG i la preparació de `municipi_treball`, conservar el límit durant les comparacions i mantenir la traça fins als originals descarregats. Un canvi d’edició o de geometria pot alterar el resultat sense que l’algorisme hagi canviat.

Els buffers de fanals parteixen d’un inventari amb IDs únics o d’un escenari sintètic explícit. En aquest segon cas, la capa es denomina `fanals_sintetics` i els resultats només expliquen geometria. Cap radi d’aquesta pràctica és una mesura de la il·luminació real.

# Procediment

## Comparar buffers de punts, línies i polígons

Es localitza **Buffer**, `native:buffer`, a Processament. Abans de cada execució es comproven entrada, CRS, selecció, distància, segments, estil dels extrems, estil de les unions, dissolució i destinació. Es varia una decisió cada vegada i es conserven noms que identifiquin l’escenari.

| Comparació | Valors de prova | Què cal observar |
| --- | --- | --- |
| Radi sobre punts | 10, 30 i 50 m | Augment de cobertura i aparició de solapaments |
| Segments sobre la mateixa entrada | 4, 8 i 16 per quadrant | Forma dels arcs, nombre de vèrtexs i superfície |
| Extrems d’una línia oberta | Arrodonit, pla i quadrat | Diferències al començament i al final del tram |
| Cantonades de línies/polígons | Arrodonida, bisellada i en punta | Extensió de les unions i efecte del límit de mitra |
| Dissolució | Desactivada i activada | Identitat dels generadors, fronteres internes i cobertura única |
| Polígon municipal | Buffer positiu de 500 m | Expansió del terme i preparació de la ROI |

Table: Comparacions controlades de paràmetres. Les distàncies són escenaris docents.

Per a la prova lineal es pot mantenir un radi de 10 m i 8 segments per quadrant mentre es canvien els extrems. Per comparar segments en punts, es manté un mateix radi. No cal provar totes les combinacions possibles: interessa atribuir una diferència a una decisió concreta.

Els extrems afecten línies obertes; no canvien un buffer puntual ni defineixen extrems d’un polígon tancat. Les unions afecten cantonades. Amb extrems quadrats o unions en punta, algunes posicions poden quedar a més distància que el radi nominal; la interpretació de proximitat màxima correspon a la configuració arrodonida i a la seva aproximació.

Els segments indiquen una aproximació per quart de circumferència. Més segments suavitzen la representació, però no milloren la precisió de la font. En buffers poligonals amb arcs parcials no s’ha d’aplicar sense comprovació la mateixa desviació que a una circumferència regular.

Es mantenen els buffers individuals amb l’ID del generador i una còpia dissolta. La suma d’àrees individuals compta les zones comunes diverses vegades; l’àrea dissolta compta la petjada una sola vegada. La dissolució no calcula automàticament un resum vàlid dels altres atributs.

## Contrastar selecció, retall i intersecció

Sobre una capa viària que travessi el municipi es comparen tres resultats: selecció per ubicació, **Retall** (`native:clip`) i **Intersecció** (`native:intersection`). La selecció conserva els trams complets. El retall conserva la part interior i els atributs de l’entrada. La intersecció conserva la part comuna i hi associa atributs de les dues entrades.

Cal mantenir un identificador d’origen propi, perquè l’eina pot regenerar els FID. Després de modificar geometries es recalculen longituds o àrees: un camp de mesura copiat de l’entrada pot haver quedat desactualitzat. Es comprova que les parts retallades quedin dins de la màscara i que la mesura no augmenti respecte de l’entitat original corresponent.

La mateixa distinció es pot examinar amb illes o parcel·les que travessin una frontera. Si una entitat es divideix, no s’ha de sumar sense més un recompte original repetit a cada fragment. La taula de sortida també forma part del resultat del geoprocessament.

Una comparació posterior amb **Diferència** mostra la part exterior. Cal mantenir explícit l’ordre: entrada menys màscara i màscara menys entrada responen preguntes diferents.

## Unir buffers i comptar solapaments

La pregunta és quines zones queden cobertes per un, dos o més buffers de fanals. Primer es comproven IDs únics i una entitat generadora per fanal o punt sintètic. Es calcula un buffer individual amb els mateixos paràmetres per a tot el conjunt i es conserva una còpia dissolta com a control de cobertura.

**Unió** (`native:union`) sense capa de superposició divideix els solapaments interns de l’entrada, però pot generar diverses peces geomètricament coincidents, una per participant. Per tant, una fila de la unió no és automàticament una zona exclusiva, i comptar files no dona directament el nombre de fanals.

El recorregut de comprovació és:

1. Conservar la unió bruta, amb els identificadors que permeten inspeccionar-ne l’origen.
2. Separar multipart si cal i obtenir les peces geomètriques úniques, sense utilitzar com a recompte els atributs arbitraris de la fila conservada.
3. Assignar un `id_zona` a cada peça i obtenir-ne un punt sobre la superfície, comprovant que queda a l’interior de la peça.
4. Relacionar aquests punts amb els buffers individuals originals i comptar **valors diferents d’`id_fanal`**. El resum espacial es desa com a enter `n_fanals` i es vincula a la peça mitjançant `id_zona`.
5. Comprovar que les peces tenen interiors disjunts i que la seva cobertura equival a la dissolució. Si hi ha duplicats o peces incompletes, el recompte encara no és interpretable.

Una unió amb una segona capa té un altre abast: talla entre les entrades i no resol per si sola els solapaments interns de cadascuna. Aquesta diferència s’ha de contrastar amb l’ajuda de l’algorisme.

El resultat es representa per `n_fanals`, amb categories 1, 2 i 3 o més quan existeixin. La capa de peces es conserva encara que s’obtingui una segona dissolució per categoria. La zona de zero generadors només es pot calcular després de definir un àmbit finit i restar-ne la cobertura conjunta.

El recompte expressa cobertura geomètrica segons els radis escollits. No mesura il·luminància, ombres, obstacles ni qualitat del servei. Si s’utilitzen punts sintètics, tampoc no descriu la distribució dels fanals reals.

## Construir i comparar envolupants

Es calcula `municipi_buffer_500m` sobre el límit municipal escollit, amb radi 500 m, 8 segments per quadrant i unions arrodonides, registrant també la resta de paràmetres. El buffer inclou el municipi i el marge exterior; no representa una franja legal.

Sobre aquest mateix buffer es comparen quatre geometries:

| Geometria | Propietat | Espai addicional que pot incloure |
| --- | --- | --- |
| Rectangle alineat als eixos | Extrems X/Y del CRS | Cantonades exteriors a la forma |
| Rectangle mínim orientat | Rectangle de mínima àrea amb orientació lliure | Zones fora de la forma, encara que l’ajust sigui més compacte |
| Envolupant convexa | Conjunt convex mínim contenidor | Concavitats i forats |
| Cercle mínim contenidor | Centre i radi que contenen la geometria | Superfície fora de la forma municipal |

Table: Comparació d’envolupants sobre una mateixa entrada.

El cercle mínim no és una variant circular de l’envolupant convexa. Tampoc no és, en general, un buffer del centroide. En comparar àrees cal conservar l’entrada i comprovar-ne la contenció; la mida del dibuix al llenç no permet decidir quina envolupant és més compacta.

La **regió d’interès (`roi`)** de continuïtat serà el rectangle alineat als eixos d’EPSG:25831 que conté `municipi_buffer_500m`. Es desen geometria i extrems. El rectangle orientat, la convexa i el cercle es conserven com a alternatives de comparació, sense substituir la ROI acordada. A PR5, ajustar-la a l’origen i a la mida de la graella pot ampliar-ne l’extensió.

# Comprovacions i interpretació

| Resultat | Control principal |
| --- | --- |
| Buffers | Entrada i paràmetres registrats; geometries vàlides; comparació amb els generadors |
| Dissolució | Cobertura única; àrea no superior a la suma d’àrees individuals |
| Retall/intersecció | Parts dins de l’àmbit; IDs d’origen i mesures recalculades |
| Zones de solapament | Interiors disjunts, `n_fanals` enter entre 1 i el total d’IDs, cobertura equivalent a la dissolució |
| Envolupants | Entrada continguda, mètode i paràmetres identificats |
| ROI | Una geometria rectangular vàlida, alineada als eixos, en EPSG:25831 i contenidora del buffer |

Table: Controls de PR4 abans de continuar amb el model ràster.

Les toleràncies de càlcul s’han de justificar i registrar. Un resultat buit, una geometria invàlida o una discrepància no s’elimina de l’informe per fer quadrar els totals. Les conclusions han d’indicar la font, els paràmetres i els límits del model.

# Aplicació al municipi escollit

Es transfereix el procediment mantenint les preguntes i els controls. Canvien les geometries i els recomptes, no la necessitat de preservar generadors i paràmetres. Les comparacions del cas sintètic es distingeixen dels resultats sobre el municipi propi.

# Fitxers i evidències

La composició compara almenys dues decisions del geoprocessament amb enquadraments i llegendes coherents. En el cas dels buffers s’identifiquen radi, segments i dissolució; en el de la ROI es distingeixen municipi, buffer i rectangle. Es conserva al projecte i s’exporta com `pr4-geoprocessament-cognom-mapa.pdf`.

El GeoPackage es desa com `pr4-geoprocessament-cognom.gpkg`, amb principal `pr4` i un nou `.qgz` homònim. La composició i el mapa exportat es conserven amb els resultats. Les sortides determinants tenen noms descriptius, no noms temporals.

Els apunts es desen com `pr4-geoprocessament-cognom-apunts.pdf`. Comparen escenaris, taules, mesures i mapes, i expliquen quines conclusions no es poden extreure del resultat.

La còpia de `dist/` es prepara amb QGIS tancat i s’obre des d’una ubicació neta. La ROI i les capes que la justifiquen han de continuar disponibles sense dependre de PR3 ni de rutes personals.

# Ampliacions i qualificació

Es pot desenvolupar una pregunta addicional al nucli seleccionat:

- **Zona zero:** definir un univers finit i calcular la superfície fora de tots els buffers. Cal comprovar que cobertura i zona zero en formin una partició completa i interpretar el resultat com a geometria, no com a il·luminació real.
- **Atributs fragmentats:** utilitzar un total sintètic declarat sobre un polígon i comparar el valor copiat als fragments amb un repartiment proporcional a l’àrea. Es comprova el total i s’explica la hipòtesi d’homogeneïtat.
- **Cost espacial de les envolupants:** mesurar superfície exterior i extensió de les alternatives sobre la mateixa entrada, comprovar-ne contenció i justificar una elecció per al càlcul ràster. L’anàlisi ha d’afegir interpretació al simple càlcul de les formes.

La qualificació és **70% treball bàsic, 20% ampliacions i 10% documentació**, fins a **7, 2 i 1 punts**. Es valoren operacions seleccionades correctes i comprovades, ampliacions amb pregunta i contrast, i apunts, mapes, captures i organització. El nombre de sortides no garanteix nota. Reus es valora segons l’encaix anunciat i cap aportació es compta dues vegades; les ampliacions no substitueixen els obligatoris.

# Referències

- [Anàlisi i geoprocessament vectorial, manual TIG](https://geourv.github.io/tig/ca/chapters/analisi-geoprocessament-vectorial/).
- [Superposicions vectorials i Unió, QGIS 3.44](https://docs.qgis.org/3.44/en/docs/user_manual/processing_algs/qgis/vectoroverlay.html#union).
- [Geometria vectorial, QGIS 3.44](https://docs.qgis.org/3.44/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html).
