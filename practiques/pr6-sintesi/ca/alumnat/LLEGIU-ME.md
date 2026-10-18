---
title: "PR6 · Model de Processament i síntesi del projecte"
lang: ca
recipient: alumnat
content_status: approved
subject: "Tecnologies de la Informació Geogràfica"
subject_code: "21234114"
author: "Benito Zaragozí"
institution: "Universitat Rovira i Virgili"
---

# Encàrrec i resultats d’aprenentatge

Com es converteix una petita operació geogràfica en una eina que es pugui executar sobre altres municipis? La pràctica formalitza el procediment de PR4: **municipi → buffer → caixa envolupant**. Després utilitza aquest model com a peça d’una síntesi del projecte acumulat.

Cal construir un model parametritzat, comparar-lo amb l’execució manual i per lots, documentar-ne l’ajuda i conservar-lo tant al projecte com en un fitxer `.model3` exportable. El professor concreta a classe i a Moodle els apartats obligatoris del **70% bàsic**, inclosa la síntesi guiada. Una funcionalitat pròpia addicional pot contribuir al **20% d’ampliacions**, amb controls explícits. PyQGIS i SQL són vies opcionals posteriors al model gràfic.

# Punt de partida i dades

Amb QGIS tancat, es copia `pr5-raster-cognom.gpkg` a `sandbox/pr6-sintesi-cognom.gpkg` i es copien els deu GeoTIFF validats de PR5 a la mateixa carpeta, **sense reanomenar-los**. El `.qgz` anterior no es copia: es prepara el principal `pr6`, se’n reorienten les fonts i es crearà un projecte extern nou.

El punt de partida és la PR5 elaborada per cada estudiant, amb la traça de les descàrregues CNIG i les preparacions pròpies. El model es construeix a partir del contracte d’aquesta lectura; un cas resolt docent es consulta separadament com a exemple del funcionament esperat.

La capa `municipi_treball` ha de contenir una sola entitat municipal, vàlida, no buida, en EPSG:25831 i amb procedència coneguda. Cal comprovar que no hi ha filtre ni selecció residuals. La capa no s’utilitza mai com a destinació.

# Procediment

## Definir el contracte del model

El model rep una capa municipal i una distància de marge en metres. Per al cas inicial s’utilitzen 500 m; el domini de treball del model és una distància positiva. El primer resultat és el buffer; el resultat final és la caixa envolupant alineada als eixos d’EPSG:25831. Són geometries diferents i tenen noms diferents.

| Element | Contracte del cas |
| --- | --- |
| Entrada vectorial | Una entitat `municipi_treball` vàlida en EPSG:25831 |
| Paràmetre | `distancia_m`, positiu, valor inicial 500 m |
| Buffer | 8 segments/quadrant, extrems i unions arrodonits, límit de mitra 2 |
| Dissolució i parts | Dissolució desactivada; separació de parts desactivada |
| Caixa | Envolupant rectangular ordinària del buffer, no rectangle mínim orientat |
| Sortides | Buffer identificat i ROI rectangular persistent |

Table: Decisions que es mantenen iguals en l’execució manual, el lot i el model.

En aquesta pràctica, `roi` designa el rectangle final. La distància de 500 m correspon al buffer intermedi, no a tots els punts de la vora rectangular. Les cantonades de la caixa poden quedar més lluny del municipi.

## Executar manualment i per lots

Es calcula el buffer amb `native:buffer` i, després, les **Caixes envolupants** (`native:boundingboxes`) sobre aquella sortida. S’utilitzen destinacions d’auditoria noves, per exemple `buffer_manual_500m` i `roi_manual_500m`, i es comproven totes dues geometries.

El lot repeteix el mateix graf amb 250, 500 i 750 m. Abans de tenir el model, s’executa un lot de buffers i després un lot de caixes, cadascuna vinculada al buffer corresponent. Cada distància conserva destinacions pròpies. Cal comparar l’evolució d’extensió i superfície; el resultat de 500 m ha de ser equivalent al manual dins de la tolerància documentada.

Una execució que ha creat un fitxer no és necessàriament correcta. Una sortida buida, una fila escrita sobre una altra o una entrada diferent invaliden la comparació encara que QGIS no hagi mostrat cap excepció.

## Construir el model al Dissenyador

Des de **Processament > Dissenyador de models**, es defineixen nom i grup, una entrada vectorial i una entrada numèrica en metres. L’entrada vectorial alimenta el buffer i la distància es vincula al seu paràmetre. La sortida del buffer alimenta l’algorisme de caixes envolupants.

Cal marcar la caixa com a sortida del model. El buffer es pot exposar també per facilitar-ne el control; si és només intermedi, la seva funció queda documentada. Les connexions entre nodes defineixen l’ordre d’execució, no la posició visual de les caixes.

L’ajuda del model explica finalitat, precondicions, unitats, valors inicials, algorismes, resultats i límits. Les comprovacions que el Dissenyador no expressi directament s’han de fer com a controls previs o posteriors identificats. **Valida el model** comprova estructura i disponibilitat d’elements; no valida la pregunta territorial ni la geometria final.

## Desar, executar i transportar el model

Es desa `pr6_roi_municipal.model3` a la carpeta de treball i es prova des del Navegador o la caixa de Processament. També s’utilitza **Save Model in project** per incorporar-ne una representació al projecte; aquesta opció no crea automàticament un `.model3` extern.

Cal desar expressament el projecte després d’incorporar-hi el model i comprovar-ne l’accés amb un altre perfil o en una ubicació neta. Un model que només existeix al perfil personal no forma part del paquet. El `.model3`, el model incrustat, el projecte extern i el projecte del GeoPackage són còpies que cal mantenir coherents.

Una execució del model amb 500 m es desa com `roi_model_500m`, separada de la sortida manual. Es comparen CRS, recompte, validesa, extrems, àrea i diferència espacial. L’objectiu és equivalència geomètrica i semàntica, no igualtat dels bytes o dels FID.

## Ampliar una funció i integrar el relleu

L’ampliació pròpia del 20% parteix d’una pregunta ja treballada i afegeix una funcionalitat al nucli guiat. Pot incorporar selecció per codi, parametrització reutilitzable o una altra operació amb sortida comprovable. Cal definir què varia, què queda fix i com es detectarà un resultat incorrecte; repetir la síntesi guiada següent no es compta també com a ampliació.

La seqüència integrada de relleu reprèn la ROI, comprova cobertura del MDT i prepara el retall amb resolució, origen i NoData declarats. Es calcula pendent en graus amb context suficient i es conserva `pr6_pendent_roi_graus.tif`. Les estadístiques zonals corresponen al municipi original, no a tot el rectangle amb marge.

No cal convertir tota la síntesi en un únic model enorme. El model petit de ROI, la branca de relleu i una altra branca reexecutada poden ser peces separades si les dependències i els controls queden clars.

# Comprovacions i interpretació

| Control | Evidència |
| --- | --- |
| Entrada | Una entitat, CRS conegut, geometria vàlida i absència d’estat residual |
| Buffer | Paràmetres del contracte, no buit i cobertura coherent amb el marge |
| Caixa | Rectangle alineat als eixos, contenidor del buffer i amb extrems comprovats |
| Equivalència | Manual, lot de 500 m i model comparats amb el mateix graf |
| Transferència | Segon municipi o entrada coneguda sense canviar rutes internes del model |
| Relleu | Graella, NoData, unitats i estadístiques sobre el municipi comprovats |
| Transport | Model i projectes reoberts sense dependre del perfil o la carpeta original |

Table: Controls del model i de la síntesi.

La síntesi ha d’explicar què aporta cada resultat a la pregunta del projecte. Una ROI és un àmbit de càlcul; el marge no certifica que s’hagi inclòs tota una conca hidrològica. Una diferència entre execucions obliga a buscar el primer pas divergent, no a editar la geometria final perquè coincideixi.

# Fitxers, evidències i enunciat de lliurament

El mínim tècnic conserva `pr6-sintesi-cognom.gpkg`, el principal incrustat `pr6`, el nou `.qgz` homònim, els deu GeoTIFF heretats de PR5, `pr6_pendent_roi_graus.tif` i `pr6_roi_municipal.model3`. També inclou una composició de síntesi, el seu PDF `pr6-sintesi-cognom-mapa.pdf` i `pr6-sintesi-cognom-apunts.pdf`, amb comparació manual/lot/model i prova de reexecució.

L’ampliació funcional, si se’n presenta una, es documenta separadament, amb entrada, decisió, resultat i control. La documentació i la presentació han de permetre explicar el projecte, no només mostrar una captura del graf. Moodle concreta els apartats seleccionats, el calendari i la forma de lliurament.

Amb QGIS tancat, es verifiquen les còpies dels GeoTIFF de PR5 i s’incorporen a `dist/` només els fitxers nous de PR6. El paquet complet s’assembla en una carpeta separada, amb els noms contractuals, i es prova després d’extreure’l en una ubicació neta. Cal obrir per separat el projecte extern, l’incrustat, els ràsters, el model i el mapa exportat.

# Ampliacions i qualificació

Una extensió petita ben contrastada pot justificar el bloc d’ampliacions. Es proposen tres preguntes:

- **Entrada per codi municipal:** incorporar un codi com a paràmetre, comprovar una selecció única i provar un codi inexistent o ambigu. La sortida es contrasta amb la selecció manual.
- **Preparació reutilitzable del relleu:** afegir un paràmetre de graella o llindar, executar-lo en un segon municipi i comparar-lo amb una preparació manual equivalent, amb NoData i cobertura declarats.
- **Diagnòstic d’entrades:** provar còpies buides, amb diverses entitats o amb CRS inadequat, i explicar quin control les detecta. Les comprovacions externes al graf també es documenten quan el model no les pot expressar.

El bonus PyQGIS/SQL és una altra via opcional dins del mateix 20%. La qualificació de PR6 té màxims de **7 punts bàsics, 2 d’ampliacions i 1 de documentació**. Es valoren funcionament i traça, pregunta i validació, i claredat d’apunts, captures, mapes i organització. No es compta una mateixa aportació com a síntesi bàsica i ampliació; ni afegir nodes ni executar més codi dona punts automàticament. La documentació també contribueix a superar la puntuació del bloc bàsic.

# Referències

- [Processament i automatització, manual TIG](https://geourv.github.io/tig/ca/chapters/processament-automatitzacio/).
- [Dissenyador de models, QGIS 3.44](https://docs.qgis.org/3.44/en/docs/user_manual/processing/modeler.html).
- [Processament per lots, QGIS 3.44](https://docs.qgis.org/3.44/en/docs/user_manual/processing/batch.html).
