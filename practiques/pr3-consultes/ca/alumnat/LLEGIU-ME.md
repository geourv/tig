---
title: "PR3 · Filtres, seleccions, expressions i mapa municipal"
lang: ca
recipient: alumnat
content_status: approved
subject: "Tecnologies de la Informació Geogràfica"
subject_code: "21234114"
author: "Benito Zaragozí"
institution: "Universitat Rovira i Virgili"
---

# Finalitat i resultats d’aprenentatge

Quines entitats cal conservar per construir un mapa municipal llegible i una base útil per analitzar? La pràctica passa de localitzar un municipi al mapa a formular criteris d’atributs i de posició. Els portals, les illes de CartoCiudad i el viari permeten contrastar punts, polígons i línies sobre un mateix terme.

En acabar, cal poder distingir filtre de capa, filtre de taula, selecció i exportació persistent; recuperar una consulta; calcular atributs amb unitats; i justificar la selecció de capes i la seva representació. La descoberta de dades cadastrals mitjançant ATOM amplia el conjunt de fonts sense confondre descàrrega i consulta d’entitats.

El professor indica a classe els apartats obligatoris del **70% bàsic** i els concreta a Moodle, inclòs l’abast de la descoberta cadastral. Les altres comparacions de la guia no es converteixen automàticament en requisits. Cal mantenir la base acumulativa i les dades que permetran continuar a PR4.

# Punt de partida i dades

Amb QGIS tancat, es copia el GeoPackage validat de PR2 a `sandbox/pr3-consultes-cognom.gpkg`. Cal conservar físicament les capes municipals, `fanals`, `carrils_bici` i `plaques_solars`, amb els seus identificadors i atributs. Les fonts locals es reorienten al nou contenidor; el principal serà `pr3` i el `.qgz` extern es crearà de nou.

| Producte del cas de classe | Edició documentada | Capa principal |
| --- | --- | --- |
| Línies límit CNIG | 28/07/2026 | Recintes municipals peninsulars i balears |
| CartoCiudad Tarragona | 04/2026 | `portalpk_publi` i `manzana`, de `tarragona.gpkg` |
| Xarxa de transport Tarragona | 07/2026 | `rt_tramo_vial`, de `red_viaria.gpkg` |

Table: Fonts del recorregut resolt de Vila-seca.

La capa municipal d’aquesta distribució s’anomena `recintos_municipales_inspire_peninbal_etrs89`. Cal identificar-la pel nom complet i comprovar-ne el nivell administratiu.

Els originals s’obtenen del [Centre de Descàrregues del CNIG](https://centrodedescargas.cnig.es/CentroDescargas/) i es conserven a `data/raw/`, amb metadades i llicències. Cal inspeccionar els camps reals de cada edició; un producte GML pot tenir noms diferents d’un Shapefile. Per a un municipi d’una altra província cal obtenir la cobertura corresponent, no aplicar els codis de Tarragona a qualsevol font.

# Procediment

## Obtenir i preparar les fonts

Al catàleg del CNIG, dins d’**Información geográfica de referencia**, es localitzen CartoCiudad i les xarxes de transport de la província del municipi propi. Les fitxes de referència són [CartoCiudad Tarragona](https://centrodedescargas.cnig.es/CentroDescargas/detalleArchivo?sec=9092) i [transport Tarragona](https://centrodedescargas.cnig.es/CentroDescargas/detalleArchivo?sec=11655613). Cal llegir cobertura, edició, format, CRS i llicència abans de descarregar.

Cada estudiant desa els ZIP originals i les metadades a `data/raw/`, els extreu en carpetes identificades i inspecciona les taules dels GeoPackage. En el cas de classe es carreguen `portalpk_publi`, `manzana` i `rt_tramo_vial`. La font de límits de PR1 es pot reutilitzar si és la mateixa edició; les consultes noves no modifiquen els originals.

Es comproven camps, dominis, CRS i recomptes abans d’aplicar les expressions. Les seleccions i exportacions següents preparen les dades locals de treball a partir d’aquestes fonts.

## Localitzar el municipi i distingir els estats de consulta

Es carrega la font municipal completa, se’n comprova el CRS i s’activa la capa vectorial. La primera selecció de Vila-seca es fa amb clic o rectangle; a la taula es contrasten `NAMEUNIT` i `NATCODE`. La selecció es neteja abans del pas següent.

El filtre de capa, accessible amb clic dret i **Filtre…**, limita les entitats que aquella capa exposa. En la distribució del cas, la consulta provincial és:

```sql
"CODNUT3" = 'ES514'
```

La font continua completa. El filtre es pot conservar al projecte, però encara no existeix un fitxer provincial nou. El constructor indica el proveïdor que avalua la consulta; la seva sintaxi no és necessàriament la de totes les funcions de QGIS.

La taula d’atributs permet mostrar tots els objectes, els seleccionats, els visibles al mapa o els que compleixen un filtre de camp o d’expressió. Mostrar tres files no selecciona automàticament tres entitats ni determina què s’exportarà.

| Estat | Què modifica | Què cal registrar |
| --- | --- | --- |
| Filtre de capa | Entitats disponibles a la capa | Consulta, proveïdor i recompte exposat |
| Filtre de taula | Files visibles al panell | Mode de visualització i recompte visible |
| Selecció | Conjunt d’entitats marcades | Mètode, criteri i recompte seleccionat |
| Exportació | Nova capa persistent | Opció de seleccionats, destinació, CRS i recompte reobert |

Table: Quatre estats diferents sobre una mateixa font.

## Formalitzar i conservar una selecció

Es comparen clic, rectangle, polígon i radi de cerca. Els modificadors s’han de provar en el context concret: clic de mapa, selecció per àrea i capçalera de fila tenen comportaments diferents. Un cercle de cerca no és un buffer desat.

A **Selecciona objectes segons una expressió…**, el municipi del cas s’identifica amb:

```sql
"NATCODE" = '34094343171'
```

Les cometes dobles identifiquen el camp i les simples, el text literal. `AND`, `OR`, `IN`, parèntesis i `IS NULL` permeten construir criteris llegibles; `= NULL` no substitueix `IS NULL`. Cal comprovar si l’acció crea, afegeix, resta o restringeix una selecció.

El municipi seleccionat s’exporta al GeoPackage de PR3 com a `municipi_consulta`, en EPSG:25831. Serà la referència de les consultes espacials. Es conserva també `municipi_treball`, heretat de PR1, i es comproven edició, codi i geometria dels dos límits CNIG. Una descàrrega posterior no substitueix silenciosament l’entrada de les fases anteriors.

## Seleccionar portals, illes i vies

Als punts de CartoCiudad s’inspecciona `tipo` i es filtren els valors `Portal`, distingint-los dels punts quilomètrics `PK`. Després s’utilitza **Selecciona per la ubicació**, `native:selectbylocation`, amb els portals com a entrada, el municipi com a comparació i una selecció nova. Cal contrastar `intersecta` amb `estan dins` quan hi pugui haver punts de frontera.

A `manzana` es comprova el tipus poligonal i es representa el farciment. El resultat principal conserva les illes completament contingudes; una segona selecció amb `intersecta` permet inspeccionar les que toquen o travessen el terme. La selecció conserva geometries senceres: el retall correspon a PR4.

Al viari s’inspeccionen els valors de `clased` abans d’anomenar-los primaris o secundaris. El cas del manual concreta les vies principals en `Autopista libre / autovía` i `Autopista de peaje`. La classificació de les vies secundàries s’ha de documentar amb les classes realment presents; no és automàticament el complement de les dues primeres ni una etiqueta importada d’un altre producte.

Les vies que travessen el terme se seleccionen amb `intersecta`. Cal distingir files de registres, identificadors `id_tramo` i itineraris: un tram pot aparèixer associat a més d’un itinerari. Abans de sumar longituds o eliminar repeticions s’ha d’explicar la unitat que representa cada fila.

Cada selecció es desa com una capa nova del GeoPackage de PR3, amb només seleccionats i EPSG:25831. Els noms han d’identificar-ne el paper, com `portals_municipi`, `illes_municipi` i `transport_candidats_c06`. En el cas de classe, els noms històrics `portals_vilaseca` i `illes_vilaseca` es conserven i es documenta aquesta correspondència.

## Calcular atributs i preparar el mapa

La calculadora diferencia crear un camp i actualitzar-lo, camp emmagatzemat i virtual, i totes les entitats o només seleccionades. Una àrea o una longitud es desa en un camp numèric; la unitat s’afegeix a l’àlies o a l’etiqueta, no dins del nombre.

`area($geometry)` i `length($geometry)` calculen sobre les coordenades de la geometria. `$area` i `$length` segueixen la configuració de mesures del projecte. Cal registrar CRS, el·lipsoide i unitats; a EPSG:25831 es poden contrastar mesures planes en metres amb les el·lipsoidals configurades.

Abans d’utilitzar una funció, se’n llegeixen arguments, retorn i exemple a l’ajuda del constructor. Un agregat com `aggregate()` resumeix el conjunt disponible; un filtre addicional pot canviar-ne el denominador. La previsualització d’una fila no valida tota la columna.

El mapa municipal diferencia viari principal i secundari segons el criteri escrit, illes amb farciment, portals i contorn municipal. Cal depurar la llegenda, donar prioritat a la informació rellevant i revisar les etiquetes a l’escala de composició. Es conserva una vista de tot el terme per fer visibles les seleccions de frontera.

## Descobrir dades cadastrals amb ATOM

Des del [portal INSPIRE del Cadastre](https://www.catastro.hacienda.gob.es/webinspire/index.html) s’identifiquen els feeds de parcel·les, edificis o adreces. Un feed ATOM és XML que enllaça feeds i paquets predefinits; no és una imatge WMS ni una petició WFS amb un filtre d’entitats.

Per a parcel·les es pot seguir el [feed general](https://www.catastro.hacienda.gob.es/INSPIRE/CadastralParcels/ES.SDGC.CP.atom.xml), després l’oficina territorial i finalment l’entrada municipal. Cal llegir el títol, `updated`, `rights`, els enllaços de metadades i `rel="enclosure"`, conservar la descàrrega i comprovar-ne el contingut i el CRS abans d’exportar.

El manual va documentar Vila-seca com `43173-VILA SECA` al feed cadastral consultat el 15 de setembre de 2026, mentre que el codi territorial CNIG del cas acaba en `43171`. Cal seguir l’entrada i les metadades de la font actual: no es construeix la URL canviant només un codi suposadament universal.

El complement Spanish Inspire Catastral Downloader és una via d’accés convenient, però no substitueix la traça del feed. Les parcel·les s’incorporen com una font separada, amb llicència i procedència. El producte cadastral no acredita per si sol propietat, edificabilitat ni un delimitament jurídic.

# Comprovacions i interpretació

Cada consulta registra font, filtre de capa, mode de taula, selecció, predicat i sortida. Es reobre la capa exportada, se’n comproven identificadors i geometries i es contrasta una mostra amb la font. Netejar la selecció o retirar la capa provincial del projecte no ha de fer desaparèixer el resultat local.

Cal confirmar que `fanals`, `carrils_bici` i `plaques_solars` mantenen els recomptes i els IDs de PR2. Una fase de consultes correcta que perdi aquestes capes trenca el recorregut posterior.

# Aplicació al municipi escollit

S’apliquen els mateixos estats i controls a l’altre municipi. Es documenten el criteri de vies principals/secundàries, els casos de frontera i la correspondència dels codis de cada font. Els recomptes de Vila-seca són referències d’una edició concreta, no valors que s’hagin d’obtenir en qualsevol territori.

# Fitxers i evidències

Es conserven `pr3-consultes-cognom.gpkg`, el nou `.qgz` homònim amb principal `pr3`, i `pr3-consultes-cognom-apunts.pdf`. La composició es desa als dos projectes i s’exporta com `pr3-consultes-cognom-mapa.pdf`. Els apunts recullen descàrregues, expressions, recomptes, paràmetres de mesura, descoberta ATOM i interpretació del mapa.

La còpia de `dist/` es prepara amb QGIS tancat i es prova des d’una ubicació neta. Les fonts locals han de resoldre’s sense el GeoPackage predecessor; la disponibilitat dels serveis remots es comprova separadament.

# Ampliacions i qualificació

Una ampliació ha d’anar més enllà dels apartats seleccionats, amb pregunta, referència i controls. Algunes opcions són:

- **Explicar els casos de frontera:** comparar dos predicats sobre la mateixa font i límit, obtenir els conjunts d’IDs exclusius i inspeccionar-ne una mostra. El resultat inclou taula i mapa dels casos que expliquen la diferència.
- **Registres versus trams:** auditar els identificadors viaris repetits, comprovar les geometries i comparar resums amb una unitat explícita. No es deduplica només per fer disminuir el total.
- **Consulta transferible:** preparar una consulta reutilitzable en un segon municipi, amb paràmetres i recomptes. Es prova un cas amb resultat i un altre sense resultat i s’explica com detectar camps o codis inadequats.

La qualificació té màxims de **7 punts pels obligatoris, 2 per ampliacions i 1 per documentació**: 70/20/10. Es valoren correcció i persistència, contrast i interpretació, i claredat d’apunts, captures, mapes i organització, respectivament. Els 7 punts són el màxim del bloc bàsic; la documentació també pot augmentar la nota. Les ampliacions no substitueixen els obligatoris ni donen punts automàtics per afegir capes.

# Referències

- [Consultes i dades relacionals, manual TIG](https://geourv.github.io/tig/ca/chapters/consultes-dades-relacionals/).
- [Expressions, QGIS 3.44](https://docs.qgis.org/3.44/en/docs/user_manual/expressions/index.html).
- [Portal INSPIRE del Cadastre](https://www.catastro.hacienda.gob.es/webinspire/index.html).
