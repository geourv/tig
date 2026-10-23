---
title: "PR4 · Envolupants, distàncies i geoprocessament"
lang: ca
recipient: alumnat
content_status: draft
subject: "Tecnologies de la Informació Geogràfica"
subject_code: "21234114"
author: "Benito Zaragozí"
institution: "Universitat Rovira i Virgili"
---

# Finalitat i resultats d’aprenentatge

Què canvia quan una consulta deixa de seleccionar entitats senceres i comença a construir geometries noves? La pràctica compara primer les envolupants d’un municipi, introdueix distàncies i buffers i en deriva una regió d’interès rectangular. Aquesta ROI permet preparar punts, línies i polígons, comparar superposicions i derivar peces i punts, amb continuïtat cap al treball ràster.

En acabar, cal poder predir l’efecte dels paràmetres d’un buffer, diferenciar les geometries i els atributs d’una superposició, identificar cobertura d’un o més generadors i justificar l’envolupant escollida. Cada operació ha de deixar una sortida persistent i una comprovació interpretable.

El professor selecciona a classe les comparacions obligatòries del **70% bàsic** i les recull a Moodle, preservant la ROI de continuïtat. La lectura no exigeix totes les combinacions possibles. Si s’hi incorpora el taller de Reus, Moodle indica si és treball bàsic o una opció d’ampliació.

# Punt de partida i dades

Amb QGIS tancat, es copia la instantània validada de PR3 a `sandbox/pr4-geoprocessament-cognom.gpkg`. Es comproven les capes municipals, els portals, les illes, els candidats viaris i la digitalització heretada. El principal serà `pr4`; el `.qgz` extern es crea de nou amb fonts relatives al contenidor homònim.

Les operacions de distància es fan en **EPSG:25831**, amb geometries locals vàlides i no buides. Cal identificar l’edició CNIG i la preparació de `municipi_treball`, conservar el límit durant les comparacions i mantenir la traça fins als originals descarregats. Un canvi d’edició o de geometria pot alterar el resultat sense que l’algorisme hagi canviat.

Els buffers de fanals parteixen d’un inventari amb IDs únics o d’un escenari sintètic explícit. En aquest segon cas, la capa es denomina `fanals_sintetics` i els resultats només expliquen geometria. Cap radi d’aquesta pràctica és una mesura de la il·luminació real.

# Procediment

## Comparar envolupants del municipi

L’Explorador ha de mostrar les connexions al GeoPackage de PR4, al de CartoCiudad i al del viari CNIG. S’hi identifiquen `portalpk_publi`, `manzana` i `rt_tramo_vial`. Es carrega el WMS IGN/PNOA sota els vectors, representats amb contorns sense farciment. El projecte treballa en EPSG:25831; la coincidència visual no substitueix la comprovació del CRS de cada font.

Una envolupant conté l’entrada i en resumeix l’extensió. **Geometria delimitadora mínima** s’aplica a `municipi_treball`, encara **sense buffer**. Es deixa buit el camp d’agrupació perquè hi ha una sola entitat municipal i es repeteix el càlcul amb els quatre tipus, desant cada sortida amb un nom propi.

L’identificador de Processament és `qgis:minimumboundinggeometry`.

![Selector del tipus d’envolupant a QGIS](assets/img/qgis/qgis-c06-envolupants-tipus.png "La mateixa eina permet escollir caixa, rectangle orientat, cercle mínim i embolcall convex. L’entrada es manté constant durant la comparació.")

| Tipus | Valor | Propietat |
| --- | ---: | --- |
| Envolupant rectangular | 0 | Costats alineats amb els eixos del CRS |
| Rectangle mínim orientat | 1 | Orientació lliure per minimitzar l’àrea rectangular |
| Cercle mínim contenidor | 2 | Centre i radi contenidors, amb aproximació poligonal |
| Embolcall convex | 3 | Conjunt convex mínim; omple concavitats i forats |

Table: Opcions de la geometria delimitadora mínima de QGIS 3.44.

![Quatre envolupants del terme de Vila-seca](assets/img/qgis/qgis-c06-envolupants-comparacio.png "Terme magenta, caixa verda, rectangle orientat blau, cercle taronja i convexa violeta. Totes resumeixen la mateixa entrada i incorporen espai que el municipi no ocupa.")

Es comproven contenció, validesa, àrea i extensió. El cercle mínim no és necessàriament un buffer del centroide. Si hi hagués diverses entitats, el camp opcional produiria una envolupant per classe; sense camp es treballaria sobre el conjunt. `native:boundingboxes` permet, en canvi, obtenir caixes per entitat.

## Interpretar la distància i construir el buffer

La distància mínima entre geometries es mesura entre les posicions més pròximes, no entre centroides. El model pla utilitzat aquí requereix coordenades mètriques en EPSG:25831. Una distància euclidiana no incorpora carrers, barreres ni temps; una zona de proximitat no és una àrea d’accessibilitat.

Un buffer arrodonit aproxima totes les posicions dins d’una distància de l’entrada. Els segments de QGIS corresponen a un quart de circumferència; augmentar-los suavitza l’aproximació, sense millorar l’exactitud de la font. Els buffers individuals conserven generadors; dissoldre’ls elimina fronteres i solapaments interns per obtenir cobertura conjunta.

Es calcula `municipi_buffer_500m` amb `native:buffer`: 500 m, 8 segments per quadrant, unions arrodonides, límit de mitra 2 i dissolució desactivada. Es desa al GeoPackage, es reobre i es comprova que conté el terme i que la geometria és vàlida. No és una franja legal.

![Buffer municipal de cinc-cents metres](assets/img/qgis/qgis-c06-buffer-municipal.png "Distància i segmentació són decisions diferents. El diàleg fixa els paràmetres; el control posterior es fa sobre la sortida persistent.")

## Desar la caixa ROI del buffer

**Sobre aquest buffer** s’executa `native:boundingboxes` i la caixa no orientada es desa com `roi` al GeoPackage. Cal tornar a carregar-la i comprovar-ne CRS, validesa, extrems i contenció del buffer. S’hi afegeix `id_roi` per identificar la màscara a les superposicions. Les cantonades de la caixa poden quedar a més de 500 m del terme.

![Caixa envolupant amb el buffer com a entrada](assets/img/qgis/qgis-c06-caixa-roi.png "Caixetins delimitadors calcula els extrems X/Y del buffer. La destinació ha d’identificar tant el fitxer GeoPackage com el nom intern roi.")

Les eines habituals es localitzen a `Vectorial > Geoprocessing Tools`; la caixa d’eines de Processament permet cercar la resta. Les captures mostren QGIS 3.44.11, amb algunes etiquetes encara en anglès. Els diàlegs fixen paràmetres; el resultat es comprova després d’executar i reobrir la sortida persistent.

![ROI desada, connexions GeoPackage i WMS](assets/img/qgis/qgis-c06-roi-desada.png "Municipi magenta, buffer blau i ROI verda són geometries diferents. La caixa incorpora entorn exterior i permet continuar amb una graella no rotada.")

## Preparar les entrades de tota la ROI

La caixa incorpora municipis veïns. Cal reprendre els originals provincials i no limitar l’entrada a les seleccions municipals de PR3. Es conserva una clau de fila d’origen, com `id_font`, i es prepara una extracció ampla de candidats, encara amb les geometries senceres, que es reprojecta a EPSG:25831. Una selecció per ubicació amb `intersecta` i `roi` permet identificar les entitats pertinents sense retallar-les.

![Selecció espacial amb la ROI com a referència](assets/img/qgis/qgis-c06-seleccio-roi.png "La selecció conserva la geometria sencera de cada candidat que interseca roi. Només una operació posterior de retall o intersecció la fragmenta.")

> **Rendiment i abast.** No cal representar una capa pesada ni obrir-ne la taula per processar-la. Desmarcar-la al panell Capes estalvia dibuix i manté les dades disponibles. Un filtre de capa, en canvi, pot restringir també l’entrada de l’algorisme; cal registrar-lo i distingir-lo del filtre de taula i de la selecció. La millora de temps depèn de la font i dels índexs.

En `portalpk_publi`, el criteri que diferencia portals de punts quilomètrics és:

```sql
"tipo" = 'Portal'
```

Per preparar específicament els carrers urbans es comprova el domini de `clased` i s’utilitza `Urbano`. Aquest filtre no s’aplica al retall general del viari, que conserva totes les classes. `id_tramo` pot repetir-se en registres diferents i no substitueix la clau de fila d’origen.

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

Sobre les capes que travessen la ROI es comparen tres resultats: selecció per ubicació, **Retall** (`native:clip`) i **Intersecció** (`native:intersection`). La selecció conserva les entitats completes. El retall conserva la part interior i els atributs de l’entrada. La intersecció conserva la part comuna i hi associa atributs de les dues entrades.

Es fan tres demostracions: retall dels portals filtrats, retall de les línies viàries i intersecció de les illes. Les sortides es desen com `portals_roi`, `viari_roi` i `illes_roi`. En la intersecció s’incorpora `id_roi` com a atribut de la màscara. Els punts es conserven o s’exclouen; les línies i els polígons poden quedar fragmentats.

![Retall dels portals filtrats per la ROI](assets/img/qgis/qgis-c06-retall-portals.png "El subconjunt Portal és l’entrada puntual i roi és la màscara. La font preparada pot quedar oculta al mapa mentre es processa.")

![Retall de les línies viàries per la ROI](assets/img/qgis/qgis-c06-retall-viari.png "El mateix algorisme aplicat a línies crea geometries parcials. La longitud s’ha de recalcular sobre la sortida.")

Cal mantenir un identificador d’origen propi, perquè l’eina pot regenerar els FID. Després de modificar geometries es recalculen longituds o àrees: un camp de mesura copiat de l’entrada pot haver quedat desactualitzat. Es comprova que les parts retallades quedin dins de la màscara i que la mesura no augmenti respecte de l’entitat original corresponent.

La mateixa distinció es pot examinar amb illes o parcel·les que travessin una frontera. Si una entitat es divideix, no s’ha de sumar sense més un recompte original repetit a cada fragment. La taula de sortida també forma part del resultat del geoprocessament.

Una comparació posterior amb **Diferència** mostra la part exterior. Cal mantenir explícit l’ordre: entrada menys màscara i màscara menys entrada responen preguntes diferents.

## Diferència per preparar context marí

Es retallen per la ROI tots els recintes administratius que hi intervenen i se’n dissol la cobertura com `terra_roi`. Aquest nom identifica una preparació operativa, no una classificació exhaustiva de terra i aigua. **Diferència** amb entrada `roi` i superposició `terra_roi` produeix `mar_complement`. Restar només el municipi de treball deixaria també els termes veïns al complement.

Cal inspeccionar totes les parts amb el WMS, sobretot en ports i desajustos de límits. A Vila-seca, la diferència té cinc components; el cas conserva el complement complet i selecciona com `mar_context` els dos components connectats amb punts marins de contrast prop de les cantonades sud-oest i sud-est. No es trasllada aquesta regla a un altre territori sense revisar-la. El resultat serveix de context derivat, no de delimitació marina oficial.

## Peces entre carrers i multipart a monopart

De `viari_roi` s’extreu la classe `Urbano` i es desa `urbans_roi`. Es calculen dos buffers dissolts, amb radis de 5 i 10 m, 8 segments per quadrant i extrems i unions arrodonits. El radi es mesura a cada costat de l’eix: 5 m aproxima una amplada total de 10 m en un tram recte. No és l’amplada real observada de cada carrer.

Es resta cada cobertura viària de `terra_roi` i es conserven les dues diferències. El resultat pot reunir moltes peces separades en una única entitat multipart.

![Diferència entre l’àmbit de treball i els buffers viaris](assets/img/qgis/qgis-c06-diferencia-illes.png "Es conserva la part de l’àmbit situada fora de les franges dels carrers. El resultat pot incloure espais rurals, peces perifèriques o interiors de rotondes.")

`native:multiparttosingleparts` crea una fila per part. El recordatori WKT és útil: `MULTIPOLYGON` pot representar diversos polígons en una fila; després de separar-los es conserva `id_origen`, s’assigna `id_peca` i es recalcula `area_m2`. La suma d’àrees ha de coincidir amb la diferència original dins de la tolerància numèrica.

![Conversió de peces multipart a parts senzilles](assets/img/qgis/qgis-c06-multipart-monopart.png "Separar les parts no redibuixa les peces ni les converteix en illes urbanes oficials. Els atributs d’origen es repeteixen a les files noves.")

La comparació es fa sobre el WMS i amb les illes `manzana` de CartoCiudad. Cal explicar què canvia amb el radi i quines peces depenen de discontinuïtats viàries o del límit de treball. No s’eliminen fragments només per fer que el recompte sembli més plausible.

## Derivar punts de polígons i línies

Es comparen `native:centroids` i `native:pointonsurface` sobre les mateixes illes, amb un punt per entitat. El centroide poligonal pot quedar fora; el punt sobre la superfície respon al requisit de pertinença. Aplicat a línies, el centroide pondera els segments per longitud i pot quedar fora del traçat: no és necessàriament el punt de mitja longitud.

`native:extractvertices` extreu els vèrtexs de línies i polígons amb els índexs de part, anell i posició que corresponguin. Es conserven els identificadors d’origen. Els vèrtexs no són una mostra regular i poden repetir coordenades, especialment al tancament d’anells. Per extreure el primer i l’últim vèrtex d’una entitat lineal, `native:extractspecificvertices` utilitza `0,-1`; si es volen els extrems de cada part, primer se separen les geometries multipart.

![Comparació de punts derivats sobre les illes de CartoCiudad](assets/img/qgis/qgis-c06-punts-resultat.png "Els triangles vermells són centroides i els punts verds pertanyen a la superfície; els vèrtexs descriuen el contorn. Cap d’aquests mètodes identifica per si sol accessos ni nodes funcionals.")

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

## Comparar el cost espacial de les envolupants del buffer

Es reprèn `municipi_buffer_500m`, conservat al començament de la pràctica, amb els paràmetres registrats. El buffer inclou el municipi i el marge exterior; no representa una franja legal.

Es repeteixen les quatre formes sobre el buffer i es mesura quanta superfície afegeixen. Aquestes sortides es distingeixen de les envolupants inicials calculades sobre el municipi. En comparar àrees es comproven la contenció i l’aproximació del cercle; la mida del dibuix al llenç no permet decidir quina geometria és més compacta.

La **regió d’interès (`roi`)** de continuïtat serà el rectangle alineat als eixos d’EPSG:25831 que conté `municipi_buffer_500m`. Es desen geometria i extrems. El rectangle orientat, la convexa i el cercle es conserven com a alternatives de comparació, sense substituir la ROI acordada. A PR5, ajustar-la a l’origen i a la mida de la graella pot ampliar-ne l’extensió.

# Comprovacions i interpretació

| Resultat | Control principal |
| --- | --- |
| Buffers | Entrada i paràmetres registrats; geometries vàlides; comparació amb els generadors |
| Dissolució | Cobertura única; àrea no superior a la suma d’àrees individuals |
| Retall/intersecció | Parts dins de l’àmbit; IDs d’origen i mesures recalculades |
| Diferència i parts | Cobertura i complement compatibles amb l’univers; suma d’àrees conservada en separar parts |
| Punts derivats | Traça fins a l’entitat, diferència entre centroide i punt interior, índexs i coordenades repetides identificats |
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
- [Geometria delimitadora mínima, QGIS 3.44](https://docs.qgis.org/3.44/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html#minimum-bounding-geometry).
