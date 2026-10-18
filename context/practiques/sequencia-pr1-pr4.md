# Preparació de PR1–PR4 i dels paquets per destinatari

Registre d’autoria i planificació. Encàrrec i reserva acceptada: [TIG #28](https://github.com/geourv/tig/issues/28), 12 d’octubre de 2026. Les fases històriques es conserven com a traça; l’aprovació actual i els productes són a `context/practiques/lliuraments.md`.

**Primera versió aprovada el 18/10/2026:** setze lectures `2026-10-v1`, 108 pàgines amb conducció docent, enunciats Moodle i criteris 70/20/10. Els vuit bundles CNIG conserven els 591 controls i les reobertures natives. PR1 explicita el contracte propi de la micropràctica confirmada amb Unaltramesa: composició opcional, sense exigència de CNIG, EPSG fix ni segon PDF. El recorregut ampliat següent manté els seus resultats pedagògics. L’índex és `practiques/README.md`; els hashes i els límits són a `context/practiques/lliuraments.md`.

## Decisions del recorregut

Es conserva la successió de sis instantànies. Aquesta unitat desenvolupa PR1–PR4; el pla de continuació recull PR5 i PR6. Vila-seca és el cas de demostració i l’alumnat transfereix el procediment a un altre municipi. L’autor ha precisat que les fonts base són CNIG; la interpretació inicial CNIG/ICGC queda superada. El complement ICGC havia estat només una via puntual i opcional d’accés a WFS.

La precisió docent del 14 d’octubre de 2026 estableix que **l’alumnat descarrega els originals i prepara les dades i el projecte**. El PDF explica aquest recorregut. Els paquets de dades i projectes preparats es destinen al professorat; el cas resolt es pot compartir explícitament com a exemple del resultat esperat. PR1 exigeix almenys una composició cartogràfica pròpia, editable i exportada a PDF.

| Fase | Seqüència | Resultat que passa a la següent fase |
| --- | --- | --- |
| PR1 | Descàrrega CNIG i metadades, originals, inspecció, selecció i exportació a EPSG:25831, GeoPackage, projecte incrustat i extern, composició pròpia | Originals documentats, base municipal, projecte transportable i mapa PDF |
| PR2 | Esquema de dades, fanals puntuals, carrils bici lineals amb ajust, plaques solars poligonals, control geomètric i temàtic | Tres capes persistents amb identificadors, procedència i estat de revisió |
| PR3 | Selecció manual, filtre de capa, filtre de taula, selecció per expressió i ubicació, exportació, calculadora; CartoCiudad, transport i descoberta ATOM cadastral | Capes heretades completes, subconjunts verificats i context per a geoprocessament |
| PR4 | Buffers i sensibilitat; retall/intersecció; diferència; unió i solapaments; envolupants i ROI | Resultats geomètrics interpretables i `roi` rectangular per al treball ràster |

La composició es treballa després del nucli tècnic de PR1 com a resultat del recorregut ampliat; és opcional en la micropràctica Moodle confirmada. Els blocs són 70% treball bàsic, 20% ampliacions i 10% documentació, equivalents a 7, 2 i 1 punts sobre 10. El professor comunica l’abast de l’activitat i el recull a Moodle, respectant els requisits de cada edició. Les guies docents incorporen preparació, durada orientativa, passos de Moodle i enunciat; les lectures d’alumnat comparteixen el criteri.

## Format compartit del LLEGIU-ME

La petició del 14 d’octubre de 2026 és preparar els esborranys i les dades de totes les pràctiques per a una revisió conjunta. Els candidats de lectura continuen en draft; la selecció de hashes per a una edició distribuïble es farà després d’aquella revisió. L’índex de revisió distingirà els originals i els casos executats de les entrades encara pendents.

### Ampliació de reserva acceptada per al conjunt

**Acceptada explícitament el 14 d’octubre de 2026**, amb la resposta «Acceptar la reserva»: 16 fonts i 29 inputs exactes. Les setze lectures i els documents de pla/índex ja estan reservats. La preparació conjunta necessita una font de càlcul del cas municipal, requests independents per fase i còpies d’entrades identificades; les funcions natives d’execució, captura, segell i reobertura continuen al proveïdor.

Fonts addicionals acceptades, amb paths exactes:

- `context/writing-profile.md`
- `practiques/recorregut-municipal/README.md`
- `practiques/recorregut-municipal/prepare_inputs.py`
- `practiques/recorregut-municipal/compute.py`
- `practiques/recorregut-municipal/pr1.json`
- `practiques/recorregut-municipal/pr2.json`
- `practiques/recorregut-municipal/pr3.json`
- `practiques/recorregut-municipal/pr4.json`
- `practiques/recorregut-municipal/reus.json`
- `practiques/recorregut-municipal/pr5.json`
- `practiques/recorregut-municipal/pr6.json`
- `practiques/recorregut-municipal/bonus.json`
- `practiques/recorregut-municipal/pr6_roi_municipal.model3`
- `practiques/recorregut-municipal/bonus_roi.py`
- `practiques/recorregut-municipal/bonus_portals.sql`
- `practiques/recorregut-municipal/bonus_postgis.sql`

Entrades addicionals acceptades, ignorades i create-only:

- `practiques/recorregut-municipal/inputs/lineas_limite_cnig_20260728.zip`
- `practiques/recorregut-municipal/inputs/cartociudad_tarragona_202604.zip`
- `practiques/recorregut-municipal/inputs/transport_tarragona_202607.zip`
- `practiques/recorregut-municipal/inputs/tarragona.gpkg`
- `practiques/recorregut-municipal/inputs/red_viaria.gpkg`
- `practiques/recorregut-municipal/inputs/mdt25_0472.tif`
- `practiques/recorregut-municipal/inputs/mdt25_0473.tif`
- `practiques/recorregut-municipal/inputs/mdt200_tarragona.tif`
- `practiques/recorregut-municipal/inputs/pr2_sintetic_original.gpkg`
- `practiques/recorregut-municipal/inputs/pnoa_vilaseca_context.png`
- `practiques/recorregut-municipal/inputs/pnoa_capabilities.xml`
- `practiques/recorregut-municipal/inputs/pnoa_vilaseca_procedencia.json`
- `practiques/recorregut-municipal/inputs/pr1-project-setup-exemple.gpkg`
- `practiques/recorregut-municipal/inputs/pr2-digitalitzacio-exemple.gpkg`
- `practiques/recorregut-municipal/inputs/pr3-consultes-exemple.gpkg`
- `practiques/recorregut-municipal/inputs/pr4-geoprocessament-exemple.gpkg`
- `practiques/recorregut-municipal/inputs/pr5-raster-exemple.gpkg`
- `practiques/recorregut-municipal/inputs/pr6-sintesi-exemple.gpkg`
- `practiques/recorregut-municipal/inputs/pr5_elevacio_25m.tif`
- `practiques/recorregut-municipal/inputs/pr5_elevacio_200m.tif`
- `practiques/recorregut-municipal/inputs/pr5_pendent_25m_graus.tif`
- `practiques/recorregut-municipal/inputs/pr5_pendent_200m_graus.tif`
- `practiques/recorregut-municipal/inputs/pr5_orientacio_25m_graus.tif`
- `practiques/recorregut-municipal/inputs/pr5_orientacio_200m_graus.tif`
- `practiques/recorregut-municipal/inputs/pr5_elevacio_classes_25m.tif`
- `practiques/recorregut-municipal/inputs/pr5_elevacio_classes_200m.tif`
- `practiques/recorregut-municipal/inputs/pr5_mascara_elevacio_pendent_25m.tif`
- `practiques/recorregut-municipal/inputs/pr5_mascara_elevacio_pendent_200m.tif`
- `practiques/recorregut-municipal/inputs/pr6_pendent_roi_graus.tif`

Les modificacions de `.gitignore` i `.unaltraweb/source-checks.json`, ja reservats, protegeixen aquestes còpies. La simplificació demanada per l’autor substitueix les exclusions individuals per les tres carpetes d’inputs del pilot, PR1 històrica i recorregut municipal. Aquesta reserva continua sent exacta: delimita l’edició, no la sintaxi dels patrons d’ignoració. Fonts, models, codi i requests continuen fora de les carpetes de dades i són versionables.

Els inputs de fases precedents només es creen després d’obtenir i comprovar els seus productes natius; els hashes no s’inventen. L’original sintètic PR2 conserva la procedència i l’estat `no_apte_per_analisi`; no acredita un inventari territorial observat. Els inputs i els artefactes ignorats es retenen, inclosos els intents i les versions prèvies.

El perfil QGIS v2 admet Shapefile amb components, GeoPackage, GeoTIFF, CSV/CSVT i recursos declarats. El bundle complet reté també les entrades d’autoria, inclosos els ZIP originals. La selecció de productes per a un paquet distribuïble no implica automàticament distribuir tots els inputs del bundle. Cal provar per separat els models i el codi: no se’n falseja el format per fer-los passar per recursos admesos.

El compositor Web consultat exigeix les dues seleccions d’alumnat/docent i hashes de lectures seleccionats per l’autor. Per a aquesta revisió conjunta es preparen PDF independents i bundles natius de revisió; les edicions finals es decidiran després. Les limitacions de composició nativa i qualsevol entrada observada que falti quedaran identificades al candidat corresponent.

El contracte consultat és el de `unaltraweb` 0.7.2, commit de release `1648e54edad794596f03ef9d36e886cd03cf946a`, especialment `docs/_documentation/en/47-private-practice-pdfs.md`. `manual_practice_pdf_build` utilitza la plantilla compartida A4 horitzontal, tipografia del manual, metadades de l’assignatura, codi 21234114, versió independent de la pràctica i logos només a la primera pàgina.

Les vuit lectures són fonts Pandoc autònomes: capçaleres, prosa, llistes, expressions i taules amb `Table:`. No utilitzen Liquid, cites Jekyll ni els wrappers de components exclusius del manual. Els enllaços a teoria són HTTPS; els futurs recursos locals necessitaran bindings explícits del compositor i una selecció per destinatari.

L’estructura comuna és finalitat, punt de partida, procediment, comprovacions, transferència i fitxers/evidències. La guia docent hi afegeix preparació de la demostració, resultats de referència, diagnòstic i límits. No es crea una còpia local de la plantilla TeX ni un empaquetador propi.

## Contracte d’herència i noms

| Fase | Base del nom de treball | Projecte principal incrustat |
| --- | --- | --- |
| PR1 | `pr1-project-setup-cognom` | `pr1` |
| PR2 | `pr2-digitalitzacio-cognom` | `pr2` |
| PR3 | `pr3-consultes-cognom` | `pr3` |
| PR4 | `pr4-geoprocessament-cognom` | `pr4` |

Cada base identifica un `.gpkg` i un `.qgz` homònims. Els apunts de l’estudiant es proposen com `<base>-apunts.pdf`, per distingir-los del `LLEGIU-ME.pdf` docent distribuït i evitar col·lisions al `dist/` pla. Aquest nom es presenta a revisió amb les lectures; no modifica retroactivament els lliuraments històrics de #10. El mapa de PR1 es proposa com `pr1-project-setup-cognom-mapa.pdf`.

La fase nova copia el GeoPackage validat de la predecessora amb QGIS tancat. Conserva físicament capes i taules, obre i reorienta els projectes que es mantinguin al contenidor nou, desa el principal amb el nom de la fase i crea un `.qgz` nou. No es copia ni es reanomena el `.qgz` predecessor. Cal inventariar i comprovar totes les vistes incrustades conservades, no només la principal.

La carpeta `tig/` de l’estudiant organitza `data/raw/`, `data/processed/`, `sandbox/` i `dist/`. Els ZIP descarregats del productor es conserven íntegres, amb les metadades; les extraccions i preparacions queden identificades. Un exemple resolt compartit s’obre separadament del treball propi. El resultat de PR3 ha de conservar `fanals`, `carrils_bici` i `plaques_solars` de PR2 encara que el cas de consultes no els utilitzi. Aquesta herència concreta està relacionada amb #12.

## Inventari de referències existents

Les observacions d’aquesta taula provenen de les fonts i els reports retinguts. Abans de reconstruir o distribuir un paquet cal verificar els bytes actuals, seleccionar-ne la closure amb el productor i repetir la reobertura que correspongui. No es declara aquí una nova execució de QGIS.

| Recurs del consumidor | Què aporta | Límit de reutilització |
| --- | --- | --- |
| `assets/projectes/vila-seca/pr1-aula/` | Originals de classe amb `vilaseca_icgc_15000`, `vilaseca_cnig`, projecte `pr1` i composició `Recordatori` | Conservar noms literals i originals; la composició de l’autor no es reconstrueix ni se sobreescriu |
| `assets/projectes/vila-seca/pr1-guia/` | Nou municipis d’entrada, exportació guiada i projectes `pr1`/`comparacio` | Cas resolt amb dues vistes; no confondre’l amb un paquet inicial sense resposta |
| `assets/projectes/vila-seca/dades_preparades/pr2-digitalitzacio-vila-seca.gpkg` | Esquemes i geometries de demostració: 3 fanals, 3 trams, 2 polígons | Totes tres capes són sintètiques, amb `estat_rev=no_apte_per_analisi` |
| `assets/projectes/vila-seca/pr3-guia/` | Consultes/exportacions CNIG verificades i nou capes locals de la guia | Exemple resolt; no acredita per si sol l’herència completa d’una PR2 d’estudiant |
| `context/practiques/pr3-sources.yml` | Edicions, recursos oficials i hashes dels tres ZIP CNIG | Cal comprovar la disponibilitat dels originals i no substituir-los silenciosament per edicions noves |
| `assets/projectes/vila-seca/dades_preparades/projecte_tig.gpkg` | `municipi_treball` CNIG, una entitat EPSG:25831 | Font del pilot autònom; cal contrastar-la amb l’edició CNIG i la transformació utilitzades al cas nou |
| `sandbox/practiques/tig-buffer-municipal-500m/run-04-validated/` | Pilot de buffer 500 m, 8 segments/quadrant, 30 controls retinguts | Cas acotat, no paquet PR4 complet; es conserva sense recalcular ni canviar el segell |

Els originals de classe tenen els SHA-256 documentats `88075560914a0da195dab9540325a7390f49d6b6cdf237c72639e3271c0f7ad9` (GPKG) i `7147be541f7da8f487ebb1e1d3ef3b9f1602f01a109f7c21e7468c161d4cc050` (QGZ). La font del pilot té SHA-256 `46aa316b88ec9f6eac559ca4f2037f1e142a997d3c0722febb8912a9a03654dd`; el segell del run-04 és `8bf979b7cc6c60312fb0a5421ab8a5f9b82bdd7d4cd128778e1ce73247dfcaff`. L’inventari complet del pilot continua a `context/practice-retention.json`.

## Materials d’aprenentatge i paquets docents

| Pràctica | Recorregut de l’alumnat explicat al PDF | Paquet docent a preparar |
| --- | --- | --- |
| PR1 | Descarregar originals CNIG, registrar metadades, preparar el municipi, crear projecte i composició propis | Originals íntegres, preparacions identificades, projecte resolt reobrible, composició completa i controls |
| PR2 | Partir de la PR1 pròpia, crear esquemes i capturar les tres geometries amb procedència i revisió | Base de demostració, inventari observat quan l’autor l’aporti i cas sintètic separat si s’utilitza |
| PR3 | Conservar la PR2 pròpia, obtenir fonts CNIG/Cadastre amb cobertura adequada i preparar les consultes | Originals, base acumulativa i resultats de filtres/exportacions/càlculs, mapa i controls |
| PR4 | Partir de la PR3 pròpia, documentar els generadors i derivar geometries, solapaments i ROI | Base acumulativa, escenari sintètic identificat, variants de buffers, superposicions i controls |

El lliurament ordinari a l’alumnat és el PDF amb instruccions de descàrrega i preparació; el paquet inicial preparat deixa de ser el model general. Un checkpoint docent pot ajudar a reprendre una demostració. Un exemple resolt de Vila-seca, si es comparteix, s’identifica com a tal i permet examinar el resultat esperat; el treball propi continua exigint obtenció de dades, preparació i resolució sobre l’altre municipi.

Els PDF d’instruccions es poden construir independentment amb `manual_practice_pdf_build`. Els noms físics dels productes docents, les dependències i els hashes finals s’han de fixar després de preparar les entrades reals. Cal provar que el contracte de productes conserva i transporta els originals requerits i admet el lliurament docent/exemple acordat; no s’adapta l’objectiu docent per generar automàticament un ZIP inicial d’alumnat.

La versió 0.6.0 del productor ja havia limitat el cas anterior a mapes/text, sense WMS ni items natius de llegenda i barra d’escala. Una composició parcial no acredita el mapa resolt complet requerit ara. El suport de les dependències i de la composició final s’ha de verificar amb el proveïdor abans de segellar la nova edició. Les sortides noves continuen en arrels ignorades i create-only, amb reserva exacta dels inputs nous.

## Font CNIG inspeccionada per a PR1

La inspecció en lectura amb GDAL/OGR 3.8.4 ha comprovat `tmp/pr3-guided/browser/LINEAS_LIMITE.ZIP`, SHA-256 `d752b1b943e6c60f46a23119d6c3d4ad0b198461c502f0a5433197d7a5e34c83`. El recinte municipal s’ha obert també directament dins del ZIP, sense crear una distribució nova.

La capa `recintos_municipales_inspire_peninbal_etrs89` conté 8.132 registres, amb `NATCODE` i `INSPIREID` únics i CRS EPSG:4258. La inspecció de la capa extreta observa 8.132 geometries vàlides i cap geometria buida. Vila-seca és una entitat vàlida amb `NAMEUNIT=Vila-seca`, `NATCODE=34094343171`, `CODNUT2=ES51` i `CODNUT3=ES514`.

El filtre català retorna 948 recintes; inclou `Comunidad de El Pont de Bar y Cava`, codi `34092553055`. El filtre provincial `CODNUT3=ES514` retorna 184. Són propietats observades de la distribució, no recomptes que s’hagin d’igualar als d’ICGC o d’una altra edició.

S’han consultat la fitxa oficial CNIG i el servei IGN/PNOA. La capa de visualització és `OI.OrthoimageCoverage`; `OI.MosaicElement` informa de data i resolució. Una consulta puntual a l’entorn de Vila-seca va retornar juliol de 2024 i 0,25 m. Aquesta dada no s’extrapola a tota l’extensió ni a un extracte de context reescalat. Encara no s’ha descarregat ni segellat un nou extracte PNOA.

## Fanals, unió i recompte de cobertura

El constructor històric conté tres punts alineats amb separació de 45 m. Són una base possible per a un escenari geomètric controlat, no coordenades observades de fanals. Qualsevol reutilització per a PR4 ha de mantenir aquesta procedència, conservar el registre original i identificar la còpia com `fanals_sintetics`. No es canvia `no_apte_per_analisi` per fer passar dades sintètiques per un inventari validat.

Es proposen radis de 10, 30 i 50 m sobre aquest escenari: permeten discutir absència, coincidències de dos generadors i coincidències de tres. Són prediccions geomètriques per validar, no resultats d’una execució ni radis d’il·luminació. Els buffers mantenen `id_fanal`; la dissolució calcula la petjada conjunta, mentre que la unió subdivideix segons fronteres.

La documentació QGIS 3.44 de `native:union` diferencia dos modes. Sense `OVERLAY`, divideix solapaments de la mateixa capa però genera peces coincidents per als diferents participants. Amb una segona capa, talla entre capes i no resol els solapaments interns de cadascuna. Per obtenir zones exclusives amb `n_fanals` cal conservar la unió bruta com a evidència, obtenir les peces geomètriques úniques i comptar identificadors diferents dels buffers que cobreixen un punt interior de cada peça. El flux concret s’haurà d’executar i validar amb casos d’un, dos i tres generadors abans de segellar el paquet PR4.

La redacció general del capítol 6 sobre els solapaments interns de `native:union` s’haurà de matisar en una revisió posterior per explicitar aquesta diferència entre modes. En aquesta unitat es conserven els capítols aprovats i les lectures noves segueixen el contracte de l’ajuda 3.44 consultada.

Controls previstos: IDs d’entrada únics, peces amb interiors disjunts, valors enters entre 1 i N, cobertura equivalent a la dissolució i identitat ponderada `sum(n_fanals * area_peca) = sum(area_buffer_individual)` dins d’una tolerància justificada. La zona de zero generadors exigeix un univers finit explícit i una diferència; no apareix espontàniament a la unió. Cap d’aquests recomptes mesura il·luminància.

## ROI de continuïtat

Es compararan l’envolupant rectangular alineada als eixos d’EPSG:25831, el rectangle mínim orientat, l’envolupant convexa i el cercle mínim contenidor sobre la mateixa entrada `municipi_buffer_500m`. El cercle mínim i l’envolupant convexa són operacions diferents. La ROI de continuïtat serà el rectangle alineat als eixos, desat com `roi`, amb contenció del buffer i extrems documentats. L’ajust posterior a origen i mida de cel·la pertany a PR5 i pot ampliar aquest rectangle.

Cal identificar explícitament l’edició CNIG i la preparació que alimenten el cas nou; no s’assumeix identitat de bytes o geometries amb el pilot anterior. Les toleràncies del pilot de 8 segments, inclosa la banda de distàncies contrastada, no es generalitzen a altres radis, geometries o paràmetres sense una nova justificació.

## Revisió següent

1. Revisar les lectures amb el criteri de descàrrega i preparació autònomes; PR1 incorpora composició obligatòria i els noms proposats d’apunts/mapa.
2. Delimitar el tram de Joanot Martorell, els carrils i la unitat poligonal de les plaques; rebre o revisar les observacions de classe. Es pot avançar el model amb l’escenari sintètic separat.
3. Reservar els paths nous, verificar els originals i preparar els paquets docents i exemples resolts amb el productor compartit, reconstruint la cadena en destins nous.
4. Executar i comprovar PR4; revisar les comparacions, el recompte de solapaments i la ROI amb l’autor.
5. Renderitzar les lectures corregides en jobs nous, revisar-les amb l’autor i fixar els hashes seleccionats; els PDF anteriors són evidència històrica.
6. Compondre les edicions, verificar inventari i reobertura dels ZIP extrets, i acordar la retenció durable abans del lliurament a Moodle.

## Validació i PDF de la preparació inicial

Els resultats següents corresponen a les lectures anteriors a la correcció CNIG i a la precisió sobre la descàrrega autònoma. La revisió conjunta vigent utilitza `2026-10-r4`, documentada a `context/practiques/lliuraments.md`. La revisió humana i la selecció dels nous hashes encara són pendents.

Les vuit fonts passen `prose-check` per selecció explícita de cada lectura privada: vuit fitxers comprovats, català, cap omissió i cap error. Es conserva un únic avís informatiu sobre una frase de 41 paraules a la guia docent de PR1; no és un criteri d’aprovació editorial.

`manual-practice-pdf-build` ha produït els vuit PDF amb `publishes=false`, versió `2026-10-r1` i run `revisio-02`. Cada job és `sandbox/practiques/<slug>/lectura-2026-10-r1-ca-<destinatari>-revisio-02/` i conserva `receipt.json`, snapshots d’entrada, PDF, preview i informes. L’índex `practiques/README.md` enllaça les fonts i aquests PDF locals.

| Pràctica | Destinatari | Pàgines | SHA-256 del PDF |
| --- | --- | ---: | --- |
| `pr1-project-setup` | alumnat | 5 | `d82247c5a9176bccd4bef3cc72ee391b72647b857bacca97be426a8dc4f530a7` |
| `pr1-project-setup` | docent | 4 | `0544adb8828e18972898c2c2ce6ac960e7c6139211125a4f960406e19d5a21a7` |
| `pr2-digitalitzacio` | alumnat | 5 | `a488558aa4f00b09fdb53ae2813f86c25495806852f4d90449e1b2cb0ceb1773` |
| `pr2-digitalitzacio` | docent | 4 | `f29413b8b64e3c94d92a075f1adabbf0ba2b79fcaaf1bafb7521d9705416d176` |
| `pr3-consultes` | alumnat | 6 | `07846d42bae08ea310d21656c3f7a2b6193b413ca8088467384dc0252348b315` |
| `pr3-consultes` | docent | 5 | `ad6a292a69ded7d64abd7eae68071eb6d0ba4cb8560b3b7b4b42967e78dbd12b` |
| `pr4-geoprocessament` | alumnat | 6 | `be1df6bb02b2877d1ecd3c50660150fc0a65f587606dff4061b11b6c7f740146` |
| `pr4-geoprocessament` | docent | 5 | `606747a44f09aefa7c5b509ddc83b68dd87d28a9feda0820459d075d278ab07e` |

La primera renderització, `revisio-01`, es conserva. La inspecció dels PDF va detectar numeració `0.1` en començar el Markdown a nivell 2, un literal de capa massa llarg dins de la taula de PR3 i dues expressions amb cometes alterades en codi en línia de la guia docent de PR3. Les fonts noves utilitzen nivell 1 per a les seccions del document autònom i nivell 2 per als apartats, situen el literal llarg en prosa i presenten les expressions en blocs SQL. A `revisio-02` s’han revisat les vuit primeres pàgines i els dos PDF complets de PR3, comprovant la numeració i les expressions corregides. La resta del contingut havia estat llegit als vuit PDF de la primera renderització. La revisió humana continua pendent.

La conversió de `"CODNUT3"` a `ÇODNUT3"` i de `"clased"` a `çlased"` en el codi en línia de `revisio-01` queda com a incidència a traslladar al core de PDF. El canvi de representació en aquestes fonts evita l’error en les expressions de les lectures; no afirma que el renderitzador hagi estat corregit. Els informes de renderització poden conservar avisos TeX de codificació TU i configuracions de captions no utilitzades, que no han impedit construir els PDF.

## Entorn de la preparació inicial

La inspecció inicial ha observat la cohort instal·lada Web 0.7.2 / QGIS 0.6.0, però el canal Web MCP s’ha tancat després de timeouts. La CLI nativa lleugera de l’host ha retornat un error de lectura de YAML (`duplicate YAML key: values`) amb cobertura zero; aquest intent no es compta com a validació. El mateix `_config.yml` és acceptat per la CLI del controlador complet, que és la que ha comprovat les lectures i construït els PDF.

S’ha utilitzat la interfície pública CLI dins del controlador ja preparat `sha256:576dcd772f2c345fa2021745f975f8392568d8d2783f7a66ba41a3521b3bd546`, amb execucions acotades i serials, xarxa desactivada, muntatges i labels natius i `reap-session` sobre l’ID exacte de cada contenidor. El worker PDF coincideix amb el digest publicat `1bb3f2dafd741e96c28639ec1cc8ccaeb81cbaa73e649f787c0b4ef59997bd4b`, ID `sha256:618163d3f924439792b2306617bd9612f566c5881166102fa544b4e782d569fa`. Les sessions efímeres retornen recursos alliberats; els jobs PDF es retenen.

El canal QGIS s’ha observat connectat, amb la mateixa instància `1838af43-0264-42a7-848f-e5738bf1257c`, binding TIG i sense drift ni workers actius. No s’ha executat cap model GIS nou en aquesta unitat. La reconnexió del canal Web és una operació separada de la preparació de fonts i no s’ha simulat amb canvis de configuració.

El diagnòstic del consumidor continua assenyalant pins de scaffold 0.7.1 i un conflicte local de `.gitignore`; no s’ha aplicat cap migració per preparar aquestes fonts. `_config.yml` conserva el SHA-256 `26c5b2947af97a0eeef000d1cc2ee8ed34e8673e67a4a49ae4c084c02d4de342` i `opencode.json`, `c1c98321c77c205f78ae9c36cb79ff69016cc9fcb38a165dc24da74157acd6b0`. No es declara un nou `site_check` global ni un build públic del manual: s’ha validat el circuit de lectures privades.

## Fonts de contracte

- [PDFs privats de pràctiques, unaltraweb 0.7.2](https://github.com/dosquartsdedocs/unaltraweb/blob/1648e54edad794596f03ef9d36e886cd03cf946a/docs/_documentation/en/47-private-practice-pdfs.md).
- [Unió i altres superposicions, QGIS 3.44](https://docs.qgis.org/3.44/en/docs/user_manual/processing_algs/qgis/vectoroverlay.html#union).
- `context/writing-profile.md`, `context/practiques/pr1-project-setup.md`, `context/practiques/pr3-filtres-expressions.md` i `context/practiques/pr3-sources.yml`.
