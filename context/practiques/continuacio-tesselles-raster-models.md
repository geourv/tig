# Continuació: tessel·lacions, ràster, model de Processament i bonus

Registre d’autoria i planificació. L’ampliació de [TIG #28](https://github.com/geourv/tig/issues/28#issuecomment-6138980980) es va acceptar a la mateixa branca `content/28-practiques-municipals`, conservant les fonts anteriors. Els preflights de continuació informaven `dirty-checkout` pels canvis propis; no es presenten com a resultats ELIGIBLE.

**Primera versió aprovada el 18/10/2026:** els casos de Reus, PR5, PR6 i bonus formen part dels vuit bundles docents. Les setze lectures actuals són `2026-10-v1`, amb 108 pàgines, conducció docent, enunciats Moodle i criteris 70/20/10. PR1 s’ha harmonitzat amb l’abast de la micropràctica confirmada. L’índex, els hashes, els resultats i els límits són a `practiques/README.md`, `practiques/recorregut-municipal/README.md` i `context/practiques/lliuraments.md`. Les inspeccions i la proposta inicial es conserven com a antecedents.

## Encaix docent i enunciats

| Bloc | Pregunta principal | Producte observable |
| --- | --- | --- |
| Activitat de PR4: Reus | Quina zonificació postal aproximada es pot inferir dels portals amb codi conegut? | Generadors auditats, Delaunay, Voronoi, zones dissoltes per codi i diagnòstic de vores |
| PR5: ràster | Com afecten graella, NoData, resolució i llindars la lectura del relleu? | Mosaic i controls de retall, derivats/classificacions de demostració i deu GeoTIFF de la comparació controlada |
| PR6: model i síntesi | Com es converteix un procediment petit i validat en una eina reutilitzable? | Model municipi → buffer → caixa envolupant, comparació manual/lot/model, extensió documentada i paquet final auditat |
| Bonus opcional | Com es reprodueix una operació coneguda amb PyQGIS o SQL espacial? | Codi explicat, entorn identificat i comparació amb el resultat de QGIS |

Reus és una activitat dins de PR4, no una setena instantània. La transferència de l’alumnat manté el municipi propi i la base `pr4-geoprocessament-cognom`. PR5 i PR6 conserven els noms contractuals `pr5-raster-cognom` i `pr6-sintesi-cognom`.

Hi ha memòria documental del patró d’enunciat a [TIG #10](https://github.com/geourv/tig/issues/10). L’autor ha adoptat **70% treball bàsic, 20% ampliacions i 10% documentació**, amb màxims de 7, 2 i 1 punts. Les guies docents incorporen el patró de Geodisseny: preparació i durada orientativa, passos de Moodle, enunciat per copiar i ampliacions amb pregunta, controls i interpretació. El professor selecciona els apartats obligatoris a classe i els recull a Moodle; la guia completa no és tota obligatòria. Calendari i tramesa es concreten a la Tasca. Els textos tenen aprovació de primera versió.

Reus s’imputa a PR4, com a bàsic o com a ampliació segons la selecció anunciada; no es puntua dues vegades. A PR6, la síntesi guiada és nucli i una funcionalitat pròpia addicional pot contribuir al 20%. El bonus és una altra via opcional d’aquell bloc, sense punts extra sobre 10. La documentació també suma respecte dels 7 punts màxims del bloc bàsic.

## Reus: comprovació real de les entrades

S’ha consultat SQLite en mode `mode=ro&immutable=1`, amb `query_only=ON`, sobre:

`tmp/pr3-guided/inputs-exact/cartociudad/CARTOCIUDAD_CALLEJERO_TARRAGONA/tarragona.gpkg`

SHA-256 comprovat: `75b3523872d582ece5dfa2edd488674852557d898bf65f36b511e45be695f90e`. La font correspon al paquet CartoCiudad Tarragona 04/2026 fixat a `context/practiques/pr3-sources.yml`. La taula `portalpk_publi` declara geometria POINT i EPSG:4258. Els camps pertinents observats són `id_porpk`, `tipo`, `cod_postal`, `ine_mun`, `municipio`, `fuente_datos` i `fecha_modificacion`.

La selecció atributiva `municipio=Reus` i `tipo=Portal` retorna 17.483 registres, tots amb `ine_mun=43123`, 17.483 `id_porpk` diferents i cap codi postal buit/nul ni geometria SQL nul·la. No és encara una selecció espacial pel terme ni una comprovació de validesa geomètrica.

| `cod_postal` | Portals atribuïts a Reus |
| --- | ---: |
| 43110 | 1 |
| 43201 | 2.498 |
| 43202 | 1.319 |
| 43203 | 1.494 |
| 43204 | 4.169 |
| 43205 | 4.618 |
| 43206 | 3.377 |
| 43330 | 1 |
| 43470 | 1 |
| 43480 | 5 |

S’han observat 54 grups de BLOB geomètric exactament coincident que reuneixen 388 registres. Això deixa 17.149 BLOB geomètrics diferents en aquest subconjunt. No hi ha codis postals diferents dins d’aquests grups del subconjunt de Reus. Cal tornar a comprovar coincidències geomètriques i proximitats després de preparar i reprojectar el conjunt complet, inclosos els generadors externs: la comparació de bytes no substitueix aquesta prova.

Els vuit registres amb codis fora del conjunt 43201–43206 són casos per revisar amb coordenades i procedència, no errors demostrats. No s’eliminaran per obtenir un mapa més compacte. La distinció entre atribució municipal i posició respecte del terme forma part de l’activitat.

## Mètode proposat per a tessel·lacions

1. Preparar límit de Reus i portals d’un entorn suficient, conservar originals i reprojectar explícitament a EPSG:25831.
2. Auditar tipus Portal/PK, IDs, codis com a text, coordenades, duplicats i possibles conflictes. Una ubicació coincident amb el mateix codi pot generar un únic punt amb una taula de correspondència als registres originals. Un conflicte de codis o un codi desconegut necessita una regla explícita.
3. Construir Delaunay i Voronoi sobre el mateix conjunt de generadors. Els codis postals són categories: no s’interpolen numèricament sobre triangles.
4. Garantir que l’extensió de construcció del Voronoi cobreixi el terme; retallar després a l’àmbit d’informe i conservar els generadors externs que hi influeixin.
5. Dissoldre les cel·les pel codi i identificar el resultat com a zonificació estimada per proximitat. No afirmar que reprodueix límits postals oficials.
6. Comprovar partició, cobertura, IDs i sensibilitat de vora; utilitzar portals reservats o blocs espacials per a un contrast que no reutilitzi tots els generadors com a prova d’exactitud.

La pertinença d’un generador a la cel·la del seu propi codi comprova consistència de construcció, no capacitat predictiva. El conjunt de validació es separa abans de construir el model, agrupant ubicacions duplicades. El cas posterior ha executat entorns rectangulars de 1.500/3.000 m, amb blocs reservats de 500 m: 4.092 ubicacions de validació i 3.435 coincidències, 83,94%. No s’han observat canvis de categoria dins del terme entre aquells dos entorns; no és una garantia sobre qualsevol marge.

## PR5: base ràster disponible i seqüència

Els capítols 7 i 8 i `assets/projectes/vila-seca/build_raster_workflows.py` ja documenten la base. Les tres fonts principals s’han hash-verificat en aquesta continuació:

| Entrada sota `tmp/unaltracaptura-qgis/cache/prepared/` | SHA-256 |
| --- | --- |
| `cnig/mdt25/source/pnoa_mdt25_etrs89_hu31_0472_lid.tif` | `325b8028bc99d4726cfdd9cb777de0ac06ed815a62da2b0e313c0c17daf4bb7c` |
| `cnig/mdt25/source/pnoa_mdt25_etrs89_hu31_0473_lid.tif` | `827b2a41b61a9636178847137647fb46f07d4f227165279d1487e757921f22bf` |
| `cnig/mdt200/source/pnoa_mdt200_etrs89_hu31_tarragona.tif` | `1827b96fd3c2d1f7cc6cb41b169fecd98ecade31581debc5264158aa3b65b118` |

Els recursos CNIG són 9074092, 9074093 i 9074255. El MDT05 0473, recurs 9072569, aporta la comprovació zero/NoData del manual, però no s’ha tornat a verificar aquí. Tampoc no s’han recalculat els resultats ràster històrics.

La seqüència diferencia mosaic, retall rectangular alineat, retall per màscara, derivats calculats amb context, reclassificació i vectorització. «Sense i amb NoData» s’interpreta com conservar les absències de la font i observar les absències addicionals del retall per màscara, no prometre que qualsevol rectangle sigui complet ni omplir els buits amb zeros.

El cas de la Pineda utilitza la calculadora ràster per a `elevacio < 2 m`; després de vectoritzar, el filtre i la calculadora de camps operen sobre polígons i atributs. Es presenta com a cribratge de cotes baixes, amb contrast amb cartografia oficial d’inundabilitat quan se n’hagi verificat producte, cobertura, fenomen i escenari. No es deriva un mapa d’inundació només del llindar. El portal SNCZI de MITECO s’ha consultat; no s’ha descarregat ni validat encara cap capa oficial específica de la Pineda.

Es conserva la distinció entre dos productes oficials 25/200 m amb orígens desplaçats 12,5 m i l’experiment controlat amb font comuna, origen compartit i niament 8 × 8. Els deu GeoTIFF contractuals del capítol 7 continuen sent els de la comparació controlada. Les demostracions de cota baixa, sectors d’orientació i pendent percentual no els substitueixen ni afegeixen nous requisits avaluats de manera implícita.

## PR6: harmonització de la ROI i petit model

La ROI acordada per la nova PR4 és la caixa alineada als eixos construïda sobre el buffer municipal de 500 m. El capítol 8 existent, en canvi, denomina ROI el buffer mateix i en fixa 10 segments/quadrant amb dissolució. No s’afirma equivalència entre aquell cas i el model nou.

El model nou `pr6_roi_municipal.model3` formalitzarà el cas de PR4: una entitat municipal vàlida EPSG:25831, marge en metres, buffer amb 8 segments/quadrant, extrems i unions arrodonits, límit de mitra 2, dissolució desactivada i caixa envolupant alineada als eixos. El buffer i la caixa tindran noms diferents. L’execució manual, el lot de 250/500/750 m i el model compararan el mateix graf i els mateixos paràmetres; no només una part del procés.

El nucli del model continua petit i reutilitzable. Les ampliacions poden afegir selecció municipal per codi, paràmetres de preparació o una altra branca ja treballada. Si se’n presenta una dins del 20%, cal justificar-la i definir-ne controls abans d’encadenar més nodes. La seqüència integrada de relleu i `pr6_pendent_roi_graus.tif` formen part de la síntesi guiada, amb màscara i graf identificats; repetir-los no es compta també com a ampliació.

La documentació QGIS 3.44 confirma tant `.model3` extern com **Save Model in project**. S’ensenyen tots dos desaments; desar una representació no garanteix actualitzar l’altra. El cas calculat ja executa el model extern a Vila-seca i Reus i el reté com a input seleccionable verificat. La representació incrustada i la seva comprovació nativa continuen sent una tasca separada; no se’n dedueix el suport només del schema o de l’èxit del fitxer extern.

Els capítols aprovats no s’han modificat en aquesta reserva. Caldrà una reserva posterior per harmonitzar els passatges de ROI del capítol 8 i les remissions corresponents abans de considerar tancat el recorregut.

## Bonus

PyQGIS i SQL són opcions posteriors al model gràfic obligatori. El bonus reutilitza una operació i unes entrades conegudes, i exigeix comparació amb el resultat de QGIS. El cas posterior executa PyQGIS i SQLite sobre GeoPackage i els contrasta amb PR6 i els 3.584 portals municipals. La font PostGIS es conserva com a exemple opcional, sense execució de servidor acreditada.

## Materials d’aprenentatge i paquets docents

La precisió de l’autor del 14 d’octubre de 2026 situa la descàrrega d’originals i la preparació de dades dins del treball de l’alumnat. Els PDF n’expliquen el procediment. Els paquets preparats es destinen al professorat i els casos resolts es poden compartir explícitament com a exemples. La taula indica què obté o conserva cada estudiant, no un ZIP inicial que rebi ja preparat.

| Bloc | Dades que l’alumnat obté o conserva | Material docent | Comprovació determinant |
| --- | --- | --- | --- |
| Reus | Descarrega portals i límit CNIG, prepara l’entorn i documenta la correspondència dels generadors | Originals, preparacions, Delaunay/Voronoi, zones per codi, incidències i controls | Vores, generadors coincidents i validació independent |
| PR5 | Conserva la PR4 pròpia i la ROI; descarrega tessel·les MDT amb metadades i les prepara | Originals, mosaics/retalls, derivats, casos NoData, comparació controlada i taules | Graelles, unitats, domini vàlid i conservació dels deu GeoTIFF |
| PR6 | Conserva la PR5 pròpia completa i els deu GeoTIFF amb els noms originals | Base de demostració, model resolt, resultat manual/lot/model i ampliació de referència | Reexecució i reobertura sense dependències del perfil personal |
| Bonus | Treballa sobre una còpia del resultat propi amb l’entorn indicat al PDF | Entrades d’exemple, codi i comparació verificada | Mateixes precondicions, semàntica i toleràncies |

Els exemples de Vila-seca/Reus mostren procediments i resultats; l’estudiant continua el municipi propi i documenta l’obtenció de les dades. Fonts i lectures són autoria; originals, dades preparades, jobs i futurs PDF/ZIP es retenen fora de Git amb el circuit compartit. Les lectures i els paquets d’aquesta continuació s’han d’harmonitzar amb el criteri abans de fixar una edició.

## Fonts consultades i estat de les eines

- `_chapters/ca/06-analisi-geoprocessament-vectorial.md`, seccions de tessel·lacions; capítol 7, preparació/derivats/àlgebra i contracte PR5; capítol 8, model, síntesi i bonus.
- [Dissenyador de models, QGIS 3.44](https://docs.qgis.org/3.44/en/docs/user_manual/processing/modeler.html).
- Implementació `QgsBoundingBoxAlgorithm` de la branca QGIS `release-3_44`: nom `boundingboxes`, caixa ordinària per entitat, camps de mida i mesura. S’ha contrastat el contracte del node; no s’ha executat un model nou.
- [ST_Buffer](https://postgis.net/docs/ST_Buffer.html) i [ST_Envelope](https://postgis.net/docs/ST_Envelope.html), documentació del projecte PostGIS.
- [SNCZI, MITECO](https://www.miteco.gob.es/es/agua/temas/gestion-de-los-riesgos-de-inundacion/snczi.html).
- CLI pública `practice-schema --profile qgis-practice-v2`, productor instal·lat 0.6.0, schema SHA-256 `528c8be229c72c346f134ffaa60094f94224094a25b6fb11bcc87802ddc7fffb`.

La CLI del controlador Web publicat ha revalidat `site-context`, llengua catalana i capacitats de lectures privades A4 horitzontals. `site-doctor` manté l’error del pin MCP 0.7.1 del scaffold i els avisos de Gem/scaffold ja documentats; no s’ha canviat la selecció persistent ni migrat el consumidor. Els processos efímers de consulta es tanquen amb el `reap-session` natiu exacte. La validació del circuit privat no es presenta com un nou build ni un `site_check` públic del manual.

## Lectures renderitzades de l’ampliació inicial

Les vuit lectures noves passen `prose-check` amb selecció explícita: vuit fitxers comprovats, català, cap omissió, cap finding ni avís. S’han produït els vuit PDF amb `manual-practice-pdf-build`, versió `2026-10-r1`, plantilla comuna A4 horitzontal, marca ESBORRANY i `publishes=false`.

Els jobs segueixen el patró `sandbox/practiques/<slug>/lectura-2026-10-r1-ca-<destinatari>-<run>/`. Cadascun conserva snapshots, PDF a `outputs/LLEGIU-ME.pdf`, preview, informes i `receipt.json`. L’índex `practiques/README.md` enllaça les fonts i les versions actuals.

| Bloc | Destinatari | Run | Pàgines | SHA-256 del PDF |
| --- | --- | --- | ---: | --- |
| `pr4-tessellacions-reus` | alumnat | `revisio-01` | 5 | `8481ae815aa105a38e5e15f5bf3ddfaaa7da0bcc4dd87ac830c4a80b5e7ec670` |
| `pr4-tessellacions-reus` | docent | `revisio-01` | 5 | `7806bb3df6d67d005840ebd49684e13df95bde98b145bfd83c843d1c97be289c` |
| `pr5-raster` | alumnat | `revisio-01` | 6 | `490ed26459e5944b64d2ec54f4082febb5aa6791d943090f6bbc76ad5a2c31cb` |
| `pr5-raster` | docent | `revisio-02` | 5 | `592cb5eb1e6162a7b1773add94776444cceccd176f1a2c5f76e296165c60d542` |
| `pr6-sintesi` | alumnat | `revisio-01` | 5 | `c9993a7426654e867e52405fef5b1ccff1216b8b30464289d6c49afdf830d42a` |
| `pr6-sintesi` | docent | `revisio-01` | 5 | `a33c0beb696346bfaa00d1b6bf967a91c555e6590c0372e6708ee8b0e66b151e` |
| `bonus-pyqgis-sql` | alumnat | `revisio-01` | 5 | `4f901f121495e37778ffdc0f016155a988a00da6b50089b0869a98c46e605779` |
| `bonus-pyqgis-sql` | docent | `revisio-02` | 4 | `ee0282b53c08326067b0a08e704d0df65573eed9ef57a292f3e0fb2ae81b4432` |

S’han obert els vuit PDF i revisat text, taules, expressions, fórmula de conversió i presentació de les primeres pàgines. La segona renderització de PR5 docent corregeix l’espai tipogràfic de la coma decimal en matemàtiques; la del bonus docent introdueix els dos entorns SQL i evita deixar el títol de secció sense text al peu de pàgina. Totes dues fonts s’han tornat a comprovar i els PDF nous s’han reobert. Els primers jobs continuen retinguts.

El controlador és el publicat `sha256:576dcd772f2c345fa2021745f975f8392568d8d2783f7a66ba41a3521b3bd546`; el worker PDF observat és `sha256:618163d3f924439792b2306617bd9612f566c5881166102fa544b4e782d569fa`, corresponent al digest publicat `1bb3f2dafd741e96c28639ec1cc8ccaeb81cbaa73e649f787c0b4ef59997bd4b`. Les execucions han estat serials, acotades, sense xarxa i amb teardown natiu exacte, que informa de recursos alliberats. No s’ha modificat cap plantilla ni sortida generada a mà.

La comprovació de prosa i la renderització inicials no acreditaven per si soles l’execució científica. Els bundles posteriors sí que incorporen els càlculs de Delaunay/Voronoi, els ràsters, el model extern i el bonus PyQGIS/SQLite, amb controls i reobertures. La revisió i aprovació humana de les lectures i dels enunciats continua pendent; les edicions distribuïbles es fixaran després de la revisió conjunta.
