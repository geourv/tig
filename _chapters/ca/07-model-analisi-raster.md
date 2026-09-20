---
layout: manual-chapter
title: Model i anàlisi ràster
description: Graelles, resolució, relleu, àlgebra de mapes i estadístiques zonals per interpretar dades ràster.
lang: ca
ref: manual-raster-model-analysis
profiles: [unaltremanual]
content_status: approved
permalink: /ca/chapters/model-analisi-raster/
weight: 80
part: Continguts
manual_references: true
---

Quines parts d'un municipi són més baixes? Com varia el pendent? On coincideixen dues condicions territorials? Aquestes preguntes no descriuen només objectes delimitats: necessiten observar una propietat a totes les posicions d'un àmbit. El model ràster ho fa mitjançant una graella regular en què cada cel·la ocupa una porció del territori i emmagatzema un valor per banda.

La mateixa estructura serveix per a elevacions, temperatures, imatges de satèl·lit, cobertes del sòl, distàncies o màscares de criteris. No totes aquestes dades, però, tenen la mateixa semàntica. Abans de calcular cal saber què representa cada valor, sobre quin suport espacial s'ha obtingut i què significa una cel·la absent. La mida de cel·la, l'origen, l'extensió, el remostreig i `NoData` poden canviar el resultat encara que dues capes semblin superposades a QGIS {% cite felicisimoModelosDigitalesTerreno1994 longleyGeographicInformationScience2015 qgisUserGuide344 %}.

>>>>> En acabar el capítol, cal poder preparar, analitzar i comparar ràsters sense confondre resolució, exactitud ni absència de dades.
>>>>>
>>>>> - Interpretar cel·les, bandes, resolució, extensió, origen, alineació, tipus i `NoData` com un únic contracte de graella.
>>>>> - Distingir variables contínues, categories, màscares, magnituds extensives i models d'elevacions.
>>>>> - Preparar un mosaic, retallar-lo i justificar el remostreig abans de calcular.
>>>>> - Calcular i interpretar derivats del terreny i expressions booleanes de mapes.
>>>>> - Relacionar valors ràster amb zones vectorials, quantificar incertesa i comprovar l'efecte de la resolució.

## Del fenomen a la graella

El ràster és útil quan la pregunta demana una cobertura completa o una mesura repetida sobre posicions regulars. També permet combinar variables diferents quan s'han portat a una geometria comuna. La decisió no depèn només del format disponible: depèn de què s'observa i de quina operació haurà de respondre la pregunta.

El **model ràster** és una manera d'abstraure el fenomen; un **conjunt de dades ràster** és una materialització concreta d'aquest model, amb una graella, unes bandes, una data i un procés d'obtenció determinats. Dos conjunts poden seguir el mateix model i, tanmateix, diferir en suport, resolució, exactitud o procedència.

::: table "Aplicacions habituals del model ràster"
| Pregunta territorial | Ràster possible | Què representa una cel·la |
| --- | --- | --- |
| Quina altitud o quin pendent hi ha en cada posició? | Model digital d'elevacions i derivats | Una estimació d'altura o inclinació sobre el suport de la graella |
| Com respon la superfície a la llum visible o infraroja? | Imatge de satèl·lit o ortoimatge multibanda | Una mesura radiomètrica resumida per píxel i banda |
| Quina coberta domina cada lloc? | Classificació de cobertes del sòl | Un codi de classe, no una magnitud contínua |
| A quina distància o cost queda el servei més pròxim? | Superfície de distància o cost | Un valor calculat des de fonts i regles de moviment |
| On coincideixen diversos criteris? | Màscara booleana o índex multicriteri | Un resultat derivat de condicions explícites |
:::

Una graella no és una col·lecció desordenada de quadrats. Les files i les columnes formen un sistema de localització implícit: una vegada coneguts l'origen, la mida de cel·la i el sistema de referència de coordenades (`CRS`), la posició de cada valor es deriva del seu índex. Aquesta regularitat fa eficients les operacions locals, els filtres de veïnatge i l'emmagatzematge de superfícies, perquè no cal repetir dues coordenades per a cada cel·la. A canvi, totes les observacions queden sotmeses a una mateixa partició de l'espai.

El **suport espacial** indica a quina porció o localització del territori es refereix el valor d'una cel·la. Segons el producte, pot representar una observació al centre, una mitjana sobre l'àrea, la classe dominant, un recompte, una probabilitat o el resultat d'una interpolació. Un píxel de 25 m d'un model d'elevacions no implica necessàriament que s'hagi mesurat tota la superfície de 625 m² ni que la cota sigui una mitjana exacta d'aquesta àrea. Aquesta semàntica s'ha de recuperar de les especificacions del producte i conservar al diari.

El terme **píxel** descriu l'element d'una imatge digital i sovint s'utilitza com a sinònim pràctic de cel·la. En anàlisi territorial és preferible parlar de cel·la quan es vol remarcar el suport geogràfic del valor. El zoom només amplia la representació del mateix píxel; no redueix la mida de cel·la ni revela observacions noves. De la mateixa manera, remostrejar una graella de 25 m a 5 m crea més files i columnes, però els valors addicionals deriven dels originals i no constitueixen una mesura de més detall.

Un **objecte discret** conserva una identitat i uns límits modelats; un **camp** assigna un valor a cada posició d'un domini i pot ser continu o categòric. Aquesta distinció orienta l'elecció entre vector i ràster, però no la resol mecànicament. Una carretera es pot modelar com una línia connectada, com la superfície pavimentada d'un polígon o com cel·les d'una imatge. Una coberta del sòl està formada per classes, però es pot emmagatzemar en una graella per analitzar-la conjuntament amb elevació, clima o teledetecció. El model adequat és el que conserva les relacions necessàries per a la pregunta i fa visibles les simplificacions introduïdes.

### Semàntica dels valors ràster

Variable contínua
: Pot prendre valors intermedis dins del seu domini, com l'elevació, la temperatura o una concentració.

Variable categòrica
: Assigna etiquetes nominals o ordinals, com el tipus de coberta o un nivell de qualitat.

Magnitud intensiva
: No creix pel simple fet d'ampliar l'àrea, com una temperatura mitjana, una proporció o una densitat.

Magnitud extensiva
: Representa una quantitat que s'ha de conservar quan s'agrega, com un total de població distribuït en cel·les.

Aquestes distincions determinen quines operacions tenen sentit. La mitjana pot resumir temperatures o elevacions sobre un suport més gran, mentre que la suma pot conservar un recompte distribuït. Una superfície de densitat és contínua encara que provingui de punts o totals administratius: cada cel·la estima una intensitat per unitat d'àrea, no un nombre independent de persones observades al seu centre. Una coberta del sòl, en canvi, continua sent categòrica encara que els codis siguin enters. Per això interpolar-ne una mitjana produiria nombres sense categoria.

### Cel·les, bandes i tipus de valor

Una **banda** és una matriu de valors que comparteix la geometria del conjunt ràster. Una ortoimatge pot tenir bandes roja, verda, blava i infraroja; un model d'elevacions acostuma a tenir una banda d'altura; una sèrie pot separar dates o variables. Compartir fitxer o extensió no garanteix que les bandes tinguin la mateixa unitat o el mateix domini. El nom, la unitat, el factor d'escala i les metadades de cada banda formen part de l'entrada analítica.

El **tipus de dada** limita què es pot emmagatzemar. Un enter compacte és adequat per a codis o màscares; la coma flotant permet elevacions decimals i valors negatius, però ocupa més espai. Els codis de classe no es converteixen en magnituds perquè siguin nombres: si `1 = bosc`, `2 = conreu` i `3 = urbà`, la mitjana 2 no descriu una transició física entre bosc i urbà.

### Mida de cel·la i resolució efectiva

La **mida de cel·la** descriu l'amplada i l'alçada de la graella en les unitats del `CRS`. La **resolució espacial efectiva** descriu el detall que el conjunt pot distingir de manera fiable i depèn també de la font, el mostreig, el procés d'interpolació o classificació i l'exactitud. Un GeoTIFF de 2 m creat a partir d'observacions escasses no conté necessàriament informació independent cada 2 m; de la mateixa manera, un punt LiDAR per metre quadrat no és una cel·la ràster d'1 m. La densitat de punts i la mida de la graella són propietats diferents.

![Comparació entre mostres vectorials i graelles ràster fines i grosses sobre el mateix àmbit]({{ site.baseurl }}/assets/quarto/07-model-analisi-raster/raster-vector-support-resolution.qmd "El suport de l'observació, l'àrea de cada cel·la i el detall fiable de la font són propietats diferents. Reduir la mida de cel·la augmenta files i columnes, però no crea observacions noves ni millora automàticament l'exactitud."){: data-figure-width-web="56rem" data-figure-width-pdf="100%"}

En un `CRS` projectat, la mida de cel·la es pot expressar directament en metres. En una graella geogràfica s'expressa en graus. Un interval d'un segon d'arc equival a `1/3600°`, aproximadament `0,000278°`: la seva dimensió nord-sud és d'uns 30 m, però l'amplada est-oest disminueix amb la latitud. Per això una resolució angular no s'ha d'interpretar com una distància constant ni és adequada per calcular directament pendents en metres.

Els noms dels productes d'elevacions utilitzen tres sigles que cal distingir abans de comparar-ne la resolució. Un **model digital d'elevacions (MDE)** és el terme general per a una representació numèrica d'altures sobre una superfície de referència; un **model digital del terreny (MDT)** intenta representar el sòl nu; i un **model digital de superfície (MDS)** representa la superfície superior observada, que pot incloure edificis, vegetació i altres objectes.

![Perfil que compara el terreny nu amb la superfície superior sobre una mateixa referència horitzontal]({{ site.baseurl }}/assets/quarto/07-model-analisi-raster/elevation-surface-models.qmd "Un MDE pot representar superfícies diferents: l'MDT estima el sòl nu i l'MDS segueix la superfície superior observada. On el sòl és descobert poden coincidir; sobre edificis o vegetació, la resta MDS menys MDT només aproxima l'altura dels objectes si la referència, la graella, la data i el tractament són compatibles."){: data-figure-width-web="43.5rem" data-figure-width-pdf="100%"}

## On s'obtenen dades ràster

La font s'ha d'escollir després de formular la pregunta. Un visor ajuda a descobrir capes, però no substitueix la fitxa del productor ni garanteix que la imatge visible contingui els valors necessaris per analitzar. Cal distingir una descàrrega de dades, un servei que retorna una imatge simbolitzada i una visualització orientativa.

::: table "Famílies de fonts ràster i criteris de selecció"
| Família | Exemples d'accés | Ús habitual | Què cal comprovar |
| --- | --- | --- | --- |
| Cartografia oficial estatal | [Centre de Descàrregues del CNIG](https://centrodedescargas.cnig.es/) i productes PNOA | Models d'elevacions, ortofotos i altres cobertures per fulls o àmbits administratius | Edició, cobertura, resolució, referència vertical, `CRS`, `NoData` i llicència |
| Cartografia oficial catalana | [Geoinformació de l'ICGC](https://www.icgc.cat/ca/Geoinformacio-i-mapes), visor de descàrregues i geoserveis | Ortoimatges, models d'elevacions i cartografia de Catalunya | Producte concret, data, via de descàrrega o servei i unitats |
| Agregadors territorials | [Hipermapa de Catalunya](https://sig.gencat.cat/visors/hipermapa.html) | Descobrir capes de productors diferents i inspeccionar-ne la cobertura | Seguir cada resultat fins al productor i a la fitxa de la capa |
| Observació de la Terra | [Copernicus Data Space](https://dataspace.copernicus.eu/) i catàlegs de missions com Sentinel o Landsat | Reflectància, temperatura, índexs i classificacions derivades | Sensor, data, núvols, bandes, resolució i nivell de processament |
| Models d'elevacions globals | Copernicus DEM GLO-30/GLO-90 o SRTM | Context regional o àmbits sense un producte local més adequat | Superfície representada, resolució angular, cobertura, buits i referència vertical |
:::

Una imatge de satèl·lit no és automàticament un model d'elevacions. Les seves bandes solen mesurar resposta electromagnètica i necessiten correccions i interpretació abans de convertir-se en una variable territorial. De la mateixa manera, un MDE global pot ser suficient per a una conca regional però inadequat per estudiar un carrer o un talús. Productes com Copernicus DEM GLO-30 i GLO-90 s'identifiquen per un espaiat nominal aproximat d'un i tres segons d'arc; prop de l'equador equivalen aproximadament a 30 i 90 m, però no són cel·les mètriques constants.

La selecció mínima ha de respondre cinc preguntes: què representa el valor, de quina data o període prové, quin detall sosté, quina cobertura i quins buits té, i si la llicència permet l'ús previst. Només després convé valorar el format o la comoditat de càrrega. Una font oficial i molt detallada pot continuar sent inadequada si representa la superfície superior quan la pregunta necessita terreny nu, si és massa antiga o si la referència vertical és desconeguda.

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

El cas de Vila-seca recuperarà aquesta precaució amb dos productes oficials de 25 m i 200 m. Abans de comparar-ne els mapes caldrà comprovar si les graelles estan realment niades o si comparteixen només el `CRS` i una extensió aproximada.

### Tipus numèrics i valors codificats

Després d'identificar el significat de la banda, cal escollir o conservar un tipus capaç de representar-ne el domini. Un enter sense signe és eficient per a codis o valors no negatius; un enter amb signe permet valors negatius; la coma flotant conserva decimals i un rang ampli, però ocupa més espai i introdueix les aproximacions pròpies de l'aritmètica binària. Escollir `Float64` per a una màscara de 0 i 1 malgasta espai, mentre que convertir elevacions decimals a enter pot truncar informació. També cal comprovar si el producte aplica un factor d'escala i un desplaçament: un enter emmagatzemat pot representar un valor físic decimal després d'aquesta conversió.

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

El producte oficial MDT05 de primera cobertura defineix un pas de malla de 5 m i altures ortomètriques {% cite ignMDT05PrimeraCobertura %}.

![QGIS mostra el MDT05 del full 0473 amb una cota zero dins de la cobertura acolorida i una cel·la NoData dins de la zona transparent]({{ site.baseurl }}/assets/img/qgis/qgis-raster-nodata.png "El MDT05 oficial conserva un domini vàlid de -6,1 a 173,5 m, que inclou la cota zero, i utilitza -32767 com a sentinella NoData. QGIS exclou aquest sentinella de la llegenda i el representa transparent; el color blau d'una cota baixa no significa absència."){: data-figure-width-web="56rem" data-figure-width-pdf="100%"}

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

En la terminologia introduïda al capítol anterior, aquesta peça **georeferencia** la imatge perquè relaciona píxels i coordenades; no geocodifica cap adreça ni geoposiciona una observació nova.

El fitxer de món no declara per si sol el `CRS`, les unitats temàtiques, les bandes ni `NoData`. Sovint necessita un `.prj` i metadades addicionals. També es pot perdre o desincronitzar si es canvia el nom només a una de les peces. Quan una imatge conté georeferenciació interna i també un fitxer de món, una discrepància entre tots dos exigeix diagnòstic: no s'ha de triar automàticament la versió que fa encaixar millor la capa. Un GeoTIFF coherent és preferible per al treball analític perquè redueix aquestes dependències laterals.

### Compressió, blocs i piràmides

La **compressió sense pèrdua**, com LZW, Deflate o ZSTD quan l'entorn destinatari l'admet, redueix l'espai sense modificar els valors descomprimits. L'eficiència depèn del tipus i del patró de les dades: una classificació amb grans zones repetides es pot comprimir molt, mentre que una superfície sorollosa de coma flotant pot reduir-se menys. La compressió JPEG és amb pèrdua i pot ser adequada per a determinades imatges de visualització; no és apropiada per a elevacions, codis categòrics o altres ràsters analítics que necessiten recuperar exactament els valors.

El **tessel·lat intern** divideix el fitxer en blocs rectangulars. Una lectura d'una finestra només necessita els blocs que la cobreixen, mentre que una organització per tires pot obligar a llegir porcions més extenses. La mida de bloc és una decisió de rendiment, no la resolució espacial de la dada. Tampoc no s'ha de confondre un bloc intern amb les tessel·les XYZ o WMTS d'un mapa web: totes dues tècniques divideixen dades, però tenen contractes i finalitats diferents.

Les **piràmides** o *overviews* són còpies reduïdes per a escales de visualització més petites. QGIS pot mostrar un ràster gran amb molta més rapidesa si llegeix el nivell adequat en lloc de resumir el detall complet a cada moviment. El mètode de generació ha de respectar la semàntica: mitjana per a una superfície contínua quan es vol una vista agregada, i veí més proper o moda per a categories. Una piràmide accelera la representació; no s'ha d'utilitzar com si fos automàticament una capa analítica de resolució més grossa sense documentar com es va crear.

Les piràmides poden quedar dins del GeoTIFF o en fitxers externs. Generar-les internament modifica el fitxer i, per tant, qualsevol suma de comprovació registrada. Les estadístiques, paletes i altres auxiliars també poden aparèixer en fitxers laterals com `.aux.xml`. Abans de traslladar o publicar una capa cal identificar quines peces són necessàries, quines són memòria cau regenerable i quines contenen metadades que no es poden perdre.

## Preparar les dades: combinar i retallar

Els productes extensos es distribueixen sovint en **tessel·les**. Una anàlisi que travessa el límit entre dos fulls necessita primer una cobertura contínua i després un àmbit de treball manejable. Són dues operacions diferents: **combinar** construeix un mosaic a partir de diverses peces; **retallar** redueix o emmascara aquest mosaic. Cap de les dues corregeix per si sola incompatibilitats entre fonts.

### Combinar tessel·les

Abans d'unir-les cal comprovar que les tessel·les comparteixen producte, data o campanya compatible, `CRS`, mida i alineació de cel·la, nombre de bandes, tipus, escala, referència vertical i política de `NoData`. Dues peces que encaixen geomètricament poden provenir d'edicions diferents o aplicar tractaments distints a l'aigua i a la vegetació. La línia de contacte s'ha d'inspeccionar tant visualment com amb perfils o diferències de valors.

Un **ràster virtual**, habitualment un VRT en l'ecosistema GDAL, descriu com es combinen les fonts sense copiar immediatament tots els píxels. És eficient per explorar un mosaic i evita una duplicació gran, però depèn de les rutes i dels fitxers originals. Un mosaic materialitzat crea un nou GeoTIFF amb valors propis, necessita espai i ha de registrar la procedència, l'ordre de solapament i qualsevol remostreig. Si dues tessel·les se superposen, cal saber quina preval; si no estan alineades, abans cal establir una graella de destinació. Combinar no significa calcular una mitjana automàtica entre peces.

A QGIS, l'algorisme `gdal:merge` obre el diàleg **Combinar**. Les entrades han de formar una sola seqüència de tessel·les. L'opció de col·locar cada fitxer en una banda separada ha de quedar desactivada quan es vol un mosaic espacial d'una mateixa variable. Els valors d'absència d'entrada i sortida s'han de declarar perquè el buit d'una tessel·la no tapi valors vàlids d'una altra.

::: subfigures a+b "El menú inicia l'eina Combinar i el diàleg en mostra els paràmetres essencials: les dues tessel·les formen una sola entrada i l'opció de separar-les en bandes queda desactivada."
![Submenú Miscellaneous complet amb l'acció Combina seleccionada]({{ site.baseurl }}/assets/img/qgis/qgis-raster-merge-menu.annotations.svg "Ràster > Miscellaneous > Combina… obre l'eina del proveïdor GDAL.")
![Finestra completa de Combinar amb dues tessel·les MDT25 seleccionades]({{ site.baseurl }}/assets/img/qgis/qgis-raster-merge-dialog.annotations.svg "Les entrades compatibles formen una sola seqüència; el NoData s'ha declarat als paràmetres avançats.")
:::

### Retallar per una capa de màscara

El **retall rectangular** redueix el volum a una extensió. Si els límits es fan coincidir amb la graella de referència, pot conservar exactament els píxels originals. El **retall per màscara** utilitza una geometria vectorial per definir l'àmbit vàlid. La sortida continua sent rectangular, però les cel·les exteriors al polígon queden com a `NoData`. Com que un límit vectorial pot travessar una cel·la, la regla de pertinença altera sobretot zones petites, estretes o amb perímetres complexos.

A QGIS, `gdal:cliprasterbymasklayer` correspon a **Retallar ràster per capa de màscara**. Cal indicar el ràster d'entrada, la capa poligonal i el `NoData` de sortida. L'opció d'ajustar l'extensió a la línia de tall redueix el rectangle al voltant de la màscara, però no garanteix que l'origen coincideixi amb una altra graella: després encara s'han de comprovar mida de cel·la, extensió i alineació.

![Menú Ràster de QGIS amb l'acció Retalla ràster per capa màscara ressaltada]({{ site.baseurl }}/assets/img/qgis/qgis-raster-clip-menu.annotations.svg "L'acció Ràster > Extraction > Retalla ràster per capa màscara… inicia l'eina de retall del proveïdor GDAL."){: data-figure-width-web="44rem" data-figure-width-pdf="100%"}

![Diàleg Retallar ràster per capa de màscara de QGIS amb el mosaic MDT25 i el límit de Vila-seca]({{ site.baseurl }}/assets/img/qgis/qgis-raster-clip-dialog.annotations.svg "El mosaic aporta els valors i el polígon municipal actua com a màscara. Retallar no afegeix detall ni converteix la frontera vectorial en una vora contínua perfecta; decideix quines cel·les continuen sent vàlides."){: data-figure-width-web="44rem" data-figure-width-pdf="100%"}

Retallar massa aviat pot eliminar context necessari. Un pendent necessita veïns, una mitjana focal necessita la finestra completa, una distància necessita conèixer fonts properes de fora del municipi i una conca hidrogràfica pot rebre flux d'aigües amunt. Per això convé calcular sobre una regió amb marge justificat i retallar al límit d'informe després. El marge ha de correspondre al radi del veïnatge, a la distància d'influència o, en processos hidrològics, a tota la conca contribuent.

### Cas guiat: de Tarragona a Vila-seca

El cas comença amb una vista provincial i avança fins al municipi. Aquesta seqüència permet veure per què el producte, la tessel·lació i la resolució s'han d'escollir segons l'escala de la pregunta. Els dos fulls MDT25 i l'MDT200 provincial pertanyen a la primera cobertura PNOA-LiDAR {% cite ignMDT25PrimeraCobertura ignMDT200PrimeraCobertura %}; així s'evita barrejar deliberadament campanyes diferents, encara que això no demostra una data ni un procés de generalització idèntics a totes les cel·les.

::: table "Fonts de la demostració de Vila-seca"
| Entrada | Identitat de descàrrega | Període i suport | Funció |
| --- | --- | --- | --- |
| [MDT200, Tarragona](https://centrodedescargas.cnig.es/CentroDescargas/detalleArchivo?sec=9074255) | CNIG `9074255`; `PNOA_MDT200_ETRS89_HU31_TARRAGONA.TIF` | Primera cobertura, 2009–2011; cel·la de 200 m | Situar el relleu provincial |
| [Límit provincial de Tarragona](https://api-features.ign.es/collections/administrativeunit/items/1174500?f=json) | API OGC Features IGN/CNIG, `administrativeunit/1174500`; `tarragona-cnig.geojson` | Consulta del 18-09-2026; `OGC:CRS84` | Contextualitzar l'MDT200; no intervé en els càlculs |
| [MDT25, full 0472](https://centrodedescargas.cnig.es/CentroDescargas/detalleArchivo?sec=9074092) | CNIG `9074092`; `PNOA_MDT25_ETRS89_HU31_0472_LID.TIF` | Primera cobertura, 2008–2011; cel·la de 25 m | Part occidental del mosaic |
| [MDT25, full 0473](https://centrodedescargas.cnig.es/CentroDescargas/detalleArchivo?sec=9074093) | CNIG `9074093`; `PNOA_MDT25_ETRS89_HU31_0473_LID.TIF` | Primera cobertura, 2008–2011; cel·la de 25 m | Part oriental i control de la costura |
| [Límit municipal de Vila-seca](https://api-features.ign.es/collections/administrativeunit/items/1172246?f=json) | API OGC Features IGN/CNIG, `administrativeunit/1172246` | Consulta del 08-09-2026; `OGC:CRS84`, preparat en `EPSG:25831` | Màscara analítica dels retalls de la demostració |
| [Ortofoto Territorial 2025](https://geoserveis.icgc.cat/servei/catalunya/orto-territorial/wms) | WMS de l'ICGC, capa `ortofoto_25cm_color_2025` | Imatge de context | Reconèixer el territori; no intervé en els càlculs |
:::

Els dos límits són objectes del conjunt oficial *Divisiones Administrativas de España*. L'IGN n'és autor i propietari i el CNIG n'és editor i distribuïdor. El registre de metadades identifica la revisió del producte del 12 de febrer de 2026, una actualització trimestral, escala de referència 1:25.000 i llicència CC BY 4.0; també adverteix que, amb caràcter general, les línies inscrites poden tenir una incertesa geomètrica de l'ordre de 40 m {% cite ignDivisionesAdministrativas2026 %}. Aquesta data descriu el conjunt, no una edició individual dels dos objectes API.

L'API pot serialitzar el mateix objecte amb espais o ordre de claus diferents. Per evitar que aquests canvis irrellevants trenquin la reproducció, el constructor comprova que la resposta provincial sigui l'objecte `1174500`, de nivell `Provincia`, codi oficial `34094300000` i geometria `MultiPolygon`; després n'escriu una representació JSON canònica. Aquesta còpia té SHA-256 `eda078ca366dc266a9f502adf1cefeb5b91f91f22b463d34f0d2bc7556c912b2`, i és la que obre la captura de QGIS.

En la demostració, `municipi_treball` deriva de l'objecte CNIG `1172246` i actua com a màscara analítica. A la micropràctica, en canvi, és la capa heretada de `pr2`: cal conservar al diari quina representació municipal es va escollir, la data, el productor i el llinatge reals, sense atribuir-li automàticament la procedència d'aquest cas resolt.

El MDT200 permet llegir la plana litoral, els relleus interiors i el delta de l'Ebre sense carregar un model més detallat del necessari. El límit administratiu situa quina part de la cobertura correspon a Tarragona; les cel·les transparents continuen sent absències i no cotes zero.

![MDT200 oficial amb el límit de la província de Tarragona, la costa i el delta de l'Ebre visibles]({{ site.baseurl }}/assets/img/qgis/qgis-raster-mdt200-tarragona.annotations.svg "El MDT200 de primera cobertura ofereix context regional amb cel·les de 200 m. El contorn provincial permet interpretar la cobertura i separar el límit administratiu de les vores tessel·lades del ràster."){: data-figure-width-web="46rem" data-figure-width-pdf="100%"}

En acostar-se a Vila-seca, una opacitat del 55% sobre l'Ortofoto Territorial 2025 fa visible el suport de cada valor. La metadada oficial identifica la capa com a `ortofoto_25cm_color_2025` {% cite icgcOrtofotoTerritorial2025 %}. Les vores quadrades no són objectes del paisatge: són cel·les de 200 m. L'ortofoto aporta context visual i la seva graella de resposta no es combina amb l'elevació.

![MDT200 de Vila-seca semitransparent sobre l'Ortofoto Territorial 2025 i el límit municipal]({{ site.baseurl }}/assets/img/qgis/qgis-raster-mdt200-orthophoto.annotations.svg "La superposició relaciona les cel·les de 200 m amb elements recognoscibles. Els valors analítics continuen procedint exclusivament del MDT200."){: data-figure-width-web="46rem" data-figure-width-pdf="100%"}

Els tres models del terreny treballen en `EPSG:25831`, expressen altures ortomètriques en metres i utilitzen `-32767` com a `NoData`. El GeoTIFF identifica el `CRS` horitzontal, però no incorpora un `CRS` vertical separat; no se n'ha d'inferir un datum vertical més específic només a partir del fitxer.

::: table "Geometria dels ràsters preparats de la demostració"
| Sortida | Dimensions | Mida de cel·la | Extensió en `EPSG:25831` (`xmin, ymin, xmax, ymax`) |
| --- | --- | --- | --- |
| Mosaic MDT25 dels fulls 0472 i 0473 | 2.262 × 794 | 25 × 25 m | `315937.5, 4539787.5, 372487.5, 4559637.5` |
| MDT25 retallat a Vila-seca | 382 × 294 | 25 × 25 m | `339912.5, 4547637.5, 349462.5, 4554987.5` |
| MDT200 retallat a Vila-seca | 48 × 38 | 200 × 200 m | `339900, 4547500, 349500, 4555100` |
:::

Els fulls MDT25 formen un VRT amb `-32767` com a absència i després es materialitzen en un GeoTIFF `Float32`; no es remostregen ni es converteixen els buits en zeros. El pendent i l'orientació es calculen sobre el mosaic complet i només després es retallen. Els retalls conserven la graella nativa de cada producte, forcen la lectura del nivell base i no incorporen piràmides analítiques.

Els orígens dels MDT25 i MDT200 publicats difereixen 12,5 m. Per tant, les dues graelles no són niades i la comparació següent no autoritza una resta cel·la a cel·la ni permet atribuir tota diferència només a la resolució. Les vistes comparteixen àmbit, escala i rang de color de 0 a 80 m perquè el canvi de suport sigui visible.

::: subfigures a+b "El mateix àmbit de Vila-seca representat primer amb el MDT200 i després amb el MDT25 oficials. La cel·la de 200 m generalitza molt més el relleu; les graelles publicades, però, també tenen orígens diferents i no constitueixen encara un experiment controlat."
![MDT200 oficial retallat a Vila-seca amb cel·les de 200 metres]({{ site.baseurl }}/assets/img/qgis/qgis-raster-mdt200-vila-seca.annotations.svg "MDT200: 48 × 38 cel·les, amb el mateix rang de color que el panell següent.")
![MDT25 oficial retallat a Vila-seca amb cel·les de 25 metres]({{ site.baseurl }}/assets/img/qgis/qgis-raster-mdt25-vila-seca.annotations.svg "MDT25: 382 × 294 cel·les i més variació local visible.")
:::

Les [especificacions tècniques PNOA-LiDAR](https://pnoa.ign.es/web/portal/pnoa-lidar/especificaciones-tecnicas) permeten separar mida de cel·la, densitat de mostreig i exactitud declarada. Els identificadors, les mides i les sumes SHA-256 de les descàrregues es conserven a la configuració reproduïble del projecte, no com a part de la lectura inicial del mapa.

## Semàntica i remostreig dels valors

El **remostreig** estima quin valor correspon a cada cel·la d'una graella de destinació. Apareix quan canvien la resolució, l'origen o el `CRS`, i també quan un canvi d'extensió obliga a crear una graella diferent. Un retall rectangular alineat amb les vores de la malla pot conservar exactament les cel·les font i no necessita estimar-ne valors nous. Encara que la interfície presenti aquestes operacions per separat, una reprojecció ràster sempre necessita decidir on queda la nova graella i com obté els seus valors. El mètode s'ha de triar segons què representa la banda i segons si es redueix o s'augmenta la mida de cel·la. La distinció anterior entre variables contínues, categories i magnituds intensives o extensives impedeix aplicar la mitjana a codis o totals i la suma a valors que ja són densitats.

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

La terminologia dels productes no és completament uniforme. Cal comprovar sempre la definició del productor en lloc de deduir el contingut només de les sigles {% cite felicisimoModelosDigitalesTerreno1994 nunesDiccionariSIG2012 %}.

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

La conversió inversa és $\theta = \arctan(p/100)$. La relació no és lineal: increments iguals en graus no corresponen a increments iguals en percentatge, i el percentatge creix sense límit quan l'angle s'aproxima als 90°.

![Set facetes mostren seccions progressivament inclinades entre zero i quaranta-cinc graus, cadascuna amb l'alçada assolida i el càlcul del pendent percentual]({{ site.baseurl }}/assets/quarto/07-model-analisi-raster/slope-degrees-percent.qmd "Cada secció manté 100 m de distància horitzontal, identifica l'alçada assolida i calcula el pendent com a guany vertical dividit per aquesta distància i multiplicat per cent. Per això, en aquest exemple, el desnivell en metres coincideix numèricament amb el percentatge."){: data-figure-width-web="46rem" data-figure-width-pdf="100%"}

El factor vertical, sovint anomenat factor `z`, relaciona les unitats d'altura amb les horitzontals. Només és 1 quan són compatibles, per exemple metres en tots dos casos. Calcular pendent directament sobre una graella geogràfica en graus amb elevacions en metres exigeix una conversió que varia amb la latitud o, preferiblement per a l'àmbit local, una reprojecció adequada. Un resultat entre 0 i 90 no demostra que el càlcul sigui correcte.

A la demostració, el pendent es calcula amb GDAL sobre el mosaic MDT25 en `EPSG:25831`, amb l'algorisme de Horn, factor d'escala 1 i sense inventar valors a les vores. El derivat es crea abans del retall municipal perquè el veïnatge de 3 × 3 disposi de context exterior. La lectura força la resolució base i les sortides analítiques no contenen piràmides, de manera que el càlcul no pot consumir silenciosament una vista general de resolució inferior.

A QGIS, l'acció `Ràster > Analysis > Pendent…` inicia l'eina del proveïdor GDAL. Per reproduir el càlcul cal registrar l'algorisme i els paràmetres, no només la ruta de menú.

![Menú Ràster de QGIS amb el submenú Analysis obert i l'acció Pendent ressaltada]({{ site.baseurl }}/assets/img/qgis/qgis-raster-slope-menu.annotations.svg "L'acció Ràster > Analysis > Pendent… inicia l'eina de càlcul del pendent."){: data-figure-width-web="44rem" data-figure-width-pdf="100%"}

Les dues unitats es calculen des del mateix MDT25 i amb el mateix algorisme. El domini observat és de 0 a 14,3° i de 0 a 25,6%; la comprovació numèrica de $p = 100\tan(\theta)$ dona un error màxim de `1,91 × 10^-6`, atribuïble a la precisió de coma flotant. Per tant, els patrons espacials coincideixen, però els nombres i qualsevol llindar s'han d'interpretar en la unitat declarada. Les dues sortides comparteixen extensió, cel·les vàlides, algorisme i rampa de color; només canvia la unitat i el rang numèric corresponent.

::: subfigures a+b "El mateix pendent expressat en graus i en percentatge. El patró espacial coincideix perquè les dues sortides provenen del mateix MDT25 i algorisme; els valors numèrics i els llindars no són intercanviables."
![Mapa en graus del pendent del MDT25 de Vila-seca]({{ site.baseurl }}/assets/img/qgis/qgis-raster-slope-degrees.annotations.svg "La sortida en graus mesura l'angle respecte del pla horitzontal i presenta valors de 0 a 14,3°.")
![Mapa en percentatge del pendent del MDT25 de Vila-seca]({{ site.baseurl }}/assets/img/qgis/qgis-raster-slope-percent.annotations.svg "La sortida percentual mesura cent vegades el quocient entre desnivell i distància horitzontal i presenta valors de 0 a 25,6%.")
:::

L'**orientació** indica la direcció de màxim descens. Sol expressar-se com un angle circular, però cal comprovar si 0° correspon al nord, en quin sentit creixen els angles i quin valor identifica superfícies planes. 1° i 359° són direccions pròximes, encara que la seva mitjana aritmètica sigui 180°. Per resumir orientacions cal utilitzar estadística circular, basada en components sinus i cosinus, i informar també de la concentració direccional.

En una superfície gairebé plana, petits errors verticals poden canviar molt l'orientació perquè no hi ha una direcció dominant. Convé separar cel·les per sota d'un llindar de pendent justificat abans d'agrupar exposicions nord, est, sud i oest. Aquest llindar no és universal: depèn de la qualitat del MDE i de la finalitat. La classe «pla» ha de continuar distingida de `NoData`.

En l'exemple de Vila-seca s'adopta 2° com a llindar docent: les cel·les inferiors queden en gris i la resta s'agrupen en nord, est, sud i oest. El mapa mostra sobretot com una decisió explícita evita assignar una orientació aparent a superfícies gairebé planes; no estableix que 2° sigui un valor universal per a qualsevol MDE o finalitat.

![Orientació del MDT25 de Vila-seca agrupada en superfícies planes i quatre sectors cardinals]({{ site.baseurl }}/assets/img/qgis/qgis-raster-aspect-sectors.annotations.svg "La classificació representa en gris les cel·les amb pendent inferior a 2°, i en blau, groc, vermell i porpra les orientacions nord, est, sud i oest. NoData continua fora de totes les classes."){: data-figure-width-web="44rem" data-figure-width-pdf="100%"}

![Una finestra de nou elevacions mostra el gradient local, la direcció de màxim descens, el pendent corresponent en perfil i la diferència entre una cel·la plana i NoData]({{ site.baseurl }}/assets/quarto/07-model-analisi-raster/terrain-gradient-slope-aspect.qmd "En aquest esquema didàctic de diferències centrals, una graella de 25 m produeix un pendent de 10,1°, equivalent al 17,9%, i un aspecte de 153,4° mesurat en sentit horari des del nord. El mateix gradient determina les dues magnituds; els proveïdors poden aplicar altres estimadors. Una superfície plana conté dades vàlides però no una direcció estable, mentre que NoData indica absència de valor."){: data-figure-width-web="33.5rem" data-figure-width-pdf="75%"}

### Ombrejat, curvatura i rugositat

L'**ombrejat del relleu** simula la il·luminació d'una superfície segons un azimut i una altura solar. Ajuda a percebre formes, però no és una observació de llum ni una banda d'elevació. Canviar la direcció de la llum pot fer més visibles unes valls i ocultar-ne d'altres, i la il·lusió perceptiva pot invertir el relleu si la llum sembla venir de baix. Un ombrejat multidireccional pot reduir part del biaix, però també és una representació derivada i n'ha de conservar els paràmetres.

La **curvatura** descriu com canvia el pendent. La curvatura de perfil es relaciona amb l'acceleració o desacceleració del flux en la direcció del vessant, mentre que la curvatura en planta ajuda a descriure convergència i divergència lateral. Són derivades de segon ordre i amplifiquen soroll, errors de tessel·la i artefactes d'interpolació. Abans d'interpretar-les cal examinar el MDE, provar l'escala del veïnatge i evitar una precisió decimal que la font no sosté.

Mesures com rugositat, índex de rugositat del terreny o posició topogràfica comparen una cel·la amb el seu entorn. El resultat canvia radicalment amb la mida de la finestra: una depressió local dins d'un radi de 75 m pot formar part d'una plana dins d'un radi de 2 km. El nom de l'índex no defineix l'escala; el radi o dimensions del veïnatge han d'aparèixer als paràmetres i a la interpretació.

### Corbes, perfils, drenatge i visibilitat

Les **corbes de nivell** uneixen posicions d'igual altura interpolades sobre el MDE. Una equidistància petita no millora la precisió vertical de la font i pot crear línies molt sinuoses sobre soroll local. Els **perfils** mostren l'elevació al llarg d'un traçat i són útils per comprovar ruptures, costures de mosaic i efectes de resolució. Tant les corbes com els perfils són derivats: han de mantenir la referència al MDE i no substituir-ne les metadades.

L'anàlisi hidrològica sol preparar el MDE abans de calcular direcció i acumulació de flux. Emplenar totes les depressions força la continuïtat del drenatge, però també pot eliminar cubetes reals; obrir una sortida o cremar una xarxa imposa una altra hipòtesi. L'algorisme de direcció pot enviar el flux a un sol veí o repartir-lo entre diversos, i l'acumulació es pot expressar en nombre de cel·les o en superfície contribuent. Sense aquestes decisions, una xarxa derivada no es pot interpretar com una xarxa hidrogràfica observada.

Una **conca visual** determina quines cel·les mantenen línia de visió amb un observador segons la superfície disponible. Necessita posició i altura de l'observador, altura de l'objectiu i, segons la distància, tractament de curvatura i refracció. Un MDT omet edificis i arbres; un MDS els pot incorporar segons la data i la resolució. La sortida representa visibilitat modelada, no tot allò que una persona veuria en condicions reals.

![Quatre facetes deriven d'un mateix model d'elevacions de dos cims el traçat, el perfil, la visibilitat acolorida al llarg del perfil i la conca visual]({{ site.baseurl }}/assets/quarto/07-model-analisi-raster/terrain-profile-viewshed.qmd "Les corbes de nivell, el perfil A–B, la visibilitat al llarg del perfil i la conca visual es calculen sobre una única superfície de dos cims. Els mateixos colors distingeixen posicions visibles i ocultes tant al perfil com a la conca visual."){: data-figure-width-web="46rem" data-figure-width-pdf="100%"}

### Veïnatge i connectivitat {#veinatge-connectivitat}

En una graella quadrada, el **model de torre**, o connectivitat de **4 veïns**, considera adjacents les cel·les que comparteixen un costat amb la cel·la central: nord, sud, est i oest. El **model de reina**, o connectivitat de **8 veïns**, hi afegeix les quatre cel·les que només comparteixen una cantonada. Els noms recorden els moviments d'aquestes peces d'escacs; la cel·la central no es compta com a veïna d'ella mateixa.

La tria modifica el resultat. Dues cel·les de la mateixa classe que només es toquen en diagonal formen dues regions amb el model de torre i una sola regió amb el model de reina. La decisió afecta l'etiquetatge de components, la vectorització de classes, l'expansió de regions i els camins permesos en una superfície de cost. En una operació focal, una finestra de 3 × 3 pot utilitzar els vuit veïns i la cel·la central, però també pot excloure posicions o assignar pesos diferents; els models de 4 i 8 veïns descriuen connectivitat, no totes les finestres possibles.

### Efectes de vora

Qualsevol operació de veïnatge perd informació al límit del ràster. Una finestra de 3 × 3 no pot calcular-se de la mateixa manera a la primera fila si falten els veïns exteriors. L'eina pot retornar `NoData`, reduir la finestra, replicar valors o aplicar una altra regla. El resultat pot formar un marc artificial al voltant de la capa sense produir cap missatge d'error.

Els derivats del municipi s'han de calcular sobre una franja de dades exterior i retallar-se després al límit d'informe. Si el MDT es talla exactament pel polígon municipal abans del pendent, les cel·les de vora perden veïns; si es calcula una distància només amb fonts interiors, s'ignoren elements externs que podrien ser els més pròxims; si s'extreu una conca dins del rectangle local, s'omet cabal potencial procedent de fora. El marge s'ha de derivar de l'operació, no adoptar-se per costum.

## Àlgebra de mapes i reclassificació

L'**àlgebra de mapes** tracta les graelles com a operands.

Operació local
: Calcula cada cel·la a partir dels valors de la mateixa posició.

Operació focal
: Utilitza un veïnatge al voltant de cada cel·la.

Operació zonal
: Resumeix les cel·les que pertanyen a una zona comuna.

Operació global
: Pot dependre de tota la superfície, com una distància acumulada.

Aquesta classificació ajuda a anticipar quines capes han d'estar alineades i quin context exterior necessita cada càlcul.

![Quatre panells comparen una operació ràster local entre cel·les alineades, una mitjana focal en una finestra de tres per tres, un resum zonal i una superfície global de distància]({{ site.baseurl }}/assets/quarto/07-model-analisi-raster/raster-neighborhood-operations.qmd "El suport necessari creix de la posició compartida al veïnatge, a les cel·les d'una zona i a la superfície completa; aquesta dependència determina alineació, marge i regles de vora."){: data-figure-width-web="56rem" data-figure-width-pdf="100%"}

Una expressió local pot sumar bandes, calcular una diferència, normalitzar un valor o avaluar una condició. Abans d'executar-la cal comprovar unitats i dominis. Restar metres a graus no té sentit; dividir per una banda que conté zeros necessita una regla; combinar una data amb una altra pot descriure canvi només si les fonts són comparables. El fet que la calculadora retorni nombres no valida l'operació.

La **reclassificació** converteix valors o intervals en classes. Els intervals han de cobrir el domini previst, no solapar-se i declarar el tractament dels límits. Una taula pot definir, per exemple, `[0, 2)` com a pendent suau i `[2, 5)` com a pendent moderat; escriure només `0–2` i `2–5` deixa ambigu on cau exactament el valor 2. També s'han de separar valors fora de rang i `NoData`.

Els llindars poden provenir d'una norma, d'una relació funcional, de la distribució observada o d'una decisió exploratòria. Aquestes justificacions no són intercanviables. Si un llindar canvia entre municipis perquè s'adapta a quantils locals, les classes ja no representen els mateixos valors absoluts; si es manté un llindar comú, alguns municipis poden quedar gairebé en una sola classe. La comparació exigeix decidir quina propietat es vol conservar.

### De les consultes als predicats ràster

Al capítol de consultes, un predicat s'avaluava per a cada fila d'una taula i retornava cert o fals. En una expressió ràster, el mateix principi s'aplica a cada posició de la graella. La comparació següent pregunta si l'elevació és inferior a 2 m. En una cel·la vàlida, QGIS codifica habitualment el resultat cert com a 1 i el fals com a 0:

::: listing "Predicat ràster elemental sobre l'elevació"
```text
"elevacio@1" < 2
```
:::

Els operadors lògics permeten construir preguntes més precises. `NOT` nega una condició, `AND` exigeix que totes siguin certes i `OR` n'accepta almenys una. Els parèntesis fan explícit què s'avalua primer i són imprescindibles quan es barregen comparacions i operadors:

::: listing "Progressió de predicats i operadors booleans"
```text
NOT ("elevacio@1" < 2)

("elevacio@1" < 20) AND ("pendent_graus@1" < 2)

("orientacio_graus@1" >= 315) OR ("orientacio_graus@1" < 45)
```
:::

La primera expressió selecciona el complement de les cotes inferiors a 2 m dins del domini vàlid. La segona conserva només cel·les baixes i planes. La tercera mostra per què `OR` és necessari en una variable circular: el sector nord travessa el canvi entre 359° i 0°. Una cel·la `NoData` no és una condició falsa; és una posició no avaluada i s'ha de mantenir fora de les classes tret que s'hagi justificat una altra política.

QGIS ofereix dues eines amb noms semblants que no s'han de confondre: la **Calculadora ràster** autònoma de `Ràster > Calculadora ràster…` i l'algorisme de Processament `native:rastercalc`. Aquest capítol i el contracte de la micropràctica utilitzen `native:rastercalc`; per reproduir el càlcul cal registrar l'identificador, les capes, l'expressió i la graella de sortida. El diàleg no resol una desalineació conceptual: totes les bandes que participen en una operació cel·la a cel·la han de compartir abans `CRS`, extensió, mida i origen.

![Menú Ràster de QGIS amb l'acció Calculadora ràster ressaltada]({{ site.baseurl }}/assets/img/qgis/qgis-raster-calculator-menu.annotations.svg "La calculadora autònoma forma part del menú Ràster. El procediment d'aquest capítol utilitza, en canvi, l'algorisme de Processament native:rastercalc."){: data-figure-width-web="44rem" data-figure-width-pdf="100%"}

![Calculadora ràster de Processament amb dues capes alineades i una expressió que combina elevació i pendent amb AND]({{ site.baseurl }}/assets/img/qgis/qgis-raster-calculator-boolean.annotations.svg "L'algorisme native:rastercalc fixa extensió, cel·la de 25 m i EPSG:25831. L'expressió combina cota inferior a 20 m i pendent inferior a 2°; és el criteri del posterior experiment controlat, no el cribratge costaner de 2 m."){: data-figure-width-web="44rem" data-figure-width-pdf="100%"}

La demostració de la Pineda utilitza el predicat elemental per separar les cotes inferiors a 2 m de la classe complementària. Els codis 1 i 2 són etiquetes, no elevacions noves:

::: listing "Dues classes d'elevació separades pel llindar de 2 metres"
```text
1 * ("elevacio@1" < 2) + 2 * ("elevacio@1" >= 2)
```
:::

La condició inferior utilitza l'interval obert per la dreta i la complementària inclou exactament 2 m; així no queda cap valor vàlid sense classe ni cap valor assignat dues vegades. Sobre les 34.734 cel·les vàlides del retall MDT25, 2.150 queden per sota del llindar, un 6,19%.

![Classificació del MDT25 de Vila-seca entre cotes inferiors a dos metres en blau i la resta del terreny en ocre]({{ site.baseurl }}/assets/img/qgis/qgis-raster-elevation-classes.annotations.svg "El llindar de 2 m produeix un cribratge topogràfic simple. La classe ocre és el complement dins de les cel·les vàlides; l'absència de dades no pertany a cap classe."){: data-figure-width-web="44rem" data-figure-width-pdf="100%"}

A QGIS, `gdal:polygonize` vectoritza totes les classes presents a la banda seleccionada. En aquest cas s'utilitzen `Elevació MDT25 · llindar 2 m`, la banda 1 i el camp de sortida `classe`; l'opció de connectivitat de vuit veïns queda desactivada, de manera que s'aplica el model de torre i només comparteixen regió les cel·les unides per un costat.

![Diàleg Vectoritza de QGIS amb el ràster classificat, el camp classe i la connectivitat de vuit veïns desactivada]({{ site.baseurl }}/assets/img/qgis/qgis-raster-polygonize-dialog.annotations.svg "L'algorisme gdal:polygonize conserva el codi de cada regió al camp classe. La connectivitat de vuit veïns queda desactivada perquè les cel·les que només es toquen per una cantonada romanguin separades."){: data-figure-width-web="44rem" data-figure-width-pdf="100%"}

La sortida completa conté 185 polígons: 95 de classe 1 i 90 de classe 2. Filtrar `classe = 1` conserva les regions amb `elevacio < 2 m`, que segueixen les vores de la graella de 25 m. L'àrea total, `1.343.750 m²`, coincideix amb les 2.150 cel·les multiplicades pels `625 m²` de cada suport. Amb el model de reina, de vuit veïns, la mateixa classe quedaria agrupada en només 24 polígons; la connectivitat és, per tant, un paràmetre geomètric del resultat i no una simple opció visual. La vectorització no recupera un límit continu original ni converteix automàticament la classe en una zona inundable.

![Polígons derivats de les cel·les del MDT25 situades per sota de dos metres sobre l'Ortofoto Territorial 2025]({{ site.baseurl }}/assets/img/qgis/qgis-raster-low-elevation-polygons.annotations.svg "La vectorització fa visible el contorn esglaonat i les illes creades per la classificació de la graella. L'ortofoto només aporta context visual; no intervé en el llindar ni en la geometria resultant."){: data-figure-width-web="46rem" data-figure-width-pdf="100%"}

Una segona expressió combina l'orientació amb el llindar de pendent que separa les superfícies planes. La convenció angular de l'algorisme situa el sector sud entre 135° inclosos i 225° exclosos:

::: listing "Màscara de cel·les orientades al sud amb pendent mínim de dos graus"
```text
("pendent_graus@1" >= 2) AND
("orientacio_graus@1" >= 135) AND
("orientacio_graus@1" < 225)
```
:::

La màscara identifica 2.764 cel·les, un 7,96% del domini vàlid. El recompte prova l'execució de la lògica, però no converteix el criteri en una estimació energètica.

![Màscara del MDT25 de Vila-seca amb els sectors orientats al sud i pendent mínim de dos graus en taronja]({{ site.baseurl }}/assets/img/qgis/qgis-raster-south-facing.annotations.svg "La classe taronja combina orientació i pendent; la resta de cel·les vàlides queda en gris. El resultat descriu la geometria aproximada del terreny, no la radiació rebuda."){: data-figure-width-web="44rem" data-figure-width-pdf="100%"}

### Combinació categòrica de ràsters

La **combinació categòrica**, anomenada sovint *Combine* en alguns SIG, no és l'eina **Combinar** que crea un mosaic de tessel·les. Aquí es crea una classe nova per a cada parella de codis en la mateixa posició. Si una cel·la és `bosc` a la coberta de 2020 i `urbà` a la de 2025, la sortida identifica la transició `bosc → urbà`. Les entrades han de compartir geometria de graella i una taula ha de relacionar cada codi nou amb les classes originals.

En una calculadora ràster es pot construir un codi sense col·lisions quan els dominis són coneguts. Si totes dues entrades utilitzen enters de `0` a `99`, una forma possible és:

::: listing "Codi de combinació per a dues classificacions amb dominis controlats"
```text
("coberta_2020@1" * 100) + "coberta_2025@1"
```
:::

El codi `103` significa classe 1 a la primera entrada i classe 3 a la segona només perquè la base 100 s'ha declarat abans. Amb codis negatius, decimals o superiors, la fórmula podria col·lidir i caldria una taula creuada. `NoData` s'ha de mantenir separat: forçar-lo a zero faria aparèixer transicions fictícies des d'una classe 0.

>>>> **Cribratge no és modelització del fenomen.** Una cota inferior a 2 m no és una zona inundable: falten cabals o nivells, connectivitat hidràulica, drenatge, rugositat, infraestructures, condicions de contorn i validació. Una orientació sud tampoc no és radiació solar: falten data i hora, trajectòria solar, ombres, nuvolositat, atmosfera i, si l'objecte és una coberta, un MDS adequat. Les dues operacions són exemples explicatius i no afegeixen lliurables a la micropràctica 5.

Una anàlisi multicriteri ponderada necessita encara més decisions: transformar variables a una escala comuna, establir la direcció de preferència, tractar valors extrems, justificar pesos i distingir restriccions absolutes de factors compensables. Un pes alt no converteix una font incerta en una evidència millor. Abans d'acceptar un mapa final convé variar llindars i pesos dins d'un rang justificable i identificar quines zones depenen d'una elecció fràgil.

## Superfícies de distància i cost

Una **distància euclidiana** assigna a cada cel·la la separació en línia recta fins a la font més pròxima. La font pot provenir de punts, línies, polígons o cel·les seleccionades, però ha de quedar rasteritzada sobre una graella definida. El resultat depèn del `CRS`, de les unitats i de com es representa el límit de la font. En un `CRS` geogràfic, una diferència angular no s'ha d'interpretar directament com metres.

A diferència d'una àrea d'influència vectorial, que crea un polígon dins o fora d'un llindar, la superfície de distància conserva un valor per a totes les cel·les avaluades. Reclassificar-la amb `distància <= d` produeix una aproximació ràster del buffer, sensible a la mida i l'origen de la graella. Tampoc no equival a una matriu vectorial: la matriu enumera parelles d'entitats, mentre que la superfície respon quina font és més pròxima a cada posició del domini.

La distància entre centres introdueix una aproximació que es fa més visible en cel·les grosses. Una font estreta pot desplaçar-se fins al centre de la cel·la que la representa, i la seva forma pot desaparèixer o engruixir-se. Quan el llindar és semblant a la mida de cel·la, la classificació dins o fora de la distància és especialment sensible a l'origen de la malla. Convé comparar una mostra amb mesures vectorials i quantificar la franja d'incertesa al voltant del llindar.

En el cas preparat de Vila-seca, `gdal:proximity` pren com a fonts només les cel·les amb valor 1 del ràster classificat. Els paràmetres `VALUES = 1`, unitats en coordenades georeferenciades, distància màxima 0 —sense límit—, `NoData = -32767` i sortida `Float32` produeixen metres perquè la graella treballa en `EPSG:25831`. El paràmetre avançat `-use_input_nodata YES` exclou del càlcul les cel·les `NoData` de l'entrada. Cada cel·la vàlida rep la distància euclidiana entre el seu centre i el centre de la cel·la font més pròxima; no és una distància fins a una isolínia contínua ni fins a la vora exterior del polígon vectoritzat.

![Diàleg Proximitat de QGIS configurat per calcular distàncies a les cel·les de classe 1 en unitats georeferenciades]({{ site.baseurl }}/assets/img/qgis/qgis-raster-proximity-dialog.annotations.svg "La classe 1 defineix les fonts i les coordenades georeferenciades fan que la sortida s'expressi en metres."){: data-figure-width-web="44rem" data-figure-width-pdf="100%"}

La sortida conserva les 382 × 294 posicions de la graella de 25 m i 34.734 cel·les vàlides. Les 2.150 cel·les font tenen distància zero; la mitjana de tot el domini vàlid és `3.175,08 m`, mentre que la de les 32.584 cel·les amb distància superior a zero és `3.384,58 m`. La distància màxima és `7.100,44 m`. Com que l'entrada ja estava retallada a Vila-seca, aquestes xifres busquen fonts només dins del domini preparat: una font exterior més pròxima no hi pot intervenir.

Per comparar suports es fixa un llindar docent de 250 m, equivalent a deu amplades de cel·la. A QGIS, la superfície es reclassifica conceptualment amb `distancia <= 250`, mentre que `native:buffer` crea un buffer dissolt de 250 m al voltant dels 95 polígons. La primera operació mesura des dels centres de les cel·les font; la segona parteix de les seves vores.

![QGIS amb la superfície de distància, els polígons font i el buffer vectorial de 250 metres ordenats al panell Capes]({{ site.baseurl }}/assets/img/qgis/qgis-raster-distance-buffer-comparison.annotations.svg "La superfície ràster conserva un valor continu a cada centre de cel·la. El buffer vectorial delimita una àrea binària des de les vores dels polígons derivats; les dues fronteres no han de coincidir exactament."){: data-figure-width-web="46rem" data-figure-width-pdf="100%"}

::: table "Comparació del llindar de 250 m sobre la mateixa màscara vàlida"
| Resultat mostrejat pels centres de la graella | Cel·les | Superfície representada |
| --- | ---: | ---: |
| Distància ràster `<= 250 m` | 5.915 | 3.696.875 m² |
| Buffer vectorial de 250 m | 5.979 | 3.736.875 m² |
| Coincidència | 5.915 | 3.696.875 m² |
| Només buffer | 64 | 40.000 m² |
:::

L'acord de Jaccard és del 98,93%. Les 64 cel·les addicionals del buffer són coherents amb la diferència de referència: el buffer comença a la vora de la petjada de 25 m i la proximitat comença al centre. L'àrea vectorial exacta del buffer retallat al municipi és `3.735.639,09 m²`, lleugerament diferent dels `3.736.875 m²` obtinguts en comptar cel·les completes pels centres. Ni el recompte de cel·les ni aquesta àrea s'han d'interpretar com una zona de risc; només comproven l'efecte del suport espacial.

Una **distància de cost** acumula una fricció en travessar les cel·les. Una superfície de cost pot representar temps per metre, energia, dificultat o una combinació explícita. Els valors han de tenir una interpretació dimensional coherent: sumar pendents, metres i categories codificades sense transformació no produeix un cost interpretable. Les barreres també s'han de distingir de `NoData`; una cel·la prohibida, una cel·la desconeguda i una cel·la molt costosa no expressen el mateix.

El cost pot ser **anisòtrop** quan depèn de la direcció. Pujar i baixar un vessant no exigeix el mateix esforç, i moure's a favor o en contra d'un corrent tampoc. Una superfície de fricció única és isòtropa i no captura aquesta diferència. La resolució controla quines barreres i corredors existeixen a la malla: una carretera estreta o un pas entre obstacles pot desaparèixer a 200 m i alterar completament la connectivitat.

Les superfícies de distància no substitueixen automàticament una xarxa. Una xarxa conserva nodes, arcs, sentits i restriccions; un ràster de cost permet moviment sobre una superfície segons un veïnatge. Tots dos poden modelar accessibilitat, però responen a representacions diferents del problema. La tria s'ha de justificar segons si el moviment queda restringit a vies o pot travessar el territori.

## Relació entre ràster i vector

Rasteritzar una capa vectorial exigeix fixar una graella de referència, seleccionar un atribut o valor constant i decidir quines cel·les s'activen. La regla basada en el centre és conservadora però pot perdre línies estretes; la regla d'incloure totes les cel·les tocades conserva presència però eixampla objectes i augmenta superfícies. Quan diverses entitats ocupen una mateixa cel·la, l'ordre, la prioritat o l'agregació han de quedar definits.

Vectoritzar un ràster crea geometries que segueixen les vores de les cel·les. Una classificació sorollosa pot produir milers de polígons petits i contorns esglaonats. Dissoldre per classe redueix registres però no recupera el límit original ni elimina la incertesa de classificació. Suavitzar el contorn canvia novament la geometria i s'ha de considerar una generalització, no una restauració.

![Un polígon vectorial sobre una graella es rasteritza segons els centres de cel·la i es torna a vectoritzar com un contorn esglaonat]({{ site.baseurl }}/assets/quarto/07-model-analisi-raster/vector-raster-conversion.qmd "Rasteritzar exigeix una graella i una regla d'activació; vectoritzar després conserva les vores de les cel·les classificades, però no recupera el límit continu original."){: data-figure-width-web="56rem" data-figure-width-pdf="100%"}

### Estadístiques zonals

Les **estadístiques zonals** resumeixen els valors d'un ràster dins de zones, normalment polígons vectorials. Per a elevació o pendent poden ser útils el recompte vàlid, la mitjana, la mediana, la desviació, el mínim i el màxim. Alguns proveïdors ofereixen també percentils, però no formen part dels estadístics disponibles a `native:zonalstatisticsfb`. La suma d'elevacions o pendents no té una interpretació territorial directa. Per a categories interessen els recomptes i proporcions per classe, no la mitjana dels codis.

La regla de pertinença de cel·les a una zona condiciona el resultat. Aquest algorisme prova primer els centres de les cel·les: només incorpora els centres situats dins del polígon que tenen un valor vàlid, diferent de `NoData`. Si aquesta primera passada produeix zero o una cel·la, en descarta els acumulats i repeteix el càlcul mitjançant interseccions precises entre cada píxel i el polígon. En aquesta segona passada, cada píxel contribueix al recompte amb la fracció de la seva àrea intersectada i a la suma amb el valor multiplicat per la mateixa fracció. Per això el recompte pot ser decimal i la mitjana és una mitjana ponderada per l'àrea intersectada.

Aquesta ponderació no converteix automàticament tots els estadístics disponibles en estimadors ponderats de la mateixa manera. En el recàlcul precís, la mediana i la desviació no tenen el mateix contracte fraccionari que el recompte, la suma i la mitjana. Per això la comparació controlada d'aquest capítol no les utilitza quan alguna zona activa aquesta segona passada. Si fossin necessàries, caldria calcular-les amb una regla de pesos explícita i idèntica a totes dues resolucions.

>>>> **Un recompte fraccionari no indica una taula corrupta.** En una zona petita o estreta pot revelar que QGIS ha activat el càlcul precís de píxel contra polígon. Arrodonir-lo abans de calcular superfícies o percentatges eliminaria justament la ponderació aplicada a les cel·les de vora; cal conservar el valor i registrar la versió de l'algorisme.

Per a una màscara binària on 1 representa la classe, 0 una cel·la avaluada que no hi pertany i `NoData` una absència, la superfície de la classe s'aproxima multiplicant la suma zonal per l'àrea d'una cel·la; el recompte multiplicat per aquesta àrea representa, en canvi, la superfície avaluada. A 25 m, cada cel·la quadrada representa 625 m²; a 200 m, 40.000 m². La mitjana de la màscara, equivalent a suma dividida per recompte, estima la proporció de superfície de la classe dins de l'àrea vàlida. Amb la prova ordinària de centres, recompte i suma acumulen cel·les completes i l'aproximació es concentra al límit vectorial. Amb el recàlcul precís de QGIS, tots dos acumulen fraccions d'intersecció; no s'han d'arrodonir ni tornar a ponderar com si totes les contribucions fossin cel·les completes.

En la comprovació de la superfície de distància, `native:zonalstatisticsfb` rep `Límit de Vila-seca` com a zona, `Distància a zones baixes · 25 m` com a ràster, la banda 1 i el prefix `z25_dist_`. Se seleccionen recompte, mitjana, mínim i màxim; no cal activar estadístics sense una interpretació prevista.

![Diàleg Estadístiques de zona de QGIS amb Vila-seca, la superfície de distància i quatre estadístics seleccionats]({{ site.baseurl }}/assets/img/qgis/qgis-raster-zonal-statistics-dialog.annotations.svg "L'algorisme native:zonalstatisticsfb resumeix la banda 1 dins del polígon municipal i escriu camps amb el prefix z25_dist_."){: data-figure-width-web="44rem" data-figure-width-pdf="100%"}

El resultat retorna `z25_dist_count = 34.734`, `z25_dist_mean = 3.175,08 m`, `z25_dist_min = 0 m` i `z25_dist_max = 7.100,44 m`. El recompte coincideix amb el domini vàlid verificat al GeoTIFF i els extrems coincideixen amb la validació del constructor. La mitjana resumeix valors als centres de les cel·les; no és una distància contínua ponderada sobre tots els punts del municipi.

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

Les captures anteriors responen com difereixen **dos productes oficials publicats**. Compartir el primer cicle PNOA-LiDAR redueix una font de confusió temporal, però els orígens desplaçats 12,5 m i un procés de producció que no es controla impedeixen presentar la diferència com l'efecte causal pur de la mida de cel·la. L'experiment següent respon una pregunta més limitada: què canvia quan es manté fixa una font comuna i només es construeixen dos suports niats.

Per a aquest experiment controlat, la font ha de ser comuna i prou detallada per sostenir les dues sortides. Si el producte original és més gros que 25 m, remostrejar-lo a 25 m no permet presentar aquesta branca com a observació fina. Es conservaran el paquet original, les metadades, la data d'accés i la identificació exacta del producte. El límit de Vila-seca o del municipi assignat serà la zona d'informe, però l'entrada d'elevacions inclourà un marge suficient per als derivats.

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

Una implementació de referència fixa els algorismes i els paràmetres que afecten el resultat. Les coordenades exactes de l'extensió i el valor `NoData` s'han d'emplenar amb les dades reals abans d'executar; no es poden substituir per la vista del llenç.

La màscara de l'experiment controlat no reutilitza el cribratge costaner anterior. Combina cota inferior a 20 m i pendent inferior a 2° com dos criteris docents fixats abans de comparar els suports; el valor de 20 m no representa una categoria física universal ni substitueix una justificació adaptada a una altra pregunta territorial.

::: table "Contracte executable de referència"
| Fase | Algorisme | Paràmetres que s'han de fixar |
| --- | --- | --- |
| Graelles d'elevació | `gdal:warpreproject`, executat directament sobre la mateixa font per a cada resolució | `TARGET_CRS`; `RESAMPLING = Average` si la font i la pregunta admeten suport mitjà; `NODATA`; `TARGET_EXTENT` numèrica comuna ja ajustada a una graella mare de 200 m; `TARGET_EXTENT_CRS`; `TARGET_RESOLUTION = 25` o `200`; tipus de sortida de coma flotant; comprovació posterior de l'origen i l'extensió exactes |
| Pendent | `gdal:slope` | `BAND = 1`; `SCALE = 1` quan les unitats horitzontals i verticals són metres; graus, no percentatge; mateixa fórmula; `COMPUTE_EDGES = False` per fer visible la vora incompleta |
| Orientació | `gdal:aspect` | `BAND = 1`; azimut des del nord; mateixa fórmula; `COMPUTE_EDGES = False`; classe plana derivada del llindar de pendent, no del codi d'orientació |
| Reclassificació | `native:reclassifybytable` | Banda, taula d'intervals, inclusió dels límits, valor per a rangs absents, `NoData` i tipus de sortida idèntics a les dues resolucions |
| Màscara de dos criteris | `native:rastercalc` | Capes explícites, expressió `("elevacio@1" < 20) AND ("pendent_graus@1" < 2)`, extensió, mida de cel·la, CRS, tractament de `NoData` i sortida persistent |
| Resum municipal | `native:zonalstatisticsfb` | `municipi_treball`, banda 1 i prefix per variable i resolució; recompte, mitjana, mínim i màxim per a elevació i pendent; suma, recompte i mitjana per a la màscara binària 0/1 |
:::

Les deu sortides ràster persistents s'escriuen a `sandbox/`, al costat de la parella `pr5-raster-cognom`, amb aquests noms fixos:

::: listing "Noms dels GeoTIFF persistents de la micropràctica 5"
```text
pr5_elevacio_25m.tif
pr5_elevacio_200m.tif
pr5_pendent_25m_graus.tif
pr5_pendent_200m_graus.tif
pr5_orientacio_25m_graus.tif
pr5_orientacio_200m_graus.tif
pr5_elevacio_classes_25m.tif
pr5_elevacio_classes_200m.tif
pr5_mascara_elevacio_pendent_25m.tif
pr5_mascara_elevacio_pendent_200m.tif
```
:::

Les sortides temporals o de diagnòstic reben altres noms i no poden substituir cap d'aquests GeoTIFF.

`native:zonalstatisticsfb` seguirà a cada resolució les dues passades descrites: prova de centres vàlids i, quan el primer recompte és zero o un, recàlcul complet amb fraccions d'intersecció. La taula ha d'admetre recomptes decimals i no pot comparar-los com si sempre fossin nombres enters de píxels. El percentatge de superfície vàlida només es calcularà si també s'obté un denominador amb una graella constant, vàlida i perfectament alineada, sotmesa al mateix algorisme sobre `municipi_treball`, i s'ha comprovat que numerador i denominador han seguit la mateixa regla de pertinença. Aleshores el recompte del MDE es dividirà pel recompte de la graella constant. Si les dues execucions activen passades diferents, cal calcular les àrees vàlida i total amb una única regla explícita d'intersecció; sense un denominador compatible s'informarà només el recompte vàlid retornat per l'eina.

La taula de resultats es prepararà abans de l'execució i deixarà les cel·les de valor buides. Per a cada resolució registrarà dimensions, nombre de cel·les vàlides, superfície ràster assignada al municipi, mínim, màxim i mitjana d'elevació, distribució del pendent, proporció de terreny pla, proporcions de classes i superfície de la màscara. El percentatge vàlid només s'hi afegirà amb el denominador anterior. També inclourà el temps i la mida de fitxer només com a mesures operatives de l'execució, no com a criteris de qualitat geogràfica.

No s'ha de pressuposar que totes les mitjanes canviaran poc ni que tots els màxims i pendents disminuiran. Aquestes són hipòtesis plausibles quan s'agrega una superfície, però poden fallar per la forma del territori, `NoData`, regles de vora o artefactes. El protocol obliga a observar primer els valors i després explicar-los. Una diferència inesperada començarà amb un diagnòstic de graella, validesa i paràmetres abans d'atribuir-se a l'escala geogràfica.

Les comparacions cel·la a cel·la necessiten un suport comú. Per a un control a 200 m, els valors de 25 m es poden agregar en blocs 8 × 8 i comparar amb la branca de 200 m creada directament; aquesta prova avalua coherència del procés. Per visualitzar desacord de classes a 25 m, la classe de 200 m es pot expandir amb veí més proper, deixant clar que cada bloc rep una etiqueta repetida i que no s'ha creat informació fina. La diferència no s'ha de calcular superposant graelles desalineades ni aplicant bilineal a codis.

L'efecte de vora es quantificarà separant una zona interior, situada almenys a la distància necessària del límit, i una franja fronterera. També es compararà la superfície vectorial amb la superfície assignada segons cada graella. Si gran part de la diferència es concentra a la franja, la interpretació parlarà de discretització del límit; si persisteix a l'interior, s'examinaran generalització, derivats i classificació. Aquesta separació impedeix atribuir a tot el relleu un problema generat només pel contorn municipal.

La conclusió de l'exercici tindrà tres parts: diferències observades amb unitats, mecanismes que les poden explicar i implicacions per a la pregunta territorial. No afirmarà que 25 m és «més exacte» sense una validació independent ni que 200 m és «incorrecte» perquè generalitza. Indicarà per a quines decisions el canvi és material, quines conclusions es mantenen i quines queden obertes per falta d'una referència de control.

## Formats de sortida i verificació final

Abans d'acceptar una sortida cal tornar-la a obrir i comprovar `CRS`, referència vertical documentada, dimensions, extensió, mida de píxel, origen, banda, tipus, `NoData`, mínim, màxim, quantils i nombre de cel·les vàlides. Després s'ha de contrastar una mostra amb la font, inspeccionar vores i costures i comparar superfícies o estadístiques amb valors plausibles. Els controls i les incidències s'incorporaran al diari; una captura només és necessària si prova una configuració o una anomalia que les taules no descriuen prou bé.

## Activitats

### Comprovació guiada: zero o absència

Cal descarregar el [MDT05 oficial del full 0473](https://centrodedescargas.cnig.es/CentroDescargas/detalleArchivo?sec=9072569), carregar-lo sense modificar-lo en un projecte amb `EPSG:25831` i comprovar a les propietats de la capa que té 5 m de mida de cel·la, una banda de coma flotant i `-32767` com a `NoData`. La simbologia s'ha de fixar entre `-6,1` i `173,5` m i ha de representar `NoData` transparent, tal com mostra la figura anterior.

Amb l'eina d'identificació s'han de consultar els dos centres de cel·la següents. Les coordenades pertanyen a `EPSG:25831`; per tant, abans de comparar-les cal assegurar que QGIS no les interpreta en el `CRS` d'una altra capa.

::: table "Dos valors de control al MDT05 del full 0473"
| Coordenada X (m) | Coordenada Y (m) | Resultat esperat | Interpretació |
| --- | --- | --- | --- |
| 355160 | 4550680 | 0 m | Cota vàlida que participa en els càlculs |
| 363360 | 4545635 | `NoData` | Absència exclosa dels càlculs, emmagatzemada amb el sentinella `-32767` |
:::

La comprovació acaba repetint una mitjana sobre una finestra que inclogui cel·les vàlides i absents: primer s'ha de mantenir `NoData` i després, només en una còpia temporal, substituir-lo per zero. Cal registrar el recompte vàlid i explicar per què la segona mitjana canvia sense que hagi aparegut cap cota nova al territori. Aquesta activitat és una prova de diagnòstic i no forma part de la micropràctica lliurable 5.

### Pràctica guiada: el relleu de Vila-seca a dues resolucions

La primera fase reprodueix la demostració amb els productes publicats. Cal identificar els recursos CNIG `9074092`, `9074093` i `9074255`, verificar-ne les sumes, registrar període, `CRS`, referència vertical, mida de cel·la, tipus, `NoData`, extensió i llicència, i conservar les fonts sense modificar. Els dos MDT25 formen el mosaic; el MDT25 i el MDT200 es retallen al municipi sobre les seves graelles natives. Les vistes mantenen el mateix àmbit, rang i escala, però la interpretació ha de declarar el desplaçament de 12,5 m i no pot atribuir totes les diferències només a la resolució.

Sobre el mosaic MDT25 es calculen pendent en graus i percentatge i orientació abans del retall. Després es reclassifiquen el llindar de 2 m i els sectors cardinals, i es construeix la màscara d'orientació sud amb pendent mínim de 2°. La comprovació inclou absència de piràmides, 34.734 cel·les vàlides, relació trigonomètrica entre les dues unitats de pendent i recomptes de les màscares. La superfície de proximitat, el buffer de 250 m i el resum zonal són diagnòstics de la demostració preparada: no afegeixen un onzè GeoTIFF ni cap altre resultat obligatori al contracte de la micropràctica 5.

La segona fase seguirà el protocol i el contracte executable de referència sense completar per endavant la taula de resultats. S'escollirà una única font oficial prou detallada, se'n documentarà la superfície representada i es crearà una regió d'interès amb marge. Les coordenades de l'extensió s'ajustaran abans del procés a una graella mare de 200 m.

A partir d'aquesta mateixa font, `gdal:warpreproject` generarà directament models de 25 m i 200 m amb l'extensió comuna i el mètode de remostreig justificat. L'origen, l'extensió i les dimensions resultants s'han de comprovar explícitament; no n'hi ha prou que el llenç sembli alineat. `gdal:slope`, `gdal:aspect`, `native:reclassifybytable` i `native:rastercalc` produiran respectivament pendent en graus, orientació, classes d'elevació i la màscara booleana, amb els paràmetres de la taula anterior. `native:zonalstatisticsfb` calcularà les estadístiques admeses sobre `municipi_treball`, no sobre la regió amb marge. Els mapes utilitzaran els mateixos intervals, colors, extensió i escala.

La validació inclourà la relació 8 × 8 entre graelles, dimensions esperades, valors vàlids, rangs, histogrames, superfície de les classes i comparació entre franja de vora i interior. Només després s'escriurà quins resultats són sensibles a la resolució. Si una diferència no es pot separar d'un canvi de remostreig, alineació o `NoData`, quedarà descrita com una limitació del disseny i no com un efecte demostrat de la mida de cel·la.

### Micropràctica 5: anàlisi ràster

Amb QGIS tancat, es fa la còpia inicial següent; la primera ruta és l'origen i la segona, la destinació:

::: listing "Origen i destinació de la còpia inicial de la micropràctica 5"
```text
dist/pr4-geoprocessament-cognom.gpkg
sandbox/pr5-raster-cognom.gpkg
```
:::

No es copia ni es reanomena el `.qgz` de `pr4`. Des de la còpia s'obre el projecte incrustat heretat, es desa com a `pr5` i s'elimina l'entrada `pr4`. Totes les fonts locals es reorienten al GeoPackage `pr5` i es comprova que no apuntin a `dist/`, al fitxer `pr4-geoprocessament-cognom.gpkg` ni a una ruta personal. Després d'incorporar els resultats validats es crea de nou, a `sandbox/`, el projecte `pr5-raster-cognom.qgz`, amb camins relatius al GeoPackage homònim i als GeoTIFF germans. Amb QGIS tancat, el conjunt complet es copia a `dist/` sense canviar-ne els noms i les dues representacions del projecte es proven des d'una ubicació neta.

::: table "Contracte de la micropràctica 5"
| Component | Requisit |
| --- | --- |
| Entrades | `dist/pr4-geoprocessament-cognom.gpkg`, que es copia a `sandbox/pr5-raster-cognom.gpkg`, amb `municipi_treball`; i subconjunt documentat d'un model d'elevacions oficial amb marge suficient |
| Operacions mínimes | No copiar el `.qgz` de `pr4`; establir un únic projecte incrustat `pr5`; reorientar les fonts locals; preparar dues resolucions niades amb `gdal:warpreproject`; calcular pendent i orientació amb `gdal:slope` i `gdal:aspect`; reclassificar amb `native:reclassifybytable`; combinar dues condicions amb `native:rastercalc`; i resumir amb `native:zonalstatisticsfb` |
| Resultats | Deu GeoTIFF continus i categòrics amb els noms fixats, com a fitxers germans de la parella `pr5-raster-cognom`; taula d'estadístiques persistent al GeoPackage; i mapa comparatiu incorporat a la instantània `pr5` |
| Evidències del diari | Font i procedència de l'elevació, `CRS`, referència vertical, resolució, alineació, `NoData`, remostreig, llindars, comportament del recompte zonal, controls i interpretació de les diferències |
| Comprovacions | Exactament un projecte incrustat `pr5`; cap URI local cap a `dist/` o `pr4`; camins relatius des del `.qgz` al GeoPackage i als GeoTIFF germans; dimensions esperades, relació de niament, rangs plausibles, recomptes zonals sense arrodonir, superfície ràster comparada amb la vectorial, efectes de vora, simbologia comuna i obertura equivalent de les dues representacions del projecte |
| Fitxers que cal conservar | `dist/pr5-raster-cognom.gpkg`, amb la taula comparativa i el projecte incrustat `pr5`; `dist/pr5-raster-cognom.qgz`; els deu GeoTIFF analítics amb els noms fixats; i diari amb els controls |
:::

Els llindars de Vila-seca no s'han de copiar automàticament a un municipi de muntanya. La transferència exigeix revisar la distribució, la mida dels processos, la qualitat de l'elevació i la finalitat de cada classe. El lliurament ha de diferenciar els valors observats dels esperats i conservar buides, fins a executar els càlculs, totes les caselles destinades als resultats de la comparació.
