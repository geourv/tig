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

Un sistema d’informació geogràfica (SIG) és la combinació de programari, maquinari, dades i coneixement per capturar, emmagatzemar, analitzar i visualitzar informació geoespacial. En aquest curs utilitzarem **QGIS** com a eina principal, però l’objectiu és més ampli: aprendre a **organitzar el treball** amb criteri perquè els projectes siguin traçables, repetibles i fàcils de compartir. Aquest primer capítol s’ocupa d’això: sistemes operatius i rutes, estructura de carpetes, criteris de nomenclatura, fitxer de projecte i gestió bàsica de comprimits.

## Sistemes operatius i rutes

QGIS és multiplataforma: funciona en Windows, macOS i GNU/Linux. Windows utilitza rutes amb barres invertides (`C:\projectes\tig\dades`), mentre que macOS i Linux en fan servir amb barres normals (`/Users/usuari/projecte` o `/home/usuari/projecte`). Quan un mateix projecte es mou entre equips i sistemes diferents, aquesta disparitat de rutes és una font típica d’errors. Per això és preferible configurar els projectes perquè apuntin a **rutes relatives** des de la ubicació del `.qgz`.

Una **ruta absoluta** indica sempre la posició completa d’un element dins el sistema de fitxers. A Windows comença per la lletra de la unitat (`C:\...`), mentre que a Linux i macOS comença des de l’arrel (`/`). Per exemple:

- Windows: `C:\Users\anna\Documents\projecte-tig\data\municipis.shp`
- Linux: `/home/anna/projecte-tig/data/municipis.shp`

En canvi, una **ruta relativa** descriu el camí a un fitxer en relació amb la carpeta on es troba el projecte. Aquesta opció és la més pràctica quan treballem amb QGIS perquè permet moure la carpeta completa del projecte sense trencar els enllaços. Les rutes relatives es basen en símbols especials:

- `./` indica la carpeta actual. Per exemple, `./dades/municipis.shp` apunta a la subcarpeta `dades` dins del projecte.
- `../` indica la carpeta superior (anar “un nivell amunt”). Per exemple, si el projecte està a `sandbox/balneari/`, la ruta `../data/municipis.shp` ens portarà a la carpeta `data` que està al mateix nivell que `sandbox`.
- Es poden encadenar: `../../` significa “pujar dos nivells”.

Això vol dir que si un fitxer de projecte `.qgz` està guardat a `sandbox/balneari/`, i la capa és a `sandbox/balneari/dades/edificis.shp`, la ruta relativa serà simplement `./dades/edificis.shp`. Si en canvi les dades són a la carpeta general `data/`, la ruta relativa podria ser `../../data/municipis.shp`.

> **Consell**: Activa i comprova l’ús de **rutes relatives** al diàleg de propietats del projecte de QGIS. Així el projecte s’obrirà igual en Windows, macOS i Linux, sense importar on es desin exactament les carpetes.
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

> **Atenció**: Conserva sempre els arxius originals a `data/` i treballa amb còpies a `sandbox/`. Així pots repetir processos i auditar el flux de treball sense risc de perdre les fonts.
{: .block-warning }

## Noms de fitxers

La nomenclatura és part del mètode i forma part de l’organització del projecte tant com les carpetes. Posar bons noms estalvia problemes i facilita la col·laboració. Quan els noms són clars i consistents, qualsevol persona que obri el projecte pot entendre immediatament què conté cada fitxer.

Cal utilitzar **minúscules** i separadors senzills (`_` o `-`), i evitar **espais**, **accents** i caràcters especials (`ç, ñ, à, é, &, %...`). Això no és una mania, sinó una necessitat pràctica: molts programes antics de SIG, i fins i tot algunes utilitats actuals, no gestionen bé aquests caràcters. Els espais es poden interpretar com a separadors d’ordres en línia de comandes, mentre que accents i símbols especials poden donar errors en programes que només esperen caràcters bàsics del conjunt ASCII. Això és especialment crític en llenguatges de programació com **Python** o **R**, molt usats en l'anàlisi de dades geoespacials.

Sobre els separadors, la majoria de sistemes operatius admeten ambdós caràcters (`_` i `-`). Ara bé, en bases de dades i en noms de camps o columnes és molt més segur utilitzar sempre `_`, ja que el guió `-` es pot interpretar com a operador de resta. Per això, un camp anomenat `nom_municipi` és clar i compatible amb **SQL** o **Python**, mentre que `nom-municipi` podria generar errors. Per tant, en projectes SIG és preferible mantenir `_` com a separador per assegurar compatibilitat.

Exemples de noms adequats serien:
`usos_sol_2023.gpkg`, `viari_municipal_utm31.gpkg`, `cens2021_municipis.shp`.

> **Consell**: Mantén un patró de noms estable (prefixos/abreviatures coherents) i documenta’l a l’inici del projecte per a ús del teu equip. Això evita malentesos i assegura la compatibilitat a llarg termini.
{: .block-tip }

## Fitxer de projecte de QGIS i formats de dades

QGIS desa la configuració del treball en `.qgs` (XML llegible) o `.qgz` (contenidor comprimit amb l’XML i recursos). El `.qgz` és l’opció recomanada perquè ocupa menys i pot incloure arxius auxiliars. En qualsevol cas, el fitxer de projecte **no conté** les dades: només guarda rutes, estils i paràmetres de visualització. Per això és important desar-lo sempre **dins** de `sandbox/<nom_projecte>/` i comprovar que les capes s’hi enllacen amb rutes relatives.

Del curs anterior coneixes el **Shapefile**, un format creat per ESRI a principis dels anys 90. Va ser l’estàndard de facto durant molt de temps, però les seves limitacions s'han fet evidents. Un Shapefile no és un sol arxiu, sinó un conjunt de fitxers que han d’anar sempre junts: com a mínim `.shp` (geometria), `.dbf` (taula d’atributs) i `.shx` (índex), i sovint també `.prj` (sistema de referència). Aquest disseny fragmentat provoca problemes de corrupció si falta un dels fitxers, i té limitacions històriques com noms de camp de màxim 10 caràcters o problemes amb caràcters especials.

Com a alternativa moderna, tenim el **GeoPackage (.gpkg)**. Aquest format, estandarditzat per l'OGC, es basa en una base de dades **SQLite** i té la gran virtut d'emmagatzemar múltiples capes (vectorials i ràster), taules i estils en un **únic fitxer**. Això redueix la dispersió d’arxius i facilita compartir dades. QGIS permet llegir i escriure directament en `.gpkg`, i molts altres programes ja ofereixen compatibilitat. Altres formats oberts i moderns que també guanyen popularitat són el **GeoJSON** per a dades web i el **Cloud Optimized GeoTIFF (COG)** per a ràsters.

Tot i que en aquesta pràctica inicial utilitzarem un Shapefile per reforçar conceptes, cal tenir present que el futur passa per formats més robustos i versàtils com el GeoPackage.

> **Consell**: El fitxer de projecte `.qgz` guarda l'estat general del treball, mentre que el GeoPackage (`.gpkg`) pot ser el magatzem de les teves dades, reduint la dispersió de fitxers i fent el projecte més manejable.
{: .block-tip }

## Comprimir i descomprimir

Moltes fonts oficials distribueixen dades en `.zip`. Convé **desar l’arxiu original a `data/`**, descomprimir-lo en una subcarpeta homònima i copiar-ne les dades de treball a `sandbox/<projecte>/`. A Windows pots utilitzar 7-Zip; a macOS i Linux tens eines integrades suficients per a la majoria de casos.

> **Consell**: Abans de començar el treball, comprova la versió exacta de QGIS (preferentment LTR) i anota-la al teu quadern de projecte. Això facilita reproduir processos i resoldre incidències.
{: .block-tip }

## Interfície bàsica de QGIS

Quan obrim QGIS ens trobem amb una finestra que combina menús, barres d’eines, panells i l’àrea principal de mapa. A la part superior hi ha la **Barra de menú**, amb entrades com **Projecte**, **Capa** o **Processament**. Just a sota hi trobem les **Barres d’eines**, amb icones que donen accés directe a funcions habituals, com la navegació, la consulta d’informació o l'edició.

A l’esquerra de la interfície apareixen els **Panells laterals**, dels quals dos són especialment rellevants: el **Panell de capes**, on s’organitzen totes les capes, i el **Panell de navegador**, que ens permet explorar carpetes locals i serveis web. A la part inferior es troba la **Barra d’estat**, que mostra informació en temps real com les coordenades del punter o el sistema de referència espacial (CRS).

Un recurs molt potent és la **barra de cerca (o localitzador)**, a la part inferior esquerra, on pots trobar qualsevol eina o funció només escrivint el seu nom.

## Pràctica

Aquesta pràctica té l’objectiu de refrescar coneixements del curs anterior i consolidar les primeres passes amb l’entorn i l’organització del treball. Segueix els passos amb calma, recordant què ja saps fer i fixant-te en les novetats de metodologia.

1. **Crea l’arbre de carpetes recomanat.** A la teva carpeta de treball, crea `projecte-tig/` i a dins `data/`, `sandbox/`, `results/` i `maps/`. A `sandbox/` crea la subcarpeta `balneari/`.

2. **Descarrega un Shapefile de referència.** Ves al Centre de Descàrregues del CNIG o a un portal similar i baixa una capa bàsica, com ara municipis. Desa l’arxiu `.zip` dins `data/municipis/` per mantenir intacta la versió original.

3. **Descomprimeix i copia a la sandbox.** Descomprimeix el `.zip` dins `data/municipis/`. Obtindràs un conjunt de fitxers (`.shp`, `.dbf`, etc.). Copia aquesta carpeta sencera a `sandbox/balneari/dades/`. Recorda: **mai** treballem directament amb `data/`.

4. **Obre QGIS i crea un projecte nou.** Inicia QGIS, ves a **Projecte \> Nou** i desa el projecte immediatament com `sandbox/balneari/balneari.qgz`. Així estableixes el punt de referència per a les rutes relatives.

5. **Afegeix la capa i comprova les rutes.** Carrega el Shapefile que has copiat a `sandbox/balneari/dades/`. Obre les propietats del projecte i revisa que les rutes estiguin configurades com a relatives.

6. **Explora i converteix la capa.** Fes clic dret a la capa i selecciona **Obrir taula d’atributs**. Repassa els camps i, a continuació, exporta la capa: fes clic dret \> **Exporta \> Desa les entitats com…**. Al diàleg, tria **GeoPackage** com a format i desa el fitxer a **`results/balneari.gpkg`**. D'aquesta manera, practiques la conversió a un format modern i robust.

7. **Aplica simbologia bàsica.** Obre les propietats de la capa i canvia la simbologia: tria un farciment diferenciat, ajusta els contorns o aplica un color uniforme.

8. **Crea una composició (Layout).** Obre l’editor de composicions i prepara un mapa senzill. Recorda els elements mínims: títol, llegenda, escala gràfica, fletxa de nord i fonts de dades/autoria. Desa la composició i exporta-la a `maps/` com a PDF.

9. **Desa i tanca el projecte.** Desa els canvis i comprova que el fitxer `balneari.qgz` s’ha actualitzat.

> **Aquesta pràctica és un punt de partida**: organitzar carpetes, treballar amb còpies a la sandbox, carregar capes, explorar atributs i, finalment, produir una primera composició i una capa en format GeoPackage. Conceptes que ja coneixies, però ara integrats en una metodologia més rigorosa que seguiràs al llarg del curs.
{: .block-tip }
