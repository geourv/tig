---
layout: manual-chapter
title: Anàlisi i geoprocessament vectorial
description: Envolupants, distàncies, superposicions i tessel·lacions, amb casos CNIG de Vila-seca i Reus i un atlas de cobertura regular.
lang: ca
ref: manual-vector-analysis-geoprocessing
profiles: [unaltremanual]
content_status: approved
permalink: /ca/chapters/analisi-geoprocessament-vectorial/
weight: 70
part: Continguts
manual_references: true
---

Quina geometria permet delimitar un àmbit de treball, conservar-ne l'entorn i comparar després punts, carrers i illes? Una consulta identifica entitats; el **geoprocessament** en pot construir de noves. El recorregut comença amb formes senzilles que contenen un municipi, incorpora distàncies i superposicions i acaba amb unitats per resumir dades, estudiar veïnatges i organitzar un atlas.

Vila-seca proporciona el cas de preparació i transformació de geometries. Reus permet seguir els mateixos portals de CartoCiudad a través d'una malla regular, una triangulació i un diagrama de Voronoi. A cada pas cal distingir la pregunta territorial, l'operació geomètrica i allò que realment acredita la sortida.

>>>>> En acabar el capítol, cal poder construir i comprovar un recorregut vectorial amb resultats persistents.
>>>>>
>>>>> - Escollir una envolupant i justificar distàncies, CRS i paràmetres del buffer.
>>>>> - Distingir selecció, retall, intersecció, diferència, unió i dissolució, inclosos els efectes sobre els atributs.
>>>>> - Derivar parts, punts representatius i vèrtexs sense perdre la identitat d'origen.
>>>>> - Interpretar malles, arestes de Delaunay i dominis de Voronoi amb controls de recompte, proximitat i vora.
>>>>> - Preparar tessel·les com a cobertura d'un atlas i comprovar ordre, escala i enquadrament de les pàgines.

## Envolupants del municipi

Una **envolupant** resumeix l'extensió d'una geometria o d'un conjunt de geometries mitjançant una forma que els conté. És útil per definir una àrea de cerca, preparar un retall o comparar l'espai addicional que comporta una aproximació. No equival al territori ocupat: les concavitats, els forats i les separacions entre parts poden quedar inclosos dins de l'envolupant.

El **caixetí delimitador** ordinari és el rectangle definit pels mínims i màxims de les coordenades X i Y. Els seus costats segueixen els eixos del sistema de referència de coordenades (**CRS**). Un rectangle mínim orientat deixa variar l'orientació per minimitzar-ne l'àrea. El primer facilita treballar amb graelles no rotades; el segon pot ajustar-se millor a una forma obliqua. Cap dels dos necessita seguir la direcció de la costa.

L'**embolcall convex** és la geometria convexa mínima contenidora: uneix els extrems i omple les concavitats. El **cercle mínim contenidor** busca un centre i un radi que continguin l'entrada; no és, en general, un buffer del centroide. Una envolupant còncava respon a una altra família de mètodes i depèn del paràmetre de concavitat. No s'ha de confondre amb aquestes quatre formes.

### Una entrada comuna i quatre tipus

La capa `municipi_treball` conté el terme CNIG de Vila-seca de juliol de 2026, preparat en EPSG:25831. En aquest primer pas l'entrada és **el municipi sense buffer**. El projecte mostra l'Explorador amb els GeoPackage de treball, CartoCiudad i viari CNIG; el WMS IGN/PNOA queda sota els vectors. Els contorns permeten llegir l'ortofoto sense alterar-ne els colors.

![Quatre envolupants del municipi de Vila-seca, amb contorns sobre el WMS i les connexions GeoPackage visibles]({{ site.baseurl }}/assets/img/qgis/qgis-c06-envolupants-comparacio.png "Les quatre formes contenen el mateix terme municipal magenta: caixa alineada verda, rectangle orientat blau, cercle taronja i embolcall convex violeta. Els espais que afegeixen responen a les seves propietats geomètriques, no a una ampliació administrativa."){: data-figure-width-web="64rem" data-figure-width-pdf="100%"}

**Geometria delimitadora mínima** permet escollir el tipus. El seu identificador a Processament és `qgis:minimumboundinggeometry`.

Amb un únic municipi, deixar el camp de grup buit produeix una geometria per al conjunt d'entrada. Si hi ha diverses entitats, el camp opcional permet calcular una envolupant per classe; deixar-lo buit no significa necessàriament calcular-ne una per fila.

Per obtenir caixes per entitat es pot emprar `native:boundingboxes`, visible com **Caixetins delimitadors** {% cite qgisUserGuide344 %}.

![Diàleg de geometria delimitadora mínima amb municipi_treball i selector del tipus destacats]({{ site.baseurl }}/assets/img/qgis/qgis-c06-envolupants-tipus.png "La mateixa eina permet canviar el tipus de geometria delimitadora. La captura mostra seleccionada l'envolupant rectangular i el camp d'agrupació buit; el municipi és l'entrada de totes les comparacions."){: data-figure-width-web="44rem" data-figure-width-pdf="88%"}

::: table "Tipus de geometria delimitadora mínima a QGIS 3.44"
| Tipus | Valor de `TYPE` | Propietat que es comprova |
| --- | ---: | --- |
| Envolupant o caixetí delimitador | 0 | Extrems X/Y i costats alineats amb el CRS |
| Rectangle mínim orientat | 1 | Contenció i mínima àrea rectangular amb orientació lliure |
| Cercle mínim contenidor | 2 | Centre, radi i aproximació poligonal del cercle |
| Embolcall convex | 3 | Contenció i absència de concavitats |
:::

Es conserva cada sortida amb un nom propi i es comproven validesa, extensió, àrea i contenció. En un cercle discretitzat, el radi matemàtic i el polígon de segments no són el mateix objecte: la tolerància ha de correspondre a l'aproximació. La comparació només és interpretable si es manté la mateixa entrada. Més endavant es repetirà sobre un buffer, que ja serà una geometria diferent.

## Distàncies, buffers i regió d'interès

### Distància i model de mesura

La distància mínima entre dues geometries és la longitud del segment més curt que les connecta sota la mètrica adoptada. Dues geometries que s'intersequen tenen distància mínima zero. Mesurar entre centroides respon una altra pregunta: dues formes allargades poden tenir centres llunyans i vores molt pròximes.

En el pla, la distància euclidiana entre dos punts es calcula amb les diferències de coordenades. La distància de Manhattan restringeix el recorregut a direccions ortogonals; una distància sobre una xarxa segueix arcs connectats i pot incorporar sentits, barreres, costos o temps. Per tant, proximitat geomètrica i accessibilitat no són intercanviables.

![Tres models de distància entre el mateix origen i destinació]({{ site.baseurl }}/assets/quarto/06-analisi-geoprocessament-vectorial/distance-models.qmd "La línia recta, el recorregut ortogonal i una ruta sobre xarxa defineixen espais de moviment diferents. Una barrera pot ser irrellevant per a la distància euclidiana i determinant per al trajecte possible."){: data-figure-width-web="56rem" data-figure-width-pdf="100%"}

Una operació plana interpreta les coordenades i les unitats del CRS pertinent. Un valor de 500 només significa 500 metres quan la unitat lineal és el metre; no té aquest significat sobre longituds i latituds en graus. En els casos locals del capítol es preparen explícitament les capes en **EPSG:25831**. Canviar només el CRS del projecte modifica la representació, no les coordenades emmagatzemades de cada font.

Una mesura geodèsica sobre l'el·lipsoide tampoc no és idèntica a una mesura plana. El procediment s'escull segons extensió, deformació admissible i pregunta. A QGIS convé distingir les funcions de mesura configurades amb l'el·lipsoide del projecte de les operacions geomètriques planes de Processament. La coincidència visual amb el WMS complementa aquests controls; no certifica l'exactitud posicional.

### Quines parelles es comparen?

Un càlcul de distàncies pot retornar un camp, una taula de parelles, arestes o una superfície. Primer cal decidir quins orígens i destinacions participen, si la distància és direccional i com es tracten empats o absències.

::: table "Patrons de comparació de distàncies"
| Patró | Resultat | Control determinant |
| --- | --- | --- |
| Origen únic o estrella | Una distància de l'origen a cada destinació | Identitat de l'origen i cobertura de destinacions |
| Veí més pròxim | Una o diverses candidates mínimes per entitat | Empats, ID de la candidata i distància |
| Dos conjunts | Fins a $n\times m$ parelles | Volum de la taula i significat de cada parella |
| Totes les parelles no dirigides | $n(n-1)/2$ parelles sense autoparelles | No duplicar A–B i B–A |
| Graf de veïnatge | Només les arestes definides pel criteri | Distingir el criteri de veïnatge de totes les parelles |
| Buffer | Zona situada dins del llindar geomètric | CRS, radi, aproximació i identitat dels generadors |
:::

Un índex espacial pot descartar moltes candidates sense calcular totes les distàncies. Aquesta acceleració no canvia la pregunta: la comprovació final es fa sobre geometries, no només sobre caixes. Les arestes de Delaunay, que es desenvoluparan amb Reus, són una manera concreta de proposar parelles veïnes; no constitueixen la matriu exhaustiva. El capítol ràster presentarà una altra representació: un valor de distància per cel·la.

### Àrea d'influència i aproximació de corbes

Un **buffer** o àrea d'influència amb extrems i unions arrodonits aproxima el conjunt de posicions situades a una distància màxima de la geometria. Al voltant d'un punt forma un disc aproximat; al voltant d'una línia, una franja; al voltant d'un polígon, una expansió. El radi es mesura des de la geometria d'entrada, no des del gruix del símbol dibuixat.

El paràmetre **segments** de `native:buffer` indica quants segments s'utilitzen per aproximar un quart de circumferència. Més segments afegeixen vèrtexs i redueixen la desviació geomètrica de l'arc, però no milloren la cartografia original. En arcs parcials, la subdivisió del motor pot diferir de la d'una circumferència regular; qualsevol control de precisió ha de correspondre al cas executat.

En línies obertes, un extrem pla acaba a la coordenada final; un de quadrat prolonga la franja i pot incloure posicions diagonals més llunyanes que el radi nominal; un d'arrodonit aproxima el semicercle de proximitat. Les unions arrodonides, bisellades o en punta també canvien la superfície a les cantonades. El límit de mitra restringeix les prolongacions en punta. Si la pregunta és literalment distància màxima, no es poden tractar tots aquests estils com a equivalents.

![Efectes del radi, els segments, els extrems i les unions]({{ site.baseurl }}/assets/quarto/06-analisi-geoprocessament-vectorial/buffer-parameters.qmd "Els paràmetres del buffer alteren la geometria resultant. Cal mantenir-los constants en una comparació de radi, o variar-ne un de sol per atribuir-li el canvi observat."){: data-figure-width-web="50.5rem" data-figure-width-pdf="100%"}

Un buffer d'un sol costat depèn de l'ordre dels vèrtexs de la línia: invertir-ne el sentit intercanvia esquerra i dreta. Una distància procedent d'un camp exigeix revisar unitats, nuls i signes. En polígons, una distància negativa produeix retracció i pot eliminar parts estretes, dividir una geometria o deixar-la buida. Aquests canvis s'han de comptar, no descartar silenciosament.

### Cobertura conjunta o generadors individuals

Els buffers individuals conserven la identitat dels generadors, però poden superposar-se. Sumar-ne les àrees compta les coincidències diverses vegades. Una còpia dissolta elimina les fronteres interiors i permet mesurar la petjada conjunta; deixa de descriure directament quin generador cobreix cada posició.

![Buffers individuals i cobertura dissolta dels mateixos generadors]({{ site.baseurl }}/assets/quarto/06-analisi-geoprocessament-vectorial/buffer-dissolve.qmd "La dissolució permet mesurar cobertura única. La capa individual continua essent necessària per atribuir cada zona als seus generadors i estudiar coincidències múltiples."){: data-figure-width-web="45rem" data-figure-width-pdf="100%"}

Per seleccionar portals pròxims a una xarxa es pot utilitzar un predicat de distància o un buffer adequadament aproximat. La selecció retorna un conjunt d'IDs: un portal no es duplica només perquè intersequi diversos buffers. En canvi, una taula que relacioni cada portal amb tots els trams pròxims sí que pot contenir diverses files per portal. La dissolució i el recompte s'escullen segons aquesta diferència.

### Buffer municipal de 500 m

El cas de continuïtat necessita un marge al voltant de Vila-seca. S'aplica `native:buffer` a `municipi_treball`, amb distància **500 m**, **8 segments per quadrant**, unions arrodonides, límit de mitra 2 i dissolució desactivada. La sortida es desa com `municipi_buffer_500m` al GeoPackage de treball. El valor és una decisió d'àmbit del cas, no una franja normativa.

![Diàleg natiu de buffer municipal amb distància i segments destacats]({{ site.baseurl }}/assets/img/qgis/qgis-c06-buffer-municipal.png "Els 500 m s'interpreten sobre la capa municipal en EPSG:25831; els 8 segments fixen l'aproximació per quadrant. La captura acredita la configuració. La validesa, la contenció i la distància es comproven sobre la sortida persistent."){: data-figure-width-web="44rem" data-figure-width-pdf="88%"}

Després d'executar, es reobre la capa i es comprova que conté el municipi, que les geometries són vàlides i que l'àrea ha augmentat. En aquesta edició CNIG, el terme ocupa **21,704 km²** i el buffer **40,286 km²**. El control mostrejat de distància observa aproximadament 495,183–500 m a la frontera exterior, coherent amb la discretització estudiada; no és una mesura d'exactitud de la font ni un certificat continu de tot el contorn.

### La caixa ROI del buffer {#cas-guiat-una-roi-comuna-per-al-geoprocessament}

La **regió d'interès (`roi`)** del recorregut és la caixa no orientada de `municipi_buffer_500m`. S'aplica `native:boundingboxes` al buffer, no directament al terme, i es desa la capa `roi` al mateix GeoPackage. S'hi incorpora `id_roi` per identificar l'àmbit en les superposicions posteriors. En el cas resolt el valor és `roi_vilaseca_500m`.

![Caixetins delimitadors amb el buffer municipal com a entrada i la destinació GeoPackage]({{ site.baseurl }}/assets/img/qgis/qgis-c06-caixa-roi.png "La destinació persistent identifica el fitxer i la capa roi. La caixa es calcula sobre el buffer municipal; no és la mateixa envolupant que s'ha comparat al començament sobre el terme original."){: data-figure-width-web="44rem" data-figure-width-pdf="88%"}

La caixa ocupa **87,609 km²** i segueix els eixos d'EPSG:25831. Les cantonades poden quedar a més de 500 m del terme: la condició de distància defineix el buffer, mentre que la caixa només el conté. Aquesta geometria facilita una graella ràster no rotada, però incorpora mar i municipis veïns. L'ajust a l'origen i mida de píxel a PR5 serà una operació posterior.

![Municipi, buffer i ROI sobre el WMS IGN PNOA amb les connexions de treball]({{ site.baseurl }}/assets/img/qgis/qgis-c06-roi-desada.png "Municipi magenta, buffer blau i ROI verda són tres geometries diferents. L'Explorador identifica el contenidor de treball i els originals; el WMS proporciona context territorial, sense intervenir com a geometria del càlcul."){: data-figure-width-web="64rem" data-figure-width-pdf="100%"}

El rectangle orientat, la convexa i el cercle mínim del **mateix buffer** ocupen, respectivament, 70,773, 54,713 i 95,193 km²; el cercle d'aquesta comparació s'ha discretitzat amb 720 segments. Aquests valors no corresponen a les envolupants municipals de la primera figura. Una alternativa més compacta pot reduir espai de càlcul, però no substitueix automàticament la caixa acordada per a la continuïtat.

### Distàncies normatives i cribratge territorial

Un buffer pot ajudar a localitzar casos que necessiten revisió, però el seu significat jurídic depèn de la norma i de la geometria des d'on aquesta mesura. No és equivalent mesurar des d'un eix viari, de la vora de la calçada o de l'aresta d'una esplanació.

::: table "Preguntes de cribratge i geometria de referència"
| Context | Comprovació necessària |
| --- | --- |
| Espai natural protegit | Perímetre oficial, zonificació i règim del pla aplicable |
| Costes | Delimitament jurídic i tipus de zona previstos a la [Llei de costes](https://www.boe.es/eli/es/l/1988/07/28/22/con), no només costa visible al WMS |
| Aigües | Llera, geometria oficial i règim establert a la [legislació d'aigües](https://www.boe.es/eli/es/rdlg/2001/07/20/1/con) |
| Carreteres | Titularitat, classe, zona i aresta des de la qual es mesura |
| Instal·lació o pla de protecció civil | Norma, pla o resolució específica; no una distància universal presumpta |
:::

El [text refós de la Llei de carreteres de Catalunya](https://portaljuridic.gencat.cat/eli/es-ct/dlg/2009/08/25/2/con) diferencia zones i referències de mesura. Els 25 m apareixen en determinats supòsits, però no defineixen una franja universal per a qualsevol autopista; les vies estatals requereixen consultar la [Llei 37/2015](https://www.boe.es/eli/es/l/2015/09/29/37/con). Els eixos CNIG poden servir per al cribratge a la seva escala, sense substituir les geometries exigides per un expedient.

## Preparació i selecció espacial

### Fonts completes per a l'àmbit ampliat

La ROI supera el terme municipal. Els portals i les vies seleccionats només per Vila-seca a PR3 no cobreixen necessàriament el nou àmbit. Es reprenen les fonts provincials: CartoCiudad Tarragona d'abril de 2026, amb `portalpk_publi` i `manzana`, i viari CNIG de juliol de 2026, amb `rt_tramo_vial`. Els originals es mantenen separats dels candidats i resultats.

En continuar la cadena de pràctiques, amb QGIS tancat es copia el GeoPackage validat de PR3 a `sandbox/pr4-geoprocessament-cognom.gpkg`. No es copia el `.qgz` anterior. S'estableix el projecte principal `pr4`, es reorienten totes les fonts locals al contenidor nou i després es crea un `.qgz` homònim amb camins relatius. Les connexions de l'Explorador pertanyen al perfil de QGIS i poden haver-se de recrear en un altre equip.

Abans de transformar es conserva una clau ordinària de fila, `id_font`, i s'extreuen candidats d'un sector que cobreixi tota la ROI, encara amb geometries senceres. Un índex o una selecció per extensió proporciona candidats, però després cal el predicat exacte. Els FID interns poden canviar en exportar o fragmentar; `id_tramo` també pot repetir-se en registres diferents del viari i no equival a una clau de fila.

>> **Processar sense dibuixar tota la font.** Una capa desmarcada al panell Capes continua disponible per a Processament. Sovint no cal representar la província ni obrir-ne la taula per retallar-la. Un filtre de capa pot restringir també l'entrada de molts algorismes; no és equivalent a ocultar-la, filtrar només la taula o mantenir una selecció. Cal registrar el filtre i comprovar el recompte. La millora de temps depèn de la font, els índexs i la consulta.

![Menú contextual del viari amb Filtre ressaltat]({{ site.baseurl }}/assets/img/qgis/qgis-c06-filtre-capa.png "El filtre es configura sobre la capa. Pot continuar actiu encara que la capa sigui invisible al mapa, i per això cal revisar-lo abans de qualsevol càlcul."){: data-figure-width-web="64rem" data-figure-width-pdf="100%"}

CartoCiudad reuneix portals i punts quilomètrics. La consulta `"tipo" = 'Portal'` delimita el subconjunt de portals; el nom del fitxer no ho garanteix. En el viari, el valor observat de `clased` per als carrers urbans és `Urbano`. El retall general conserva totes les classes i el subconjunt urbà es materialitza quan la pregunta el necessita.

### Predicats i geometries senceres

Quines vies intersequen la ROI? **Selecciona per ubicació** avalua una relació entre la capa objectiu i la referència. Amb el predicat `intersects`, una via que comparteix qualsevol punt amb `roi` queda seleccionada **sencera**, encara que la major part sigui fora. Exportar només les seleccionades materialitza aquesta selecció; encara no calcula el tros interior.

![Selecció per ubicació amb els candidats viaris i la ROI]({{ site.baseurl }}/assets/img/qgis/qgis-c06-seleccio-roi.png "La capa objectiu determina quines entitats es seleccionen. La ROI participa en el predicat, però no retalla la geometria de les vies seleccionades."){: data-figure-width-web="44rem" data-figure-width-pdf="88%"}

La **topologia d'edició** ajuda a mantenir límits o nodes compartits; un **predicat** avalua una relació i retorna un valor lògic; una operació de **geoprocessament** pot crear geometries noves. Superar una regla d'edició no substitueix el predicat que exigeix l'anàlisi, i seleccionar correctament no construeix la superfície que només una superposició pot obtenir {% cite ogcSimpleFeatures2011 %}.

::: table "Predicats habituals i interpretació"
| Predicat | Relació | Precaució |
| --- | --- | --- |
| `intersects` | Almenys un punt comú | Inclou contacte, creuament, contenció i solapament |
| `disjoint` | Cap punt comú | Una escletxa petita continua essent separació |
| `touches` | Contacte sense intersecció dels interiors | No equival a compartir superfície |
| `within` / `contains` | Contenció, amb la relació d'interiors exigida | Són inversos; un punt només sobre la frontera no és estrictament interior |
| `overlaps` | Solapament parcial entre geometries de la mateixa dimensió | Exclou igualtat i contenció completa |
| `crosses` | Creuament amb la dimensió d'intersecció adequada | El significat depèn dels tipus geomètrics |
| `equals` | Igualtat topològica dels conjunts de punts | No exigeix els mateixos IDs, atributs ni ordre de vèrtexs |
:::

![Predicats entre punts, línies i polígons ideals]({{ site.baseurl }}/assets/quarto/06-analisi-geoprocessament-vectorial/spatial-predicates-by-geometry.qmd "La dimensió geomètrica condiciona la relació: tocar una frontera, creuar una línia i compartir superfície no són situacions equivalents."){: data-figure-width-web="56rem" data-figure-width-pdf="100%"}

### Interior, frontera i DE-9IM

L'interior d'un polígon exclou els anells; la frontera inclou tant el contorn exterior com els anells dels forats. Un punt dins d'un forat és exterior al polígon, i un punt sobre l'anell interior és a la frontera. En una línia oberta simple, els extrems formen la frontera; la resta del recorregut és interior. Una línia tancada simple té frontera buida segons la regla topològica corresponent i no es converteix en polígon pel fet de tancar-se. El punt té interior, però frontera buida.

El model **DE-9IM** compara interior, frontera i exterior d'A amb els mateixos conjunts de B. Cada intersecció és buida o té una dimensió màxima: punt, línia o superfície. Aquesta formulació permet expressar els predicats sense deduir-los del gruix dels símbols {% cite egenhoferPointSetTopological1991 clementiniFormalTopological1993 ogcSimpleFeatures2011 %}.

::: table "Les nou interseccions de DE-9IM"
| A respecte de B | Interior de B | Frontera de B | Exterior de B |
| --- | --- | --- | --- |
| Interior d'A | $I(A)\cap I(B)$ | $I(A)\cap\partial B$ | $I(A)\cap E(B)$ |
| Frontera d'A | $\partial A\cap I(B)$ | $\partial A\cap\partial B$ | $\partial A\cap E(B)$ |
| Exterior d'A | $E(A)\cap I(B)$ | $E(A)\cap\partial B$ | $E(A)\cap E(B)$ |
:::

La codificació utilitza `F` per a una intersecció buida i `0`, `1` o `2` per a la dimensió; en un patró, `T` admet qualsevol intersecció no buida i `*` no imposa condició. No cal memoritzar tots els patrons, però sí distingir-los de la distància: dos polígons amb una escletxa continuen sent `disjoint`, per petita que sigui. Els predicats `covers` i `covered_by`, quan l'eina els ofereix, permeten tractar explícitament la cobertura de la frontera.

Una prova ideal amb WKT fa aquesta distinció reproduïble. WKT és text de geometria, no una capa completa ni un CRS; WKB n'és una representació binària.

::: listing "Interior, frontera i exterior en un exemple cartesià"
```text
POLYGON ((0 0, 2 0, 2 2, 0 2, 0 0))
POINT (1 1)
POINT (0 1)
POINT (3 1)
```
:::

El primer punt és interior, el segon toca la frontera i el tercer és exterior. Els dos primers intersequen el polígon, però només el primer és `within`. Les coordenades són didàctiques, sense unitat territorial. Amb dades reals, precisió finita, geometries invàlides o límits de fonts diferents poden alterar les relacions i requereixen diagnòstic.

## Superposicions i atributs

Seleccionar, unir atributs i tallar geometries responen preguntes diferents. Una **unió espacial d'atributs** conserva habitualment la geometria objectiu i hi associa informació de les coincidències. Un **retall** construeix la part interior a una màscara. Una **intersecció** construeix parts comunes i relaciona les files que les han generades.

![Selecció, retall i intersecció sobre les mateixes geometries]({{ site.baseurl }}/assets/quarto/06-analisi-geoprocessament-vectorial/selection-overlay.qmd "La selecció conserva l'entitat completa. Retall i intersecció en construeixen la part comuna, però propaguen atributs diferents."){: data-figure-width-web="43.5rem" data-figure-width-pdf="100%"}

Les eines habituals es troben a `Vectorial > Eines de geoprocessament` i a la caixa de Processament. Les captures corresponen a QGIS 3.44.11, amb algunes etiquetes encara en anglès. L'identificador de cada algorisme permet reconèixer-lo encara que la traducció variï.

![Accés a les operacions de geoprocessament vectorial]({{ site.baseurl }}/assets/img/qgis/qgis-c06-menu-geoprocessament.png "El menú dona accés a les operacions de superposició. L'elecció depèn de la geometria i la taula que ha de produir la resposta, no de la proximitat dels botons."){: data-figure-width-web="64rem" data-figure-width-pdf="100%"}

### Retall de portals i viari

El **retall**, `native:clip`, utilitza `roi` com a màscara i conserva els atributs de l'entrada. En punts, cada posició es conserva o s'exclou; no es genera mig portal. En línies, el tall crea extrems nous i pot produir diverses parts d'un mateix registre. El recorregut desa `portals_roi`, després del filtre Portal, i `viari_roi`, amb totes les classes viàries.

![Retall de les línies viàries per la ROI]({{ site.baseurl }}/assets/img/qgis/qgis-c06-retall-viari.png "L'entrada és vies_candidats i la màscara és roi. La longitud es recalcula sobre la sortida: un camp antic copiat de l'entrada no mesura els nous fragments."){: data-figure-width-web="44rem" data-figure-width-pdf="88%"}

Cap geometria resultant ha de quedar fora de la màscara i la longitud o superfície no ha d'augmentar respecte de l'original corresponent. `id_font` permet relacionar els fragments amb la seva fila de procedència. El recompte de registres no es confon amb el d'itineraris ni amb el de trams geomètrics diferents.

### Intersecció d'illes i identitat de la màscara

La **intersecció**, `native:intersection`, calcula les parts comunes i hi incorpora camps de les dues entrades. Les illes de `manzana` es preparen com `illes_candidates`, s'intersecten amb `roi` i es desen com `illes_roi`, conservant `id_font` i l'atribut de màscara `id_roi`.

![Intersecció de les illes de CartoCiudad amb el camp id_roi seleccionat]({{ site.baseurl }}/assets/img/qgis/qgis-c06-interseccio-illes.png "La intersecció identifica tant l'illa d'origen com la màscara que participa en el resultat. Els FID de la sortida no substitueixen aquestes claus."){: data-figure-width-web="44rem" data-figure-width-pdf="88%"}

Si una entitat amb un recompte $N$ es divideix en dos fragments, tots dos poden rebre el mateix $N$. Sumar-lo donaria $2N$, no un total desagregat. Repartir-lo proporcionalment a l'àrea exigeix una hipòtesi d'homogeneïtat, que pot ser inadequada. La geometria correcta no garanteix l'ús correcte dels atributs.

::: table "Recomptes del cas CNIG sobre la ROI de Vila-seca"
| Entrada preparada | Files candidates | Sortida | Files resultants |
| --- | ---: | --- | ---: |
| Punts CartoCiudad, encara amb Portal/PK | 17.793 | `portals_roi`, després de filtrar Portal | 16.756 |
| Viari de totes les classes | 10.262 | `viari_roi` | 9.780 |
| Illes completes | 1.490 | `illes_roi` | 1.399 |
:::

Les diferències combinen criteri espacial i, en els portals, filtre de tipus. No són una mesura de pèrdua de qualitat. Els valors corresponen a les edicions i a la preparació declarades; no s'imposen a un altre municipi.

![Punts, línies i polígons limitats per la mateixa ROI]({{ site.baseurl }}/assets/img/qgis/qgis-c06-retalls-resultat.png "Els tres resultats comparteixen àmbit. El límit municipal permet veure que la ROI conserva també l'entorn exterior de Vila-seca."){: data-figure-width-web="64rem" data-figure-width-pdf="100%"}

### Unió geomètrica i dissolució

La **unió geomètrica**, `native:union`, cobreix $A\cup B$ i segmenta les geometries pels límits entre entrades. A les peces exclusives d'A, els camps de B queden nuls, i a la inversa; a la part comuna hi ha atributs de totes dues. Aquest patró de nuls expressa pertinença espacial. La unió no és apilar files de capes compatibles.

![Partició i atributs d'una unió geomètrica]({{ site.baseurl }}/assets/quarto/06-analisi-geoprocessament-vectorial/union-geometry-and-attributes.qmd "Les peces exclusives i comunes conserven camps de procedència. Els nuls de l'altra capa són esperables a les zones on aquella capa no participa."){: data-figure-width-web="45rem" data-figure-width-pdf="100%"}

La sortida només és una partició disjunta si es compleixen les condicions de les entrades i de l'algorisme. Amb dues capes, `native:union` no resol per si sol els solapaments interns de cadascuna. Sense capa de superposició, pot dividir coincidències de la mateixa entrada i conservar peces geomètricament coincidents per als participants. Comptar files no equival, per tant, a comptar zones exclusives.

La **dissolució**, `native:dissolve`, agrupa geometries segons un camp o calcula una geometria conjunta si no se n'indica cap. Elimina fronteres internes, però no defineix sumes, mitjanes ni recomptes dels altres camps. QGIS conserva valors de la primera entitat processada per a camps no agrupadors; no s'interpreten com a estadístiques. Amb `Keep disjoint features separate` poden aparèixer diverses files per grup {% cite qgisUserGuide344 %}.

Quan calen geometria i totals, es calculen separadament la cobertura dissolta i una taula agregada per la mateixa clau, i se'n comprova la unicitat abans d'unir-les. Per estudiar cobertura de fanals, les peces geomètriques úniques es relacionen de nou amb els buffers individuals i es compten IDs diferents. La petjada conjunta, el nombre de generadors i la il·luminació real són magnituds diferents.

## Diferències, components i peces entre carrers

### Complement dins d'un univers finit

La **diferència** $A\setminus B$ conserva la part d'A no coberta per B. És direccional: invertir les entrades canvia la pregunta. La **diferència simètrica** conserva les parts exclusives de totes dues i és útil per localitzar desacords entre cobertures, sense identificar per si sola si es deuen a canvi territorial, escala o desplaçament.

Per obtenir un complement finit cal definir l'univers. En el cas costaner, `roi` és aquest univers i `terra_roi` és la unió dels recintes administratius retallats que hi intervenen: Cambrils, Constantí, Reus, Riudoms, Tarragona, Vila-seca, Salou i la Canonja. Restar només Vila-seca deixaria també els municipis veïns al complement. El nom `terra_roi` és operatiu; no identifica tota la terra física ni exclou qualsevol superfície d'aigua.

![Diferència entre la ROI i la unió dels recintes administratius]({{ site.baseurl }}/assets/img/qgis/qgis-c06-diferencia-mar.png "L'ordre és roi menys terra_roi. El complement s'ha de conservar i inspeccionar abans d'atribuir-li un significat territorial."){: data-figure-width-web="44rem" data-figure-width-pdf="88%"}

La sortida `mar_complement` ocupa **14,826 km²** i conté **cinc components**. S'inspeccionen amb el WMS, especialment als ports i als desajustos de límits. El cas conserva tota la diferència i identifica com `mar_context` els dos components connectats amb punts marins de contrast prop de les cantonades sud-oest i sud-est. Sumen **14,447 km²**. No és una regla universal de conservar el polígon més gran.

![Contorns del context marí derivat sobre el WMS]({{ site.baseurl }}/assets/img/qgis/qgis-c06-mar-resultat.png "Els components seleccionats proporcionen context cartogràfic. No substitueixen una delimitació marina oficial ni una línia de costa específica; les altres parts del complement continuen disponibles per al diagnòstic."){: data-figure-width-web="64rem" data-figure-width-pdf="100%"}

El balanç compara l'àrea de `terra_roi` amb la del complement: han de reconstruir l'àrea de `roi`, dins de la tolerància declarada, sense superposició d'interiors. Una igualtat d'àrea no basta per etiquetar el complement com a mar; el control geomètric i la interpretació territorial són passos diferents.

### Franges viàries i conversió multipart

La segona diferència pregunta què queda entre franges uniformes al voltant dels carrers. De `viari_roi` s'extreu `"clased" = 'Urbano'`, amb **5.475 registres**, i es desa `urbans_roi`. Es comparen buffers dissolts de **5 i 10 m**, amb 8 segments per quadrant i extrems i unions arrodonits. Un radi de 5 m dona aproximadament 10 m d'amplada total en un tram recte; no mesura l'amplada real del carrer.

![Buffer de cinc metres sobre els carrers urbans amb dissolució]({{ site.baseurl }}/assets/img/qgis/qgis-c06-buffer-carrers.png "La dissolució obté una petjada conjunta dels carrers. Els radis de 5 i 10 m són dues hipòtesis comparables del model, amb la mateixa entrada i els mateixos paràmetres de corba."){: data-figure-width-web="44rem" data-figure-width-pdf="88%"}

Es resta cada petjada de `terra_roi`. Una sola fila pot contenir moltes peces separades: una geometria **multipart**. En WKT, `MULTIPOLYGON` agrupa diversos polígons sota una geometria; no implica una fila per polígon.

L'algorisme `native:multiparttosingleparts`, visible com **Compost a parts senzilles**, crea una fila per part i repeteix els atributs d'origen.

![Separació d'una geometria multipart en parts senzilles]({{ site.baseurl }}/assets/img/qgis/qgis-c06-multipart-monopart.png "La conversió canvia el nombre de files, no la cobertura. Després es conserva la clau d'origen, s'assigna id_peca i es recalcula l'àrea de cada part."){: data-figure-width-web="44rem" data-figure-width-pdf="88%"}

Amb 5 m s'obtenen **1.330 parts** i amb 10 m, **1.131**. La suma d'àrees de les parts ha de coincidir amb la diferència anterior. Les peces poden incloure espais rurals, rotondes, discontinuïtats viàries i fragments del límit: no són un inventari oficial d'illes urbanes. El contrast amb `manzana` i l'ortofoto permet explicar aquestes diferències.

![Peces delimitades pels buffers viaris al nucli de Vila-seca]({{ site.baseurl }}/assets/img/qgis/qgis-c06-illes-resultat.png "Els eixos blaus i els contorns de les peces permeten llegir el model sobre el teixit urbà. Una franja uniforme simplifica amplades, places, cruïlles i culs-de-sac."){: data-figure-width-web="64rem" data-figure-width-pdf="100%"}

### Combinació de criteris territorials

Les operacions anteriors permeten expressar una decisió multicriteri. Si U és l'àmbit, C una coberta compatible, P una proximitat i E una exclusió, una zona candidata pot ser $(U\cap C\cap P)\setminus E$. Cal conservar cada criteri amb un nom interpretable i comprovar-lo abans de combinar-lo. Canviar una intersecció per una unió o invertir una diferència canvia el significat.

En la branca municipal de PR4, els candidats viaris de PR3 es preparen com `vies_principals`, amb una clau `id_tram` pròpia, única i no nul·la després de fragmentar, `codi_muni` i traça d'origen. Aquesta preparació es distingeix del viari de tota la ROI. Es poden comparar proximitat al viari, a fanals inventariats i a l'entorn de la Facultat, mantenint separats buffers individuals i cobertures dissoltes. Un escenari sintètic s'identifica com a tal.

La sensibilitat repeteix el flux variant una decisió plausible —distància, predicat, tolerància o edició— i mantenint les altres. S'analitzen àrees comunes i exclusives, components i entitats que canvien de classe, no només superfície total. La sortida afirma compatibilitat amb les regles codificades; no demostra disponibilitat jurídica, il·luminació, accessibilitat ni cap factor omès.

## Punts derivats de línies i polígons

### Centroide i punt sobre la superfície

Un **centroide** resumeix tota la geometria. En polígons es pondera per superfície i en línies per longitud. Pot quedar fora d'un polígon còncau o multipart, i el centroide d'una línia corbada pot quedar fora del traçat: no és necessàriament el punt de mitja longitud.

`native:centroids` permet obtenir un punt per entitat o per part. En les **1.399 illes** retallades del cas, amb un punt per entitat, **35 centroides queden fora** del polígon corresponent. No s'han de moure per fer-los semblar interiors: és una propietat del mètode que cal interpretar.

![Centroide de cada entitat poligonal a QGIS]({{ site.baseurl }}/assets/img/qgis/qgis-c06-centroides.png "La comparació manté un punt per entitat. Activar el càlcul per part canviaria la unitat del resultat en geometries multipart."){: data-figure-width-web="44rem" data-figure-width-pdf="88%"}

Quan la posició ha de pertànyer a la superfície, es fa servir **Punt sobre la superfície**, `native:pointonsurface`. Els 1.399 punts del cas s'han contrastat amb la seva illa d'origen. La pertinença els pot fer adequats per a una etiqueta o per consultar la peça, però no els converteix en portals, accessos ni centres funcionals.

### Vèrtexs i extrems

**Extreu vèrtexs**, `native:extractvertices`, conserva coordenades de la geometria amb índexs de vèrtex, part i anell quan correspongui. El cas genera **137.919 registres** per a les illes i **92.789** per als carrers urbans. Els anells tancats i les coincidències entre entitats poden repetir coordenades; el recompte no és el de posicions diferents ni un mostreig regular per distància.

![Extracció de vèrtexs de les illes de CartoCiudad]({{ site.baseurl }}/assets/img/qgis/qgis-c06-vertices.png "La capa puntual conserva la relació amb l'entitat i els índexs geomètrics. Aquesta informació permet distingir anells, parts i coincidències."){: data-figure-width-web="44rem" data-figure-width-pdf="88%"}

`native:extractspecificvertices` accepta `0,-1` per al primer i l'últim vèrtex d'una entitat lineal. Per obtenir els extrems de **cada part**, primer es converteix la geometria multipart a parts senzilles. En una línia tancada, els dos índexs poden donar la mateixa coordenada. Aquests punts no són automàticament nodes topològics d'una xarxa.

![Comparació dels punts derivats sobre les mateixes illes]({{ site.baseurl }}/assets/img/qgis/qgis-c06-punts-resultat.png "Triangles vermells: centroides; diamants verds: punts sobre superfície; punts blaus: vèrtexs. Les posicions responen a preguntes diferents i conserven la traça fins al polígon d'origen."){: data-figure-width-web="64rem" data-figure-width-pdf="100%"}

## Tessel·lacions regulars i unitat d'anàlisi

Una **tessel·lació** divideix un domini en cel·les sense buits ni superposició d'interiors. Una malla regular defineix les unitats abans d'agregar-hi observacions. Serveix per comparar recomptes sobre superfícies comunes, però mida, forma, origen i orientació condicionen quins punts queden junts {% cite longleyGeographicInformationScience2015 %}.

Els quadrats s'alineen fàcilment amb eixos cartesians i ràsters; els veïns laterals i diagonals tenen distàncies diferents entre centres. Els hexàgons regulars tenen sis veïns laterals equidistants. Aquesta propietat no els fa universalment superiors: la tria també depèn de les dades amb què s'ha de comparar i de la jerarquia espacial que es necessita.

### Portals de Reus: registres i ubicacions

El nou cas utilitza CartoCiudad Tarragona 04/2026 i el terme CNIG de Reus en EPSG:25831. El municipi té el valor `34094343123` al camp `NATCODE`. El domini és el rectangle municipal ampliat almenys **1.500 m** i arrodonit exteriorment a múltiples de **1.000 m**. És un marge rectangular, no un buffer euclidià. S'hi conserven tots els punts de tipus Portal, inclosos els de municipis veïns.

Hi ha **35.190 registres de portals** i **34.614 ubicacions diferents** després de la preparació. Cada ubicació rep `id_generador`, `cod_postal` textual i `n_portals`; una taula de correspondència manté les files originals. Diverses adreces coincidents no es desplacen artificialment per crear dominis geomètrics diferents. Els codis absents o incompatibles requereixen categories i regles explícites.

Aquest conjunt complet alimenta les malles, Delaunay i Voronoi del recorregut. Una partició d'entrenament/validació és un experiment diferent: els seus recomptes no es barregen amb els del model que utilitza tots els generadors.

### Construcció i recompte per cel·la

**Crea una quadrícula**, `native:creategrid`, permet escollir el tipus, l'extensió, els espaiaments i el CRS. Per als quadrats de 500 m se seleccionen rectangles poligonals, espaiaments horitzontal i vertical de 500 m i solapament zero. Es manté el mateix origen per repetir el càlcul a 1.000 m; així es poden comparar dues mides de suport.

![Paràmetres de la quadrícula de cinc-cents metres]({{ site.baseurl }}/assets/img/qgis/qgis-c06-graella-parametres.png "El domini, el CRS i els dos espaiaments defineixen la malla. Per obtenir quadrats, els costats són iguals; el solapament és zero."){: data-figure-width-web="44rem" data-figure-width-pdf="88%"}

Cada cel·la conserva `id_cella`, fila i columna. S'hi compten per separat **ubicacions** i **registres de portals**: comptar generadors i sumar `n_portals` no dona la mateixa magnitud. Les cel·les sense punts també es conserven. La suma sobre el domini complet ha de recuperar 34.614 ubicacions i 35.190 portals.

![Quadrícula regular de 500 metres sobre Reus]({{ site.baseurl }}/assets/img/qgis/qgis-c06-graella-resultat.png "La malla continua més enllà del límit magenta de Reus. Les cel·les s'han definit sobre el domini complet, abans d'escollir un àmbit d'informe o una cobertura de pàgines."){: data-figure-width-web="64rem" data-figure-width-pdf="100%"}

Els punts sobre fronteres poden intersectar dues o més cel·les. Per evitar doble recompte cal una assignació unívoca. El cas calculat utilitza índexs de fila/columna i intervals semioberts, incloent el límit exterior final a l'última cel·la. En una unió espacial de QGIS s'han de detectar les coincidències múltiples i aplicar una regla equivalent, no sumar-les com si fossin observacions noves.

### Mida, origen i efectes de vora

El **problema de la unitat espacial modificable** (**MAUP**) descriu els canvis dels resums quan varien la mida o la delimitació de les unitats. L'efecte d'escala apareix en passar, per exemple, de 500 a 1.000 m; l'efecte de zonificació, en desplaçar l'origen mantenint la mida. Les observacions poden ser les mateixes i, tanmateix, canviar els punts agrupats en cada cel·la {% cite longleyGeographicInformationScience2015 nunesDiccionariSIG2012 %}.

Retallar cel·les pel terme crea peces parcials. Un recompte brut sobre una peça petita no és directament comparable amb el d'una cel·la completa. Dividir per l'àrea dona densitat geomètrica; una taxa per població o exposició necessita un denominador diferent. Zero observacions i absència de cobertura de la font també s'han de distingir.

Una comparació amb hexàgons ha de fixar el domini i documentar les dimensions reals produïdes per l'eina. No s'ha de suposar que el mateix nombre escrit als espaiaments genera la mateixa àrea que un quadrat. Per a l'atlas posterior es conservaran quadrats complets: la pàgina necessita un enquadrament regular, no una peça retallada de mida variable.

## Delaunay: triangles, arestes i agrupacions

La **triangulació de Delaunay** connecta punts de manera que l'interior del cercle circumscrit a cada triangle no contingui altres punts del conjunt. Proposa un veïnatge geomètric sense haver de fixar primer un radi. Els duplicats, la col·linearitat i les configuracions cocirculars poden provocar degeneracions o triangulacions equivalents; els triangles perifèrics també reflecteixen l'extensió del conjunt observat.

### Triangular els mateixos generadors

S'executa `native:delaunaytriangulation` sobre `generadors`, amb tolerància zero i conservació de la informació dels vèrtexs. La tolerància no s'utilitza per eliminar coincidències sense diagnòstic: la preparació ja ha separat registres i ubicacions. El cas produeix **69.195 triangles**.

![Diàleg de triangulació de Delaunay amb els generadors únics]({{ site.baseurl }}/assets/img/qgis/qgis-c06-delaunay-parametres.png "La triangulació utilitza les mateixes ubicacions que la resta del recorregut. Els identificadors retornats dels vèrtexs s'han de relacionar amb la capa d'entrada; no s'assumeix que siguin claus estables del nou GeoPackage."){: data-figure-width-web="44rem" data-figure-width-pdf="88%"}

Per analitzar distàncies entre veïns interessen les **arestes**, no només els polígons triangulars. Una ruta a QGIS transforma polígons a línies, explota les línies en segments i elimina geometries duplicades. Una aresta interior apareix a dos triangles; la de la vora exterior pot aparèixer només a un. Cal conservar-ne una sola còpia no dirigida i els IDs dels dos generadors extrems.

Es calcula `distancia_m` sobre cada segment en el CRS mètric. El cas resolt conserva **103.808 parelles úniques**, amb `id_a` i `id_b`. L'ordre dels extrems es normalitza per no comptar A–B i B–A com a parelles diferents. Una comprovació recalcula la longitud a partir de les coordenades dels generadors.

![Arestes de Delaunay en un sector del nord de Reus]({{ site.baseurl }}/assets/img/qgis/qgis-c06-delaunay-arestes.png "Les arestes blaves relacionen ubicacions veïnes sobre el WMS. Les connexions llargues travessen espais poc mostrejats i poden creuar barreres; no són carrers ni trajectes de repartiment."){: data-figure-width-web="64rem" data-figure-width-pdf="100%"}

### Retirar arestes llargues

Un llindar de distància conserva només les arestes que el compleixen. Amb 50 m, l'expressió és `"distancia_m" <= 50`. La capa completa es manté i la selecció es desa com una sortida nova. La comparació cartogràfica utilitza el mateix enquadrament i escala, de manera que el canvi observat correspon al llindar.

Un **component connectat** reuneix punts entre els quals existeix una cadena d'arestes conservades. Els punts sense cap aresta també formen components, d'una sola ubicació. L'efecte de cadena és essencial: dos extrems d'un mateix component poden quedar molt més lluny de 50 m, encara que cadascun dels passos de la cadena compleixi el llindar.

![Arestes de fins a cinquanta metres i components en el mateix sector]({{ site.baseurl }}/assets/img/qgis/qgis-c06-delaunay-llindar.png "S'han retirat les arestes de més de 50 m i es conserven també els punts aïllats. Els colors dels punts indiquen mida del component: gris, una ubicació; blau, 2–9; verd, 10–99; magenta, 100 o més. Dos components diferents poden tenir el mateix color."){: data-figure-width-web="64rem" data-figure-width-pdf="100%"}

::: table "Sensibilitat al llindar sobre els 34.614 generadors"
| Distància màxima | Arestes conservades | Components | Components d'una ubicació |
| --- | ---: | ---: | ---: |
| 25 m | 53.237 | 6.810 | 5.074 |
| 50 m | 78.132 | 3.098 | 2.355 |
| 100 m | 92.649 | 1.323 | 916 |
:::

Augmentar el llindar afegeix arestes i pot unir components; no els ha de dividir. Les agrupacions són exploratòries i depenen de la densitat de portals, de les fonts i del radi. Una frontera administrativa, una autopista o una discontinuïtat de recorregut no interrompen automàticament aquestes connexions euclidianes.

L'algorisme `native:dbscanclustering` permet contrastar els components amb **DBSCAN** a QGIS. Amb distància 50 m, mínim **1 punt** i DBSCAN* desactivat, cada ubicació pot ser nucli i els aïllats es conserven. En aquest cas s'ha comprovat la coincidència amb els components del graf. És una configuració específica; amb un mínim superior intervenen densitat, punts de vora i soroll, i ja no s'ha de presentar com el mateix procediment. Els identificadors numèrics de clúster poden canviar entre execucions: es compara la pertinença, no el número de la classe.

## Voronoi i codis postals de Reus

El **diagrama de Voronoi** assigna cada posició al generador més pròxim segons la mètrica adoptada. Els límits són llocs equidistants. En el cas pla, les cel·les no tenen en compte carrers, barreres, capacitat ni recorreguts. En configuracions no degenerades, dos generadors les cel·les dels quals comparteixen una aresta són veïns de Delaunay: dominis i connexions són dues lectures del mateix conjunt.

### Cel·les de proximitat amb atributs

S'aplica `native:voronoipolygons` a `generadors`. Es fixen tolerància zero i còpia d'atributs. El paràmetre `BUFFER` d'aquesta eina amplia **percentualment** l'extensió de construcció; no és un buffer en metres al voltant dels punts. A la demostració es fixa a 100 i es comprova que els polígons cobreixen el municipi abans de retallar-los.

![Diàleg de Voronoi amb ampliació de l'extensió i còpia d'atributs]({{ site.baseurl }}/assets/img/qgis/qgis-c06-reus-voronoi-parametres.png "Es conserven id_generador i cod_postal. L'ampliació percentual evita confondre l'extensió de construcció amb el marge territorial dels generadors, que s'ha preparat en metres."){: data-figure-width-web="44rem" data-figure-width-pdf="88%"}

Els generadors externs continuen participant en la construcció. Retallar els portals pel terme abans de calcular faria desaparèixer veïns que poden ser més pròxims a posicions interiors. El resultat s'intersecta després amb `municipi_reus` i es desa com `voronoi`, amb **17.318 cel·les retallades** en aquest cas. No totes les ubicacions del domini ampli han de conservar una peça dins del terme.

![Cel·les de Voronoi retallades pel terme al sector de comparació]({{ site.baseurl }}/assets/img/qgis/qgis-c06-reus-voronoi-resultat.png "Els contorns mostren dominis de proximitat dels portals. Les cel·les grans corresponen a generadors dominants sobre espais amplis del conjunt observat; no demostren per si soles demanda ni cobertura funcional."){: data-figure-width-web="64rem" data-figure-width-pdf="100%"}

### Dissoldre per categoria postal

`cod_postal` es conserva com a **text categòric**. No té sentit interpolar una mitjana de codis sobre els triangles. Es manté el Voronoi amb identitat del generador i se'n crea una segona capa dissolta per `cod_postal`, `zones_postals`. Pot haver-hi parts separades o enclavaments per a una mateixa categoria.

El cas complet dona **15 categories** dins de Reus: 43006, 43110, 43120, 43201, 43202, 43203, 43204, 43205, 43206, 43330, 43381, 43392, 43393, 43470 i 43480. Les categories minoritàries o que no comencen per 432 no s'eliminen només perquè resultin inesperades; cal tornar als portals i a la seva procedència.

![Zones postals estimades a partir dels portals de l'entorn de Reus]({{ site.baseurl }}/assets/img/qgis/qgis-c06-reus-codis-postals.png "Els contorns i les etiquetes representen la dissolució de cel·les pel codi del generador. És una zonificació postal estimada per proximitat amb CartoCiudad 04/2026, no una delimitació postal oficial."){: data-figure-width-web="64rem" data-figure-width-pdf="100%"}

La unió de les cel·les i la de les zones dissoltes han de cobrir el mateix terme, sense buits ni solapaments d'àrea no explicats. També cal contrastar IDs i categories, inspeccionar punts prop de fronteres i valorar si ampliar l'entorn modifica les zones. Una cobertura geomètrica correcta no prova que la frontera postal inferida sigui correcta.

### Construcció i validació independent

Que el generador rebi el seu propi codi és una comprovació de consistència, no una estimació independent de capacitat predictiva. Per a un contrast, es reserven abans ubicacions completes o blocs espacials; les adreces coincidents queden al mateix grup per evitar validar una còpia amb una altra. Es reconstrueix el model només amb els punts d'entrenament i es comparen codis reservats, classes rares i localització dels desacords.

Aquest experiment ha de tenir les seves pròpies sortides i recomptes. El mapa principal del capítol utilitza tots els generadors: no se li atribueix un percentatge obtingut amb una partició diferent. Fins i tot un bon resultat sobre adreces reservades no valida les fronteres en espais sense portals. Una delimitació independent, amb llicència i metadades, proporciona un contrast territorial addicional.

## Tessel·les com a cobertura d'un atlas

Un **atlas** repeteix una composició cartogràfica canviant l'entitat de referència. La capa de cobertura determina les pàgines; el mapa del layout determina com s'hi enquadra cada entitat. Una quadrícula pot servir alhora per resumir observacions i per organitzar fulls, però són funcions diferents: la cel·la és una unitat de dades, mentre que la pàgina és una vista amb escala, marges i elements cartogràfics.

### Cobertura completa i ordre de pàgines

Es reprèn `malla_1000m` i s'extreuen els quadrats amb **intersecció d'àrea positiva** amb Reus. Es conserven sencers, sense retallar-los pel terme. Un contacte només puntual o lineal no justifica una pàgina en aquest cas. La capa `cobertura_atlas` conté **82 cel·les**, amb `id_cella`, fila, columna i `pagina`.

![Cobertura d'atlas de Reus amb vuitanta-dues cel·les numerades]({{ site.baseurl }}/assets/img/qgis/qgis-c06-atlas-cobertura.png "Els quadrats d'1 km es conserven complets i s'ordenen de nord a sud i d'oest a est. Les cel·les perifèriques inclouen entorn exterior al terme: la cobertura de pàgines no redefineix el municipi."){: data-figure-width-web="64rem" data-figure-width-pdf="100%"}

`id_cella` identifica la unitat encara que canviï l'ordre; `pagina` controla la seqüència. Es comproven identificadors únics, numeració consecutiva i cobertura de tot el terme. L'ordre no es deriva dels FID ni de l'ordre accidental de lectura del GeoPackage.

### Pràctica guiada al compositor

Des de `Projecte > Dissenys` s'obre el disseny existent o es crea un disseny d'impressió nou. Al cas resolt s'anomena **Atlas de tessel·les de Reus**. La configuració segueix aquests passos:

1. Establir una pàgina A4 vertical de **210 × 297 mm** i inserir un element de mapa quadrat de **200 × 200 mm**, a 5 mm del marge esquerre i 40 mm del superior. El mapa rep l'ID `mapa_atlas`.
2. Al panell **Atlas**, activar-ne la generació i escollir `cobertura_atlas`. Utilitzar `id_cella` com a nom de pàgina i ordenar per `pagina` en sentit ascendent. El nom de fitxer pot derivar de l'expressió `'reus_' || "id_cella"`.
3. A les propietats de l'element de mapa, activar **Controlat per atlas** i escollir **escala fixa 1:5.000**, amb rotació zero i EPSG:25831. Activar l'atlas sense vincular-hi el mapa no fa canviar l'enquadrament.
4. Fixar les capes que ha de mostrar el mapa i comprovar que el canvi de visibilitat al llenç principal no n'alteri accidentalment el contingut. El WMS necessita xarxa; les fonts locals han de continuar resolent-se al projecte.
5. Afegir títol amb el nom de cel·la, numeració amb les variables `@atlas_featurenumber` i `@atlas_totalfeatures`, escala, CRS, nord i fonts. A QGIS, els fragments d'expressió d'una etiqueta s'insereixen entre `[%` i `%]`.

La relació d'escala és comprovable: 200 mm sobre el paper a 1:5.000 representen **1.000 m** sobre el terreny. Per això el marc quadrat coincideix amb la cel·la d'1 km. Un marc amb proporcions diferents, una rotació o un marge automàtic canviarien l'extensió visible. El projecte resolt conserva aquesta configuració i s'han comprovat l'ordre i els enquadraments de les 82 entitats mitjançant la iteració nativa de QGIS.

### Navegació, exportació i control

S'activa la previsualització de l'atlas i es recorren, com a mínim, primera i última pàgina, una d'interior i una de vora. En canviar de pàgina han de variar l'entitat de cobertura, el títol i l'enquadrament, mentre que escala, dimensions i llegenda es mantenen coherents. El full perifèric ha de mostrar el quadrat complet i el contorn municipal dins seu.

L'exportació de l'atlas és diferent de la d'un únic layout. Es pot iniciar des del compositor o amb **Exporta el disseny d'atles com a PDF, fitxer únic**, `native:atlaslayouttopdf`. Si s'hi especifica una capa de cobertura, els paràmetres de filtre i ordenació de l'algorisme substitueixen els corresponents del layout; cal tornar a fixar l'ordre per `pagina` {% cite qgisUserGuide344 %}.

![Diàleg natiu d'exportació de l'atlas a PDF amb disseny i cobertura]({{ site.baseurl }}/assets/img/qgis/qgis-c06-atlas-configuracio.png "La captura mostra la configuració de l'algorisme d'exportació, no un PDF ja produït ni la previsualització del compositor. Es vinculen el disseny, la cobertura i l'ordre de les pàgines."){: data-figure-width-web="44rem" data-figure-width-pdf="88%"}

Després d'exportar s'obre el PDF i es comproven nombre de pàgines, dimensions, ordre, noms, enquadraments, textos i disponibilitat del fons. Per al disseny d'una pàgina i les 82 cel·les, s'espera un PDF de 82 pàgines. Aquesta expectativa s'ha de contrastar amb el fitxer, no donar per complerta perquè el diàleg estigui emplenat. Es conserven també la cobertura i el layout editable al projecte incrustat i a l'extern; desar-ne un no actualitza l'altre.

## Errors geomètrics i controls

### Validesa, dimensió i fragments

Una geometria **invàlida** incompleix les regles del seu tipus, com un anell autointersectat. Una geometria vàlida encara pot ser inadequada per al model: una partició pot solapar-se o una xarxa pot contenir una connexió interrompuda. Un extrem penjant pot ser error o cul-de-sac legítim; un pseudonode pot ser redundant o conservar un canvi d'atribut. Cal interpretar la regla abans de corregir.

`Fix geometries` intenta reparar l'estructura, però pot separar parts o modificar components. S'aplica sobre una còpia després del diagnòstic i es comparen tipus, files, parts, àrea o longitud i localització dels canvis. També es compten geometries nul·les i buides: una fila sense geometria i una geometria que ha quedat sense punts no són el mateix estat.

Una intersecció matemàtica pot tenir dimensió inferior: dos polígons poden compartir només una aresta o un vèrtex. Un algorisme que produeix polígons pot ometre aquests contactes. Una sortida buida d'intersecció poligonal no prova `disjoint`; cal contrastar el predicat i el tipus de sortida. No s'ha d'inventar superfície amb un buffer per ocultar un col·lapse dimensional.

Els fragments estrets, escletxes o *slivers* poden provenir de límits nominalment iguals però geomètricament diferents, o representar entitats reals. Eliminar-los només per àrea pot esborrar corredors o illes legítimes. Ajustar coordenades decideix quina font és referència i necessita una tolerància i una traça de canvis.

### Índexs i invariants

Els índexs espacials organitzen caixes envolupants per reduir candidates. Si dues caixes no se superposen, les geometries tampoc no poden intersectar-se; si se superposen, encara cal el predicat exacte. Crear un índex no corregeix un CRS, una geometria ni un filtre, i no hauria de canviar els resultats exactes de la mateixa operació.

::: table "Controls vinculats a cada transformació"
| Resultat | Comprovació |
| --- | --- |
| Envolupant | Entrada continguda, tipus i agrupació correctes |
| Buffer | Unitats, paràmetres, geometries buides i control de distància adequat a l'aproximació |
| Retall/intersecció | Parts dins de l'àmbit, IDs preservats i mesures recalculades |
| Diferència | Interiors disjunts de l'exclusió; part restant i part comuna reconstrueixen l'entrada |
| Unió/dissolució | Cobertura, coincidències, nuls i absència d'agregats estadístics presumptes |
| Parts i punts | Cobertura conservada, claus noves i relació amb la geometria original |
| Malla | Mida/origen, assignació unívoca i suma de recomptes |
| Delaunay/llindar | Parelles úniques, longituds, components i aïllats |
| Voronoi postal | Cobertura/disjunció, IDs/categories, generadors externs i contrast independent |
| Atlas | Cobertura completa, ordre, escala, enquadrament i fitxer exportat reobert |
:::

Els balanços utilitzen mesures de les geometries resultants i toleràncies numèriques explícites. Una àrea total correcta pot ocultar una atribució errònia; una captura sense avisos pot mostrar un diàleg que encara no s'ha executat. Per això es combinen dades, controls, mapes i reobertura, i es distingeix consistència interna de validació amb fonts independents.

## Activitats

### Comparar envolupants i sensibilitat del buffer

Sobre un municipi, es calculen les quatre envolupants amb la mateixa entrada i es comparen contenció, extensió i espai addicional. Després es construeix un buffer amb distància justificada i se'n deriva la caixa. El diari ha d'explicar per què la caixa del terme i la del buffer no són intercanviables.

Una segona comparació manté entrada i radi mentre varia 4, 8 i 16 segments per quadrant; o manté la segmentació mentre varia el radi. Es conserven els resultats i es compara forma, àrea i nombre de vèrtexs. Cap escenari es presenta com una franja legal sense font i geometria de referència adequades.

### Micropràctica 4: un GeoPackage de geoprocessament

El recorregut parteix de PR3 i conserva la ROI de continuïtat. Moodle concreta els apartats seleccionats; el capítol ofereix comparacions addicionals sense convertir-les totes en obligacions.

::: table "Continuïtat del projecte PR4"
| Component | Resultat observable |
| --- | --- |
| Entrada | Còpia validada de PR3 i originals CNIG per cobrir l'entorn exterior |
| Projecte | Principal `pr4`, fonts locals reorientades i `.qgz` nou, homònim i relatiu |
| Preparació | `vies_principals` amb claus comprovades en la branca municipal; candidats complets en la branca ROI |
| Continuïtat | `municipi_buffer_500m` i caixa no orientada `roi` persistents |
| Anàlisi seleccionada | Comparacions justificades, selecció espacial i transformacions geomètriques amb traça |
| Evidència | Mapa comparatiu, apunts, recomptes, mesures, incidències i límits de la interpretació |
| Reobertura | GeoPackage, projecte incrustat i extern verificats sense dependències locals de PR3 ni de `dist/` |
:::

La base és `pr4-geoprocessament-cognom`: fitxers `.gpkg` i `.qgz`, `-mapa.pdf` i `-apunts.pdf`. Amb QGIS tancat es prepara la còpia de distribució i es prova des d'una ubicació neta. El mapa i les captures no substitueixen les capes ni la composició editable.

### Reus i transferència al municipi propi

Sobre un mateix conjunt de portals amb entorn es construeixen una malla, Delaunay i Voronoi. La malla respon quants registres o ubicacions hi ha a cada unitat; les arestes descriuen veïnatges; les cel·les assignen proximitat. Cal conservar les correspondències i comparar almenys una decisió seleccionada: mida/origen, llindar d'arestes o extensió dels generadors.

La zonificació postal es dissol per categoria textual i es presenta com a estimació. Un contrast amb punts reservats és un experiment separat amb partició prèvia. Els resultats propis s'incorporen a PR4; Reus continua identificat com a cas de demostració i no crea una setena instantània.

### Atlas de cobertura regular

Es transfereix el procediment de cobertura al municipi escollit: malla completa, selecció de cel·les amb àrea comuna, IDs, ordre de pàgines, layout i mapa controlat per atlas. Cal justificar conjuntament costat de cel·la, dimensions del marc i escala; una variant pot comparar dues mides mantenint el format de paper.

Les evidències són la cobertura desada, el layout editable, una previsualització interior i una de vora, el PDF exportat reobert i el recompte de pàgines. Els apunts expliquen qualsevol diferència entre extensió de cel·la i extensió visible. L'encaix de Reus i de l'atlas en el treball seleccionat es concreta a Moodle, amb els blocs habituals **70% bàsic, 20% ampliacions i 10% documentació** i sense doble recompte.
