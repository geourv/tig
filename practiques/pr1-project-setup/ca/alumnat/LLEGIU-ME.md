---
title: "PR1 · Projecte municipal i composició cartogràfica"
lang: ca
recipient: alumnat
content_status: approved
subject: "Tecnologies de la Informació Geogràfica"
subject_code: "21234114"
author: "Benito Zaragozí"
institution: "Universitat Rovira i Virgili"
---

# Finalitat i resultats d’aprenentatge

Com es prepara un projecte municipal que una altra persona pugui obrir, entendre i continuar? PR1 treballa la selecció del terme, el GeoPackage, el projecte QGIS i uns apunts útils per repetir el procediment. Aquesta guia desenvolupa un recorregut amb fonts CNIG i una composició cartogràfica, amb un abast més ampli que la micropràctica avaluada a Moodle.

En acabar, cal poder localitzar i documentar una font, seleccionar i exportar un municipi, comprovar el sistema de referència de coordenades (CRS), distingir dades i projectes i revisar el mapa a la seva mida final. El treball propi correspon al municipi escollit.

Vila-seca il·lustra el procediment; la micropràctica permet escollir el municipi. La font, els codis i la preparació s’han d’identificar per al cas realment treballat.

# Abast de la micropràctica Moodle

L’enunciat confirmat el 18 d’octubre de 2026 demana un GeoPackage amb el terme municipal desat i carregat des d’aquest contenidor, el projecte QGIS incrustat, una còpia externa `.qgz` i uns apunts breus en PDF. El projecte incorpora també una capa cartogràfica WMS. Cal seguir les pautes de noms comunicades a classe i comprovar obertura, disponibilitat de capes i rutes.

La **composició és una ampliació opcional** d’aquesta micropràctica. Un únic PDF d’apunts satisfà el tipus documental obligatori. L’enunciat admet una font de límits adequada i no fixa un productor, un municipi docent ni un codi EPSG. Els noms i les configuracions del cas següent serveixen per aprendre i continuar el recorregut; no afegeixen requisits a aquell lliurament.

El **recorregut ampliat CNIG** inclou descàrrega pròpia, metadades, preparació mètrica, composició editable i exportació cartogràfica. Aquests resultats es treballen quan el professor selecciona aquella via i es conserven per a les fases posteriors. Moodle identifica l’activitat i l’abast que s’avaluen.

# Fonts del recorregut ampliat

Per seguir el recorregut mètric següent, cal escollir un municipi dins de l’àmbit de les fonts i d’un ús adequat d’ETRS89 / UTM zona 31N, **EPSG:25831**. La capa general pot cobrir un territori més extens que l’àmbit adequat d’aquesta projecció; el treball en metres es farà sobre el municipi escollit.

El [Centre de Descàrregues del CNIG](https://centrodedescargas.cnig.es/CentroDescargas/) proporciona el vector de límits administratius. El servei oficial IGN/PNOA aporta la imatge de context. La descàrrega, la lectura de metadades i la preparació d’aquestes fonts formen part de l’activitat.

Un WMS proporciona una imatge del mapa: el vector que es descarrega és el que permet seleccionar i exportar el terme municipal. Consultar el WMS no desa automàticament una ortofoto local. Per a cada font cal registrar productor, producte, edició, data d’accés, URL, llicència, CRS i escala o resolució.

# Procediment del recorregut ampliat

## Organitzar i identificar el treball

La carpeta de curs s’anomena `tig/`. `data/raw/` conserva els originals descarregats i les metadades; `data/processed/`, les preparacions reutilitzables; `sandbox/`, el treball actiu; i `dist/`, les còpies validades per distribuir. Es crea una carpeta identificada per producte i edició per a cada descàrrega. Els originals no se sobreescriuen.

La base de noms del recorregut és `pr1-project-setup-cognom`, amb `cognom` substituït per l’identificador acordat. El GeoPackage i el projecte extern comparteixen aquesta base. En el lliurament de la micropràctica preval la pauta comunicada a classe. El nom d’un fitxer, el d’una capa i el d’un projecte incrustat tenen funcions diferents.

## Descarregar i conservar els límits originals

1. Al Centre de Descàrregues s’obre **Información geográfica de referencia > Límites municipales, provinciales y autonómicos**. La [fitxa de Límites y Unidades Administrativas Actuales](https://centrodedescargas.cnig.es/CentroDescargas/detalleArchivo?sec=9000029) identifica l’arxiu, la data, el format, la cobertura i el sistema de referència.
2. Es revisen la fitxa i les condicions d’ús. El cas de referència utilitza `LINEAS_LIMITE.ZIP`, en format Shapefile, edició de **28/07/2026**. Si el portal ofereix una edició posterior, s’anota la que realment es descarrega.
3. S’utilitza el botó de descàrrega del portal i es desa el ZIP original a `data/raw/`, dins de la carpeta del producte i l’edició. Es conserven també les metadades i el document de lectura que l’acompanyen.
4. El ZIP s’extreu en una subcarpeta identificada, sense substituir l’arxiu comprimit. Dins de `SHP_ETRS89` es localitzen els **recintes municipals**. Els fitxers de línies límit representen fronteres; per seleccionar la superfície municipal cal la capa de recintes.

El fitxer `recintos_municipales_inspire_peninbal_etrs89.shp` conté les geometries dels recintes del cas de referència.

Cal conservar junts tots els components d’aquesta capa: `.shp`, `.shx`, `.dbf`, `.prj` i `.cpg`. Copiar només el `.shp` pot deixar sense atributs, referència espacial o informació de codificació. La carpeta completa extreta i el ZIP original es mantenen a l’arxiu de treball.

Als apunts es registra la fitxa consultada, el nom de l’arxiu, l’edició, la data de descàrrega i la llicència. Aquesta evidència permet explicar d’on provenen les dades que després s’exportaran al GeoPackage.

## Inspeccionar la capa en un projecte nou

Es crea un projecte QGIS nou, amb CRS **EPSG:25831**, i s’hi afegeix el Shapefile de recintes des de la carpeta extreta. A les propietats de la capa es comproven el proveïdor, la ruta, la geometria i el CRS declarat. La font de referència és **ETRS89, EPSG:4258**, amb coordenades geogràfiques; QGIS la transforma per representar-la al projecte.

A la taula d’atributs s’identifiquen `NAMEUNIT`, amb el nom, i `NATCODE`, amb el codi de la unitat. Es llegeixen els valors de l’edició descarregada i es comprova el nombre de registres. La capa conté recintes administratius, incloses algunes unitats singulars; el recompte de files no s’interpreta automàticament com un recompte de municipis ordinaris.

## Connectar el fons IGN/PNOA

Al **Gestor de fonts de dades > WMS/WMTS** es crea una connexió amb un nom recognoscible, com `PNOA IGN`, i aquesta URL:

```text
https://www.ign.es/wms-inspire/pnoa-ma?
```

Es prem **Connecta**, es tria la capa **Ortoimagen**, identificador `OI.OrthoimageCoverage`, i s’afegeix al projecte. Es col·loca sota el vector municipal; un contorn sense farciment opac permet veure la imatge i el límit alhora.

Cal apropar-se al municipi a una escala útil. El servei combina imatges de satèl·lit a escales petites i ortofotos PNOA a partir d’una escala aproximada d’1:70.000. «Màxima actualitat» no és una data de vol: s’anota la data de consulta i es comproven les metadades de la imatge que cobreix la zona. La capa **Mosaico** del mateix servei permet consultar data i resolució als punts d’interès.

La connexió utilitza eines natives de QGIS. Als apunts es conserven URL, capa i atribució del servei, juntament amb la distinció entre la descàrrega vectorial local i la imatge consultada en línia.

## Seleccionar el municipi i exportar-lo

1. Es localitza el municipi al mapa i s’activa la capa de recintes. Amb l’eina de selecció s’escull el terme i se’n comproven nom, codi i recompte a la taula. Cal obtenir l’entitat municipal completa, també si té diverses parts.
2. Al menú contextual de la capa s’obre **Exporta > Desa els objectes seleccionats com a…**. Es tria GeoPackage, `sandbox/pr1-project-setup-cognom.gpkg`, nom de capa `municipi_treball` i CRS de sortida **EPSG:25831**. L’opció de només seleccionats ha de quedar activada.
3. S’afegeix la capa desada al projecte i es comproven la ruta dins del GeoPackage, el recompte, el nom, el codi i el CRS. Les coordenades de la capa exportada són ara en metres.
4. Es reobre la capa des del GeoPackage. Quan el resultat està comprovat, es pot retirar la capa general del projecte de treball i conservar-la amb els originals descarregats.

Canviar el CRS de la vista no transforma les coordenades desades. L’exportació amb un CRS de sortida explícit sí que pot reprojectar-les. Cal identificar el CRS original, no assignar EPSG:25831 a unes coordenades en graus per fer desaparèixer un avís.

La capa `municipi_treball` és el límit CNIG que continuarà a les pràctiques següents. La seva procedència ha de permetre relacionar-la amb el registre seleccionat i amb l’edició original.

## Desar el projecte incrustat i l’extern

Al panell **Explorador** es crea o s’obre una connexió amb el GeoPackage. A **Projecte > Desa a > GeoPackage** s’escull el contenidor de treball i el nom de projecte **`pr1`**. Després cal actualitzar la connexió per veure’n les capes i el projecte.

Es desa també `sandbox/pr1-project-setup-cognom.qgz`, amb camins relatius cap al GeoPackage que l’acompanya. El `.qgz` guarda la configuració del mapa, però no incorpora automàticament les capes vectorials. Desar-lo no actualitza el projecte `pr1` incrustat, ni a l’inrevés.

El projecte principal és `pr1`. Si es conserva una vista addicional, també cal comprovar-ne les fonts. El nombre de projectes incrustats no s’ha de confondre amb el nombre de capes.

## Crear la composició cartogràfica

La composició completa el recorregut ampliat i és una ampliació opcional de la micropràctica Moodle. Amb el projecte funcional, es defineix què ha d’explicar el mapa municipal i a quin públic s’adreça. A **Projecte > Nova composició d’impressió** es crea una composició amb un nom identificable, com `Mapa municipal`.

Es trien mida i orientació del paper, s’insereix el mapa i se n’ajusten l’enquadrament i l’escala. El terme ha de quedar complet i recognoscible; la informació de context ha d’ajudar a situar-lo. Després s’incorporen un títol informatiu, una llegenda depurada, una escala gràfica vinculada al mapa, les fonts i l’autoria. S’hi identifiquen el CRS i les dates disponibles de les dades; l’orientació ha de quedar clara, especialment si el mapa es gira.

Cal revisar jerarquia de gruixos i colors, contrast, etiquetes, espais i coherència entre llegenda i capes visibles. Si s’afegeix un localitzador, ha d’ajudar a comprendre la posició del municipi. Una imatge molt detallada no compensa textos il·legibles ni una frontera amagada.

La composició s’exporta com `pr1-project-setup-cognom-mapa.pdf`. El PDF s’obre separadament i s’examina al 100%: retalls, textos, símbols, escala i atribucions han de ser llegibles. El mapa exportat i els apunts tècnics són productes diferents.

Després d’acabar la composició, es tornen a desar **tant `pr1` incrustat com el `.qgz` extern**. Cal reobrir-los per comprovar que tots dos conserven la composició editable i les fonts previstes.

# Comprovacions i interpretació

| Comprovació | Evidència que cal conservar |
| --- | --- |
| Descàrrega pròpia | ZIP original, metadades, edició i data d’accés registrades |
| Municipi correcte | Nom i codi a la taula; recompte coherent amb la font |
| Dades locals | Font del vector dins del GeoPackage de PR1, sense capa temporal |
| CRS | Origen EPSG:4258 identificat; exportació i projecte EPSG:25831 |
| Dues representacions | Obertura independent de `pr1` i del `.qgz`, amb la composició desada |
| Composició pròpia | Mapa complet i elements llegibles al PDF exportat |
| Transport | Reobertura de la còpia en una ubicació diferent amb les fonts locals resoltes |

Table: Controls del recorregut ampliat CNIG i de la composició, quan es treballa aquesta via.

Una prova offline pot deixar el WMS sense imatge; el vector municipal local ha de continuar disponible. Cal distingir aquest comportament d’una ruta trencada al GeoPackage. Les rutes absolutes personals, les capes temporals i la dependència d’una carpeta de descàrregues aliena són problemes de transport.

# Aplicació al municipi escollit

Cada estudiant resol el recorregut des de la descàrrega original fins al mapa del seu municipi. Els codis de Vila-seca serveixen per entendre la demostració; el treball propi utilitza els identificadors comprovats a la seva font.

El cas resolt de Vila-seca, quan s’ofereixi, es consulta en una carpeta separada com a **exemple del resultat esperat**. Permet examinar el projecte, les fonts i la composició. Als apunts s’expliquen els criteris que s’han adoptat o adaptat; la preparació de les dades i el mapa del municipi propi formen part del treball de l’estudiant.

# Fitxers i evidències

La micropràctica Moodle exigeix el GeoPackage, les dues representacions del projecte i el PDF d’apunts, amb la capa WMS configurada i les fonts locals resoltes. La taula següent identifica els productes del recorregut ampliat; el PDF cartogràfic és addicional en la micropràctica.

Amb l’edició desactivada i QGIS tancat, cal comprovar que el GeoPackage ha acabat les escriptures. Els fitxers de journal o WAL no s’eliminen manualment. Després es prepara una còpia completa a `dist/` i es prova des d’una ubicació neta.

| Producte propi | Contingut |
| --- | --- |
| `pr1-project-setup-cognom.gpkg` | Límit municipal local i projecte incrustat `pr1` amb composició |
| `pr1-project-setup-cognom.qgz` | Projecte extern homònim, amb les fonts i la composició comprovades |
| `pr1-project-setup-cognom-mapa.pdf` | Com a mínim un mapa exportat i revisat a mida final |
| `pr1-project-setup-cognom-apunts.pdf` | Descàrrega, fonts, preparació, decisions cartogràfiques i controls |

Table: Noms i productes del recorregut ampliat, amb mapa addicional al lliurament bàsic de Moodle.

Els originals descarregats i les seves metadades es conserven a `data/raw/`. Si el projecte utilitza altres fitxers locals, han d’acompanyar la còpia de transport amb camins relatius. Moodle concreta la forma de lliurament. El `LLEGIU-ME.pdf` explica l’activitat; els apunts propis en documenten l’execució, amb captures significatives de les decisions i comprovacions.

# Ampliacions i qualificació

Una ampliació ha de ser funcional, pertinent i explicable. Es poden afegir altres WMS, capes vectorials, simbologies, etiquetes, grups, mapes o composicions; no cal reunir totes les opcions. Algunes preguntes per orientar-ne el desenvolupament són:

- **Mapa municipal:** crear una composició que comuniqui el terme i el context. Si es comparen dues escales, explicar com canvien etiquetes, gruixos i contingut. Es comproven el desament i la llegibilitat; el nombre de mapes no determina la puntuació.
- **Procedència dins del projecte:** incorporar un registre de fonts al GeoPackage, vincular-lo a les capes i contrastar metadades i rutes després de transportar la còpia.
- **Localitzador justificat:** representar un municipi discontinu o litoral amb context CNIG i comprovar què aporta el localitzador a la lectura del terme i de la seva posició.

La micropràctica té tres blocs: **70% requisits imprescindibles, 20% ampliacions funcionals i 10% apunts, captures, presentació i organització**. Equivalen a màxims de **7, 2 i 1 punts** sobre 10. Es valora cada bloc globalment, sense subpesos fixos ni quotes per tipus d’ampliació. El primer WMS i el municipi són bàsics; una mateixa millora es puntua una sola vegada. Les ampliacions no substitueixen els requisits imprescindibles i la documentació també pot augmentar la nota sobre el bloc bàsic.

# Referències

- [CNIG: límits municipals, provincials i autonòmics](https://centrodedescargas.cnig.es/CentroDescargas/limites-municipales-provinciales-autonomicos).
- [IGN: serveis web oficials, inclòs PNOA](https://www.ign.es/web/ign/portal/ide-area-nodo-ide-ign).
- [Fonts i serveis geogràfics del manual TIG](https://geourv.github.io/tig/ca/chapters/tig-preguntes-fonts/).
- [Guia de QGIS 3.44: projectes](https://docs.qgis.org/3.44/en/docs/user_manual/introduction/project_files.html).
- [Guia de QGIS 3.44: composicions de mapa](https://docs.qgis.org/3.44/en/docs/user_manual/print_layout/index.html).
