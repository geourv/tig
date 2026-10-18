---
title: "PR6 · Guia docent del model de ROI i de la síntesi"
lang: ca
recipient: docent
content_status: approved
subject: "Tecnologies de la Informació Geogràfica"
subject_code: "21234114"
author: "Benito Zaragozí"
institution: "Universitat Rovira i Virgili"
---

# Propòsit i enunciat

La pràctica formalitza una petita aportació reutilitzable: obtenir una ROI rectangular a partir d’un municipi i d’una distància. La demostració ha de mostrar per què un model és més que una seqüència de botons. Una ampliació pròpia pot afegir una funció, justificada i comprovada, al nucli guiat.

El nucli obligatori inclou caixa de Processament, historial, lot, Dissenyador, model exportable i síntesi auditada. SQL i PyQGIS són ampliacions opcionals posteriors. La correcció ha de distingir una estructura que es pot executar d’un resultat geogràficament vàlid.

# Preparació i conducció de la sessió

| Component | Durada orientativa |
| --- | --- |
| Aula, model i síntesi guiada | 150–180 min |
| Treball autònom i auditoria | 120–180 min |
| Preparació docent | 45–60 min |

Table: Estimació de PR6 per al model de dos nodes i la síntesi guiada.

Estimació pendent de contrast amb una classe, amb PR5 completa i experiència amb Processament. Una funcionalitat pròpia o el bonus de codi requereixen dedicació addicional. Convé reservar un bloc final per a la prova de transport.

La preparació comprova les còpies de PR5, el model extern i la disponibilitat dels algorismes. A classe es construeix primer el graf manual i després el model; es demana quina entrada alimenta cada node i quines constants s’han fixat. Les aturades són equivalència a 500 m, execució sobre un segon municipi i reobertura amb totes les dependències. El desament al projecte es demostra i comprova separadament del fitxer extern.

# Preparar Moodle

1. Crear una **Tasca** amb el nom **PR6 · Model de ROI i síntesi del projecte**.
2. Copiar l’enunciat següent a **Descripció**, fins al final de «Qualificació». Identificar els apartats bàsics anunciats a classe i separar la síntesi guiada d’una funcionalitat pròpia del 20%.
3. Adjuntar a **Fitxers addicionals** el PDF d’alumnat. Si s’ofereix la via de codi, adjuntar també la lectura del bonus i indicar que contribueix al mateix 20%, sense puntuació duplicada.
4. Fixar dates, tramesa i mida per als projectes, els onze GeoTIFF, el model i els PDF; màxim 10 amb blocs 7/2/1. El model resolt es pot compartir com a exemple identificat.
5. Revisar la **vista d’estudiant**, els adjunts i la correspondència entre requisits i rúbrica. El paquet docent es conserva per preparar les execucions i els controls.

## Enunciat per copiar a la descripció

**Dades i objectiu.** Cal continuar la PR5 pròpia i construir el model municipi → buffer → caixa envolupant. El model rep municipi i distància en metres, conserva sortides comprovables i es documenta perquè es pugui executar en un altre cas.

**Treball bàsic —70%.** El professor selecciona a classe i recull en aquesta Tasca els apartats obligatoris de Processament, historial, lot, Dissenyador, desament i síntesi. El nucli compara manual, lot i model amb els mateixos paràmetres, comprova la transferència i conserva la branca guiada de pendent. Els deu GeoTIFF PR5 es mantenen amb els mateixos noms i contingut; la lectura completa inclou altres propostes que no són obligatòries per defecte.

**Ampliacions —20%.** Es pot afegir una funcionalitat amb pregunta i controls propis:

- Com es pot seleccionar el municipi per codi sense capturar una capa personal? Incorporar una entrada de codi, comprovar un resultat únic i diagnosticar codis inexistents o ambigus. Contrastar la geometria amb la selecció manual.
- Com es pot reutilitzar la preparació del relleu en un altre municipi? Parametritzar graella o llindar, definir cobertura i NoData i comparar la sortida amb una execució manual sobre la mateixa entrada. Repetir la branca guiada sense cap decisió nova no és una ampliació.
- Com es detecta una entrada inadequada abans d’interpretar el resultat? Dissenyar un conjunt petit de proves sobre còpies —capa buida, diverses entitats o CRS incorrecte— i explicar quin control les detecta. Si el graf no pot expressar-lo, conservar el control extern documentat.

El bonus PyQGIS/SQL és una altra via opcional del mateix bloc, amb el seu contracte de comparació.

**Documentació i lliurament —10%.** La base és `pr6-sintesi-cognom`, amb GeoPackage, principal `pr6`, `.qgz`, mapa i apunts. L’acompanyen els deu GeoTIFF PR5, el nou pendent `pr6_pendent_roi_graus.tif` i el model extern `pr6_roi_municipal.model3`. Cal conservar ajuda, paràmetres, controls i prova de reexecució, i comprovar separadament el model desat als projectes. El conjunt complet es reobre en una ubicació neta.

**Qualificació.** Fins a **7 punts** pel nucli seleccionat, funcional i contrastat; **2 punts** per ampliacions justificades i validades; **1 punt** per apunts, mapes, captures i organització. La síntesi guiada i una extensió pròpia no es puntuen dues vegades com la mateixa aportació. Els màxims no són automàtics; les ampliacions no substitueixen els obligatoris i la documentació aporta puntuació pròpia.

# Entrades i continuïtat

La instantània PR6 copia físicament el GeoPackage de PR5 i els deu GeoTIFF amb els mateixos noms. El projecte principal és `pr6`; el `.qgz` es crea de nou. Totes les fonts locals, incloses les de les vistes conservades, han de deixar de dependre de PR5 o de `dist/`.

El model petit rep una sola entitat municipal vàlida en EPSG:25831 i una distància positiva en metres. La demostració usa Vila-seca i 500 m; la transferència pot utilitzar el municipi propi o un segon cas de control. S’han de conservar les entrades canòniques i les destinacions d’auditoria separades.

# Graf i paràmetres

El graf d’aquesta pràctica conté **dos passos geomètrics**: `native:buffer` i `native:boundingboxes`. El primer construeix el marge; el segon, el rectangle alineat amb els eixos. El buffer s’identifica com a intermedi i la caixa és la ROI final.

| Paràmetre o decisió | Valor del cas comparat |
| --- | --- |
| Distància | 500 m en la comparació principal; 250/500/750 m en el lot |
| Segments | 8 per quadrant |
| Extrems i unions | Arrodonits |
| Límit de mitra | 2 |
| Dissolució | Desactivada |
| Separar parts disjuntes | Desactivat |
| Envolupant | Caixa ordinària alineada als eixos d’EPSG:25831 |

Table: Constants i paràmetre variable del model de ROI.

La distància del buffer no és la distància de cada punt del rectangle al municipi. El control de la caixa és contenció, rectangularitat, alineació i extrems; no s’hi trasllada una banda de distàncies pensada per al buffer.

# Demostració manual, lot i model

La primera execució manual conserva `buffer_manual_500m` i `roi_manual_500m`. Abans de tenir el model, s’encadenen un lot de buffers i un lot de caixes, comprovant la correspondència entre entrades i sortides de cada distància. El model també ha de contenir tots dos passos: comparar una caixa amb un buffer perquè tots dos s’anomenen ROI seria una prova incorrecta.

Al Dissenyador es distingeixen entrada del model, valor fix, sortida d’un algorisme i sortida exposada del model. La distància numèrica porta la unitat a la descripció i un domini admès. El model no ha de capturar una ruta personal o l’ID d’una capa temporal com a entrada immutable accidental.

L’ajuda explica pregunta, supòsits, esquema, CRS, paràmetres, resultats i errors. La validació formal del model comprova estructura i disponibilitat; la validació de dades exigeix executar-lo i comparar-ne la sortida. Les precondicions que no es puguin representar al graf es comproven explícitament abans o després.

Una prova negativa pot utilitzar una còpia amb zero municipis, diverses entitats o CRS inadequat. El procediment ha de detectar la precondició incorrecta de manera interpretable, sense considerar un fitxer creat com a prova d’èxit. Les dades canòniques no es modifiquen per fer aquella prova.

# Model extern i model al projecte

QGIS permet desar `.model3` i utilitzar **Save Model in project**. La segona opció incorpora el model al fitxer de projecte i el fa accessible entre els models del projecte; no escriu automàticament un `.model3` extern. Es mostren i es comproven totes dues vies.

El model al perfil personal és una comoditat d’execució, no una peça transportada. Cal exportar `pr6_roi_municipal.model3`, desar el projecte i reobrir-los des d’una ubicació neta. El projecte extern i el del GeoPackage es comproven separadament; si tots dos han d’incloure el model, s’ha de verificar cadascuna de les representacions desades.

La versió, els proveïdors i les entrades continuen sent dependències. Que el graf viatgi amb el projecte no incorpora automàticament MDT, tipografies, connexions ni dades externes. La prova de transport ha d’obrir el model i resoldre totes les peces requerides des d’una ubicació nova.

# Ampliació pròpia i síntesi

L’ampliació del 20% ha de resoldre una necessitat addicional sobre dades ja conegudes: selecció per codi, paràmetre reutilitzable o branca vectorial contrastada. Cal exigir contracte i controls abans d’afegir nodes. La integració guiada del relleu que segueix pertany al nucli; només una funcionalitat addicional justificada es valora com a ampliació.

La seqüència integrada de relleu utilitza la ROI rectangular com a àmbit, conserva el suport necessari per als derivats i produeix `pr6_pendent_roi_graus.tif`. Es documenten resolució, origen, extensió, NoData, fórmula i unitats; el resum zonal s’aplica al municipi original. No substitueix els deu GeoTIFF heretats.

El model petit, la branca integrada i una reexecució de control del projecte acumulat poden ser peces separades. Això facilita localitzar el primer pas divergent i evita convertir la síntesi en un graf gran que només funciona en una sessió concreta.

# Controls d’acceptació

| Dimensió | Criteri |
| --- | --- |
| Entrada | Una entitat, validesa, CRS i absència de filtres/seleccions residuals |
| Geometria intermèdia | Buffer coherent amb els paràmetres fixats |
| Geometria final | Caixa contenidora alineada als eixos, extrems i àrea comprovats |
| Comparació | Manual, fila de 500 m del lot i model equivalents dins de la tolerància declarada |
| Generalització | Segon cas executat sense reescriure dependències ocultes |
| Relleu | Graella, domini vàlid, rang del pendent i estadístiques municipals coherents |
| Paquet | Projectes, model i dades reoberts sense l’arrel original ni el perfil personal |

Table: Controls del nucli i de la seva integració.

La comparació geomètrica pot utilitzar diferència simètrica, extrems, àrea, recompte i validesa. L’ordre de vèrtexs o els identificadors interns poden canviar sense alterar el resultat semàntic. Una coincidència de superfície sola tampoc no basta, perquè geometries diferents poden tenir la mateixa àrea.

El cas resolt executa el fitxer extern `pr6_roi_municipal.model3` a QGIS 3.44.11. A Vila-seca, buffer i caixa de 500 m coincideixen geomètricament amb les execucions manual i per lots; una segona execució sobre Reus comprova la transferència sense editar el graf. Els deu GeoTIFF de PR5 es conserven byte per byte, i la branca de pendent reexecutada des dels MDT originals conserva el domini i els valors comprovats.

Les entrades internes del model d’exemple s’anomenen `MUNICIPI` i `DISTANCIA`. Aquesta última correspon al paràmetre `distancia_m` del guió i es mostra al diàleg com a marge en metres.

El fitxer extern i les seves sortides són peces verificades del cas de referència. El desament del model dins de cada representació del projecte és una comprovació separada: l’execució correcta del `.model3` no acredita, per si sola, l’opció **Save Model in project**.

# Paquets i revisió de l’enunciat

L’alumnat conserva la PR5 pròpia i construeix el model amb el contracte del PDF. El suport docent inclou originals, base acumulativa, model resolt, sortides manual/lot/model, controls i composició de síntesi. Un exemple resolt compartit facilita el contrast del funcionament; el treball propi ha de conservar la traça i la reexecució del seu model.

Els mínims es valoren per funcionament i traça; les ampliacions, per pregunta i validació; la documentació, per capacitat de reconstrucció i explicació. Moodle concreta apartats seleccionats, dates i tramesa amb els blocs 70/20/10. Una captura del graf o una exportació PDF del diagrama no substitueixen el `.model3` executable.

El paquet final conserva el GeoPackage PR6, el `.qgz` homònim, els deu GeoTIFF de PR5 amb els noms originals, el nou pendent, el model, el mapa i els apunts. Les correccions es fan a les fonts i es regeneren els descendents; una fita lliurada anterior es conserva intacta.

# Referències

- [Dissenyador i desament de models, QGIS 3.44](https://docs.qgis.org/3.44/en/docs/user_manual/processing/modeler.html).
- [Caixa de Processament, QGIS 3.44](https://docs.qgis.org/3.44/en/docs/user_manual/processing/toolbox.html).
- [Processament i síntesi, manual TIG](https://geourv.github.io/tig/ca/chapters/processament-automatitzacio/).
