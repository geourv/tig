---
title: "PR5 · Mosaic, NoData i anàlisi ràster del relleu"
lang: ca
recipient: alumnat
content_status: approved
subject: "Tecnologies de la Informació Geogràfica"
subject_code: "21234114"
author: "Benito Zaragozí"
institution: "Universitat Rovira i Virgili"
---

# Encàrrec i resultats d’aprenentatge

Com condicionen la graella i els valors absents una anàlisi del relleu? La pràctica prepara un mosaic d’elevacions, compara retalls, calcula pendent i orientació i construeix classificacions amb criteris explícits. Vila-seca i la Pineda permeten observar aquests efectes en un entorn litoral.

El nucli del treball propi és una comparació controlada a 25 i 200 m, amb deu GeoTIFF, una taula d’estadístiques i un mapa comparatiu. Els casos de cotes baixes i orientacions introdueixen les operacions; cal distingir-los dels fitxers contractuals de la comparació. La transferència manté el municipi escollit i justifica els llindars per a aquell territori.

El professor indica a classe els apartats obligatoris del **70% bàsic** i els recull a Moodle, mantenint els deu GeoTIFF de continuïtat. Les demostracions addicionals no generen nous requisits de lliurament si no s’han seleccionat. Les ampliacions permeten aprofundir en una pregunta amb controls propis.

# Punt de partida i dades

Amb QGIS tancat, es copia el GeoPackage validat de PR4 a `sandbox/pr5-raster-cognom.gpkg`. Es conserven les capes heretades, `municipi_treball` i la `roi` rectangular creada a partir del buffer municipal de 500 m. El `.qgz` anterior no es copia: es prepara el principal `pr5` i un projecte extern nou amb camins relatius.

El cas de demostració utilitza els MDT25 dels fulls 0472 i 0473 i el MDT200 de Tarragona de la primera cobertura PNOA-LiDAR. Els recursos del CNIG són 9074092, 9074093 i 9074255. Cal conservar originals, metadades, edició, llicència, CRS horitzontal, unitat vertical i política de NoData.

Les fonts del cas treballen en **EPSG:25831**, amb altures ortomètriques en metres i sentinella **−32767** per a NoData. El CRS horitzontal no identifica per si sol tota la referència vertical. Una cel·la amb cota 0 m pot ser vàlida; no s’ha de substituir l’absència per zero.

# Procediment

## Descarregar les tessel·les originals

Al Centre de Descàrregues del CNIG es consulta **Modelos Digitales de Elevaciones** i es tria el producte i la cobertura que s’utilitzaran. Les fitxes del cas són [MDT25 0472](https://centrodedescargas.cnig.es/CentroDescargas/detalleArchivo?sec=9074092), [MDT25 0473](https://centrodedescargas.cnig.es/CentroDescargas/detalleArchivo?sec=9074093) i [MDT200 Tarragona](https://centrodedescargas.cnig.es/CentroDescargas/detalleArchivo?sec=9074255).

Per al municipi propi es localitzen totes les peces que cobreixen la ROI i el marge de càlcul. Cada estudiant descarrega els GeoTIFF originals, conserva fitxes i condicions d’ús a `data/raw/` i inspecciona bandes, CRS, resolució, extensió i NoData a QGIS. Les dates de descàrrega, producte i adquisició es registren separadament.

El mosaic reutilitzable es prepara a `data/processed/`; els resultats de PR5 es desen a `sandbox/`. El mapa d’exemple docent ajuda a interpretar els efectes, però el treball propi conserva la traça de les seves tessel·les i operacions.

## Combinar les tessel·les

Cal comprovar compatibilitat de producte, edició, bandes, resolució, alineació i valors absents. **Combinar** (`gdal:merge`) crea un mosaic espacial: l’opció de posar cada entrada en una banda separada queda desactivada. S’expliciten NoData d’entrada i sortida i l’ordre de les peces si hi ha solapaments.

Un VRT pot descriure el mosaic sense copiar els píxels, però continua depenent dels fitxers originals i de les seves rutes. El GeoTIFF materialitzat és una sortida física diferent. Cal inspeccionar la costura entre fulls i comprovar que els buits d’una peça no hagin substituït valors vàlids d’una altra.

## Comparar extensió rectangular i màscara

El primer retall redueix el mosaic a una extensió rectangular derivada de la ROI. Si aquesta extensió s’alinea amb la graella, pot conservar els píxels originals. Les absències que ja tenia la font continuen sent NoData: retallar per rectangle no garanteix una cobertura completa.

El segon retall utilitza el polígon municipal o una altra màscara explícita, amb **Retalla ràster per capa de màscara** (`gdal:cliprasterbymasklayer`). La matriu resultant continua sent rectangular, però les cel·les exteriors al polígon passen a NoData. La transparència és la representació d’aquella absència, no una cota ni una classe zero.

Cal comparar transformació de graella, dimensions, valors vàlids i absents. La mida de cel·la pot ser la mateixa mentre l’origen es desplaça. Una superposició aparentment correcta al llenç no prova alineació cel·la a cel·la.

## Calcular pendent i orientació amb context

Els derivats de veïnatge es calculen sobre una cobertura amb marge i es retallen després a l’àmbit d’informe. Una finestra de 3 × 3 necessita cel·les veïnes; retallar massa aviat pot crear vores artificials. A la costa es conserven les absències de la font en lloc d’inventar elevacions.

Amb `gdal:slope` es comparen graus i percentatge sobre la mateixa entrada, fórmula i política de vores. Quan les unitats horitzontals i verticals són metres, el factor d’escala és 1. La relació entre les dues unitats és:

$$
p=100\tan\left(\theta\,\frac{\pi}{180}\right),
$$

on $\theta$ és l’angle en graus i $p$ el pendent percentual. **45° equivalen al 100%**; 2° equivalen aproximadament al 3,49%, no al 2%. Cal indicar la unitat al nom de la capa i als llindars.

Amb `gdal:aspect` es comproven convenció angular, fórmula i tractament de superfícies planes. En la convenció utilitzada, l’azimut creix en sentit horari des del nord. L’orientació és circular: 359° i 1° són pròxims.

| Classe | Regla docent |
| --- | --- |
| Pla | Pendent vàlid inferior a 2° |
| Nord | Pendent almenys 2° i orientació en [315°, 360°) o [0°, 45°) |
| Est | Pendent almenys 2° i orientació en [45°, 135°) |
| Sud | Pendent almenys 2° i orientació en [135°, 225°) |
| Oest | Pendent almenys 2° i orientació en [225°, 315°) |

Table: Reclassificació d’orientacions, amb intervals sense solapament.

El llindar de 2° és una decisió del cas. La classe plana es deriva del pendent i no d’un codi d’orientació suposat. Si l’algorisme retorna NoData per a una cel·la plana, cal que el procediment de classificació la distingeixi d’una cel·la sense elevació o sense veïnatge suficient.

## Explorar les cotes baixes de la Pineda

La **calculadora ràster** de Processament, `native:rastercalc`, avalua valors de cel·la. Amb la banda d’elevació identificada com `elevacio@1`, el predicat elemental és:

```text
"elevacio@1" < 2
```

Sobre el domini vàlid produeix cert/fals, habitualment 1/0. Cal conservar NoData fora d’aquest domini. Per construir dues classes etiquetades, inferior a 2 m i complementària, es pot utilitzar:

```text
1 * ("elevacio@1" < 2) + 2 * ("elevacio@1" >= 2)
```

Després, `gdal:polygonize` transforma les regions en polígons amb un camp `classe`. Cal fixar si s’uneixen cel·les per quatre o vuit veïns. Ara sí que el filtre de taula o la calculadora de camps actuen sobre files vectorials, per exemple per seleccionar la classe 1 o calcular-ne l’àrea.

El resultat identifica **cotes baixes del model d’elevacions**, útils per formular preguntes sobre la Pineda. La inundabilitat necessita també nivell o cabal, connectivitat hidràulica, drenatge, infraestructures i condicions de contorn. El contrast amb cartografia oficial s’ha de fer sobre un producte i escenari identificats; no es reanomena automàticament la màscara de cota com a zona inundable.

## Comparar dues resolucions de manera controlada

Els MDT25 i MDT200 publicats del cas tenen orígens desplaçats 12,5 m. La seva comparació visual mostra dos productes, però no aïlla l’efecte de la mida de cel·la. Per al treball propi s’escull **una font comuna** prou detallada i una extensió derivada de la ROI, ajustada a una graella mare de 200 m.

Les graelles de 25 i 200 m comparteixen origen i extensió: cada cel·la grossa correspon a 8 × 8 cel·les fines. Totes dues es generen directament de la font comuna amb `gdal:warpreproject`, el mateix principi de remostreig i NoData explícit. No es presenta una ampliació artificial d’una font grossa com si fos informació fina.

Es calculen pendent en graus i orientació sobre cadascuna de les dues elevacions, amb les mateixes opcions. Es reclassifica l’elevació amb la mateixa taula d’intervals i es conserva la màscara docent de dos criteris:

| Codi de classe d’elevació | Interval del cas de referència |
| --- | --- |
| 1 | Cota inferior a 20 m |
| 2 | De 20 m inclosos a menys de 50 m |
| 3 | De 50 m inclosos a menys de 100 m |
| 4 | Cota igual o superior a 100 m |

Table: Intervals comuns per comparar les dues resolucions; NoData continua separat.

La màscara combina elevació i pendent:

```text
("elevacio@1" < 20) AND ("pendent_graus@1" < 2)
```

El llindar de 20 m pertany a aquesta comparació i és diferent del cribratge litoral de 2 m. Abans del càlcul cal comprovar alineació i domini vàlid de les dues bandes. Categories i màscares es remostregen amb un mètode que conservi les classes, no amb una interpolació bilineal de codis.

# Comprovacions i interpretació

Per a cada sortida es registren CRS, banda, tipus, dimensions, origen, extensió, mida de cel·la, NoData, rang i recompte vàlid. Es contrasten vores, costures i una mostra de posicions. Una màscara ha de distingir condició certa, falsa i no avaluada.

Les estadístiques zonals es calculen sobre `municipi_treball`, no sobre tot el rectangle amb marge. El recompte retornat per l’eina pot incloure contribucions fraccionàries en casos de vora; no s’arrodoneix per convertir-lo en un nombre aparent de píxels sencers. Els percentatges necessiten un denominador calculat amb una regla compatible.

El resum també ha de respectar el tipus de variable. La mitjana aritmètica dels angles no és una orientació mitjana circular, i la mitjana dels codis de classe no és una elevació. Per a classes es comparen freqüències; en una màscara 0/1, la mitjana sobre el domini vàlid correspon a la proporció de cel·les certes amb aquella regla de recompte.

El mapa comparatiu manté extensió, escala i llegendes comparables. La conclusió separa diferències observades, possibles mecanismes —resolució, alineació, remostreig, vora o NoData— i limitacions. No es pressuposa que totes les mitjanes o pendents hagin de canviar en la mateixa direcció.

# Fitxers i evidències

| Variable | GeoTIFF de 25 m | GeoTIFF de 200 m |
| --- | --- | --- |
| Elevació | `pr5_elevacio_25m.tif` | `pr5_elevacio_200m.tif` |
| Pendent | `pr5_pendent_25m_graus.tif` | `pr5_pendent_200m_graus.tif` |
| Orientació | `pr5_orientacio_25m_graus.tif` | `pr5_orientacio_200m_graus.tif` |
| Classes d’elevació | `pr5_elevacio_classes_25m.tif` | `pr5_elevacio_classes_200m.tif` |
| Màscara | `pr5_mascara_elevacio_pendent_25m.tif` | `pr5_mascara_elevacio_pendent_200m.tif` |

Table: Deu sortides persistents de la comparació controlada.

Els GeoTIFF es conserven com a fitxers germans de `pr5-raster-cognom.gpkg` i `.qgz`; la taula comparativa i les capes vectorials continuen al GeoPackage. La composició comparativa es desa als projectes i s’exporta com `pr5-raster-cognom-mapa.pdf`. Els diagnòstics i les demostracions tenen noms propis i no substitueixen aquestes sortides. Els apunts es desen com `pr5-raster-cognom-apunts.pdf`.

Es desen expressament el projecte principal `pr5` incrustat i el nou `.qgz`. Les vistes heretades només es mantenen si se n’han comprovat les fonts. Amb QGIS tancat, es copia el conjunt validat i es prova en una ubicació neta; PR6 heretarà aquests deu GeoTIFF sense reanomenar-los.

# Ampliacions i qualificació

Una ampliació afegeix una pregunta i controls al treball seleccionat. Es pot triar una d’aquestes vies:

- **Sensibilitat del llindar:** comparar pendents d’1°, 2° i 3° en la màscara, mantenint cota, graella i domini vàlid. Cal informar de proporcions amb el mateix criteri de recompte i interpretar els canvis.
- **Ordre de les operacions:** comparar agregar el pendent amb derivar-lo després d’agregar l’elevació, fixant font, remostreig i vores. El contrast es fa sobre cel·les avaluables comunes i explica les diferències observades.
- **Contrast territorial:** obtenir una capa oficial d’inundabilitat amb fenomen, escenari i cobertura coneguts i comparar-la amb les cotes baixes. Cal quantificar coincidències i diferències sense equiparar els dos significats.

La qualificació és **70% treball bàsic, 20% ampliacions i 10% documentació**, fins a **7, 2 i 1 punts**. Es valoren correcció i controls del nucli, pregunta i interpretació de l’ampliació, i claredat d’apunts, captures, mapes i organització. Els 7 punts són el màxim del bloc bàsic; la documentació també suma. Les ampliacions no substitueixen els obligatoris ni garanteixen més nota pel nombre de ràsters. Moodle concreta calendari i forma de lliurament.

# Referències

- [Model i anàlisi ràster, manual TIG](https://geourv.github.io/tig/ca/chapters/model-analisi-raster/).
- [Calculadores ràster de QGIS 3.44](https://docs.qgis.org/3.44/en/docs/user_manual/processing_algs/qgis/rasteranalysis.html).
- [Sistema Nacional de Cartografía de Zonas Inundables](https://www.miteco.gob.es/es/agua/temas/gestion-de-los-riesgos-de-inundacion/snczi.html).
