---
layout: manual-chapter
title: Model vectorial i digitalització
description: Disseny i captura d'entitats vectorials amb criteris d'escala, atributs, topologia i control de qualitat.
lang: ca
ref: manual-vector-model-digitizing
profiles: [unaltremanual]
content_status: draft
permalink: /ca/chapters/model-vectorial-digitalitzacio/
weight: 50
part: Continguts
manual_references: true
---

Digitalitzar no és calcar una imatge. És decidir quins objectes es representaran, amb quina geometria, quins atributs els descriuran i quines relacions s'han de preservar. La qualitat d'una capa comença abans del primer vèrtex: depèn de la finalitat, la font, l'escala de captura i les regles que defineixen què es considera una entitat correcta.

El model vectorial representa fenòmens mitjançant **punts, línies i polígons** associats a registres d'una taula. Aquestes primitives permeten descriure objectes discrets, xarxes i límits, però continuen sent abstraccions. Un carrer pot modelar-se com un eix lineal per estudiar connectivitat o com una superfície per calcular ocupació; cap representació no és completa fora de la pregunta que l'ha motivada.

>>>>> En acabar el capítol, cal poder planificar, capturar i validar una capa vectorial adequada per a una finalitat territorial explícita.
>>>>>
>>>>> - Justificar l'ús de punts, línies o polígons segons fenomen, escala i anàlisi prevista.
>>>>> - Dissenyar camps, identificadors, tipus, unitats, dominis i política de valors nuls abans de capturar.
>>>>> - Aplicar ajust automàtic, traçat i edició topològica segons regles definides.
>>>>> - Distingir validesa geomètrica, coherència topològica, exactitud posicional i qualitat temàtica.

## Entitats, geometries i atributs

Una **entitat** combina identitat, geometria i atributs. La geometria situa i dona forma a l'objecte; els atributs n'expressen propietats; i un identificador estable permet relacionar-lo amb altres observacions. Una capa vectorial ha de declarar un tipus geomètric i un CRS, però també necessita un esquema coherent perquè les files representin unitats comparables {% cite isoSimpleFeatureAccess2004 ogcSimpleFeatures2011 %}.

Convé distingir l'entitat de cadascuna de les seves representacions. L'entitat és la unitat que el conjunt de dades afirma que existeix o que s'ha observat: un fanal, un tram de carril bici o una instal·lació solar. La **geometria** és només el valor espacial associat a aquesta unitat, de la mateixa manera que `estat` o `data_obs` són valors temàtics. Un registre pot conservar la identitat encara que la geometria sigui temporalment desconeguda, i una mateixa entitat pot tenir representacions diferents segons la versió o l'escala. Per contra, dues geometries iguals no demostren que hi hagi una sola entitat: poden ser duplicats accidentals, observacions en dates diferents o objectes superposats legítimament.

La **unitat d'observació** determina què significa cada fila. Si una fila representa una instal·lació solar, totes les plaques separades que pertanyen a la mateixa instal·lació poden formar una geometria multipart. Si una fila representa una placa, cada peça necessita una entitat i un identificador propis. Cap eina geomètrica no pot resoldre aquesta decisió semàntica després de la captura. Abans de crear la capa cal escriure una frase verificable del tipus «cada fila representa...» i comprovar que els camps, la geometria i les regles hi concorden.

Un punt té dimensió zero i representa una posició. Una línia és una seqüència ordenada de vèrtexs connectats per segments; els seus extrems o cruïlles poden actuar com a nodes d'una xarxa. Un polígon conté un anell exterior i pot tenir anells interiors. Les geometries també poden ser multipart quan una sola entitat està formada per peces separades.

En el model de geometries simples de l'OGC, un `Point` conté una única posició. Un `LineString` ordena dues posicions o més i interpola segments entre posicions consecutives. El primer i l'últim punt formen la frontera d'una línia oberta; si coincideixen, la línia és tancada. Un anell apte per delimitar un polígon ha de ser tancat i simple, és a dir, no s'ha d'autointersectar. La paraula **node** s'ha de reservar per a una posició a la qual el model atribueix una funció de connectivitat; qualsevol vèrtex intermedi d'una línia no és necessàriament un node de xarxa.

Un `Polygon` representa una superfície plana delimitada per un anell exterior i zero o més anells interiors. Els anells interiors representen forats: una illa construïda dins d'una zona verda no és automàticament un forat, perquè pot ser una altra categoria que exigeixi una entitat pròpia. Els anells tampoc no són entitats independents ni línies de la capa. El polígon inclou el seu interior i la seva frontera per a moltes operacions de cobertura, però els predicats topològics distingeixen aquestes parts; per això un punt sobre la vora no produeix necessàriament el mateix resultat que un punt estrictament interior.

La jerarquia de geometries parteix d'un tipus general i en separa les famílies puntuals, lineals, superficials i de col·lecció. Dins de cada família, els tipus simples i múltiples indiquen com s'estructura un únic valor geomètric; no defineixen què constitueix una entitat ni obliguen a barrejar famílies en una mateixa capa.

Punts, línies i polígons són abstraccions topològiques, no símbols. Un punt no té longitud ni superfície, una línia no té amplada i la superfície d'un polígon no depèn del color del farciment. Un carrer dibuixat amb una línia de tres mil·límetres continua sense representar les voreres ni la calçada ocupada. Si l'anàlisi necessita amplada, aquesta propietat s'ha d'incorporar com a atribut, derivar-se mitjançant una hipòtesi explícita o representar-se amb una superfície adequada.

>> El símbol no altera la geometria: un marcador gran continua sent un punt i una línia gruixuda no es converteix en una superfície. Les mesures i els predicats operen sobre les coordenades, no sobre l'aparença del mapa.

::: table "Elecció de geometria segons la pregunta"
| Fenomen | Representació possible | Pregunta que permet respondre | Limitació principal |
| --- | --- | --- | --- |
| Fanal | Punt | On és i a quina distància queda d'un tram? | No representa la base ni l'àrea real il·luminada |
| Carril bici | Línia central | Quins trams connecten i quina longitud tenen? | No representa l'amplada de la infraestructura |
| Plaques solars | Polígon | Quina superfície ocupen sobre una coberta? | El límit depèn de la resolució i la visibilitat de la font |
| Edifici | Punt o polígon | Localització regional o superfície urbana | La representació adequada canvia amb escala i finalitat |
| Riu | Línia o polígon | Connectivitat de la xarxa o superfície de la llera | Cap opció no descriu simultàniament tots els processos fluvials |
:::

### Geometries simples, multipart i col·leccions

En llenguatge quotidià, «geometria simple» pot semblar sinònim de geometria amb pocs vèrtexs, però a l'estàndard té un sentit topològic. Un punt és simple. Una línia és simple quan no passa dues vegades pel mateix punt, amb l'excepció permesa que els extrems coincideixin en una línia tancada. Una línia amb només tres segments pot no ser simple si s'autointersecta, mentre que una línia de milers de vèrtexs pot ser simple. Per als polígons, la propietat operativa central és la **validesa**: els anells han de formar una superfície coherent i no es poden creuar de manera que l'interior quedi ambigu {% cite ogcSimpleFeatures2011 %}.

El prefix `Multi` no significa «molts vèrtexs».

Un `MultiPoint` agrupa punts, un `MultiLineString` agrupa línies i un `MultiPolygon` agrupa polígons dins d'un únic valor geomètric. Una illa amb centenars de vèrtexs continua sent un `Polygon`; un municipi format pel territori principal i diversos enclavaments pot ser un `MultiPolygon`. Les parts comparteixen una sola fila d'atributs. Si cada part necessita categoria, data o responsabilitat diferents, probablement han de ser entitats separades relacionades per un identificador de grup.

Una capa declarada com a tipus multipart pot contenir entitats amb una sola part sense que hi hagi contradicció: aquesta part queda embolcallada en una estructura múltiple. El pas invers no sempre és segur. Convertir multipart a parts simples duplica els atributs i exigeix decidir si es conserva un identificador comú, si es creen identificadors nous i com es tracten mesures totals. Agrupar entitats simples en multipart pot ocultar diferències d'atributs o convertir objectes només pròxims en una unitat falsa. Les eines `Multipart to singleparts` i `Collect geometries` executen una transformació estructural; no decideixen què constitueix una entitat.

Una `GeometryCollection` pot barrejar geometries de famílies diferents, per exemple un punt i una línia. És útil com a valor de resultats o intercanvis generals, però no equival a una capa homogènia de punts, línies o polígons. Moltes eines de QGIS i formats de treball esperen una família única perquè les operacions i la simbologia siguin previsibles. Si arriba una col·lecció heterogènia, cal inventariar-ne els components i separar-los amb criteri abans de forçar-los dins d'una capa.

També s'han de distingir tres absències. Un valor geomètric **nul** indica que la fila no té geometria assignada. Una geometria **buida**, com `POINT EMPTY`, és un objecte geomètric tipat sense cap posició. Una part col·lapsada pot sorgir quan una operació elimina tots els vèrtexs útils. Aquestes situacions poden ser admeses tècnicament i continuar sent inacceptables per a una capa d'inventari que exigeix localització. La restricció pertany a l'esquema i al control de completesa, no al color amb què QGIS mostra la fila.

### Coordenades, dimensió i corbes

Cada posició conté una tupla de coordenades. Les formes habituals són `XY`, `XYZ`, `XYM` i `XYZM`: Z acostuma a representar una coordenada vertical i M, una mesura associada al recorregut, com un punt quilomètric o un temps. El significat no queda determinat per la lletra. Una Z pot ser altura el·lipsoidal, cota ortomètrica, profunditat o un valor local, i una M només és interpretable si se'n documenten unitat, origen i sentit. Declarar una capa com a `PointZ` no crea una referència vertical ni converteix una observació bidimensional en tridimensional.

La **dimensió de coordenades** és diferent de la **dimensió topològica**. Un punt és de dimensió topològica 0, una línia d'1 i una superfície de 2, encara que les seves posicions siguin `XYZ`. Aquesta distinció intervé en predicats com `crosses`: una línia pot travessar una altra en un punt, mentre que dos polígons se solapen en una àrea. Gran part del model de geometries simples i molts algorismes de QGIS avaluen aquestes relacions en el pla XY; les Z es poden conservar, interpolar o perdre sense participar en la decisió topològica. Dos carrils que comparteixen X i Y però circulen per cotes diferents poden aparèixer intersectats geomètricament i no estar connectats funcionalment.

La M tampoc no substitueix la segmentació d'una xarxa. Permet localitzar esdeveniments al llarg d'una geometria si les mesures són monotòniques i comparteixen una referència, però una cruïlla continua necessitant nodes i regles de connectivitat. Abans d'utilitzar Z o M s'ha de verificar que el format, el proveïdor, l'eina d'edició i cada procés posterior en conserven els valors. Una exportació que manté XY i descarta M pot obrir-se sense avisos visibles i haver perdut la capacitat de localitzar incidències per quilometratge.

QGIS també pot treballar amb determinades geometries corbes. Una corba circular no és equivalent a una polilínia amb molts segments: la primera conserva una definició paramètrica i la segona n'és una aproximació. El suport varia segons el proveïdor i l'algorisme, i alguns formats o processos segmenten les corbes en exportar-les. Si la curvatura exacta és necessària, cal definir una tolerància de segmentació, conservar l'original i comparar longitud, superfície i desviació màxima després de la conversió. Per a la micropràctica, les geometries lineals ordinàries són suficients i eviten una dependència que no aporta informació observable a la font.

### WKT, WKB, EWKT i EWKB

WKT (*Well-Known Text*) i WKB (*Well-Known Binary*) són representacions serialitzades d'una geometria. Permeten transferir-ne el tipus i les coordenades entre motors, però no són formats complets de capa: no contenen per si sols la resta de camps, els dominis, la simbologia, la procedència ni totes les metadades del CRS. Una columna WKT dins d'un CSV continua necessitant una convenció que identifiqui el CRS i vinculi cada text amb la fila correcta.

El WKT geomètric tampoc no s'ha de confondre amb el WKT utilitzat per descriure un CRS. Comparteixen el principi d'una codificació textual normalitzada, però tenen gramàtiques i objectes diferents: `POINT (1 2)` representa una geometria, mentre que una definició WKT2 de CRS descriu eixos, datum, unitats i altres components de la referència.

El WKT és llegible i resulta adequat per inspeccionar casos petits. Els parèntesis expressen la jerarquia de posicions, anells i parts:

```text
POINT (344469 4551807)
LINESTRING (344460 4551800, 344470 4551810, 344490 4551805)
POLYGON ((0 0, 8 0, 8 6, 0 6, 0 0),
         (2 2, 2 4, 4 4, 4 2, 2 2))
MULTIPOLYGON (((0 0, 2 0, 2 2, 0 2, 0 0)),
              ((5 0, 7 0, 7 2, 5 2, 5 0)))
```

El primer anell del polígon és exterior i el segon delimita un forat. En el multipolígon, cada nivell addicional de parèntesis separa anells, polígons i el conjunt. L'exemple no declara cap CRS; les primeres coordenades només són plausibles com a UTM i no s'han d'interpretar com a `EPSG:25831` sense metadades. L'ordre de les posicions d'una línia també és significatiu perquè defineix inici, final i sentit, encara que la forma dibuixada sembli la mateixa en invertir-lo.

El WKB codifica la mateixa classe d'estructura en bytes. Inclou informació sobre ordre dels bytes, tipus geomètric, recomptes i coordenades, de manera que és compacte i ràpid d'interpretar per una base de dades, però no és apropiat per editar-lo manualment. Mostrar un WKB com una cadena hexadecimal només és una representació textual dels bytes. Convertir WKT a WKB no millora l'exactitud ni valida la geometria; canvia la codificació.

Les sigles EWKT i EWKB designen variants **ampliades** associades sobretot a PostGIS, l'extensió espacial del sistema gestor de bases de dades PostgreSQL. Poden incorporar un identificador de referència espacial i convencions addicionals de dimensionalitat. Per exemple, és habitual trobar `SRID=25831;POINT(344469 4551807)` com a EWKT. Aquest prefix és útil dins d'un contracte que el reconeix, però no forma part del WKT simple interoperable de l'OGC i un lector genèric el pot rebutjar. De manera semblant, l'EWKB no s'ha de presentar com si qualsevol lector WKB hagués d'interpretar-ne les marques pròpies {% cite postgisManual364 %}.

Les revisions i implementacions de WKT/WKB tampoc no tracten Z i M exactament igual. Un productor pot escriure `POINT Z (...)`, utilitzar codis de tipus ampliats o mantenir la dimensionalitat en metadades laterals. La prova correcta consisteix a acordar el perfil d'intercanvi i tornar a llegir una mostra `XY`, `XYZ`, `XYM`, multipart, buida i nul·la amb el receptor. Assignar un SRID dins d'una serialització declara una interpretació; no transforma les coordenades ni certifica que el codi sigui l'adequat.

>>>> **Una geometria no és una entitat completa.** WKT, WKB, EWKT i EWKB poden conservar la forma i, segons la variant, part de la referenciació, però no substitueixen l'esquema, la identitat, la procedència ni les regles de qualitat de la capa.

## Escala de captura i qualitat de la font

L'escala de captura expressa el nivell de detall coherent amb la font i l'ús previst; no és el nivell de zoom de la pantalla. Ampliar una ortofoto no revela detalls que el sensor no ha registrat. Afegir vèrtexs sobre contorns borrosos només crea precisió aparent.

La representació s'ha de derivar de la finalitat. Un edifici pot ser un punt en un inventari regional, un polígon de petjada en un càlcul d'ocupació o diverses superfícies si es distingeixen cossos constructius. El centroide d'una petjada no és necessàriament l'accés principal, i un punt capturat sobre una etiqueta cartogràfica no és necessàriament el centre geomètric. Per a cada capa cal indicar tant el fenomen com la **referència geomètrica**: centre aproximat, accés, eix, límit visible, petjada o una altra convenció reproduïble.

L'escala numèrica relaciona una distància a la representació amb la distància al terreny. En una font a `1:5.000`, un mil·límetre representa cinc metres; això ajuda a interpretar el detall dibuixable, però no converteix automàticament cinc metres en l'error de totes les entitats. Una ortofoto digital tampoc no té una escala fixa mentre es visualitza. Té una mida de píxel al terreny, un procés d'ortorectificació i unes especificacions d'exactitud. QGIS permet ampliar-la a `1:100`, però la informació original no augmenta.

La **unitat mínima cartografiable** defineix la dimensió mínima que el projecte decideix representar. Depèn del fenomen, la font, la simbologia i el producte final. La generalització pot seleccionar, agregar, simplificar, desplaçar o canviar la dimensió dels objectes. Si s'aplica sense considerar els límits compartits, pot generar buits i solapaments.

No hi ha una fórmula universal que fixi la unitat mínima per a qualsevol projecte. Una marca puntual pot fer visible un fanal que seria massa petit per dibuixar-ne la petjada, mentre que una clapa de vegetació inferior al llindar acordat es pot agregar a la categoria veïna. La fitxa de captura ha de concretar llindars separats per a longitud, superfície i separació quan siguin necessaris, i ha d'indicar què es fa amb els elements inferiors: s'ometen, s'agrupen, es representen amb una altra geometria o es conserven perquè tenen interès excepcional.

La generalització també afecta el significat. Simplificar elimina vèrtexs; suavitzar els desplaça per reduir canvis bruscos; agregar fusiona objectes; col·lapsar transforma una superfície en línia o punt; i desplaçar evita conflictes de representació. Aplicar una simplificació independent a dos polígons adjacents pot crear fronteres diferents. Si una cobertura ha de continuar sent una partició, el procediment ha d'operar sobre els límits compartits o reconstruir i validar la cobertura després del canvi.

La mida del píxel d'una ortofoto no equival a l'exactitud posicional de la capa digitalitzada. Cal distingir resolució espacial, exactitud declarada de la font, ambigüitat del límit observat i precisió de la captura. Els límits jurídics, cadastrals o administratius no s'han de deduir visualment d'una fotografia quan existeix una font oficial.

Una vora de coberta ben contrastada es pot identificar amb menys ambigüitat que la capçada difusa d'un arbre sobre la mateixa imatge. Els objectes elevats també poden presentar desplaçament residual o ocultar la base, i una ombra no forma part de la petjada. La data introdueix una altra incertesa: una ortofoto anterior a una reforma pot ser nítida i estar desactualitzada. La captura ha de separar la qualitat del producte d'origen, la interpretació del fenomen i l'error introduït pel traçat.

Quan la font és un servei cartogràfic, s'han de conservar productor, títol de la capa, data o edició, escala o resolució recomanada, CRS, llicència i URL estable si existeix. Una captura de pantalla o una tessel·la de mapa base no substitueix aquestes metadades. Si la font només serveix de context visual i no autoritza derivar dades, no es pot convertir en font de digitalització per conveniència tècnica.

Abans de capturar s'ha de preparar una fitxa amb finalitat, àmbit, font, data, CRS, rang d'escales, unitat mínima, geometria, esquema i regles de qualitat. Una prova pilot curta permet comprovar si aquestes decisions són aplicables abans de completar tota la zona.

La prova pilot ha d'incloure una zona fàcil i una d'ambigua. S'hi mesuren temps per entitat, densitat de vèrtexs, desacords entre operadors, proporció de valors desconeguts i errors detectats per les regles. Si dos operadors interpreten sistemàticament de manera diferent el final d'un carril bici o l'agrupació de plaques, falta una regla semàntica; augmentar el zoom o la tolerància d'ajust no resoldrà el desacord.

La fitxa també ha d'establir què no es pot afirmar. Una placa identificada sobre una coberta no prova potència, connexió a xarxa ni estat de funcionament. Un eix visible d'un carril no determina necessàriament el sentit de circulació. Registrar `desconegut` o un nul justificat és preferible a completar atributs per inferència no documentada.

## Disseny de la taula d'atributs

Els atributs s'han de definir mentre encara és possible modificar el model sense recodificar tota la capa. Cada camp necessita un nom, una definició, un tipus, una unitat, un domini i una política de valors nuls. Les categories observades s'han de separar de les interpretacions que no es poden verificar amb la font.

L'esquema comença amb la unitat d'observació i no amb una llista de columnes disponibles en una altra capa. Per a cada camp s'ha d'especificar si descriu el fenomen, la font, el procés de captura o el control. `tipus_fanal` descriu l'objecte; `font` i `data_font`, l'origen; `operador` i `data_captura`, el procés; i `estat_rev`, el control. Barrejar aquestes funcions en un camp `notes` dificulta les consultes i impedeix aplicar restriccions.

::: table "Diccionari abreujat per a una capa de fanals"
| Camp | Tipus | Significat | Control |
| --- | --- | --- | --- |
| `id_fanal` | Text | Identificador únic i estable | Obligatori i sense duplicats |
| `tipus` | Text | Categoria observada segons un domini definit | Llista de valors admesos |
| `estat` | Text | Estat observat en la data de camp | Valor controlat o nul justificat |
| `data_obs` | Data | Data de l'observació | Data vàlida, no text lliure |
| `font` | Text | Campanya, producte o registre de procedència | Obligatori |
| `observacio` | Text | Incidència que no encaixa en els camps anteriors | Ús excepcional i breu |
:::

Els tipus s'han d'escollir pel significat i per les operacions previstes. Un codi com `0017` és text encara que contingui dígits; una quantitat comptable és un enter; una mesura pot necessitar decimal i unitat; una data s'ha de conservar com a data si el proveïdor ho permet. Desar-ho tot com a text ajorna els errors: `2`, `10` i `9` s'ordenen de manera diferent com a cadenes, i variants com `sí`, `Si` i `1` no formen un booleà coherent.

Un **domini** defineix valors admesos. Pot ser una llista tancada, un interval numèric o una relació amb una taula de codis. Una llista curta com `operatiu`, `avariat`, `desconegut` es pot presentar amb un giny de mapa de valors. Un catàleg llarg i reutilitzat és més mantenible en una taula relacionada amb codi estable, etiqueta llegible, definició i vigència. Canviar una etiqueta no hauria d'obligar a recodificar totes les entitats si el codi conserva el mateix significat.

`NULL` indica absència de valor, però la causa pot ser diferent: no observat, no aplicable, desconegut o encara no comprovat. Si aquestes causes afecten l'anàlisi, cal representar-les amb un camp d'estat o un domini explícit en lloc d'inventar nombres sentinella. Una cadena buida no és necessàriament nul·la, zero no significa desconegut i `0 m` pot ser una mesura legítima. La política de nuls ha d'indicar quins camps són obligatoris i en quines excepcions es permet l'absència.

Un identificador no ha de dependre de la posició de la fila ni d'un `FID` que una exportació pot regenerar. Els codis s'han de conservar com a text quan tenen zeros inicials. Els dominis i restriccions de QGIS redueixen errors d'entrada, però no comproven si l'observació territorial és certa.

L'identificador estable ha de ser únic, no nul i immutable durant la vida prevista del conjunt. Pot ser una seqüència gestionada, un UUID o un codi compost si existeix una regla institucional que n'evita les col·lisions. Incorporar-hi una categoria mutable o una coordenada és arriscat: traslladar un fanal o corregir-ne el tipus no hauria de canviar totes les relacions històriques. El `fid` intern pot servir al proveïdor per editar la fila, però no és una clau pública si no se n'ha documentat l'estabilitat.

Les restriccions més habituals són **no nul**, **únic**, expressió de comprovació i clau forana. Un valor predeterminat accelera la captura, però no s'ha de confondre amb una observació: omplir automàticament `estat = operatiu` falsejaria els fanals que no s'han pogut inspeccionar. En canvi, una data de captura generada en crear la fila pot ser adequada si queda diferenciada de la data de la font. Una expressió pot comprovar que `altura_m >= 0` o que `data_obs <= current_date`, però necessita una regla per a excepcions legítimes.

QGIS pot definir restriccions, formularis, valors predeterminats, àlies i ginys dins del projecte o desar part de la configuració amb l'estil. La base GeoPackage també pot contenir restriccions reals de SQLite. No tenen el mateix abast: una advertència configurada només al `.qgz` pot desaparèixer quan la capa s'obre en un altre projecte, mentre que una restricció de base s'aplica a qualsevol escriptura que la respecti. Abans del lliurament s'ha de reobrir el GeoPackage en un projecte net i comprovar quines regles viatgen amb les dades {% cite qgisUserGuide344 %}.

La definició geomètrica forma part de l'esquema. Cal fixar família (`Point`, `LineString` o `Polygon`), admissió de multipart, dimensions Z/M i CRS. Crear una capa genèrica o més permissiva «per si de cas» trasllada la incertesa als processos posteriors. Si només s'admet un punt per fanal, una multipunt ha de ser rebutjada o investigada; si una instal·lació pot tenir cobertes separades, el multipolígon pot formar part explícita del contracte.

La superfície i la longitud es poden derivar de la geometria. No sempre cal emmagatzemar-les. Un camp calculat permanent queda obsolet quan s'edita la forma, tret que un mecanisme el recalculi. Si la mesura és una evidència vinculada a una versió concreta, es pot conservar amb el CRS, mètode, unitat i data de càlcul. Si només es necessita per visualitzar o filtrar, un camp virtual o una expressió evita duplicar informació, tot assumint que depèn del projecte i de la geometria actual.

### Preparar les capes a QGIS

La creació d'una capa no s'ha de reduir a escollir «punt, línia o polígon». En crear una taula nova al GeoPackage cal seleccionar el fitxer de treball correcte, donar un nom estable a la capa, declarar el tipus i les dimensions, escollir el CRS de captura i afegir els camps amb els tipus previstos. Tot seguit es configuren àlies, formularis, dominis, valors predeterminats i restriccions. Desar el projecte després d'aquest pas conserva la configuració de QGIS, però encara cal provar una alta, una modificació i un valor rebutjat.

Una prova d'esquema mínima crea una entitat vàlida, intenta repetir-ne l'identificador, deixa buit un camp obligatori, introdueix una categoria fora del domini i torna a obrir la capa. El resultat permet distingir una validació només visual d'una restricció efectiva. També s'ha de comprovar com s'exporten accents, dates, nuls i geometries multipart si hi haurà intercanvi amb un altre format.

Les tres capes de la micropràctica han d'estar separades perquè tenen unitats i regles diferents. No convé crear una única taula genèrica amb un camp `tipus_geometria`, ni una `GeometryCollection` que barregi fanals, carrils i plaques. Compartir camps de procedència no obliga a compartir esquema: es poden mantenir noms i dominis coherents o relacionar les capes amb una taula de fonts sense renunciar a la seva especificitat.

## Captura i edició controlades

Ajust automàtic (*snapping*)
: Aproxima un vèrtex a un vèrtex o segment existent dins d'una tolerància d'interacció.

Traçat
: Reutilitza un recorregut geomètric existent entre un punt inicial i un punt final.

Edició topològica
: Permet moure de manera coordinada elements que comparteixen un límit o un node.

Són mecanismes diferents i cap d'ells assegura que s'hagi triat l'objecte correcte.

La configuració ha de respondre a les regles de cada capa. Ajustar els extrems d'un carril bici als extrems d'altres trams pot preservar la connectivitat; ajustar-los a qualsevol vèrtex d'edifici pròxim seria un error encara que la tolerància fos petita. Per als fanals, l'ajust a altres fanals podria crear duplicats coincidents, mentre que l'ajust a un inventari oficial pot ser útil si la tasca consisteix a actualitzar-ne els atributs. Cal declarar quines capes actuen com a destinació, si s'ajusta a vèrtexs, segments o tots dos i quina relació s'espera obtenir.

La tolerància d'ajust s'ha d'adaptar a la densitat d'entitats, l'escala de treball i la pantalla. Un valor massa petit deixa microbuits; un valor massa gran pot connectar amb una entitat equivocada. Durant la captura convé revisar lots petits, emplenar els atributs quan la font encara és present i registrar les excepcions.

Una tolerància en píxels controla una distància d'interacció a la pantalla i manté una sensació semblant quan canvia el zoom, però representa distàncies diferents al terreny. Una tolerància en unitats de mapa representa una distància territorial estable i ocupa més o menys píxels segons l'escala. S'ha de provar en la zona més densa de la capa i comprovar l'indicador d'ajust abans de confirmar cada vèrtex; acceptar el punt proposat sense identificar-ne la capa i l'entitat pot crear una connexió falsa.

>>>> La tolerància d'ajust no és exactitud posicional. Només estableix a quina distància interactiva QGIS proposa una coincidència; no mesura l'error de la font ni justifica que dos objectes siguin el mateix.

L'ajust modifica la coordenada que s'introdueix durant una acció interactiva. No repara retroactivament els vèrtexs antics, no força que una línia tingui un node en tots els encreuaments i no manté per sempre la relació després d'una edició posterior. Si dues línies s'han d'unir, cal comprovar que comparteixen exactament l'extrem; si una nova línia acaba sobre el segment interior d'una altra, el model de xarxa pot exigir també partir aquesta altra línia o inserir-hi un node.

El **traçat** calcula un camí sobre segments existents entre un punt inicial i un de final i n'incorpora els vèrtexs a la geometria nova. Evita redibuixar un límit sinuós, però hereta qualsevol error o excés de detall de la font. També pot seguir el camí equivocat quan hi ha bifurcacions o geometries molt pròximes. Abans de tancar la nova entitat cal revisar el recorregut complet, i després cal verificar que la coincidència es manté amb una prova geomètrica, no només amb una línia visualment superposada.

L'**edició topològica** de QGIS ajuda a mantenir coincidències ja existents quan es mouen vèrtexs compartits. No converteix una capa de geometries independents (*spaghetti*) en una xarxa formal, no crea una taula de nodes i no aplica totes les regles territorials. L'opció d'evitar solapaments pot retallar la part d'un polígon nou que envaeix determinades capes, però només és apropiada quan el model prohibeix realment aquests solapaments. Si dues cobertures temporals o dos drets territorials poden coexistir, activar-la alteraria informació legítima.

Les eines de digitalització avançada afegeixen restriccions geomètriques com distància, angle, paral·lelisme o perpendicularitat. Serveixen per construir una forma segons mesures o alineacions conegudes; no fan més exacta una vora que només s'intueix en una ortofoto. Introduir un angle recte és defensable per a una placa rectangular ben identificada o a partir d'un plànol fiable, però no perquè l'edifici «sembli» ortogonal a una escala insuficient.

La interfície separa aquestes funcions en controls diferents. La barra d'**Autoensamblat** configura a quines capes i components es pot ajustar el cursor; la de **Digitalització** inicia i desa l'edició o captura entitats; la de **Digitalització avançada** agrupa transformacions i tècniques addicionals; i el panell homònim permet imposar coordenades, distàncies i angles durant una captura. Fer visibles els quatre elements ajuda a localitzar-los, però encara cal decidir quins són pertinents per a la regla que s'aplica.

![Interfície de QGIS amb les barres d'Autoensamblat, Digitalització i Digitalització avançada i el panell de Digitalització avançada identificats]({{ site.baseurl }}/assets/img/qgis/qgis-digitizing-tools.png "Les barres donen accés a famílies d'accions diferents; els controls del panell s'activen en iniciar una captura editable. Veure una eina no demostra que la geometria compleixi la regla del projecte."){: data-figure-width-web="56rem" data-figure-width-pdf="100%"}

Per treballar amb distàncies i angles territorials, la pràctica utilitza un CRS projectat adequat, `EPSG:25831`. El panell de digitalització avançada no s'ha d'interpretar com una calculadora mètrica sobre longitud i latitud: QGIS en limita les restriccions quan el llenç treballa amb coordenades geogràfiques. Canviar el CRS del projecte tampoc no millora una font ni transforma mesures aproximades en observacions exactes.

Els complements que ofereixen segmentació o assistència automàtica, incloses funcions presentades com a intel·ligència artificial, poden servir per explorar possibilitats, però no formen part del flux obligatori del curs ni constitueixen una recomanació institucional. Abans d'utilitzar-ne un cal revisar manteniment, llicència, dades enviades a tercers, model emprat i possibilitat de reproduir i validar el resultat. La sortida continua sent una hipòtesi que s'ha de contrastar amb la font i les mateixes regles que una captura manual.

### Preparar una sessió d'edició

Abans d'activar l'edició cal verificar que la capa correcta és editable, que la font original no se sobreescriu i que el projecte resol les rutes previstes. La capa de captura ha de destacar sobre la font sense ocultar-la: un farciment semitransparent per als polígons, una línia contrastada i símbols que mostrin els vèrtexs durant l'edició permeten veure errors sense confondre simbologia i geometria. Les capes de referència que no s'han de modificar poden quedar només de lectura.

La configuració d'ajust s'ha de provar amb casos deliberats: un vèrtex pròxim però que no s'ha d'utilitzar, un segment al qual sí que cal arribar i dues destinacions dins de la tolerància. Aquesta prova revela si l'ordre o la prioritat de les capes produeix resultats ambigus. La configuració s'ha de registrar amb les unitats, no només com «ajust activat», perquè `10 px` i `10 m` descriuen comportaments molt diferents.

Una sessió curta ha de tenir un àmbit identificable, com un carrer o un conjunt de cobertes. En acabar cada lot es desen les edicions i s'executen controls locals. Desar confirma una transacció o escriu els canvis al proveïdor, però no certifica la qualitat. També cal distingir desar les edicions de desar el projecte: el primer modifica les dades; el segon conserva la configuració, els estils i les referències.

### Capturar punts

Capturar un punt exigeix una convenció de posició. Per a un fanal es pot utilitzar el peu del suport observat al terreny, el centre visible de la base o la coordenada d'un receptor, però no alternar criteris segons la nitidesa de cada objecte. Si la capçada o l'ombra tapa la base, la geometria s'ha de marcar com a incerta o obtenir d'una altra font. La mida del marcador no justifica situar diversos fanals en un únic punt.

Els duplicats puntuals mereixen una prova específica. Dos punts amb coordenades iguals poden ser un duplicat de captura, dos elements superposats en altura o dues observacions temporals del mateix objecte. Una cerca geomètrica de coincidències ha d'anar seguida de la comparació d'identificadors, dates i unitat d'observació. Eliminar automàticament totes les geometries duplicades pot esborrar registres legítims.

Els atributs s'han d'emplenar mentre la font i el criteri utilitzat encara són visibles. Els valors predeterminats acceleren camps de procedència comuns al lot, però s'han de revisar abans de confirmar. Si no es pot identificar el tipus de fanal, el valor correcte és el codi acordat per a desconegut o un nul permès, no la categoria més freqüent.

#### Punts observats amb GNSS

Una coordenada capturada al camp pot provenir d'un receptor d'un **sistema global de navegació per satèl·lit** (GNSS, de l'anglès *Global Navigation Satellite System*). En l'ús corrent, *GPS* s'empra sovint com a nom genèric, però GPS és el sistema operat pels Estats Units; Galileo, GLONASS i BeiDou són altres sistemes GNSS. Cadascun disposa d'una constel·lació, i molts receptors utilitzen senyals de diversos sistemes alhora. Aquesta disponibilitat pot millorar la geometria de l'observació, però no converteix la coordenada mostrada en una posició exacta ni elimina la necessitat d'una convenció de captura {% cite euspaWhatGNSS2026 %}.

El receptor estima una **pseudodistància** multiplicant el temps aparent de propagació del senyal per la velocitat de la llum. Se'n diu pseudo perquè, entre altres errors, el rellotge del receptor no està perfectament sincronitzat amb els rellotges dels satèl·lits: aquest biaix temporal comú es tradueix en un error de distància. En el cas ideal, una solució tridimensional ha de determinar quatre incògnites —les coordenades X, Y i Z i el biaix del rellotge— i necessita almenys quatre mesures simultànies de pseudodistància a satèl·lits diferents. Mesures addicionals aporten redundància i poden millorar l'estimació, però no eliminen per si soles els errors de propagació o recepció {% cite sanzGNSSBasicObservables2011 %}.

La incertesa depèn de la geometria dels satèl·lits, que es pot resumir amb indicadors de dilució de la precisió (DOP), dels retards atmosfèrics, dels obstacles, de la vegetació i els edificis, dels errors de recepció múltiple causats per senyals reflectits, del receptor i l'antena, de la durada de l'observació i del mètode de correcció {% cite gpsGovAccuracy2026 sanzGNSSBasicObservables2011 %}. Un valor DOP favorable descriu només la geometria disponible i no és, tot sol, una estimació de l'error final. Un nombre elevat de satèl·lits o molts decimals tampoc no garanteixen exactitud. La qualitat s'ha de valorar respecte de l'escala i la finalitat de l'inventari, repetint o contrastant observacions amb una referència independent quan l'ús ho exigeixi.

Cada registre ha de conservar la data i l'hora, el CRS i el dàtum o marc de referència, la referència vertical si s'utilitza l'altura, el dispositiu, la posició de l'antena, el mètode, la durada, les correccions aplicades i un estimador de precisió o incertesa. Si la coordenada es transforma abans d'incorporar-la a la capa, convé conservar també l'observació original i documentar l'operació. La validació final ha de comprovar que el punt representa l'objecte definit, concorda amb les fonts de control dins de la tolerància justificada i és adequat per a l'anàlisi prevista.

### Capturar línies i xarxes

Una línia és ordenada. El sentit de digitalització pot determinar l'origen i la destinació, el costat esquerre i dret, el sentit de flux o l'increment d'una mesura M. Si aquests conceptes intervenen en l'anàlisi, la regla de sentit s'ha de fixar abans de capturar i es pot comprovar amb símbols de fletxa. Invertir una línia després modifica aquesta orientació, però no corregeix automàticament atributs com `des_de`, `fins_a` o pendent signada.

La segmentació ha de seguir esdeveniments del model, no la longitud còmoda per dibuixar. Un tram pot acabar en una intersecció connectada, un canvi de categoria, una interrupció física o el límit de l'àmbit. Afegir un vèrtex per seguir una corba no crea necessàriament un tram nou. En canvi, una cruïlla funcional pot requerir partir les línies perquè el motor de xarxa reconegui el node. Un pont sobre un altre vial s'ha de mantenir sense connexió si no hi ha accés entre nivells, encara que les línies es creuin en XY.

Els errors típics són l'extrem curt que no arriba al node, el tram que sobrepassa la intersecció, el segment duplicat, la línia de longitud nul·la i el pseudonode creat sense necessitat analítica. «Extrem penjant» descriu una configuració, no sempre un error: un cul-de-sac, l'inici d'un carril o el límit del conjunt poden acabar legítimament. La regla ha de distingir aquests casos amb atributs o excepcions documentades.

En reutilitzar una línia existent com a límit, el traçat conserva la coincidència inicial. Si després s'edita només una de les còpies sense edició topològica, la relació es perd. Quan el límit té identitat pròpia i s'ha de mantenir una sola vegada, pot ser necessari un model topològic o relacional més explícit que dues geometries redundants. Per a una capa senzilla de carrils, la verificació de nodes i continuïtat és suficient sempre que no s'afirmi que el GeoPackage conté una xarxa completa de rutes.

### Capturar polígons i límits compartits

Un polígon s'ha de traçar amb un anell exterior coherent i, només quan correspon semànticament, anells interiors. QGIS tanca l'anell en acabar la captura, però això no evita una autointersecció produïda per un ordre incorrecte de vèrtexs. Les eines d'anell creen un forat dins d'una superfície existent; les eines de part afegeixen una peça separada a la mateixa entitat. Confondre-les modifica tant la superfície com el significat.

En una partició territorial, cada punt de l'àmbit ha de pertànyer a la categoria prevista i els interiors no s'han de superposar. Redibuixar cada frontera dues vegades és una font d'escletxes i encavalcaments. El traçat, l'ajust a segments i l'edició topològica redueixen aquest risc, però la validació final encara ha de buscar buits, solapaments i parts estretes creades accidentalment. El fet que el color de fons no sigui visible entre polígons no és una prova topològica.

Per a objectes independents, la regla pot ser diferent. Les projeccions de dues cobertes es poden solapar en planta si són a nivells diferents, i dues zones de protecció poden coexistir. Una capa de plaques solars sobre cobertes no és necessàriament una cobertura exhaustiva ni una partició; la regla «sense buits» no hi té sentit. Sí que poden ser apropiades «cada polígon queda dins d'una coberta de referència» o «les parts d'una mateixa instal·lació no se solapen» si les fonts permeten comprovar-ho.

Les operacions de dividir, fusionar i remodelar tenen efectes sobre els atributs. Dividir una geometria pot duplicar els valors de la fila original, encara que una superfície total o un identificador únic ja no siguin vàlids per a les dues parts. Fusionar obliga a resoldre camps discordants. Remodelar conserva habitualment la fila però altera mesures derivades. Després de qualsevol d'aquestes accions s'han de revisar identitat, atributs, geometria i relacions, no només desar la nova forma.

En una xarxa lineal, els trams que s'han de connectar han de compartir coordenades als nodes. Una intersecció visual no sempre implica connexió: un pont i una carretera inferior poden creuar-se sense compartir node. En una cobertura poligonal, la reutilització de límits evita que dues entitats adjacents defineixin el mateix contorn de manera independent.

### Cicle de captura i revisió

El cicle operatiu és preparar, capturar un lot, revisar atributs, validar geometries i relacions, corregir i tornar a validar. Els lots petits permeten relacionar cada error amb l'acció que l'ha produït. La mida no ha de ser una xifra universal: deu polígons complexos poden requerir més revisió que cent punts simples. El criteri és que el lot es pugui inspeccionar abans de perdre el context de captura.

La revisió visual s'ha de fer a dues escales. Una escala pròxima a la de captura permet detectar vèrtexs sobrers, desviacions de la font i ajustos equivocats; una vista general revela discontinuïtats, densitats anòmales i zones omeses. Els controls automàtics afegeixen propietats invisibles, com duplicats exactes, identificadors repetits o anells autointersectats. Cap dels dos modes substitueix l'altre.

Per conservar traçabilitat no cal crear una còpia completa després de cada clic. Sí que cal mantenir l'original, establir fites recuperables abans de reparacions massives, registrar l'àmbit i la data de cada sessió i anotar incidències que afectin la interpretació. Si diverses persones editen el mateix fitxer GeoPackage mitjançant una carpeta sincronitzada, una convenció de lots no resol els conflictes d'escriptura; cal serialitzar el treball o utilitzar una base preparada per a concurrència.

## Geometria, topologia i altres dimensions de qualitat

Una geometria pot ser vàlida de manera individual i incomplir el model territorial. Dos polígons municipals sense autointerseccions poden deixar una escletxa entre ells; dues línies vàlides poden quedar desconnectades; un punt pot ser correcte però situar-se fora de la zona on el model l'admet.

Validesa geomètrica
: Avalua si un valor geomètric compleix les regles estructurals del seu tipus. En un polígon, els anells han de delimitar un interior interpretable, els forats han de quedar dins de l'exterior i les parts no s'han de solapar de manera incompatible.

Simplicitat
: Propietat relacionada però diferent, especialment útil per a línies; una línia autointersectada no és simple.

Topologia
: Descriu relacions que no depenen de distàncies exactes, com separació, contacte, intersecció, contenció o solapament.

Una geometria pot ser vàlida i simple i continuar tenint una coordenada posicionalment equivocada. El model de nou interseccions dimensionalment estès, DE-9IM, compara l'interior, la frontera i l'exterior de dues geometries i registra si cada intersecció és buida o té dimensió 0, 1 o 2. Predicats com `intersects`, `touches`, `within`, `contains`, `crosses`, `overlaps`, `equals` i `disjoint` resumeixen determinats patrons d'aquesta matriu {% cite ogcSimpleFeatures2011 %}.

El predicat s'ha d'escollir segons la frontera. Un punt estrictament dins d'un polígon compleix `within`; un punt sobre la vora pot complir `touches`, però no necessàriament `within`. `intersects` és més ampli perquè inclou qualsevol punt compartit. `overlaps` no és un sinònim general d'intersecció: s'aplica quan geometries de la mateixa dimensió comparteixen una part de l'interior i cap no conté completament l'altra. Aquestes diferències expliquen resultats aparentment contradictoris en seleccions espacials.

Una **regla topològica de conjunt** converteix una relació en un requisit del model. «Els polígons no s'han de solapar» compara entitats de la mateixa capa; «els fanals han de quedar coberts per l'àmbit municipal» compara dues capes; «els extrems dels trams han de coincidir excepte en finals justificats» combina geometria i atributs. El programari pot detectar candidats, però la definició de la regla i de les excepcions és responsabilitat del projecte.

![Quatre casos de captura vectorial: una escletxa i un solapament entre polígons, dos extrems de xarxa pròxims però desconnectats i un conjunt correcte amb frontera i node compartits]({{ site.baseurl }}/assets/quarto/04-model-vectorial-digitalitzacio/topology-capture-errors.qmd "La proximitat visual no prova una relació topològica: els buits, els solapaments i els extrems desconnectats s'han de detectar amb regles del model, mentre que una frontera o un node correctes comparteixen coordenades exactes."){: data-figure-width-web="52rem" data-figure-width-pdf="100%"}

::: table "Regles possibles segons el model"
| Capa o relació | Regla candidata | Excepció que cal preveure | Control complementari |
| --- | --- | --- | --- |
| Partició administrativa | Polígons sense solapaments ni buits dins de l'àmbit | Exclavaments o àrees sense assignació documentades | Comparar la unió amb el límit oficial |
| Instal·lacions independents | Polígons sense duplicats ni solapaments dins d'una mateixa coberta | Elements a cotes diferents o dates diferents | Revisar identificador, Z i data |
| Xarxa de carrils | Extrems connectats als nodes funcionals | Inicis, finals i interrupcions reals | Classificar extrems i revisar sentit |
| Torres i trams de cable | Cada extrem queda cobert per una torre i cada torre funcional divideix els trams | Terminals, passos sense connexió o elements a cotes diferents | Extreure extrems, creuar capes i comparar identificadors |
| Fanals i municipi | Punts estrictament interiors a l'àmbit de treball | Elements sobre el límit acceptats per la convenció del projecte | Contrastar amb font i tolerància posicional |
| Plaques i cobertes | Plaques cobertes per una coberta de referència | Desajust admissible entre fonts de dates diferents | Quantificar distància i revisar la imatge |
:::

Les regles poden relacionar capes diferents. En una xarxa aèria simplificada, una capa puntual representa les torres i una capa lineal, els trams de cable. Cada extrem d'un tram ha de coincidir amb una torre, excepte en terminals documentats; si una torre intermèdia representa un canvi de connectivitat, el cable s'hi ha de dividir en dos trams. Un punt pròxim a l'extrem o dibuixat sobre una línia contínua no compleix necessàriament aquests contractes.

![Relacions entre una capa puntual de torres i una capa lineal de trams: extrems coincidents, segmentació en una torre intermèdia i dos candidats a error]({{ site.baseurl }}/assets/quarto/04-model-vectorial-digitalitzacio/network-cross-layer-topology.qmd "La validació entre capes ha de comprovar tant que cada extrem queda cobert per una torre com que les torres funcionals divideixen el cable en trams; la coincidència visual no substitueix aquestes dues proves."){: data-figure-width-web="54rem" data-figure-width-pdf="100%"}

Aquest control necessita més d'un predicat. Es poden extreure els extrems de les línies i comprovar-ne la cobertura per punts, però també cal detectar torres que cauen sobre l'interior d'un tram i decidir si l'han de segmentar. Les coordenades XY tampoc no expressen per si soles circuits, nivells o estat de servei: aquestes relacions requereixen atributs, identificadors i excepcions explícites.

Un conjunt *spaghetti* emmagatzema cada geometria independentment. Dues línies poden compartir coordenades, però no hi ha necessàriament un node persistent que mantingui la relació; dos polígons poden repetir una frontera sencera. L'ajust i l'edició topològica ajuden a conservar coincidències durant la captura, però no transformen aquest emmagatzematge en un model topològic explícit d'arcs, nodes i cares. Aquesta diferència és rellevant quan es promet manteniment automàtic de connectivitat, no per negar la utilitat de capes simples ben validades.

![Comparació entre geometries independents, amb fronteres i extrems repetits, i una topologia explícita que manté una frontera comuna i arcs relacionats per un node]({{ site.baseurl }}/assets/quarto/04-model-vectorial-digitalitzacio/arc-node-spaghetti.qmd "En un conjunt spaghetti les coincidències s'han de conservar i validar entre geometries independents; en un model topològic explícit, arcs, nodes i cares tenen identitat i mantenen les relacions declarades."){: data-figure-width-web="54rem" data-figure-width-pdf="100%"}

No són dos nivells de qualitat d'un mateix fitxer. Les geometries simples són adequades per a moltes capes de QGIS quan el projecte defineix i valida les relacions necessàries. Altres entorns poden requerir una topologia persistent, regles de xarxa i edició transaccional entre molts actius; [Octave GeoMedia](https://www.octave.com/products/geospatial-intelligence/geomedia) i [GE Vernova Smallworld](https://www.gevernova.com/software/products/geospatial-network-management-smallworld-gis) són exemples de famílies especialitzades on aquests models poden formar part de la gestió corporativa. Esmentar-les no converteix el capítol en formació sobre aquests productes ni implica que una capa GeoPackage senzilla n'hagi de reproduir l'arquitectura.

::: table "Dimensions diferents del control vectorial"
| Dimensió | Què comprova | Exemple d'error |
| --- | --- | --- |
| Representació | Adequació del tipus geomètric a la finalitat | Modelar com a punt una superfície que s'ha de mesurar |
| Validesa geomètrica | Estructura interna de cada geometria | Polígon autointersectat o línia de longitud nul·la |
| Coherència topològica | Relacions exigides entre entitats | Solapament en una partició o tram desconnectat |
| Exactitud posicional | Correspondència amb una referència adequada | Element desplaçat respecte d'un control independent |
| Qualitat temàtica | Correcció dels atributs | Placa solar classificada com una altra coberta |
| Completesa i vigència | Entitats absents, sobrants o desactualitzades | Fanals que no s'han capturat o que ja no existeixen |
:::

Les regles topològiques depenen del model. «Sense buits» només és apropiat si els polígons han de cobrir una extensió definida. Un extrem penjant pot ser un error en una canonada i una via sense sortida legítima. Un punt sobre el límit pot ser acceptable o no segons si la regla exigeix interior estricte o cobertura inclosa la frontera.

La tolerància utilitzada per detectar relacions no s'ha de convertir en una reparació indiscriminada. Si dos extrems són a `0,3 m`, una eina pot considerar-los pròxims, però moure'ls fins a coincidir només és correcte si la incertesa de la font i el model justifiquen que són el mateix node. Una tolerància superior a la separació entre carrils paral·lels pot fusionar connexions diferents. El valor s'ha de provar amb casos coneguts i registrar juntament amb el CRS i les unitats.

La validació ha de precedir qualsevol reparació automàtica. `Check validity` examina principalment la geometria individual; un validador topològic aplica relacions entre entitats. `Fix geometries` pot modificar formes i tipus, de manera que només s'ha d'aplicar quan l'error s'ha interpretat i sobre una còpia controlada.

Un control en QGIS comença amb l'esquema i els recomptes, continua amb la validesa individual i acaba amb les regles entre entitats. L'eina de comprovació de validesa ha de generar una sortida d'entitats vàlides, una d'invàlides i una capa o taula amb la causa i la posició dels errors quan el proveïdor ho permet. El validador topològic s'ha de configurar només amb regles pertinents i executar tant sobre els lots nous com sobre el conjunt final {% cite qgisUserGuide344 %}.

La reparació automàtica pot dividir un polígon, convertir una sortida en multipart, eliminar components col·lapsats o moure vèrtexs segons el mètode. Abans d'acceptar-la s'han de comparar nombre d'entitats i parts, tipus i dimensionalitat, superfície o longitud, identificadors i regles topològiques. Després cal tornar a executar el mateix control que havia detectat l'error i revisar la zona sobre la font. Si la diferència no es pot justificar, s'ha de restaurar la còpia anterior i corregir manualment o redefinir la font.

>>> Una reparació pot tancar tècnicament un anell eliminant una peça estreta i produir una geometria vàlida, però aquella peça podria representar un corredor territorial real. L'eina no coneix la intenció territorial: el canvi només s'accepta després de comparar-lo amb la font i les regles del projecte.

Els errors detectats necessiten un registre mínim amb identificador, regla, ubicació, causa interpretada, acció, responsable i estat. Una excepció acceptada no s'ha d'esborrar del recompte sense explicació: es marca com a justificada i es vincula a una raó, com un final real de xarxa. Aquesta separació entre errors oberts, corregits i excepcions permet repetir la validació sense discutir de nou cada cas.

## Un cas de captura a Vila-seca

La demostració reobre i amplia el mateix projecte extern `projecte_tig.qgz` i el mateix GeoPackage `dades_preparades/projecte_tig.gpkg` iniciats als capítols anteriors; no parteix d'un projecte buit ni crea un contenidor paral·lel. Abans d'editar, cal comprovar que les fonts es resolen, que no hi ha cap capa temporal pendent i que el punt de control incrustat `projecte_tig` del GeoPackage correspon al mateix estat que el fitxer extern.

El cas combina tres capes creades amb finalitats diferents. Els **fanals** es capturen com a punts a partir d'una observació adequada; els **carrils bici**, com a línies connectades; i les **plaques o conjunts de plaques solars**, com a polígons quan la font permet delimitar-ne la superfície. Les capes comparteixen l'àmbit i el CRS, però no l'esquema ni les regles topològiques.

La preparació comença amb una taula de fonts i tres frases d'unitat d'observació. Per als fanals, cada fila representa un suport individual i la posició correspon al peu observat o a la coordenada documentada de l'inventari. Per als carrils, cada fila representa un tram homogeni entre canvis de connectivitat o atributs. Per a les plaques, cada fila pot representar una superfície contínua visible; si es vol representar la instal·lació completa, les peces separades s'agrupen només quan una font permet afirmar que hi pertanyen.

El GeoPackage incorpora tres taules homogènies amb identificadors independents i camps comuns de font i data. Els identificadors es creen com a valors estables, únics i no nuls, i no es recalculen a partir del número de fila, la geometria o una categoria mutable: els capítols posteriors els necessitaran per a unions, diagnòstics i anàlisis. Abans de capturar es prova un registre vàlid i un d'invàlid de cada esquema, es configura l'ajust només a les capes necessàries i es fixa una escala de captura compatible amb la font. La zona pilot inclou una cruïlla, una coberta amb ombres i un fanal ambigu per comprovar les tres decisions que no resol l'eina.

Per als carrils bici, els extrems s'han d'ajustar quan existeix continuïtat física i s'han de mantenir separats quan la infraestructura s'interromp. Per als polígons solars, la generalització ha de ser coherent amb la resolució de la imatge i no ha d'inventar límits ocults. Per als fanals, l'activitat ha d'indicar si la posició prové de camp, d'un inventari o d'una imatge i quina exactitud es pot defensar.

La captura s'organitza per carrers o illes i cada lot es tanca amb una consulta d'identificadors i camps obligatoris. En fanals es busquen coordenades coincidents i distàncies anormalment petites; en carrils es classifiquen els extrems no connectats i els encreuaments sense node; en plaques es comproven validesa, duplicats, solapaments no admesos i relació amb la coberta. Els casos dubtosos no es corregeixen perquè encaixin visualment: queden identificats per revisar-los amb una font millor.

El control final combina recompte, identificadors, camps obligatoris, geometries invàlides, duplicats, extrems de xarxa i una mostra contrastada amb la font. Corregir un error obliga a repetir els controls afectats i a registrar la incidència al diari.

La mostra de contrast ha d'incloure casos ordinaris i extrems, no només les entitats més netes. El diari conserva la fitxa de captura, la configuració d'ajust amb unitats, els resultats de validació, les excepcions i una breu interpretació del que cada capa permet analitzar. Després del control es desa el mateix `projecte_tig.qgz`, s'actualitza el punt de control incrustat `projecte_tig` al mateix GeoPackage i es tanquen i reobren tots dos estats. El mapa final pot mostrar les tres capes, però la verificació es basa en les dades reobertes des del GeoPackage i en la conservació dels identificadors, no en una captura de pantalla del llenç.

## Activitats

### Comprovació: representar el mateix fenomen

Cal proposar dues representacions per a un riu, una carretera i un edifici, cadascuna associada a una pregunta diferent. L'activitat s'avalua per la justificació de la geometria i de l'escala, no per l'aparença del símbol.

### Pràctica guiada: classificació d'errors

Sobre una capa de prova s'identificaran una autointersecció, un buit, un solapament, un duplicat, un extrem penjant, un punt exterior i un atribut nul. Cada cas s'ha de classificar com a error geomètric, topològic, posicional o temàtic, i s'ha d'explicar si la regla depèn de la finalitat de la capa.

### Micropràctica 2: digitalització vectorial

La segona micropràctica lliurable aplica el model de punts, línies i polígons al municipi assignat. Si alguna categoria no és observable o no existeix al territori, s'ha de substituir per una entitat equivalent que permeti demostrar la mateixa decisió geomètrica.

::: table "Contracte de la micropràctica 2"
| Component | Requisit |
| --- | --- |
| Entrades | `projecte_tig.qgz` i `dades_preparades/projecte_tig.gpkg` existents, font oficial o observació documentada, límit de treball i criteris de captura |
| Operacions mínimes | Dissenyar tres esquemes, configurar dominis i ajust, capturar punts, línies i polígons i executar controls geomètrics i topològics |
| Resultats | Tres capes noves dins del mateix GeoPackage, amb identificadors estables i atributs complets |
| Evidències del diari | Finalitat de cada capa, font, escala, esquema, regles, incidències i correccions |
| Comprovacions | Identificadors únics, geometries vàlides, connectivitat justificada, absència de solapaments no admesos i mostra contrastada |
| Fitxers que cal conservar | El mateix GeoPackage actualitzat amb el punt de control incrustat `projecte_tig`, `projecte_tig.qgz` actualitzat i diari amb la taula de controls |
:::

El cas resolt de Vila-seca utilitzarà fanals, carrils bici i plaques solars. El lliurament ha de respondre al municipi assignat i no reproduir sense comprovació les geometries de la demostració.
