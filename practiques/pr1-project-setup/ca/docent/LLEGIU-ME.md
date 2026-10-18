---
title: "PR1 · Guia docent del projecte municipal i del mapa"
lang: ca
recipient: docent
content_status: approved
subject: "Tecnologies de la Informació Geogràfica"
subject_code: "21234114"
author: "Benito Zaragozí"
institution: "Universitat Rovira i Virgili"
---

# Finalitat i resultats d’aprenentatge

PR1 treballa la selecció municipal, el GeoPackage, els projectes i la documentació. La micropràctica Moodle confirmada el 18 d’octubre de 2026 en delimita els requisits avaluats. El recorregut ampliat d’aquesta guia utilitza descàrrega CNIG, preparació mètrica i composició per establir una base de continuïtat del curs.

La composició recupera escala, jerarquia visual, llegenda, etiquetes i comunicació cartogràfica treballades a TIGIT. És un resultat del recorregut ampliat i una **ampliació opcional de la micropràctica Moodle**.

Vila-seca és el cas de demostració. La micropràctica permet escollir el municipi i utilitzar una font de límits adequada; no fixa CNIG, un EPSG ni un PDF cartogràfic separat. Un únic PDF d’apunts satisfà el tipus documental obligatori. La pauta de noms s’obté del que s’ha comunicat a classe, no del nom dels fitxers d’exemple.

La definició de revisió és `tig/pr1-moodle`, edició `moodle-confirmed-2026-10-18`. Els seus fitxers importats són immutables. Les comprovacions del cas CNIG que segueixen ajuden a preparar el laboratori, però no afegeixen requisits a aquella edició ni substitueixen la rúbrica confirmada.

# Preparació i conducció de la sessió

Les durades corresponen al recorregut ampliat amb un municipi i una composició, QGIS instal·lat i nocions prèvies de capes i mapes. Són estimacions pendents de contrast amb una classe. Les esperes de descàrrega, instal·lació i ampliacions poden augmentar el temps; la composició es pot continuar en una segona sessió.

| Component | Durada orientativa |
| --- | --- |
| Aula, projecte i composició | 120–150 min |
| Treball autònom i apunts | 90–150 min |
| Preparació docent | 30–45 min |

Table: Estimació del recorregut ampliat PR1 amb un municipi i una composició.

Abans de classe es comproven portal, WMS, originals i obertura del cas docent. Convé preparar una còpia per a la demostració i comprovar el municipi escollit per cada estudiant. La seqüència té tres aturades: identitat i CRS de la font, entitat exportada i doble reobertura amb composició. A cada aturada es demana quina dada s’ha desat i on; la resposta permet distingir una selecció visible d’un resultat persistent.

# Preparar Moodle

1. Crear una **Tasca** amb el nom **PR1 · Micropràctica del projecte municipal**.
2. Copiar a **Descripció** l’enunciat següent, fins al final de «Qualificació». Recollir-hi la pauta de noms realment comunicada a classe. L’edició confirmada manté el mapa i la composició com a ampliacions.
3. Adjuntar a **Fitxers addicionals** el PDF d’alumnat, assenyalant-ne la secció d’abast. El cas CNIG de Vila-seca, si es comparteix, és un exemple ampliat amb les dependències comprovades.
4. Fixar dates, forma de tramesa i límit de mida. La rúbrica d’Unaltramesa usa 100 punts, distribuïts en 70/20/10; la conversió a una nota sobre 10 és 7/2/1. Cal conservar els tres blocs sense subpesos ni quotes per ampliació.
5. Desar i revisar la **vista d’estudiant**, els enllaços i l’adjunt. La guia i el paquet docent serveixen per preparar la sessió; la pujada efectiva correspon al professorat.

## Enunciat per copiar a la descripció

**Dades i objectiu.** Cal crear un projecte QGIS sobre un municipi escollit. El terme s’ha de seleccionar a partir d’una capa de límits municipals adequada, exportar al GeoPackage i carregar des d’aquest fitxer. El projecte ha de contenir una capa cartogràfica carregada mitjançant WMS.

**Treball bàsic —70%.** El lliurament inclou un GeoPackage amb el terme municipal i el projecte QGIS incrustat, una còpia externa `.qgz` i uns apunts breus en PDF. Cal seguir les pautes de noms indicades a classe i comprovar que el projecte s’obre, les capes necessàries estan disponibles i les rutes funcionen. La guia descriu també un recorregut CNIG ampliat; aquella font, l’EPSG i la composició del cas no són requisits addicionals d’aquesta micropràctica.

**Ampliacions —20%.** Es valoren millores funcionals i pertinents: altres serveis WMS, capes vectorials, simbologies, etiquetes, grups, mapes o composicions. Algunes preguntes orientatives són:

- Quina informació afegeix un segon WMS o una capa local? Identificar font, cobertura i funció i comprovar que es pot recuperar al projecte.
- Com milloren la lectura la simbologia, les etiquetes o els grups? Justificar la configuració i contrastar-la amb les dades i l’escala de treball.
- Què aporta una composició municipal? Preparar un mapa amb elements llegibles i comprovar que continua editable després de desar i reobrir el projecte.

No cal reunir tots els tipus d’ampliació. L’existència d’una capa o una composició no n’acredita tota sola la funcionalitat; cal explicar què aporta i comprovar-la.

**Documentació i lliurament —10%.** Els apunts han de servir per repassar i repetir el procediment: passos importants, decisions, comprovacions i problemes, amb explicacions i captures llegibles. Un únic PDF d’apunts satisfà el requisit documental; els fitxers addicionals s’identifiquen pel seu paper. El conjunt conserva les dependències necessàries i segueix la nomenclatura comunicada a classe.

**Qualificació.** Es valoren globalment els tres blocs: **70%** realització correcta dels requisits imprescindibles, **20%** ampliacions funcionals i **10%** qualitat dels apunts, captures, presentació i organització. Equivalen a màxims de **7, 2 i 1 punts** sobre 10, sense subpesos fixos. El primer WMS i el municipi pertanyen al bàsic; les ampliacions no els substitueixen ni es puntuen dues vegades. La documentació també pot augmentar la nota sobre el bloc bàsic.

# Dades del recorregut ampliat CNIG

La font vectorial és [Límites y Unidades Administrativas Actuales](https://centrodedescargas.cnig.es/CentroDescargas/detalleArchivo?sec=9000029), del Centre de Descàrregues del CNIG. El cas de referència conserva `LINEAS_LIMITE.ZIP`, edició de **28/07/2026**, amb metadades i document de lectura. Cal disposar de la descàrrega original completa per mostrar com s’identifica i s’extreu la capa de recintes.

El fitxer `recintos_municipales_inspire_peninbal_etrs89.shp` conté les geometries dels recintes del cas de referència.

La inspecció de la distribució retinguda observa **8.132 recintes**, amb codis únics i geometries vàlides, en **ETRS89, EPSG:4258**. El recompte és una referència d’aquesta edició, no un valor que s’hagi d’imposar a una descàrrega posterior. La selecció de recintes amb `CODNUT2` igual a `ES51` retorna 948 registres. Inclou la unitat singular `Comunidad de El Pont de Bar y Cava`.

| Dada del cas Vila-seca | Valor observat | Funció |
| --- | --- | --- |
| `NAMEUNIT` | Vila-seca | Contrast del nom |
| `NATCODE` | `34094343171` | Identificador de la selecció, conservat com a text |
| `CODNUT3` | `ES514` | Referència provincial de la font |
| CRS original | EPSG:4258 | Coordenades geogràfiques de la descàrrega |
| CRS de sortida | EPSG:25831 | Coordenades en metres del límit de treball |

Table: Referències de la font que es comproven durant la demostració.

El context es consulta al WMS oficial IGN/PNOA, URL `https://www.ign.es/wms-inspire/pnoa-ma?`, capa `OI.OrthoimageCoverage`. Cal distingir la data d’accés de la data de la imatge i consultar les metadades de la zona. La capa `OI.MosaicElement` permet consultar data i resolució; una resposta puntual no acredita tota una extensió.

# Materials docents i exemple resolt

El paquet de suport al professorat ha de permetre repetir la demostració i contrastar els resultats. Els originals, les preparacions i el projecte resolt mantenen funcions identificables:

| Material docent | Contingut i ús |
| --- | --- |
| Originals | ZIP CNIG conservat íntegre, metadades, llicència i registre de descàrrega |
| Capa extreta | Components complets del Shapefile per mostrar la inspecció i la selecció |
| Preparacions | Derivats identificats, amb operacions, CRS i procedència explícits |
| Cas resolt | GeoPackage municipal, `pr1` incrustat i `.qgz` homònim reobribles |
| Composició | Mapa municipal editable i PDF revisat amb llegenda, escala, fonts i autoria |
| Guia i controls | Seqüència de demostració, valors de referència i diagnòstic d’errors |

Table: Contingut funcional del material de suport al professorat.

Un estat inicial preparat pot servir al professorat per reprendre la demostració. El recorregut ampliat de l’alumnat comença amb el PDF d’instruccions i la descàrrega pròpia al portal. La cerca del producte, la conservació dels originals i la preparació del GeoPackage són resultats d’aprenentatge d’aquesta via.

El cas resolt de Vila-seca es pot compartir com a **exemple del resultat esperat**, amb el projecte i el mapa clarament identificats. Aquesta consulta permet comentar decisions i controls; cada estudiant construeix el projecte i la composició del seu municipi a partir de les dades que ha obtingut.

Els projectes d’exemple es conserven en una carpeta separada del treball propi. Si el material docent inclou un extracte local de context, s’identifiquen servei, petició, extensió, CRS, mida de píxel i data de consulta. Una imatge WMS retinguda és un derivat de visualització; el seu detall no es presenta com el d’una descàrrega original d’ortofoto.

# Demostració del recorregut ampliat

La demostració conserva tres estats comprovables: la font original descarregada, el municipi exportat i el projecte reobert amb la composició. Els controls es fan en cada estat per poder localitzar en quin pas apareix una incidència.

## Mostrar l’obtenció i la lectura dels originals

La sessió comença al catàleg del CNIG, dins d’**Información geográfica de referencia > Límites municipales, provinciales y autonómicos**. Es llegeix la fitxa abans de descarregar: productor, edició, cobertura, format, sistema de referència i condicions d’ús. Es mostra el botó de descàrrega i el registre de l’arxiu original a `data/raw/`.

L’extracció conserva el ZIP i tots els components de la capa. Cal fer visible la diferència entre línies de límit i recintes, i entre un Shapefile complet i el fitxer `.shp` aïllat. Després es crea un projecte nou, s’hi carrega la capa de recintes i es comproven les propietats i els camps `NAMEUNIT` i `NATCODE`.

La connexió PNOA es crea al **Gestor de fonts de dades > WMS/WMTS**, amb l’URL oficial i la capa d’ortofoto. Es representa sota un contorn municipal visible. Cal explicar què és local, què depèn de xarxa i per què el servei mostra satèl·lit o ortofoto segons l’escala.

## Fer observable la selecció i l’exportació

La seqüència comença amb el municipi visible sobre l’ortofoto i les dues funcions identificades al panell de capes: imatge de context i vector seleccionable. Es comprova el codi de Vila-seca a la taula i es mostra la diferència entre el total de la font i la selecció d’una entitat.

Cal obrir realment el menú contextual i el diàleg d’exportació. El diàleg ha de mostrar GeoPackage, destinació a `sandbox/`, nom de capa, només seleccionats i EPSG:25831. El resultat s’afegeix al mapa i es reobre des del contenidor. El diàleg configurat és una evidència diferent de la capa efectivament desada.

El projecte es representa en EPSG:25831 mentre la font conserva EPSG:4258. L’exportació de la selecció a `municipi_treball`, amb sortida EPSG:25831, transforma efectivament les coordenades. Cal contrastar aquesta operació amb assignar un CRS o canviar només el de visualització.

## Fer observable el desament del projecte

Es crea la connexió GeoPackage a l’Explorador, es desa `pr1` amb **Projecte > Desa a > GeoPackage** i s’actualitza la connexió. La llista ha de permetre distingir les capes del projecte incrustat. Es desa el `.qgz` homònim amb camins relatius.

Una vista addicional pot mostrar que dos projectes comparteixen dades sense conservar la mateixa configuració. `pr1` continua sent el principal; totes les vistes que es mantinguin han de tenir inventari i fonts comprovats.

Cal efectuar dues obertures independents. Un canvi de simbologia pot mostrar que desar la representació externa no actualitza l’incrustada. Les edicions de les dades i les modificacions del projecte també es desen amb accions diferents.

## Composició cartogràfica del recorregut ampliat

La demostració parteix del projecte validat i crea una composició municipal des de **Projecte > Nova composició d’impressió**. Es justifiquen mida de pàgina, escala i enquadrament; després es relacionen gruixos, color, etiquetes i llegenda amb la pregunta del mapa. Es comprova el vincle entre escala gràfica i mapa principal, i la funció d’un possible localitzador.

El mapa del recorregut ampliat inclou terme recognoscible, context útil, títol, llegenda, escala gràfica, fonts i autoria; s’identifiquen CRS, dates disponibles i orientació. Cal exportar-lo i obrir el PDF al 100% per revisar textos, símbols, retalls i atribucions. En la micropràctica confirmada, aquesta composició és una ampliació opcional.

Després de crear o modificar la composició es desen de nou les dues representacions, `pr1` incrustat i `.qgz`. La comprovació final consisteix a reobrir-les i trobar-hi la composició editable amb les fonts resoltes. Un PDF correcte, per si sol, no acredita aquest desament.

# Comprovacions i interpretació

| Control docent | Criteri d’acceptació |
| --- | --- |
| Obtenció de dades | Originals descarregats per l’estudiant, edició i procedència documentades |
| Lectura de la font | Recintes identificats, components complets i camps inspeccionats |
| Identitat municipal | Codi i nom concordants amb la font seleccionada |
| Capa persistent | Vector local dins del GeoPackage; sense dependència d’una capa temporal |
| Referència | Font EPSG:4258 i resultat EPSG:25831; reprojecció comprovada |
| Projectes | `pr1` i `.qgz` conserven les fonts previstes i la composició editable |
| Vistes addicionals | Inventari explícit i cap font local dirigida a una còpia antiga |
| Mapa propi | Composició municipal completa i PDF llegible a la mida final |
| Portabilitat | Obertura en una ruta nova; indisponibilitat remota diferenciada d’error local |

Table: Controls del cas CNIG ampliat i de la seva transferència; l’enunciat Moodle delimita els requisits avaluats.

Els recomptes d’una font general no són requisits del subconjunt final. Un municipi multipart pot continuar sent una sola entitat. Cal identificar l’edició i la selecció reals; una diferència respecte d’una referència s’investiga comparant fonts i operacions.

Els errors més útils per discutir són perdre components del Shapefile, carregar línies en lloc de recintes, exportar tota la font, deixar el resultat temporal o canviar només el CRS declarat. També convé mostrar què passa en desar només una representació o construir una composició sobre una capa que no viatja amb el projecte.

# Aplicació al municipi escollit

La revisió segueix el recorregut del municipi propi: descàrrega, inspecció, selecció, preparació, projecte i mapa. Els apunts han de permetre relacionar el resultat amb els originals i amb les decisions cartogràfiques. El cas resolt de Vila-seca facilita la discussió dels criteris; l’enquadrament i la simbologia de l’estudiant han de respondre al seu territori.

# Fitxers i evidències

La micropràctica conserva GPKG, projecte incrustat/extern i apunts PDF, amb WMS i fonts comprovats. El recorregut ampliat segueix la base `pr1-project-setup-cognom`: `.gpkg`, `.qgz`, `-mapa.pdf` i `-apunts.pdf`. Aquells noms orienten la continuïtat; la pauta avaluada és la comunicada a classe. Els originals es conserven a `data/raw/` i una còpia validada a `dist/`.

El GeoPackage es copia amb QGIS tancat i l’estat de la base estable; els journals no s’esborren per forçar el lliurament. En la correcció assistida s’utilitza la definició confirmada d’Unaltramesa, amb tres blocs i sense convertir els controls del cas ampliat en subpesos.

El PDF de l’alumnat proporciona les instruccions per obtenir i preparar les dades. El paquet de professorat reuneix originals, preparacions, projecte resolt, composició i controls. L’exemple que es comparteixi amb l’alumnat s’identifica expressament com a cas resolt de Vila-seca. Moodle concreta els fitxers i la forma del lliurament avaluat.

# Referències

- [CNIG: fitxa del producte de límits i unitats administratives](https://centrodedescargas.cnig.es/CentroDescargas/detalleArchivo?sec=9000029).
- [IGN: serveis web oficials, inclòs PNOA](https://www.ign.es/web/ign/portal/ide-area-nodo-ide-ign).
- [Guia de QGIS 3.44: projectes](https://docs.qgis.org/3.44/en/docs/user_manual/introduction/project_files.html).
- [Guia de QGIS 3.44: composicions](https://docs.qgis.org/3.44/en/docs/user_manual/print_layout/index.html).
