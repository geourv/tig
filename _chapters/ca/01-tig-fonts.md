---
layout: manual-chapter
title: TIG, preguntes i fonts geogràfiques
description: Criteris per formular preguntes territorials, entendre un SIG i seleccionar fonts geogràfiques adequades.
lang: ca
ref: manual-tig-questions-sources
profiles: [unaltremanual]
content_status: approved
permalink: /ca/chapters/tig-preguntes-fonts/
weight: 20
part: Continguts
manual_references: true
---

Una tecnologia de la informació geogràfica només és útil quan ajuda a respondre una pregunta sobre el territori. Localitzar una carretera, delimitar una zona inundable, estudiar l'accés a un equipament o comparar el relleu de dos municipis exigeix relacionar **on passa un fenomen**, **què se'n coneix** i **amb quina qualitat s'ha observat**. Obrir una capa sense haver formulat aquesta relació pot produir un mapa, però no necessàriament una resposta.

>>>>> En acabar el capítol, cal poder convertir una necessitat territorial en una pregunta de dades i justificar quines fonts permeten respondre-la.
>>>>>
>>>>> - Distingir els SIG, les TIG i la ciència de la informació geogràfica, i relacionar-los amb perfils professionals diferents.
>>>>> - Delimitar fenomen, unitat d'observació, àmbit, període i mesura.
>>>>> - Explicar la funció de les persones, les dades, els mètodes, el programari i la infraestructura dins d'un SIG.
>>>>> - Distingir una descàrrega de dades d'un servei de visualització o consulta.
>>>>> - Avaluar autoria, data, escala o resolució, sistema de referència, llicència i limitacions d'una font.

## SIG, TIG i ciència de la informació geogràfica

Sistema d'informació geogràfica (SIG)
: Organització concreta de persones, dades, mètodes, programari i infraestructura orientada a una finalitat.

Tecnologies de la informació geogràfica (TIG)
: Mètodes i instruments que permeten obtenir, gestionar, analitzar i comunicar informació georeferenciada.

Ciència de la informació geogràfica (GIScience)
: Disciplina que investiga com es representa, s'analitza, es visualitza i s'interpreta la informació referida a la Terra, inclosos els efectes de l'escala, la incertesa i les decisions de modelització.

QGIS és l'aplicació principal del curs, però no és tot el sistema: la pregunta, les fonts, les decisions i les comprovacions continuen existint fora del programa. Tampoc no és tota la disciplina. Goodchild va proposar la GIScience com un camp de recerca sobre les qüestions fonamentals que plantegen els SIG, i els desenvolupaments científics i tècnics s'han alimentat mútuament des d'aleshores {% cite goodchildGeographicalInformationScience1992 longleyGeographicInformationScience2015 nunesDiccionariSIG2012 %}.

En una pregunta com «quins habitatges queden més exposats a una inundació?», les TIG inclouen la captura, el modelatge i la comunicació; el SIG concreta les persones, dades, regles i eines que executen el treball; i la GIScience obliga a preguntar què significa proximitat, com es representa la inundació, quina incertesa tenen els límits i quina conclusió permet sostenir el resultat. No és una tercera aplicació, sinó el marc que permet raonar sobre allò que el sistema fa.

La figura següent mostra una convergència didàctica, no una delimitació exhaustiva de la disciplina. El cercle de TIG i SIG aporta les preguntes territorials i els sistemes de treball; l'estadística i les matemàtiques aporten models, dependència i incertesa; i la informàtica aporta estructures de dades, algorismes i bases de dades. La GIScience estudia les decisions que apareixen quan aquestes peces es combinen. També incorpora dimensions cognitives, socials, institucionals i ètiques que aquest esquema breu no representa.

![Convergència de les TIG i els SIG, l'estadística i les matemàtiques, i la informàtica en preguntes pròpies de la GIScience]({{ site.baseurl }}/assets/diagrams/ca/01-tig-fonts/giscience-intersections.mmd "Síntesi didàctica de tres aportacions a la ciència de la informació geogràfica: preguntes i sistemes territorials, models i incertesa, i estructures i algorismes. La disciplina és més àmplia que els tres àmbits representats."){: data-figure-width-web="43rem" data-figure-width-pdf="95%"}

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

>>> **Pregunta operativa.** La pregunta «On falten fanals?» no defineix una unitat ni un criteri. Una versió analitzable podria ser: «Quins trams de la xarxa de carrers del nucli de Vila-seca queden a més de 30 m d'un fanal inventariat durant la campanya de camp?». Ara es poden identificar les capes, la distància, l'àmbit i la data, tot i que el llindar encara s'ha de justificar.

La formulació permet derivar una **especificació de dades**. Per al cas dels fanals caldria una observació puntual amb identificador i data, una xarxa de carrers amb trams connectats, una delimitació del nucli i un sistema de referència de coordenades (CRS) adequat per interpretar la distància. També caldria saber si «quedar a més de 30 m» es mesura en línia recta, al llarg de la xarxa o respecte de la superfície il·luminada. La mateixa frase que orienta la cerca revela, doncs, decisions metodològiques encara pendents.

Una font candidata s'ha de poder descartar. Si el recurs només retorna una imatge amb els carrers dibuixats, pot servir per orientar-se, però no aporta necessàriament els eixos vectorials sobre els quals calcular distàncies de xarxa. Si l'inventari de fanals no declara la data o només cobreix una part del nucli, el resultat descriurà la cobertura de l'inventari i no tots els fanals existents. Definir abans aquests criteris evita confondre disponibilitat amb adequació.

La unitat d'observació mereix una comprovació específica perquè sovint queda amagada darrere del nom de la capa. Una capa anomenada «carreteres» pot contenir eixos, trams entre interseccions, calçades separades, plataformes o enllaços; una capa «edificis» pot representar petjades, construccions cadastrals o punts d'adreça. Abans de buscar una operació de QGIS cal poder completar la frase «cada entitat representa...». Si la resposta no es troba a les metadades o a l'esquema, la font encara no està prou entesa.

## Els components d'un SIG

La informació georeferenciada combina un **component espacial**, que descriu posició, forma i relacions, amb un **component temàtic**, que descriu identitat, categoria o valor. Un SIG coordina tots dos components mitjançant cinc peces interdependents: persones, dades, mètodes, programari i infraestructura.

![Relació interdependent entre un SIG i les persones, les dades, els mètodes, el programari i la infraestructura]({{ site.baseurl }}/assets/diagrams/ca/01-tig-fonts/gis-components.mmd "Un SIG orientat a una finalitat territorial necessita persones que decideixen i interpreten, dades que representen el fenomen, mètodes que ordenen el procés, programari que executa operacions i infraestructura que sosté el treball."){: data-figure-width-web="39.5rem" data-figure-width-pdf="94%"}

La figura no descriu una cadena lineal ni cinc recursos substituïbles. Les persones defineixen la finalitat i interpreten els resultats; els mètodes converteixen aquesta finalitat en procediments i controls; i les dades, el programari i la infraestructura en fan possible l'execució. Una modificació en qualsevol peça pot obligar a revisar les altres: canviar de font pot alterar l'esquema i el mètode, i canviar d'entorn pot exigir altres formats, permisos o estratègies de còpia.

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

### Perfils professionals i responsabilitats

El component **persones** no correspon a un únic lloc de treball. Els noms dels perfils canvien entre organitzacions i sovint se solapen: la classificació O*NET de tecnòlegs i tècnics SIG, per exemple, reuneix tasques de manteniment de bases de dades, control de qualitat, cartografia, anàlisi, desenvolupament d'aplicacions i suport a usuaris. La categoria de ciència de dades comparteix preparació, programació, modelització, visualització i comunicació de resultats, però posa més èmfasi en els models estadístics i predictius. Aquestes categories descriuen l'economia dels Estats Units i són útils per comparar responsabilitats, però no constitueixen una taxonomia universal {% cite nationalCenterONETGIS2026 nationalCenterONETDataScientists2026 %}.

::: table "Perfils geoespacials, responsabilitats i exemples de treball"
| Perfil | Responsabilitat predominant | Exemple i eines habituals |
| --- | --- | --- |
| Tècnic o tècnica SIG | Capturar, digitalitzar, convertir i revisar dades; mantenir esquemes, metadades i productes cartogràfics | Preparar un inventari de fanals i comprovar geometries i camps amb QGIS, aplicacions de camp, GNSS, fulls de càlcul i GDAL |
| Analista SIG | Convertir una pregunta territorial en indicadors, operacions espacials, controls i una interpretació | Identificar trams allunyats dels fanals mitjançant QGIS, SQL espacial, PostGIS i, quan cal, Python o R |
| Especialista en ciència de dades geoespacials | Preparar variables, ajustar i validar models estadístics o d'aprenentatge automàtic i quantificar la incertesa | Modelitzar patrons d'incidències amb Python o R, quaderns reproduïbles, biblioteques espacials i bases de dades |
| Especialista en desenvolupament o enginyeria geoespacial | Construir processos ETL, API, aplicacions cartogràfiques, connectors i desplegaments | Publicar una API i un visor amb Python, JavaScript, SQL, GDAL, PostGIS o les API de QGIS |
| Responsable d'administració o coordinació SIG | Governar catàlegs, permisos, versions, serveis, còpies i criteris de qualitat entre equips | Mantenir una base espacial i els seus serveis, documentar dependències i comprovar-ne recuperació i disponibilitat |
:::

Els perfils es diferencien per la responsabilitat predominant, no per una frontera d'eines. En un equip petit, una mateixa persona pot preparar dades, analitzar-les i publicar un mapa; en un projecte gran, aquestes funcions es poden repartir entre diverses especialitats. El domini de QGIS tampoc no defineix tot un perfil: cal entendre la pregunta, el model de dades, els controls i les conseqüències de les decisions.

En portals professionals com LinkedIn, el títol pot ometre el qualificatiu **geoespacial** encara que les tasques utilitzin adreces, xarxes, imatges, coordenades, SQL espacial o cartografia. Una oferta d'analista de dades pot requerir geocodificació i QGIS; una de ciència de dades pot construir variables de proximitat; i una d'enginyeria de programari pot mantenir una API de mapes. Per interpretar un perfil cal llegir les dades, les responsabilitats, els resultats i les eines demanades, no cercar només `GIS` o `SIG` al títol.

## Fonts, productes i vies d'accés

Font
: Identifica qui produeix o manté la informació i amb quin procediment.

Producte
: Conjunt de dades concret, amb una versió, una cobertura i unes especificacions.

Capa
: Unitat de contingut espacial homogeni que una aplicació pot obrir o consultar.

Via d'accés
: Mecanisme per arribar al producte o a una capa, com una URL, una descàrrega, un connector o un servei web.

Barrejar aquests nivells dificulta atribuir les dades i saber què ha canviat quan una connexió deixa de funcionar.

També convé separar el **portal de descoberta** del recurs utilitzat. Un catàleg permet cercar productes i llegir-ne fitxes; un visor o agregador, com l'[Hipermapa de Catalunya](https://sig.gencat.cat/visors/hipermapa.html), permet explorar una zona i descobrir informació publicada per organismes diferents; una pàgina de documentació publica l'adreça d'un servei; i un fitxer o una resposta web aporta les dades efectives. El nom del portal no substitueix el productor, el títol del producte ni la capa concreta. En un inventari de fonts, «Hipermapa», «ICGC» o «CNIG» és massa genèric si no s'hi afegeixen el producte, l'edició i la via d'accés.

En el curs s'utilitzaran sobretot fonts institucionals. El Centro Nacional de Información Geográfica (CNIG) distribueix cartografia estatal; l'[Institut Cartogràfic i Geològic de Catalunya](https://www.icgc.cat/) publica cartografia, ortofotos i models d'elevacions; el [Cadastre](https://www.sedecatastro.gob.es/) ofereix informació cadastral amb condicions pròpies; i el portal de [dades obertes de la Generalitat](https://dadesobertes.gencat.cat/) reuneix registres administratius i altres conjunts temàtics. Que una font sigui oficial no evita haver de llegir-ne les metadades ni comprovar que respon la pregunta.

### Mapa, fotografia aèria i imatge de satèl·lit

Un mapa i una imatge poden compartir extensió i aparença zenital, però no fan la mateixa afirmació. El mapa és una representació cartogràfica intencional: selecciona, generalitza i simbolitza objectes o valors segons una escala i una finalitat. Una fotografia o una imatge de sensor registra resposta electromagnètica en un instant i necessita processament i interpretació abans que cada forma visible es pugui tractar com una entitat.

::: table "Distincions bàsiques entre productes cartogràfics i imatges"
| Producte | Com s'obté | Què cal recordar |
| --- | --- | --- |
| Mapa | Selecció i simbolització de dades geogràfiques | La llegenda, l'escala, la font, la data i el CRS expliquen què representa; no és una còpia literal del paisatge |
| Fotografia aèria | Càmera transportada per una aeronau, amb presa vertical o obliqua | La perspectiva, la inclinació, el relleu i l'òptica poden variar l'escala i desplaçar objectes; no és necessàriament una base de mesura |
| Ortofoto | Fotografia aèria orientada i corregida geomètricament amb informació del relleu | Permet mesures planimètriques dins de l'exactitud declarada, però conserva una data de captura, oclusions i possibles errors residuals |
| Ortofotomapa | Ortofoto combinada amb elements cartogràfics, com topònims, retícula, límits, escala o llegenda | És un producte cartogràfic compost; cal distingir la data de la imatge de la data i la font de les capes superposades |
| Imatge de satèl·lit | Sensor situat en una plataforma orbital, sovint amb diverses bandes | L'òrbita, la resolució espacial, espectral i temporal i el nivell de processament en condicionen l'ús; pot estar ortorectificada, però no és un mapa pel sol fet d'estar georeferenciada |
:::

La paraula **ortofoto** descriu el tractament geomètric d'una fotografia aèria, no qualsevol vista des de dalt. **Ortoimatge** és un terme més general que també pot incloure imatges de satèl·lit ortorectificades. En tots dos casos, ampliar el zoom no supera la resolució ni l'exactitud del producte, i la presència visible d'un objecte no n'aporta automàticament geometria vectorial ni atributs.

## Interoperabilitat, estàndards i llicències

La **interoperabilitat** és la capacitat de sistemes diferents per intercanviar informació i interpretar-la de manera compatible. No n'hi ha prou que dos programes obrin un fitxer o mostrin una imatge: han de coincidir en el significat de geometries, camps, valors absents, dates, CRS, operacions i respostes. Els estàndards fixen parts d'aquest contracte perquè el projecte no depengui exclusivament d'una aplicació o d'un proveïdor.

Tres nivells institucionals apareixeran repetidament al manual:

::: table "ISO, INSPIRE i OGC dins de la interoperabilitat geogràfica"
| Marc | Funció | Exemple útil al curs |
| --- | --- | --- |
| [ISO/TC 211](https://committee.iso.org/home/tc211) | Desenvolupa la família internacional de normes sobre informació geogràfica digital, inclosos models, metadades, qualitat i serveis | ISO 19115 estructura metadades; ISO 19128 correspon al mateix document tècnic que WMS 1.3.0 |
| [INSPIRE](https://knowledge-base.inspire.ec.europa.eu/legislation_en) | Estableix el marc jurídic de la Unió Europea per fer compatibles i utilitzables les infraestructures d'informació espacial dels estats | Les regles d'execució són vinculants; les guies tècniques expliquen com aplicar-les amb estàndards existents |
| [Open Geospatial Consortium](https://www.ogc.org/standards-overview/) (OGC) | Elabora especificacions geoespacials obertes per compartir dades i funcions entre sistemes | WMS demana mapes, WMTS demana tessel·les i WFS demana objectes geogràfics {% cite ogcWMS2006 ogcWMTS2010 ogcWFS2014 %} |
:::

Aquests nivells es relacionen, però no són sinònims. ISO publica normes internacionals; INSPIRE imposa i orienta una infraestructura europea; i OGC desenvolupa molts dels contractes tècnics que implementen clients i servidors. Un servei pot seguir WMS 1.3.0 i, alhora, aplicar el perfil INSPIRE d'ISO 19128. La conformitat tècnica no demostra que la dada sigui exacta, actual, oberta o adequada per a una pregunta concreta.

La **llicència** resol una qüestió diferent: què es pot fer legalment amb el programari, les dades o el resultat. [QGIS es distribueix amb la GNU GPL](https://qgis.org/license/), que permet estudiar, modificar i redistribuir el programa segons les seves condicions; això no converteix automàticament en GPL les dades obertes o els mapes creats amb QGIS. De manera semblant, [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.ca) permet compartir i adaptar el material amb atribució, però no elimina drets de privacitat ni altres restriccions.

Poder obrir una capa no implica poder reutilitzar-la. La llicència del producte pot regular atribució, redistribució, transformació o ús comercial; les condicions del servei poden regular, a més, freqüència de peticions, credencials i comportament del client. «Gratuït», «accessible» i «obert» no són sinònims. En un mapa compost poden coexistir una geometria amb llicència oberta, un fons amb condicions específiques i una composició d'autoria pròpia.

>> **Estàndards i llicències redueixen dependències, però no eliminen els canvis.** Un format o servei estàndard i una llicència oberta faciliten traslladar dades i coneixement entre eines, inspeccionar el procés i reconstruir el treball. No garanteixen que totes les implementacions siguin idèntiques, que un servidor continuï disponible o que una versió futura conservi cada comportament. Per això també cal conservar formats, versions, peticions, metadades i proves d'obertura.

La fitxa mínima de la font ha de conservar la llicència identificada, l'atribució prevista i qualsevol restricció que afecti el projecte. Quan les condicions no són clares, la decisió prudent és no redistribuir ni afirmar un permís que no s'ha pogut verificar.

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

Un connector de QGIS pot simplificar l'accés, però no substitueix el productor, la llicència ni les especificacions del producte, i tampoc no converteix una imatge de mapa en dades analítiques. La connexió directa al servei fa més visible quin contracte s'està utilitzant.

La diferència operativa principal és la persistència. Una descàrrega crea una còpia local vinculada a una versió; un servei o una API consulta allò que el servidor ofereix en aquell moment. Durant la descoberta es pot explorar un WMS o un WMTS i després obtenir la capa vectorial adequada per a l'anàlisi. La via remota resol l'accés i la còpia local fixa una entrada, però totes dues han de conservar el producte, la consulta, la data i la llicència.

## Peticions i respostes d'un servei geogràfic

QGIS actua com a **client**: envia al servidor una petició que identifica una operació, una capa, una extensió, un CRS i altres paràmetres. El servidor valida la petició, consulta o representa les dades i retorna una resposta. L'adreça base no és «la capa»; la capa i el resultat concret depenen dels paràmetres i de l'estat del servidor en la data de consulta.

En WMS, WMTS i WFS, `GetCapabilities` demana un document, habitualment XML, que descriu les operacions, les capes, els formats i els CRS admesos. QGIS el llegeix en connectar-se. Si el document no arriba, cal revisar adreça, xarxa, certificat o servidor; si arriba però una consulta falla, cal revisar capa, extensió, CRS, format, límits i autenticació. Les capacitats s'han de contrastar amb la fitxa institucional: no garanteixen llicència, qualitat, completesa ni disponibilitat permanent.

### WMS: una representació renderitzada

El [Web Map Service (WMS)](https://www.ogc.org/standards/wms/) està orientat a obtenir imatges de mapes georeferenciades. L'operació `GetMap` indica, entre altres peces, la capa, l'estil, el CRS, el rectangle geogràfic (`BBOX`), l'amplada, l'alçada i el format, com PNG o JPEG. El servidor selecciona les dades necessàries, aplica la simbolització i genera els píxels que el client col·loca al llenç.

La connexió de context de la primera micropràctica utilitza l'[adreça base del WMS de l'Ortofoto Territorial de l'ICGC](https://geoserveis.icgc.cat/servei/catalunya/orto-territorial/wms). El seu [`GetCapabilities`](https://geoserveis.icgc.cat/servei/catalunya/orto-territorial/wms?SERVICE=WMS&REQUEST=GetCapabilities&VERSION=1.3.0) descriu la capa vigent i les edicions disponibles, entre les quals caldrà identificar la de 2025. L'[adreça base del WMS PNOA màxima actualitat](https://www.ign.es/wms-inspire/pnoa-ma) i el seu [document de capacitats](https://www.ign.es/wms-inspire/pnoa-ma?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities) serveixen aquí com a segon exemple per observar el mateix contracte, però no són el fons de la micropràctica. A QGIS es desa l'adreça base; els paràmetres de cada imatge els compon el client.

La primera petició es pot enganxar directament al navegador. La resposta no és un mapa, sinó el document XML amb què l'ICGC descriu les capacitats del servei:

::: listing "Capacitats del WMS Ortofoto Territorial"
```url
https://geoserveis.icgc.cat/servei/catalunya/orto-territorial/wms?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities
```
:::

Una segona petició demana la capa `ortofoto_25cm_color_2025` sobre una extensió de `10.000 × 7.500 m` que inclou Vila-seca. En `EPSG:25831`, el rectangle `BBOX` s'expressa en coordenades est i nord. Els `800 × 600` píxels de la resposta representen 12,5 m sobre el terreny cadascun: aquesta mida de sortida no substitueix la resolució font de 25 cm anunciada pel nom de la capa.

::: listing "Petició GetMap de l'Ortofoto Territorial 2025 sobre Vila-seca"
```url
https://geoserveis.icgc.cat/servei/catalunya/orto-territorial/wms?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&LAYERS=ortofoto_25cm_color_2025&STYLES=&CRS=EPSG:25831&BBOX=340000,4549500,350000,4557000&WIDTH=800&HEIGHT=600&FORMAT=image/jpeg
```
:::

>> **No cal memoritzar la URL.** En aquest punt n'hi ha prou amb reconèixer que `SERVICE` identifica la família, `REQUEST` l'operació, `LAYERS` la capa, `CRS` la referència espacial, `BBOX` el lloc i `WIDTH`, `HEIGHT` i `FORMAT` la resposta. QGIS compon aquests paràmetres després de llegir les capacitats; escriure'ls una vegada al navegador permet observar el contracte que normalment queda ocult darrere de la interfície.

Les dues respostes següents provenen de peticions independents sobre la mateixa capa i extensió. La segona duplica l'amplada i l'alçada i, per tant, quadruplica el nombre de píxels de sortida; permet una representació més fina a la pantalla, però no millora l'exactitud ni crea observacions noves a la font.

::: subfigures a+b "Dues respostes GetMap de la mateixa capa i extensió. Canviar WIDTH i HEIGHT modifica la graella de la imatge retornada, no la resolució ni la qualitat de les dades d'origen. Respostes conservades el 15 de setembre de 2026. Font: ICGC."
![Resposta GetMap de 800 per 600 píxels de l'Ortofoto Territorial 2025 sobre Vila-seca]({{ site.baseurl }}/assets/img/icgc/ortofoto-territorial-2025-catalunya-800.jpg "Sortida de 800 × 600 píxels, equivalent a 12,5 m per píxel per a l'extensió demanada.")
![Resposta GetMap de 1600 per 1200 píxels de l'Ortofoto Territorial 2025 sobre Vila-seca]({{ site.baseurl }}/assets/img/icgc/ortofoto-territorial-2025-catalunya-1600.jpg "Sortida de 1.600 × 1.200 píxels, equivalent a 6,25 m per píxel per a la mateixa extensió.")
:::

El recorregut deixa clar que la simbolització i la renderització es resolen al servidor abans que la resposta arribi al client.

![Recorregut d'una petició GetMap des del client SIG fins a la imatge retornada pel servidor WMS]({{ site.baseurl }}/assets/diagrams/ca/01-tig-fonts/wms-request-response.mmd "Una petició GetMap combina capa, estil, CRS, extensió, mida i format; el servidor aplica aquests paràmetres i retorna una imatge renderitzada, no les geometries font."){: data-figure-width-web="46rem" data-figure-width-pdf="100%"}

La resposta conserva una relació espacial amb l'extensió demanada, però no lliura necessàriament les geometries ni la taula que hi ha darrere. No es poden seleccionar les parcel·les d'un PNG, canviar-ne els camps o executar-hi una intersecció vectorial. Alguns WMS ofereixen `GetFeatureInfo`, que retorna informació sobre la posició o el píxel consultat. Aquesta operació és útil per identificar allò que el productor exposa, però no transforma la imatge en una capa vectorial completa.

El WMS és adequat per donar context, comparar visualment una capa pròpia amb una cartografia oficial o consultar una representació temàtica controlada pel productor. També permet demanar imatges transparents i superposar-les. No és la via correcta si la pregunta exigeix editar geometries, recalcular una classificació a partir dels atributs o conservar els valors originals d'un sensor. En aquests casos cal localitzar una descàrrega, un servei d'objectes o una cobertura adequada.

### WMTS: tessel·les i nivells definits

El [Web Map Tile Service (WMTS)](https://www.ogc.org/standards/wmts/) distribueix imatges segons una o més matrius de tessel·les. En lloc de generar una imatge amb qualsevol amplada, alçada i extensió, el client demana una tessel·la identificada per la matriu, la fila i la columna d'un nivell. Els límits, les resolucions i els CRS disponibles queden declarats al document de capacitats.

El PNOA també es publica a l'[adreça base del seu WMTS](https://www.ign.es/wmts/pnoa-ma). El [`GetCapabilities` del WMTS](https://www.ign.es/wmts/pnoa-ma?SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetCapabilities) no descriu rectangles arbitraris, sinó capes i conjunts de matrius amb els nivells, els CRS i els formats disponibles.

::: listing "Capacitats WMTS del PNOA"
```url
https://www.ign.es/wmts/pnoa-ma?SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetCapabilities
```
:::

La petició següent recupera una sola tessel·la JPEG de `256 × 256` píxels que cobreix una part de Vila-seca. A diferència de `GetMap`, no defineix una extensió i una mida arbitràries: identifica una matriu, un nivell, una fila i una columna que el servidor ja havia anunciat.

::: listing "Petició GetTile del PNOA sobre Vila-seca"
```url
https://www.ign.es/wmts/pnoa-ma?SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetTile&LAYER=OI.OrthoimageCoverage&STYLE=default&TILEMATRIXSET=GoogleMapsCompatible&TILEMATRIX=15&TILEROW=12272&TILECOL=16488&FORMAT=image/jpeg
```
:::

El primer esquema descriu la jerarquia del conjunt de matrius, el nivell, la fila i la columna que determina quina tessel·la concreta es recupera.

![Relació entre el conjunt de matrius WMTS, els nivells i l'adreça d'una tessel·la]({{ site.baseurl }}/assets/diagrams/ca/01-tig-fonts/wmts-tile-matrix.mmd "GetCapabilities declara el CRS i les matrius disponibles; GetTile identifica una cel·la mitjançant el conjunt, el nivell, la fila i la columna i en retorna la tessel·la d'imatge."){: data-figure-width-web="46rem" data-figure-width-pdf="95%"}

Aquesta regularitat permet reutilitzar tessel·les entre usuaris i peticions. Molts serveis les preparen anticipadament o les generen quan es demanen i les guarden en memòria cau. El resultat acostuma a ser més àgil per navegar per un mapa base, però no hi ha una garantia universal de velocitat: la xarxa, el servidor, la cobertura de la memòria cau i el nombre de capes continuen intervenint.

El diagrama de seqüència mostra després que QGIS no demana una extensió arbitrària, sinó una cel·la concreta de la matriu declarada.

![Seqüència entre QGIS, un servidor WMTS i el magatzem de tessel·les]({{ site.baseurl }}/assets/diagrams/ca/01-tig-fonts/wmts-request-response.mmd "Després de llegir GetCapabilities, el client identifica la tessel·la amb el conjunt de matrius, el nivell, la fila i la columna; el servidor retorna la imatge disponible o una excepció."){: data-figure-width-web="46rem" data-figure-width-pdf="100%"}

El cost d'aquesta estratègia és que el client s'ha d'ajustar als nivells disponibles. Entre dos nivells, QGIS pot reescalar una tessel·la, però no apareix informació nova. El mapa també arriba renderitzat; encara que els contorns siguin molt nítids, no són objectes seleccionables. Un WMTS és, per tant, una bona base visual quan la seva cartografia, data, escala i llicència són adequades, però no una substitució d'una capa vectorial d'anàlisi.

### WFS: objectes i atributs

El [Web Feature Service (WFS)](https://www.ogc.org/standards/wfs/) consulta objectes geogràfics. `GetFeature` pot retornar geometries i atributs filtrats per tipus d'entitat, extensió o condició, i QGIS els pot tractar com a vector. Això no implica rebre la base mestra completa: el servidor pot publicar una vista, ometre camps, simplificar geometries, paginar o limitar el nombre de resultats. Cal comprovar l'esquema, el recompte efectivament recuperat i qualsevol avís abans d'analitzar la resposta.

El Cadastre publica les parcel·les a l'[adreça base del WFS INSPIRE](https://ovc.catastro.meh.es/INSPIRE/wfsCP.aspx). El seu [`GetCapabilities`](https://ovc.catastro.meh.es/INSPIRE/wfsCP.aspx?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetCapabilities) descriu els tipus d'entitat, les operacions i els formats anunciats; la connexió no s'ha de confondre amb el [WMS cadastral](https://ovc.catastro.meh.es/cartografia/INSPIRE/spadgcwms.aspx), que només retorna representacions.

::: listing "Capacitats del WFS de parcel·les cadastrals"
```url
https://ovc.catastro.meh.es/INSPIRE/wfsCP.aspx?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetCapabilities
```
:::

Una petició `GetFeature` pot acotar la resposta a una extensió molt petita i limitar-la a una entitat. En aquest servei, `EPSG:4258` segueix l'ordre oficial latitud-longitud; l'ordre del `BBOX` no s'ha de copiar a un altre CRS sense consultar-ne la definició.

::: listing "Una parcel·la retornada pel WFS del Cadastre"
```url
https://ovc.catastro.meh.es/INSPIRE/wfsCP.aspx?SERVICE=WFS&VERSION=2.0.0&REQUEST=GetFeature&TYPENAMES=cp:CadastralParcel&SRSNAME=urn:ogc:def:crs:EPSG::4258&BBOX=41.10897,1.14250,41.10899,1.14253,urn:ogc:def:crs:EPSG::4258&COUNT=1
```
:::

El navegador retorna XML amb la geometria i els atributs que el servei exposa per a aquella consulta. Rebre una parcel·la no autoritza a interpretar-ne titularitat, propietat o validesa registral, ni garanteix que una consulta més extensa no quedi limitada.

Abans de consultar objectes, el client pot llegir les capacitats i l'esquema publicat; aquest recorregut explica per què una capa WFS conserva camps i geometries que no existeixen en una resposta WMS o WMTS.

![Seqüència de descoberta, consulta i possible transacció entre QGIS, un servidor WFS i les dades publicades]({{ site.baseurl }}/assets/diagrams/ca/01-tig-fonts/wfs-feature-access.mmd "GetCapabilities i DescribeFeatureType descriuen el contracte; GetFeature retorna objectes filtrats, mentre que una transacció només és possible quan el servei l'anuncia i l'usuari està autoritzat."){: data-figure-width-web="47rem" data-figure-width-pdf="100%"}

La prova decisiva és què arriba al client. Un WMS o un WMTS retorna píxels representats pel servidor; un WFS retorna objectes amb geometria i propietats. `GetFeatureInfo` pot mostrar informació d'un píxel WMS, però no converteix la imatge en una capa vectorial. Les operacions transaccionals WFS-T són opcionals i requereixen permisos; carregar un WFS no autoritza a modificar la font institucional.

::: subfigures a+b "El gestor de fonts separa les connexions que retornen imatges de les que retornen objectes. En tots dos casos, Nova només obre la configuració: aquestes captures no mostren cap URL desada, cap resposta del Cadastre ni una connexió validada. QGIS 3.44.11."
![Entrada WMS/WMTS del gestor de fonts de QGIS]({{ site.baseurl }}/assets/img/qgis/qgis-cadastre-wms-connection.png "WMS/WMTS és la família adequada per crear una connexió a un servei que retorna una imatge cartogràfica.")
![Entrada WFS i OGC API Features del gestor de fonts de QGIS]({{ site.baseurl }}/assets/img/qgis/qgis-cadastre-wfs-connection.png "WFS / OGC API - Features és la família adequada per consultar objectes i atributs, amb opcions pròpies com limitar la petició a l'extensió visible.")
:::

### QuickMapServices i Open ICGC

La connexió directa és la via més transparent per aprendre què identifica una URL, quines operacions anuncia `GetCapabilities` i quina capa s'ha seleccionat. Dos connectors de QGIS poden abreujar després la descoberta i l'accés. [QuickMapServices](https://plugins.qgis.org/plugins/quick_map_services/) consulta un catàleg comunitari de mapes base i serveis geogràfics; [Open ICGC](https://plugins.qgis.org/plugins/OpenICGC/) dona accés a dades obertes de l'ICGC, mapes base, cerques, fototeca històrica i descàrregues de productes vectorials o ràster. Tots dos s'instal·len des de `Complements > Gestiona i instal·la complements`.

El connector és una interfície d'accés, no el productor de totes les capes que mostra. Abans d'incorporar-ne una al projecte cal obrir-ne la informació, identificar el productor o distribuïdor i el producte, determinar si arriba per WMS, WMTS, XYZ, WFS o descàrrega, i registrar metadades, data d'accés, llicència i atribució. En QuickMapServices, una definició aportada per la comunitat pot canviar o deixar de funcionar; en Open ICGC, cada eina o capa pot correspondre a un servei i unes condicions diferents.

![Menús imbricats d'Open ICGC fins a la capa de municipis de les divisions administratives a escala 1:5.000]({{ site.baseurl }}/assets/img/qgis/qgis-open-icgc-menu.png "Open ICGC facilita la ruta fins a Divisions administratives > Municipis > Municipis 1:5.000. La captura identifica la via d'accés a QGIS 3.44.11; no demostra que la capa s'hagi carregat ni substitueix les metadades, la llicència o la identificació de l'ICGC com a productor."){: data-figure-width-web="56rem" data-figure-width-pdf="100%"}

>>> **Comparació verificable.** Una mateixa zona es pot obrir amb una connexió WMS directa i amb un connector. La prova no consisteix només a constatar que les dues imatges s'assemblen: cal comparar productor, nom de capa, tipus de servei, URL efectiva, CRS anunciats, atribució i comportament de l'eina **Identifica**. Si aquests elements no es poden recuperar, el connector és útil per explorar però encara no documenta una entrada del projecte.

## Escala, resolució i disponibilitat

Escala cartogràfica
: Relació entre una distància representada i la distància corresponent al territori.

Resolució espacial
: Unitat de mostreig o de sortida que limita el detall distingible d'un producte.

Generalització
: Selecció, simplificació, agregació o desplaçament d'elements per fer-los llegibles o adequats a una escala.

Aquestes propietats estan relacionades, però no són sinònimes, i canviar el zoom no en modifica la qualitat original.

En un WMS, `WIDTH`, `HEIGHT` i `BBOX` determinen la mida dels píxels de la imatge retornada. Demanar més píxels no augmenta l'exactitud ni recupera detalls que la dada font o l'estil han omès. El servidor també pot aplicar visibilitat dependent de l'escala: una carretera local o una etiqueta pot aparèixer només en determinats intervals. Una absència a escala regional no demostra que l'objecte no existeixi al producte.

En un WMTS, cada nivell de la matriu té una resolució definida. QGIS pot mostrar el mapa a una escala intermèdia, però ho fa ampliant o reduint les tessel·les disponibles. En un WFS o una descàrrega vectorial, la geometria pot provenir d'una generalització prèvia encara que es pugui ampliar indefinidament. El nombre de vèrtexs visible no és una mesura suficient d'exactitud; cal recuperar l'escala o les especificacions de producció.

Una prova de font ha d'observar almenys tres escales relacionades amb l'ús: una vista de context, l'escala prevista d'anàlisi i una ampliació de diagnòstic. La vista de context comprova cobertura i posició general. L'escala de treball mostra si els objectes necessaris són distingibles. L'ampliació revela pixelació o simplificació, però no autoritza a treballar a aquell detall. El diari ha de registrar a quina escala la font deixa de sostenir la lectura requerida.

La disponibilitat forma part de la qualitat operativa. Un servei remot depèn del servidor, la xarxa, els certificats, les credencials, els límits de petició i les decisions futures del productor. No s'ha d'afirmar que un servei està «sempre actualitzat» o disponible en temps real si la documentació no defineix l'actualització ni un compromís de servei. Una capa visible avui pot canviar de nom, estil, contingut o adreça.

Les memòries cau redueixen transferències i temps de resposta, però introdueixen un altre estat. El servidor pot conservar tessel·les generades amb una versió anterior i el client pot mostrar una resposta local quan la xarxa ja no està disponible. Veure una capa després de desconnectar-se no demostra que el servei funcioni, i buidar la memòria cau no corregeix una font obsoleta. Per diagnosticar cal distingir la còpia del client, la memòria cau del servidor i la dada publicada.

Quan l'anàlisi ha de ser repetible, convé fixar una entrada local autoritzada o conservar una petició prou precisa juntament amb la data i les propietats de la resposta. Si només existeix un servei de visualització, cal declarar que el context depèn del servidor i que no constitueix una entrada analítica. Per al treball sense connexió, una prova prèvia ha de confirmar quines capes continuen disponibles i quines quedaran absents.

## Repositoris i catàlegs: de l'àmbit global al local

Un servei respon una petició en el moment de la consulta; un repositori o un centre de descàrregues permet obtenir i conservar una còpia d'un producte. Un catàleg ajuda a descobrir-lo i a llegir-ne la fitxa, però no és necessàriament el productor ni el lloc on resideix el fitxer. Després d'entendre què pot retornar cada geoservei, convé ordenar on buscar una còpia segons l'escala de la pregunta.

::: table "Punts de cerca segons l'àmbit territorial"
| Àmbit | Repositoris, catàlegs o productors útils | Ús inicial i control principal |
| --- | --- | --- |
| Global | [Natural Earth](https://www.naturalearthdata.com/) i [OpenStreetMap](https://www.openstreetmap.org/about) | Context mundial o xarxa col·laborativa; comprovar escala, autoria i llicència |
| Europeu | [GISCO](https://ec.europa.eu/eurostat/web/gisco/geodata) i [Copernicus Data Space](https://dataspace.copernicus.eu/) | Regions harmonitzades o observació de la Terra; comprovar versió territorial, data, resolució i processament |
| Estatal | [IGN/CNIG](https://centrodedescargas.cnig.es/) i [Cadastre INSPIRE](https://www.catastro.hacienda.gob.es/webinspire/index.html) | Cartografia de referència, ortofotos, relleu, límits o parcel·les; distingir finalitat, escala i producte |
| Català | [Hipermapa](https://sig.gencat.cat/visors/hipermapa.html), [ICGC](https://www.icgc.cat/ca/Geoinformacio-i-mapes) i [Dades Obertes de la Generalitat](https://dadesobertes.gencat.cat/) | Descoberta de capes, productes cartogràfics i registres administratius; seguir cada resultat fins al productor, el producte i la data |
| Local | Geoportals i portals de dades obertes municipals | Barris, equipaments, planejament o serveis; comprovar cobertura, comparabilitat i drets de reutilització |
:::

### Àmbits global i europeu

[Natural Earth](https://www.naturalearthdata.com/) distribueix cartografia mundial generalitzada a escales 1:10.000.000, 1:50.000.000 i 1:110.000.000 i la declara de domini públic. És adequada per situar països, costes o grans xarxes en mapes de petita escala, no per delimitar un municipi o una frontera jurídica amb detall. [OpenStreetMap](https://www.openstreetmap.org/about) ofereix una base geogràfica col·laborativa molt més detallada en molts llocs, però la cobertura i actualització varien i la seva Open Database License imposa condicions pròpies.

En l'àmbit europeu, [GISCO](https://ec.europa.eu/eurostat/web/gisco/geodata) distribueix geometries compatibles amb classificacions estadístiques com NUTS, en diverses escales i CRS; cal conservar la versió territorial i les condicions de cada família. [Copernicus Data Space](https://dataspace.copernicus.eu/) permet descobrir i obtenir imatges Sentinel i altres productes d'observació de la Terra. La missió, la data de captació, els núvols, la resolució i el nivell de processament formen part de la selecció: «Copernicus» encara no identifica una entrada concreta.

### CNIG i IGN

La portada del Centro de Descargas és el punt de descoberta: permet cercar i recórrer el catàleg, però encara no identifica per si sola cap fitxer ni capa del projecte.

![Portada del Centro de Descargas del CNIG amb el catàleg, el cercador general i l'accés a la cerca sobre el mapa]({{ site.baseurl }}/assets/img/cnig/centro-descargas-cnig.png "Portada del portal oficial consultada el 8 de setembre de 2026. El cercador serveix per descobrir productes; la dada utilitzada s'ha d'identificar després a la fitxa i al recurs concret. Font: IGN/CNIG."){: data-figure-width-web="52rem" data-figure-width-pdf="100%"}

El [Centro de Descargas del CNIG](https://centrodedescargas.cnig.es/) organitza l'accés per productes cartogràfics i àmbits. Abans de descarregar cal obrir la fitxa del producte i identificar el contingut, l'escala o resolució, la data o edició, els formats, el CRS, la llicència i la unitat de distribució. Després es selecciona l'àrea necessària, que pot correspondre a un full, un municipi, una província o una altra divisió segons el producte. El paquet rebut i la fitxa no s'han de separar: el nom del `.zip` rarament explica tot el que conté. El capítol següent aplicarà aquest itinerari al producte d'unitats administratives.

L'IGN i el CNIG també publiquen serveis de visualització i descàrrega. El PNOA, per exemple, es pot explorar mitjançant el WMS i el document de capacitats presentats més amunt. El servei és compost i dependent de l'escala: cal registrar quina capa o cobertura s'ha observat i a quina escala. La imatge és adequada per revisar visualment l'entorn i la data s'ha de recuperar de les metadades de la capa o campanya. Si la pregunta exigeix valors ràster, bandes o treball fora de línia, cal cercar el producte descarregable corresponent en lloc d'exportar una imatge del WMS.

El control després d'una descàrrega inclou conservar el paquet original, llegir qualsevol document o fitxer de metadades, descomprimir en una ubicació separada i inventariar les capes. A QGIS s'han de revisar extensió, CRS, geometria o dimensions, camps o bandes i correspondència amb la unitat anunciada. No s'ha de triar el primer fitxer que s'obre si el paquet conté versions, fulls o nivells de detall diferents.

### ICGC

La secció de [Geoinformació i mapes de l'ICGC](https://www.icgc.cat/ca/Geoinformacio-i-mapes) diferencia dades i productes, geoinformació en línia, mapes i eines. Per a una ortofoto, la [fitxa d'Ortofoto Territorial](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Imatge/Ortofoto-Territorial) descriu el producte; el [visor de descàrregues](https://visors.icgc.cat/appdownloads/) permet escollir sèrie, àrea i format; i la pàgina del [WMS Ortofoto Territorial](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Geoinformacio-en-linia-Geoserveis/WMS-Ortoimatges/WMS-Ortofoto-Territorial) documenta la via de visualització. L'Hipermapa pot ajudar a descobrir capes de l'ICGC o d'altres organismes, però continua sent un agregador: la identificació de la font s'ha de completar a la fitxa del productor. Són destinacions relacionades, però no intercanviables.

![Visor de descàrregues de l'ICGC amb una àrea de l'entorn de la Facultat, la família Ortoimatges, l'Ortofoto Territorial de 25 cm, els formats i la previsualització identificables]({{ site.baseurl }}/assets/img/icgc/visor-descarregues-icgc.png "Visor oficial consultat el 9 de setembre de 2026. La seqüència visible és seleccionar l'àrea, identificar el producte i la resolució, escollir un format i previsualitzar abans de descarregar. La disponibilitat i l'edició concreta s'han de comprovar a la fitxa vigent. Font: ICGC."){: data-figure-width-web="56rem" data-figure-width-pdf="100%"}

La captura mostra per què «baixar l'ortofoto» encara no és una especificació suficient. Cal definir l'àmbit, distingir les sèries locals i territorials, triar la resolució compatible amb la pregunta i seleccionar un format que conservi la georeferenciació necessària. La previsualització confirma cobertura i aparença, però la fitxa del producte és la que permet interpretar edició, resolució, qualitat i condicions d'ús. El paquet descarregat s'ha d'inventariar després; prémer **Descarregar** no valida el contingut.

Per orientar el llenç o contrastar una capa, un servei de mapa base o d'ortofoto de l'ICGC pot ser suficient. Si el producte ofereix diverses escales o resolucions, no s'ha de triar la més detallada per inèrcia: el nivell adequat depèn de l'extensió, de l'objecte que cal distingir i de la qualitat declarada. La primera micropràctica compararà dues representacions oficials del municipi: les divisions administratives 1:5.000 accessibles des d'Open ICGC i les unitats administratives del CNIG. Que totes dues siguin oficials no implica que comparteixin escala, esquema, format o CRS.

### Cadastre

La Direcció General del Cadastre publica un [punt d'accés als conjunts i serveis INSPIRE](https://www.catastro.hacienda.gob.es/webinspire/index.html) que diferencia parcel·les cadastrals, adreces i edificis i permet descobrir-ne les vies de visualització, consulta o descàrrega {% cite direccionGeneralCatastroServiciosINSPIRE %}. El WMS retorna una representació, el WFS permet consultar objectes dins dels límits anunciats i els feeds ATOM enllacen conjunts predefinits descarregables. El portal és el punt d'entrada; la font continua sent el producte cadastral concret i la resposta efectiva depèn del servei utilitzat.

![Secció de descàrrega del portal INSPIRE del Cadastre amb els serveis WFS i els feeds ATOM de parcel·les, adreces i edificis]({{ site.baseurl }}/assets/img/cadastre/serveis-descarrega-inspire.png "El portal oficial separa la consulta d'objectes mitjançant WFS de la descàrrega de conjunts predefinits mitjançant ATOM. La pàgina és un punt de descoberta: encara cal seguir els enllaços i llegir les metadades del servei i del conjunt. Captura del 9 de setembre de 2026. Font: Direcció General del Cadastre."){: data-figure-width-web="56rem" data-figure-width-pdf="100%"}

La cartografia cadastral té una finalitat administrativa i fiscal concreta. No s'ha de presentar automàticament com a Registre de la Propietat, aixecament topogràfic de límits jurídics o planejament urbanístic. Una parcel·la visible pot ser molt útil com a unitat geomètrica de consulta, però qualsevol conclusió sobre titularitat, dret edificatori, propietat o delimitació legal exigeix les fonts i els procediments competents.

El complement de tercers [Spanish Inspire Catastral Downloader](https://plugins.qgis.org/plugins/Spanish_Inspire_Catastral_Downloader/) facilita a QGIS la descàrrega de parcel·les, edificis i adreces mitjançant el servei ATOM. El complement no crea les dades ni substitueix els feeds oficials: depèn del seu esquema, de la xarxa i de la compatibilitat de la versió instal·lada. Si falla, la traça manual del feed permet distingir una incidència del complement d'un canvi al servei o d'una entrada municipal inexistent.

![Menú Complements de QGIS amb l'entrada Spanish Inspire Catastral Downloader identificada]({{ site.baseurl }}/assets/img/qgis/qgis-cadastre-plugin-menu.png "El complement instal·lat ofereix una entrada convenient dins de QGIS 3.44.11. La captura no acredita una descàrrega correcta: la font continua sent la Direcció General del Cadastre i cal validar el feed ATOM i el paquet retornat."){: data-figure-width-web="44rem" data-figure-width-pdf="88%"}

Un feed ATOM és un document XML que enllaça altres feeds o fitxers. No cal inventar l'adreça final ni copiar-la d'un tutorial. El recorregut manual verificat per a les parcel·les de Vila-seca és el següent:

1. Obrir el [feed general de parcel·les cadastrals](https://www.catastro.hacienda.gob.es/INSPIRE/CadastralParcels/ES.SDGC.CP.atom.xml) des de la secció ATOM oficial i identificar-ne `title`, `updated`, `rights` i els elements `link`.
2. Cercar l'entrada `Territorial office 43 Tarragona` i seguir el seu `link rel="enclosure"` fins al [feed territorial de Tarragona](https://www.catastro.hacienda.gob.es/INSPIRE/CadastralParcels/43/ES.SDGC.CP.atom_43.xml). El `43` identifica aquí l'oficina territorial anunciada pel mateix feed.
3. Dins del feed de Tarragona, cercar el títol `43173-VILA SECA Cadastral Parcels` i comprovar que l'enllaç de descàrrega apunta al [paquet municipal `A.ES.SDGC.CP.43173.zip`](https://www.catastro.hacienda.gob.es/INSPIRE/CadastralParcels/43/43173-VILA%20SECA/A.ES.SDGC.CP.43173.zip).
4. Abans de tractar el ZIP com una entrada, registrar la data `updated`, les condicions indicades, el CRS anunciat, l'extensió i el vincle de metadades; després cal conservar el paquet i validar-ne el contingut com qualsevol altra descàrrega.

El codi s'ha de llegir dins del contracte del productor. A l'objecte administratiu del CNIG, `nationalcode` val `34094343171`; el sufix territorial `43171` identifica Vila-seca en aquell esquema. Al feed ATOM cadastral consultat el 15 de setembre de 2026, en canvi, `43171` correspon a Vilaplana i Vila-seca apareix com `43173`. Aquesta diferència observada impedeix reutilitzar un codi d'una font com si fos una clau universal. Una unió entre productes exigeix una correspondència documentada per a les versions concretes, no només cinc dígits amb una aparença compatible.

### Fonts locals

Quan la pregunta baixa del municipi al barri, al carrer, a l'equipament o al planejament, una font local pot aportar un detall que les cobertures estatals o catalanes no contenen. El [Geoportal de Reus](https://geoportal.reus.cat/inici/serveis.html), el [portal de dades obertes de Reus](https://opendata.reus.cat/) i l'espai [TGN Dades](https://www.tarragona.cat/governobert/tgn-dades) són punts de descoberta pròxims al territori del curs. La seva proximitat no els fa intercanviables: una capa de barris, una base topogràfica municipal i un indicador d'un quadre de comandament tenen unitats, dates, llicències i vies d'accés diferents.

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

El tercer bloc descriu la representació i la qualitat. En vector interessa el tipus de geometria, la unitat mínima cartografiada, el criteri de generalització, la completesa, la coherència topològica i l'exactitud posicional i temàtica declarades. En ràster cal afegir mida de cel·la, bandes, tipus de valor, valor sense dades (`NoData`), nivell de processament i, quan correspongui, resolució radiomètrica o temporal. El capítol 03, sobre estructura, formats i referenciació, desenvoluparà aquestes propietats; en aquesta fase importa comprovar que existeixen i s'ajusten a la pregunta.

#### Exemple real: els auxiliars d'una descàrrega del CNIG

La fitxa de [Límites municipales, provinciales y autonómicos](https://centrodedescargas.cnig.es/CentroDescargas/limites-municipales-provinciales-autonomicos) ofereix més d'una distribució. La primera micropràctica utilitzarà concretament la [distribució GML `LINEAS_LIMITE_GML.ZIP`](https://centrodedescargas.cnig.es/CentroDescargas/detalleArchivo?sec=12408588), publicada el 10 d'agost de 2026, que inclou els objectes `AdministrativeUnit` i `AdministrativeBoundary` i `readme.txt`. La fitxa declara coordenades geogràfiques ETRS89 per a la Península, que corresponen a `EPSG:4258`; dins del paquet caldrà seleccionar les unitats administratives municipals de quart ordre. La distribució Shapefile `LINEAS_LIMITE.ZIP`, publicada el 28 de juliol de 2026, inclou les geometries, un PDF explicatiu i `20190208MetadatosDivisionesAdministrativas.xml`. No hi ha un únic ZIP actual que contingui tots dos auxiliars.

El fragment següent prové de l'XML inclòs al ZIP Shapefile, no de la distribució GML triada per a la micropràctica. Les etiquetes `gmd` estructuren els elements de metadades i les etiquetes `gco` contenen valors. Amb poques línies ja es poden recuperar identificador, productor, data del registre, títol, un CRS documentat, llicència i escala:

::: listing "Fragments de les metadades XML incloses amb els límits administratius"
```xml
<gmd:fileIdentifier>
  <gco:CharacterString>spaignLLM2013</gco:CharacterString>
</gmd:fileIdentifier>
<gmd:organisationName>
  <gco:CharacterString>Instituto Geográfico Nacional</gco:CharacterString>
</gmd:organisationName>
<gmd:dateStamp>
  <gco:Date>2019-02-01</gco:Date>
</gmd:dateStamp>
<gmd:title>
  <gco:CharacterString>Base de Datos de Divisiones Administrativas de España</gco:CharacterString>
</gmd:title>
<gmd:code>
  <gco:CharacterString>http://www.opengis.net/def/crs/EPSG/0/25831</gco:CharacterString>
</gmd:code>
<gmd:otherConstraints>
  <gco:CharacterString>CC BY 4.0 http://www.ign.es</gco:CharacterString>
</gmd:otherConstraints>
<gmd:denominator>
  <gco:Integer>25000</gco:Integer>
</gmd:denominator>
```
:::

L'XML complet també adverteix que, amb caràcter general, la geometria té una incertesa d'uns `40 m` i que alguns trams poden ser provisionals. Aquesta informació impedeix usar el producte com si fos un aixecament cadastral o una delimitació local de precisió. El `readme.txt` del ZIP GML compleix una altra funció, més pròxima a un inventari:

::: listing "Estructura resumida al readme del paquet GML"
```filetree
AdministrativeBoundary
  1stOrder: fronteres estatals
  2ndOrder: comunitats autònomes
  3rdOrder: províncies
  4thOrder: municipis
AdministrativeUnit
  1stOrder: país
  2ndOrder: comunitats autònomes
  3rdOrder: províncies
  4thOrder: municipis
Cada fitxer .gml conté com a màxim 10.000 entitats.
```
:::

El contrast temporal i entre distribucions és una comprovació en si mateix: el paquet Shapefile és de 2026, però l'XML que incorpora té data de 2019 i el fragment mostra `EPSG:25831`, mentre que la fitxa actual descriu coordenades geogràfiques ETRS89. Aquest XML s'ha de conservar perquè documenta allò rebut, però no permet atribuir el seu CRS a la distribució GML. El [registre normalitzat vigent del catàleg IDEE](https://www.idee.es/csw-codsi-idee/srv/api/records/spaignLLM/formatters/xml) declara una revisió del producte de `2026-02-12`, identifica l'IGN com a propietari i el CNIG com a distribuïdor, i manté l'escala 1:25.000 i la llicència CC BY 4.0. A la micropràctica, la prova decisiva serà comprovar a QGIS que la capa `AdministrativeUnit` municipal del GML declara `EPSG:4258` abans de transformar-la.

Les metadades no converteixen automàticament una font en adequada. Són evidència per prendre una decisió i també poden revelar un límit. Si un producte declara una escala de producció incompatible amb el detall demanat, no s'ha de compensar ampliant el zoom. Si no informa de la data o del criteri de cobertura, aquesta absència s'ha de registrar i pot obligar a cercar una altra font. «Sense informació» no és equivalent a «sense error».

### Qualitat relativa a l'ús

L'avaluació es pot formular com una correspondència entre requisit i evidència. Si la pregunta exigeix distingir voreres, cal una unitat espacial i una exactitud compatibles amb aquest objecte. Si exigeix comparar dos anys, calen dates de referència i mètodes prou consistents. Si exigeix unir estadístiques municipals, la geometria ha de conservar el codi territorial correcte per al mateix marc administratiu. Cada requisit ha de tenir una propietat observable o una limitació explícita.

La inspecció visual és necessària però insuficient. Una capa pot superposar-se bé a una ortofoto i contenir identificadors duplicats; un ràster pot semblar continu i tenir valors `NoData` codificats com a zero; un WMS pot mostrar parcel·les nítides sense proporcionar-ne cap geometria. Els controls han de combinar metadades, esquema, recompte, rangs, valors absents, extensió i contrast espacial. Encara no cal executar tota l'anàlisi, però sí descartar una entrada que no pugui superar aquests controls inicials.

Quan dues fonts discrepen, no s'ha de triar automàticament la que sembla més detallada. Cal comprovar si representen el mateix fenomen, data i definició. Un eix viari no ha de coincidir exactament amb el centre visible de totes les calçades; un límit administratiu i una tanca física poden respondre realitats diferents; una petjada cadastral i una coberta observada en ortofoto poden tenir dates i finalitats distintes. La discrepància pot ser un error, però també informació sobre els models comparats.

## Incorporació inicial a QGIS

Carregar una font a QGIS és una primera inspecció, no una validació completa. Cal revisar l'extensió, el nombre d'entitats o les dimensions del ràster, el CRS declarat, els camps o bandes, els valors absents i la coherència visual amb una capa de referència. Si una capa apareix en un lloc inesperat, no s'ha d'assignar un CRS a l'atzar per fer-la coincidir: primer cal esbrinar què signifiquen les coordenades originals.

Les connexions remotes són útils per explorar. Quan una activitat requereix transformar dades o conservar exactament l'entrada, convé descarregar una còpia autoritzada i registrar-ne la versió. Les dades originals del projecte es mantindran sense modificacions; les seleccions, conversions i retalls es desaran com a dades preparades o derivades.

La connexió directa evita dependre d'un complement i fa visible quin tipus de servei s'està utilitzant. A QGIS 3.44 en català, el recorregut general es pot fer des de `Capa > Afegeix una capa` o des del `Gestor de fonts de dades`; el panell `Explorador` ofereix les mateixes famílies de connexió. La disposició pot variar segons el perfil, però la diferència funcional entre `WMS/WMTS` i `WFS / OGC API - Features` es manté {% cite qgisUserGuide344 %}.

Per a un WMS o WMTS, el flux de connexió és el següent:

1. Localitzar a la pàgina oficial l'adreça del servei i la fitxa del producte; no s'ha de copiar una URL d'un projecte aliè sense saber-ne el productor.
2. Obrir la font `WMS/WMTS`, crear una connexió i donar-li un nom que identifiqui organisme, producte i funció, com `ign_pnoa_context` o `icgc_ortofoto_context`.
3. Introduir l'adreça base publicada. Les opcions d'autenticació només s'han de configurar si el servei les exigeix, i les credencials no s'han d'escriure al diari ni al nom de la connexió.
4. Prémer **Connecta** perquè QGIS llegeixi `GetCapabilities`, desplegar la jerarquia i seleccionar la capa concreta, no el grup genèric si no és el que demana el cas.
5. Revisar els CRS, el format d'imatge, la transparència i, en WMTS, la matriu disponible. L'elecció s'ha de basar en la compatibilitat amb el projecte i l'ús visual previst.
6. Afegir la capa, obrir-ne `Propietats > Informació` i registrar títol, font, tipus de servei, CRS, extensió, atribució i data de consulta.

En QGIS, la distinció entre portal, servei i capa es tradueix en tres comprovacions visibles: triar la família de connexió adequada, identificar l'adreça oficial desada i consultar les capacitats abans de seleccionar cap capa.

![Gestor de fonts de dades de QGIS amb la família WMS/WMTS, el botó per crear una connexió i el control Connecta identificats]({{ site.baseurl }}/assets/img/qgis/qgis-web-service-connection.png "La captura mostra on es crea o se selecciona una connexió WMS/WMTS i des d'on se'n consulten les capacitats. El panell buit no mostra cap URL desada ni una resposta del servidor; l'adreça oficial i el GetCapabilities s'han de verificar separadament."){: data-figure-width-web="52rem" data-figure-width-pdf="100%"}

La validació no acaba quan el mapa apareix. Cal navegar a una posició coneguda, comparar-la amb una capa vectorial de referència, observar el comportament a diverses escales i provar **Identifica**. Un resultat correcte és que la capa cobreixi l'àmbit declarat, mantingui la posició esperada i es comporti com el tipus de resposta documentat. Si no hi ha taula ni selecció vectorial, aquesta absència confirma que el recurs s'ha de conservar com a context, no com a entrada de geoprocessament.

Per a un WFS, es crea una connexió a la família corresponent, es consulta la llista de tipus d'entitat i se selecciona només el necessari. Si QGIS ofereix limitar la petició a l'extensió actual o aplicar un filtre, convé reduir primer l'àmbit per evitar una consulta massiva. Després de carregar la capa s'han de comprovar la taula, el tipus geomètric, l'esquema, el CRS, l'extensió i si el nombre recuperat ha estat limitat. Una advertència de truncament o paginació forma part del resultat de la prova i s'ha de resoldre abans d'analitzar.

Quan una consulta vectorial remota es converteix en entrada estable, `Exporta > Desa els objectes com a...` permet crear una còpia local en un format adequat, sempre que la llicència ho autoritzi. El nom i el diari han d'indicar que es tracta d'una extracció, amb la font, la data, el filtre i el CRS de sortida. L'exportació no s'ha de fer sobre el paquet original ni confondre amb una nova font independent.

Les descàrregues s'incorporen amb el gestor vectorial o ràster segons el contingut, no segons el nom comercial del producte. Abans d'afegir-les convé haver descomprimit el paquet i haver identificat el fitxer principal i els auxiliars. Si QGIS mostra diverses subcapes dins d'un GeoPackage, cal seleccionar-les pel nom i la descripció, no carregar-les totes per defecte. El capítol següent establirà on es conserva cada estat del fitxer.

## Exploració inicial de fonts

El primer contacte amb les fonts no produeix encara cap capa de treball. A l'aula, Vila-seca permet comparar quatre portes d'entrada: una cerca general a Internet, l'Hipermapa com a agregador territorial, les pàgines dels organismes productors i els connectors Open ICGC i QuickMapServices dins de QGIS. Cada estudiant pot repetir l'exploració sobre el municipi assignat, però no ha de descarregar ni transformar cap conjunt en aquest capítol.

L'exploració ha de permetre reconèixer dues funcions diferents. L'Ortofoto Territorial de 2025 de l'ICGC serà el context visual de la primera micropràctica, mentre que les divisions administratives 1:5.000 d'Open ICGC i les unitats administratives del CNIG seran candidates vectorials. En aquest punt només cal localitzar-ne la fitxa o l'accés i observar quina informació permet distingir productor, producte, capa i via d'accés.

Els connectors faciliten la cerca, però no converteixen el catàleg que mostren en productor. Quan una capa descoberta amb Open ICGC o QuickMapServices resulta pertinent, cal seguir-ne la informació fins a l'organisme responsable i comprovar el tipus de servei, la data, l'escala o resolució, el CRS, la llicència i l'atribució. El capítol següent iniciarà el projecte i conservarà les primeres dades.

## Activitats

### Cerca guiada en portals i visors

Cal formular una pregunta senzilla sobre el municipi assignat i cercar tres recursos que hi puguin contribuir. La cerca combinarà Internet, l'Hipermapa i almenys una pàgina d'un organisme productor. Per a cada resultat cal identificar provisionalment si es tracta d'un portal, un visor, una fitxa de producte, una descàrrega o un servei, i seguir l'enllaç fins al productor quan sigui possible.

L'activitat és exploratòria: no cal descarregar paquets, crear cap projecte ni preparar cap capa. La comprovació consisteix a poder explicar quina informació aportaria cada recurs i quina dada o metadada encara faltaria abans d'utilitzar-lo en una anàlisi.

### Exploració amb Open ICGC i QuickMapServices

Des de `Complements > Gestiona i instal·la complements` es poden localitzar Open ICGC i QuickMapServices. Cal explorar com organitzen els recursos i comparar una capa descoberta amb la seva pàgina o servei oficial. La comparació ha de distingir el connector, el productor, el producte, el tipus d'accés i les condicions d'ús.

També es poden provar les adreces oficials de serveis presentades al capítol i observar què anuncia `GetCapabilities` o què mostra QGIS. No cal conservar cap descàrrega ni seguir encara cap procés d'obtenció de dades. El projecte de la primera micropràctica començarà al capítol següent amb les fonts ja identificades.

### Traça d'una descàrrega cadastral ATOM

Cal reconstruir la ruta des del portal INSPIRE fins a un paquet municipal sense començar per l'adreça final. Primer es reprodueix la traça controlada de Vila-seca; després se segueix el mateix procediment fins al municipi assignat, si el feed el publica. L'evidència ha d'identificar el feed general, l'entrada territorial, el feed de l'oficina, el títol municipal, el `link rel="enclosure"`, la data `updated`, els drets i el CRS anunciat.

La comprovació final compara el codi cadastral amb els identificadors de les fonts administratives ja localitzades. Si no coincideixen, la diferència es conserva i s'investiga; no s'ha de corregir cap codi només perquè un altre organisme utilitza una clau semblant. Es pot repetir la descoberta amb el complement, però el resultat s'ha de poder explicar a partir dels feeds oficials.
