---
layout: manual-chapter
title: Models de dades, formats i referenciació
description: Models conceptuals, lògics i físics; representacions vectorials, ràster i 3D; formats i sistemes de referència per integrar dades geogràfiques.
lang: ca
ref: manual-data-structures-formats-crs
profiles: [unaltremanual]
content_status: approved
permalink: /ca/chapters/estructura-formats-referenciacio/
weight: 40
part: Continguts
manual_references: true
---

Dues capes poden representar el mateix territori i, tanmateix, no ser directament comparables. Una pot descriure municipis mitjançant polígons i una altra, elevacions mitjançant cel·les; poden utilitzar formats, resolucions, dates i sistemes de coordenades diferents. Integrar-les exigeix distingir què modelen, com s'estructuren, on s'emmagatzemen i què signifiquen les coordenades.

El nom d'un fitxer no resol aquestes preguntes. L'extensió informa del format, però no determina si la dada és adequada ni si el CRS declarat és correcte. Aquest capítol separa quatre conceptes que sovint es confonen: **model**, **estructura**, **format** i **sistema de referència de coordenades**.

>>>>> En acabar el capítol, cal poder diagnosticar l'estructura i la referenciació d'una capa, transformar-la amb criteri i completar la primera micropràctica.
>>>>>
>>>>> - Distingir els nivells conceptual, lògic i físic, i justificar representacions vectorials, ràster, de superfície o de volum segons la pregunta.
>>>>> - Triar un format segons edició, anàlisi, intercanvi i conservació.
>>>>> - Explicar què aporta un CRS i diferenciar assignació, transformació i visualització al vol.
>>>>> - Relacionar escala, resolució, precisió i exactitud amb l'ús previst.
>>>>> - Materialitzar en `EPSG:25831` les dues representacions municipals, validar el projecte `pr1` i preparar-ne els dos fitxers lliurables.

## Referenciació terrestre i coordenades

Una coordenada és el final d'una cadena de decisions, no una etiqueta enganxada a un punt. El punt pertany primer a la Terra física. Per descriure'l cal adoptar una superfície i un marc de referència, expressar-ne la posició mitjançant un sistema de coordenades i, si es necessita un mapa pla, aplicar una projecció. Només aleshores apareixen nombres com longitud i latitud en graus o est i nord en metres.

La cadena es pot llegir en cinc passos: **lloc sobre la Terra**, **marc i superfície de referència**, **coordenades geogràfiques**, **projecció cartogràfica** i **coordenades planes**. Un sistema de referència de coordenades (CRS) identifica les regles necessàries per interpretar el resultat. Ometre'l deixa nombres sense unitats, eixos ni àrea d'ús coneguts.

![Seqüència des d'una posició sobre la Terra fins a les coordenades geogràfiques i les coordenades UTM d'un mapa pla]({{ site.baseurl }}/assets/quarto/03-estructura-formats-referenciacio/geographic-projected-utm.qmd "Una posició es relaciona amb un marc terrestre, s'expressa amb longitud i latitud i es projecta dins d'un fus UTM per obtenir coordenades d'est i nord; cada pas necessita una referència explícita."){: data-figure-width-web="48rem" data-figure-width-pdf="95%"}

>>>> **Una parella de nombres no identifica una posició per si sola.** Cal conservar com a mínim el CRS, l'ordre dels eixos i les unitats; quan l'exactitud ho exigeixi, també l'operació i l'època de les coordenades.

### Geoposicionar, geocodificar i georeferenciar {#geoposicionar-geocodificar-georeferenciar}

Geoposicionar
: Determinar o registrar la posició geogràfica d'un objecte o una observació, per exemple a partir d'un receptor GNSS o d'un sensor que ja produeix coordenades.

Geocodificar
: Convertir un descriptor textual, com una adreça o un topònim, en una posició amb coordenades. La geocodificació inversa parteix de les coordenades i retorna un descriptor territorial probable.

Georeferenciar
: Establir la correspondència entre les posicions internes d'un conjunt de dades i posicions expressades en un CRS declarat. En una imatge sense referència, sol requerir punts de control i una transformació; en altres formats, la transformació ja pot estar integrada o conservar-se en un fitxer lateral.

Les tres operacions es poden encadenar, però no són sinònimes. Un receptor GNSS geoposiciona una observació sense geocodificar cap adreça; un servei pot geocodificar `carrer de Joanot Martorell, Vila-seca` i retornar un punt; i uns punts de control poden georeferenciar un plànol escanejat. Declarar el CRS que correspon a unes coordenades conegudes completa la seva interpretació sense moure-les, mentre que transformar-les a un altre CRS canvia els nombres per conservar la mateixa posició. Un *world file* aporta una transformació afí per georeferenciar una imatge, però no identifica tot sol el CRS.

### Latitud i longitud

La **latitud** mesura la separació angular respecte de l'equador. El rang vàlid és de `-90°` a `+90°`: el nord és positiu i el sud, negatiu. La **longitud** mesura la separació angular respecte del meridià d'origen. Habitualment s'expressa de `-180°` a `+180°`: l'est és positiu i l'oest, negatiu. Els meridians `180° E` i `180° O` coincideixen; als pols, una longitud concreta no diferencia la posició. Alguns sistemes utilitzen longituds de `0°` a `360°`, de manera que cal conèixer la convenció abans de comparar valors.

Els graus decimals i els graus, minuts i segons (GMS) expressen el mateix angle. En GMS, els minuts i els segons han de complir `0 <= valor < 60`. El signe i l'hemisferi no s'han de contradir: `41° 06′ 09,5″ N` és vàlid, però `41° 61′ N` no ho és i `-41° N` barreja dues convencions. Per convertir un valor, es calcula `graus + minuts / 60 + segons / 3600` i s'aplica signe negatiu al resultat complet si és sud o oest.

Per exemple, `41° 06′ 09,5″ N` equival aproximadament a `41,1026389°`, i `1° 08′ 51,3″ E`, a `1,1475833°`. Una longitud de `1° 08′ 51,3″ O` seria `-1,1475833°`. Els decimals indiquen com s'ha escrit el nombre, no l'exactitud amb què s'ha observat la posició.

En llenguatge geogràfic és habitual dir **latitud i longitud**, però molts formats i programes escriuen primer X i després Y, és a dir, longitud i latitud. L'ordre forma part del contracte. No s'ha d'invertir una parella fins que s'hagin comprovat la definició del CRS, el format i l'eina que la llegeix.

### Coordenades geogràfiques i projectades

Un CRS geogràfic situa punts sobre un el·lipsoide amb coordenades angulars, normalment longitud i latitud en graus. Els graus no són metres: la longitud terrestre d'un grau de longitud disminueix cap als pols i la d'un grau de latitud tampoc no és exactament constant. Es poden calcular distàncies geodèsiques sobre l'el·lipsoide, però no s'ha d'interpretar una diferència de graus com una distància plana.

Un CRS projectat transforma una part de la superfície corba en un pla i produeix coordenades cartesianes, habitualment en metres o peus. Això facilita moltes mesures i operacions, però cap projecció no conserva alhora totes les distàncies, àrees, direccions i formes sobre tota la Terra. La projecció i la seva **àrea d'ús** s'han de triar segons el territori i la propietat que interessa mesurar.

### UTM, fus, hemisferi i MGRS

El sistema **Universal Transversa de Mercator** (UTM) divideix el món entre aproximadament `80° S` i `84° N` en seixanta fusos de `6°` de longitud. Cada fus aplica la Transversa de Mercator al voltant d'un meridià central. El fus 31 s'estén convencionalment de `0°` a `6° E`, té el meridià central a `3° E` i cobreix Catalunya. El número de fus i l'hemisferi no basten encara per definir el CRS: també cal el marc geodèsic, com ETRS89 a `EPSG:25831` {% cite realDecreto1071_2007 %}.

Les coordenades UTM ordinàries són **est** (`E`) i **nord** (`N`) en metres. Al meridià central s'aplica un factor d'escala de `0,9996` i un fals est de `500.000 m`. A l'hemisferi nord, el fals nord és `0 m` a l'equador; al sud és `10.000.000 m`. Aquests falsos orígens eviten valors negatius dins de l'ús ordinari, però no identifiquen el fus, l'hemisferi ni el datum. Un parell com `344448 m E, 4551803 m N` només es pot localitzar inequívocament quan també se'n declara el CRS.

La distorsió UTM és controlada dins i prop de cada fus i augmenta en allunyar-se del meridià central. UTM no cobreix les regions polars i una anàlisi que travessa diversos fusos pot necessitar una altra projecció o un càlcul geodèsic. Que les unitats siguin metres no garanteix que el CRS sigui adequat fora de la seva àrea d'ús.

Una coordenada UTM no és una referència **MGRS**. MGRS és un sistema de designació de quadrícula que utilitza UTM entre `80° S` i `84° N` i UPS a les regions polars. En l'àmbit UTM combina un número de fus, una lletra de banda latitudinal, lletres per al quadrat de `100 km` i parelles de dígits d'est i nord amb una precisió determinada pel nombre de dígits. En un nom de CRS com `UTM zone 31N`, la `N` indica l'hemisferi nord; en una referència MGRS, la lletra de banda té una altra funció. MGRS codifica una referència de quadrícula i una precisió, però no substitueix la identificació completa del CRS.

## Mapa, imatge i lectura cartogràfica

Una imatge registra valors captats per un sensor; un mapa selecciona i organitza informació per comunicar una lectura del territori. Una ortofoto pot servir de fons mesurable dins de la seva exactitud, però no incorpora necessàriament una llegenda ni converteix els objectes visibles en entitats. Un mapa pot utilitzar una ortofoto i capes vectorials alhora, però ha de declarar què aporta cada font i de quina data és.

### Escala numèrica i escala gràfica

La **fracció representativa** `1:n` relaciona una distància al mapa amb `n` unitats iguals al territori. A `1:25.000`, `1 cm` al mapa representa `25.000 cm`, és a dir, `250 m`; `4 cm` representen `1 km`. A la inversa, si `3 cm` representen `750 m`, primer es converteixen `750 m` en `75.000 cm` i es divideix per `3`: l'escala és `1:25.000`. En superfícies, el denominador s'aplica al quadrat: a `1:10.000`, `2 cm²` representen `2 × 10.000² cm²`, és a dir, `20.000 m²` o `2 ha`.

Una escala `1:5.000` és **més gran** que una escala `1:1.000.000` perquè la fracció és més gran. L'escala gran cobreix menys territori i permet representar més detall; l'escala petita cobreix més extensió i exigeix més generalització. «Gran» i «petita» no descriuen la mida física del full ni el nivell de zoom.

L'**escala gràfica** representa distàncies mitjançant una barra graduada. Si el mapa es redimensiona proporcionalment, la barra es redimensiona amb ell i continua permetent una lectura aproximada; la fracció numèrica impresa deixa de ser correcta. En una pantalla, el zoom canvia l'escala de visualització, però no millora l'escala de producció, la resolució ni l'exactitud de la font. En una composició o exportació cal fixar l'escala de sortida i comprovar que el detall i els textos són llegibles a la mida final.

### Generalització i elements de lectura

Canviar d'escala obliga a **generalitzar**: seleccionar allò pertinent, simplificar formes, agrupar objectes, desplaçar-los per evitar conflictes o exagerar algun element perquè continuï sent llegible. Aquestes operacions modifiquen la representació, no el fenomen original. Ampliar una geometria generalitzada no recupera els detalls omesos i ampliar una imatge no crea noves observacions.

::: table "Elements mínims per interpretar un mapa"
| Element | Pregunta que ha de resoldre |
| --- | --- |
| Extensió i marc | Quin territori inclou el mapa i què queda fora? |
| Escala | Quina relació hi ha entre la representació i les distàncies del territori? |
| Nord i orientació | Cap a on s'orienta la vista? El nord no s'ha de suposar sempre a la part superior |
| Llegenda | Quins objectes, categories o valors representen els símbols necessaris per llegir el resultat? |
| Font i data | Qui ha produït cada dada i a quin moment o període correspon? |
| CRS i unitats | Com s'han interpretat la posició, les distàncies i les superfícies? |
:::

No tots els mapes necessiten una fletxa de nord o una llegenda extensa. L'orientació pot quedar inequívoca per una retícula i una capa única amb significat explícit pot no requerir llegenda. Tanmateix, ometre un element només és correcte si la pregunta que resol continua tenint una resposta clara. El títol o el text que acompanya el mapa ha d'identificar el fenomen i l'àmbit, i la font, la data, el CRS i les unitats no s'han de deixar a la memòria de qui l'ha elaborat.

## Models conceptuals, lògics i físics {#nivells-model-dades}

Un **model de dades** selecciona els objectes, les propietats i les relacions necessaris per respondre una pregunta geogràfica. En una xarxa elèctrica pot interessar saber quines torres sostenen cada tram i quina altura té cada suport. El paisatge conté molta més informació de la que cal conservar per a aquest inventari {% cite longleyGeographicInformationScience2015 %}.

Les tres figures següents mantenen la mateixa escena de torres i cables. Les anotacions mostren què s'hi decideix en cada nivell: **quins objectes interessen**, **com es representen amb dades** i **com es desen en un sistema concret**. Dins de cada model, tots els elements del mateix tipus repeteixen les mateixes propietats, amb els seus valors corresponents.

### Model conceptual: objectes, propietats i relacions

El **model conceptual** identifica els elements rellevants i el seu significat. En el cas de la figura hi ha torres de suport i trams de cable. Cada tram queda delimitat per dues torres, i la torre central és compartida pels dos trams. La posició i l'altura són propietats que cal conèixer per descriure els suports.

![Tres torres amb la seva posició relativa, altura i nombre de trams, i dos trams de cable amb els dos suports identificats en llenguatge corrent]({{ site.baseurl }}/assets/quarto/03-estructura-formats-referenciacio/tower-model-conceptual.qmd "Model conceptual de la xarxa elèctrica. Identifica les torres, els trams i les relacions de suport, amb propietats com la posició i l'altura, sense fixar encara una geometria digital ni un format."){: data-figure-width-web="42rem" data-figure-width-pdf="88%" data-caption-source="Font: elaboració pròpia; escena i valors sintètics."}

### Model lògic: geometries, identificadors i atributs

El **model lògic** especifica com es representaran aquells objectes amb dades. En l'exemple, cada torre es representa amb un punt al peu del suport, un identificador i un atribut d'altura. Cada tram té una representació lineal i conserva els identificadors de les dues torres extremes. T2 és compartida per L1 i L2: aquesta relació queda expressada en les dades, no només suggerida pel dibuix.

![Cada torre amb identificador, geometria puntual, altura i trams relacionats, i cada tram amb identificador, geometria lineal i torres inicial i final]({{ site.baseurl }}/assets/quarto/03-estructura-formats-referenciacio/tower-model-logical.qmd "Model lògic de la xarxa elèctrica. Representa les torres amb punts i els trams amb línies, amb identificadors, altures i referències als suports. Les altures no són cotes del terreny; l'ordre dels extrems no indica el sentit del corrent."){: data-figure-width-web="42rem" data-figure-width-pdf="88%" data-caption-source="Font: elaboració pròpia; escena i valors sintètics."}

### Model físic: fitxers, capes i tipus de camp

El **model físic** concreta on i com es desaran les dades. Una implementació possible utilitza el fitxer GeoPackage `xarxa.gpkg`, amb una capa de punts `torres` i una capa de línies `trams`. Cada torre conserva `id_torre` com a text i `altura_m` com a nombre decimal. Cada tram conserva `id_tram`, `torre_inici` i `torre_final` com a text; aquests dos darrers camps identifiquen els suports. Totes dues capes utilitzen `EPSG:25831` {% cite ogcGeoPackage2024 %}.

![Cada torre amb la capa i els camps id_torre i altura_m, amb tipus i valors, i cada tram amb id_tram, torre_inici i torre_final complets; el fitxer i el CRS són comuns]({{ site.baseurl }}/assets/quarto/03-estructura-formats-referenciacio/tower-model-physical.qmd "Model físic de la xarxa elèctrica en un GeoPackage. Especifica el fitxer, les capes, el CRS i els noms i tipus de camp. Cada element mostra els camps de la seva capa amb els valors corresponents."){: data-figure-width-web="42rem" data-figure-width-pdf="88%" data-caption-source="Font: elaboració pròpia; exemple d'emmagatzematge de l'escena sintètica."}

Canviar el format de desament pot mantenir la mateixa organització lògica, sempre que conservi les geometries, els atributs i les relacions necessàries. En canvi, representar tota la xarxa com una imatge faria perdre la identificació directa de cada torre i tram. Per això el format és una decisió d'emmagatzematge i no defineix, tot sol, què modelen les dades.

>> **«Físic» es refereix aquí a l'emmagatzematge digital.** Les tres figures mostren el mateix paisatge; el que canvia és la informació que s'hi especifica per construir el conjunt de dades.

## Objectes i camps: representacions vectorials i ràster {#objectes-camps-vector-raster}

Un **objecte discret** té identitat i límits definits pel model: un fanal, una parcel·la o un municipi. Un **camp** associa una propietat a les posicions d'un domini, com l'elevació, la temperatura o la classe de coberta. «Camp» no significa necessàriament variable contínua: les cobertes són categòriques. Tampoc no s'ha de confondre aquest ús geogràfic amb un camp o columna d'una taula.

El **model vectorial** representa geometries mitjançant coordenades. Els punts localitzen, les línies descriuen trajectes i els polígons delimiten superfícies; els atributs n'expliquen el significat. Un bosc es pot descriure com un polígon per mesurar-ne l'àrea o com un conjunt de punts si l'objectiu és inventariar cada arbre. Els límits d'un municipi poden ser nítids per convenció administrativa encara que no siguin visibles sobre el terreny.

El **model ràster** divideix l'espai en una graella i associa un valor a cada cel·la i banda. Una ortofoto registra una resposta radiomètrica; un model d'elevacions, altures; i un ràster de cobertes, classes. La posició de les cel·les es deriva de les files i columnes, l'origen, la mida, l'orientació i el CRS. El valor pot representar una observació, una mitjana, una classe dominant o una estimació: la cel·la i la seva semàntica s'han de definir conjuntament.

![El mateix paisatge amb bosc, edifici, carretera i tres torres unides per cable es representa en perspectiva, en vector i en una graella quadrada amb els mateixos colors i posicions]({{ site.baseurl }}/assets/quarto/03-estructura-formats-referenciacio/real-world-vector-raster.qmd "Correspondència entre paisatge, vector i ràster sobre el mateix àmbit. Les cel·les són quadrades i la carretera forma una franja contínua d'un costat a l'altre. El ràster mostra les mateixes classes, però discretitza els contorns i representa punts i cables amb cel·les; no conserva els identificadors ni la connectivitat del vector."){: data-figure-width-web="42rem" data-figure-width-pdf="88%" data-caption-source="Font: elaboració pròpia amb geometries sintètiques; el paisatge és un esquema, no una observació territorial."}

En aquesta transposició didàctica, els polígons aporten la classe del centre de cada cel·la; les torres i els trams de cable marquen les cel·les que els contenen, amb prioritat de la torre sobre el cable. Els colors permeten reconèixer els mateixos elements en les tres vistes. La cel·la ocupada per una torre no representa la seva petjada real, i la continuïtat de cel·les blaves no substitueix una taula de connexions entre torres.

La distinció objecte/camp orienta la tria, però no imposa vector/ràster. Un camp d'elevacions es pot descriure amb punts de mostreig, corbes de nivell, triangles o una graella. Una classificació del sòl es pot representar amb polígons o cel·les. Cal preguntar quina informació ha de conservar-se: la identitat de cada parcel·la, la connectivitat d'una xarxa o la comparació de valors sobre un suport regular.

>>> **Dues preguntes sobre una carretera.** Per estimar la superfície pavimentada cal un polígon de calçada o una classificació ràster amb detall adequat. Per calcular un itinerari cal una xarxa amb trams, connexions i restriccions de pas. Una línia que dibuixa l'eix no aporta per si sola ni l'amplada real ni els girs permesos.

Rasteritzar i vectoritzar exigeix regles i pot perdre informació. Una carretera més estreta que la cel·la pot desaparèixer si s'assigna la classe del centre; marcar totes les cel·les que toca pot exagerar-ne la superfície. El [capítol de model i anàlisi ràster]({{ site.baseurl }}/ca/chapters/model-analisi-raster/) desenvolupa resolució, alineació, `NoData`, remostreig i conversió. Aquí interessa reconèixer que canviar de representació altera allò que es pot identificar i mesurar.

## Geometries independents, topologia i xarxes {#geometries-topologia-xarxes}

En una estructura d'**espagueti** (*spaghetti*), cada geometria desa les seves coordenades independentment. Dos polígons adjacents poden repetir tots els vèrtexs de la frontera; dues línies poden tenir extrems coincidents sense referenciar un mateix node. Aquest emmagatzematge no implica necessàriament errors: les capes de geometries simples són útils per a moltes anàlisis i permeten calcular relacions espacials. El que no incorporen per defecte és una estructura compartida que mantingui totes les coincidències {% cite ogcSimpleFeatures2011 %}.

Una **estructura topològica explícita** representa relacions mitjançant elements amb identitat, com nodes, arcs i cares. Una frontera comuna pot emmagatzemar-se una vegada i ser referenciada per dues cares. En una xarxa, els arcs indiquen els nodes que connecten. El model funcional hi afegeix informació que la geometria no resol: circuits, sentit de circulació, costos o restriccions. Dues línies que es creuen en planta poden estar a altures diferents i no tenir connexió.

### Torres i trams: geometries vinculades

En una xarxa elèctrica simplificada es poden capturar primer els punts de les torres i registrar després els parells que defineixen els trams. L1 uneix T1 amb T2, i L2 uneix T2 amb T3. A partir d'aquestes referències es construeix cada línia entre les posicions actuals dels seus extrems. No cal digitalitzar dues vegades les mateixes coordenades.

Dibuixar les torres no permet deduir tota la xarxa: cal conèixer els parells connectats o disposar d'un ordre documentat dins de cada circuit. Unir cada punt amb el més proper podria inventar connexions. A més, una recta entre suports només és una representació planimètrica simplificada; calcular distàncies de seguretat respecte del cable real exigeix considerar-ne la cota, la curvatura i les condicions físiques.

![La torre T2 es desplaça: en geometries independents els trams queden a la posició antiga, mentre que els trams reconstruïts amb els identificadors de les torres mantenen la connexió]({{ site.baseurl }}/assets/quarto/03-estructura-formats-referenciacio/tower-network-update.qmd "El moviment de T2 afecta L1 i L2. A l'esquerra només s'ha editat el punt; a la dreta una regla reconstrueix els trams des de les torres referenciades. La línia discontínua indica la posició anterior, no un tercer tram."){: data-figure-width-web="42rem" data-figure-width-pdf="88%" data-caption-source="Font: elaboració pròpia; xarxa sintètica."}

>>> **Correcció de la torre central.** Si es corregeix la posició de T2, cal actualitzar els extrems de L1 i L2 que hi arriben. Les tres torres continuen sent les mateixes i els trams mantenen les connexions; el que canvia és la seva geometria.

L'eina d'edició ha de mantenir expressament la connexió o reconstruir les línies després de moure la torre. Desar les dues capes dins d'un mateix GeoPackage no activa aquest comportament automàticament. La comprovació consisteix a verificar que cada tram continua arribant als suports que té assignats.

>>>> **L'ajust de vèrtexs no és una dependència persistent.** L'autoensamblat ajuda a fer coincidir coordenades durant la captura. El moviment posterior d'una torre només arrossega els trams si l'eina i el model mantenen expressament aquesta relació. La comprovació ha de comparar els extrems de cada tram amb les torres referenciades i detectar identificadors inexistents.

El [capítol de digitalització vectorial]({{ site.baseurl }}/ca/chapters/model-vectorial-digitalitzacio/) concreta les regles de captura i els controls de topologia. La distinció entre emmagatzematge independent i elements compartits reapareix més endavant en la comparació entre GeoJSON i TopoJSON.

## Núvols de punts i superfícies TIN {#nuvols-punts-tin}

Un aixecament LiDAR o una reconstrucció fotogramètrica pot produir un **núvol de punts**: moltes mostres amb coordenades X, Y i Z i, segons l'adquisició, intensitat, color, nombre de retorn o classificació. Les mostres descriuen superfícies observades, no necessàriament objectes identificats. Mil punts sobre una coberta no són mil edificis, i els buits poden correspondre a oclusions o manca d'observació {% cite qgisUserGuide344 %}.

LAS i la seva forma comprimida LAZ són formats habituals de núvols de punts. Conservar-los permet tornar a classificar mostres de sòl, vegetació o construccions sense haver reduït prematurament la informació a una altura per cel·la. La densitat de punts no equival a la resolució d'un ràster: primer cal decidir quines mostres s'utilitzen i com s'estima una superfície entre elles.

Una **xarxa irregular de triangles**, o **TIN** (*triangulated irregular network*), connecta vèrtexs mitjançant arestes i cares triangulars. En un TIN del terreny cada vèrtex té una cota i cada cara permet interpolar la superfície interior, habitualment com un pla. La distribució irregular pot concentrar vèrtexs en canvis de pendent i utilitzar triangles més grans en zones uniformes. Les línies de ruptura poden imposar arestes al llarg d'una carena o un talús perquè la triangulació no els travessi arbitràriament {% cite felicisimoModelosDigitalesTerreno1994 %}.

![Mostres de sòl, vegetació i coberta en un núvol tridimensional, al costat d'una superfície de triangles formada amb punts seleccionats del sòl]({{ site.baseurl }}/assets/quarto/03-estructura-formats-referenciacio/point-cloud-tin.qmd "Un núvol conserva mostres separades; un TIN afegeix connectivitat i una interpolació entre vèrtexs. En aquest exemple, el TIN utilitza una selecció de punts de sòl i exclou la vegetació i la coberta. Les cares entre mostres són estimades."){: data-figure-width-web="42rem" data-figure-width-pdf="88%" data-caption-source="Font: elaboració pròpia amb un relleu i un mostreig sintètics."}

>>> **Un talús al costat d'una carretera.** Si s'han mesurat punts a la coronació i al peu, un TIN pot conservar aquestes dues línies com a ruptures de pendent. Una graella representa el mateix relleu amb altures en posicions regulars; si les cel·les són grans, el talús queda generalitzat. Cap opció recupera un peu de talús que no s'hagi observat.

El TIN és una estructura vectorial de superfície, no una família oposada a qualsevol vector. Tampoc no és superior al ràster en tots els casos: la graella facilita l'àlgebra de mapes i les operacions de veïnatge, mentre que el TIN explicita la malla i les ruptures incorporades. Convertir entre tots dos implica interpolació i una decisió sobre el detall que es conserva.

## Superfícies 2,5D, volums i models semàntics 3D {#superficies-volums-3d}

Un model d'elevacions convencional assigna una sola altura a cada posició horitzontal: $z=f(x,y)$. Se sol descriure com a **2,5D** perquè utilitza Z, però no representa lliurement tot el volum. Tant una graella d'elevacions com un TIN del terreny poden seguir aquest supòsit. Permeten representar el relleu, però una sola superfície no conserva alhora el tauler d'un pont i el sòl que hi ha a sota.

Una geometria **3D** pot representar posicions superposades en planta, parets verticals, voladissos i cavitats. Un núvol pot mostrejar-ne diverses superfícies; una **malla de superfície** connecta vèrtexs i cares per descriure una pell; i un **sòlid** delimita un volum amb una frontera tancada i coherent. Una malla oberta de façanes no defineix necessàriament un interior ni permet calcular un volum vàlid.

### Voxels i malles de volum

Un **voxel** és una cel·la volumètrica. En una graella regular s'identifica amb tres índexs i unes dimensions en X, Y i Z; no cal que sigui un cub. Cada voxel pot contenir una classe geològica, una concentració o una temperatura. A diferència d'un ràster d'elevacions, el model pot assignar valors diferents a diversos nivells d'una mateixa columna vertical.

![El mateix terreny verd i pont blau es representen com una superfície del sòl, una geometria 3D amb piles i tauler i una graella de voxels que conserva el pas d'aire sota el pont]({{ site.baseurl }}/assets/quarto/03-estructura-formats-referenciacio/surface-volume-models.qmd "Tres models del mateix àmbit. La superfície 2,5D conserva només la cota del sòl; la geometria 3D incorpora el pont. Els voxels discretitzen aquest mateix sòl i les mateixes piles i tauler, amb els mateixos colors. Les cel·les d'aire no es dibuixen, de manera que el buit sota el pont continua visible."){: data-figure-width-web="42rem" data-figure-width-pdf="88%" data-caption-source="Font: elaboració pròpia; geometries sintètiques."}

La graella de la figura assigna a cada voxel la classe del seu centre: sòl, pont o aire. Els contorns es tornen esglaonats, però es conserva la diferència entre el terreny, la construcció i l'espai buit inferior. L'aire és una classe coneguda que s'ha ocultat per llegibilitat, no una absència de dades. Una graella més grossa podria perdre una pila estreta o tancar un pas que el model geomètric manté obert.

Per estudiar un aqüífer, una superfície pot descriure la cota del sostre d'una formació; un volum de voxels pot representar materials o concentracions a profunditats diferents. Una **malla de volum** utilitza cel·les, per exemple tetraedres, que s'adapten a geometries més complexes. En simulacions d'aigua o calor, els valors poden associar-se a nodes, cares o cel·les i variar amb el temps. Cal llegir aquesta associació per interpretar-los: una visualització 3D acolorida no la revela tota sola.

>> **Perspectiva, dimensió i exactitud són propietats diferents.** Una ortofoto estesa sobre un terreny pot semblar tridimensional sense contenir parets ni objectes 3D. Extrudir una planta d'edifici amb una altura estimada crea una geometria, però no certifica una coberta observada. Z també necessita unitats i referència vertical.

### CityGML i BIM: significat dels objectes construïts

La geometria no explica tota sola si una cara representa una coberta, un mur o un forjat. **CityGML** defineix un model d'informació per a objectes urbans, com edificis, vies, vegetació i ponts, amb propietats i relacions semàntiques. Aquesta distinció permet consultar edificis o superfícies de coberta i relacionar-los amb el context territorial. CityGML 3.0 separa el model conceptual de les codificacions que l'implementen, entre les quals hi ha GML; no és simplement una extensió per desar triangles {% cite ogcCityGMLOverview %}.

Els **nivells de detall** (*Level of Detail*, LoD) expressen diferents graus de representació geomètrica. Un volum simplificat pot ser suficient per a una primera estimació d'ombres, mentre que l'estudi de cobertes pot requerir-ne la forma. Un nivell de detall superior no garanteix més exactitud ni que totes les propietats estiguin informades. Els models urbans també poden descriure espais interiors: no s'han de definir només per l'aparença exterior.

**BIM** (*Building Information Modelling*) és una metodologia de gestió d'informació de construccions al llarg del seu cicle de vida, no un únic format. Els seus models poden identificar murs, forjats, portes, instal·lacions i espais, amb materials, dimensions i relacions constructives. **IFC**, mantingut per buildingSMART, és un esquema obert per intercanviar aquesta informació i admet diferents codificacions. Un model IFC aporta objectes i propietats, no només una forma visible {% cite buildingSMARTIndustryFoundationClasses %}.

![Un edifici representat en el seu context urbà amb coberta i façanes diferenciades i el mateix volum descompost en murs, forjats i un conducte]({{ site.baseurl }}/assets/quarto/03-estructura-formats-referenciacio/citygml-bim.qmd "Dues finalitats de modelització d'un edifici. La vista urbana destaca l'objecte i les seves superfícies; la vista constructiva, els components i les propietats que permeten gestionar-los. La vista esclatada és una convenció gràfica i no representa la posició real de les peces."){: data-figure-width-web="42rem" data-figure-width-pdf="88%" data-caption-source="Font: elaboració pròpia; esquema conceptual, no exportació d'un fitxer CityGML o IFC."}

>>> **Ombres al barri i reforma d'una coberta.** Per estimar quins edificis projecten ombra sobre una plaça cal el seu emplaçament i una geometria urbana adequada. Per preparar la reforma interessa distingir elements de coberta, capes de material, gruixos i connexions constructives. Una mateixa construcció participa en tots dos problemes, però les dades necessàries no són idèntiques.

Integrar SIG i BIM requereix acordar la referenciació, les unitats, els identificadors i les equivalències entre classes. Un model constructiu pot utilitzar coordenades locals; un model urbà, un CRS territorial. A més de situar-los correctament, cal decidir com s'agrupen peces en un edifici i quines propietats es conserven. Exportar només una malla visible pot perdre aquesta semàntica, encara que el resultat mantingui una aparença detallada.

## Fitxers, conjunts i contenidors

Un **conjunt de dades** és una unitat identificable que pot contenir una o més capes, taules o bandes. Una **capa** és una vista organitzada d'un contingut espacial per treballar-hi al SIG. Un GeoPackage pot contenir moltes capes, un conjunt Shapefile en representa normalment una i un GeoTIFF pot tenir diverses bandes. L'arbre de capes de QGIS organitza el projecte, però no indica quants fitxers hi ha al disc.

Un **fitxer** és una unitat d'emmagatzematge, però una dada pot dependre de diverses peces: el Shapefile distribueix una capa i una imatge pot requerir un *world file* i un `.prj`. Un **contenidor** agrupa continguts gestionats; un `.gpkg` pot allotjar taules, índexs i metadades dins de SQLite. Ni la carpeta ni el contenidor substitueixen la còpia de seguretat i la documentació.

Una base espacial de servidor afegeix concurrència, permisos i transaccions multiusuari; compartir un GeoPackage en una carpeta sincronitzada no hi equival. El `.qgz` tampoc no és un contenidor de dades: conserva referències, estils, formularis i composicions, però no incorpora automàticament les fonts. A la primera micropràctica, el GeoPackage conté les capes locals i el projecte de treball incrustat; el `.qgz` independent es crea al final com a versió lliurable i ha de continuar referenciant el GeoPackage que l'acompanya.

## Formats d'ús habitual

Un format adequat ha de conservar els tipus, els noms, el CRS i els valors necessaris sense introduir limitacions innecessàries. Convertir totes les dades al mateix format no resol les diferències de model ni de qualitat.

::: table "Formats geogràfics i decisions d'ús"
| Format | Contingut habitual | Ús adequat | Precaució principal |
| --- | --- | --- | --- |
| GeoPackage | Capes vectorials, taules i tessel·les dins d'una base SQLite | Edició, organització i intercanvi de dades vectorials | Els estils i projectes QGIS són extensions, no contingut universal de l'estàndard {% cite ogcGeoPackage2024 %} |
| Shapefile | Conjunt de fitxers per a geometria, índex i atributs | Compatibilitat amb sistemes antics | Camps, tipus, codificació i gestió fragmentada són limitats {% cite esriShapefile1998 %} |
| GeoJSON | Text estructurat amb entitats | Intercanvi web i conjunts moderats | RFC 7946 fixa coordenades geogràfiques WGS 84 i ordre longitud-latitud {% cite butlerGeoJSON2016 %} |
| TopoJSON | Text JSON amb geometries construïdes a partir d'arcs compartits | Distribució web de límits amb topologia comuna | Requereix eines compatibles i la quantificació pot modificar coordenades {% cite bostockTopoJSON2013 %} |
| GeoTIFF | Graella georeferenciada | Anàlisi i distribució de ràsters | Cal decidir compressió, blocs, piràmides, tipus i `NoData` {% cite ogcGeoTIFF2019 %} |
| COG | GeoTIFF organitzat per lectura parcial remota | Distribució web de ràsters grans | La conformitat depèn de l'estructura interna, no només de l'extensió `.tif` {% cite ogcCOG2023 %} |
| ASCII Grid | Una graella i una capçalera en text | Intercanvi simple i inspecció de valors | És voluminós i normalment no incorpora el CRS |
| CSV | Taula de text delimitat | Intercanvi d'atributs o punts amb coordenades | Tipus, separador, codificació, decimals i CRS s'han de declarar externament |
:::

La tria depèn del receptor, el programari, l'edició, la concurrència, el volum i les regles que s'han de conservar. El Shapefile pot ser necessari per compatibilitat; GeoPackage és preferible per a moltes capes vectorials de treball; i un ràster analític de coma flotant sol ser més previsible com a GeoTIFF. Cap d'aquestes preferències elimina la prova d'intercanvi.

### Shapefile: un conjunt de peces coordinades

El nom **Shapefile** pot induir a pensar en un únic fitxer `.shp`, però una capa funcional es distribueix com a mínim entre tres peces amb el mateix nom base. El `.shp` emmagatzema les geometries; el `.shx`, l'índex que permet localitzar cada registre geomètric; i el `.dbf`, els atributs en una taula dBase. El número d'ordre relaciona geometria i fila, de manera que no s'han d'ordenar o substituir les peces separadament.

>>>> **Un Shapefile no és un fitxer `.shp`.** Copiar, reanomenar o lliurar només aquesta peça separa les geometries de l'índex i dels atributs. S'ha de conservar i transportar el conjunt complet de fitxers amb el mateix nom base.

Altres fitxers laterals completen informació que el nucli no resol. El `.prj` conté una descripció textual del CRS, però no sempre permet recuperar sense ambigüitat l'edició o l'operació geodèsica esperada. El `.cpg` declara la codificació dels textos del `.dbf`. Un `.qix` pot aportar un índex espacial utilitzat per QGIS i altres programes; `.sbn` i `.sbx` són índexs d'altres implementacions; i `.shp.xml` pot contenir metadades. No totes aquestes peces són obligatòries, però eliminar-les sense saber-ne la funció pot perdre referenciació, accents, metadades o rendiment.

::: table "Components habituals d'un conjunt Shapefile"
| Extensió | Funció | Conseqüència probable si falta o es descoordina |
| --- | --- | --- |
| `.shp` | Geometries | No hi ha formes espacials que es puguin llegir |
| `.shx` | Índex dels registres geomètrics | La capa pot no obrir-se o pot requerir reconstrucció de l'índex |
| `.dbf` | Files i camps d'atributs | Es perden els atributs o la correspondència amb les geometries |
| `.prj` | Descripció del CRS | Les coordenades queden sense una referència declarada fiable |
| `.cpg` | Codificació del text | Els caràcters poden interpretar-se amb una pàgina de codis errònia |
| `.qix`, `.sbn`, `.sbx` | Índex espacial | Les consultes poden ser més lentes; l'índex es pot regenerar quan calgui |
| `.shp.xml` | Metadades laterals | Es perd documentació, encara que la geometria pugui continuar obrint-se |
:::

La taula dBase limita els noms de camp tradicionals a deu caràcters i ofereix tipus, dates, nuls i precisió més pobres que una base moderna. Una exportació pot truncar noms i trencar expressions o diccionaris. La capa també queda restringida a una família geomètrica i no conserva de manera interoperable dominis, formularis o relacions. Els límits de mida depenen de l'estructura i del controlador; la recomanació pràctica d'aproximadament `2 GB` per component no s'ha de presentar com un màxim matemàtic universal.

Un ZIP manté les peces juntes durant el transport, però no repara l'esquema o la codificació. En importar a GeoPackage cal conservar l'original i comparar recompte, tipus geomètric, camps, nuls, extensió i CRS.

### GeoPackage: estàndard, extensions i contingut de QGIS

GeoPackage és un estàndard d'implementació de l'OGC basat en SQLite. Defineix una base comuna i opcions per emmagatzemar entitats vectorials, taules d'atributs, piràmides de tessel·les i extensions. Les taules de sistema fan que el contenidor sigui autodescriptiu: `gpkg_spatial_ref_sys` registra definicions de referència; `gpkg_contents` inventaria el contingut; `gpkg_geometry_columns` descriu les columnes geomètriques de les taules d'entitats; i les taules de matriu de tessel·les documenten nivells, dimensions i resolucions quan aquest contingut existeix {% cite ogcGeoPackage2024 %}.

«GeoPackage pot contenir ràsters» necessita precisió: el nucli inclou piràmides de tessel·les d'imatges o mapes, mentre que les cobertures numèriques en tessel·les depenen d'una extensió. Un lector vectorial no ha de suportar totes les extensions; per intercanviar un ràster analític de coma flotant, GeoTIFF sol ser més previsible.

La taula `gpkg_extensions` declara funcionalitats addicionals, que poden ser compartides o pròpies d'un productor. `layer_styles` pot contenir estils de QGIS i `qgis_projects`, projectes; un altre client pot llegir les entitats i ignorar aquesta configuració. Al GeoPackage de `sandbox/`, l'entrada incrustada `pr1` és la còpia de treball del projecte municipal. La representació externa només es prepara després dels controls.

>>>> **Els fitxers `-journal`, `-wal` i `-shm` no són residus que es puguin esborrar.** Durant una escriptura SQLite, al costat de `projecte.gpkg` pot aparèixer `projecte.gpkg-journal` o la parella `projecte.gpkg-wal` i `projecte.gpkg-shm`. Aquestes peces registren o coordinen la transacció activa. Desar els canvis no obliga el programa a tancar-ne la connexió, i els fitxers laterals poden continuar presents fins que la sessió d'escriptura queda completament tancada, per exemple en tancar QGIS. Mentre hi siguin, no s'han d'eliminar, reanomenar, moure ni separar del `.gpkg`. Abans de copiar, comprimir, sincronitzar o lliurar el contenidor cal tancar totes les connexions, comprovar que els fitxers laterals han desaparegut i reobrir una còpia per verificar que les capes i taules esperades es llegeixen correctament. Si continuen presents després del tancament, s'ha de conservar el conjunt i diagnosticar-lo; eliminar-los a mà pot perdre canvis o malmetre la base.

Un GeoPackage en una carpeta sincronitzada no és una base multiusuari i pot patir conflictes si s'edita simultàniament.

### GeoJSON i TopoJSON per a intercanvi web

GeoJSON és un format textual basat en JSON, adequat per a respostes web i conjunts moderats. Una `Feature` associa una geometria amb `properties`, i una `FeatureCollection` n'agrupa diverses. La transparència del text facilita inspeccionar-lo, però repeteix noms i coordenades i no incorpora un índex espacial intern; no és la millor base general per editar un projecte gran {% cite butlerGeoJSON2016 %}.

RFC 7946 fixa les posicions en longitud i latitud, en aquest ordre, dins de WGS 84 segons `OGC:CRS84`. El membre `crs` antic ja no forma part d'aquest contracte. Una capa UTM destinada a GeoJSON s'ha de transformar en una sortida d'intercanvi i reobrir per comprovar geometries, atributs, extensió i ordre dels eixos. El nombre de decimals no certifica l'exactitud.

El GeoJSON següent descriu dos polígons adjacents, `A` i `B`. Cada `Feature` és completa i independent: les sis posicions de la frontera situada a la longitud 2 apareixen primer de sud a nord dins de `A` i després de nord a sud dins de `B`.

::: listing "Dos polígons adjacents en GeoJSON: cada geometria repeteix la frontera comuna"
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {"nom": "A"},
      "geometry": {
        "type": "Polygon",
        "coordinates": [[
          [2, 41], [2, 41.2], [2, 41.4],
          [2, 41.6], [2, 41.8], [2, 42],
          [1, 42], [1, 41], [2, 41]
        ]]
      }
    },
    {
      "type": "Feature",
      "properties": {"nom": "B"},
      "geometry": {
        "type": "Polygon",
        "coordinates": [[
          [2, 41], [3, 41], [3, 42],
          [2, 42], [2, 41.8], [2, 41.6],
          [2, 41.4], [2, 41.2], [2, 41]
        ]]
      }
    }
  ]
}
```
:::

TopoJSON és una especificació comunitària que separa els objectes geomètrics dels **arcs compartits**. En l'exemple equivalent, `arcs[1]` conté una sola vegada les sis posicions de la frontera. El polígon `A` la recorre com a arc `1`; el valor `-2` de `B` significa «arc 1 en sentit invers», perquè TopoJSON codifica la inversió de l'índex 1 com `~1 = -2`. Els arcs `0` i `2` completen els perímetres exteriors. Aquest exemple no aplica cap `transform`: manté coordenades absolutes perquè l'estructura sigui visible {% cite bostockTopoJSON2013 %}.

::: listing "Els mateixos polígons en TopoJSON: la frontera comuna es desa com un sol arc"
```json
{
  "type": "Topology",
  "objects": {
    "municipis": {
      "type": "GeometryCollection",
      "geometries": [
        {
          "type": "Polygon",
          "arcs": [[1, 0]],
          "properties": {"nom": "A"}
        },
        {
          "type": "Polygon",
          "arcs": [[2, -2]],
          "properties": {"nom": "B"}
        }
      ]
    }
  },
  "arcs": [
    [[2, 42], [1, 42], [1, 41], [2, 41]],
    [
      [2, 41], [2, 41.2], [2, 41.4],
      [2, 41.6], [2, 41.8], [2, 42]
    ],
    [[2, 41], [3, 41], [3, 42], [2, 42]]
  ]
}
```
:::

![Comparació de dos polígons que repeteixen la frontera en GeoJSON amb els mateixos polígons construïts a partir d'un únic arc compartit en TopoJSON, juntament amb la mida serialitzada dels dos exemples]({{ site.baseurl }}/assets/quarto/03-estructura-formats-referenciacio/geojson-topojson-shared-border.qmd "En el cas didàctic, GeoJSON desa 18 posicions i repeteix la frontera; TopoJSON en desa 14 i permet que els dos polígons recorrin el mateix arc en sentits oposats. El JSON minificat i sense compressió passa de 367 a 328 bytes, un 10,6% menys."){: data-figure-width-web="54rem" data-figure-width-pdf="100%"}

La xifra és una mesura reproduïble d'aquests dos objectes serialitzats en UTF-8, sense espais ni compressió: s'estalvien 39 bytes, o un 10,6%. No és un percentatge universal ni una garantia d'estalvi de memòria RAM. El guany sol créixer quan moltes entitats comparteixen fronteres llargues, però depèn de la complexitat dels arcs, els atributs, la quantificació i la compressió del transport; un lector també pot expandir els arcs a geometries independents en carregar-los. Per tant, el volum s'ha de mesurar sobre el conjunt i la compressió que realment es distribuiran.

Els blocs anteriors es poden desar directament com a fitxers: cal copiar el JSON complet de cada exemple en un editor de text pla, desar-lo amb codificació UTF-8 i utilitzar, respectivament, noms com `poligons_adjacents.geojson` i `poligons_adjacents.topojson`. S'ha de copiar només el contingut JSON i comprovar que l'editor no hi afegeixi una extensió `.txt`, com en `poligons_adjacents.geojson.txt`. L'extensió identifica el format, però canviar-la no transforma l'estructura GeoJSON en TopoJSON.

Per visualitzar la capa al navegador, [geojson.io](https://geojson.io/) permet obrir el fitxer GeoJSON i consultar-ne geometries i atributs. [Mapshaper](https://mapshaper.org/) admet tant GeoJSON com TopoJSON: s'hi pot arrossegar cadascun dels fitxers i contrastar el resultat. En tots dos casos s'han de reconèixer els dos polígons adjacents `A` i `B` i l'atribut `nom`. La coincidència del mapa ajuda a comprovar la geometria; la diferència en l'emmagatzematge de la frontera compartida s'observa en el text dels fitxers.

TopoJSON pot reduir la mida de cobertures administratives i mantenir la coincidència dels límits compartits, però té menys suport directe i no és un estàndard OGC o IETF {% cite bostockTopoJSON2013 %}.

La quantificació de TopoJSON ajusta coordenades a una graella i pot simplificar o col·lapsar detalls. Per això és una transformació amb pèrdua que exigeix conservar els paràmetres i validar recompte, propietats, extensió i geometries. Al projecte del curs, GeoPackage continua sent el format de treball; GeoJSON o TopoJSON només són sortides d'intercanvi quan el destinatari les necessita.

### GeoTIFF i COG

TIFF és un contenidor flexible d'imatges. **GeoTIFF** hi incorpora etiquetes que relacionen files i columnes amb un espai de model i descriuen el CRS. Un GeoTIFF pot contenir una o més bandes, mostres enteres o de coma flotant, diferents compressions i una organització en tires o blocs. El sufix `.tif` no demostra que hi hagi georeferenciació ni que el CRS sigui complet: cal inspeccionar les etiquetes i l'extensió espacial.

Per a un ràster analític s'han de documentar files, columnes, nombre de bandes, tipus de mostra, resolució, origen, extensió, CRS, unitats de cada banda i `NoData`. La compressió sense pèrdua, com DEFLATE, LZW o altres opcions admeses pel lector de destinació, conserva els valors; una compressió amb pèrdua com JPEG pot ser adequada per a determinada imatge visual, però no per a valors categòrics o mesures que s'han de recuperar exactament. El tipus de dada també importa: convertir elevacions decimals a enters o nombres amb signe a un tipus sense signe pot truncar o reinterpretar valors.

L'organització en blocs permet llegir una finestra sense recórrer tot el ràster. Les **piràmides** o vistes de resolució reduïda acceleren la visualització a escales petites, però els seus valors depenen del mètode de remostreig. Per a una ortofoto pot convenir una mitjana; per a classes de sòl, el veí més proper o una moda, segons la finalitat. La piràmide no substitueix les dades de resolució completa i no ha de participar inadvertidament en un càlcul que les necessiti.

Un **Cloud Optimized GeoTIFF** (COG) és un GeoTIFF organitzat internament amb blocs, nivells reduïts i una disposició dels índexs i bytes que permet peticions parcials. Quan el servidor admet sol·licituds HTTP de rang i el client entén l'estructura, només cal descarregar els blocs i el nivell necessaris. Un fitxer no esdevé COG perquè es canviï el nom o perquè tingui `.tif`; s'ha de crear i validar amb el perfil corresponent. Inversament, un COG continua sent llegible com a GeoTIFF per molts clients que no n'aprofiten l'accés parcial.

COG millora l'accés, no la qualitat intrínseca. Un COG pot conservar un CRS equivocat, un `NoData` mal definit, valors amb una compressió inadequada o una resolució que no respon a la pregunta. Tampoc no assegura rapidesa si el servidor no accepta rangs, si els blocs són inadequats o si l'operació necessita gairebé totes les cel·les. Per al curs, la distinció inicial és suficient: GeoTIFF descriu la graella georeferenciada; COG n'afegeix una organització pensada per a lectura parcial remota.

### ASCII Grid i georeferenciació lateral {#ascii-grid-georeferenciacio-lateral}

L'**ASCII Grid** d'Esri, identificat sovint com AAIGrid pels controladors GDAL, representa una banda com una capçalera de text seguida de files de valors. La capçalera habitual declara `ncols`, `nrows`, la coordenada inferior esquerra amb `xllcorner` i `yllcorner` o amb les variants de centre, `cellsize` i, opcionalment, `NODATA_value`. La primera fila de valors correspon habitualment a la part superior de la graella, encara que l'origen declarat sigui inferior {% cite rouaultGDAL2026 %}.

```text
ncols         6
nrows         5
xllcorner     300000
yllcorner     4600000
cellsize      25
NODATA_value  -9999
12 11 10 9 8 7
13 12 11 10 9 8
```

El format és fàcil d'inspeccionar i pot resultar útil per intercanviar una graella simple, però repeteix els nombres com a text, ocupa més, no incorpora compressió ni piràmides i té una capacitat limitada per a múltiples bandes o metadades. La capçalera situa la graella en un sistema de coordenades, però no identifica necessàriament quin CRS dona significat als valors; aquesta informació sol dependre d'un `.prj` o de documentació externa. Un `.asc` sense CRS no s'ha d'assignar per semblança sense contrastar la font.

Un **fitxer de georeferenciació lateral** o *world file* relaciona una imatge amb coordenades mitjançant sis coeficients d'una transformació afí. Les extensions habituals són `.tfw` per a TIFF, `.jgw` per a JPEG, `.pgw` per a PNG o `.wld` de forma genèrica. Els sis valors descriuen l'escala de píxel en X, dos termes de rotació, l'escala en Y —sovint negativa perquè les files creixen cap avall— i les coordenades del centre del píxel superior esquerre. Aquesta última convenció de centre és rellevant: interpretar-la com la cantonada desplaça la imatge mitja cel·la.

El *world file* no conté el CRS, ni els valors `NoData`, ni les bandes. Una imatge amb `.jgw` pot aparèixer al lloc aproximat perquè QGIS aplica l'afinitat i continuar sense una referència terrestre completa. Un `.prj` lateral pot aportar el CRS, però totes les peces s'han de mantenir juntes. GeoTIFF integra la georeferenciació principal dins del fitxer i redueix aquest risc, encara que les metadades i la llicència continuïn requerint documentació.

## Codificació i interoperabilitat

La **interoperabilitat** exigeix que dos programes interpretin de manera compatible geometries, camps, nuls, text, dates, CRS i extensions, no només que obrin el fitxer. Una codificació de caràcters defineix com una seqüència de bytes representa lletres, dígits i signes. Si s'interpreta malament, `Móra d'Ebre` pot continuar tenint una geometria correcta mentre els accents, els símbols o els noms dels atributs es mostren alterats.

### Codificació del DBF i caràcters mal interpretats

En un Shapefile, els textos són al `.dbf`. El controlador de GDAL intenta llegir primer la codificació declarada al `.cpg` i, si no hi és, pot recórrer a la marca de pàgina de codis del mateix DBF. Totes dues indicacions poden faltar, ser ambigües o no descriure correctament els bytes; per això una capa que s'obre sense error encara pot mostrar text mal interpretat {% cite gdalContributorsESRIShapefileDBF2026 %}.

>> El `.cpg` és un fitxer de text separat que comparteix nom base amb `.shp`, `.shx` i `.dbf`. Es pot obrir amb un editor de text i pot contenir valors com `UTF-8`, `1252` o `ISO-8859-1`. Modificar aquesta etiqueta no converteix els bytes del DBF: només canvia com un lector intenta interpretar-los.

Windows-1252 i ISO-8859-1, també anomenada Latin-1, comparteixen ASCII i molts caràcters occidentals, però no són sinònims. Als bytes entre `0x80` i `0x9F`, Windows-1252 defineix, entre altres signes, l'euro i cometes tipogràfiques, mentre que ISO-8859-1 reserva codis de control. Escollir una opció perquè «els accents es veuen bé» pot deixar altres caràcters equivocats.

Un diagnòstic reproduïble segueix aquests passos:

1. Conservar intactes el paquet i totes les peces originals del Shapefile.
2. Consultar les metadades del productor i inspeccionar el `.cpg`; si falta, registrar també aquesta absència.
3. Obrir una còpia amb el selector de codificació de la font i contrastar paraules conegudes que continguin accents, `ç`, euro o cometes. Canviar aquest selector rellegeix els mateixos bytes; no els recodifica.
4. Quan s'ha identificat la codificació d'origen, exportar a una font nova, preferentment GeoPackage per al treball del curs, i tornar-la a obrir per comparar recompte, camps, nuls, caràcters i identificadors.

Substituir manualment els accents visibles no resol el problema: pot alterar només alguns registres i ocultar que tota la columna s'ha descodificat amb una regla equivocada. Tampoc no s'ha de declarar `UTF-8` en un `.cpg` si el DBF continua codificat en Windows-1252. La conversió real necessita llegir els bytes amb la codificació correcta i escriure una sortida nova amb la codificació de destinació.

### Codificació i tipus d'atribut en GeoPackage, CSV i GeoJSON

GeoPackage no necessita un `.cpg` lateral perquè el text es gestiona dins de la base SQLite. Un CSV, en canvi, no fixa per si sol una única codificació i l'ha de declarar el productor o el contracte d'intercanvi. GeoJSON és text JSON: RFC 7946 recomana seguir el perfil I-JSON i l'estàndard JSON vigent exigeix UTF-8 per a l'intercanvi entre sistemes fora d'un ecosistema tancat. Per tant, un GeoJSON conforme destinat a intercanvi s'ha d'escriure en UTF-8, no acompanyar-se d'un `.cpg` {% cite butlerGeoJSON2016 brayJSON2017 %}.

La codificació no resol els tipus. `00123` pot ser un identificador textual, una data no és una cadena, i `NULL`, buit, zero i `-9999` no són equivalents. La truncació de noms d'un Shapefile també pot crear col·lisions que obliguen a actualitzar expressions i diccionaris.

La sortida s'ha de reobrir com una font nova i comparar recompte, geometria, esquema, nuls, caràcters, identificadors, extensió, CRS i valors. En ràster s'afegeixen dimensions, bandes, tipus, resolució, alineació i `NoData`. Un checksum només prova identitat de bytes.

## Eixos, dimensions i sistemes de referència de coordenades

Un cop establerta la cadena bàsica, cal reconèixer els casos en què l'ordre, una dimensió addicional o una referència antiga canvien la interpretació. Una **coordenada** és un dels nombres d'una seqüència ordenada i la seqüència completa és una **tupla de coordenades**. El mateix parell pot significar est i nord en metres, índexs d'una graella o dos atributs sense component espacial.

En la convenció SIG més habitual, `X` precedeix `Y`; en un sistema projectat orientat de manera convencional això sol correspondre a est i nord. En coordenades geogràfiques, moltes API i formats utilitzen longitud i latitud. Tanmateix, l'ordre oficial dels eixos d'un CRS pot ser diferent. `EPSG:4326` defineix latitud geodèsica com a primer eix i longitud com a segon, mentre que GeoJSON exigeix longitud–latitud perquè segueix `OGC:CRS84`. Les biblioteques i interfícies poden aplicar un ordre tradicional `X/Y` per comoditat o respectar estrictament l'autoritat. Per això no s'ha d'aprendre una única regla de memòria: s'ha de llegir el contracte del format, del servei o de l'eina.

Una posició bidimensional és `XY`. Si incorpora altura geomètrica, pot ser `XYZ`; si incorpora una mesura al llarg d'una línia, `XYM`; i si conté totes dues, `XYZM`. La **dimensió de coordenades** no s'ha de confondre amb la **dimensió topològica** de la geometria: un punt és topològicament de dimensió zero encara que tingui X, Y i Z; una línia és de dimensió u; una superfície, de dimensió dos. Tampoc no s'ha de confondre una escena visualitzada en perspectiva amb una geometria que conserva Z.

Z necessita una semàntica: altura el·lipsoidal, cota física, profunditat o referència local. Un tercer nombre no crea un CRS vertical, i molts algorismes avaluen relacions només en XY. M és una mesura, com distància acumulada, temps o punt quilomètric, no necessàriament un eix espacial. Si Z o M intervenen en l'anàlisi, cal documentar referència, unitat i sentit i provar que formats i processos les conserven.

Els decimals expressen resolució numèrica, no exactitud. Retallar-los pot reduir volum o precisió aparent si la tolerància respecta el detall útil i després es tornen a validar geometria i topologia; afegir zeros no aporta informació.

### Components i abast d'un CRS

Un **sistema de referència de coordenades** (CRS) dona significat a una seqüència de coordenades. Sense aquesta informació, els valors `344000, 4552000` no indiquen per si sols una posició, unes unitats ni una àrea d'ús. Un CRS relaciona el sistema de coordenades amb un model de la Terra i defineix com s'interpreten els eixos.

Un **CRS geodèsic** expressa habitualment longitud i latitud sobre un el·lipsoide associat a un datum o marc de referència. Un **CRS projectat** combina un CRS geodèsic base amb una conversió cartogràfica i un sistema cartesià. La projecció permet treballar en unitats lineals dins d'una àrea d'ús, però introdueix deformacions de distància, superfície, direcció o forma.

Els codis del registre EPSG identifiquen definicions concretes. `EPSG:4326` correspon a WGS 84 geogràfic, mentre que `EPSG:25831` correspon a ETRS89 / UTM zona 31N. Aquest darrer és habitual a Catalunya i utilitza metres, però la seva adequació depèn de l'àrea d'ús i de l'operació. El Reial decret 1071/2007 adopta ETRS89 com a sistema de referència geodèsic oficial a la península i les Balears {% cite realDecreto1071_2007 %}.

### Ampliació: referència vertical i geoide

La distinció vertical és necessària quan es combinen cotes, punts GNSS o models d'elevacions; per a una anàlisi només planimètrica es pot deixar com a ampliació. La superfície física de la Terra no és la superfície regular sobre la qual es calculen les coordenades. L'**el·lipsoide de referència** és un model matemàtic regular que permet resoldre latituds, longituds, distàncies geodèsiques i projeccions.

El **geoide** és una superfície equipotencial del camp de gravetat terrestre que s'aproxima al nivell mitjà del mar en repòs i es prolonga sota els continents. No és el relleu ni un el·lipsoide amb muntanyes exagerades. Com que depèn de la distribució de masses i de les observacions gravimètriques, s'aproxima mitjançant models de geoide que tenen resolució, data i àrea d'aplicació pròpies. Serveix com a referència física per entendre determinades altures, però la seva irregularitat no és adequada per definir directament una xarxa simple de latitud i longitud.

![Globus amb l'ondulació del geoide codificada en colors i amb el relleu molt exagerat]({{ site.baseurl }}/assets/img/crs/geoid.png "Ondulació del geoide en fals color i amb un factor d'exageració vertical de 10.000; no representa la forma física de la Terra. Font: International Centre for Global Earth Models, 2019, via Wikimedia Commons; llicència CC BY 4.0."){: data-figure-width-web="31rem" data-figure-width-pdf="72%"}

Font i llicència: [International Centre for Global Earth Models, via Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Geoid_undulation_10k_scale.jpg), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Un receptor GNSS proporciona habitualment una **altura el·lipsoidal** $h$, mesurada respecte de l'el·lipsoide de la solució. La cartografia topogràfica utilitza sovint una **altura ortomètrica** $H$, referida al geoide i relacionada amb el camp de gravetat. L'**ondulació del geoide** $N$ expressa la separació entre geoide i el·lipsoide. En l'aproximació habitual, la relació correcta és:

$$
h = H + N
\label{eq:altura-geoidal}
$$

Per tant, $H = h - N$. El signe de $N$ forma part del model; no s'ha de substituir per una diferència absoluta. La relació és conceptualment clara, però una conversió precisa necessita un model de geoide compatible amb els marcs horitzontal i vertical, la ubicació i les convencions de l'organisme productor. En alguns sistemes s'utilitzen altures normals i quasi-geoides; identificar simplement qualsevol Z com a «metres sobre el nivell del mar» pot introduir errors de diversos ordres de magnitud segons la font.

### Dàtum, marc i època de coordenades

Un **sistema de coordenades** és el conjunt de regles matemàtiques que permet assignar nombres a posicions. Un **dàtum geodèsic** o, en terminologia moderna, un **marc de referència**, relaciona aquest sistema i l'el·lipsoide amb la Terra mitjançant origen, orientació, escala i una materialització observada. La definició no consisteix simplement a «ajustar l'el·lipsoide al geoide»: el geoide intervé en la referència física de les altures, mentre que un marc geodèsic tridimensional es materialitza amb estacions, observacions i coordenades.

Els marcs contemporanis poden ser **dinàmics**. Les plaques tectòniques i les estacions es mouen, de manera que una coordenada d'alta exactitud pot necessitar una **època de coordenades**, és a dir, la data a la qual correspon la posició. Un codi de CRS sense època pot ser suficient per a una cartografia municipal de precisió mètrica i insuficient per comparar campanyes geodèsiques centimètriques. La precisió requerida determina si aquest component temporal és operativament rellevant.

Un **CRS vertical** és un sistema unidimensional basat en una referència vertical i una unitat. Pot expressar altures físiques o profunditats. Un **CRS compost** combina components, per exemple un CRS projectat horitzontal i un CRS vertical. Aquesta estructura és més informativa que una capa `XYZ` amb Z sense definir. Quan es combinen un model d'elevacions i punts GNSS, s'han de revisar separadament el CRS horitzontal i la referència vertical; una coincidència correcta en planta no prova que les cotes siguin comparables.

### Distorsió i elecció de projecció

La distorsió és una propietat espacialment variable de qualsevol projecció, no un error aleatori del fitxer. Una projecció **conforme** conserva angles i formes locals; una d'**equivalent**, proporcions d'àrea; i una d'**equidistant**, només les distàncies definides pel seu disseny. Cap d'aquestes propietats no es conserva universalment sobre tot el planeta.

La selecció ha de partir de l'operació i de l'àrea d'ús. Un mapa que compara superfícies pot necessitar una projecció equivalent; una cartografia local pot prioritzar conformitat i escala controlada; una distància llarga es pot calcular geodèsicament. Web Mercator (`EPSG:3857`) és útil per compatibilitat entre tessel·les web, però la seva escala varia amb la latitud i no és una opció general per calcular àrees o distàncies territorials.

La longitud `1,14759°` i la latitud `41,10263°` en `EPSG:4326`, per exemple, es transformen aproximadament en `E 344448 m, N 4551803 m` en `EPSG:25831`. Els dos parells representen una posició comparable perquè se n'han declarat els CRS i s'ha aplicat una operació, no perquè els nombres s'assemblin. La documentació ha d'indicar quin CRS ha utilitzat l'algorisme, que pot diferir del CRS del llenç.

### ETRS89, WGS 84 i ED50

**ETRS89** és el sistema europeu adoptat per mantenir coordenades estables respecte de la part estable de la placa eurasiàtica. Les seves materialitzacions concretes són marcs ETRF de diferents realitzacions i èpoques. `EPSG:4258` n'és el CRS geogràfic 2D i `EPSG:25831`, la combinació projectada amb UTM zona 31N. El Reial decret 1071/2007 estableix ETRS89 com a sistema oficial a la península i les Balears i REGCAN95 a les Canàries; això no converteix `EPSG:25831` en adequat per a qualsevol territori espanyol ni per a qualsevol operació {% cite realDecreto1071_2007 %}.

**WGS 84** és un sistema global mantingut per al posicionament i la navegació. Té diverses realitzacions i evoluciona amb el marc terrestre global. En molts usos cartogràfics ordinaris, coordenades WGS 84 i ETRS89 poden aparèixer pràcticament coincidents a Europa; en treballs de més exactitud, la realització i l'època fan que no s'hagin de tractar com a idèntiques per defecte. `EPSG:4326` identifica el CRS geogràfic 2D de l'agrupació WGS 84, però no descriu l'altura ortomètrica ni una projecció mètrica.

**ED50** és un dàtum europeu històric, materialitzat amb xarxes terrestres i l'el·lipsoide Internacional de 1924. Va ser habitual en cartografia espanyola anterior a l'adopció d'ETRS89; `EPSG:23031` correspon a ED50 / UTM zona 31N. El codi continua sent necessari per interpretar dades històriques encara que el CRS sigui obsolet per a nova cartografia oficial. «Obsolet» no significa que s'hagi d'assignar un codi modern a les coordenades antigues: significa que cal declarar ED50 com a origen i transformar-lo amb una operació adequada quan el projecte ho requereixi.

El desplaçament ED50–ETRS89 no és una constant universal que es pugui sumar a X i Y. Varia espacialment i segons la materialització i l'operació utilitzada; en cartografia peninsular pot ser de l'ordre de desenes o més d'un centenar de metres. Una transformació basada en una graella oficial pot modelar variacions locals millor que una transformació paramètrica general. El resultat s'ha de comprovar amb punts o capes de control independents, no només perquè el contorn «sembli encaixar».

### Identificadors EPSG i definicions completes

El conjunt de dades EPSG, mantingut per l'IOGP, assigna identificadors a CRS, datums, el·lipsoides, sistemes de coordenades i operacions. Un codi com `EPSG:25831` identifica una definició concreta, no una etiqueta inventada pel projecte. Els codis d'operacions de transformació són objectes diferents dels codis de CRS; conèixer origen i destinació no determina sempre una única operació {% cite iogpEPSGDataset2026 %}.

::: table "CRS habituals que cal saber distingir"
| Identificador | Nom i tipus | Eixos i unitats | Ús o precaució |
| --- | --- | --- | --- |
| `EPSG:4326` | WGS 84 geogràfic 2D | Ordre oficial latitud, longitud; graus | Intercanvi global; moltes eines mostren ordre X/Y per convenció |
| `OGC:CRS84` | WGS 84 geogràfic 2D | Longitud, latitud; graus | Convenció utilitzada per GeoJSON RFC 7946 |
| `EPSG:4258` | ETRS89 geogràfic 2D | Latitud, longitud; graus | Referència geogràfica europea |
| `EPSG:25831` | ETRS89 / UTM zona 31N | Est, nord; metres | Treball regional dins l'àrea europea del fus 31 |
| `EPSG:3857` | WGS 84 / Pseudo-Mercator | X, Y; metres de projecció | Tessel·les web; no és una opció mètrica general |
| `EPSG:23031` | ED50 / UTM zona 31N | Est, nord; metres | Cartografia històrica; cal transformar, no reassignar, per passar a ETRS89 |
:::

L'identificador és preferible a una cadena PROJ antiga escrita a mà. Les cadenes heretades no poden representar tota la informació moderna sobre eixos, àrea d'ús, realització, època o operació i una conversió d'anada i tornada pot perdre metadades. Per intercanviar una definició que no disposa d'un identificador d'autoritat convé utilitzar una representació completa com WKT2 o PROJJSON i conservar-ne la procedència. No s'ha de copiar una cadena `+proj=...` d'un tutorial antic com si fos la definició canònica del CRS {% cite projContributorsPROJ2026 %}.

Un codi tampoc no prova que les dades el compleixin. És possible etiquetar coordenades ED50 com `EPSG:25831` i obtenir un fitxer formalment llegible però desplaçat. L'extensió numèrica, les unitats, la font i un control conegut han de concordar amb la definició. Si un codi ha estat retirat o substituït, les dades antigues continuen necessitant la identificació original per poder aplicar l'operació correcta.

El selector de CRS de QGIS permet cercar l'identificador d'autoritat i consultar-ne el nom, l'àrea d'ús i la definició. Aquesta informació serveix per verificar la tria; la presència d'un codi a la llista no demostra que coincideixi amb les coordenades de la capa.

El codi de la cantonada inferior dreta de QGIS identifica el CRS del projecte i governa la visualització o **reprojecció al vol** del llenç. La crida de la figura assenyala aquest control i indica el CRS en què es mostra el mapa, no necessàriament el de les fonts. El selector de CRS pot aparèixer en configurar el projecte, declarar la referència d'una font o definir la sortida d'un algorisme. Cal identificar el context de l'eina per distingir si s'està canviant la vista, assignant significat a unes coordenades existents o preparant una transformació.

::: subfigures a+b "Control de la reprojecció al vol i selecció del CRS a QGIS 3.44.11. La crida identifica EPSG:25831 com a CRS del llenç; el selector en detalla la definició i l'àrea d'ús."
![Finestra de QGIS amb l'ortofoto de Vila-seca i una crida de reprojecció al vol cap al control EPSG 25831]({{ site.baseurl }}/assets/img/qgis/qgis-project-crs-icgc-2025.png "Reprojecció al vol: el llenç es mostra en EPSG:25831, ETRS89 / UTM zona 31N, sobre l'ortofoto ICGC 2025."){: data-figure-width-web="100%" data-figure-width-pdf="100%"}
![Selector de CRS de QGIS amb el codi 25831, ETRS89 UTM zona 31N seleccionat i la seva àrea d'ús visible]({{ site.baseurl }}/assets/img/qgis/qgis-crs-selection.png "Definició d'EPSG:25831: nom, unitats en metres i àrea d'ús del fus 31N."){: data-figure-width-web="100%" data-figure-width-pdf="100%"}
:::

Font de l'ortofoto: [ICGC, Ortofoto Territorial 2025, servei WMS](https://geoserveis.icgc.cat/servei/catalunya/orto-territorial/wms), llicència [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

### Lectura d'una cadena de CRS: EPSG:25831 {#cadena-crs-epsg-25831}

Una **cadena de CRS** és una representació textual de la seva definició. `EPSG:25831` és la forma breu d'identificar-la: `EPSG` indica el registre d'autoritat i `25831`, l'entrada corresponent a **ETRS89 / UTM zona 31N**. El número és una clau de consulta; no s'ha d'intentar deduir tota la definició separant-ne els dígits.

Una cadena **PROJ** fa visibles els paràmetres mitjançant expressions `+nom=valor` i alguns indicadors sense valor. La forma compacta següent descriu la projecció UTM sobre l'el·lipsoide GRS80 utilitzada per `EPSG:25831`. És útil per llegir la configuració cartogràfica, però no conserva tota la informació de la definició EPSG {% cite projContributorsPROJ2026 %}.

::: listing "Paràmetres cartogràfics d'EPSG:25831 expressats com a cadena PROJ"
```text
+proj=utm +zone=31 +ellps=GRS80 +units=m +no_defs +type=crs
```
:::

::: table "Lectura de la cadena PROJ per components"
| Component | Què significa |
| --- | --- |
| `+proj=utm` | Utilitza la projecció Universal Transversa de Mercator, basada en la Transversa de Mercator amb els paràmetres de cada fus |
| `+zone=31` | Selecciona el fus 31, amb meridià central a 3° est de Greenwich |
| Absència de `+south` | En la convenció UTM de PROJ, correspon a l'hemisferi nord; `+south` seleccionaria el sud |
| `+ellps=GRS80` | Defineix l'el·lipsoide GRS80: semieix major de 6.378.137 m i invers de l'aplanament de 298,257222101; no identifica tot sol el marc ETRS89 |
| `+units=m` | Les coordenades projectades horitzontals s'expressen en metres; no defineix un CRS vertical |
| `+no_defs` | Indicador heretat que evitava carregar paràmetres de fitxers de valors predeterminats; no significa «sense sistema de referència» |
| `+type=crs` | Indica a PROJ que la cadena descriu un CRS, en lloc de només una operació de coordenades |
:::

La forma `utm` incorpora paràmetres que no apareixen escrits a la cadena curta. La mateixa **conversió cartogràfica** del fus 31 nord es pot desplegar amb `tmerc`, el nom de la Transversa de Mercator a PROJ. Els salts de línia següents només separen grups de paràmetres per facilitar-ne la lectura:

::: listing "La mateixa projecció amb origen, escala i falsos orígens explícits"
```text
+proj=tmerc +lat_0=0 +lon_0=3 +k_0=0.9996
+x_0=500000 +y_0=0
+ellps=GRS80 +units=m +type=crs
```
:::

::: table "Paràmetres que la convenció UTM fixa per al fus 31 nord"
| Paràmetre | Valor i interpretació |
| --- | --- |
| `+lat_0=0` | Latitud de l'origen: l'equador, 0° |
| `+lon_0=3` | Longitud del meridià central: 3° est |
| `+k_0=0.9996` | Factor d'escala al meridià central, sense unitats; controla la deformació de la projecció, no l'escala d'impressió del mapa |
| `+x_0=500000` | Fals est de 500.000 m; el meridià central rep aquesta coordenada E |
| `+y_0=0` | Fals nord de 0 m; a l'equador la coordenada N és zero per a aquest fus nord |
:::

>>> **Comprovació dels paràmetres.** Per a una posició del meridià central a 3° E i 41° N, expressada en ETRS89, l'est projectat és 500.000 m. La coordenada nord és aproximadament 4.538.757 m. El primer valor deriva del fals est; el segon depèn de la latitud i de la projecció. Canviar només `+units` o `+zone` alteraria la interpretació o el càlcul, no el lloc real observat.

>>>> **GRS80 no és sinònim d'ETRS89.** L'el·lipsoide descriu una forma matemàtica, mentre que el marc relaciona les coordenades amb la Terra. Per configurar la capa cal seleccionar `EPSG:25831`; per conservar una definició completa es pot utilitzar WKT2 o PROJJSON. Una exportació PROJ pot incloure també un `+towgs84` heretat amb zeros: no prova que ETRS89 i WGS 84 siguin idèntics a qualsevol època i exactitud.

En WKT2, `PROJCRS` identifica el CRS projectat i `BASEGEOGCRS`, la referència geogràfica ETRS89. Els blocs `CONVERSION` i `PARAMETER` descriuen la projecció. `AXIS` i `LENGTHUNIT` especifiquen els eixos est–nord en metres, mentre que `ID["EPSG",25831]` identifica el CRS complet. Llegir aquests blocs permet comprovar la referència, els paràmetres i les unitats sense confondre'ls amb la simbologia del mapa.

### Assignar, transformar i visualitzar

Assignar un CRS
: Declara què signifiquen unes coordenades existents sense modificar-ne els valors. Només corregeix metadades absents o equivocades quan es coneix la referència real.

Reprojectar o transformar
: Calcula coordenades noves en un altre CRS mitjançant una operació espacial explícita.

Visualitzar al vol
: Fa coincidir capes al llenç sense canviar el CRS ni les coordenades emmagatzemades a la font.

Confondre assignació i transformació pot desplaçar una capa milers de quilòmetres o ocultar visualment un error. Abans de calcular distàncies, àrees o resolucions cal inspeccionar el CRS de cada entrada, el CRS de sortida i l'operació aplicada.

>>>> **El CRS que apareix a la barra del projecte no identifica necessàriament el CRS de la capa activa.** La comprovació s'ha de fer a la informació de cada font. Canviar el CRS del projecte pot modificar la visualització sense corregir una capa mal declarada.

La comparació següent amplia la vista a la cobertura mundial d'OpenStreetMap per fer més visibles les deformacions. Les tessel·les de la font es mantenen en `EPSG:3857`; QGIS les reprojecta al vol al CRS del projecte que identifica cada crida. En `EPSG:4326`, el llenç utilitza coordenades angulars en graus: representar longitud i latitud sobre una graella plana no conserva uniformement distàncies, formes ni àrees.

`EPSG:25831`, en canvi, és un CRS regional basat en UTM zona 31N, adequat per al seu àmbit europeu. Aplicar-lo a una vista mundial és una prova deliberada fora de l'àrea d'ús: s'hi observen deformacions extremes i discontinuïtats, no una alternativa vàlida per construir un planisferi. Els buits als pols tenen una causa diferent: la font de tessel·les Web Mercator només arriba aproximadament als 85° nord i sud. Les dues vistes canvien la representació del mapa, però no modifiquen les dades originals {% cite projContributorsPROJ2026 qgisUserGuide344 %}.

::: subfigures a+b "Reprojecció al vol d'OpenStreetMap a escala mundial a QGIS 3.44.11. Les crides identifiquen el CRS de cada llenç; la vista UTM posa en evidència els límits d'aplicar un CRS regional fora de la seva àrea d'ús."
![Finestra de QGIS amb la cobertura mundial d'OpenStreetMap i una crida de reprojecció al vol en EPSG 4326]({{ site.baseurl }}/assets/img/qgis/qgis-osm-crs-4326.png "Reprojecció al vol a EPSG:4326, WGS 84: vista mundial amb coordenades en graus."){: data-figure-width-web="100%" data-figure-width-pdf="100%"}
![Finestra de QGIS amb el mapa mundial d'OpenStreetMap fortament deformat i una crida de reprojecció al vol en EPSG 25831]({{ site.baseurl }}/assets/img/qgis/qgis-osm-crs-25831.png "Reprojecció al vol a EPSG:25831, ETRS89 / UTM zona 31N: ús fora de l'àrea regional, amb deformacions i talls."){: data-figure-width-web="100%" data-figure-width-pdf="100%"}
:::

Mapa base: [© OpenStreetMap contributors](https://www.openstreetmap.org/copyright).

Una **conversió de coordenades** canvia el sistema de coordenades sense canviar el dàtum, com el pas d'ETRS89 geogràfic a ETRS89 / UTM zona 31N. Una **transformació de coordenades** relaciona marcs o datums diferents, com ED50 i ETRS89. Una operació real pot concatenar diversos passos: desprojectar, transformar el marc amb una graella i projectar al destí. En l'ús general de QGIS, «reprojectar» s'empra sovint per a tota la cadena; documentar origen, destinació i operació evita que aquesta simplificació amagui què s'ha calculat.

### Operacions candidates i graelles de transformació

Entre dos CRS hi pot haver més d'una operació candidata. Cadascuna té una àrea d'ús, una exactitud declarada, uns paràmetres i, de vegades, dependències de fitxers. QGIS i PROJ seleccionen operacions a partir de les definicions, l'extensió i els recursos disponibles, però la selecció automàtica s'ha de revisar quan el canvi de dàtum afecta el resultat o quan es necessita una exactitud concreta {% cite qgisUserGuide344 %}.

Una **graella de transformació** conté correccions que varien segons la posició i té cobertura, resolució i versió pròpies. Si falta una graella o una època necessària, QGIS pot oferir una operació aproximada, però el programari no pot inventar la informació absent. Cal registrar l'operació triada, qualsevol recurs extern i l'avís d'exactitud; una posició coneguda detecta errors grossos, però no substitueix un control geodèsic quan es demana precisió topogràfica.

### Quan cal materialitzar una reprojecció

La visualització al vol és apropiada per explorar capes amb CRS diferents i pot ser suficient quan l'algorisme declara que transforma les entrades i calcula en un CRS adequat. No cal exportar físicament totes les capes al mateix CRS abans de qualsevol anàlisi. Cal, però, saber si el procés adopta el CRS d'una entrada, el del projecte o un CRS de sortida, i en quines unitats interpreta les distàncies.

Materialitzar una capa transformada és convenient quan s'ha de distribuir en un format amb un CRS fix, quan moltes operacions repetiran la mateixa transformació, quan el programari receptor no transforma al vol, quan cal congelar una operació i una graella per reproduïbilitat o quan les unitats de treball han de quedar inequívocament en la font. La sortida ha de tenir un nom nou, conservar l'original i registrar CRS d'origen, CRS de destinació i operació.

En vector, la transformació recalcula cada vèrtex. Les línies rectes en un CRS poden esdevenir corbes en un altre, però una geometria segmentada només en transforma els vèrtexs existents; en trajectes llargs pot caldre densificar abans si s'ha de representar bé la corba. En ràster, la reprojecció crea una graella nova i necessita resolució, extensió, alineació i mètode de remostreig. El veí més proper sol preservar codis categòrics; mètodes interpoladors poden ser adequats per a camps continus, però creen valors nous. Aquesta diferència fa especialment inadequat reprojectar ràsters repetidament només per uniformar una carpeta.

### Verificació del CRS de la font, del projecte i de la sortida a QGIS

QGIS separa el CRS de la font, el CRS del projecte i el CRS escollit per a una sortida. La barra d'estat mostra el del projecte. Les propietats de cada capa, a les pestanyes d'informació o font segons el proveïdor, mostren el CRS interpretat, l'extensió, la geometria, el nombre d'entitats o les dimensions ràster. La primera comprovació consisteix a llegir aquestes propietats, no a canviar el CRS del projecte fins que el dibuix sembli correcte {% cite qgisUserGuide344 %}.

L'ordre operatiu següent redueix els diagnòstics per prova i error:

1. **Conservar l'origen.** Cal anotar productor, nom, data, format i CRS declarat abans de modificar res.
2. **Inspeccionar els nombres.** Extensió, unitats i ordre de magnitud poden descartar hipòtesis, però no demostren un codi. A Catalunya, valors propers a `1,15; 41,10` són plausibles en graus i `344469; 4551807`, en UTM.
3. **Comprovar eixos i definició.** En un CSV s'ha d'identificar X/longitud i Y/latitud; de cada CRS cal llegir identificador, unitats, eixos i àrea d'ús.
4. **Contrastar una posició.** Una entitat o coordenada coneguda s'ha de comparar amb una font independent. Un mapa base només detecta errors grossos.
5. **Decidir l'acció.** Si les coordenades ja pertanyen al CRS conegut i falta l'etiqueta, s'assigna; si calen coordenades en un altre CRS, es transforma.
6. **Revisar l'operació.** Quan canvia el marc, cal comprovar àrea, exactitud i graelles i resoldre o documentar qualsevol aproximació.
7. **Fixar el càlcul i validar.** S'ha d'indicar el CRS analític i comparar extensió, recompte i una posició; en ràster també resolució, alineació, `NoData` i remostreig. No cal duplicar entrades si l'eina les transforma explícitament.

L'acció **Estableix el CRS de la capa** o una opció equivalent canvia la interpretació i correspon a l'assignació; no és una eina per moure coordenades. **Desa les entitats com a...** amb un CRS de destinació o els algorismes de reprojecció creen una font nova transformada. En ràster, la reprojecció es fa amb una operació de deformació de graella i paràmetres de remostreig. Els noms exactes de menú poden variar entre versions, de manera que el diari ha de registrar l'operació i els paràmetres, no només una successió de clics.

>>> **Assignació o reprojecció.** La prova consisteix a desactivar temporalment una capa de referència i llegir una coordenada concreta en el CRS de la font i en el del projecte. Si en canviar només el CRS del projecte la capa continua al mateix lloc visual, està actuant la transformació al vol. Si s'exporta una còpia i els valors numèrics canvien però la posició coincideix, s'ha materialitzat una reprojecció. Si els nombres no canvien després d'«assignar» un altre codi i la capa salta de lloc, s'ha canviat el significat sense transformar-la.

## Resolució, precisió i exactitud

Resolució espacial
: Detall espacial que una font pot distingir de manera fiable. En un ràster, la mida de cel·la descriu la geometria de la graella, però no garanteix per si sola la resolució efectiva, que també depèn de la font, el mostreig, el processament i l'exactitud.

Precisió
: Grau de detall numèric o de repetibilitat d'una mesura.

Exactitud
: Proximitat d'una observació o resultat a una referència adequada.

Totes tres propietats s'han d'interpretar juntament amb l'escala de producció i de sortida.

Afegir decimals o vèrtexs no millora l'exactitud d'una font. Una ortofoto de píxel petit pot conservar un desplaçament i una geometria detallada pot ser menys exacta que un límit oficial simplificat. La transformació de coordenades només afegeix un component al pressupost d'incertesa: una operació centimètrica no converteix en centimètric un límit ambigu digitalitzat sobre una imatge mètrica.

També s'han de comparar data, unitat d'observació i generalització. Un eix viari i un polígon de calçada poden compartir CRS i representar objectes diferents; una ortofoto de 2024 i un inventari de 2018 poden estar alineats i discrepar per un canvi real. Més classes no impliquen més exactitud si la font no permet distingir-les. Les xifres finals han de reflectir el component menys precís que condiciona la pregunta.

## Errors de posició, unitats i codificació de les capes {#diagnostic-errors-capes}

Una capa desplaçada, una superfície de magnitud inesperada i un nom amb accents alterats són símptomes de problemes diferents. L'extensió numèrica, les unitats, el CRS declarat, la codificació i les metadades permeten contrastar-ne les causes. Una posició coneguda ajuda a decidir si falta assignar la referència correcta, si cal transformar les coordenades o si les fonts representen realitats incompatibles.

Una conversió de format s'ha de verificar amb recomptes, tipus geomètric, camps, valors nuls, extensió i CRS. En ràsters també cal comparar files, columnes, bandes, tipus numèric, resolució i `NoData`. El fet que el fitxer nou s'obri no demostra que la conversió sigui completa.

::: table "Símptomes que no tenen una única causa"
| Símptoma | Hipòtesis que cal contrastar | Prova discriminant |
| --- | --- | --- |
| La capa apareix prop de `0,0` | CRS projectat assignat a graus, X/Y invertits o coordenades buides convertides a zero | Revisar valors originals, camps X/Y i CRS de la font |
| Hi ha un desplaçament gairebé uniforme | Dàtum mal assignat, operació aproximada o font desplaçada | Identificar ED50/ETRS89, operació i diversos punts de control |
| El desplaçament varia pel territori | Projecció inadequada, graella absent, georeferenciació deformada o errors de font | Comparar residus en punts distribuïts i àrea d'ús |
| Els accents es trenquen | Codificació incorrecta, no geometria ni CRS | Reobrir el text amb la pàgina de codis documentada |
| Les àrees són molt petites o enormes | Graus tractats com metres, unitat diferent o fórmula inadequada | Revisar CRS de càlcul, unitats i una entitat coneguda |
| Un ràster queda desplaçat mitja cel·la | Confusió entre centre i cantonada, *world file* incorrecte o alineació diferent | Comparar origen, mida de cel·la i convenció de georeferenciació |
:::

La conversió també pot revelar incompatibilitats legítimes. Una `GeometryCollection` heterogènia no cap en una capa Shapefile d'un sol tipus sense separar-ne les peces. Un `DateTime` amb zona no es conserva en un camp de data dBase. Un GeoPackage amb projectes i estils QGIS pot perdre aquestes taules en exportar només les entitats. En aquests casos, el procediment correcte no és ocultar l'avís, sinó definir quina part es transfereix, quina es conserva a l'original i quina limitació tindrà el producte.

## Formats i CRS del projecte municipal {#cas-projecte-municipal}

El [cas guiat del capítol anterior]({{ site.baseurl }}/ca/chapters/sintesi-documentacio/#primer-projecte-municipal) ha creat una capa local a partir de la selecció de Vila-seca i ha desat dues vistes QGIS dins del mateix GeoPackage. Ara es poden comprovar els models, les estructures i les referències espacials d'aquell resultat, més enllà de la seva aparença al mapa.

### Un fitxer, una capa i diverses vistes

La taula `municipi_vilaseca` conté la geometria i els atributs. `pr1` i `comparacio` són projectes QGIS: conserven maneres diferents d'organitzar i representar aquella capa i el WMS. El `.qgz` extern és una altra representació del projecte principal i continua llegint les dades del GeoPackage. No hi ha tres còpies del terme municipal només perquè existeixin tres maneres d'obrir el mapa.

![GeoPackage amb una capa municipal compartida pels projectes pr1 i comparacio i per un projecte extern QGZ]({{ site.baseurl }}/assets/diagrams/ca/03-estructura-formats-referenciacio/geopackage-projects.puml "Relació entre contenidor, capa i projectes del cas guiat. Les tres vistes llegeixen la mateixa capa municipal. El GeoPackage és un fitxer, no una carpeta; l'agrupació interior del diagrama representa el seu contingut lògic."){: data-figure-width-web="37rem" data-figure-width-pdf="88%"}

Una modificació de la geometria compartida pot afectar totes les vistes quan es tornin a carregar. En canvi, un canvi d'estil desat només en un projecte no actualitza automàticament els altres. Per interpretar una discrepància cal identificar si ha canviat la dada, la configuració de la capa o el projecte obert.

::: table "Controls del resultat municipal comprovat amb QGIS"
| Propietat | Resultat del cas | Què acredita |
| --- | --- | --- |
| Selecció d'origen | Una entitat dins de nou municipis de l'entorn | S'ha acotat el subconjunt que s'exporta |
| Identitat | `CODIMUNI = '431711'`; `NOMMUNI = 'Vila-seca'` | El registre correspon al municipi previst |
| Capa local | `municipi_vilaseca`, una entitat `MultiPolygon` | La selecció s'ha materialitzat al contenidor |
| CRS de la capa | `EPSG:25831` | Les coordenades locals es conserven en ETRS89 / UTM 31N |
| Geometria | No buida, vàlida i igual a la seleccionada | L'exportació conserva el terme de la font |
| Projectes incrustats | `pr1` i `comparacio` | El mateix GeoPackage admet projectes amb noms diferents |
| Reobertura | Projecte extern i dues entrades incrustades oberts des d'una ruta nova | Les fonts locals es resolen al contenidor traslladat |
:::

### Comprovar què ha canviat durant l'exportació

En el cas ICGC, la font i la capa exportada declaren `EPSG:25831`. La selecció i el canvi de contenidor no han modificat les coordenades de la geometria. Si s'utilitza, en canvi, una entrada geogràfica en `EPSG:4258` i es desa la sortida en `EPSG:25831`, cal conservar els dos CRS i l'operació aplicada. Coincidir visualment al llenç no permet distingir aquestes dues situacions.

A `Propietats > Informació` s'han de llegir el CRS i l'extensió de la font efectiva. El CRS de la barra d'estat correspon a la vista del projecte. Si es canvia només aquest últim, no s'han reescrit les coordenades del GeoPackage. Si es canvia el nom visible de la capa al panell, tampoc no s'ha reanomenat necessàriament la taula interna.

La prova sense connexió comprova les dependències locals: al cas, la geometria es recupera des del GeoPackage traslladat. El WMS necessita xarxa per tornar a dibuixar el context. Aquesta dependència remota s'ha d'explicar als apunts i provar separadament; una imatge que encara apareix a la memòria cau no demostra que el servidor estigui responent.

### Comparar una segona representació municipal

Una ampliació pot incorporar una font del CNIG. Cal inspeccionar-ne els camps, el nivell administratiu, el format i el CRS reals abans de copiar-hi una expressió d'una altra distribució. Els codis ICGC i CNIG poden identificar el mateix municipi amb estructures diferents; la seva aparença numèrica no els converteix en una clau comuna.

La comparació cartogràfica manté extensió i escala i utilitza contorns distingibles. Les diferències poden respondre a data, escala, finalitat o criteri de delimitació. Una font més detallada no és automàticament més adequada per a qualsevol pregunta, i una diferència entre contorns no s'ha d'atribuir al CRS sense haver comprovat les referències de totes dues capes.

## Activitats

### Identificació dels nivells de modelització

Cal afegir una quarta torre i un tram nou a un esbós de l'escena. L'explicació ha de distingir l'objecte i la seva relació amb la xarxa, la geometria i els atributs que el representaran, i la capa i el fitxer on es conservaran. La comprovació consisteix a poder assignar cada decisió al nivell conceptual, lògic o físic i justificar-la sobre el mateix dibuix.

### Elecció d'una representació de superfície o volum

Cal justificar una representació per a cadascun d'aquests casos: inventari d'edificis, pendent del sòl, cotes del pont i del terreny inferior, concentració d'un contaminant al subsòl i materials d'una reforma. Per a cada cas s'indica la unitat representada, una dada imprescindible i una informació que es perdria en reduir-lo a una sola graella d'elevacions. Es pot proposar més d'un model si s'explica què aporta cadascun.

### Fitxa de les fonts del projecte

La fitxa iniciada al capítol anterior es completa amb el WMS i la font del límit municipal escollits. Per a cada recurs cal identificar productor, producte, model, estructura, format o servei, CRS, unitat d'observació, escala o resolució i data. Si s'ha incorporat una segona font municipal, la comparació explica què aporta i quines diferències s'han observat. La conclusió ha de distingir el context visual de la geometria local que es conservarà al GeoPackage.

### Comprovació de la visualització al vol

Amb `pr1` obert des de `sandbox/pr1-project-setup-cognom.gpkg`, cal llegir el CRS de la barra d'estat i el de cada font a `Propietats > Informació`. En l'ampliació amb el GML del CNIG en `EPSG:4258`, la coincidència visual amb el projecte de Vila-seca en `EPSG:25831` mostra la representació al vol, no una transformació del fitxer. Si només es disposa de les capes locals ja exportades en `EPSG:25831`, la seva superposició no prova aquest canvi: cal conservar una entrada en un CRS diferent per fer l'experiment.

El diari ha de conservar el CRS del projecte, el CRS de cada font, les unitats i l'extensió observada. Canviar el CRS del projecte no forma part de la prova; l'objectiu és distingir la referència de la vista de la referència emmagatzemada a cada capa.

>>>> **Canviar el format o el CRS del projecte no repara una capa mal referenciada.** Una correcció només és justificable si la font permet saber què significaven les coordenades originals; en cas contrari, la incertesa s'ha de conservar i la capa es pot haver de descartar.

### Preguntes: interpretar els controls del cas

Quina diferència hi ha entre seleccionar un municipi i conservar-ne una capa local? Com es detectaria que l'exportació ha inclòs tota la capa original? Per què una sola entitat pot ser `MultiPolygon`? Què permet afirmar la prova fora de línia del cas de Vila-seca i quina comprovació encara exigeix connexió? Les respostes han d'indicar una evidència del projecte o dels apunts.

### Activitat integradora: projecte municipal i apunts reproduïbles {#activitat-projecte-municipal}

Cal completar el projecte del municipi escollit amb un terme seleccionat d'una capa de límits, exportat al GeoPackage i carregat des d'aquest contenidor. El resultat conserva el projecte incrustat, la còpia externa, un WMS i uns apunts breus en PDF. Les explicacions i captures han de permetre repetir els passos importants, entendre les decisions i comprovar els resultats.

::: table "Resultats essencials del projecte municipal"
| Component | Requisit |
| --- | --- |
| Entrades | Projecte iniciat al capítol 02, una capa de límits municipals i un servei WMS adequat |
| Preparació | Seleccionar el municipi, exportar-lo al GeoPackage amb un CRS justificat i carregar-ne la taula local |
| Projectes | Entrada incrustada `pr1` i còpia externa `.qgz`, amb fonts coherents i camins locals relatius |
| Apunts PDF | Fonts, passos importants, camp i valor de selecció, paràmetres d'exportació, decisions, captures llegibles, controls i incidències |
| Comprovacions | Municipi correcte; recompte coherent; geometria i CRS comprovats; capa local reoberta; WMS comprovat amb connexió; dues obertures independents en una ubicació nova |
| Fitxers que cal conservar | `pr1-project-setup-cognom.gpkg`, `pr1-project-setup-cognom.qgz` i els apunts PDF, amb `cognom` substituït pel de l'estudiant |
:::

La primera comprovació es fa sobre les dades reobertes, no sobre el nom del fitxer: el terme ha de correspondre al municipi escollit i conservar l'identificador útil de la font. En una font amb una entitat per municipi, s'espera una entitat a la sortida. Si l'estructura de la font és diferent, cal explicar el recompte i comprovar que s'han conservat totes les parts del terme.

Els apunts segueixen el criteri del [capítol de documentació]({{ site.baseurl }}/ca/chapters/sintesi-documentacio/#apunts-projecte-municipal): cada captura sosté una decisió o un control i va acompanyada d'una explicació. El PDF ha de permetre localitzar les fonts, repetir la selecció i l'exportació i distingir com es desen i s'obren les dues representacions del projecte.

Les ampliacions poden afegir altres WMS, capes vectorials, simbologies, etiquetes, grups, mapes o composicions. S'han de poder obrir i explicar juntament amb el projecte, i els apunts n'han de justificar la funció. Afegir una composició no compensa una capa municipal absent del GeoPackage ni una ruta trencada.

Després de validar les dades es desen expressament el projecte incrustat `pr1` i la còpia externa `.qgz`, tots dos a `sandbox/` i amb la nomenclatura establerta. Amb QGIS tancat, la parella es copia conjuntament a `dist/` i s'hi afegeixen els apunts PDF revisats. El nom base dels fitxers geogràfics es manté; el PDF pot compartir aquest nom amb la seva extensió pròpia.

La prova final obre el `.qgz` i el projecte incrustat des d'una còpia en una ubicació nova. Les capes locals necessàries han d'apuntar al GeoPackage d'aquesta còpia i conservar contingut, CRS i configuració. El WMS es comprova amb connexió i el PDF, en un lector extern. Qualsevol reparació manual d'una ruta obliga a corregir el projecte de treball, tornar-lo a desar en totes dues representacions i repetir la prova.

>> **Resultat conservat.** El GeoPackage reuneix el terme municipal i el projecte incrustat `pr1`; el `.qgz` permet obrir-ne la representació externa; els apunts PDF expliquen com s'ha preparat i comprovat el conjunt. Aquesta instantània serà el punt de partida de la digitalització.
