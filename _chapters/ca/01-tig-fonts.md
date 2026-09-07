---
layout: manual-chapter
title: TIG, preguntes i fonts geogràfiques
description: Criteris per formular preguntes territorials, entendre un SIG i seleccionar fonts geogràfiques adequades.
lang: ca
ref: manual-tig-questions-sources
profiles: [unaltremanual]
content_status: draft
permalink: /ca/chapters/tig-preguntes-fonts/
weight: 20
part: Continguts
manual_references: true
---

Una tecnologia de la informació geogràfica només és útil quan ajuda a respondre una pregunta sobre el territori. Localitzar una carretera, delimitar una zona inundable, estudiar l'accés a un equipament o comparar el relleu de dos municipis exigeix relacionar **on passa un fenomen**, **què se'n coneix** i **amb quina qualitat s'ha observat**. Obrir una capa sense haver formulat aquesta relació pot produir un mapa, però no necessàriament una resposta.

Les **tecnologies de la informació geogràfica** (TIG) inclouen els mètodes i instruments que permeten obtenir, gestionar, analitzar i comunicar informació georeferenciada. Un **sistema d'informació geogràfica** (SIG) és una organització concreta de persones, dades, mètodes, programari i infraestructura orientada a una finalitat. QGIS és l'aplicació principal del curs, però no és tot el sistema: la pregunta, les fonts, les decisions i les comprovacions continuen existint fora del programa {% cite longleyGeographicInformationScience2015 nunesDiccionariSIG2012 %}.

>>>>> En acabar el capítol, cal poder convertir una necessitat territorial en una pregunta de dades i justificar quines fonts permeten respondre-la.
>>>>>
>>>>> - Delimitar fenomen, unitat d'observació, àmbit, període i mesura.
>>>>> - Explicar la funció de les persones, les dades, els mètodes, el programari i la infraestructura dins d'un SIG.
>>>>> - Distingir una descàrrega de dades d'un servei de visualització o consulta.
>>>>> - Avaluar autoria, data, escala o resolució, sistema de referència, llicència i limitacions d'una font.

Aquest punt de partida canvia l'ordre habitual de treball. No es tracta de trobar primer un mapa atractiu i decidir després què se'n pot extreure, sinó d'especificar quina evidència necessita la pregunta i buscar la representació que la pugui aportar. Una ortofoto pot mostrar que hi ha una construcció en una data determinada; una capa cadastral pot delimitar una parcel·la segons el producte publicat; una xarxa vectorial pot permetre calcular recorreguts. Que totes tres capes coincideixin visualment no les fa intercanviables.

La selecció d'una font és, per tant, una decisió analítica. Inclou el productor i el procés d'observació, però també el producte, la versió, la via d'accés i la resposta concreta que arriba a QGIS.

## De la necessitat a la pregunta geogràfica

Una necessitat inicial acostuma a ser massa oberta per orientar una anàlisi. «Millorar la mobilitat ciclista» no indica encara què cal observar. Es pot concretar preguntant quins trams de carril bici formen una xarxa connectada, quins equipaments queden a menys de cinc minuts d'aquesta xarxa o en quins carrers hi ha discontinuïtats. Cada formulació exigeix unitats, dades i operacions diferents.

Una pregunta geogràfica operativa ha d'acotar cinc components:

1. **Fenomen:** què s'observa o es vol explicar, com ara mobilitat, relleu, població o coberta del sòl.
2. **Unitat d'observació:** què representa cada registre o cel·la, com un fanal, un tram, una parcel·la, un municipi o un píxel.
3. **Àmbit:** on s'estudia el fenomen i quins límits s'accepten.
4. **Període:** a quin instant o interval corresponen les dades.
5. **Mesura:** quin recompte, distància, superfície, proporció, categoria o valor permetrà contrastar la pregunta.

La pregunta també ha d'anticipar què podria demostrar que la resposta inicial era incompleta. Si es busca sòl potencialment adequat per a una activitat, per exemple, la coincidència de tres criteris espacials només identifica àrees candidates segons aquells criteris. No demostra que la resta de condicionants socials, jurídics, ambientals o econòmics s'hagin satisfet.

>>> **Exemple de formulació.** La pregunta «On falten fanals?» no defineix una unitat ni un criteri. Una versió analitzable podria ser: «Quins trams de la xarxa de carrers del nucli de Vila-seca queden a més de 30 m d'un fanal inventariat durant la campanya de camp?». Ara es poden identificar les capes, la distància, l'àmbit i la data, tot i que el llindar encara s'ha de justificar.

La formulació permet derivar una **especificació de dades**. Per al cas dels fanals caldria una observació puntual amb identificador i data, una xarxa de carrers amb trams connectats, una delimitació del nucli i un sistema de referència de coordenades (CRS) adequat per interpretar la distància. També caldria saber si «quedar a més de 30 m» es mesura en línia recta, al llarg de la xarxa o respecte de la superfície il·luminada. La mateixa frase que orienta la cerca revela, doncs, decisions metodològiques encara pendents.

Una font candidata s'ha de poder descartar. Si el recurs només retorna una imatge amb els carrers dibuixats, pot servir per orientar-se, però no aporta necessàriament els eixos vectorials sobre els quals calcular distàncies de xarxa. Si l'inventari de fanals no declara la data o només cobreix una part del nucli, el resultat descriurà la cobertura de l'inventari i no tots els fanals existents. Definir abans aquests criteris evita confondre disponibilitat amb adequació.

La unitat d'observació mereix una comprovació específica perquè sovint queda amagada darrere del nom de la capa. Una capa anomenada «carreteres» pot contenir eixos, trams entre interseccions, calçades separades, plataformes o enllaços; una capa «edificis» pot representar petjades, construccions cadastrals o punts d'adreça. Abans de buscar una operació de QGIS cal poder completar la frase «cada entitat representa...». Si la resposta no es troba a les metadades o a l'esquema, la font encara no està prou entesa.

## Els components d'un SIG

La informació georeferenciada combina un **component espacial**, que descriu posició, forma i relacions, amb un **component temàtic**, que descriu identitat, categoria o valor. Un SIG coordina aquests components mitjançant cinc peces interdependents.

::: table "Components d'un SIG i preguntes de control"
| Component | Funció dins del projecte | Pregunta de control |
| --- | --- | --- |
| Persones | Formulen la pregunta, produeixen o validen dades i interpreten els resultats | Qui respon de cada decisió i qui utilitzarà el resultat? |
| Dades | Representen geometries, atributs, temps i metadades | Són adequades per al fenomen, el període i l'escala? |
| Mètodes | Defineixen com es captura, transforma, analitza i comprova la informació | Per què l'operació respon la pregunta? |
| Programari | Executa operacions i conserva part de l'estat del treball | Què registra QGIS i què s'ha de documentar fora del projecte? |
| Infraestructura | Proporciona equips, emmagatzematge, xarxa i còpies de seguretat | On són les dades i com es podran recuperar? |
:::

Cap peça no compensa completament l'absència d'una altra. Un algorisme correcte aplicat a una font inadequada produeix un resultat enganyós; unes dades precises sense un criteri d'anàlisi no responen cap pregunta; i un projecte que només s'obre a l'ordinador on es va crear no és una evidència transferible.

## Fonts, productes i vies d'accés

Una **font** identifica qui produeix o manté la informació i amb quin procediment. Un **producte** és un conjunt de dades concret, amb una versió, una cobertura i unes especificacions. Una **capa** és una unitat que una aplicació pot obrir o consultar. Finalment, una URL, un connector o un servei web només són vies d'accés. Barrejar aquests nivells dificulta atribuir les dades i saber què ha canviat quan una connexió deixa de funcionar.

També convé separar el **portal de descoberta** del recurs utilitzat. Un catàleg permet cercar productes i llegir-ne fitxes; un visor permet explorar una zona; una pàgina de documentació publica l'adreça d'un servei; i un fitxer o una resposta web aporta les dades efectives. El nom del portal no substitueix el títol del producte ni la capa concreta. En un inventari de fonts, «ICGC» o «CNIG» és massa genèric si no s'hi afegeixen el producte, l'edició i la via d'accés.

En el curs s'utilitzaran sobretot fonts institucionals. El [Centro Nacional de Información Geográfica](https://centrodedescargas.cnig.es/) distribueix cartografia estatal; l'[Institut Cartogràfic i Geològic de Catalunya](https://www.icgc.cat/) publica cartografia, ortofotos i models d'elevacions; el [Cadastre](https://www.sedecatastro.gob.es/) ofereix informació cadastral amb condicions pròpies; i el portal de [dades obertes de la Generalitat](https://dadesobertes.gencat.cat/) reuneix registres administratius i altres conjunts temàtics. Que una font sigui oficial no evita haver de llegir-ne les metadades ni comprovar que respon la pregunta.

Les dades es poden obtenir per descàrrega, una interfície de consulta, una API o un servei geoespacial. Els serveis de l'Open Geospatial Consortium permeten reconèixer funcions diferents:

::: table "Diferències entre vies habituals d'accés geogràfic"
| Via | Què proporciona | Ús adequat | Limitació que cal controlar |
| --- | --- | --- | --- |
| Descàrrega | Una còpia local d'un producte | Anàlisi repetible, edició i treball sense connexió | La còpia queda vinculada a una versió i s'ha d'actualitzar explícitament |
| WMS | Una imatge cartogràfica generada pel servidor | Context i inspecció visual | No proporciona necessàriament les geometries ni els valors originals {% cite ogcWMS2006 %} |
| WMTS | Tessel·les preparades per nivells d'escala | Mapa base amb resposta ràpida | Escales, estils i sistemes de referència estan predefinits {% cite ogcWMTS2010 %} |
| WFS | Entitats vectorials i atributs | Consulta o obtenció de dades vectorials | Pot aplicar límits, paginació, generalització o restriccions d'edició {% cite ogcWFS2014 %} |
| XYZ | Tessel·les d'un mapa web | Context visual | No és necessàriament un servei OGC ni una font apta per a anàlisi |
| API | Respostes estructurades segons una consulta | Automatització i selecció de registres | Cal entendre paràmetres, límits, versions i esquema de resposta {% cite ogcAPIFeatures2022 %} |
:::

Un connector de QGIS, com els d'ICGC, Cadastre o QuickMapServices, pot simplificar la connexió. El connector no substitueix el productor, la llicència ni les especificacions del producte. Tampoc no converteix una imatge de mapa en dades analítiques.

Les captures històriques següents, procedents de material docent anterior, mostren dues formes d'accés mediat per connectors en una configuració anterior de QGIS 3.x. Són només orientatives: la interfície i les entrades dels catàlegs poden haver canviat, i cal comprovar les metadades vigents de la font, la llicència i el servei.

![Panell del connector QuickMapServices obert en una configuració anterior de QGIS 3.x]({{ site.baseurl }}/assets/img/qgis/qgis-qms-panel.png "En una configuració anterior de QGIS 3.x, el panell de QuickMapServices mediava la cerca de serveis; les entrades del catàleg podien canviar i no substituïen la comprovació de la font, la llicència i el servei vigents."){: data-figure-width-web="48rem" data-figure-width-pdf="100%"}

![Barra d'eines d'un connector de l'ICGC en una configuració anterior de QGIS 3.x]({{ site.baseurl }}/assets/img/qgis/qgis-icgc-bar.png "En una configuració anterior de QGIS 3.x, una barra de connector abreujava l'accés a recursos de l'ICGC; la interfície podia canviar i cal verificar la font, la llicència i les metadades del servei vigents."){: data-figure-width-web="38rem" data-figure-width-pdf="90%"}

La diferència entre una descàrrega i un accés remot afecta la reproducció. Una descàrrega crea una còpia local que pot conservar-se amb el projecte, sempre que la llicència n'autoritzi l'ús i la redistribució prevista. La còpia no s'actualitza sola, però permet repetir una anàlisi sobre la mateixa entrada. Un servei o una API consulta l'estat que el servidor ofereix en aquell moment. Pot evitar transferir un producte complet i pot reflectir revisions del productor, però la mateixa consulta repetida més endavant no té per què retornar exactament el mateix contingut.

Una **interfície de programació d'aplicacions** (API) defineix com un programa demana recursos o operacions a un altre. Un servei geoespacial pot estar definit per un estàndard de l'Open Geospatial Consortium (OGC), per una API pròpia o per una especificació OGC més recent orientada al web. «API» i «servei» no designen, per si sols, el model de dades retornat. Cal llegir el contracte: una resposta pot ser una imatge, objectes vectorials, una cobertura ràster, metadades o només un missatge d'error.

L'elecció no sempre és exclusiva. Durant la descoberta pot ser eficient explorar un WMS o un WMTS, i després obtenir una descàrrega vectorial per a l'anàlisi. També es pot consultar un WFS sobre una àrea petita, exportar la selecció autoritzada a una capa local i registrar la consulta. La via remota resol l'accés; la còpia local fixa l'entrada del procediment. Totes dues continuen referint-se a un producte i una llicència que s'han d'identificar.

## Com avaluar una font

La qualitat no és una propietat absoluta: una mateixa dada pot ser adequada per a un mapa regional i insuficient per digitalitzar una vorera. L'avaluació ha de relacionar les característiques del producte amb l'ús previst. Com a mínim, cal registrar:

::: table "Fitxa mínima d'una font geogràfica"
| Camp | Què cal identificar |
| --- | --- |
| Productor i producte | Organisme responsable, nom complet i identificador de la capa o conjunt |
| Versió i dates | Data de les dades, edició o actualització i data d'accés |
| Cobertura | Extensió territorial i període representat |
| Escala o resolució | Nivell de detall justificable i unitat mínima observable |
| Model i format | Vector, ràster o taula; format i estructura dels fitxers |
| Sistema de referència | CRS declarat, unitats i àrea d'ús |
| Esquema | Significat, tipus, unitat i domini dels camps o bandes |
| Qualitat | Exactitud, completesa, coherència i limitacions documentades |
| Llicència | Condicions de reutilització i atribució requerida |
| Accés | URL estable, servei, consulta o nom del paquet conservat |
:::

La inspecció ha d'arribar fins a les dades reals. Abans d'utilitzar un camp cal comprovar-ne el nom, el tipus, el domini i els valors absents. Un codi territorial pot semblar un nombre, però s'ha de conservar com a text si els zeros inicials són significatius. Una data de publicació tampoc no és necessàriament la data del fenomen observat.

### Metadades que permeten decidir

Les **metadades** descriuen una dada, un conjunt o un servei. Poden aparèixer en una fitxa del catàleg, un document d'especificacions, un registre normalitzat, un fitxer auxiliar o les propietats que QGIS llegeix de la font. Aquestes peces no sempre coincideixen. La propietat d'una capa pot declarar un CRS i una extensió, mentre que la fitxa del producte explica el mètode de captura, la data, la freqüència d'actualització i l'exactitud. Una inspecció completa relaciona totes dues escales.

El primer bloc de metadades identifica responsabilitat i significat. Cal saber qui produeix les observacions, qui les distribueix, quin títol i identificador té el producte i què representa cada entitat, cel·la o camp. Un distribuïdor pot no ser el productor original. Igualment, una capa derivada pot conservar la marca d'un organisme sense explicar quina simplificació, agregació o conversió ha aplicat un tercer. Quan la cadena no es pot reconstruir, la font només és adequada per a usos que tolerin aquesta incertesa.

El segon bloc situa les dades en l'espai i el temps. La cobertura geogràfica indica on hi ha dades, però no necessàriament on són completes. La data de captura, la data de referència, l'edició i la data de publicació responen preguntes diferents. Una ortofoto pot haver estat publicada aquest any i provenir d'un vol anterior; una divisió administrativa pot tenir una data de vigència diferent de la geometria amb què es distribueix. Per comparar capes cal identificar la data del fenomen, no només la del fitxer.

El tercer bloc descriu la representació i la qualitat. En vector interessa el tipus de geometria, la unitat mínima cartografiada, el criteri de generalització, la completesa, la coherència topològica i l'exactitud posicional i temàtica declarades. En ràster cal afegir mida de cel·la, bandes, tipus de valor, `NoData`, nivell de processament i, quan correspongui, resolució radiomètrica o temporal. El capítol següent sobre models i formats desenvoluparà aquestes estructures; en aquesta fase importa comprovar que les propietats necessàries existeixen i s'ajusten a la pregunta.

Les metadades no converteixen automàticament una font en adequada. Són evidència per prendre una decisió i també poden revelar un límit. Si un producte declara una escala de producció incompatible amb el detall demanat, no s'ha de compensar ampliant el zoom. Si no informa de la data o del criteri de cobertura, aquesta absència s'ha de registrar i pot obligar a cercar una altra font. «Sense informació» no és equivalent a «sense error».

### Qualitat relativa a l'ús

L'avaluació es pot formular com una correspondència entre requisit i evidència. Si la pregunta exigeix distingir voreres, cal una unitat espacial i una exactitud compatibles amb aquest objecte. Si exigeix comparar dos anys, calen dates de referència i mètodes prou consistents. Si exigeix unir estadístiques municipals, la geometria ha de conservar el codi territorial correcte per al mateix marc administratiu. Cada requisit ha de tenir una propietat observable o una limitació explícita.

La inspecció visual és necessària però insuficient. Una capa pot superposar-se bé a una ortofoto i contenir identificadors duplicats; un ràster pot semblar continu i tenir valors `NoData` codificats com a zero; un WMS pot mostrar parcel·les nítides sense proporcionar-ne cap geometria. Els controls han de combinar metadades, esquema, recompte, rangs, valors absents, extensió i contrast espacial. Encara no cal executar tota l'anàlisi, però sí descartar una entrada que no pugui superar aquests controls inicials.

Quan dues fonts discrepen, no s'ha de triar automàticament la que sembla més detallada. Cal comprovar si representen el mateix fenomen, data i definició. Un eix viari no ha de coincidir exactament amb el centre visible de totes les calçades; un límit administratiu i una tanca física poden respondre realitats diferents; una petjada cadastral i una coberta observada en ortofoto poden tenir dates i finalitats distintes. La discrepància pot ser un error, però també informació sobre els models comparats.

### Accés, llicència i responsabilitat

Poder obrir una capa no implica poder reutilitzar-la. La **llicència** estableix permisos i obligacions sobre el contingut: atribució, redistribució, transformació, ús comercial o compartició d'una base derivada, segons el cas. Les condicions del portal o de l'API poden regular, a més, l'accés tècnic, la freqüència de peticions, les credencials i el comportament del client. Cal llegir la llicència del producte i no inferir-la del fet que la consulta sigui gratuïta.

En un mapa compost poden coexistir règims diferents. La geometria analítica pot tenir una llicència oberta, el servei de fons unes condicions específiques i el text o la composició una autoria pròpia. L'atribució ha d'identificar cada aportació amb la forma exigida pel productor. Si una llicència no permet redistribuir el fitxer original, el projecte pot documentar com obtenir-lo sense incorporar-lo al paquet de lliurament. La reproducció tècnica no anul·la els drets ni les restriccions de dades personals.

La paraula «obert» tampoc no resol tots els dubtes. Cal saber quina versió de la llicència s'aplica, a quin recurs i quina atribució demana. Les llicències de programari, de bases de dades, de documents i d'imatges regulen objectes diferents. Per això no s'han de traslladar automàticament les condicions de QGIS a les dades obertes amb el programa, ni les d'un portal institucional a tots els conjunts que enllaça.

La fitxa mínima de la font ha de conservar la redacció o l'enllaç vigent de les condicions en la data d'accés. No cal copiar tot el text legal al diari, però sí registrar la llicència identificada, l'atribució prevista i qualsevol restricció que afecti el projecte. Quan les condicions no són clares, la decisió prudent és no redistribuir ni afirmar un permís que no s'ha pogut verificar.

## Com funciona un servei geogràfic

Un servei web distribueix la feina entre un **client** i un **servidor**. QGIS és el client: prepara una petició amb una operació, una capa, una extensió, un CRS i altres paràmetres. El servidor valida la petició, consulta les dades que manté, pot filtrar-les o representar-les i retorna una resposta. Entre tots dos hi pot haver passarel·les d'autenticació, balancejadors i memòries cau. El client no necessita conèixer la base de dades interna, però sí el contracte públic del servei.

Aquesta arquitectura explica per què una URL no és «la capa». L'adreça base identifica un punt d'accés; els paràmetres indiquen què es demana; i la resposta és un resultat concret. Si canvien la capa, l'extensió, el nivell d'escala, el format o la data de consulta, canvia l'objecte rebut. Si el productor actualitza les dades del servidor, una petició idèntica també pot retornar contingut diferent.

El flux separa qui formula la consulta, qui l'executa i quin tipus de resposta torna al client.

![Flux entre un client SIG, un servidor geogràfic i les dades publicades]({{ site.baseurl }}/assets/diagrams/ca/01-tig-fonts/ogc-client-server.mmd "QGIS envia una petició HTTP segons el contracte del servei; el servidor consulta les dades publicades i retorna una representació diferent segons si s'utilitza WMS, WMTS o WFS."){: data-figure-width-web="30rem" data-figure-width-pdf="70%"}

Els estàndards oberts permeten que clients i servidors de fabricants diferents comparteixin aquesta gramàtica. No obliguen el productor a oferir totes les operacions, no concedeixen una llicència i no asseguren disponibilitat permanent. Un servei conforme pot limitar el volum, restringir l'edició, publicar només una vista generalitzada o exigir autenticació. La interoperabilitat tècnica és una condició útil, no una certificació de qualitat temàtica.

### La petició GetCapabilities

En WMS, WMTS i WFS, l'operació `GetCapabilities` demana al servei que descrigui què ofereix. La resposta acostuma a ser un document XML llegible per màquina. QGIS el consulta quan es prem **Connecta** i construeix la llista de capes, formats i opcions. També es pot obrir al navegador per diagnosticar una connexió; per exemple, el document del servei PNOA es demana amb `SERVICE=WMS&REQUEST=GetCapabilities` a l'adreça publicada per l'IGN.

El document de capacitats informa, segons el tipus i la versió del servei, del títol i el responsable, les operacions disponibles, els formats de resposta, les capes o tipus d'entitat, els CRS admesos, les extensions, els estils, les matrius de tessel·les i algunes restriccions. En WFS, `DescribeFeatureType` pot descriure després l'esquema dels objectes. En WMTS, les matrius indiquen quines quadrícules i nivells es poden sol·licitar. Aquestes respostes són la font tècnica per saber què entén el servidor, no una llista que s'hagi d'endevinar a partir del visor.

`GetCapabilities` també té límits. Pot descriure una capa amb un títol poc informatiu, remetre a metadades externes o no concretar prou la llicència i la qualitat. Que una capa aparegui al document no demostra que estigui completa ni que respongui amb rapidesa. Per això la lectura tècnica s'ha de relacionar amb la fitxa institucional del producte i amb una prova real de consulta.

Quan una connexió falla, el document ajuda a separar causes. Si no s'obté cap resposta, pot haver-hi un problema d'adreça, xarxa, certificat o servidor. Si el document arriba però la capa no hi figura, el nom o la versió poden haver canviat. Si la capa hi figura i `GetMap` o `GetFeature` falla, cal revisar CRS, extensió, format, límits o autenticació. Aquesta seqüència és més informativa que reinstal·lar un connector o repetir clics.

### WMS: una representació renderitzada

El [Web Map Service (WMS)](https://www.ogc.org/standards/wms/) està orientat a obtenir imatges de mapes georeferenciades. L'operació `GetMap` indica, entre altres peces, la capa, l'estil, el CRS, el rectangle geogràfic (`BBOX`), l'amplada, l'alçada i el format, com PNG o JPEG. El servidor selecciona les dades necessàries, aplica la simbolització i genera els píxels que el client col·loca al llenç.

El recorregut deixa clar que la simbolització i la renderització es resolen al servidor abans que la resposta arribi al client.

![Recorregut d'una petició GetMap des del client SIG fins a la imatge retornada pel servidor WMS]({{ site.baseurl }}/assets/diagrams/ca/01-tig-fonts/wms-request-response.mmd "Una petició GetMap combina capa, estil, CRS, extensió, mida i format; el servidor aplica aquests paràmetres i retorna una imatge renderitzada, no les geometries font."){: data-figure-width-web="31rem" data-figure-width-pdf="73%"}

La resposta conserva una relació espacial amb l'extensió demanada, però no lliura necessàriament les geometries ni la taula que hi ha darrere. No es poden seleccionar les parcel·les d'un PNG, canviar-ne els camps o executar-hi una intersecció vectorial. Alguns WMS ofereixen `GetFeatureInfo`, que retorna informació sobre la posició o el píxel consultat. Aquesta operació és útil per identificar allò que el productor exposa, però no transforma la imatge en una capa vectorial completa.

El WMS és adequat per donar context, comparar visualment una capa pròpia amb una cartografia oficial o consultar una representació temàtica controlada pel productor. També permet demanar imatges transparents i superposar-les. No és la via correcta si la pregunta exigeix editar geometries, recalcular una classificació a partir dels atributs o conservar els valors originals d'un sensor. En aquests casos cal localitzar una descàrrega, un servei d'objectes o una cobertura adequada.

### WMTS: tessel·les i nivells definits

El [Web Map Tile Service (WMTS)](https://www.ogc.org/standards/wmts/) distribueix imatges segons una o més matrius de tessel·les. En lloc de generar una imatge amb qualsevol amplada, alçada i extensió, el client demana una tessel·la identificada per la matriu, la fila i la columna d'un nivell. Els límits, les resolucions i els CRS disponibles queden declarats al document de capacitats.

La jerarquia del conjunt de matrius, el nivell, la fila i la columna determina quina tessel·la concreta es recupera.

![Relació entre el conjunt de matrius WMTS, els nivells i l'adreça d'una tessel·la]({{ site.baseurl }}/assets/diagrams/ca/01-tig-fonts/wmts-tile-matrix.mmd "GetCapabilities declara el CRS i les matrius disponibles; GetTile identifica una cel·la mitjançant el conjunt, el nivell, la fila i la columna i en retorna la tessel·la d'imatge."){: data-figure-width-web="46rem" data-figure-width-pdf="95%"}

Aquesta regularitat permet reutilitzar tessel·les entre usuaris i peticions. Molts serveis les preparen anticipadament o les generen quan es demanen i les guarden en memòria cau. El resultat acostuma a ser més àgil per navegar per un mapa base, però no hi ha una garantia universal de velocitat: la xarxa, el servidor, la cobertura de la memòria cau i el nombre de capes continuen intervenint.

El cost d'aquesta estratègia és que el client s'ha d'ajustar als nivells disponibles. Entre dos nivells, QGIS pot reescalar una tessel·la, però no apareix informació nova. El mapa també arriba renderitzat; encara que els contorns siguin molt nítids, no són objectes seleccionables. Un WMTS és, per tant, una bona base visual quan la seva cartografia, data, escala i llicència són adequades, però no una substitució d'una capa vectorial d'anàlisi.

### WFS: objectes i atributs

El [Web Feature Service (WFS)](https://www.ogc.org/standards/wfs/) està orientat a consultar objectes geogràfics. `GetFeature` pot retornar geometries i atributs filtrats per tipus d'entitat, extensió o condició, en un format admès pel servidor. QGIS els interpreta com a entitats vectorials: es pot obrir la taula, seleccionar objectes i, si el proveïdor i el flux ho permeten, utilitzar-los en operacions d'anàlisi.

Accedir a objectes no significa rebre sempre la base mestra completa. El servei pot publicar una vista, ometre camps, simplificar geometries, limitar el nombre de resultats o paginar-los. Una consulta sense filtre sobre una capa extensa pot ser lenta o superar un límit del servidor. Abans d'utilitzar-la cal inspeccionar les capacitats, l'esquema, la quantitat efectivament recuperada i els missatges de QGIS.

Alguns WFS anuncien operacions transaccionals, conegudes com WFS-T, que permeten proposar insercions, canvis o supressions. Aquesta capacitat és opcional i sol requerir permisos. Carregar una capa WFS no autoritza a editar la font institucional, i una interfície editable no demostra que el servidor accepti transaccions. En el curs, el WFS s'utilitzarà principalment per consultar o obtenir dades; qualsevol edició es farà sobre còpies de treball autoritzades.

L'esquema separa la consulta d'entitats de les operacions transaccionals opcionals i subjectes a permisos.

![Accés WFS a geometries i atributs mitjançant GetFeature i operacions transaccionals opcionals]({{ site.baseurl }}/assets/diagrams/ca/01-tig-fonts/wfs-feature-access.mmd "GetFeature retorna geometries i atributs segons el tipus d'entitat, el filtre i el format demanats; les operacions WFS-T són una capacitat separada que requereix permisos."){: data-figure-width-web="46rem" data-figure-width-pdf="95%"}

### Dades vectorials o mapa dibuixat

La prova més directa consisteix a preguntar què arriba al client. En una resposta renderitzada arriben píxels amb colors decidits pel servidor. Es pot observar una línia, però no recuperar-ne necessàriament els vèrtexs ni el camp que n'ha determinat el color. En una resposta vectorial arriben objectes amb geometria i propietats. QGIS pot representar-los de nou, filtrar-los i analitzar-los, dins dels límits de l'esquema rebut.

La funció **Identifica** no elimina aquesta distinció. Sobre un vector consulta l'entitat i els seus camps. Sobre un WMS pot formular una petició `GetFeatureInfo` i mostrar text retornat pel servidor. Sobre un WMTS o un XYZ pot no obtenir cap registre. El fet que aparegui una finestra amb informació no prova que hi hagi una geometria vectorial disponible per al geoprocessament.

## Escala, resolució i disponibilitat

Un servei permet canviar de zoom amb facilitat, però el zoom no modifica la qualitat de la font. L'**escala cartogràfica** relaciona la representació amb el territori; la **resolució espacial** descriu la unitat de mostreig o de sortida; i la **generalització** selecciona, simplifica, agrega o desplaça elements per fer-los llegibles o adequats a una escala. Aquestes propietats estan relacionades, però no són sinònimes.

En un WMS, `WIDTH`, `HEIGHT` i `BBOX` determinen la mida dels píxels de la imatge retornada. Demanar més píxels no augmenta l'exactitud ni recupera detalls que la dada font o l'estil han omès. El servidor també pot aplicar visibilitat dependent de l'escala: una carretera local o una etiqueta pot aparèixer només en determinats intervals. Una absència a escala regional no demostra que l'objecte no existeixi al producte.

En un WMTS, cada nivell de la matriu té una resolució definida. QGIS pot mostrar el mapa a una escala intermèdia, però ho fa ampliant o reduint les tessel·les disponibles. En un WFS o una descàrrega vectorial, la geometria pot provenir d'una generalització prèvia encara que es pugui ampliar indefinidament. El nombre de vèrtexs visible no és una mesura suficient d'exactitud; cal recuperar l'escala o les especificacions de producció.

Una prova de font ha d'observar almenys tres escales relacionades amb l'ús: una vista de context, l'escala prevista d'anàlisi i una ampliació de diagnòstic. La vista de context comprova cobertura i posició general. L'escala de treball mostra si els objectes necessaris són distingibles. L'ampliació revela pixelació o simplificació, però no autoritza a treballar a aquell detall. El diari ha de registrar a quina escala la font deixa de sostenir la lectura requerida.

La disponibilitat forma part de la qualitat operativa. Un servei remot depèn del servidor, la xarxa, els certificats, les credencials, els límits de petició i les decisions futures del productor. No s'ha d'afirmar que un servei està «sempre actualitzat» o disponible en temps real si la documentació no defineix l'actualització ni un compromís de servei. Una capa visible avui pot canviar de nom, estil, contingut o adreça.

Les memòries cau redueixen transferències i temps de resposta, però introdueixen un altre estat. El servidor pot conservar tessel·les generades amb una versió anterior i el client pot mostrar una resposta local quan la xarxa ja no està disponible. Veure una capa després de desconnectar-se no demostra que el servei funcioni, i buidar la memòria cau no corregeix una font obsoleta. Per diagnosticar cal distingir la còpia del client, la memòria cau del servidor i la dada publicada.

Quan l'anàlisi ha de ser repetible, convé fixar una entrada local autoritzada o conservar una petició prou precisa juntament amb la data i les propietats de la resposta. Si només existeix un servei de visualització, cal declarar que el context depèn del servidor i que no constitueix una entrada analítica. Per al treball sense connexió, una prova prèvia ha de confirmar quines capes continuen disponibles i quines quedaran absents.

## Fluxos amb CNIG, ICGC i Cadastre

Els tres organismes ofereixen recursos diferents i, en alguns casos, vies múltiples per arribar-hi. El procediment no consisteix a instal·lar tres connectors, sinó a entrar per la pàgina oficial, identificar el producte i decidir si cal una descàrrega, una consulta d'objectes o una representació. Les interfícies canvien; la seqüència de preguntes es manté.

### CNIG i IGN

El [Centro de Descargas del CNIG](https://centrodedescargas.cnig.es/) organitza l'accés per productes cartogràfics i àmbits. Abans de descarregar cal obrir la fitxa del producte i identificar el contingut, l'escala o resolució, la data o edició, els formats, el CRS, la llicència i la unitat de distribució. Després es selecciona l'àrea necessària, que pot correspondre a un full, un municipi, una província o una altra divisió segons el producte. El paquet rebut i la fitxa no s'han de separar: el nom del `.zip` rarament explica tot el que conté.

L'IGN i el CNIG també publiquen serveis de visualització i descàrrega. El PNOA, per exemple, es pot explorar mitjançant un WMS; el seu [document `GetCapabilities`](https://www.ign.es/wms-inspire/pnoa-ma?SERVICE=WMS&REQUEST=GetCapabilities) permet comprovar les capes, els CRS i els formats que el servidor anuncia en el moment de la consulta. La imatge és adequada per revisar visualment l'entorn i la data s'ha de recuperar de les metadades de la capa o campanya. Si la pregunta exigeix valors ràster, bandes o treball fora de línia, cal cercar el producte descarregable corresponent en lloc d'exportar una captura del WMS.

El control després d'una descàrrega inclou conservar el paquet original, llegir qualsevol document o fitxer de metadades, descomprimir en una ubicació separada i inventariar les capes. A QGIS s'han de revisar extensió, CRS, geometria o dimensions, camps o bandes i correspondència amb la unitat anunciada. No s'ha de triar el primer fitxer que s'obre si el paquet conté versions, fulls o nivells de detall diferents.

### ICGC

La secció de [Geoinformació i mapes de l'ICGC](https://www.icgc.cat/ca/Geoinformacio-i-mapes) diferencia dades i productes, geoinformació en línia, mapes i eines. El [visor de descàrregues](https://visors.icgc.cat/appdownloads/) permet localitzar productes per àrea, mentre que la pàgina de [geoserveis](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Geoinformacio-en-linia-Geoserveis) publica opcions de mapes base, ortoimatges i altres temes. La ruta correcta depèn de si cal conservar geometries i valors o només un context cartogràfic.

Per obtenir una divisió administrativa destinada a unions o geoprocessament, cal seleccionar una descàrrega vectorial amb els codis i el nivell de detall necessaris. Per orientar el llenç o contrastar una capa, un servei de mapa base o d'ortofoto pot ser suficient. Si el producte ofereix diverses escales, no s'ha de carregar la més detallada per inèrcia: una base municipal general pot beneficiar-se d'una geometria generalitzada, mentre que una comprovació local pot exigir una versió de més detall.

### Cadastre

La Direcció General del Cadastre publica un [punt d'accés als conjunts i serveis INSPIRE](https://www.catastro.hacienda.gob.es/webinspire/index.html) que diferencia parcel·les cadastrals, adreces i edificis, i ofereix metadades, visualització WMS i vies de descàrrega. Aquesta separació és especialment útil: el WMS permet veure la cartografia; el WFS permet consultar objectes dins dels límits anunciats; i les descàrregues predefinides permeten obtenir conjunts per àmbits quan aquesta és la via adequada.

La cartografia cadastral té una finalitat administrativa i fiscal concreta. No s'ha de presentar automàticament com a Registre de la Propietat, aixecament topogràfic de límits jurídics o planejament urbanístic. Una parcel·la visible pot ser molt útil com a unitat geomètrica de consulta, però qualsevol conclusió sobre titularitat, dret edificatori, propietat o delimitació legal exigeix les fonts i els procediments competents.

Per explorar una zona petita, es pot afegir el WMS oficial i comprovar si la representació ajuda a situar les parcel·les. Si cal seleccionar-les o relacionar-ne atributs, s'ha d'utilitzar el WFS o una descàrrega autoritzada, no digitalitzar els contorns de la imatge. Per treballar amb tot un municipi de manera repetible, una descàrrega predefinida pot ser preferible a una consulta remota extensa. En tots els casos cal registrar l'àmbit institucional del servei, la data d'accés, les metadades i la llicència publicada.

## Incorporació inicial a QGIS

Carregar una font a QGIS és una primera inspecció, no una validació completa. Cal revisar l'extensió, el nombre d'entitats o les dimensions del ràster, el CRS declarat, els camps o bandes, els valors absents i la coherència visual amb una capa de referència. Si una capa apareix en un lloc inesperat, no s'ha d'assignar un CRS a l'atzar per fer-la coincidir: primer cal esbrinar què signifiquen les coordenades originals.

Les connexions remotes són útils per explorar. Quan una activitat requereix transformar dades o conservar exactament l'entrada, convé descarregar una còpia autoritzada i registrar-ne la versió. Les dades originals del projecte es mantindran sense modificacions; les seleccions, conversions i retalls es desaran com a dades preparades o derivades.

La connexió directa evita dependre d'un complement i fa visible quin tipus de servei s'està utilitzant. A QGIS 3.44 en català, el recorregut general es pot fer des de `Capa > Afegeix una capa` o des del `Gestor de fonts de dades`; el panell `Explorador` ofereix les mateixes famílies de connexió. La disposició pot variar segons el perfil, però la diferència entre `WMS/WMTS` i `WFS / OGC API - Features` s'ha de mantenir {% cite qgisUserGuide344 %}.

La disposició del panell permet identificar aquestes famílies abans de crear cap connexió.

![Captura en castellà del panell de fonts web de QGIS, amb WMS/WMTS i un grup ampli de connexions directes ressaltats]({{ site.baseurl }}/assets/img/qgis/qgis-web-services.png "El requadre superior assenyala WMS/WMTS. El requadre inferior inclou Vector Tiles, XYZ Tiles, WCS i WFS / OGC API - Features; d'aquest grup, la fila WFS és la que dona accés a entitats vectorials."){: data-figure-width-web="18rem" data-figure-width-pdf="45%"}

Per a un WMS o WMTS, el flux de connexió és el següent:

1. Localitzar a la pàgina oficial l'adreça del servei i la fitxa del producte; no s'ha de copiar una URL d'un projecte aliè sense saber-ne el productor.
2. Obrir la font `WMS/WMTS`, crear una connexió i donar-li un nom que identifiqui organisme, producte i funció, com `ign_pnoa_context` o `icgc_ortofoto_context`.
3. Introduir l'adreça base publicada. Les opcions d'autenticació només s'han de configurar si el servei les exigeix, i les credencials no s'han d'escriure al diari ni al nom de la connexió.
4. Prémer **Connecta** perquè QGIS llegeixi `GetCapabilities`, desplegar la jerarquia i seleccionar la capa concreta, no el grup genèric si no és el que demana el cas.
5. Revisar els CRS, el format d'imatge, la transparència i, en WMTS, la matriu disponible. L'elecció s'ha de basar en la compatibilitat amb el projecte i l'ús visual previst.
6. Afegir la capa, obrir-ne `Propietats > Informació` i registrar títol, font, tipus de servei, CRS, extensió, atribució i data de consulta.

La validació no acaba quan el mapa apareix. Cal navegar a una posició coneguda, comparar-la amb una capa vectorial de referència, observar el comportament a diverses escales i provar **Identifica**. Un resultat correcte és que la capa cobreixi l'àmbit declarat, mantingui la posició esperada i es comporti com el tipus de resposta documentat. Si no hi ha taula ni selecció vectorial, aquesta absència confirma que el recurs s'ha de conservar com a context, no com a entrada de geoprocessament.

Per a un WFS, es crea una connexió a la família corresponent, es consulta la llista de tipus d'entitat i se selecciona només el necessari. Si QGIS ofereix limitar la petició a l'extensió actual o aplicar un filtre, convé reduir primer l'àmbit per evitar una consulta massiva. Després de carregar la capa s'han de comprovar la taula, el tipus geomètric, l'esquema, el CRS, l'extensió i si el nombre recuperat ha estat limitat. Una advertència de truncament o paginació forma part del resultat de la prova i s'ha de resoldre abans d'analitzar.

Quan una consulta vectorial remota es converteix en entrada estable, `Exporta > Desa els objectes com a...` permet crear una còpia local en un format adequat, sempre que la llicència ho autoritzi. El nom i el diari han d'indicar que es tracta d'una extracció, amb la font, la data, el filtre i el CRS de sortida. L'exportació no s'ha de fer sobre el paquet original ni confondre amb una nova font independent.

Les descàrregues s'incorporen amb el gestor vectorial o ràster segons el contingut, no segons el nom comercial del producte. Abans d'afegir-les convé haver descomprimit el paquet i haver identificat el fitxer principal i els auxiliars. Si QGIS mostra diverses subcapes dins d'un GeoPackage, cal seleccionar-les pel nom i la descripció, no carregar-les totes per defecte. El capítol següent establirà on es conserva cada estat del fitxer.

## Cas resolt: seleccionar fonts per a una franja viària

Es planteja una decisió de fonts, no encara el geoprocessament complet: **quines parcel·les cadastrals de Vila-seca intersectarien una franja d'estudi definida al voltant d'un eix viari, i quina informació de context permetria revisar visualment la selecció?** La pregunta delimita quatre necessitats: un àmbit municipal, un eix vectorial, parcel·les vectorials i una imatge recent de context. La distància de la franja i la interpretació territorial correspondran al cas d'anàlisi i no es fixen en aquest capítol.

Per a l'àmbit, una descàrrega vectorial de divisions administratives de l'ICGC és preferible a dibuixar el contorn visible d'un mapa base. La capa triada ha de contenir el codi i el municipi de Vila-seca, declarar la data territorial, el CRS, l'escala o nivell de detall i la llicència. Una geometria molt generalitzada podria servir per situar el municipi i ser insuficient per retallar parcel·les a tocar del límit; per això la fitxa del producte ha de justificar el nivell escollit.

Per a l'eix viari, el Centro de Descargas del CNIG permet cercar un producte vectorial de xarxes de transport amb cobertura de la zona. La decisió es basa en què cada registre representi un eix o tram adequat, disposi dels camps necessaris per identificar la via i tingui una escala de producció compatible amb l'amplada de la franja. Un WMS amb carreteres dibuixades queda descartat com a entrada analítica perquè no aporta la geometria seleccionable. Si el producte estatal no conté el detall local requerit, la decisió s'ha de reobrir i cercar una font competent més detallada; no s'ha de completar la xarxa per intuïció.

Per a les parcel·les, el WMS cadastral és útil durant l'exploració, però queda descartat per calcular la intersecció. La via seleccionada és una descàrrega INSPIRE predefinida del municipi o, si l'àmbit és realment petit i el servei ho admet sense truncament, una consulta WFS documentada i exportada a una còpia local. La capa ha de conservar l'identificador cadastral publicat i la seva data de consulta. El resultat només podrà afirmar quines geometries del producte cadastral coincideixen amb la franja; no determinarà propietat, edificabilitat ni validesa jurídica del límit.

Per al context, es comparen el WMS PNOA de l'IGN/CNIG i l'ortofoto en línia de l'ICGC. No cal incorporar-los tots dos. Se selecciona el que documenti una data de captura i una resolució adequades a la inspecció, tingui cobertura de tot l'àmbit i ofereixi condicions d'ús compatibles amb el mapa. Si tots dos satisfan el requisit, la tria pot prioritzar la campanya més pertinent o la continuïtat amb la resta del projecte. La imatge servirà per detectar desajustos aparents i formular incidències, no per corregir automàticament les geometries oficials.

La selecció resolta queda formada, doncs, per tres entrades vectorials locals o fixades (divisió ICGC, eix viari CNIG i parcel·les del Cadastre) i un únic servei d'imatge per al context. Abans de continuar, QGIS ha de mostrar les tres taules vectorials, permetre seleccionar-ne entitats, declarar-ne els CRS i situar-ne les extensions sobre el mateix municipi. El servei d'imatge ha de cobrir la zona i respondre a l'escala de revisió. Els recomptes, les dates exactes i qualsevol discrepància observada s'han d'anotar després d'executar la pràctica; no es poden substituir per valors suposats.

## Activitats

### Comprovació: una pregunta, tres fonts

Cal formular una pregunta sobre mobilitat, equipaments o transformació urbana i localitzar tres recursos que aparentment hi estiguin relacionats. Per a cada recurs s'ha d'indicar si aporta context visual, geometries, atributs o una combinació d'aquests elements. L'activitat es completa explicant quin recurs no permetria executar l'anàlisi i per què.

La comparació ha d'incloure la unitat d'observació, la data del fenomen, l'escala o resolució, la llicència i la via d'accés. Si un recurs només s'ha trobat en un visor o mitjançant un connector, cal seguir-ne la traça fins a la pàgina del productor. La resposta no es valora pel nombre de portals consultats, sinó per la correspondència entre la pregunta i el contingut efectiu de cada font.

### Pràctica guiada: ortofoto i límit municipal

La demostració de Vila-seca combinarà una ortofoto servida en línia amb un límit municipal descarregat. Cal identificar productor, data, resolució o escala, CRS, llicència i via d'accés de cada font. Després s'ha de comprovar quines propietats es poden consultar sobre el límit vectorial i quines només es poden observar a la imatge.

La connexió al servei es farà des del `Gestor de fonts de dades`, sense requerir cap connector. Abans d'afegir l'ortofoto s'obrirà la fitxa oficial i es comprovarà el document de capacitats. Un cop carregades les dues fonts, la validació ha de deixar constància de si el límit té taula i geometria seleccionable, si els CRS estan identificats, si les extensions coincideixen amb l'àmbit i com canvia la imatge en variar l'escala. No s'han de deduir exactituds a partir de la superposició visual.

### Preparació de la micropràctica 1

Cada estudiant seleccionarà el municipi assignat i redactarà una pregunta que es pugui desenvolupar durant el curs. La proposta haurà d'identificar, com a mínim, una font de referència, una font vectorial i una font ràster o servei d'imatge. Aquesta preparació no és encara el lliurament: el capítol següent convertirà la selecció en un projecte documentat i transportable.

Per a cada candidata cal conservar el títol exacte del producte, el productor, la URL de la fitxa, la data d'accés, l'àmbit, el període, l'escala o resolució, el CRS, la llicència, el model de dades i la via d'accés. També s'ha d'indicar quina operació futura necessita aquella font i quin control podria fer-la descartar. Les còpies locals, les connexions i el diari s'organitzaran al capítol següent; en aquesta fase la prioritat és que cap capa entri al projecte sense una funció definida.
