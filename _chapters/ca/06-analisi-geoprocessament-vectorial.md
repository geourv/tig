---
layout: manual-chapter
title: Anàlisi i geoprocessament vectorial
description: Relacions espacials, àrees d'influència, superposicions i tessel·lacions per construir i validar resultats vectorials.
lang: ca
ref: manual-vector-analysis-geoprocessing
profiles: [unaltremanual]
content_status: draft
permalink: /ca/chapters/analisi-geoprocessament-vectorial/
weight: 70
part: Continguts
manual_references: true
---

Una consulta identifica entitats que compleixen una condició; el geoprocessament pot crear geometries noves a partir d'aquestes entitats. Delimitar una franja al voltant d'una carretera, retallar una capa pel terme municipal o calcular la part comuna de dues zones transforma tant l'espai com la taula associada. El resultat només és interpretable si es coneix què conserva i què modifica cada operació.

L'anàlisi vectorial treballa amb relacions de distància, contenció, contacte i superposició. Aquestes relacions no són només eines de QGIS: expressen un model del problema. Un `buffer` representa una distància geomètrica; una intersecció representa coincidència entre geometries; cap de les dues operacions incorpora per si sola accessibilitat, risc o causalitat.

>>>>> En acabar el capítol, cal poder construir i validar una seqüència de geoprocessament vectorial adequada per a una pregunta territorial.
>>>>>
>>>>> - Distingir selecció espacial, unió d'atributs, retall i superposició geomètrica.
>>>>> - Triar entre àrea d'influència, intersecció, diferència, unió i dissolució segons el resultat esperat.
>>>>> - Interpretar com una operació fragmenta geometries i replica o agrega atributs.
>>>>> - Comprovar CRS, validesa, recomptes, superfícies i múltiples coincidències.

## Predicats i transformacions

Els predicats topològics descriuen relacions com `intersects`, `disjoint`, `touches`, `within`, `contains`, `overlaps`, `crosses` i `equals`. Alguns són direccionals: si un punt és `within` d'un polígon, el polígon el `contains`. Una selecció per `intersects` conserva la geometria completa de l'entitat seleccionada, encara que només una petita part coincideixi amb la zona de consulta {% cite ogcSimpleFeatures2011 %}.

La **topologia d'edició**, els **predicats topològics** i el **geoprocessament** no són sinònims. L'edició topològica ajuda a mantenir límits o nodes compartits mentre es modifiquen dades. Un predicat avalua una relació entre dues geometries i retorna un valor lògic. El geoprocessament construeix una geometria nova, com la part comuna o la diferència. Una capa pot superar una regla d'edició i, tanmateix, no complir el predicat que exigeix l'anàlisi; una selecció correcta tampoc no crea la superfície que només una superposició pot obtenir.

### Interior, frontera i exterior

El model topològic parteix de tres conjunts per a cada geometria. L'**interior** conté els punts que pertanyen a l'objecte sense formar-ne la frontera. La **frontera** separa l'interior de l'exterior segons la dimensió i el tipus geomètric. L'**exterior** és la resta de l'espai que no pertany ni a l'interior ni a la frontera. Aquestes definicions permeten descriure una relació sense dependre de la mida, l'orientació o la forma visual dels símbols.

::: table "Interior i frontera segons la dimensió geomètrica"
| Geometria simple | Interior | Frontera | Conseqüència analítica |
| --- | --- | --- | --- |
| Punt | El mateix punt | Conjunt buit | Un punt no té una vora lineal amagada sota el marcador |
| Línia oberta | Els punts de la línia excepte els extrems | Els dos extrems, en el cas simple | Un contacte en un extrem pot ser `touches`; un tall interior pot ser `crosses` |
| Línia tancada simple | El recorregut lineal | Frontera buida segons la regla topològica de la corba tancada | Tancar visualment una línia no la converteix en polígon |
| Polígon | La superfície situada dins dels anells | Anell exterior i anells dels forats | Un punt sobre l'anell no és a l'interior, tot i que interseca el polígon |
:::

La frontera no és el traç que es veu a la pantalla. El gruix d'una línia o del contorn d'un polígon és simbologia i no participa en el predicat. Un punt que sembla quedar «sobre» un límit a una escala concreta pot estar a un costat quan s'examinen les coordenades. Per això els casos de frontera s'han de comprovar amb la geometria, l'exactitud de la font i l'escala del problema, no només ampliant el mapa.

En un polígon amb un forat, l'interior exclou el forat i la frontera inclou l'anell que el delimita. Un punt dins del forat és a l'exterior del polígon; un punt sobre l'anell interior és a la frontera. En una multigeometria, la frontera es deriva del conjunt complet i pot no coincidir amb la simple suma intuïtiva de les fronteres de cada part. Aquestes diferències expliquen per què cal utilitzar predicats implementats segons un model formal en lloc de deduir relacions a partir de caixes envolupants.

### La matriu DE-9IM

El **model d'intersecció estès dimensional de nou posicions** (DE-9IM) compara l'interior, la frontera i l'exterior d'una geometria A amb els mateixos tres conjunts d'una geometria B. Les nou interseccions formen una matriu 3 × 3. Cada cel·la indica si la intersecció és buida o quina dimensió màxima té: punt, línia o superfície {% cite ogcSimpleFeatures2011 %}.

La formulació de les nou interseccions parteix del treball d'Egenhofer i Franzosa sobre relacions topològiques entre conjunts de punts {% cite egenhoferPointSetTopological1991 %}. Clementini, Di Felice i van Oosterom hi van incorporar la dimensió de les interseccions i van proposar un conjunt reduït de relacions amb nom per a la interacció amb usuaris {% cite clementiniFormalTopological1993 %}.

::: table "Estructura de la matriu DE-9IM per a A i B"
| A respecte de B | Interior de B | Frontera de B | Exterior de B |
| --- | --- | --- | --- |
| Interior d'A | $I(A) \cap I(B)$ | $I(A) \cap \partial B$ | $I(A) \cap E(B)$ |
| Frontera d'A | $\partial A \cap I(B)$ | $\partial A \cap \partial B$ | $\partial A \cap E(B)$ |
| Exterior d'A | $E(A) \cap I(B)$ | $E(A) \cap \partial B$ | $E(A) \cap E(B)$ |
:::

Una implementació pot codificar les cel·les com `F` quan són buides o com `0`, `1` i `2` segons la dimensió de la intersecció; en patrons de consulta, `T` admet qualsevol intersecció no buida i `*` no imposa cap condició. Els predicats amb nom són patrons interpretables sobre aquesta matriu. No cal memoritzar les nou posicions de cada predicat, però sí entendre que `touches`, `crosses` o `overlaps` no es decideixen per una semblança visual: exigeixen combinacions concretes d'interiors i fronteres.

![Matriu DE-9IM amb les nou interseccions entre l'interior, la frontera i l'exterior de dues geometries]({{ site.baseurl }}/assets/diagrams/ca/06-analisi-geoprocessament-vectorial/de9im-relations.mmd "Matriu esquemàtica de les nou interseccions entre interior, frontera i exterior; cada predicat amb nom imposa després un patró i unes condicions dimensionals concretes."){: data-figure-width-web="50rem" data-figure-width-pdf="100%"}

DE-9IM descriu relacions topològiques, no distàncies. Dos polígons separats per una escletxa mínima continuen sent `disjoint`; dos que comparteixen un segment poden estar en contacte (`touches`); i dos que comparteixen superfície s'intersequen (`intersects`), però no només es toquen. Si la pregunta diu «a menys de», cal un predicat de distància o una àrea d'influència, no una reinterpretació de `intersects`.

La direcció ocupa un paper diferent segons el predicat. `intersects`, `disjoint`, `touches`, `overlaps`, `equals` i `crosses` són simètrics: intercanviar A i B no canvia el valor lògic quan la relació és aplicable. En `crosses`, les dimensions de les geometries determinen si el predicat és aplicable i què significa. `within` i `contains` són inversos: A pot ser dins de B mentre B conté A. En una selecció de QGIS, la capa objectiu continua determinant quines entitats es conserven encara que el predicat sigui simètric.

### Semàntica dels predicats habituals

::: table "Predicats espacials i condicions que no s'han de confondre"
| Predicat | Relació essencial | Exemple conceptual | Precaució |
| --- | --- | --- | --- |
| `intersects` | Les geometries comparteixen almenys un punt | Una línia entra en un polígon o només en toca la vora | És la negació de `disjoint` i inclou moltes relacions més específiques |
| `disjoint` | No comparteixen cap punt | Dos polígons separats | Una distància molt petita continua sent separació topològica |
| `touches` | Comparteixen punts, però els interiors no es comparteixen | Dos polígons adjacents amb frontera comuna | Un solapament d'àrea no és contacte pur |
| `crosses` | La intersecció travessa l'interior amb una dimensió inferior adequada | Dues línies que es tallen en un punt interior | No és un sinònim general d'`intersects` |
| `within` | A queda dins de B i els interiors tenen la relació exigida | Un punt estrictament interior a un polígon | Un punt només sobre la frontera no és `within` en el sentit estricte |
| `contains` | A conté B; és la relació inversa de `within` | Un polígon conté un punt interior | Cal situar correctament capa objectiu i capa de comparació |
| `overlaps` | Geometries de la mateixa dimensió comparteixen part de l'interior sense ser iguals ni contenir-se completament | Dos polígons amb una zona comuna parcial | No descriu qualsevol intersecció ni una contenció completa |
| `equals` | Interiors, fronteres i exteriors ocupen els mateixos conjunts de punts | Dues geometries topològicament iguals | No implica que comparteixin identificador, ordre de vèrtexs o atributs |
:::

`intersects` és deliberadament ampli. Retorna cert per contacte, creuament, solapament, contenció i igualtat, sempre que hi hagi almenys un punt comú. És útil per no perdre candidats, però sovint necessita un diagnòstic posterior. Si es volen només municipis limítrofs sense superfície comuna, `touches` expressa millor la pregunta; si es volen zones parcialment superposades, `overlaps` exclou les contencions completes.

La distinció entre contenció estricta i cobertura de la frontera és especialment important amb punts. `within` exigeix la relació d'interiors definida pel model; una família de predicats com `covered_by` i `covers`, quan l'eina els ofereix, permet incloure explícitament la frontera. No s'ha de canviar de predicat només per augmentar el recompte. Primer cal decidir si el fenomen pot pertànyer legítimament al límit i com s'han de tractar les coincidències múltiples.

`crosses` depèn de les dimensions. Dues línies que es troben només als extrems poden complir `touches`, mentre que si els interiors es tallen en un punt poden complir `crosses`. Una línia que entra i surt d'un polígon pot creuar-lo; dos polígons amb superfície comuna parcial se solen descriure amb `overlaps`. El nom quotidià «creuar» no determina el predicat formal.

### Exemple resolt amb geometries ideals

En un conjunt ideal hi ha un polígon quadrat B, un punt P al seu interior, un punt Q sobre una aresta i un punt R a l'exterior. Són geometries didàctiques exactes, no observacions mesurades. P compleix `within(P, B)` i `intersects(P, B)`; Q compleix `touches(Q, B)` i `intersects(Q, B)`, però no `within(Q, B)`; R compleix `disjoint(R, B)`.

En el mateix exercici, dues línies obertes L1 i L2 compleixen `crosses(L1, L2)` si es tallen en un punt interior de totes dues. Si només comparteixen un extrem, poden complir `touches` sense creuar-se. Finalment, dos polígons A i B amb una franja interior parcial compleixen `overlaps(A, B)`; si A queda completament dins de B, compleix `within(A, B)` i ja no és un solapament parcial. Aquestes resolucions permeten predir l'eina abans d'aplicar-la a geometries reals amb toleràncies i errors.

Les geometries ideals es poden escriure com a **text ben conegut** (WKT, de l'anglès *well-known text*) per repetir la prova sense dibuixar-les manualment. El **binari ben conegut** (WKB) codifica el mateix model en forma binària i no es llegeix directament com a text. Tots dos són representacions d'intercanvi de geometries definides per Simple Features, no predicats ni formats complets de capa {% cite ogcSimpleFeatures2011 %}.

::: listing "Geometries WKT per comprovar interior, frontera i exterior"
```text
POLYGON ((0 0, 2 0, 2 2, 0 2, 0 0))
POINT (1 1)
POINT (0 1)
POINT (3 1)
```
:::

Respecte del polígon de la primera línia, els punts següents representen, per ordre, interior, frontera i exterior. Les coordenades només defineixen un exercici cartesià sense unitat territorial. Assignar-los un CRS o interpretar-ne la distància exigiria una decisió addicional que aquesta prova topològica no necessita.

### Model formal i càlcul finit

Les coordenades digitals tenen precisió finita. Geometries procedents de fonts diferents poden representar el mateix límit amb vèrtexs lleugerament separats, i una transformació de CRS pot introduir diferències numèriques. El predicat avalua les geometries disponibles, no la intenció del productor. Ajustar o arrodonir coordenades pot canviar relacions i no s'ha d'aplicar sense una tolerància justificada per l'exactitud i l'escala.

Una geometria invàlida pot fer que la seva frontera o interior no es puguin interpretar de manera consistent i que una operació falli o doni fragments inesperats. La validació individual i les regles entre entitats s'han de revisar abans del geoprocessament. Reparar automàticament totes les entrades tampoc no és neutral: pot moure, dividir o eliminar components i obliga a comparar la sortida amb la font.

Les operacions de superposició creen geometries derivades. Cal triar-les segons la pregunta, no segons la semblança dels noms.

::: table "Operacions vectorials i efecte sobre el resultat"
| Operació | Geometria resultant | Atributs habituals | Pregunta típica |
| --- | --- | --- | --- |
| Extracció | Entitats completes seleccionades | De l'entrada | Quines entitats compleixen el criteri? |
| Unió espacial | Geometria de la capa objectiu | Camps afegits de la capa relacionada | A quina zona correspon cada entitat? |
| Retall (`clip`) | Part de l'entrada dins de la màscara | De l'entrada | Quina part queda dins l'àmbit? |
| Intersecció | Parts comunes entre entrades | De totes dues capes | On coincideixen els dos fenòmens? |
| Diferència | Part de l'entrada fora de la màscara | De l'entrada | Què queda exclòs? |
| Diferència simètrica | Parts exclusives de cadascuna de les dues entrades | De la capa corresponent, amb nuls o camps separats segons l'eina | On apareix exactament un dels dos fenòmens? |
| Unió geomètrica (`union`) | Extensió conjunta segmentada pels límits entre les dues capes; només és una partició disjunta si cada entrada ja és una cobertura sense solapaments interns | De totes dues capes, amb nuls | Quines zones són comunes o exclusives? |
| Dissolució | Geometria agregada per grup | Camps de l'entrada; els valors no formen un resum estadístic | Quin contorn únic correspon a cada classe? |
:::

![Comparació de la geometria de sortida i els atributs propagats pel retall, la intersecció, la unió, la diferència i la dissolució]({{ site.baseurl }}/assets/diagrams/ca/06-analisi-geoprocessament-vectorial/vector-overlay-semantics.mmd "La geometria i els atributs conservats depenen de l'operació. La lectura de la unió com a zones exclusives o comunes pressuposa entrades sense solapaments interns."){: data-figure-width-web="34rem" data-figure-width-pdf="80%"}

Una intersecció pot dividir una entitat en molts fragments i copiar-hi el mateix atribut original. Si una parcel·la amb un recompte $N$ queda partida en dos fragments, tots dos poden conservar $N$ i sumar-los produiria $2N$. Repartir una variable extensa segons superfície exigeix una hipòtesi explícita de distribució uniforme i no és adequat per a qualsevol fenomen.

La dissolució és una operació geomètrica, no una agregació estadística.

L'algorisme `native:dissolve` de QGIS conserva per als camps no agrupadors els valors de la primera entitat processada, que no representen necessàriament tot el grup. L'opció `Keep disjoint features separate` pot crear més d'una fila per valor de grup. Quan cal sumar, comptar o resumir atributs, s'ha d'aplicar una agregació explícita i comprovar-la separadament {% cite qgisUserGuide344 %}.

### Selecció per ubicació o transformació

Una **selecció per ubicació** avalua un predicat entre una capa objectiu i una capa de comparació. Si una línia interseca una zona, queda seleccionada sencera encara que només un segment hi entri. Una **extracció per ubicació** pot materialitzar les mateixes entitats completes en una capa nova. Cap de les dues calcula només el tros comú.

Una **unió espacial** també conserva habitualment la geometria objectiu, però hi afegeix atributs de les coincidències. Una **intersecció geomètrica** construeix les parts comunes i pot fragmentar l'objectiu. Un **retall** construeix la part interior a la màscara sense incorporar normalment els seus atributs. Triar entre aquestes operacions exigeix decidir si la sortida ha de respondre «quines entitats?», «a quina zona correspon cada entitat?» o «quina part exacta coincideix?».

::: table "La mateixa relació aplicada amb efectes diferents"
| Procediment | Conserva la geometria completa de l'objectiu | Afegeix atributs de l'altra capa | Crea parts geomètriques noves |
| --- | --- | --- | --- |
| Selecció per ubicació | Sí | No | No |
| Extracció per ubicació | Sí | No | No; només materialitza les entitats coincidents |
| Unió d'atributs per ubicació | Sí, segons la capa objectiu | Sí | No en la forma ordinària |
| Retall | No | No, llevat de camps afegits per un altre pas | Sí |
| Intersecció | No | Sí | Sí |
:::

![Comparació de la línia A que interseca el polígon B quan se selecciona sencera, es retalla o es transforma mitjançant una intersecció]({{ site.baseurl }}/assets/quarto/06-analisi-geoprocessament-vectorial/selection-overlay.qmd "La selecció i l'extracció conserven l'entitat completa; el retall i la intersecció en construeixen només la part comuna amb la màscara, però propaguen atributs diferents."){: data-figure-width-web="54rem" data-figure-width-pdf="100%"}

La direcció s'ha d'explicitar fins i tot per a un predicat simètric. «Seleccionar portals que intersecten zones» conserva portals; «seleccionar zones que intersecten portals» conserva zones. El predicat és el mateix, però la unitat de la resposta i el recompte canvien. En una unió espacial, la direcció determina quina geometria es conserva i quins atributs es repeteixen.

Les coincidències múltiples formen part del resultat. Un punt en una partició poligonal ben construïda acostuma a tenir una zona interior, però un punt de frontera pot intersectar-ne més d'una. Una línia pot travessar molts polígons de manera legítima. L'eina pot crear una fila per coincidència, seleccionar una sola entitat relacionada o calcular un resum; cal declarar l'opció i comptar objectius amb zero, una i diverses parelles.

### Operacions de conjunts espacials

Si A representa la geometria d'entrada i B la màscara o segona entrada, el retall i la intersecció conserven geomètricament $A \cap B$, però no construeixen la mateixa taula. La diferència conserva $A \setminus B$. La unió cobreix $A \cup B$ i segmenta els límits entre A i B. Aquesta segmentació diferencia zones només d'A, només de B i comunes quan cada entrada és una cobertura sense solapaments interns; si A o B ja contenen entitats superposades, la sortida pot conservar peces coincidents o duplicades i no és una partició disjunta. La diferència simètrica conserva $(A \setminus B) \cup (B \setminus A)$ i elimina la part comuna.

Aquestes equivalències descriuen conjunts de punts ideals. Un algorisme concret també imposa tipus de geometria, regles d'atributs, precisió numèrica i tractament de geometries buides. Dues operacions amb la mateixa extensió geomètrica teòrica poden produir esquemes i nombres de files diferents. La documentació de QGIS i la informació de l'algorisme s'han de consultar per conèixer el contracte de la versió i del proveïdor utilitzats {% cite qgisUserGuide344 %}.

#### Retall

El **retall** (`clip`) utilitza B com un motlle. Conserva de cada entitat d'A la part situada dins de la geometria conjunta de B i manté els atributs d'A. Els camps de B no s'incorporen perquè la màscara respon on es talla, no quina entitat aporta cada tros. Si aquesta identitat és necessària, cal una intersecció.

Retallar una xarxa pel municipi modifica la longitud dels trams que creuen el límit. Qualsevol camp de longitud calculat abans queda desactualitzat, encara que continuï a la taula. També poden aparèixer diverses parts procedents d'una mateixa entitat. El control ha de comprovar que cap part queda fora de la màscara, que la mesura no augmenta i que l'identificador d'origen permet reconstruir la fragmentació.

#### Intersecció

La **intersecció** compara entitats d'A amb entitats de B i crea una peça per a cada coincidència geomètrica amb dimensió admesa per la sortida. Cada peça rep atributs de les dues files que l'han generada. Intersectar cobertes amb municipis permet saber quina categoria i quin municipi corresponen a cada fragment, però una coberta que travessa tres municipis pot convertir-se en tres files.

La multiplicació de files és correcta quan reflecteix parelles espacials diferents. El risc apareix en els atributs extensius. Si una entitat d'origen tenia un recompte referit a tota la seva geometria, copiar-lo a cada fragment no reparteix el fenomen. Sumar-lo després el comptaria diverses vegades. Una ponderació per superfície només és defensable si la variable es pot suposar distribuïda uniformement o si hi ha una font més detallada que en justifiqui la desagregació.

#### Unió geomètrica

La **unió geomètrica** (`union`) conserva tota l'extensió coberta per A o B i talla les geometries pels límits entre totes dues capes. A la part només d'A, els camps de B queden nuls; a la part només de B, els camps d'A queden nuls; a la zona comuna hi ha atributs de totes dues. Aquest patró de nuls és informació sobre pertinença espacial, no necessàriament manca de dades. L'algorisme `native:union` no resol per si sol els solapaments interns de cada entrada: abans i després cal comptar-los i comprovar si el cas requeria una cobertura sense duplicacions.

`Union` no significa apilar files ni combinar fitxers amb el mateix esquema. Afegir entitats d'una capa sota les d'una altra és una fusió o annexió de capes i no calcula superposicions. Tampoc no equival a dissolució: la unió crea més particions quan hi ha límits creuats, mentre que la dissolució elimina límits interns segons un criteri.

#### Diferència i diferència simètrica

La **diferència** és direccional. $A \setminus B$ conserva les parts d'A que no són cobertes per B; intercanviar les entrades produeix $B \setminus A$, una resposta diferent. És adequada per aplicar una exclusió, sempre que B representi exactament la zona que s'ha de treure. Si només se seleccionessin les entitats d'A disjuntes de B, es perdrien també les parts exteriors de les entitats que el travessen.

La **diferència simètrica** conserva les zones que pertanyen exclusivament a una de les dues entrades. És útil per comparar cobertures quan interessa localitzar desacords i no només allò que una té de més respecte de l'altra. No indica per si sola si el canvi és real, un desplaçament posicional o una diferència d'escala; els camps de procedència i la inspecció dels límits han de permetre classificar-lo.

#### Dissolució i geometries multipart

La **dissolució** agrupa geometries d'una mateixa capa segons un o més camps i calcula la unió geomètrica de cada grup. Si no es defineix cap camp, pot produir una entitat que representa la geometria agregada de tota la capa. Per defecte, les parts separades d'un mateix grup poden quedar dins d'una sola geometria multipart. Si s'activa `Keep disjoint features separate`, cada component desconnectat pot generar una fila i ja no hi ha necessàriament un únic registre per grup.

L'operació geomètrica no defineix la suma, la mitjana, el recompte ni cap altra estadística dels atributs. Que l'algorisme conservi una fila i alguns camps no converteix els valors retinguts en representants del grup. Per obtenir una població agregada cal sumar explícitament poblacions compatibles; per obtenir una densitat cal dividir totals adequats; per comptar entitats originals cal conservar-ne un identificador o calcular el recompte abans o durant una agregació separada.

Quan calen geometria dissolta i estadístiques, el flux més transparent produeix dos resultats controlables: una geometria per clau de grup i una taula agregada per la mateixa clau. Després es comprova que totes dues claus siguin úniques i s'uneixen. Una eina que ofereixi simultàniament geometria i agregats també és vàlida si cada estadística queda configurada explícitament; el nom `Dissolve`, tot sol, no autoritza a suposar-les.

### Exemple resolt: què conserva cada operació

Dos polígons didàctics A i B se superposen parcialment i tenen un identificador propi. Una selecció d'A per `intersects` amb B conserva A complet. Un retall d'A amb B conserva només la part comuna i només els atributs d'A. Una intersecció conserva la mateixa part comuna i hi associa els identificadors d'A i B. La diferència d'A respecte de B conserva la part exclusiva d'A.

La unió produeix peces per a la part exclusiva d'A, la part comuna i la part exclusiva de B, amb nuls als camps de la capa absent. La diferència simètrica conserva les dues parts exclusives i elimina la comuna. Dissoldre A i B sense camp, si abans s'han incorporat a una mateixa capa compatible, elimina el límit interior de la seva geometria conjunta, però no calcula cap resum vàlid dels seus atributs. La predicció de geometria i esquema permet escollir l'operació sense basar-se en el nom del botó.

## Àrees d'influència i distància

Una àrea d'influència o `buffer` amb extrems i unions arrodonits aproxima el conjunt de punts situats a una distància màxima d'una geometria. Al voltant d'un punt forma una aproximació poligonal a un disc; al voltant d'una línia, una franja; i al voltant d'un polígon, una expansió o retracció. Amb extrems plans o quadrats i unions bisellades o en punta, la sortida deixa de coincidir exactament amb aquest conjunt de distància.

La distància, les unitats, el nombre de segments, la forma dels extrems i la dissolució condicionen la sortida. El càlcul necessita un CRS i un model de distància adequats. Crear un `buffer` de 200 sobre coordenades en graus no produeix una franja de 200 m.

Dissoldre els buffers elimina solapaments interns i evita comptar diverses vegades una mateixa superfície, però també elimina la identitat de cada entitat d'origen. Quan interessa saber quin fanal o quin tram genera cada cobertura, convé conservar els buffers individuals i crear una segona capa dissolta per calcular la superfície conjunta.

>>>> **Proximitat no és accessibilitat.** Una distància euclidiana no incorpora sentit de circulació, pendents, passos de vianants, barreres, temps ni capacitat. El resultat s'ha de descriure com una zona geomètrica de proximitat llevat que el model incorpori explícitament una xarxa o altres restriccions.

### Distància, CRS i model de mesura

La distància del `buffer` s'interpreta segons el contracte de l'algorisme. En una operació plana ordinària, el valor s'expressa en les unitats del CRS de processament o de la capa; un valor `200` només significa 200 m si la unitat lineal pertinent és el metre. En un CRS geogràfic, els eixos s'expressen angularment i no es poden tractar els graus com una distància mètrica constant. Reprojectar explícitament a un CRS adequat a l'àrea d'estudi fa visibles la referència, les unitats i l'extensió d'ús.

Una distància geodèsica sobre l'el·lipsoide i una distància plana en una projecció no són idèntiques. Per a un àmbit local i un CRS projectat apropiat, l'aproximació plana pot ser suficient; per a extensions grans o zones on la projecció deforma fortament la distància, cal un algorisme o un procediment geodèsic. Canviar només el CRS del projecte no transforma les coordenades emmagatzemades ni modifica necessàriament el model que utilitza l'eina.

El llindar ha de provenir de la pregunta. Pot correspondre a una distància normativa, a una hipòtesi exploratòria o a una aproximació funcional; aquestes justificacions no són equivalents. Si la norma mesura des de la vora d'una plataforma i la capa només conté l'eix de la carretera, un `buffer` des de l'eix no representa exactament la franja legal. L'abstracció geomètrica de l'entrada forma part de la incertesa.

### Aproximació de corbes, extrems i cantonades

Els arcs circulars s'emmagatzemen sovint com una successió de segments rectes. El paràmetre **segments** del `Buffer` natiu de QGIS indica la quantitat utilitzada per aproximar un quart de circumferència. Un nombre més gran suavitza l'arc i augmenta el nombre de vèrtexs, el volum i el cost de les operacions posteriors. No hi ha un valor universal: ha de ser prou fi per a l'escala i la mesura exigides, i s'ha de mantenir constant quan es comparen escenaris {% cite qgisUserGuide344 %}.

En buffers de línies, l'estil dels extrems pot ser arrodonit, pla o quadrat. L'extrem pla acaba a la coordenada final i exclou punts pròxims més enllà de l'extrem; el quadrat s'estén més enllà i pot incloure punts a una distància superior al valor nominal en diagonal; l'arrodonit hi afegeix un semicercle aproximat. En trams curts, aquesta decisió pot afectar una part considerable de la superfície. Si la pregunta és literalment «quins punts són a una distància màxima $d$?», cal usar extrems i unions arrodonits amb una segmentació suficient o l'algorisme `Select within distance`. Dissoldre una xarxa després pot ocultar algunes juntes internes, però no corregeix una connectivitat defectuosa.

L'estil d'unió controla les cantonades entre segments: arrodonida, bisellada o en punta. Una unió en punta pot produir prolongacions molt llargues en angles aguts, i el paràmetre `Miter limit` en restringeix l'extensió. Aquests paràmetres no són decoratius quan el resultat es mesura o s'utilitza com a màscara. El diari ha d'indicar-los si poden canviar la zona candidata.

![Efecte del radi, els segments per quadrant, els extrems i les unions sobre buffers de punts, línies i polígons]({{ site.baseurl }}/assets/quarto/06-analisi-geoprocessament-vectorial/buffer-parameters.qmd "Un buffer depèn de la geometria d'entrada i del radi, però també de l'aproximació de les corbes, els extrems de les línies i les unions entre segments; aquestes opcions poden canviar la superfície resultant."){: data-figure-width-web="50.5rem" data-figure-width-pdf="100%"}

Un `buffer` d'un sol costat és útil quan una línia orientada representa un marge concret, però «esquerra» i «dreta» depenen de l'ordre dels vèrtexs. Invertir la digitalització inverteix el costat. Abans d'utilitzar-lo cal comprovar el sentit de les línies i conservar una mostra on la relació entre orientació i sortida sigui visible.

### Distància variable i buffers negatius

La distància pot procedir d'un camp o d'una expressió. Això permet aplicar una franja diferent segons la categoria d'una via o una propietat de l'entitat, però converteix l'esquema atributiu en un paràmetre geomètric. Cal revisar nuls, unitats, signes, valors extrems i domini abans de processar. Un nul no s'ha de substituir per zero sense decidir si significa «sense franja», «dada desconeguda» o «entitat no aplicable».

Un valor negatiu sobre polígons genera una retracció interior quan la geometria i l'algorisme ho permeten. Les parts estretes poden desaparèixer, un polígon pot dividir-se i una distància superior a la seva amplada local pot produir geometria buida. No és una manera general de corregir límits ni d'estimar una superfície útil: és una transformació morfològica amb efectes que s'han de comptar i inspeccionar.

### Dissoldre cobertura o conservar origen

Amb buffers individuals, cada polígon conserva la fila i els atributs de l'entitat generadora. Les zones solapades existeixen en més d'una geometria i sumar-ne les àrees compta la coincidència diverses vegades. Amb dissolució, la geometria conjunta elimina les fronteres internes i permet mesurar la cobertura única, però ja no indica directament quin origen cobreix cada posició.

Quan calen totes dues preguntes, convé conservar dues sortides: buffers individuals per atribuir cobertura i una còpia dissolta per calcular la unió espacial. Dissoldre per categoria conserva una geometria per valor de grup, no necessàriament per entitat. En cap cas la dissolució defineix per si sola com s'han de sumar capacitats, intensitats o altres atributs dels generadors.

![Comparació de quatre buffers individuals amb una cobertura dissolta que conserva dos components desconnectats]({{ site.baseurl }}/assets/quarto/06-analisi-geoprocessament-vectorial/buffer-dissolve.qmd "Els buffers individuals mantenen l'origen però superposen cobertures; la dissolució elimina les fronteres internes i permet mesurar una cobertura única, a canvi de perdre l'atribució directa a cada generador."){: data-figure-width-web="51rem" data-figure-width-pdf="100%"}

### Exemple resolt: franja al voltant d'una xarxa

En una xarxa didàctica, alguns trams comparteixen node i altres se solapen parcialment. Si la pregunta demana quins portals queden a una distància geomètrica $d$, el flux pot utilitzar `Select within distance` o crear un `buffer` amb $d$, extrems i unions arrodonits i una segmentació suficient en un CRS mètric adequat. Una còpia dissolta representa la cobertura única i és útil per mesurar-ne la superfície; no és necessària per evitar portals duplicats en una selecció espacial ordinària, perquè el resultat és un conjunt d'identificadors d'entitat.

Si, en canvi, la pregunta demana quin tram podria associar-se a cada portal, la capa individual és necessària i les coincidències múltiples s'han de conservar o resoldre amb una regla de distància. El `buffer` dissolt respon a cobertura conjunta; els buffers individuals responen a possibles generadors. Cap resultat no mesura temps de recorregut ni accessibilitat sense incorporar una xarxa i els seus costos.

## Superposició i anàlisi multicriteri

Una anàlisi multicriteri transforma cada condició en una capa o màscara i després les combina. La lògica espacial ha de quedar escrita abans d'obrir l'algorisme. Per exemple, una zona candidata podria haver d'estar fora de dues franges viàries, a prop d'una carretera secundària i dins d'una àrea urbana. Canviar `AND` per `OR`, o aplicar diferència en un ordre diferent, canvia el significat territorial.

La seqüència més fàcil de validar avança de geometries existents a derivades i després a combinades:

1. Seleccionar i extreure les entitats d'entrada.
2. Validar geometries, CRS, unitats i extensió.
3. Crear una zona per a cada criteri.
4. Comprovar cada zona per separat.
5. Combinar-les amb intersecció, diferència o unió.
6. Recalcular superfícies i revisar fragments.
7. Interpretar la zona final com a resultat del model, no com una observació directa.

Els llindars han de respondre al cas. Una franja de 50 m pot provenir d'una norma, d'una hipòtesi pedagògica o d'una decisió exploratòria; aquestes justificacions no són equivalents. El diari ha d'indicar-ne la font o la funció.

### Criteris d'inclusió i d'exclusió

Cada criteri s'ha de formular com un conjunt espacial. Una zona d'inclusió conté les posicions admeses per una condició, mentre que una zona d'exclusió conté les que s'han de retirar. Si U és l'univers d'estudi, C una zona compatible per coberta, P una zona de proximitat i E una exclusió, una formulació possible és $(U \cap C \cap P) \setminus E$. L'expressió deixa clar que totes les inclusions s'han de complir i que l'exclusió s'aplica al resultat.

La geometria de l'univers és necessària perquè el complement d'una exclusió no és finit sense un àmbit. «Fora del buffer» vol dir la part d'U que no queda dins del buffer, no tot l'espai exterior del planeta. El límit municipal pot servir d'univers si la pregunta és municipal, però no si equipaments externs o processos transfronterers condicionen el fenomen.

Un criteri atributiu s'ha d'aplicar abans de derivar-ne la geometria quan defineix quines entitats són rellevants. Si només les vies d'una categoria generen una franja, primer se seleccionen i s'extreuen amb el camp documentat; després es calcula el `buffer`. Dissoldre totes les vies i intentar recuperar la categoria més tard perdria la traça de quines geometries han contribuït al criteri.

### Ordre, equivalències i resultats intermedis

Algunes operacions de conjunts tenen equivalències matemàtiques, però el flux digital pot diferir per atributs, precisió i cost. Intersectar primer amb un àmbit petit pot reduir el volum de dades. En `native:clip`, les entitats de la màscara ja es tracten com una geometria conjunta, de manera que predissoldre-les no evita fragments causats pels límits interns; amb altres proveïdors cal comprovar el contracte. Predissoldre continua sent una simplificació possible si redueix volum i si els identificadors i límits eliminats no són necessaris per a la pregunta.

Els resultats intermedis han de correspondre a criteris interpretables.

Una capa `zona_proximitat`, una `zona_exclusio` i una `zona_compatible` es poden validar separadament; una seqüència de capes `temp1`, `temp2` i `final3` no permet relacionar un error amb una decisió. Conservar els intermedis determinants no obliga a conservar totes les proves, però sí les entrades que permeten auditar el resultat final.

### Exemple resolt: combinar tres condicions

En un cas didàctic, les zones candidates han de quedar dins de l'àmbit U, dins d'una coberta admesa C, prop d'una xarxa seleccionada V i fora d'una zona incompatible E. Primer es valida U i s'extreu C amb una consulta atributiva. Després es crea el `buffer` P de V amb una distància $d$ justificada i es dissol només per obtenir cobertura conjunta. La intersecció $U \cap C \cap P$ crea les inclusions comunes, i la diferència respecte d'E produeix el resultat R.

Si s'utilitzés `OR` entre C i P, R inclouria posicions que només compleixen un dels criteris. Si s'apliqués una selecció espacial en lloc d'una intersecció, es conservarien polígons complets de C encara que només una part fos pròxima. Si es calculés la diferència en l'ordre invers, $E \setminus (U \cap C \cap P)$, el resultat descriuria la part de l'exclusió que queda fora de les inclusions, no les candidatures. Predir aquests efectes és part de la resolució.

El resultat final només afirma que les geometries disponibles compleixen les regles codificades. No prova disponibilitat jurídica, propietat, accessibilitat, cost, acceptació social ni qualsevol factor omès. Una zona candidata és una sortida del model i necessita comprovació amb fonts independents i, quan la decisió ho exigeix, treball de camp.

### Sensibilitat als supòsits

Una **anàlisi de sensibilitat** repeteix el flux modificant una decisió plausible mentre manté constants les altres. En aquest context pot variar la distància $d$, el predicat que tracta la frontera, l'edició d'una font, la tolerància de precisió o la mida d'una cel·la d'agregació. L'objectiu no és trobar el paràmetre que produeix el mapa més convincent, sinó observar quines conclusions depenen fortament d'una elecció.

Comparar només la superfície total pot ocultar canvis de forma i localització. Dues alternatives poden tenir àrees semblants i ocupar zones diferents. La sensibilitat s'ha de descriure amb mesures adequades al cas: àrea comuna i exclusiva, nombre de components, entitats incloses de manera estable, canvis prop dels límits i inspecció de les zones que entren o surten. No s'han d'inventar valors esperats abans d'executar l'anàlisi.

Si una variació petita del llindar elimina la major part de les candidatures o canvia quins equipaments hi entren, el resultat és fràgil respecte d'aquell paràmetre. Això no invalida necessàriament el model, però obliga a comunicar el rang, justificar millor el criteri o evitar una classificació binària excessivament concloent. Si les alternatives produeixen el mateix patró essencial, aquesta estabilitat és una evidència de consistència, no una prova de veritat externa.

### Validació del flux multicriteri

La validació combina invariants geomètrics, recomptes, atributs i contrast territorial. Cada resultat d'intersecció ha de quedar dins de totes les entrades; una diferència no ha d'intersectar l'interior de l'exclusió; la cobertura dissolta no ha de tenir més àrea que la suma dels buffers individuals; i la suma de parts exclusives i comunes s'ha de poder relacionar amb la unió, dins de la tolerància numèrica adoptada.

També cal cercar casos negatius i de frontera. Una posició que compleix clarament tots els criteris ha d'aparèixer; una que n'incompleix un de manera clara no; i una mostra sobre cada límit permet comprovar com s'ha aplicat el predicat. Les comprovacions manuals s'han de triar abans de mirar el resultat quan sigui possible, perquè seleccionar només exemples favorables no posa a prova el flux.

La validació externa contrasta la sortida amb una font o una observació que no s'ha utilitzat per construir-la. Una ortofoto pot revelar una barrera omesa, una visita de camp pot mostrar que un pas no existeix i un registre administratiu pot descartar una zona geomètricament compatible. Aquest contrast no s'ha de confondre amb ajustar repetidament els criteris fins que coincideixin amb una expectativa no documentada.

## Cas guiat: vies, portals i fanals

La demostració de Vila-seca selecciona primer les vies principals i crea àrees d'influència amb distàncies justificades. Una selecció espacial identifica els portals que intersecten aquestes zones, mentre que un retall o una intersecció permetria crear geometries noves. Comparar les sortides fa visible la diferència entre conservar una entitat completa i fragmentar-la.

Una segona anàlisi combina dues distàncies: proximitat als fanals inventariats del carrer de Joanot Martorell i proximitat a l'entorn de la Facultat. La intersecció dels buffers delimita l'espai que compleix tots dos criteris. El recompte de fanals no s'ha de confondre amb una mesura d'il·luminació, perquè el model no incorpora potència, obstacles ni mesura lumínica.

La validació compara el nombre d'entitats abans i després, l'àrea de cada zona, les coincidències múltiples i una mostra sobre una ortofoto. Els camps d'àrea emmagatzemats s'han de recalcular després de fragmentar geometries.

El cas comença amb un contracte per a cada entrada: què representa la geometria viària, quina data i exactitud tenen els portals i fanals, quin és el límit de treball i en quin CRS es faran les mesures. Les vies es filtren per la categoria necessària i s'extreuen perquè el criteri quedi materialitzat. Abans del `buffer` es comproven geometries nul·les, longituds no positives, duplicats i trams que aparentment haurien de connectar.

La primera comparació resol dues preguntes diferents. `Select by location` identifica els portals complets que intersecten la franja viària; una intersecció entre línies o polígons i la franja crearia les parts geomètriques comunes. Com que els portals són punts, fragmentar-los no aporta una geometria parcial: la selecció o extracció és suficient si només cal saber quins hi entren. Si un punt cau exactament al límit, el predicat i la precisió de la font s'han d'examinar abans de classificar-lo.

Per a la combinació de fanals i Facultat es conserven els buffers individuals i les cobertures dissoltes. Els primers permeten rastrejar quin origen participa en cada coincidència; les segones delimiten cada criteri sense solapaments interns. Intersectar les dues cobertures produeix la zona que compleix simultàniament les proximitats geomètriques. La sortida no rep una puntuació d'il·luminació ni d'accessibilitat perquè les entrades no contenen prou informació per calcular-les.

Cada pas produeix una fila de control al diari: nom d'entrada, filtre, algorisme, distància i unitat, paràmetres de corba, dissolució, nombre d'entitats, geometries buides i mesura recalculada. Una mostra inclou un cas clarament interior, un d'exterior i un de frontera. La revisió sobre ortofoto serveix per detectar obstacles o desplaçaments, no per substituir la font ni per redibuixar el resultat fins que coincideixi visualment.

## Tessel·lacions i dominis de proximitat

Una **tessel·lació** divideix l'espai en cel·les sense buits ni solapaments. Les malles quadrades i hexagonals ofereixen unitats regulars per agregar punts o comparar densitats. Aquesta regularitat no és neutral: la mida, l'origen i l'orientació de la graella poden alterar el patró observat {% cite longleyGeographicInformationScience2015 %}.

Els quadrats tenen una estructura simple però distingeixen veïnatge lateral i diagonal. Els hexàgons tenen sis veïns laterals a una distància homogènia entre centroides. En tots dos casos, un recompte per cel·la mesura intensitat espacial; només es converteix en taxa quan es divideix per una població o exposició adequada.

Els polígons de **Voronoi** assignen cada posició al punt generador més proper segons distància euclidiana. S'han de retallar a una àrea d'estudi defensable i han d'incloure equipaments propers situats fora del límit si poden influir en el territori. No representen àrees de servei reals perquè ometen barreres, xarxes, capacitat i demanda.

La triangulació de **Delaunay** és dual del diagrama de Voronoi i proposa veïnatges geomètrics entre punts. Les arestes no són automàticament connexions funcionals ni els triangles grans demostren per si sols l'existència d'una anomalia. Serveixen per formular hipòtesis que cal contrastar amb el fenomen.

### Graelles regulars i unitat d'anàlisi

Una graella imposa una zonificació comuna quan els límits administratius són massa desiguals o no corresponen al procés estudiat. Això facilita comparar recomptes sobre cel·les de mida semblant, però no converteix la malla en una observació neutral. La posició de l'origen, l'orientació, la mida i la forma decideixen quins punts queden junts i quins es reparteixen entre cel·les.

Aquest efecte forma part del problema de la unitat espacial modificable. Un patró concentrat a una mida pot suavitzar-se en cel·les més grans, i desplaçar la graella pot moure una concentració a través de diversos límits. Per això una malla exploratòria necessita almenys una segona mida o origen en l'anàlisi de sensibilitat. Si la conclusió desapareix amb un canvi plausible, s'ha de descriure com a dependent de la zonificació.

Els quadrats s'alineen de manera directa amb eixos cartesians i tenen veïns laterals i diagonals a distàncies diferents entre centroides. Els hexàgons tenen sis veïns que comparteixen costat i ofereixen una relació més homogènia en aquest sentit. Aquesta propietat no fa els hexàgons superiors per a qualsevol pregunta: els quadrats poden encaixar millor amb altres ràsters, facilitar una jerarquia niada o simplificar l'intercanvi.

La mida declarada només té lectura mètrica en un CRS projectat adequat. `Create grid` necessita una extensió, espaiaments i un CRS; aquests paràmetres han de quedar fixats perquè una execució posterior reprodueixi les mateixes cel·les. Retallar la graella exactament pel límit d'estudi crea cel·les parcials a la vora. Comparar-ne recomptes bruts amb els de cel·les completes pot ser enganyós si l'exposició o l'àrea observable no es corregeixen.

Per agregar punts, cal definir què passa sobre una frontera de cel·la, amb duplicats i amb punts sense coordenada. Un recompte descriu intensitat observada, no risc ni taxa. Dividir per l'àrea pot construir una densitat geomètrica; dividir per població, temps d'observació o una altra exposició construeix indicadors diferents. Les cel·les sense casos observats han de distingir-se de les cel·les sense cobertura de la font.

### Dominis de Voronoi

Donat un conjunt de punts generadors, el diagrama de Voronoi assigna a cada posició el generador amb menor distància segons la mètrica utilitzada. Els límits són llocs equidistants entre dos o més generadors. En una implementació plana ordinària, la distància és euclidiana en les coordenades del CRS; carrers, barreres, pendents i capacitat no alteren les cel·les.

La construcció necessita un domini finit per convertir les regions exteriors teòricament no acotades en polígons manejables. Retallar pel municipi és adequat només si la pregunta es limita a aquest àmbit i s'han incorporat els generadors externs prou pròxims per influir-hi. Si s'omet un equipament just fora del límit, una cel·la interior pot atribuir-se erròniament a un punt més llunyà situat dins.

Els punts duplicats o gairebé coincidents necessiten una regla. Dos registres a la mateixa coordenada no defineixen dominis separables només per distància; poden representar un duplicat, dos serveis al mateix edifici o entitats diferents. Agregar-los, conservar-los o desplaçar-los altera el model i s'ha de decidir amb atributs, no mitjançant una correcció geomètrica arbitrària.

Una cel·la gran indica que, dins del conjunt de generadors i el domini adoptats, el seu punt és el més pròxim sobre una regió extensa. No demostra demanda desatesa, cobertura efectiva ni capacitat suficient. Per parlar d'àrees de servei caldria incorporar xarxa, temps, barreres, horaris, capacitat i població potencial segons la pregunta.

### Veïnatge de Delaunay

La triangulació de Delaunay connecta punts de manera dual al Voronoi: dos generadors són veïns quan les seves cel·les comparteixen una aresta, en els casos no degenerats. Una propietat geomètrica de la triangulació és que l'interior del cercle circumscrit a cada triangle no conté altres punts del conjunt. Aquesta estructura evita triar una distància fixa per proposar veïns geomètrics, però continua depenent de tots els punts inclosos.

Punts col·lineals, duplicats o configuracions cocirculars poden produir casos degenerats o més d'una triangulació equivalent. Els punts de la vora acostumen a connectar-se mitjançant triangles més oberts perquè no hi ha generadors fora del domini. Abans d'interpretar longituds o formes cal revisar duplicats, extensió i efectes de vora.

Una aresta de Delaunay no prova que existeixi una carretera, una relació social, un flux o una connexió viable. Pot proposar parelles per a una inspecció, ajudar a construir una interpolació o descriure veïnatge geomètric. Convertir-la directament en xarxa funcional ignoraria obstacles i costos. De manera semblant, un triangle gran pot indicar separació relativa entre punts observats, però no identifica per si sol un buit de servei.

### Exemple resolt: tres estructures per als mateixos punts

Amb una capa didàctica de punts d'equipament, una graella respon quants punts o quina exposició correspon a cada unitat regular definida prèviament. Un Voronoi respon quin punt és el més proper a cada posició segons distància euclidiana dins del domini. Una triangulació de Delaunay respon quins punts són veïns geomètrics segons el conjunt complet. Cap sortida substitueix les altres perquè canvien la unitat i la pregunta.

El control de la graella compara mides i orígens i reconstrueix el recompte total a partir de cel·les. El de Voronoi verifica una correspondència entre generadors únics i cel·les dins de les limitacions de l'eina, incorpora punts externs rellevants i comprova posicions equidistants. El de Delaunay revisa duplicats, casos de vora i arestes que travessen barreres. La interpretació final conserva només les afirmacions que la mètrica geomètrica permet sostenir.

## Controls abans i després

Abans de processar cal comprovar el CRS real, les unitats, l'extensió, la validesa geomètrica, els identificadors estables, els filtres actius i la naturalesa dels atributs. Els FID interns del proveïdor no són identificadors de procedència: `union`, intersecció, diferència, dissolució i altres algorismes poden regenerar-los. Abans d'executar-los cal conservar una clau ordinària i explícita, com `id_font_a` o `id_font_b`, si s'ha de reconstruir la fragmentació. Després, cada operació necessita controls propis.

### Validesa individual i coherència entre entitats

Una geometria **invàlida** incompleix les regles estructurals del seu tipus, per exemple un polígon amb un anell autointersectat. Una geometria vàlida pot ser incorrecta per al model: dos polígons d'una partició poden solapar-se, una xarxa pot tenir un extrem desconnectat o un punt pot quedar fora de la zona exigida. `Check validity`, les regles topològiques i els predicats entre capes responen controls diferents.

En una xarxa, un extrem penjant pot indicar una connexió interrompuda o un cul-de-sac legítim. Un pseudonode, on dos trams formen una continuïtat de grau dos, pot ser redundant o conservar un canvi d'atribut necessari. La regla no s'ha de deduir del nom de l'error: cal saber si el model representa connectivitat, canvis de categoria, passos a diferent nivell i interrupcions reals. La correcció correspon a l'edició de la font preparada, no a una superposició posterior que n'amagui la causa.

L'algorisme `Fix geometries` intenta produir geometries vàlides, però no coneix el significat territorial. Una reparació pot convertir una peça en multipart, separar lòbuls, descartar components de dimensió inferior o modificar vèrtexs. S'ha d'aplicar sobre una còpia, després d'identificar l'error, i comparar nombre d'entitats, tipus, parts, àrea o longitud i localització de les modificacions.

Les geometries buides i les geometries nul·les tampoc no són el mateix. Una fila amb geometria nul·la no té cap geometria associada; una geometria buida pot conservar un objecte geomètric sense punts després d'una operació. Cap de les dues pot satisfer predicats ordinaris com una geometria present. Cal comptar-les abans i després, perquè algunes eines les ometen i altres en conserven la fila.

### Col·lapse dimensional

La intersecció matemàtica pot tenir una dimensió inferior a la de les entrades. Dos polígons que només comparteixen una aresta tenen una intersecció lineal; si només comparteixen un vèrtex, és puntual. Dos trams que se superposen comparteixen una línia, mentre que dos trams que es creuen comparteixen un punt. El predicat `intersects` pot ser cert en tots aquests casos, però l'àrea comuna pot ser zero.

Un algorisme de superposició orientat a polígons pot conservar només components poligonals i ometre contactes lineals o puntuals, o bé oferir una opció per mantenir dimensions inferiors. Una sortida buida d'intersecció poligonal no implica necessàriament que les capes siguin `disjoint`: poden tocar-se sense compartir superfície. El tipus esperat de la sortida s'ha de comprovar abans d'interpretar-ne el recompte.

Una transformació també pot eliminar parts estretes o crear una geometria multipart. Si l'anàlisi necessita els contactes, s'han de consultar amb el predicat o extreure la dimensió adequada; no s'ha de forçar una superfície artificial mitjançant un `buffer` només perquè l'eina de polígons retorni una capa buida.

### Fragments estrets, escletxes i solapaments

Els **fragments residuals** o *slivers* són polígons molt estrets o petits que sovint apareixen quan se superposen límits que pretenen representar la mateixa frontera amb coordenades diferents. També poden ser entitats territorials reals. La mida sola no permet classificar-los com a error: cal relacionar forma, font, escala, exactitud i fenomen.

Una unió entre dues cobertures nominalment coincidents fa visibles aquests desacords com franges amb atributs només d'una capa. Eliminar-les amb un llindar d'àrea pot esborrar illes, corredors o parcel·les legítimes. Ajustar una capa a l'altra decideix quina geometria actua com a referència i pot alterar superfícies. Qualsevol neteja necessita una tolerància justificada i una taula de canvis.

Les escletxes i solapaments interns també poden provocar doble comptatge o àrea sense assignar. Dissoldre amaga els límits interns, però no explica si l'entrada era una partició coherent. Abans de dissoldre convé comprovar les regles «no se solapa» i «no deixa buits» només dins del domini on siguin conceptualment exigibles.

### Índexs espacials i verificació exacta

Un **índex espacial** accelera la cerca de parelles candidates. Estructures habituals com els arbres R organitzen caixes envolupants perquè l'algorisme no hagi de comparar exhaustivament cada geometria amb totes les altres. Si dues caixes no se superposen, les geometries tampoc no poden intersectar-se; si les caixes se superposen, encara cal avaluar el predicat exacte.

L'índex modifica el rendiment, no la semàntica esperada. Una caixa envolupant que interseca una altra pot contenir geometries disjuntes, especialment amb formes còncaves o forats. Per això una selecció basada només en caixes dona candidats, no una resposta final a `within`, `touches` o `overlaps`. Els algorismes de QGIS acostumen a gestionar aquesta fase internament, però en conjunts grans convé comprovar que les fonts admeten o tenen índex i evitar reconstruir consultes espacials costoses fila per fila {% cite qgisUserGuide344 %}.

Crear un índex no corregeix geometries, CRS ni filtres. Tampoc no ha de canviar el conjunt de resultats d'una mateixa operació exacta. Si executar amb una còpia indexada altera les coincidències, cal investigar diferències de dades, proveïdor, precisió o paràmetres en lloc d'atribuir-ho a una «aproximació» acceptable de l'índex.

### Invariants i balanços

Els controls més útils deriven de propietats que l'operació no hauria de violar. Un retall no ha d'afegir superfície o longitud a l'entrada; una intersecció ha de quedar dins de totes dues capes; una diferència i la part comuna haurien de reconstruir l'entrada, llevat de fronteres de dimensió inferior i toleràncies numèriques; una dissolució no ha de crear cobertura fora de la unió dels membres del grup.

Els balanços s'han d'aplicar a mesures recalculades sobre les geometries resultants, no a camps antics copiats. Les petites diferències de coma flotant necessiten una tolerància definida segons escala i CRS, però una tolerància no pot convertir-se en permís per ignorar qualsevol discrepància. També cal comparar identificadors d'origen, nombre de parts i patró de nuls, perquè una àrea total correcta pot ocultar atribucions errònies.

::: table "Controls mínims de geoprocessament vectorial"
| Operació | Comprovació mínima |
| --- | --- |
| Buffer | Distància mostrejada, unitats, entitats sense sortida i àrea dissolta no superior a la suma individual |
| Retall | Cap geometria fora de la màscara i superfície o longitud que no augmenta |
| Intersecció | Camps de les dues fonts, fragments justificats i totals coherents |
| Diferència | Cap intersecció amb l'interior de la màscara i absència de fragments residuals inesperats; la frontera de tall es pot compartir |
| Diferència simètrica | Absència de la part comuna, procedència de les parts exclusives i efecte dels desajustos de límit |
| Unió | Extensió conjunta, patró de nuls i fragments estrets o solapaments |
| Dissolució | Nombre de resultats compatible amb `Keep disjoint features separate`, geometries multipart esperades, camps no resumits identificats i agregacions separades quan calgui |
| Tessel·lació | Extensió, mida i origen documentats, suma de recomptes i efectes de vora |
:::

Reparar geometries sense diagnòstic no substitueix aquests controls.

Primer s'ha d'identificar l'error i comparar recompte, tipus i superfície abans i després de la correcció.

## Activitats

### Comprovació: quatre operacions sobre el mateix cas

Cal aplicar selecció espacial, unió espacial, retall i intersecció a les mateixes capes simples. Per a cada sortida s'han de comparar geometria, nombre de files i camps. L'objectiu és predir l'efecte abans d'executar-lo.

### Pràctica guiada: sensibilitat d'una distància

Es crearan buffers de 100, 300 i 500 m, amb i sense dissolució, sobre una mateixa xarxa. Cal representar com canvien superfície i nombre d'entitats relacionades, i explicar per què cap distància no s'ha d'interpretar com un temps de recorregut sense un model de xarxa.

### Micropràctica 4: geoprocessament vectorial

::: table "Contracte de la micropràctica 4"
| Component | Requisit |
| --- | --- |
| Entrades | Límit del municipi assignat, xarxa viària seleccionada, portals o equipaments i una capa capturada a la micropràctica 2 |
| Operacions mínimes | Extracció, validació, dos buffers justificats, selecció espacial i una superposició geomètrica |
| Resultats | Capes de criteri i resultat final dins del GeoPackage, amb superfícies recalculades |
| Evidències del diari | Pregunta, llindars, CRS, ordre d'operacions, recompte i àrea després de cada pas i limitacions |
| Comprovacions | Distàncies en metres, geometries vàlides, coincidències múltiples identificades i inspecció d'una mostra |
| Fitxers que cal conservar | GeoPackage, projecte `.qgz`, diari i capes intermèdies necessàries per auditar el flux |
:::

Com a ampliació, el resultat es pot agregar sobre una malla quadrada o hexagonal amb dues mides de cel·la. La comparació ha d'explicar quins patrons es mantenen i quins depenen de la tessel·lació.
