---
title: "PR5 · Guia docent del relleu, NoData i classificació ràster"
lang: ca
recipient: docent
content_status: approved
subject: "Tecnologies de la Informació Geogràfica"
subject_code: "21234114"
author: "Benito Zaragozí"
institution: "Universitat Rovira i Virgili"
---

# Propòsit i enunciat

La pràctica s’organitza en dos moviments: una demostració progressiva sobre Vila-seca i la Pineda, i una comparació controlada sobre el municipi propi. El primer moviment introdueix mosaic, retalls, NoData, derivats i àlgebra; el segon exigeix aplicar-los sense confondre productes oficials diferents amb un experiment de resolució.

El resultat essencial continua sent el contracte PR5 del manual: instantània del GeoPackage, deu GeoTIFF, taula comparativa, mapa i evidències. Les demostracions de cota baixa, orientació reclassificada i pendent percentual ajuden a comprendre les decisions, però no creen requisits de lliurament addicionals sense una decisió explícita d’avaluació.

# Preparació i conducció de la sessió

| Component | Durada orientativa |
| --- | --- |
| Aula, mosaic, derivats i comparació | 180–240 min |
| Treball autònom i apunts | 150–240 min |
| Preparació docent | 45–75 min |

Table: Estimació de PR5, distribuïble en dues sessions de laboratori.

Estimació pendent de contrast amb alumnat, amb PR4 validada i una ROI municipal acotada. La descàrrega i el càlcul depenen de cobertura, xarxa i equip; les ampliacions poden requerir més temps. Convé obtenir les tessel·les abans de la sessió de derivats.

La preparació comprova espai disponible, metadades, costures i cobertura amb marge. La primera sessió pot arribar al mosaic i al diagnòstic zero/NoData; la segona, als derivats i a les graelles niades. Abans de comparar mapes es fan aturades en origen/extensió, unitats de pendent i domini vàlid. La pregunta «quin denominador justifica aquest percentatge?» permet detectar comparacions de màscares incompatibles.

# Preparar Moodle

1. Crear una **Tasca** anomenada **PR5 · Relleu i comparació de resolucions**.
2. Copiar a **Descripció** el bloc següent fins al final de «Qualificació». Enumerar les demostracions seleccionades a classe i conservar el contracte dels deu GeoTIFF de la comparació.
3. Adjuntar a **Fitxers addicionals** el PDF d’alumnat, que enllaça les fitxes CNIG. Indicar el treball previ de descàrrega; el cas resolt compartit, si n’hi ha, és una referència identificada.
4. Fixar dates, tramesa i límit de mida suficient per al conjunt de GeoTIFF, projectes i PDF; màxim 10 amb blocs 7/2/1. Evitar una configuració que només admeti el `.qgz` sense dades.
5. Revisar la **vista d’estudiant**, els enllaços i els adjunts. El paquet docent conserva originals, preparacions i controls per contrastar la sessió.

## Enunciat per copiar a la descripció

**Dades i objectiu.** Cal continuar la PR4 pròpia, descarregar els MDT del CNIG que cobreixen la ROI amb marge i preparar una comparació controlada a 25 i 200 m. La font comuna, la graella, NoData i les unitats s’identifiquen abans de calcular derivats i màscares.

**Treball bàsic —70%.** El professor indica a classe i recull en aquesta Tasca els apartats obligatoris de mosaic, retalls, derivats i classificació. La comparació conserva els deu GeoTIFF contractuals, origen i extensió comuns, una taula interpretable, mapa i projectes reobribles. Les demostracions de cota baixa i orientacions no afegeixen productes obligatoris si no s’han seleccionat.

**Ampliacions —20%.** Es pot desenvolupar una pregunta addicional com aquestes:

- És estable la màscara en variar un llindar? Comparar, per exemple, pendents d’1°, 2° i 3° mantenint cota, graella i domini vàlid; informar d’àrea o proporció amb un denominador coherent i interpretar la sensibilitat.
- Donen el mateix resultat agregar el pendent i derivar-lo després d’agregar l’elevació? Mantenir font, remostreig, suport i política de vores, comparar cel·les comunes i explicar per què les operacions poden no commutar.
- Coincideixen cotes baixes i una cartografia oficial d’inundabilitat? Identificar fenomen, escenari, edició i cobertura, obtenir dades adequades per a la comparació i quantificar coincidències i diferències. Una zona baixa no és per si sola una zona inundable.

**Documentació i lliurament —10%.** La base és `pr5-raster-cognom`, amb GeoPackage, principal `pr5`, `.qgz`, mapa i apunts PDF. Els deu GeoTIFF de la lectura l’acompanyen amb els noms prescrits. Cal explicar fonts, graelles, NoData, unitats, controls i conclusions, amb captures significatives i llegendes comparables. El conjunt es prova en una carpeta nova.

**Qualificació.** Fins a **7 punts** pel treball bàsic seleccionat i validat, **2 punts** per ampliacions amb pregunta, comparació i interpretació i **1 punt** per apunts, mapes, captures i organització. Són màxims; més ràsters no impliquen més nota. Les ampliacions no substitueixen els obligatoris i la qualitat documental té puntuació pròpia.

# Entrades i referències del cas

La base és PR4, amb `municipi_treball` i la ROI rectangular del buffer de 500 m. Els MDT25 0472/0473 i el MDT200 de Tarragona són de primera cobertura PNOA-LiDAR, EPSG:25831, altures ortomètriques en metres i NoData −32767. La font comuna de l’experiment posterior ha de ser adequada per a 25 m i disposar del marge necessari.

| Referència retinguda del manual | Valor o propietat |
| --- | --- |
| Recursos CNIG | 9074092, 9074093 i 9074255 |
| Mosaic MDT25 | 2.262 × 794 cel·les de 25 m |
| Retall MDT25 de demostració | 382 × 294 cel·les; 34.734 vàlides |
| Retall MDT200 publicat | 48 × 38 cel·les de 200 m |
| Desplaçament d’origen entre productes | 12,5 m; no són graelles niades |
| Zero/NoData del MDT05 0473 | Dues cel·les de control al manual; recurs 9072569 |

Table: Referències de la demostració històrica, no resultats d’una nova execució.

Els recomptes corresponen al límit CNIG i als paràmetres documentats. Una altra edició, preparació o extensió de ROI necessita els seus controls. Cal distingir mida de cel·la, exactitud vertical, data del producte i superfície física representada.

# Seqüència de demostració

## Mosaic i retalls

La demostració comença per les fitxes CNIG de les tessel·les i les seves metadades. Cada estudiant descarrega les peces del seu àmbit, comprova la cobertura amb marge i conserva els originals. El material docent reté les descàrregues i les preparacions identificades per poder reconstruir el cas de Vila-seca.

El mosaic combina les dues tessel·les com una banda espacial, no com dues bandes d’un apilament. Es contrasten metadades, ordre de solapament, NoData i costura. El VRT permet explicar dependències; un GeoTIFF materialitzat permet explicar còpia de valors i espai d’emmagatzematge.

La comparació de retalls manté primer un rectangle alineat amb la graella i després aplica una màscara poligonal. El segon resultat continua rectangular, amb absències fora del polígon. Cal conservar les absències originals en tots dos casos i mostrar que un color transparent o una cel·la amb valor 0 no tenen el mateix significat.

El cas MDT05 del manual identifica 0 m a X=355160, Y=4550680 i NoData a X=363360, Y=4545635, en EPSG:25831. Són controls de l’edició fixada. Una prova separada que substitueixi NoData per zero pot mostrar l’error de mitjana introduït, però no es converteix en la preparació correcta de l’anàlisi.

## Derivats, unitats i superfícies planes

El pendent i l’orientació es calculen amb context exterior abans del retall d’informe. Cal fixar fórmula —Horn en la demostració—, unitats, factor d’escala i tractament de vores. Amb `COMPUTE_EDGES=False` queden visibles les posicions sense veïnatge suficient.

La comparació de graus i percentatge utilitza la mateixa entrada i cel·les vàlides. El control és:

$$
p=100\tan\left(\theta\,\frac{\pi}{180}\right).
$$

El cas històric observa 0–14,3° i 0–25,6%, amb error màxim de conversió aproximat de $1{,}91\times10^{-6}$. Són controls de la demostració, no rangs universals. La conversió no és lineal; un llindar de 2° equival aproximadament al 3,49%.

La reclassificació d’orientacions separa primer les cel·les amb pendent vàlid inferior a 2°. La resta s’agrupa en nord, est, sud i oest, amb intervals explícits i el nord partit entre 315–360° i 0–45°. La classe plana no es dedueix només del codi d’aspecte retornat per l’algorisme.

Prop d’un pla, una variació molt petita del gradient pot canviar força l’angle d’orientació. El contrast numèric de Horn ha de considerar el tipus de dada i la propagació de l’arrodoniment; la comparació angular se centra en les cel·les de la classe no plana. La classificació dels plans es comprova separadament amb el pendent.

Cal provar específicament una cel·la plana, una de pendent gairebé nul, una sense elevació i una amb veïnatge incomplet. Multiplicar un NoData per zero no el converteix necessàriament en zero: una expressió aparentment lògica pot propagar absències i perdre la classe plana. La regla s’ha de comprovar a les sortides, amb tipus i sentinelles compatibles.

## Cotes baixes i vectorització a la Pineda

La calculadora ràster aplica el llindar de cota 2 m al domini vàlid. La classificació 1/2 manté separada la resta del terreny i permet vectoritzar totes dues categories amb `gdal:polygonize`. El filtre de `classe` i la calculadora de camps actuen després sobre les regions vectorials.

| Control històric del retall MDT25 | Resultat documentat |
| --- | ---: |
| Cel·les vàlides | 34.734 |
| Cel·les amb cota inferior a 2 m | 2.150 |
| Proporció sobre el domini vàlid | 6,19% |
| Àrea de la classe baixa | 1.343.750 m² |
| Polígons de classe baixa, quatre veïns | 95 |
| Polígons de classe baixa, vuit veïns | 24 |

Table: Referències per discutir suport de cel·la i connectivitat.

L’àrea es reconstrueix amb 2.150 × 625 m². La connectivitat canvia l’agrupació de regions, no el significat de l’altura ni la resolució. La vectorització conserva vores de cel·la; no recupera una frontera contínua exacta.

El mapa es presenta com a cribratge topogràfic. Per parlar d’inundabilitat cal identificar una font oficial, fenomen —fluvial, litoral o un altre—, escenari, període de retorn quan correspongui, data i cobertura. Un visor WMS aporta context, però no substitueix una capa vectorial si es volen calcular àrees d’intersecció. L’absència de cartografia d’un fenomen no equival a absència de risc.

## Experiment controlat a 25 i 200 m

Es fixa una font comuna, el mateix principi de remostreig i una extensió amb origen compartit, ajustada a la graella de 200 m. Es creen les dues elevacions directament de la font; pendent i orientació es calculen després sobre cada suport.

Les graelles han de satisfer la relació 8 × 8, mateixa extensió i mateix CRS. Cal revisar també el patró de NoData: compartir resolució nominal no garanteix que es comparin les mateixes posicions avaluables. El contrast entre els dos productes oficials publicats continua separat d’aquest experiment.

La taula de reclassificació es fixa abans de comparar resultats. La màscara de l’experiment combina elevació inferior a 20 m i pendent inferior a 2°; no reutilitza el criteri litoral de 2 m com si fos la mateixa pregunta. Les llegendes i l’escala cartogràfica han de permetre una comparació coherent.

El cas calculat utilitza mitjana d’àrea per remostrejar directament la font comuna i graelles niades amb origen compartit. La classificació de cota utilitza els intervals inferior a 20 m, 20–50 m, 50–100 m i igual o superior a 100 m, amb la frontera inferior inclosa en cada classe.

| Mesura municipal del cas calculat | 25 m | 200 m |
| --- | ---: | ---: |
| Cel·les vàlides segons el control per centres | 34.733 | 545 |
| Elevació mitjana, m | 33,12186 | 33,30754 |
| Pendent mitjà, graus | 1,48458 | 0,86961 |
| Màscara de cota i pendent, proporció certa | 0,24510 | 0,25688 |

Table: Comparació sobre el mateix municipi amb la graella comuna del cas resolt.

El retall rectangular fi té 424 × 344 cel·les. En aquest àmbit, la font aporta també zeros vàlids; la màscara municipal és la que introdueix absències fora del polígon. La classificació de cotes inferiors a 2 m identifica 2.068 cel·les municipals, equivalents a 1.292.500 m² abans d’interpretar-ne cap significat territorial. La nova alineació i el remostreig expliquen per què aquestes xifres no s’han d’igualar a les del retall històric.

# Controls i interpretació

`native:zonalstatisticsfb` opera sobre el municipi d’informe. El seu recompte pot incorporar fraccions d’intersecció quan s’activa la passada precisa en zones petites; no s’ha de forçar a enter. Un percentatge de cobertura requereix un denominador compatible amb la regla utilitzada, no només àrea vectorial dividida per mida de píxel.

La revisió separa errors de dades, graella, unitats, expressió, vora i interpretació. Per a les màscares es comproven classes certes/falses i absències; per als continus, rangs, valors vàlids i mostra de cel·les. Les comparacions han de separar franja de vora i interior quan es vulgui atribuir una diferència a la resolució.

La taula `estadistiques_raster` conserva la sortida aritmètica de l’eina per diagnosticar les deu bandes. Les mitjanes dels angles i dels codis de classe no s’interpreten com una direcció dominant ni com una cota. Una síntesi direccional necessita estadística circular; les classes s’expliquen amb freqüències. La mitjana d’una màscara 0/1 sí que expressa una proporció sobre el domini avaluat.

No s’emplena prèviament la taula de l’experiment amb resultats esperats. Que una generalització acostumi a suavitzar el relleu no prova que tots els màxims o pendents hagin de disminuir en qualsevol execució.

# Paquets, mínims i ampliacions

L’alumnat continua la seva PR4 i descarrega i prepara els MDT amb les instruccions del PDF. El paquet docent conserva originals, base acumulativa, resultats de demostració, controls i comparació resolta amb composició. Les fonts, els derivats pedagògics i els deu GeoTIFF contractuals tenen funcions diferents; un exemple compartit s’identifica com a resultat de referència.

Els deu GeoTIFF conserven exactament els noms definits al LLEGIU-ME d’alumnat i al manual. Són germans del GeoPackage i del `.qgz`, amb rutes relatives; la taula estadística queda al GeoPackage. PR6 els heretarà byte per byte, sense reanomenar-los ni sobreescriure la fita anterior.

Una ampliació pot contrastar una capa oficial d’inundabilitat, variar llindars o comparar derivar-després-d’agregar amb agregar-després-de-derivar. Cal definir pregunta, entrades, controls i limitacions. Les ampliacions no substitueixen la graella coherent, els fitxers persistents ni la reobertura del nucli.

# Referències

- [Model i anàlisi ràster, manual TIG](https://geourv.github.io/tig/ca/chapters/model-analisi-raster/).
- [Proveïdor GDAL a QGIS 3.44](https://docs.qgis.org/3.44/en/docs/user_manual/processing_algs/gdal/index.html).
- [SNCZI, MITECO](https://www.miteco.gob.es/es/agua/temas/gestion-de-los-riesgos-de-inundacion/snczi.html).
