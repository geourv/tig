---
title: "PR4 · Guia docent d’envolupants, distàncies i geoprocessament"
lang: ca
recipient: docent
content_status: draft
subject: "Tecnologies de la Informació Geogràfica"
subject_code: "21234114"
author: "Benito Zaragozí"
institution: "Universitat Rovira i Virgili"
---

# Finalitat i resultats d’aprenentatge

La pràctica desenvolupa el pas de consultar entitats a derivar geometries. Comença amb les envolupants del municipi, desenvolupa distància i buffer i construeix la ROI rectangular. Aquest àmbit comú permet preparar punts, línies i polígons, contrastar superposicions i obtenir peces i punts derivats. Les comparacions es vinculen al capítol 6 i a la continuïtat ràster.

La seqüència ha de permetre predir què conservarà cada algorisme i comprovar-ho després. Processament forma part del recorregut principal; la programació d’un model de reproducció és una eina d’autoria, no un requisit previ perquè l’alumnat pugui executar els procediments de QGIS.

# Preparació i conducció de la sessió

| Component | Durada orientativa |
| --- | --- |
| Aula, recorregut complet amb demostracions | 210–270 min |
| Treball autònom i apunts | 150–210 min |
| Preparació docent | 45–60 min |

Table: Estimació de PR4, sense afegir-hi el taller de tessel·lacions.

Estimació pendent de contrast amb una classe, amb PR3 validada i fonts descarregades. Convé repartir-la en tres blocs: envolupants, distància i ROI; preparació, superposicions i peces; punts derivats i comparacions seleccionades. El recorregut complet és més ampli que una sessió ordinària: el professor concreta a Moodle els apartats obligatoris. Les ampliacions tenen dedicació addicional segons la pregunta.

La preparació comprova IDs, capes heretades i una còpia del cas sintètic. Abans de cada operació es demana una predicció sobre geometria i atributs; després es contrasta amb la sortida desada. Les aturades determinants són la pèrdua d’identitat en dissoldre, les peces coincidents de la unió i la diferència entre buffer i caixa. Una taula de fragments i mesures és necessària per explicar un mapa que visualment sembla correcte.

# Preparar Moodle

1. Crear una **Tasca** anomenada **PR4 · Buffers, superposicions i ROI**.
2. Copiar a **Descripció** l’enunciat fins al final de «Qualificació». Concretar les comparacions obligatòries indicades a classe, preservant la ROI de continuïtat.
3. Adjuntar a **Fitxers addicionals** el PDF d’alumnat. Si s’incorpora el taller Reus, afegir-ne la lectura i indicar si forma part del 70% o és una opció del 20%; una mateixa aportació es valora una sola vegada.
4. Configurar dates, tramesa completa i límit de mida, amb màxim 10 i blocs 7/2/1. Identificar qualsevol joc sintètic compartit com a demostració geomètrica.
5. Revisar la **vista d’estudiant**, els adjunts i la selecció d’apartats. El paquet docent permet preparar i contrastar els casos resolts.

## Enunciat per copiar a la descripció

**Dades i objectiu.** Cal continuar la PR3 pròpia, conservar l’herència i derivar geometries amb Processament. Les entrades són els límits CNIG, les fonts provincials de CartoCiudad i del viari, les preparacions de PR3 i els generadors de PR2 o un escenari sintètic declarat. La ROI inclou entorn exterior al terme; una selecció només municipal pot ser insuficient. El resultat ha d’explicar l’efecte de les decisions i conservar la ROI per a PR5.

**Treball bàsic —70%.** El professor selecciona a classe i enumera en aquesta Tasca les preparacions, superposicions, comparacions de buffers, parts i punts derivats obligatòries. Cal preservar IDs, recalcular mesures i comprovar les sortides persistents. La `roi` de continuïtat és la caixa alineada als eixos d’EPSG:25831 del buffer municipal de 500 m. Les altres variants de la guia no són totes obligatòries per defecte.

**Ampliacions —20%.** Una aportació pot desenvolupar una pregunta com aquestes:

- Quina part d’un sector queda fora de tots els buffers? Definir un univers finit, calcular-ne la diferència i comprovar que zona zero i cobertura formen una partició completa, amb àrees compatibles. La interpretació és geomètrica, no d’il·luminació.
- Què passa amb un atribut extensiu quan un polígon es fragmenta? Utilitzar un total sintètic declarat, comparar duplicació i repartiment proporcional i comprovar la conservació del total. Explicar la hipòtesi d’homogeneïtat que exigeix el repartiment.
- Quanta superfície de càlcul afegeix cada envolupant? Comparar àrea exterior i extensió sobre la mateixa entrada, comprovar-ne contenció i justificar la tria per a una graella no rotada. Aquesta anàlisi ha d’afegir criteri al simple càlcul de les formes.

**Documentació i lliurament —10%.** La base és `pr4-geoprocessament-cognom`: GeoPackage amb principal `pr4`, `.qgz`, mapa comparatiu i apunts PDF. Cal registrar paràmetres, IDs, controls, toleràncies, incidències i interpretació. El mapa diferencia generadors, derivats i ROI; les captures acrediten decisions concretes. Es prova el conjunt en una ubicació neta.

**Qualificació.** Fins a **7 punts** pels obligatoris correctes i comprovats, **2 punts** per ampliacions amb pregunta i contrast i **1 punt** per documentació, lectura dels mapes i organització. Els màxims no són automàtics ni es reparteixen segons el nombre de capes. Les ampliacions no substitueixen els obligatoris; la documentació també pot augmentar la nota respecte del bloc bàsic.

# Punt de partida i dades

Cal verificar la PR3 completa, inclosa la presència de `fanals`, `carrils_bici` i `plaques_solars` procedents de PR2. El GeoPackage de PR4 és una còpia nova, amb fonts locals reorientades, principal `pr4` i `.qgz` nou. Els IDs dels generadors es conserven abans de qualsevol transformació.

El límit de treball s’identifica per productor, edició i capa, conservant la traça de la descàrrega CNIG pròpia. El pilot municipal de 500 m utilitza una font CNIG preparada; cal contrastar-la amb l’edició i la transformació de la cadena nova. Els seus recomptes o mesures no s’imposen a una entrada diferent.

Per avançar el cas dels fanals es pot emprar un escenari sintètic declarat. L’exemple històric té tres punts alineats i separats 45 m, amb IDs propis i estat `no_apte_per_analisi`. La reutilització docent manté l’original i identifica el derivat com `fanals_sintetics`: és apte per contrastar geometria ideal, no per concloure sobre l’enllumenat real de Joanot Martorell.

# Procediment de demostració

Les comparacions conserven la mateixa entrada mentre varia una decisió. Cada sortida es desa amb els paràmetres i la clau d’origen perquè es pugui reprendre el control després de tancar QGIS.

## Envolupants del municipi i selector del tipus

La primera vista mostra l’Explorador amb les connexions als tres GeoPackage: projecte PR4, CartoCiudad i viari CNIG. El WMS IGN/PNOA es carrega sota els vectors, amb contorns sense farciment. Cal comprovar CRS i una mostra de coincidències territorials. Les connexions de l’Explorador es recreen al perfil de l’equip quan calgui; no s’han de confondre amb les referències desades al projecte.

La primera entrada de la demostració és `municipi_treball`, **sense buffer**. Es comparen caixa alineada, rectangle orientat, cercle mínim i convexa mitjançant `qgis:minimumboundinggeometry`, amb `TYPE` 0, 1, 2 i 3. Cal mostrar que és un selector de la mateixa eina i distingir conjunt, grup per camp i càlcul per entitat.

![Eina de geometria delimitadora mínima](assets/img/qgis/qgis-c06-envolupants-tipus.png "L’entrada és el terme original. El camp d’agrupació és opcional i no equival a demanar una envolupant per fila.")

![Envolupants del mateix municipi](assets/img/qgis/qgis-c06-envolupants-comparacio.png "La comparació manté entrada i CRS: caixa verda, rectangle orientat blau, cercle taronja, convexa violeta i terme magenta.")

La pregunta d’aturada és quin espai afegeix cada forma i per què. S’esperen contenció i validesa; les mesures han de correspondre a la mateixa entrada. El cercle discretitzat necessita una tolerància vinculada a l’aproximació. Aquest bloc no utilitza encara el buffer de 500 m.

## Distàncies, buffer i ROI

Abans d’obrir Buffer es distingeixen distància mínima entre geometries, distància entre centroides i distància de recorregut. Els metres requereixen una preparació explícita en EPSG:25831; canviar només el CRS de la vista no reprojecta la font. La segmentació aproxima corbes i no millora l’exactitud topogràfica.

Es calcula el buffer municipal de 500 m amb 8 segments per quadrant i dissolució desactivada. La caixa ROI es deriva després d’aquest buffer amb l’algorisme de caixetins delimitadors.

![Configuració del buffer municipal](assets/img/qgis/qgis-c06-buffer-municipal.png "La distància s’ha explicat abans d’arribar al diàleg. La sortida persistent es reobre i se’n comproven validesa, contenció i mesures.")

`native:boundingboxes` produeix la capa `roi`. Cal preguntar per què les cantonades no es troben a 500 m del terme i per què s’incorporen municipis veïns. La preparació reprèn els originals provincials, conserva `id_font`, extreu candidats amb geometries senceres i els reprojecta a EPSG:25831.

![Municipi, buffer i caixa ROI](assets/img/qgis/qgis-c06-roi-desada.png "La caixa del buffer, verda, és la ROI de continuïtat. No es confon amb la caixa inicial del terme ni amb una franja de distància constant.")

## Preparació de les fonts provincials

La demostració de rendiment diferencia capa oculta, filtre de capa, filtre de taula i selecció. Es pot processar sense dibuixar tota la província ni obrir-ne la taula. El filtre de capa afecta també moltes entrades de Processament: convé comparar-ne el recompte i el criteri, sense atribuir una acceleració concreta a una prova que no s’ha cronometrat.

## Un retall de cada tipus geomètric

El cas compara portals filtrats per `tipo = Portal`, viari de totes les classes i illes de CartoCiudad. Es fan dos retalls i una intersecció d’illes amb el camp de màscara `id_roi`. Un punt només es conserva o s’exclou; una línia o un polígon poden fragmentar-se. Les captures dels diàlegs documenten la configuració, i els resultats reoberts i els controls acrediten el càlcul.

| Preparació | Candidats | Sortida dins de la ROI |
| --- | ---: | ---: |
| Punts Portal/PK; després filtre Portal | 17.793 | 16.756 |
| Viari de totes les classes | 10.262 | 9.780 |
| Illes | 1.490 | 1.399 |

Table: Referències del cas CNIG amb límits de juliol de 2026, CartoCiudad d’abril de 2026 i viari de juliol de 2026.

![Resultats dels retalls de punts, línies i polígons](assets/img/qgis/qgis-c06-retalls-resultat.png "Els tres tipus de geometria comparteixen la mateixa ROI, que incorpora territori exterior a Vila-seca. Els registres viaris no equivalen necessàriament a trams diferents.")

## Diferències i interpretació dels components

Per al context marí, `terra_roi` és la unió dels recintes administratius retallats. Intervenen vuit municipis: Cambrils, Constantí, Reus, Riudoms, Tarragona, Vila-seca, Salou i la Canonja. La diferència `roi − terra_roi` conserva cinc components i 14,826 km². Cal examinar-los amb l’ortofoto: una geometria exterior als recintes no es classifica com a mar només pel nom de la sortida.

El cas conserva la diferència sencera i selecciona dos components connectats amb punts marins de contrast prop de les cantonades sud-oest i sud-est, amb 14,447 km². Els altres components continuen disponibles per inspecció. La selecció no és una regla general de «conservar el polígon més gran», ni una nova costa oficial; a l’entorn portuari cal distingir límit administratiu i superfície d’aigua.

![Context marí derivat sobre el WMS](assets/img/qgis/qgis-c06-mar-resultat.png "El context marí és una interpretació acotada del complement. El WMS ajuda a revisar ports, costa i components; la diferència completa es conserva.")

La segona diferència utilitza els 5.475 registres `Urbano` de `viari_roi`. Es comparen buffers dissolts de 5 i 10 m i es resten de `terra_roi`. La conversió multipart a monopart produeix 1.330 i 1.131 parts, respectivament. La disminució del recompte no és una prova que el radi major sigui millor: pot eliminar peces petites o unir exclusions. Cal contrastar amb `manzana`, ortofoto, límits i discontinuïtats del viari.

La pregunta WKT és quantes files i quantes parts descriu una geometria `MULTIPOLYGON`. Després de separar-la, es conserva la clau d’origen, es crea `id_peca` i es comprova que la suma d’àrees correspon a la diferència original. Els atributs repetits no s’han de sumar automàticament.

## Centroides, punts sobre superfície i vèrtexs

El cas calcula un centroide per entitat sobre les illes i sobre els carrers. El centre lineal pondera per longitud, no identifica necessàriament una posició sobre el traçat ni el punt de mitja longitud. Entre les 1.399 illes, 35 centroides queden fora del seu polígon; aquest resultat permet discutir la diferència entre centre geomètric i punt interior.

![Diàleg de centroides sobre les illes](assets/img/qgis/qgis-c06-centroides.png "L’opció d’un punt per entitat es manté constant en la comparació. En multipart, un punt per part respon una pregunta diferent.")

![Diàleg de punts sobre la superfície](assets/img/qgis/qgis-c06-punt-superficie.png "Els punts sobre superfície es contrasten amb la geometria d’origen. La pertinença al polígon no implica que siguin accessos o centres funcionals.")

L’extracció de vèrtexs produeix 137.919 files per a les illes i 92.789 per als carrers urbans. Es comproven coordenades i índexs contra les geometries d’origen. Cal recordar els vèrtexs de tancament i les coordenades coincidents: nombre de files i nombre de posicions diferents són preguntes distintes.

![Extracció dels índexs inicial i final de les línies](assets/img/qgis/qgis-c06-extrems-linies.png "Els índexs 0 i −1 identifiquen el primer i l’últim vèrtex de l’entitat. Per treballar amb els extrems de cada part cal separar abans les geometries multipart.")

Aquest bloc acaba amb punts derivats i comprovats. La construcció de tessel·lacions correspon al taller posterior, amb decisions pròpies sobre duplicats, domini i generadors externs.

## Sensibilitat dels buffers

La primera demostració conserva el generador i varia un únic paràmetre cada vegada. Sobre punts es proposen radis de 10, 30 i 50 m; sobre una línia oberta, 10 m amb extrems arrodonits, plans i quadrats; sobre el municipi, 500 m. La comparació de 4, 8 i 16 segments per quadrant manté constants entrada i radi.

Els tres punts amb separació 45 m ofereixen prediccions controlables: 10 m no arriba al veí, 30 m permet solapaments de parelles consecutives i 50 m pot generar una zona comuna als tres. Són prediccions del disseny sintètic que s’han de comprovar a les geometries persistides, no resultats d’un inventari de fanals.

Cal contrastar extrems de línia i unions de cantonades. Un buffer amb extrems plans o quadrats no representa exactament el mateix conjunt de proximitat que un d’arrodonit. El límit de mitra condiciona prolongacions de les unions en punta. Els controls han de correspondre als paràmetres utilitzats, no a una única banda de distància aplicada indiscriminadament.

En un buffer puntual regular es pot comparar l’aproximació de la circumferència amb el nombre de segments. Als arcs parcials de geometries lineals i poligonals, la subdivisió del motor pot ser diferent. Més vèrtexs no impliquen més exactitud posicional de la cartografia d’entrada.

La dissolució es construeix com a segona sortida. Cal comparar la suma d’àrees individuals amb l’àrea única i conservar la identitat dels generadors a la primera capa. Els atributs retinguts per `native:dissolve` no s’interpreten com sumes, mitjanes o recomptes del grup.

## Retall, intersecció i diferència

El viari seleccionat a PR3 proporciona trams que travessen el terme. Es compara el resultat complet de la selecció amb `native:clip` i `native:intersection`. Si s’utilitza la mateixa màscara municipal, cal observar tant la geometria comuna com la diferència d’esquema.

La validació manté una clau d’origen independent dels FID, comprova fragments i recalcula longituds. Les files associades a diferents itineraris no es converteixen en eixos únics per haver estat retallades. La unitat analítica s’ha de decidir abans de sumar o deduplicar.

Els punts nous d’intersecció poden introduir arrodoniments de coma flotant. Una diferència simètrica exacta entre línies pot comptar segments gairebé coincidents com a diferents. La comparació combina identitats, conservació de longitud per registre i distància geomètrica amb una tolerància numèrica explícita; aquesta tolerància no representa l’exactitud de la font.

Amb polígons, convé mostrar un atribut extensiu copiat a diversos fragments. Sumar-lo repeteix el valor original; repartir-lo proporcionalment a l’àrea exigeix una hipòtesi addicional. La diferència i la diferència simètrica es poden introduir sobre el mateix parell de geometries, explicant-ne direcció i significat.

## Unió i nombre de generadors

La petjada conjunta i la multiplicitat de cobertura són productes diferents. Una dissolució elimina fronteres internes; una unió ajuda a identificar les peces, però no garanteix per si sola una capa de zones exclusives amb recompte correcte.

Segons el contracte de QGIS 3.44, `native:union` sense `OVERLAY` divideix les coincidències de la mateixa capa i conserva peces coincidents per als participants. Amb `OVERLAY`, talla entre capes i no divideix automàticament les coincidències internes de cadascuna. La demostració ha de mostrar les files coincidents, no només acolorir-les com si fossin zones independents.

Es conserva la unió bruta amb procedència, se separen les parts que calgui i s’obtenen geometries de peça úniques. La deduplicació geomètrica no constitueix un resum d’atributs: l’`id_fanal` de la fila que sobrevisqui no representa tots els generadors. El recompte es reconstrueix sempre contra els buffers individuals originals.

Cada peça rep un `id_zona` i un punt interior. Un resum per ubicació compta els valors diferents d’`id_fanal` dels buffers que contenen aquest punt; el resultat torna a la peça per `id_zona`, com `n_fanals`. Cal inspeccionar les peces petites i comprovar interiors disjunts. Un centroide que quedi fora de la peça no és un substitut vàlid del punt interior.

| Control | Condició |
| --- | --- |
| Generadors | `id_fanal` únic i no nul; un buffer individual per generador admès |
| Peces | Geometries vàlides, àrea positiva i interiors disjunts |
| Multiplicitat | `n_fanals` enter, entre 1 i el nombre d’IDs diferents |
| Cobertura | Unió de peces equivalent a la petjada dissolta |
| Conservació ponderada | Suma d’àrea de peça per multiplicitat equivalent a suma d’àrees individuals |
| Casos coneguts | Regions d’un, dos i tres generadors contrastades amb la geometria sintètica |

Table: Controls independents del mapa de solapaments.

La identitat ponderada és:

$$
\sum_j n_j\,A(Z_j)=\sum_i A(B_i),
$$

on les peces $Z_j$ formen una partició de la cobertura i $B_i$ són els buffers individuals. S’avalua amb les mateixes geometries poligonals i mesura plana, dins d’una tolerància numèrica justificada. No és una comparació amb l’àrea teòrica de cercles perfectes.

La zona zero necessita un univers explícit, com el corredor d’estudi, i la diferència respecte de la cobertura. No s’infereix de l’absència de files a la unió. El mapa de `n_fanals` representa multiplicitat geomètrica, no intensitat lluminosa ni suficiència del servei.

## Sensibilitat de les envolupants sobre el buffer

La comparació addicional utilitza `municipi_buffer_500m` com a entrada comuna de les quatre formes. Aquestes mesures es distingeixen de les envolupants inicials del terme. Es comproven contenció, àrea i extensió; el cercle d’aquesta comparació s’ha discretitzat amb 720 segments.

La caixa alineada als eixos es desa com `roi`. És la decisió de continuïtat cap a una graella ràster no rotada en EPSG:25831, no una afirmació que sigui la geometria més ajustada. Es conserven el rectangle orientat i les altres envolupants com a comparacions. L’alineació futura de cel·les a PR5 és una operació posterior i pot ampliar l’extensió.

Un rectangle orientat de mínima àrea no és un polígon dibuixat a ull seguint la costa. El cercle mínim no és el buffer d’un centre qualsevol i l’envolupant convexa no conserva concavitats ni forats. Aquestes diferències s’han d’interpretar sobre la mateixa entrada, sense canviar-ne el límit entre proves.

# Comprovacions i interpretació

El cas complementari d’envolupants, ROI, retalls, diferències i punts s’ha executat amb QGIS 3.44.11 i **143 controls** sobre fonts i sortides persistides. Conserva 34 capes vectorials, incloses les quatre envolupants del terme original. Els projectes externs i incrustats s’han reobert sense xarxa; el WMS s’afegeix a l’escena de captura online. La configuració d’un diàleg no substitueix el càlcul ni la reobertura de la sortida.

El pilot retingut `tig-buffer-municipal-500m` constitueix una referència acotada: una entitat CNIG, 500 m, 8 segments per quadrant, unions arrodonides i dissolució desactivada. Disposa de 30 controls retinguts i d’una banda contínua contrastada d’aproximadament 494,5782549823905 a 500,01 m respecte del límit original. El mínim mesurat del run acceptat és 495,0869662890991 m.

Aquesta banda correspon al cas i al mecanisme d’aproximació estudiats; no és l’exactitud topogràfica de la font ni un criteri universal per als nous buffers. El pilot no valida automàticament les variants de PR4, les unions o les envolupants. Cada cas nou necessita resultats persistits, controls pertinents i reobertura pròpia.

Per a `roi` es comproven una geometria rectangular vàlida, EPSG:25831, alineació amb els eixos, extrems coherents i contenció del buffer. Per a les superposicions es registren fragments, IDs, nuls dels atributs i mesures recalculades. Les discrepàncies es diagnostiquen sense descartar peces silenciosament ni ajustar llindars per fer passar el resultat.

# Aplicació al municipi escollit

La revisió exigeix una comparació de paràmetres i una interpretació, no només una carpeta de sortides. Els resultats sobre el municipi propi s’han de distingir de la demostració sintètica. Si l’inventari real és incomplet, el recompte descriu només els generadors disponibles i aquella cobertura de captura.

L’elecció final de ROI ha de quedar prou documentada perquè una altra persona pugui reprendre el projecte a PR5. Els criteris de revisió de la pràctica inclouen geometria, esquema, conservació de l’herència, lectura cartogràfica i límits de la conclusió.

# Fitxers i evidències

La base del nom és `pr4-geoprocessament-cognom`, per al GeoPackage i el `.qgz` homònim, amb principal `pr4`. S’hi afegeixen el mapa comparatiu i els apunts, amb els sufixos `-mapa.pdf` i `-apunts.pdf`.

L’alumnat prepara les operacions sobre la seva PR3 seguint el PDF. El paquet docent conserva originals, base acumulativa, variants, resultats i controls; es pot compartir el cas resolt com a exemple identificat.

Cal conservar un registre de paràmetres, errors i correccions, i comprovar els projectes externs i incrustats des d’una ubicació neta. La reobertura de la còpia s’ha de fer sense utilitzar el GeoPackage predecessor com a font alternativa. La presència de captures o d’un PDF no substitueix aquests controls sobre les dades.

El desenvolupament conceptual es pot consultar al [manual TIG](https://geourv.github.io/tig/ca/chapters/analisi-geoprocessament-vectorial/). La documentació de QGIS 3.44 concreta els contractes d’[Unió i superposicions](https://docs.qgis.org/3.44/en/docs/user_manual/processing_algs/qgis/vectoroverlay.html#union) i de [geometria vectorial](https://docs.qgis.org/3.44/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html).
