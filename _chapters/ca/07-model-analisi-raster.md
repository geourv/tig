---
layout: manual-chapter
title: Model i anàlisi ràster
description: Graelles, resolució, relleu, àlgebra de mapes i estadístiques zonals per interpretar dades ràster.
lang: ca
ref: manual-raster-model-analysis
profiles: [unaltremanual]
content_status: draft
permalink: /ca/chapters/model-analisi-raster/
weight: 80
part: Continguts
manual_references: true
---

El model vectorial identifica entitats; el model ràster representa una cobertura espacial mitjançant una graella regular. Cada cel·la ocupa una porció del territori i conté un valor per banda. Aquesta estructura és adequada per descriure camps que varien de manera contínua, com l'elevació o la temperatura, però també pot codificar categories, imatges, recomptes i màscares lògiques. El fet que totes aquestes dades comparteixin files i columnes no significa que admetin les mateixes operacions.

La simplicitat aparent de la graella amaga decisions determinants. La mida de cel·la, l'origen, l'extensió, el mètode de remostreig i el tractament de `NoData` poden canviar pendents, superfícies i coincidències. Comparar dos ràsters exigeix comprovar que comparteixen un contracte espacial i semàntic coherent abans d'aplicar una operació cel·la a cel·la. La resolució tampoc no és sinònim d'exactitud: una graella fina pot contenir una superfície interpolada, una classificació incerta o valors procedents d'una font menys precisa {% cite felicisimoModelosDigitalesTerreno1994 longleyGeographicInformationScience2015 qgisUserGuide344 %}.

>>>>> En acabar el capítol, cal poder preparar, analitzar i comparar ràsters sense confondre resolució, exactitud ni absència de dades.
>>>>>
>>>>> - Interpretar cel·les, bandes, resolució, extensió, origen, alineació, tipus i `NoData` com un únic contracte de graella.
>>>>> - Distingir variables contínues, categories, màscares, magnituds extensives i models d'elevacions.
>>>>> - Calcular i interpretar derivats del terreny, reclassificacions, distàncies i expressions de mapes.
>>>>> - Relacionar valors ràster amb zones vectorials, quantificar incertesa i comprovar l'efecte de la resolució.

## El ràster com a model del territori

Una graella no és una col·lecció desordenada de quadrats. Les files i les columnes formen un sistema de localització implícit: una vegada coneguts l'origen, la mida de cel·la i el sistema de referència de coordenades (`CRS`), la posició de cada valor es deriva del seu índex. Aquesta regularitat fa eficients les operacions locals, els filtres de veïnatge i l'emmagatzematge de superfícies, perquè no cal repetir dues coordenades per a cada cel·la. A canvi, totes les observacions queden sotmeses a una mateixa partició de l'espai.

La cel·la té una **extensió espacial**, no és només un punt acolorit a la pantalla. Segons el producte, el valor pot representar una observació al centre, una mitjana sobre l'àrea, la classe dominant, un recompte, una probabilitat o el resultat d'una interpolació. Un píxel de 25 m d'un model d'elevacions no implica necessàriament que s'hagi mesurat tota la superfície de 625 m² ni que la cota sigui una mitjana exacta d'aquesta àrea. Aquesta semàntica s'ha de recuperar de les especificacions del producte i conservar al diari.

El terme **píxel** descriu l'element d'una imatge digital i sovint s'utilitza com a sinònim pràctic de cel·la. En anàlisi territorial és preferible parlar de cel·la quan es vol remarcar el suport geogràfic del valor. El zoom només amplia la representació del mateix píxel; no redueix la mida de cel·la ni revela observacions noves. De la mateixa manera, remostrejar una graella de 25 m a 5 m crea més files i columnes, però els valors addicionals deriven dels originals i no constitueixen una mesura de més detall.

La distinció habitual entre **objectes discrets** i **camps continus** orienta l'elecció entre vector i ràster, però no la resol mecànicament. Una carretera es pot modelar com una línia connectada, com la superfície pavimentada d'un polígon o com cel·les d'una imatge. Una coberta del sòl està formada per classes, però es pot emmagatzemar en una graella per analitzar-la conjuntament amb elevació, clima o teledetecció. El model adequat és el que conserva les relacions necessàries per a la pregunta i fa visibles les simplificacions introduïdes.

## Geometria i alineació de la graella

La geometria completa d'un ràster es pot descriure amb el `CRS`, l'extensió, l'origen, la mida de cel·la, el nombre de files i columnes i, si existeix, la rotació. En una graella orientada al nord, les columnes avancen habitualment cap a l'est i les files cap al sud des de la cantonada superior esquerra. Tanmateix, el fitxer pot conservar una transformació afí més general, amb píxels rectangulars o eixos girats. Pressuposar sempre cel·les quadrades i sense rotació pot fer que una exportació canviï lleugerament la posició o l'àrea representada.

::: table "Propietats que defineixen una graella ràster"
| Propietat | Significat | Error que evita comprovar-la |
| --- | --- | --- |
| `CRS` | Referència, eixos i unitats de les coordenades | Superposicions, distàncies o àrees incoherents |
| Extensió | Límits externs del rectangle cobert | Comparar àmbits diferents com si fossin equivalents |
| Origen | Punt a partir del qual es disposen files i columnes | Desplaçar tota la malla una fracció de cel·la |
| Mida de cel·la | Amplada i alçada del suport espacial | Confondre detall espacial amb zoom de pantalla |
| Files i columnes | Dimensions discretes de la matriu | Acceptar una extensió o resolució arrodonida de manera inesperada |
| Alineació | Coincidència de les línies de separació entre cel·les | Operar amb valors que no representen la mateixa superfície |
| Bandes | Variables o components co-registrats | Analitzar una banda diferent de la prevista |
| Tipus de dada | Rang, signe i precisió numèrica | Desbordar, truncar o inflar els valors i els fitxers |
| `NoData` o màscara | Regla que identifica cel·les no vàlides | Interpretar absència com un valor real |
:::

En una graella no girada, l'amplada de l'extensió hauria de correspondre al nombre de columnes multiplicat per la mida horitzontal de cel·la, i l'alçada, al nombre de files multiplicat per la mida vertical. Si el quocient no és enter, l'eina de creació haurà d'arrodonir dimensions, ampliar l'extensió o alterar lleugerament la resolució. Aquest comportament no s'ha de deixar implícit. Una extensió de sortida per a cel·les de 200 m s'ha d'ajustar a múltiples de 200 m respecte d'un origen declarat abans de calcular-ne les dimensions.

L'**origen** pot descriure la cantonada exterior de la graella, mentre que altres fitxers o convencions donen la coordenada del centre de la primera cel·la. La diferència és de mitja cel·la. No es resol comparant només els nombres de resolució: cal inspeccionar l'extensió i, si és necessari, calcular les coordenades dels centres i dels límits. Aquesta comprovació és especialment important quan es combinen un ASCII Grid, una imatge amb fitxer de georeferenciació extern i un GeoTIFF.

Dues graelles poden tenir el mateix `CRS`, la mateixa extensió aproximada i una resolució de 25 m, però continuar desalineades. Si una comença a `x = 300000` i una altra a `x = 300012,5`, les línies de cel·la no coincideixen. Una calculadora ràster haurà de remostrejar-ne almenys una, encara que la interfície no faci prou visible aquesta decisió. L'alineació exigeix que la diferència entre els orígens sigui un múltiple enter de la mida de cel·la en tots dos eixos.

![Comparació d'una graella alineada amb una graella desplaçada mitja cel·la tot i compartir una mida de cel·la de 25 metres]({{ site.baseurl }}/assets/diagrams/ca/07-model-analisi-raster/raster-grid-alignment.mmd "Dues graelles de 25 m queden alineades quan els orígens difereixen un nombre enter de cel·les; amb un desplaçament de mitja cel·la, els límits ja no coincideixen."){: data-figure-width-web="40rem" data-figure-width-pdf="90%"}

Una graella de 200 m pot quedar **niada** dins d'una de 25 m perquè 200 és vuit vegades 25. Cada cel·la grossa contindria aleshores 8 × 8, és a dir, 64 cel·les fines. Aquesta relació només es compleix si les dues graelles comparteixen origen, orientació i límits compatibles. El simple fet d'escollir dues resolucions divisibles no crea el niament.

### Bandes, tipus i valors codificats

Una **banda** és una matriu de valors que comparteix la geometria del conjunt ràster. Una ortoimatge pot tenir bandes roja, verda, blava i infraroja; una sèrie o un producte multidimensional pot representar dates o variables; un model d'elevacions acostuma a tenir una sola banda. Les bandes d'un mateix fitxer solen estar co-registrades, però no s'ha de suposar que tenen la mateixa unitat, escala numèrica o significat. El nom i les metadades de cada banda formen part de l'entrada analítica.

El **tipus de dada** determina els valors que es poden emmagatzemar. Un enter sense signe és eficient per a codis o valors no negatius; un enter amb signe permet valors negatius; la coma flotant conserva decimals i un rang ampli, però ocupa més espai i introdueix les aproximacions pròpies de l'aritmètica binària. Escollir `Float64` per a una màscara de 0 i 1 malgasta espai, mentre que convertir elevacions decimals a enter pot truncar informació. També cal comprovar si el producte aplica un factor d'escala i un desplaçament: un enter emmagatzemat pot representar un valor físic decimal després d'aquesta conversió.

::: table "Tipus numèric i ús analític orientatiu"
| Necessitat | Tipus habitual | Control necessari |
| --- | --- | --- |
| Màscara 0/1 o classe amb pocs codis | Enter sense signe compacte | Reservar un codi o una màscara separada per a l'absència |
| Recompte | Enter amb rang suficient | Preveure el màxim i evitar desbordaments en sumes |
| Elevació o variable física amb decimals | Coma flotant | Conservar unitat, precisió útil i `NoData` compatible |
| Diferència que pot ser negativa | Enter amb signe o coma flotant | No exportar a un tipus que converteixi negatius en valors extrems |
| Imatge multibanda escalada | Enter més factor d'escala, segons el producte | Aplicar escala i desplaçament abans d'interpretar el valor físic |
:::

Els codis de classe no són magnituds encara que s'emmagatzemin com a nombres. En una coberta del sòl, `1 = bosc`, `2 = conreu` i `3 = urbà` no impliquen que urbà sigui tres vegades bosc ni que la mitjana entre bosc i urbà sigui conreu. La taula de classes, la paleta i les etiquetes han de viatjar amb la dada o quedar documentades separadament. Ordenar els codis per conveniència tampoc converteix automàticament una variable nominal en ordinal.

### `NoData`, màscares i transparència

`NoData` indica que una cel·la no té un valor vàlid per a aquella banda. Pot correspondre a una zona fora de cobertura, a un núvol, a aigua exclosa del producte, a una fallada de sensor o a una operació que no es pot calcular. Aquestes causes no són equivalents. Si una anàlisi necessita diferenciar-les, un únic codi d'absència és insuficient i cal conservar una capa de qualitat o una classificació de motius.

`NoData` no és zero. En un model d'elevacions, 0 m pot ser una cota vàlida; en una distància, 0 identifica la font; en una màscara binària, 0 pot significar que la condició és falsa. Substituir absències per zero incorpora observacions inexistents al càlcul i pot abaixar mitjanes, crear costes artificials o convertir àrees no avaluades en àrees que no compleixen el criteri.

La validesa es pot expressar mitjançant un valor sentinella, una màscara interna o externa i, en alguns productes d'imatge, un canal alfa de transparència. La transparència és sobretot una propietat de representació i no sempre equival a una màscara analítica. Un valor sentinella, com `-9999`, només és segur si queda fora del domini possible; en una conversió de tipus o d'unitat podria col·lidir amb un valor real. Els ràsters de coma flotant també poden utilitzar `NaN`, però el comportament de les eines s'ha de provar en lloc de pressuposar-lo.

El tractament de `NoData` durant el remostreig varia segons l'algorisme i els paràmetres. Una interpolació pot ignorar veïns no vàlids i renormalitzar els pesos, exigir un nombre mínim de valors o propagar l'absència. Qualsevol opció modifica la vora de la cobertura. Per això cal comparar el nombre de cel·les vàlides abans i després, inspeccionar el litoral o els buits i registrar la política utilitzada. Una sortida visualment contínua pot haver emplenat zones que la font declarava desconegudes.

## Formats ràster i organització interna

El model i el format resolen preguntes diferents. El model defineix què significa la graella; el format determina com es conserven la matriu, la georeferenciació, les bandes i altres metadades. Convertir un ASCII Grid a GeoTIFF pot millorar el rendiment i la portabilitat, però no corregeix una resolució inadequada, un origen erroni ni una referència vertical desconeguda. En el curs, GDAL actua sovint sota les eines de QGIS per llegir, transformar i escriure aquests formats {% cite qgisUserGuide344 rouaultGDAL2026 %}.

### GeoTIFF i COG

Un **GeoTIFF** és un fitxer TIFF que incorpora etiquetes per relacionar els píxels amb coordenades i descriure el sistema de referència. Pot contenir una o diverses bandes, tipus enters o de coma flotant, compressió, blocs interns, `NoData` i piràmides, segons el perfil i les eines utilitzades. La georeferenciació integrada redueix el risc de separar la imatge del fitxer que la posiciona, però no eximeix de comprovar si el `CRS`, l'extensió i el valor d'absència són correctes {% cite ogcGeoTIFF2019 %}.

Un **COG** (*Cloud-Optimized GeoTIFF*) continua sent un GeoTIFF.

La diferència és l'organització interna: els blocs de dades i, quan n'hi ha, els nivells de resolució es disposen perquè un client pugui demanar només els fragments necessaris mitjançant peticions parcials. Això permet consultar una finestra o una vista general d'un fitxer remot sense descarregar-lo complet. Canviar el nom d'un `.tif` o afegir-hi la paraula `cog` no el converteix en COG; la disposició s'ha de crear i validar. Tampoc no millora l'exactitud ni la resolució de les dades: resol un problema de distribució i accés {% cite ogcCOG2023 %}.

### ASCII Grid

L'**ASCII Grid** emmagatzema una graella d'una banda com a text. L'encapçalament habitual declara `ncols`, `nrows`, `xllcorner` i `yllcorner` o les variants referides al centre, `cellsize` i `NODATA_value`; a continuació apareixen els valors per files. La transparència del text és útil per inspeccionar una matriu petita, explicar un model o intercanviar dades amb programari senzill.

::: listing "Encapçalament il·lustratiu d'un ASCII Grid de 25 m"
```text
ncols         6
nrows         5
xllcorner     300000
yllcorner     4600000
cellsize      25
NODATA_value  -9999
12 11 10 9 8 7
13 12 11 10 9 8
...
```
:::

La llegibilitat té costos. Els nombres en text ocupen més que una codificació binària, no hi ha compressió ni piràmides integrades comparables a les d'un GeoTIFF i la precisió pot canviar si l'exportació limita els decimals. La forma bàsica amb `cellsize` pressuposa cel·les quadrades; algunes variants admeten altres camps, però no s'han de donar per compatibles sense prova. El `CRS` tampoc no queda habitualment definit dins de l'encapçalament i necessita metadades o un fitxer lateral. En convertir-lo, cal comprovar especialment si les coordenades inferiors es referien al centre o a la cantonada de la cel·la.

### Imatges amb fitxer de món

Una imatge TIFF, JPEG o PNG pot quedar situada mitjançant un **fitxer de món** (*world file*) adjacent. Les extensions habituals són `.tfw`, `.jgw`, `.pgw` o la forma genèrica `.wld`. El fitxer conté sis coeficients d'una transformació afí: escala horitzontal, dos termes de rotació, escala vertical i coordenades del centre del píxel superior esquerre. En una imatge orientada al nord, els termes de rotació són zero i l'escala vertical sol ser negativa perquè les files avancen cap avall.

El fitxer de món no declara per si sol el `CRS`, les unitats temàtiques, les bandes ni `NoData`. Sovint necessita un `.prj` i metadades addicionals. També es pot perdre o desincronitzar si es canvia el nom només a una de les peces. Quan una imatge conté georeferenciació interna i també un fitxer de món, una discrepància entre tots dos exigeix diagnòstic: no s'ha de triar automàticament la versió que fa encaixar millor la capa. Un GeoTIFF coherent és preferible per al treball analític perquè redueix aquestes dependències laterals.

### Compressió, blocs i piràmides

La **compressió sense pèrdua**, com LZW, Deflate o ZSTD quan l'entorn destinatari l'admet, redueix l'espai sense modificar els valors descomprimits. L'eficiència depèn del tipus i del patró de les dades: una classificació amb grans zones repetides es pot comprimir molt, mentre que una superfície sorollosa de coma flotant pot reduir-se menys. La compressió JPEG és amb pèrdua i pot ser adequada per a determinades imatges de visualització; no és apropiada per a elevacions, codis categòrics o altres ràsters analítics que necessiten recuperar exactament els valors.

El **tessel·lat intern** divideix el fitxer en blocs rectangulars. Una lectura d'una finestra només necessita els blocs que la cobreixen, mentre que una organització per tires pot obligar a llegir porcions més extenses. La mida de bloc és una decisió de rendiment, no la resolució espacial de la dada. Tampoc no s'ha de confondre un bloc intern amb les tessel·les XYZ o WMTS d'un mapa web: totes dues tècniques divideixen dades, però tenen contractes i finalitats diferents.

Les **piràmides** o *overviews* són còpies reduïdes per a escales de visualització més petites. QGIS pot mostrar un ràster gran amb molta més rapidesa si llegeix el nivell adequat en lloc de resumir el detall complet a cada moviment. El mètode de generació ha de respectar la semàntica: mitjana per a una superfície contínua quan es vol una vista agregada, i veí més proper o moda per a categories. Una piràmide accelera la representació; no s'ha d'utilitzar com si fos automàticament una capa analítica de resolució més grossa sense documentar com es va crear.

Les piràmides poden quedar dins del GeoTIFF o en fitxers externs. Generar-les internament modifica el fitxer i, per tant, qualsevol suma de comprovació registrada. Les estadístiques, paletes i altres auxiliars també poden aparèixer en fitxers laterals com `.aux.xml`. Abans de traslladar o publicar una capa cal identificar quines peces són necessàries, quines són memòria cau regenerable i quines contenen metadades que no es poden perdre.

## Preparació, mosaic i retall

Els productes extensos es distribueixen sovint en **tessel·les**. Abans d'unir-les cal comprovar que comparteixen producte, data o campanya compatible, `CRS`, mida i alineació de cel·la, nombre de bandes, tipus, escala, referència vertical i política de `NoData`. Dues peces que encaixen geomètricament poden provenir d'edicions diferents o aplicar tractaments distints a l'aigua i a la vegetació. La línia de contacte s'ha d'inspeccionar tant visualment com amb perfils o diferències de valors.

Un **ràster virtual**, habitualment un VRT en l'ecosistema GDAL, descriu com es combinen les fonts sense copiar immediatament tots els píxels. És eficient per explorar un mosaic i evita una duplicació gran, però depèn de les rutes i dels fitxers originals. Un mosaic materialitzat crea un nou GeoTIFF amb valors propis, necessita espai i ha de registrar la procedència, l'ordre de solapament i qualsevol remostreig. Si dues tessel·les se superposen, cal saber quina preval o com es combinen; la unió no és només enganxar rectangles.

El **retall rectangular** redueix el volum a una extensió. Si els límits es fan coincidir amb la graella de referència, pot conservar exactament els píxels originals. El **retall per màscara** aplica una geometria vectorial i decideix quines cel·les queden vàlides dins del polígon. Com que un límit vectorial pot travessar una cel·la, l'algorisme ha d'adoptar una regla, per exemple considerar el centre o incloure qualsevol cel·la tocada. Aquesta elecció altera sobretot zones petites, estretes o amb perímetres complexos.

Retallar massa aviat pot eliminar context necessari. Un pendent necessita veïns, una mitjana focal necessita la finestra completa, una distància necessita conèixer fonts properes de fora del municipi i una conca hidrogràfica pot rebre flux d'aigües amunt. Per això els càlculs es faran sobre una regió d'interès amb marge justificat i es retallaran al límit d'informe després. El marge no és sempre el mateix: ha de cobrir, com a mínim, el radi màxim del veïnatge o la distància d'influència i, en processos hidrològics, pot exigir tota la conca contribuent.

## Semàntica i remostreig dels valors

El **remostreig** estima quin valor correspon a cada cel·la d'una graella de destinació. Apareix quan canvien la resolució, l'origen o el `CRS`, i també quan un canvi d'extensió obliga a crear una graella diferent. Un retall rectangular alineat amb les vores de la malla pot conservar exactament les cel·les font i no necessita estimar-ne valors nous. Encara que la interfície presenti aquestes operacions per separat, una reprojecció ràster sempre necessita decidir on queda la nova graella i com obté els seus valors. El mètode s'ha de triar segons què representa la banda i segons si es redueix o s'augmenta la mida de cel·la.

Una variable **contínua** pot prendre valors intermedis dins del seu domini: elevació, temperatura o concentració en són exemples habituals. Una variable **categòrica** assigna etiquetes nominals o ordinals, com tipus de coberta o nivell de qualitat. Una magnitud **intensiva**, com una temperatura mitjana o una proporció, no creix pel simple fet d'ampliar l'àrea; una magnitud **extensiva**, com un total de població distribuït en cel·les, sí que s'ha de conservar quan s'agrega. Aquesta darrera distinció impedeix aplicar la mitjana a totals o la suma a valors que ja són densitats.

::: table "Mètodes de remostreig i conseqüències"
| Mètode | Com obté el valor | Ús orientatiu | Precaució |
| --- | --- | --- | --- |
| Veí més proper | Copia el centre de font més pròxim | Categories, identificadors i màscares | Conserva codis però desplaça vores i pot alterar freqüències |
| Bilineal | Mitjana ponderada dels quatre centres pròxims | Superfícies contínues | Suavitza valors i no és vàlida per a codis de classe |
| Cúbic | Interpola amb un veïnatge més gran | Imatges o superfícies contínues quan es justifica | Pot crear oscil·lacions o valors fora del rang original |
| Mitjana | Agrega contribucions dins de la cel·la de destinació | Reducció de resolució de valors continus o intensius | Canvia el suport i redueix extrems locals |
| Moda | Tria la categoria més freqüent | Generalització de classes | Pot eliminar classes minoritàries però territorialment rellevants |
| Suma | Acumula magnituds extensives | Recomptes o totals distribuïts | Només conserva el total si l'algorisme tracta correctament les àrees parcials |
| Mínim o màxim | Reté un extrem del conjunt contribuent | Aplicacions on l'extrem és la pregunta | No representa el valor típic i és sensible a errors locals |
:::

El veí més proper copia el valor d'una sola cel·la font i, per tant, no crea codis intermedis, però no conserva necessàriament la superfície de cada classe. Una carretera d'una cel·la d'amplada pot desaparèixer en una graella més grossa si cap centre de destinació la selecciona. La moda, el mínim i el màxim també retenen valors presents al domini font, però els obtenen d'un conjunt de cel·les i responen criteris diferents. En particular, la moda substitueix la diversitat interna per la classe dominant. Si les classes rares són l'objecte de l'estudi, convé calcular proporcions per classe o una taula de transició en lloc de confiar en una única classe generalitzada.

Reduir la resolució és una operació d'**agregació**. Si es passa de 25 m a 200 m en graelles niades, cada resultat pot resumir 64 cel·les fines. La mitjana respon quina elevació mitjana o quin valor intensiu caracteritza el bloc; el màxim respon quin extrem hi apareix; la desviació descriu l'heterogeneïtat interna. Són preguntes diferents i poden necessitar diverses bandes o taules, no un únic ràster suposadament representatiu.

## Reprojecció i graella de referència

Reprojectar un ràster transforma les coordenades i crea una nova matriu. A diferència d'una capa vectorial, on es poden transformar directament els vèrtexs, una graella projectada deixa de formar una graella regular en el nou sistema si només es transformen les cantonades. L'algorisme defineix una graella regular de destinació, relaciona cada cel·la amb la font i aplica un remostreig. Per això la reprojecció modifica simultàniament geometria de la malla i valors {% cite projContributorsPROJ2026 rouaultGDAL2026 %}.

El `CRS` del projecte QGIS controla principalment la visualització. Veure dues capes superposades al llenç no prova que comparteixin coordenades emmagatzemades, resolució ni alineació. Abans d'una expressió cel·la a cel·la cal materialitzar, si és necessari, una versió de treball en un `CRS` projectat adequat i en una graella comuna. Assignar un `CRS` només corregeix la interpretació de coordenades conegudes; no substitueix aquesta transformació.

La **graella de referència** fixa el contracte de totes les sortides: `CRS`, mida de cel·la, origen, extensió, files, columnes i regla de `NoData`. QGIS i els proveïdors de Processament ofereixen opcions per establir resolució i extensió, però no totes exposen l'origen de la mateixa manera. La forma més segura és utilitzar una capa de referència comprovada o calcular explícitament els límits ajustats i verificar després la transformació de sortida.

Una seqüència eficient evita remostreigs acumulats. Si la font comuna es pot transformar directament a les graelles de 25 m i 200 m, és preferible crear cadascuna des de la font que generar 200 m a partir de la còpia de 25 m. La segona via incorpora la transformació anterior i en dificulta la interpretació. Una còpia temporal remostrejada pot servir per a una comparació concreta, però no s'ha de confondre amb la branca principal de derivació.

## Models digitals d'elevacions

Un **model digital d'elevacions** (MDE) és una representació numèrica d'altures sobre una superfície de referència. La terminologia dels productes no és completament uniforme. En aquest manual, **model digital del terreny** (MDT, també anomenat MET en alguns materials) designa una superfície que intenta representar el sòl nu, mentre que **model digital de superfície** (MDS) representa la superfície superior observada i pot incloure edificis, vegetació i altres objectes. Cal comprovar sempre la definició del productor en lloc de deduir el contingut només de les sigles {% cite felicisimoModelosDigitalesTerreno1994 nunesDiccionariSIG2012 %}.

La diferència entre MDS i MDT pot aproximar l'altura d'objectes si les dues superfícies comparteixen adquisició compatible, referència vertical, alineació i tractament. Restar productes de dates o procediments diferents pot barrejar creixement de vegetació, obres, errors de classificació, moviments reals i desajustos geomètrics. Una diferència positiva no identifica automàticament un edifici, i una diferència petita pot quedar dins de la incertesa vertical.

### Procedència de l'elevació

Un MDE pot derivar de punts LiDAR, correlació fotogramètrica, radar, restitució estereoscòpica, corbes de nivell o interpolació de punts topogràfics. Cada origen deixa una estructura d'error diferent. El LiDAR necessita classificar quins retorns corresponen al terreny i interpolar entre punts; la fotogrametria pot fallar en superfícies uniformes, aigua o oclusions; el radar respon a la geometria d'observació i a les propietats de la superfície; una superfície interpolada de corbes hereta l'escala i la generalització del mapa de partida.

Les metadades necessàries no acaben en la mida de cel·la. Cal conèixer, quan estigui disponible, la data de captura, densitat i distribució dels punts, classificació, resolució original, mètode d'interpolació, tractament d'edificis i vegetació, línies de ruptura, aigua, ponts, buits i vores de tessel·la, així com indicadors d'exactitud. Un GeoTIFF ben alineat només és l'últim contenidor d'aquesta cadena de producció.

### Referència vertical i unitats

Una altura necessita una referència vertical. Un receptor GNSS produeix habitualment altura el·lipsoidal, mentre que molts productes topogràfics publiquen altures ortomètriques o normals relacionades amb un geoide o quasi-geoide. Les dues magnituds poden diferir desenes de metres sense que cap mesura sigui necessàriament errònia. El `CRS` horitzontal no sempre codifica aquesta dimensió; veure `EPSG:25831` no basta per saber respecte de què es mesura la cota.

Abans de combinar elevacions cal registrar el tipus d'altura, el datum o model vertical, la unitat i, quan sigui rellevant, l'època. Una font en peus i una altra en metres poden semblar superfícies plausibles si no es comparen rangs. Una cota zero a la costa tampoc no demostra per si sola que el producte utilitzi el nivell mitjà del mar esperat: pot ser un valor vàlid, una convenció imposada a l'aigua o un error de tractament de `NoData`.

La transformació vertical no consisteix a sumar una constant universal. La separació entre el·lipsoide i geoide varia espacialment i necessita un model adequat. Si no hi ha informació suficient per harmonitzar dues referències, la limitació s'ha de declarar i no s'ha de presentar la diferència d'elevació com un canvi físic precís.

## Derivats del terreny

Els derivats converteixen la superfície d'altures en propietats locals o regionals. Cada resultat depèn de l'algorisme, el veïnatge, la resolució i el tractament de vores. Dues eines anomenades `Slope` poden aplicar aproximacions diferents sobre una finestra de 3 × 3 cel·les i produir valors lleugerament diferents. Registrar l'identificador de l'algorisme i la versió del proveïdor és part del mètode, especialment quan el resultat s'ha de comparar o repetir {% cite qgisUserGuide344 %}.

### Pendent i orientació

El **pendent** expressa la taxa màxima de canvi d'altura al voltant d'una cel·la. Es pot donar en graus, com l'angle respecte d'un pla horitzontal, o en percentatge, com el desnivell dividit per la distància horitzontal i multiplicat per cent. La relació és $p = 100\tan(\theta)$. Per tant, 45° equivalen a un pendent del 100%; el 100% no representa una paret vertical. Les unitats s'han d'indicar al nom de la capa, la llegenda i qualsevol llindar.

El factor vertical, sovint anomenat factor `z`, relaciona les unitats d'altura amb les horitzontals. Només és 1 quan són compatibles, per exemple metres en tots dos casos. Calcular pendent directament sobre una graella geogràfica en graus amb elevacions en metres exigeix una conversió que varia amb la latitud o, preferiblement per a l'àmbit local, una reprojecció adequada. Un resultat entre 0 i 90 no demostra que el càlcul sigui correcte.

L'**orientació** indica la direcció de màxim descens. Sol expressar-se com un angle circular, però cal comprovar si 0° correspon al nord, en quin sentit creixen els angles i quin valor identifica superfícies planes. 1° i 359° són direccions pròximes, encara que la seva mitjana aritmètica sigui 180°. Per resumir orientacions cal utilitzar estadística circular, basada en components sinus i cosinus, i informar també de la concentració direccional.

En una superfície gairebé plana, petits errors verticals poden canviar molt l'orientació perquè no hi ha una direcció dominant. Convé separar cel·les per sota d'un llindar de pendent justificat abans d'agrupar exposicions nord, est, sud i oest. Aquest llindar no és universal: depèn de la qualitat del MDE i de la finalitat. La classe «pla» ha de continuar distingida de `NoData`.

### Ombrejat, curvatura i rugositat

L'**ombrejat del relleu** simula la il·luminació d'una superfície segons un azimut i una altura solar. Ajuda a percebre formes, però no és una observació de llum ni una banda d'elevació. Canviar la direcció de la llum pot fer més visibles unes valls i ocultar-ne d'altres, i la il·lusió perceptiva pot invertir el relleu si la llum sembla venir de baix. Un ombrejat multidireccional pot reduir part del biaix, però també és una representació derivada i n'ha de conservar els paràmetres.

La **curvatura** descriu com canvia el pendent. La curvatura de perfil es relaciona amb l'acceleració o desacceleració del flux en la direcció del vessant, mentre que la curvatura en planta ajuda a descriure convergència i divergència lateral. Són derivades de segon ordre i amplifiquen soroll, errors de tessel·la i artefactes d'interpolació. Abans d'interpretar-les cal examinar el MDE, provar l'escala del veïnatge i evitar una precisió decimal que la font no sosté.

Mesures com rugositat, índex de rugositat del terreny o posició topogràfica comparen una cel·la amb el seu entorn. El resultat canvia radicalment amb la mida de la finestra: una depressió local dins d'un radi de 75 m pot formar part d'una plana dins d'un radi de 2 km. El nom de l'índex no defineix l'escala; el radi o dimensions del veïnatge han d'aparèixer als paràmetres i a la interpretació.

### Corbes, perfils, drenatge i visibilitat

Les **corbes de nivell** uneixen posicions d'igual altura interpolades sobre el MDE. Una equidistància petita no millora la precisió vertical de la font i pot crear línies molt sinuoses sobre soroll local. Els **perfils** mostren l'elevació al llarg d'un traçat i són útils per comprovar ruptures, costures de mosaic i efectes de resolució. Tant les corbes com els perfils són derivats: han de mantenir la referència al MDE i no substituir-ne les metadades.

L'anàlisi hidrològica sol preparar el MDE abans de calcular direcció i acumulació de flux. Emplenar totes les depressions força la continuïtat del drenatge, però també pot eliminar cubetes reals; obrir una sortida o cremar una xarxa imposa una altra hipòtesi. L'algorisme de direcció pot enviar el flux a un sol veí o repartir-lo entre diversos, i l'acumulació es pot expressar en nombre de cel·les o en superfície contribuent. Sense aquestes decisions, una xarxa derivada no es pot interpretar com una xarxa hidrogràfica observada.

Una **conca visual** determina quines cel·les mantenen línia de visió amb un observador segons la superfície disponible. Necessita posició i altura de l'observador, altura de l'objectiu i, segons la distància, tractament de curvatura i refracció. Un MDT omet edificis i arbres; un MDS els pot incorporar segons la data i la resolució. La sortida representa visibilitat modelada, no tot allò que una persona veuria en condicions reals.

### Efectes de vora

Qualsevol operació de veïnatge perd informació al límit del ràster. Una finestra de 3 × 3 no pot calcular-se de la mateixa manera a la primera fila si falten els veïns exteriors. L'eina pot retornar `NoData`, reduir la finestra, replicar valors o aplicar una altra regla. El resultat pot formar un marc artificial al voltant de la capa sense produir cap missatge d'error.

Els derivats del municipi s'han de calcular sobre una franja de dades exterior i retallar-se després al límit d'informe. Si el MDT es talla exactament pel polígon municipal abans del pendent, les cel·les de vora perden veïns; si es calcula una distància només amb fonts interiors, s'ignoren elements externs que podrien ser els més pròxims; si s'extreu una conca dins del rectangle local, s'omet cabal potencial procedent de fora. El marge s'ha de derivar de l'operació, no adoptar-se per costum.

## Àlgebra de mapes i reclassificació

L'**àlgebra de mapes** tracta les graelles com a operands. Una operació **local** calcula cada cel·la a partir dels valors de la mateixa posició; una operació **focal** utilitza un veïnatge; una operació **zonal** resumeix cel·les que pertanyen a una zona; i una operació **global** pot dependre de tota la superfície, com una distància acumulada. Aquesta classificació ajuda a anticipar quines capes han d'estar alineades i quin context exterior necessita cada càlcul.

Una expressió local pot sumar bandes, calcular una diferència, normalitzar un valor o avaluar una condició. Abans d'executar-la cal comprovar unitats i dominis. Restar metres a graus no té sentit; dividir per una banda que conté zeros necessita una regla; combinar una data amb una altra pot descriure canvi només si les fonts són comparables. El fet que la calculadora retorni nombres no valida l'operació.

La **reclassificació** converteix valors o intervals en classes. Els intervals han de cobrir el domini previst, no solapar-se i declarar el tractament dels límits. Una taula pot definir, per exemple, `[0, 2)` com a pendent suau i `[2, 5)` com a pendent moderat; escriure només `0–2` i `2–5` deixa ambigu on cau exactament el valor 2. També s'han de separar valors fora de rang i `NoData`.

Els llindars poden provenir d'una norma, d'una relació funcional, de la distribució observada o d'una decisió exploratòria. Aquestes justificacions no són intercanviables. Si un llindar canvia entre municipis perquè s'adapta a quantils locals, les classes ja no representen els mateixos valors absoluts; si es manté un llindar comú, alguns municipis poden quedar gairebé en una sola classe. La comparació exigeix decidir quina propietat es vol conservar.

Una comparació genera una màscara booleana i els operadors lògics combinen condicions. Per exemple:

::: listing "Màscara exploratòria de terreny baix i pendent suau"
```sql
("elevacio@1" < 20) AND ("pendent_graus@1" < 2)
```
:::

Aquesta expressió és sintaxi de la calculadora ràster de QGIS quan les capes carregades s'anomenen `elevacio` i `pendent_graus`; els llindars s'interpreten en les unitats documentades de les bandes, metres i graus respectivament. Identifica cel·les que compleixen dos criteris pedagògics i no determina per si sola una aptitud urbanística o ambiental. `AND` conserva només la coincidència de totes les condicions; `OR` accepta qualsevol condició. La diferència entre les dues sortides és una comprovació útil de la lògica, però cal decidir també què passa quan una entrada és `NoData`. Convertir l'absència automàticament en fals ocultaria zones no avaluades.

Una anàlisi multicriteri ponderada necessita encara més decisions: transformar variables a una escala comuna, establir la direcció de preferència, tractar valors extrems, justificar pesos i distingir restriccions absolutes de factors compensables. Un pes alt no converteix una font incerta en una evidència millor. Abans d'acceptar un mapa final convé variar llindars i pesos dins d'un rang justificable i identificar quines zones depenen d'una elecció fràgil.

## Superfícies de distància i cost

Una **distància euclidiana** assigna a cada cel·la la separació en línia recta fins a la font més pròxima. La font pot provenir de punts, línies, polígons o cel·les seleccionades, però ha de quedar rasteritzada sobre una graella definida. El resultat depèn del `CRS`, de les unitats i de com es representa el límit de la font. En un `CRS` geogràfic, una diferència angular no s'ha d'interpretar directament com metres.

La distància entre centres introdueix una aproximació que es fa més visible en cel·les grosses. Una font estreta pot desplaçar-se fins al centre de la cel·la que la representa, i la seva forma pot desaparèixer o engruixir-se. Quan el llindar és semblant a la mida de cel·la, la classificació dins o fora de la distància és especialment sensible a l'origen de la malla. Convé comparar una mostra amb mesures vectorials i quantificar la franja d'incertesa al voltant del llindar.

Una **distància de cost** acumula una fricció en travessar les cel·les. Una superfície de cost pot representar temps per metre, energia, dificultat o una combinació explícita. Els valors han de tenir una interpretació dimensional coherent: sumar pendents, metres i categories codificades sense transformació no produeix un cost interpretable. Les barreres també s'han de distingir de `NoData`; una cel·la prohibida, una cel·la desconeguda i una cel·la molt costosa no expressen el mateix.

El cost pot ser **anisòtrop** quan depèn de la direcció. Pujar i baixar un vessant no exigeix el mateix esforç, i moure's a favor o en contra d'un corrent tampoc. Una superfície de fricció única és isòtropa i no captura aquesta diferència. La resolució controla quines barreres i corredors existeixen a la malla: una carretera estreta o un pas entre obstacles pot desaparèixer a 200 m i alterar completament la connectivitat.

Les superfícies de distància no substitueixen automàticament una xarxa. Una xarxa conserva nodes, arcs, sentits i restriccions; un ràster de cost permet moviment sobre una superfície segons un veïnatge. Tots dos poden modelar accessibilitat, però responen a representacions diferents del problema. La tria s'ha de justificar segons si el moviment queda restringit a vies o pot travessar el territori.

## Relació entre ràster i vector

Rasteritzar una capa vectorial exigeix fixar una graella de referència, seleccionar un atribut o valor constant i decidir quines cel·les s'activen. La regla basada en el centre és conservadora però pot perdre línies estretes; la regla d'incloure totes les cel·les tocades conserva presència però eixampla objectes i augmenta superfícies. Quan diverses entitats ocupen una mateixa cel·la, l'ordre, la prioritat o l'agregació han de quedar definits.

Vectoritzar un ràster crea geometries que segueixen les vores de les cel·les. Una classificació sorollosa pot produir milers de polígons petits i contorns esglaonats. Dissoldre per classe redueix registres però no recupera el límit original ni elimina la incertesa de classificació. Suavitzar el contorn canvia novament la geometria i s'ha de considerar una generalització, no una restauració.

### Estadístiques zonals

Les **estadístiques zonals** resumeixen els valors d'un ràster dins de zones, normalment polígons vectorials. Per a elevació o pendent poden ser útils el recompte vàlid, la mitjana, la mediana, la desviació, el mínim i el màxim. Alguns proveïdors ofereixen també percentils, però l'algorisme `native:zonalstatisticsfb` de QGIS 3.44 no els calcula. La suma d'elevacions o pendents no té una interpretació territorial directa. Per a categories interessen els recomptes i proporcions per classe, no la mitjana dels codis.

La regla de pertinença de cel·les a una zona condiciona el resultat. Alguns algorismes utilitzen el centre, altres inclouen cel·les tocades i altres ponderen la fracció coberta. Un municipi petit o estret pot no contenir cap centre de cel·la a 200 m encara que intersequi la graella. La documentació de l'eina i una geometria de prova simple permeten saber què s'està comptant.

Per a una classe ràster, la superfície aproximada es calcula multiplicant el nombre de cel·les completes per l'àrea d'una cel·la. A 25 m, cada cel·la quadrada representa 625 m²; a 200 m, 40.000 m². Aquesta fórmula és exacta per a la superfície de les cel·les en un `CRS` projectat adequat, però la seva assignació íntegra a un municipi és una aproximació al límit vectorial. Si es ponderen fraccions de cel·la, cal conservar el mètode i no tornar a multiplicar com si totes fossin completes.

Les estadístiques zonals afegeixen camps a una capa o generen una taula. Els noms han d'incloure la variable, la resolució i l'estadístic, com `z25_elev_mean` o `z200_slope_max`, dins dels límits del format. Abans de la unió cal assegurar que l'identificador de zona és únic; després, comprovar zones sense valors, recompte de files i unitats. Una taula llarga amb una fila per zona, resolució, variable i estadístic pot ser més fàcil de comparar i ampliar que desenes de camps amb noms abreujats.

## Incertesa, sensibilitat i control de qualitat

La incertesa d'un resultat ràster combina diverses fonts. Hi ha error de mesura i posició a les observacions originals; error de classificació o interpolació durant la producció; discretització per la mida i l'origen de les cel·les; quantificació pel tipus numèric; i transformacions introduïdes per reprojecció, remostreig, filtres i reclassificacions. Un valor final amb sis decimals no elimina cap d'aquestes fonts.

L'exactitud vertical d'un MDE se sol resumir amb mesures com l'error mitjà o l'arrel de l'error quadràtic respecte de punts de control. Aquestes mesures no són un error màxim i poden variar amb pendent, coberta, sensor i densitat de mostreig. Si només es disposa d'un indicador global, no s'ha d'aplicar com si descrivís igualment una platja oberta, un bosc dens i un nucli urbà. Les metadades han d'acompanyar qualsevol contrast local.

Els derivats poden amplificar errors. El pendent calcula diferències entre cel·les veïnes: una petita variació vertical sobre una distància curta pot produir un canvi angular apreciable. La curvatura torna a diferenciar el pendent i és encara més sensible. Agregar a una resolució grossa pot reduir soroll i extrems, però també eliminar ruptures reals. No hi ha una direcció universalment millor; cal relacionar el nivell de suavització amb la mida del procés estudiat.

L'origen de la graella és una font de sensibilitat semblant a la mida. Desplaçar una malla 12,5 m sense canviar la resolució de 25 m pot alterar quina classe domina a les cel·les de vora, quins punts s'agrupen junts i quina superfície s'assigna a cada zona. Aquesta dependència és paral·lela a la que apareix en tessel·lacions vectorials: les unitats regulars simplifiquen la comparació, però el seu origen i orientació no són neutrals.

Una **anàlisi de sensibilitat** repeteix el càlcul canviant només una decisió: resolució, remostreig, origen, llindar, mida de finestra o regla de vora. L'objectiu no és escollir després la variant visualment preferida, sinó identificar quines conclusions es mantenen. Si una zona candidata desapareix en moure lleugerament la graella o variar un llindar dins de la incertesa de la font, s'ha de descriure com a resultat inestable.

Els controls combinen metadades, nombres i inspecció espacial. Abans de processar cal revisar font, banda, `CRS` horitzontal i referència vertical, resolució efectiva, extensió, alineació, tipus i `NoData`. Després de cada pas cal comprovar dimensions, rang, quantils, cel·les vàlides, patró de buits, vores, costures i una mostra de posicions conegudes. Un histograma pot detectar un sentinella incorporat com a mínim extrem; un perfil pot revelar una línia entre tessel·les; un recompte pot mostrar que un retall ha eliminat tot un municipi.

::: table "Diagnòstic de problemes ràster habituals"
| Símptoma | Causa possible | Comprovació abans de corregir |
| --- | --- | --- |
| La capa apareix desplaçada | `CRS` mal assignat, origen erroni o fitxer de món inconsistent | Extensió numèrica, metadades i punts coneguts |
| Franja extrema al voltant de la cobertura | `NoData` incorporat a una interpolació | Valor sentinella, màscara i recompte vàlid |
| Costura entre tessel·les | Edicions, referències verticals o interpolacions diferents | Perfil transversal i metadades de cada peça |
| Pendent exagerat o massa baix | Unitats incompatibles, factor `z` o resolució incorrectes | Unitats horitzontals i verticals, rang i algorisme |
| Classes noves després de remostrejar | Interpolació aplicada a codis | Valors únics abans i després i mètode utilitzat |
| Ràster pesant i lent | Sense compressió, blocs o piràmides adequats | Estructura interna i patró de lectura |
| Resultats diferents amb la mateixa mida de cel·la | Origen o extensió desalineats | Coordenades de límits i centres de cel·la |
| Vora municipal anòmala | Retall anterior a un càlcul focal | Comparació amb una versió calculada amb marge |
:::

## Disseny reproduïble per comparar 25 m i 200 m

La comparació entre 25 m i 200 m no busca demostrar que una resolució sigui sempre millor. La pregunta és quina part del resultat canvia quan el mateix fenomen es representa sobre suports espacials de mida diferent. Abans de calcular res cal definir quines variables es compararan, quines diferències serien plausibles per generalització i quines obligarien a revisar el procés. Aquest plantejament evita convertir una expectativa en un resultat inventat.

La font ha de ser comuna i prou detallada per sostenir les dues sortides. Si el producte original és més gros que 25 m, remostrejar-lo a 25 m no permet presentar aquesta branca com a observació fina. Es conservaran el paquet original, les metadades, la data d'accés i la identificació exacta del producte. El límit de Vila-seca o del municipi assignat serà la zona d'informe, però l'entrada d'elevacions inclourà un marge suficient per als derivats.

L'extensió de treball es definirà en un `CRS` projectat adequat. Els seus límits s'ajustaran a una graella mare de 200 m i aquesta es niarà amb la de 25 m. L'origen serà idèntic i l'amplada i l'alçada seran múltiples de 200 m. D'aquesta manera, cada cel·la de 200 m correspondrà exactament a 64 cel·les de 25 m i es podrà separar l'efecte de la mida de l'efecte d'un desplaçament de malla.

Les dues graelles d'elevació es generaran directament de la font comuna amb el mateix principi d'agregació, no una a partir de l'altra. Per a una comparació principal del suport mitjà es pot adoptar la mitjana ponderada sobre la superfície contribuent, sempre que la semàntica i la resolució de la font ho permetin. Si interessa conservar cims, depressions o una altra propietat, es produiran capes addicionals de mínim, màxim o dispersió amb noms explícits; no se substituirà silenciosament la mitjana per un extrem.

El pendent i l'orientació es calcularan després sobre cada MDE de destinació amb el mateix algorisme, unitats i política de vores. Aquesta seqüència respon com canvia el relleu derivat quan la superfície es representa a cada suport. Una altra seqüència possible consistiria a calcular pendent a la resolució original i agregar-lo després. Respon una pregunta diferent, perquè resumeix pendents locals en lloc de calcular el pendent d'una superfície generalitzada. Les dues branques es poden comparar com a ampliació, però no barrejar en una mateixa columna sense identificar-les.

Els intervals d'elevació, les classes de pendent i la màscara booleana utilitzaran els mateixos llindars absoluts en totes dues resolucions. Els llindars es fixaran abans de veure la sortida comparativa i se'n documentarà l'origen. Si s'utilitzessin quantils independents, cada mapa tindria aproximadament proporcions semblants per construcció i les classes deixarien de representar els mateixos valors. Els estiraments de color, el rang de llegenda, l'extensió cartogràfica i l'escala també seran comuns.

::: table "Protocol de la comparació controlada"
| Fase | Decisió que es manté fixa | Evidència que cal registrar |
| --- | --- | --- |
| Font | Producte, edició, banda, referència vertical i còpia d'entrada | Identificador, metadades i rang original |
| Àmbit | Municipi d'informe i regió amb marge | Extensió vectorial, extensió ajustada i justificació del marge |
| Graelles | `CRS`, origen comú, 25 m i 200 m niats | Transformació, files, columnes i relació 8 × 8 |
| Remostreig | Mateix principi des de la font comuna | Algorisme, paràmetres i regla de `NoData` |
| Derivats | Mateix algorisme de pendent i orientació | Identificador, unitats, factor vertical i tractament de planes |
| Classes | Mateixos llindars i límits d'interval | Taula de reclassificació conservada |
| Zones | Mateix límit municipal i regla de pertinença | Recompte vàlid i tractament de cel·les de vora |
| Mapes | Mateixa extensió, escala i simbologia | Composicions comparables sense estirament automàtic independent |
| Controls | Mateix conjunt d'indicadors | Taula llarga per resolució, variable i estadístic |
:::

Una implementació de referència per a QGIS 3.44 fixa els algorismes i els paràmetres que afecten el resultat. Les coordenades exactes de l'extensió i el valor `NoData` s'han d'emplenar amb les dades reals abans d'executar; no es poden substituir per la vista del llenç.

::: table "Contracte executable de referència en QGIS 3.44"
| Fase | Algorisme | Paràmetres que s'han de fixar |
| --- | --- | --- |
| Graelles d'elevació | `gdal:warpreproject`, executat directament sobre la mateixa font per a cada resolució | `TARGET_CRS`; `RESAMPLING = Average` si la font i la pregunta admeten suport mitjà; `NODATA`; `TARGET_EXTENT` numèrica comuna ajustada a 200 m; `TARGET_EXTENT_CRS`; `TARGET_RESOLUTION = 25` o `200`; `EXTRA = -tap`; tipus de sortida de coma flotant |
| Pendent | `gdal:slope` | `BAND = 1`; `SCALE = 1` quan les unitats horitzontals i verticals són metres; graus, no percentatge; mateixa fórmula; `COMPUTE_EDGES = False` per fer visible la vora incompleta |
| Orientació | `gdal:aspect` | `BAND = 1`; azimut des del nord; mateixa fórmula; `COMPUTE_EDGES = False`; classe plana derivada del llindar de pendent, no del codi d'orientació |
| Reclassificació | `native:reclassifybytable` | Banda, taula d'intervals, inclusió dels límits, valor per a rangs absents, `NoData` i tipus de sortida idèntics a les dues resolucions |
| Màscara de dos criteris | `native:rastercalc` | Capes explícites, expressió `("elevacio@1" < 20) AND ("pendent_graus@1" < 2)`, extensió, mida de cel·la, CRS, tractament de `NoData` i sortida persistent |
| Resum municipal | `native:zonalstatisticsfb` | Municipi original, banda 1, prefix per variable i resolució, i només estadístics admesos: recompte, mitjana, mediana, desviació, mínim i màxim |
:::

`native:zonalstatisticsfb` assigna habitualment els píxels pel centre i aplica una selecció per intersecció quan una zona petita no conté cap centre. Aquesta regla s'ha de conservar a totes dues resolucions i provar amb un polígon simple. El percentatge de cel·les vàlides només es calcularà si també s'obté un denominador amb una graella constant, vàlida i perfectament alineada: el recompte del MDE dividit pel recompte de la graella constant sobre el mateix municipi. Sense aquest segon recompte s'informarà només el nombre de valors vàlids.

La taula de resultats es prepararà abans de l'execució i deixarà les cel·les de valor buides. Per a cada resolució registrarà dimensions, nombre de cel·les vàlides, superfície ràster assignada al municipi, mínim, màxim, mitjana, mediana i desviació d'elevació, distribució del pendent, proporció de terreny pla, proporcions de classes i superfície de la màscara. El percentatge vàlid només s'hi afegirà amb el denominador anterior. També inclourà el temps i la mida de fitxer només com a mesures operatives de l'execució, no com a criteris de qualitat geogràfica.

No s'ha de pressuposar que totes les mitjanes canviaran poc ni que tots els màxims i pendents disminuiran. Aquestes són hipòtesis plausibles quan s'agrega una superfície, però poden fallar per la forma del territori, `NoData`, regles de vora o artefactes. El protocol obliga a observar primer els valors i després explicar-los. Una diferència inesperada començarà amb un diagnòstic de graella, validesa i paràmetres abans d'atribuir-se a l'escala geogràfica.

Les comparacions cel·la a cel·la necessiten un suport comú. Per a un control a 200 m, els valors de 25 m es poden agregar en blocs 8 × 8 i comparar amb la branca de 200 m creada directament; aquesta prova avalua coherència del procés. Per visualitzar desacord de classes a 25 m, la classe de 200 m es pot expandir amb veí més proper, deixant clar que cada bloc rep una etiqueta repetida i que no s'ha creat informació fina. La diferència no s'ha de calcular superposant graelles desalineades ni aplicant bilineal a codis.

L'efecte de vora es quantificarà separant una zona interior, situada almenys a la distància necessària del límit, i una franja fronterera. També es compararà la superfície vectorial amb la superfície assignada segons cada graella. Si gran part de la diferència es concentra a la franja, la interpretació parlarà de discretització del límit; si persisteix a l'interior, s'examinaran generalització, derivats i classificació. Aquesta separació impedeix atribuir a tot el relleu un problema generat només pel contorn municipal.

La conclusió de l'exercici tindrà tres parts: diferències observades amb unitats, mecanismes que les poden explicar i implicacions per a la pregunta territorial. No afirmarà que 25 m és «més exacte» sense una validació independent ni que 200 m és «incorrecte» perquè generalitza. Indicarà per a quines decisions el canvi és material, quines conclusions es mantenen i quines queden obertes per falta d'una referència de control.

## Formats de sortida i verificació final

Abans d'acceptar una sortida cal tornar-la a obrir i comprovar `CRS`, referència vertical documentada, dimensions, extensió, mida de píxel, origen, banda, tipus, `NoData`, mínim, màxim, quantils i nombre de cel·les vàlides. Després s'ha de contrastar una mostra amb la font, inspeccionar vores i costures i comparar superfícies o estadístiques amb valors plausibles. Els controls i les incidències s'incorporaran al diari; una captura només és necessària si prova una configuració o una anomalia que les taules no descriuen prou bé.

## Activitats

### Comprovació: zero o absència

Cal preparar una graella petita amb valors positius, zero i `NoData`, i predir el resultat d'una mitjana, una suma i una condició booleana sota dues polítiques d'absència.

Després s'executaran les operacions i es compararà la predicció amb el recompte de valors vàlids. L'activitat ha d'explicar quina conclusió falsa apareix si `NoData` es converteix en zero i quina informació es perd si qualsevol absència es converteix automàticament en fals.

### Pràctica guiada: el relleu de Vila-seca a dues resolucions

La pràctica seguirà el protocol i el contracte executable de referència sense completar per endavant la taula de resultats. Primer s'identificarà el producte oficial d'elevacions, la superfície representada, les referències horitzontal i vertical, la resolució original, el tipus, `NoData` i les limitacions. Després es crearà una regió d'interès amb marge i s'anotaran les coordenades d'una extensió ajustada a la graella de 200 m.

A partir de la mateixa font, `gdal:warpreproject` generarà directament models de 25 m i 200 m amb l'extensió comuna, `-tap` i el mètode de remostreig justificat. `gdal:slope`, `gdal:aspect`, `native:reclassifybytable` i `native:rastercalc` produiran respectivament pendent en graus, orientació, classes d'elevació i la màscara booleana, amb els paràmetres de la taula anterior. `native:zonalstatisticsfb` calcularà les estadístiques admeses sobre el municipi original, no sobre la regió amb marge. Els mapes utilitzaran els mateixos intervals, colors, extensió i escala.

La validació inclourà la relació 8 × 8 entre graelles, dimensions esperades, valors vàlids, rangs, histogrames, superfície de les classes i comparació entre franja de vora i interior. Només després s'escriurà quins resultats són sensibles a la resolució. Si una diferència no es pot separar d'un canvi de remostreig, alineació o `NoData`, quedarà descrita com una limitació del disseny i no com un efecte demostrat de la mida de cel·la.

### Micropràctica 5: anàlisi ràster

::: table "Contracte de la micropràctica 5"
| Component | Requisit |
| --- | --- |
| Entrades | Límit del municipi assignat i subconjunt d'un model d'elevacions oficial amb marge suficient |
| Operacions mínimes | Preparar dues resolucions niades amb `gdal:warpreproject`, calcular pendent i orientació amb `gdal:slope` i `gdal:aspect`, reclassificar amb `native:reclassifybytable`, combinar dues condicions amb `native:rastercalc` i resumir amb `native:zonalstatisticsfb` |
| Resultats | GeoTIFF continus i categòrics, taula d'estadístiques al GeoPackage i mapa comparatiu |
| Evidències del diari | Font i procedència de l'elevació, `CRS`, referència vertical, resolució, alineació, `NoData`, remostreig, llindars, controls i interpretació de les diferències |
| Comprovacions | Dimensions esperades, relació de niament, rangs plausibles, cel·les vàlides, superfície ràster comparada amb la vectorial, efectes de vora i simbologia comuna |
| Fitxers que cal conservar | Ràsters finals, taula comparativa al GeoPackage, projecte `.qgz` i diari amb els controls |
:::

Els llindars de Vila-seca no s'han de copiar automàticament a un municipi de muntanya. La transferència exigeix revisar la distribució, la mida dels processos, la qualitat de l'elevació i la finalitat de cada classe. El lliurament ha de diferenciar els valors observats dels esperats i conservar buides, fins a executar els càlculs, totes les caselles destinades als resultats de la comparació.
