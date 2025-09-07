---
lang: ca
permalink: /:title/ca/
title: "Preparant l'entorn SIG"
author: Benito Zaragozí
date: 2025-09-07
weight: 1
layout: chapter
mermaid: false
---

Un sistema d’informació geogràfica (SIG) és la combinació de programari, maquinari, dades i coneixement per capturar, emmagatzemar, analitzar i visualitzar informació geoespacial. En aquest curs utilitzarem QGIS com a eina principal, però l’objectiu és més ampli: aprendre a **organitzar el treball** amb criteri perquè els projectes siguen traçables, repetibles i fàcils de compartir. Aquest primer capítol s’ocupa d’això: sistemes operatius i rutes, estructura de carpetes, criteris de nomenclatura, fitxer de projecte i gestió bàsica de comprimits.

## Sistemes operatius i rutes

QGIS és multiplataforma: funciona en Windows, macOS i GNU/Linux. Windows utilitza rutes amb barres invertides (`C:\projectes\tig\dades`), mentre que macOS i Linux en fan servir amb barres normals (`/Users/usuari/projecte` o `/home/usuari/projecte`). macOS i Linux comparteixen arrels Unix i, malgrat diferències d’interfície i gestor de paquets (en Linux hi ha múltiples distribucions), tenen una lògica de fitxers semblant. Quan un mateix projecte es mou entre equips i sistemes diferents, aquesta disparitat de rutes és una font típica d’errors. Per això és preferible configurar els projectes perquè apunten a **rutes relatives** des de la ubicació del `.qgz`.

Una **ruta absoluta** indica sempre la posició completa d’un element dins el sistema de fitxers. A Windows comença per la lletra de la unitat (`C:\...`), mentre que a Linux i macOS comença des de l’arrel (`/`). Alguns exemples serien:

- Windows: `C:\Users\anna\Documents\projecte-tig\data\municipis.shp`  
- Linux: `/home/anna/projecte-tig/data/municipis.shp`  

En canvi, una **ruta relativa** descriu el camí a un fitxer en relació amb la carpeta on es troba el projecte. Aquesta opció és la més pràctica quan treballem amb QGIS perquè permet moure la carpeta completa del projecte sense trencar els enllaços. Les rutes relatives es basen en símbols especials:

- `./` indica la carpeta actual. Per exemple, `./dades/municipis.shp` apunta a la subcarpeta `dades` dins del projecte.  
- `../` indica la carpeta superior (anar “un nivell amunt”). Per exemple, si el projecte està a `sandbox/balneari/`, la ruta `../data/municipis.shp` ens portarà a la carpeta `data` que està al mateix nivell que `sandbox`.  
- Es poden encadenar: `../../` significa “pujar dos nivells”.

Això vol dir que si un fitxer de projecte `.qgz` està guardat a `sandbox/balneari/`, i la capa és a `sandbox/balneari/dades/edificis.shp`, la ruta relativa serà simplement `./dades/edificis.shp`. Si en canvi les dades són a la carpeta general `data/`, la ruta relativa podria ser `../../data/municipis.shp`.

> Activa i comprova l’ús de **rutes relatives** al diàleg de propietats del projecte de QGIS. Així el projecte s’obrirà igual en Windows, macOS i Linux, sense importar on es desin exactament les carpetes.
{: .block-tip }

## Organització de carpetes

Treballar amb dades espacials implica manejar molts fitxers. Una organització mínima i estable evita confusions i pèrdues de temps. Per això convé separar clarament **orígens**, **espai de treball** i **sortides**. La carpeta `data/` ha de contenir les dades originals, descarregades de fonts oficials o obertes, que no s’han de modificar mai. La carpeta `sandbox/` és l’espai de treball actiu: cada projecte hi té la seva pròpia subcarpeta amb el fitxer de projecte `.qgz` i els derivats temporals. Quan un resultat es considera definitiu, passa a `results/`, que actua com a magatzem de capes i taules consolidades i reutilitzables. Les sortides cartogràfiques finals, preparades amb l’editor de composicions, es guarden a `maps/` en format PDF o imatge.

```bash
projecte-tig/
├── data/       # dades originals (no modificar mai)
├── sandbox/    # espai de treball actiu
│   ├── balneari/    # projecte 1: .qgz + derivats temporals
│   └── mobilitat/   # projecte 2: estructura anàloga
├── results/    # capes i taules definitives (reutilitzables)
└── maps/       # sortides cartogràfiques finals (PDF/PNG)
```

Anomenar bé les carpetes i mantenir coherència és tan important com la seva estructura. Si la carpeta es diu `balneari/` o `mobilitat/`, queda clar a quin projecte es refereix. Si en canvi s’utilitzen noms com `proj1/` o `prova/`, és fàcil oblidar què contenen. El mateix passa amb les subcarpetes: és recomanable utilitzar noms curts, clars i sense espais, com ara `dades/`, `sortides/`, `vector/` o `raster/`. D’aquesta manera, escriure rutes relatives resulta més intuïtiu i estalvia temps cada vegada que busquem un fitxer.

També és útil recordar com funcionen les rutes relatives. Si el projecte està guardat dins `sandbox/balneari/`, una capa emmagatzemada a la subcarpeta `dades/` es pot escriure com `./dades/nom_capa.shp`. Si la capa es troba a la carpeta general `data/`, la ruta relativa seria `../../data/nom_capa.shp`, ja que cal pujar dos nivells per arribar a l’arrel del projecte. Quan els noms de carpetes són clars i consistents, aquestes rutes es tornen intuïtives i fàcils de recordar, i això estalvia temps i esforç en la gestió quotidiana.

> Conserva sempre els arxius originals a `data/` i treballa amb còpies a `sandbox/`. Així pots repetir processos i auditar el flux de treball sense risc de perdre les fonts.
{: .block-warning }

## Noms de fitxers

La nomenclatura és part del mètode i forma part de l’organització del projecte tant com les carpetes. Posar bons noms estalvia problemes i facilita la col·laboració. Quan els noms són clars i consistents, qualsevol persona que obri el projecte pot entendre immediatament què conté cada fitxer, i quan passen mesos també ens és més fàcil recuperar la lògica del que havíem fet.

Cal utilitzar **minúscules** i separadors senzills (`_` o `-`), i evitar **espais**, **accents** i caràcters especials (`ç, ñ, à, é, &, %...`). Això no és una mania, sinó una necessitat pràctica: molts programes antics de SIG, i fins i tot algunes utilitats actuals, no gestionen bé aquests caràcters. Els espais es poden interpretar com a separadors d’ordres en línia de comandes; els accents i símbols especials poden donar errors quan el sistema espera només caràcters bàsics del conjunt ASCII. Avui dia la majoria de programes admeten codificacions modernes com UTF-8, però no tots els formats les gestionen igual. El Shapefile, per exemple, té un suport limitat per a noms amb caràcters especials i pot provocar problemes de compatibilitat entre sistemes.

Sobre els separadors, la diferència entre `_` (guió baix) i `-` (guió normal) depèn del context. En noms de fitxers, la majoria de sistemes operatius admeten ambdós caràcters i per això és habitual trobar tant `_` com `-`. Ara bé, en bases de dades i en noms de camps o columnes és molt més segur utilitzar sempre `_`, ja que el guió `-` es pot interpretar com a operador de resta i obligaria a posar cometes o escapaments incòmodes. Per això, un camp anomenat `nom_municipi` és clar, compatible i fàcil d’utilitzar a SQL, Python o R, mentre que `nom-municipi` podria generar errors. En canvi, en entorns web és freqüent veure noms amb `-` perquè s’integren bé a les URL. En resum: en projectes SIG i en gestió de dades és preferible mantenir `_` com a separador per assegurar compatibilitat, i reservar `-` només per a casos específics com noms visibles en contextos web.

Exemples de noms adequats serien:
`usos_sol_2023.gpkg`, `viari_municipal_utm31.gpkg`, `cens2021_municipis.shp`.

En canvi, noms com `Mapa Final.shp`, `Parcel·lesç_noves.shp` o `Datos nº1.shp` poden semblar correctes a primera vista, però tenen espais, accents o símbols que poden trencar fluxos de treball quan s’automatitzen processos o es comparteix el projecte amb altres usuaris.

> Mantén un patró de noms estable (prefixos/abreviatures coherents) i documenta’l a l’inici del projecte per a ús del teu equip. Això evita malentesos i assegura la compatibilitat a llarg termini.
{: .block-tip }

## Fitxer de projecte de QGIS

QGIS desa la configuració del treball en `.qgs` (XML llegible) o `.qgz` (contenidor comprimit amb l’XML i recursos). El `.qgz` és l’opció recomanada actualment perquè ocupa menys i pot incloure arxius auxiliars com miniatures o anotacions, però en qualsevol cas el fitxer de projecte **no conté** les dades: només guarda rutes, estils i paràmetres de visualització. Per això és important desar-lo sempre **dins** de `sandbox/<nom_projecte>/` i comprovar que les capes s’hi enllacen amb rutes relatives. Evita acumular moltes còpies amb noms confusos; si cal, fes snapshots datats en moments clau o bé utilitza control de versions amb Git.

Ara bé, hi ha formats que sí que poden autocontenir dades i projecte en un sol paquet. L’exemple més clar és el **GeoPackage (.gpkg)**, un contenidor basat en SQLite que pot incloure múltiples capes vectorials i ràster, taules i fins i tot estils. QGIS permet desar estils dins del mateix `.gpkg`, de manera que la informació de representació viatja amb les dades. Això el converteix en una alternativa molt més robusta que el Shapefile i en un bon complement als fitxers de projecte. Tot i així, el `.gpkg` no substitueix el `.qgz`: el projecte continua sent el document que enllaça totes les capes i defineix la seva organització. El que sí que pots fer és reduir la dispersió de fitxers: en lloc de tenir vint shapefiles separats, pots concentrar-los en un únic GeoPackage i enllaçar-los des del projecte. Així el conjunt és més fàcil de moure i compartir.

> Encara que existeixin contenidors com el GeoPackage, QGIS continua necessitant un fitxer de projecte `.qgz` per guardar l’estat general del treball. El `.gpkg` pot ser el magatzem de les dades, mentre que el projecte en defineix l’estructura i la visualització.
{: .block-tip }

## Formats de dades (recordatori)

Del curs anterior coneixes el **Shapefile**, un format creat per ESRI a principis dels anys 90. Durant molts anys va ser l’estàndard de facto en el món dels SIG perquè era lleuger, relativament senzill i compatible amb gairebé tots els programes existents en aquella època, quan els ordinadors personals eren molt menys potents que els actuals. La seva estructura permetia emmagatzemar geometries i atributs de manera prou eficient, però amb el pas del temps les seves limitacions s’han fet molt evidents. Un shapefile no és mai un sol arxiu, sinó un conjunt de fitxers que han d’anar sempre junts: com a mínim `.shp` (geometria), `.dbf` (taula d’atributs) i `.shx` (índex), i sovint també `.prj` (sistema de referència) i `.cpg` (codificació de caràcters).

Aquest disseny fragmentat provoca problemes: si falta un dels fitxers, la capa es pot corrompre; el fitxer `.dbf` té limitacions històriques (noms de camp de màxim 10 caràcters, tipus d’atribut restringits, problemes amb caràcters no ASCII); i un shapefile només pot contenir una capa alhora. A més, el límit de 2 GB de mida total i el nombre màxim d’entitats poden ser insuficients per a projectes actuals. Aquestes restriccions s’entenen pel context tecnològic dels anys 90, però avui condicionen negativament l’ús professional. Per això moltes veus del sector promouen abandonar-lo; un recurs conegut és la pàgina [**“Why Shapefiles Are Bad”**](https://switchfromshapefile.org/), que recull i explica de manera detallada tots aquests inconvenients.

Com a alternativa moderna trobem el **GeoPackage (.gpkg)**, un format estandarditzat per l’OGC ([document oficial de l’estàndard](https://www.ogc.org/standards/geopackage)). El GeoPackage es basa en una base de dades SQLite i té la gran virtut de permetre emmagatzemar múltiples capes vectorials i ràster, taules i fins i tot estils en un únic arxiu. Això redueix dràsticament la dispersió de fitxers i facilita compartir dades i projectes. QGIS pot llegir i escriure directament en `.gpkg`, i molts altres programes ja ofereixen compatibilitat.

Un exemple ajuda a veure la diferència: si volem treballar amb dues capes vectorials en format Shapefile (per exemple, municipis i carreteres), necessitarem almenys aquests fitxers:

- `municipis.shp`  
- `municipis.dbf`  
- `municipis.shx`  
- `municipis.prj`  
- `carreteres.shp`  
- `carreteres.dbf`  
- `carreteres.shx`  
- `carreteres.prj`  
- i un fitxer de projecte de QGIS `.qgz` que les enllaci.

En canvi, amb GeoPackage podem tenir un únic arxiu `projecte.gpkg` que contingui dues capes internes (`municipis` i `carreteres`) i el projecte `.qgz` que hi apunta. Així el conjunt és molt més compacte i manejable. Aquest avantatge és especialment important quan treballem en grup o quan hem de compartir els resultats amb tercers.

Tot i que en aquest capítol seguirem utilitzant shapefiles per reforçar conceptes i mantenir la compatibilitat amb coneixements previs, cal tenir present que el futur passa per formats més robustos i versàtils com el GeoPackage.

## Comprimir i descomprimir

Moltes fonts oficials distribueixen dades en `.zip`. Convé **desar l’arxiu original a `data/`**, descomprimir-lo en una subcarpeta homònima i copiar-ne les dades de treball a `sandbox/<projecte>/`. A Windows pots utilitzar 7-Zip; a macOS i Linux tens eines integrades suficients per a la majoria de casos.

> Abans de començar el treball, comprova la versió exacta de QGIS (preferentment LTR) i anota-la al teu quadern de projecte. Això facilita reproduir processos i resoldre incidències.
{: .block-tip }

## Interfície bàsica de QGIS

![Interfície bàsica de QGIS]({{ site.baseurl }}/images/qgis-gui-schema.png)

Quan obrim QGIS ens trobem amb una finestra que combina menús, barres d’eines, panells i l’àrea principal de mapa. A la part superior hi ha la **Barra de menú**, amb entrades com **Projecte**, **Editar**, **Visualitza**, **Capa**, **Vector**, **Ràster**, **Base de dades**, **Complementos** o **Ajuda**. Des d’aquí podem crear i desar projectes, afegir i eliminar capes, configurar el sistema de referència, instal·lar complements o accedir a la documentació oficial. Just a sota hi trobem les **Barres d’eines**, amb icones que donen accés directe a funcions habituals. Entre les més importants hi ha la navegació del mapa (Zoom +, Zoom −, Panoràmica, Zoom a la capa activa), la consulta d’informació (Identificar entitat, Mesurar distància i superfície), la selecció de dades (per atributs o per localització), o la gestió de l’edició (Afegir entitats, Moure, Dividir o Fusionar). També hi ha la barra per obrir l’**Editor de composicions (Layout)**, que ja has utilitzat per preparar mapes maquetats al curs anterior.

A l’esquerra de la interfície apareixen els **Panells laterals**, dels quals dos són especialment rellevants:

- el **Panell de capes**, on s’organitzen totes les capes carregades i on podem activar o desactivar-ne la visibilitat, canviar-ne l’ordre i accedir a opcions ràpides; i 
- el **Panell de navegador**, que ens permet explorar carpetes locals, bases de dades i serveis web com WMS o WFS. 

Un altre panell habitual és el de **Processament**, on es concentren totes les eines analítiques del programa i dels complements. Si algun d’aquests panells no es mostra, el pots activar amb el menú **Visualitza > Panells** o fent clic dret sobre una zona buida de la interfície. El mateix passa amb les barres d’eines, que es poden amagar o mostrar segons les necessitats.

Al centre de la finestra hi ha l’**Àrea de mapa (map canvas)**, que és on es dibuixen totes les capes i on podem interactuar directament amb les dades fent zoom, panoràmiques o edició segons l’eina seleccionada. A la part inferior es troba la **Barra d’estat**, que mostra informació en temps real: les coordenades del punter, l’escala actual, el sistema de referència espacial del projecte (CRS), el progrés de càrrega o si el renderitzat està actiu. També ofereix accés ràpid a opcions per bloquejar o desbloquejar el renderitzat i veure missatges generats pels processos o complements.

Cal tenir present que QGIS incorpora molts **menús contextuals** que només apareixen amb el botó dret del ratolí sobre elements concrets. Per exemple, fent clic dret sobre una capa activa al Panell de capes s’accedeix a les seves propietats, estils, exportació o opcions de zoom. Aquests menús són molt útils perquè adapten les opcions al context i permeten treballar més ràpidament.

## Pràctica

Aquesta pràctica té l’objectiu de refrescar coneixements del curs anterior i consolidar les primeres passes amb l’entorn i l’organització del treball. Segueix els passos amb calma, recordant què ja saps fer i fixant-te en les novetats de metodologia.

1. **Crea l’arbre de carpetes recomanat.**  
   A la teva carpeta de treball crea `projecte-tig/` i a dins `data/`, `sandbox/`, `results/` i `maps/`. A `sandbox/` crea la subcarpeta `balneari/`. Assegura’t que tens una estructura clara perquè és la base de tot el projecte.

2. **Descarrega un Shapefile de referència.**  
   Ves al Centre de Descàrregues del CNIG o a un portal similar i baixa una capa bàsica, com ara municipis. Desa l’arxiu `.zip` dins `data/municipis/` per mantenir intacta la versió original.

3. **Descomprimeix i copia a la sandbox.**  
   Si el fitxer és `.zip`, descomprimeix-lo dins `data/municipis/`. Obtindràs un conjunt de fitxers (`.shp`, `.dbf`, `.shx`, `.prj`, etc.). Copia aquesta carpeta sencera a `sandbox/balneari/dades/`. Recorda: **mai** treballem directament amb `data/`.

4. **Obre QGIS i crea un projecte nou.**  
   Inicia QGIS, ves a **Projecte > Nou** i desa el projecte immediatament com `sandbox/balneari/balneari.qgz`. Així estableixes el punt de referència des del qual QGIS crearà rutes relatives.

5. **Afegeix la capa i comprova les rutes.**  
   Carrega el Shapefile que has copiat a `sandbox/balneari/dades/`. Obre les propietats del projecte i revisa que les rutes estiguin configurades com a relatives. D’aquesta manera el projecte serà transportable entre ordinadors i sistemes operatius.

6. **Obre la taula d’atributs i explora les dades.**  
   Fes clic dret a la capa i selecciona **Obrir taula d’atributs**. Repassa els camps disponibles: codis de municipi, noms, població si n’hi ha… Recorda que el `.dbf` del Shapefile té limitacions (per exemple, noms de camp curts).

7. **Aplica simbologia bàsica.**  
   Obre les propietats de la capa i canvia la simbologia: tria un farciment diferenciat, ajusta els contorns o aplica un color uniforme. Això et permetrà reconèixer millor les dades al mapa i començar a treballar la representació visual.

8. **Crea una composició (Layout).**  
   Obre l’editor de composicions i prepara un mapa senzill. Recorda els elements mínims que sempre ha d’incloure una composició cartogràfica:  
   - Títol clar i llegible.  
   - Llegenda amb els símbols utilitzats.  
   - Escala gràfica.  
   - Fletxa de nord.  
   - Fonts de dades i autoria.  

   Pots afegir també una graella de coordenades si vols practicar. Desa la composició amb un nom descriptiu dins el projecte i exporta-la a `maps/` com a PDF.

9. **Desa i tanca el projecte.**  
   Desa els canvis i comprova que el fitxer `balneari.qgz` s’ha actualitzat. Aquest serà el teu primer projecte ben organitzat dins l’estructura recomanada.

> Aquesta pràctica és un punt de partida: organitzar carpetes, treballar amb còpies a la sandbox, carregar capes, aplicar simbologia, explorar atributs i produir una primera composició. Conceptes que ja coneixies, però ara integrats en una metodologia més rigorosa que seguiràs al llarg del curs.
{: .block-tip }
