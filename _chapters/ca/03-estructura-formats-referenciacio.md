---
layout: manual-chapter
title: Estructura, formats i referenciació
description: Models de dades, formats geogràfics, sistemes de referència i criteris per integrar capes sense falsejar-ne la posició.
lang: ca
ref: manual-data-structures-formats-crs
profiles: [unaltremanual]
content_status: draft
permalink: /ca/chapters/estructura-formats-referenciacio/
weight: 40
part: Continguts
manual_references: true
---

Dues capes poden representar el mateix territori i, tanmateix, no ser directament comparables. Una pot descriure municipis mitjançant polígons i una altra, elevacions mitjançant cel·les; poden utilitzar formats, resolucions, dates i sistemes de coordenades diferents. Integrar-les exigeix distingir què modelen, com s'estructuren, on s'emmagatzemen i què signifiquen les coordenades.

El nom d'un fitxer no resol aquestes preguntes. L'extensió informa del format, però no determina si la dada és adequada ni si el CRS declarat és correcte. Aquest capítol separa quatre conceptes que sovint es confonen: **model**, **estructura**, **format** i **sistema de referència de coordenades**.

>>>>> En acabar el capítol, cal poder diagnosticar l'estructura i la referenciació d'una capa abans de transformar-la o combinar-la.
>>>>>
>>>>> - Distingir model vectorial, model ràster, estructura interna i format d'emmagatzematge.
>>>>> - Triar un format segons edició, anàlisi, intercanvi i conservació.
>>>>> - Explicar què aporta un CRS i diferenciar assignació, transformació i visualització al vol.
>>>>> - Relacionar escala, resolució, precisió i exactitud amb l'ús previst.

## De la Terra a una parella de coordenades

Una coordenada és el final d'una cadena de decisions, no una etiqueta enganxada a un punt. El punt pertany primer a la Terra física. Per descriure'l cal adoptar una superfície i un marc de referència, expressar-ne la posició mitjançant un sistema de coordenades i, si es necessita un mapa pla, aplicar una projecció. Només aleshores apareixen nombres com longitud i latitud en graus o est i nord en metres.

La cadena es pot llegir en cinc passos: **lloc sobre la Terra**, **marc i superfície de referència**, **coordenades geogràfiques**, **projecció cartogràfica** i **coordenades planes**. Un sistema de referència de coordenades (CRS) identifica les regles necessàries per interpretar el resultat. Ometre'l deixa nombres sense unitats, eixos ni àrea d'ús coneguts.

![Seqüència des d'una posició sobre la Terra fins a les coordenades geogràfiques i les coordenades UTM d'un mapa pla]({{ site.baseurl }}/assets/quarto/03-estructura-formats-referenciacio/geographic-projected-utm.qmd "Una posició es relaciona amb un marc terrestre, s'expressa amb longitud i latitud i es projecta dins d'un fus UTM per obtenir coordenades d'est i nord; cada pas necessita una referència explícita."){: data-figure-width-web="48rem" data-figure-width-pdf="95%"}

>>>> **Una parella de nombres no identifica una posició per si sola.** Cal conservar com a mínim el CRS, l'ordre dels eixos i les unitats; quan l'exactitud ho exigeixi, també l'operació i l'època de les coordenades.

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

## Model, estructura i format

Model de dades
: Defineix com s'abstrau un fenomen. El model vectorial utilitza entitats discretes amb geometries i atributs; el model ràster divideix l'espai en una graella de cel·les i registra un valor per banda.

Estructura
: Descriu com s'organitzen les peces dins del model, com el tipus geomètric, els camps i les relacions d'un vector o les files, columnes, bandes, mida de cel·la i `NoData` d'un ràster.

Format
: Convenció que permet emmagatzemar o intercanviar una estructura de dades.

Cap model no és superior en tots els casos: l'elecció depèn de la pregunta, la naturalesa del fenomen i l'operació prevista {% cite longleyGeographicInformationScience2015 %}.

La distinció entre fenòmens discrets i camps continus ajuda a començar, però no és una regla automàtica. Límits municipals i fanals acostumen a representar-se com a entitats vectorials; l'elevació i la temperatura, com a camps ràster. Tanmateix, un camp continu es pot mostrejar amb punts i una categoria d'ús del sòl es pot codificar en una graella. El mètode d'observació i l'anàlisi prevista també intervenen en l'elecció.

Aquestes tres paraules responen, per tant, preguntes diferents. El model diu quina mena de món es construeix amb les dades; l'estructura diu quins elements i regles el formen; i el format diu com es codifica perquè un programa el pugui llegir o escriure. Canviar un Shapefile per un GeoPackage modifica l'emmagatzematge, però no converteix una línia central de carretera en una superfície viària. Vectoritzar un ràster, en canvi, sí que canvia el model i obliga a definir com les cel·les es converteixen en objectes, quins contorns se simplifiquen i quins valors es conserven.

També cal separar el **conjunt de dades** de la **capa**. Un conjunt de dades és una unitat identificable que pot contenir una o més capes, taules o bandes. Una capa és una vista organitzada d'un contingut espacial homogeni per treballar-hi al SIG. Un fitxer GeoPackage pot contenir moltes capes; un conjunt Shapefile representa normalment una sola capa; un GeoTIFF pot tenir diverses bandes; i un projecte QGIS pot enllaçar tots aquests recursos sense copiar-los dins del fitxer `.qgz`. L'arbre de capes que es veu a QGIS és una organització del projecte, no una descripció fiable de quants fitxers o contenidors hi ha al disc.

### Objectes discrets i camps

El model vectorial és especialment adequat quan interessa conservar la identitat d'objectes o unitats: cada municipi, tram, parcel·la o fanal pot tenir un identificador i un registre d'atributs. La geometria n'expressa una abstracció espacial i la taula permet descriure'n categoria, data, font o estat. Els límits poden ser nítids per convenció, com una divisió administrativa, encara que no siguin visibles sobre el terreny. La possibilitat de consultar cada entitat no implica, però, que la realitat estigui formada necessàriament per objectes independents; és una decisió del model.

El model ràster és especialment adequat quan una variable es concep com un camp observat o estimat sobre una graella. Cada cel·la ocupa una posició definida per l'origen, les dimensions, l'orientació i el CRS de la graella, i emmagatzema un valor per banda. Una ortofoto sol tenir bandes de resposta radiomètrica; un model digital d'elevacions, una banda d'altura; i un ràster classificat, codis de coberta. El significat d'un valor depèn del tipus de variable, de la unitat, del mètode de mostreig i de la convenció de `NoData`, no només del color amb què es representa {% cite felicisimoModelosDigitalesTerreno1994 %}.

La cel·la no és sempre una observació puntual situada al centre. En un producte pot representar una mitjana, una classe dominant, una mesura instantània, una estimació interpolada o una quantitat integrada sobre l'àrea. Tampoc no s'ha de confondre **píxel de pantalla** amb **cel·la de dades**: el primer depèn del dispositiu i del zoom; la segona forma part de l'estructura del ràster. Quan QGIS reescala la visualització, pot assignar molts píxels de pantalla a una cel·la o resumir moltes cel·les en un píxel sense canviar la resolució original.

La conversió entre vector i ràster sempre requereix una regla. Rasteritzar polígons obliga a triar mida i alineació de cel·la i a decidir quin valor rep una cel·la travessada per més d'una entitat. Vectoritzar classes ràster obliga a decidir quines cel·les formen una regió, com es tracta el veïnatge i quant se simplifica un contorn esglaonat. El resultat pot ser útil, però no és una còpia neutral: hereta la resolució d'origen i afegeix les decisions de conversió.

### Altres models amb un abast delimitat

Vector i ràster són les estructures generals del curs, però altres models conserven relacions que es perdrien si es forcés qualsevol dada dins de punts, línies o cel·les independents:

- Una **xarxa** afegeix nodes, connectivitat, direcció, costos i restriccions. Dues línies que es creuen en planta no queden connectades automàticament.
- Una xarxa irregular de triangles o **TIN** aproxima una superfície amb triangles i línies de ruptura, concentrant detall on varia el relleu {% cite felicisimoModelosDigitalesTerreno1994 %}.
- Un **núvol de punts** conserva grans volums de mostres 3D, sovint LiDAR o fotogramètriques, amb atributs d'adquisició; no equival operativament a una multipunt ordinària.
- Un **voxel** discretitza un volum, per exemple geològic, mentre que una **malla** connecta elements d'una superfície o un volum i associa valors a nodes, cares o cel·les.
- Una **cobertura** assigna valors a posicions d'un domini espacial o espaciotemporal; el ràster n'és una implementació habitual, però no l'única.
- Un **DGGS** divideix la Terra en cel·les jeràrquiques identificables per indexar i agregar dades a diverses resolucions.

Les tessel·les XYZ o WMTS són principalment una estratègia de distribució i memòria cau. Una imatge renderitzada pot haver perdut atributs i valors originals, i una vista 3D no prova que la font tingui Z ni un CRS vertical.

### Estructura lògica i estructura física

L'estructura lògica indica entitats, camps, relacions, bandes o cel·les; la física ordena bytes, índexs i taules. Dos GeoTIFF poden conservar els mateixos valors i tenir costos diferents de lectura segons l'organització en tires o blocs. Un índex espacial accelera consultes sense canviar les geometries.

L'esquema ha de declarar unitat d'observació, geometria o graella, camps o bandes, tipus, unitats, nuls, identificadors, CRS, temps i restriccions. Si el format de destinació trunca camps, converteix dates, elimina dominis o perd la referència vertical, la sortida pot obrir-se i no ser equivalent.

## Fitxers, conjunts i contenidors

Un **fitxer** és una unitat d'emmagatzematge, però una dada pot dependre de diverses peces: el Shapefile distribueix una capa i una imatge pot requerir un *world file* i un `.prj`. Un **contenidor** agrupa continguts gestionats; un `.gpkg` pot allotjar taules, índexs i metadades dins de SQLite. Ni la carpeta ni el contenidor substitueixen la còpia de seguretat i la documentació.

Una base espacial de servidor afegeix concurrència, permisos i transaccions multiusuari; compartir un GeoPackage en una carpeta sincronitzada no hi equival. El `.qgz` tampoc no és un contenidor de dades: conserva referències, estils, formularis i composicions, però no incorpora automàticament les fonts. El projecte del curs utilitza rutes relatives i manté el `.qgz` independent per fer visible aquesta dependència.

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

La taula `gpkg_extensions` declara funcionalitats addicionals, que poden ser compartides o pròpies d'un productor. `layer_styles` pot contenir estils de QGIS i `qgis_projects`, projectes; un altre client pot llegir les entitats i ignorar aquesta configuració. Al curs, `projecte_tig.qgz` continua sent la còpia canònica i l'entrada incrustada `projecte_tig` només s'actualitza a les fites explícites.

Durant una escriptura SQLite poden aparèixer fitxers `-journal`, `-wal` o `-shm`, que no s'han de separar ni eliminar. Abans de copiar el contenidor cal tancar les connexions i provar la còpia. Un GeoPackage en una carpeta sincronitzada no és una base multiusuari i pot patir conflictes si s'edita simultàniament.

### GeoJSON i TopoJSON per a intercanvi web

GeoJSON és un format textual basat en JSON, adequat per a respostes web i conjunts moderats. Una `Feature` associa una geometria amb `properties`, i una `FeatureCollection` n'agrupa diverses. La transparència del text facilita inspeccionar-lo, però repeteix noms i coordenades i no incorpora un índex espacial intern; no és la millor base general per editar un projecte gran {% cite butlerGeoJSON2016 %}.

RFC 7946 fixa les posicions en longitud i latitud, en aquest ordre, dins de WGS 84 segons `OGC:CRS84`. El membre `crs` antic ja no forma part d'aquest contracte. Una capa UTM destinada a GeoJSON s'ha de transformar en una sortida d'intercanvi i reobrir per comprovar geometries, atributs, extensió i ordre dels eixos. El nombre de decimals no certifica l'exactitud.

TopoJSON és una especificació comunitària que permet que línies i polígons facin referència a **arcs compartits** en lloc de repetir una frontera. Pot reduir la mida de cobertures administratives i mantenir la coincidència dels límits compartits, però té menys suport directe i no és un estàndard OGC o IETF {% cite bostockTopoJSON2013 %}.

La quantificació de TopoJSON ajusta coordenades a una graella i pot simplificar o col·lapsar detalls. Per això és una transformació amb pèrdua que exigeix conservar els paràmetres i validar recompte, propietats, extensió i geometries. Al projecte del curs, GeoPackage continua sent el format de treball; GeoJSON o TopoJSON només són sortides d'intercanvi quan el destinatari les necessita.

### GeoTIFF i COG

TIFF és un contenidor flexible d'imatges. **GeoTIFF** hi incorpora etiquetes que relacionen files i columnes amb un espai de model i descriuen el CRS. Un GeoTIFF pot contenir una o més bandes, mostres enteres o de coma flotant, diferents compressions i una organització en tires o blocs. El sufix `.tif` no demostra que hi hagi georeferenciació ni que el CRS sigui complet: cal inspeccionar les etiquetes i l'extensió espacial.

Per a un ràster analític s'han de documentar files, columnes, nombre de bandes, tipus de mostra, resolució, origen, extensió, CRS, unitats de cada banda i `NoData`. La compressió sense pèrdua, com DEFLATE, LZW o altres opcions admeses pel lector de destinació, conserva els valors; una compressió amb pèrdua com JPEG pot ser adequada per a determinada imatge visual, però no per a valors categòrics o mesures que s'han de recuperar exactament. El tipus de dada també importa: convertir elevacions decimals a enters o nombres amb signe a un tipus sense signe pot truncar o reinterpretar valors.

L'organització en blocs permet llegir una finestra sense recórrer tot el ràster. Les **piràmides** o vistes de resolució reduïda acceleren la visualització a escales petites, però els seus valors depenen del mètode de remostreig. Per a una ortofoto pot convenir una mitjana; per a classes de sòl, el veí més proper o una moda, segons la finalitat. La piràmide no substitueix les dades de resolució completa i no ha de participar inadvertidament en un càlcul que les necessiti.

Un **Cloud Optimized GeoTIFF** (COG) és un GeoTIFF organitzat internament amb blocs, nivells reduïts i una disposició dels índexs i bytes que permet peticions parcials. Quan el servidor admet sol·licituds HTTP de rang i el client entén l'estructura, només cal descarregar els blocs i el nivell necessaris. Un fitxer no esdevé COG perquè es canviï el nom o perquè tingui `.tif`; s'ha de crear i validar amb el perfil corresponent. Inversament, un COG continua sent llegible com a GeoTIFF per molts clients que no n'aprofiten l'accés parcial.

COG millora l'accés, no la qualitat intrínseca. Un COG pot conservar un CRS equivocat, un `NoData` mal definit, valors amb una compressió inadequada o una resolució que no respon a la pregunta. Tampoc no assegura rapidesa si el servidor no accepta rangs, si els blocs són inadequats o si l'operació necessita gairebé totes les cel·les. Per al curs, la distinció inicial és suficient: GeoTIFF descriu la graella georeferenciada; COG n'afegeix una organització pensada per a lectura parcial remota.

### ASCII Grid i georeferenciació lateral

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

La **interoperabilitat** exigeix que dos programes interpretin de manera compatible geometries, camps, nuls, text, dates, CRS i extensions, no només que obrin el fitxer.

GeoJSON utilitza UTF-8 i GeoPackage no necessita `.cpg`; en Shapefile, el `.cpg` i la pàgina de codis dBase poden faltar o discrepar. Cal rellegir els bytes amb la codificació documentada, no substituir accents manualment. Els tipus també s'han de conservar: `00123` pot ser text, una data no és una cadena, i `NULL`, buit, zero i `-9999` no són equivalents. La truncació de noms pot crear col·lisions que obliguen a actualitzar expressions i diccionaris.

La sortida s'ha de reobrir com una font nova i comparar recompte, geometria, esquema, nuls, caràcters, identificadors, extensió, CRS i valors. En ràster s'afegeixen dimensions, bandes, tipus, resolució, alineació i `NoData`. Un checksum només prova identitat de bytes.

## Detalls de coordenades i referències

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

En QGIS, el mateix selector pot aparèixer en configurar el projecte, declarar la referència d'una font o definir la sortida d'un algorisme. La captura només verifica quina definició s'ha triat; l'eina des d'on s'ha obert determina si s'està canviant la vista, assignant significat a unes coordenades existents o preparant una transformació.

![Selector de CRS de QGIS amb la cerca del codi 25831, ETRS89 UTM zona 31N seleccionat i la seva àrea d'ús visible]({{ site.baseurl }}/assets/img/qgis/qgis-crs-selection.png "Cercar per codi redueix l'ambigüitat, però abans d'acceptar cal comprovar el nom complet, les unitats i l'àrea d'ús. El selector identifica una definició; no indica per si sol si QGIS l'aplicarà al projecte, a la font o a una sortida transformada."){: data-figure-width-web="38rem" data-figure-width-pdf="78%"}

### Assignar, transformar i visualitzar

Assignar un CRS
: Declara què signifiquen unes coordenades existents sense modificar-ne els valors. Només corregeix metadades absents o equivocades quan es coneix la referència real.

Reprojectar o transformar
: Calcula coordenades noves en un altre CRS mitjançant una operació espacial explícita.

Visualitzar al vol
: Fa coincidir capes al llenç sense canviar el CRS ni les coordenades emmagatzemades a la font.

Confondre assignació i transformació pot desplaçar una capa milers de quilòmetres o ocultar visualment un error. Abans de calcular distàncies, àrees o resolucions cal inspeccionar el CRS de cada entrada, el CRS de sortida i l'operació aplicada.

>>>> **El CRS que apareix a la barra del projecte no identifica necessàriament el CRS de la capa activa.** La comprovació s'ha de fer a la informació de cada font. Canviar el CRS del projecte pot modificar la visualització sense corregir una capa mal declarada.

Una **conversió de coordenades** canvia el sistema de coordenades sense canviar el dàtum, com el pas d'ETRS89 geogràfic a ETRS89 / UTM zona 31N. Una **transformació de coordenades** relaciona marcs o datums diferents, com ED50 i ETRS89. Una operació real pot concatenar diversos passos: desprojectar, transformar el marc amb una graella i projectar al destí. En l'ús general de QGIS, «reprojectar» s'empra sovint per a tota la cadena; documentar origen, destinació i operació evita que aquesta simplificació amagui què s'ha calculat.

### Operacions candidates i graelles de transformació

Entre dos CRS hi pot haver més d'una operació candidata. Cadascuna té una àrea d'ús, una exactitud declarada, uns paràmetres i, de vegades, dependències de fitxers. QGIS i PROJ seleccionen operacions a partir de les definicions, l'extensió i els recursos disponibles, però la selecció automàtica s'ha de revisar quan el canvi de dàtum afecta el resultat o quan es necessita una exactitud concreta {% cite qgisUserGuide344 %}.

Una **graella de transformació** conté correccions que varien segons la posició i té cobertura, resolució i versió pròpies. Si falta una graella o una època necessària, QGIS pot oferir una operació aproximada, però el programari no pot inventar la informació absent. Cal registrar l'operació triada, qualsevol recurs extern i l'avís d'exactitud; una posició coneguda detecta errors grossos, però no substitueix un control geodèsic quan es demana precisió topogràfica.

### Quan cal materialitzar una reprojecció

La visualització al vol és apropiada per explorar capes amb CRS diferents i pot ser suficient quan l'algorisme declara que transforma les entrades i calcula en un CRS adequat. No cal exportar físicament totes les capes al mateix CRS abans de qualsevol anàlisi. Cal, però, saber si el procés adopta el CRS d'una entrada, el del projecte o un CRS de sortida, i en quines unitats interpreta les distàncies.

Materialitzar una capa transformada és convenient quan s'ha de distribuir en un format amb un CRS fix, quan moltes operacions repetiran la mateixa transformació, quan el programari receptor no transforma al vol, quan cal congelar una operació i una graella per reproduïbilitat o quan les unitats de treball han de quedar inequívocament en la font. La sortida ha de tenir un nom nou, conservar l'original i registrar CRS d'origen, CRS de destinació i operació.

En vector, la transformació recalcula cada vèrtex. Les línies rectes en un CRS poden esdevenir corbes en un altre, però una geometria segmentada només en transforma els vèrtexs existents; en trajectes llargs pot caldre densificar abans si s'ha de representar bé la corba. En ràster, la reprojecció crea una graella nova i necessita resolució, extensió, alineació i mètode de remostreig. El veí més proper sol preservar codis categòrics; mètodes interpoladors poden ser adequats per a camps continus, però creen valors nous. Aquesta diferència fa especialment inadequat reprojectar ràsters repetidament només per uniformar una carpeta.

### Comprovacions operatives a QGIS

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

>>> **Assignació o reprojecció.** Desactiveu temporalment una capa de referència i llegiu una coordenada concreta en el CRS de la font i en el del projecte. Si en canviar només el CRS del projecte la capa continua al mateix lloc visual, està actuant la transformació al vol. Si s'exporta una còpia i els valors numèrics canvien però la posició coincideix, s'ha materialitzat una reprojecció. Si els nombres no canvien després d'«assignar» un altre codi i la capa salta de lloc, s'ha canviat el significat sense transformar-la.

## Resolució, precisió i exactitud

Resolució espacial
: Mida de la cel·la o unitat mínima de mostreig d'un ràster; no expressa l'error de l'observació.

Precisió
: Grau de detall numèric o de repetibilitat d'una mesura.

Exactitud
: Proximitat d'una observació o resultat a una referència adequada.

Totes tres propietats s'han d'interpretar juntament amb l'escala de producció i de sortida.

Afegir decimals o vèrtexs no millora l'exactitud d'una font. Una ortofoto de píxel petit pot conservar un desplaçament i una geometria detallada pot ser menys exacta que un límit oficial simplificat. La transformació de coordenades només afegeix un component al pressupost d'incertesa: una operació centimètrica no converteix en centimètric un límit ambigu digitalitzat sobre una imatge mètrica.

També s'han de comparar data, unitat d'observació i generalització. Un eix viari i un polígon de calçada poden compartir CRS i representar objectes diferents; una ortofoto de 2024 i un inventari de 2018 poden estar alineats i discrepar per un canvi real. Més classes no impliquen més exactitud si la font no permet distingir-les. Les xifres finals han de reflectir el component menys precís que condiciona la pregunta.

## Diagnòstic abans de convertir

Quan una capa no encaixa, el diagnòstic ha de precedir la conversió. Cal comprovar l'extensió numèrica, les unitats plausibles, el CRS declarat, el format, les metadades i una posició coneguda. Després es pot decidir si falta assignar la referència correcta, si cal transformar les coordenades o si les dades no són compatibles.

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

## Activitats

### Fitxa comparativa de quatre recursos

El resultat conservat serà una fitxa d'una capa municipal, una ortofoto, un model d'elevacions i una taula CSV amb coordenades. Per a cada recurs identificarà model, estructura, format, CRS, unitat d'observació, escala o resolució, font i data. La conclusió explicarà per què compartir extensió territorial no implica compartir model, resolució ni aptitud analítica, i distingirà quins elements pertanyen a una imatge i quins a un mapa.

### Registre d'assignació i reprojecció

La pràctica partirà d'una capa amb el CRS correctament declarat i d'una còpia sense aquesta informació. El diari conservarà les prediccions i els resultats observats en assignar la definició correcta, assignar-ne una d'incorrecta i reprojectar l'original. Per a cada estat registrarà els valors d'una coordenada, l'extensió, el CRS declarat i la posició respecte d'una font de referència. Les còpies de prova descartades no s'incorporaran com a resultats finals.

>>>> **Canviar el format o el CRS del projecte no repara una capa mal referenciada.** Una correcció només és justificable si la font permet saber què significaven les coordenades originals; en cas contrari, la incertesa s'ha de conservar i la capa es pot haver de descartar.

### Fita del projecte: formats i CRS comprovats

L'inventari del projecte s'actualitzarà amb el model, el format, el CRS, l'escala o resolució i la data del WMS de context, del límit municipal oficial del CNIG i de les altres fonts incorporades. Quan correspongui, també registrarà ordre dels eixos, referència vertical, codificació, valor nul, extensió utilitzada i operació de coordenades prevista. Si l'original és un Shapefile, l'inventari identificarà el conjunt complet i no només el `.shp`.

Per a cada conversió realment necessària es conservaran l'entrada original, la sortida amb un nom funcional i els controls de recompte, esquema, nuls, extensió, CRS i una posició coneguda. Si l'eina posterior transforma de manera explícita i segura, no es crearà una còpia redundant: el resultat observable serà la decisió documentada, amb el CRS i les unitats efectives del càlcul.

La fita es tanca desant primer `projecte_tig.qgz`, comprovant que el WMS continua separat de les entrades analítiques i que el límit municipal preparat conserva identificador, geometria, CRS i extensió, i actualitzant després l'entrada incrustada `projecte_tig` del GeoPackage. Des d'una còpia de l'arbre es tornaran a obrir per separat el `.qgz` i el projecte incrustat, sense utilitzar la llista de projectes recents.

>> **Resultat de la fita.** Es conserven l'inventari actualitzat, els controls de format i CRS, les conversions justificades, el diari, el `.qgz` canònic i la representació incrustada `projecte_tig` comprovada. Desar una representació no sincronitza l'altra i la fita incrustada no és una còpia de seguretat del GeoPackage que la conté.
