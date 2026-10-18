# PR1: instruccions, originals i cas resolt docent

Fonts d’autoria de la pràctica; reserva acceptada a [TIG #28](https://github.com/geourv/tig/issues/28#issuecomment-6153809062). El productor QGIS compartit és responsable dels snapshots, els projectes, la inspecció de recursos, les captures, l’exportació i el segell. Unaltraweb és responsable dels LLEGIU-ME PDF, la selecció per destinatari i els PDF/ZIP de l’edició.

## Criteri docent actual

La [micropràctica Moodle confirmada el 18/10/2026](revisio/moodle-confirmed-2026-10-18/README.md) conserva una edició de correcció independent: tres blocs 70/20/10, composicions opcionals i cap exigència de CNIG, EPSG fix o PDF de mapa separat. El recorregut ampliat descrit a continuació no n'afegeix requisits. El motor i els checks de correcció pertanyen a Unaltramesa.

En el recorregut ampliat, l’alumnat descarrega els originals CNIG, en conserva les metadades i prepara dades, GeoPackage, projecte i composició pròpia. Les lectures identifiquen quins requisits corresponen a la micropràctica confirmada i quins a aquella via ampliada. El paquet preparat es destina al professorat; el cas resolt de Vila-seca es pot compartir com a exemple identificat.

El material docent conserva originals, preparacions identificades, projecte resolt i controls. El constructor vigent és el [recorregut municipal](../recorregut-municipal/README.md), amb reserva conjunta [acceptada](https://github.com/geourv/tig/issues/28#issuecomment-6175858065) i el criteri incorporat a `context/writing-profile.md`. La composició completa manté els límits del productor explicats a l’índex.

El paquet CNIG vigent és `sandbox/practiques/pr1-project-setup/run-cnig-01/`, segell `2fdbd4d06815f3e5934ee8ff02f9c507cbd0548def53ca4b2487dd683921860b`, amb 20 controls i reobertures natives. El [projecte](../../sandbox/practiques/pr1-project-setup/run-cnig-01/payload/projects/pr1-project-setup-exemple.qgz) i el [mapa de revisió](../../sandbox/practiques/pr1-project-setup/run-cnig-01/payload/figures/mapa-revisio.pdf) s’obren conservant tota la carpeta del paquet.

**Estat executable: edició anterior superada.** `prepare_inputs.py`, `activity.json` i `compute.py` encara corresponen a ICGC, activitat 0.1.1. Les dues lectures actives ja descriuen el nou recorregut CNIG. Les ordres, seleccions i hashes següents documenten l’execució històrica; no constitueixen una reconstrucció CNIG ni una aprovació dels textos actuals.

## Primera versió aprovada de les lectures

- [PDF d’alumnat, 8 pàgines](../../sandbox/practiques/pr1-project-setup/lectura-2026-10-v1-ca-alumnat-primera-01/outputs/LLEGIU-ME.pdf).
- [PDF docent, 9 pàgines](../../sandbox/practiques/pr1-project-setup/lectura-2026-10-v1-ca-docent-primera-01/outputs/LLEGIU-ME.pdf).

Versió `2026-10-v1`, aprovada per l’autor el 18/10/2026 i harmonitzada amb la micropràctica Moodle. Les dues fonts passen `prose_check`; els PDF A4 horitzontals s’han generat amb `manual_practice_pdf_build`, sense marca ESBORRANY. Fonts i hashes són a `context/practiques/lliuraments.md`. Els set fitxers importats d’Unaltramesa es conserven byte per byte.

## Entrades exactes de l’edició anterior

`prepare_inputs.py` prepara còpies create-only, sense descàrregues ni sobreescriptura:

| Input | Origen conservat | SHA-256 |
| --- | --- | --- |
| `municipis-icgc-20260120.fgb` | `tmp/reference-exercises/sources/divisions-administratives-v2r2-municipis-5000-20260120.fgb` | `069f755f253f7af969e80403f6e81fa2cadefbd4c40ffd2f825f30e167bf2b2d` |
| `municipi-cnig-font.gpkg` | `assets/projectes/vila-seca/dades_preparades/projecte_tig.gpkg` | `46aa316b88ec9f6eac559ca4f2037f1e142a997d3c0722febb8912a9a03654dd` |
| `ortofoto-vilaseca-2025.tif` | `tmp/unaltracaptura-qgis/cache/prepared/terrain/vila-seca/ortofoto_territorial_2025_vila_seca.tif` | `8cfdb39b6fce124844644087bc39a365da9bcef6401286644590b60c4fd07ad0` |

Les còpies es desen a `inputs/`, una carpeta ignorada i protegida com a dades per `.unaltraweb/source-checks.json`. La reserva i els hashes continuen identificant cada entrada exacta; el patró d’ignoració cobreix la carpeta. Una còpia existent diferent es refusa i es conserva per diagnòstic. No s’afegeix cap entrada al `data_root` global de captures.

```bash
python3 practiques/pr1-project-setup/prepare_inputs.py --dry-run
python3 practiques/pr1-project-setup/prepare_inputs.py
```

## Model i controls de l’edició anterior

`activity.json` utilitza el perfil `qgis-practice-request-v2`, versió d’activitat **0.1.1**, i el motor preparat `sha256:1003721d96abe9607d8337b36851f9b29f84c2f8f92b377d1a73ff03c9d15cd2`. `compute.py` només implementa l’activitat i la cartografia de PR1.

S’executen quatre exportacions `native:savefeatures`: catàleg ICGC inicial, catàleg al contenidor docent, selecció ICGC amb `CODIMUNI=431711` i vector CNIG de Vila-seca. Els atributs, identificadors i geometries dels 947 municipis es comparen amb la font. La selecció es contrasta també amb la cerca independent pel nom municipal. El callback `verify` reobre les dades persistides i retorna **35 controls**, sense repetir l’exportació per donar-la per bona.

El GeoPackage inicial només té `municipis_icgc`, `fonts_dades` i el projecte incrustat `inicial`. El docent afegeix `municipi_treball`, `municipi_cnig`, els projectes `pr1`/`comparacio` i la base editable de composició. El model conserva físicament el catàleg al GeoPackage docent, sense enllaçar-lo al contenidor inicial.

L’ortofoto local és una resposta WMS retinguda de context, no una descàrrega analítica a 25 cm. Els projectes distribuïts són locals; les connexions WMS continuen com a activitat separada. La base `Base municipal` conté mapes i text, amb marcs a 1:60.000 i 1:400.000. Els elements natius de llegenda i escala gràfica no formen part del subconjunt verificat pel productor 0.6.0 i es completen a QGIS durant el repàs.

La font DejaVu Sans es conserva amb el seu text de llicència en CSV/CSVT. La llicència se selecciona explícitament en cada edició: és un recurs documental, no una dependència de lectura interna del fitxer TTF.

## Execució compartida històrica

Amb la CLI instal·lada del productor i el consumidor explícit:

```bash
unaltracaptura-qgis practice-run --workspace "$PWD" \
  --request practiques/pr1-project-setup/activity.json \
  --output sandbox/practiques/pr1-project-setup/run-02
```

El nom de sortida és create-only. Per reconstruir cal triar un nom nou i revisar la nova identitat; no substituir el run conservat.

Run acceptat: `sandbox/practiques/pr1-project-setup/run-02/bundle.json`, SHA-256 **`e0d3b9d3a591b0566fdd6cef3afbc65cdc91856f8c89cf92017f3ac6d9e321dc`**. Job retingut: `sandbox/qgis-practice-jobs/practice-eeaa699be9bb44deb029cfc921c8cc98`.

El primer intent 0.1.0, job `practice-2597c02eafb6429aaa557e2329dc3f06`, conserva dades, controls i captures, però no es va publicar al destí `run-01`: la declaració TTF → llicència era excessiva respecte del graf tècnic. La versió 0.1.1 retira només aquella aresta; les llicències continuen seleccionades per destinatari.

## Selecció de l’edició anterior

L’autor va confirmar l’ús de les dues fonts exactes a l’edició local de revisió **`2026-10-review-r1`**, després dels PDF `paquet-01` d’alumnat i `paquet-02` de docent. Els camps `approved_sha256` de `edition-2026-10-review-r1.json` registren aquella selecció acotada; els snapshots i PDF històrics conserven draft/ESBORRANY. El descriptor es versiona com a antecedent, no com a configuració activa de la primera versió CNIG.

Aquella selecció es conserva amb els snapshots i artefactes de l’edició superada. Les fonts actives han canviat: el JSON r1 no s’ha de reutilitzar ni actualitzar amb hashes nous. La nova lectura es renderitza separadament per revisar el recorregut abans de fixar una altra edició.

| Destinatari | Arrels seleccionades | Closure GIS/recursos comprovada |
| --- | --- | ---: |
| Alumnat | `initial-project`, `initial-project-png`, `font-licence` | 7 fitxers |
| Docent | `initial-project`, `resolved-project`, `resolved-project-png`, `map-base-pdf`, `font-licence` | 10 fitxers |

El verificador és la imatge privada preparada 0.6.0, origen `prepared-image`, revisió instal·lada `sha256:4dcd2c40bca4836a202c0c5cc400553b0f134925023b7300e0c0ff2fff1d8492`. El schema v2 és `528c8be229c72c346f134ffaa60094f94224094a25b6fb11bcc87802ddc7fffb`. La configuració d’edició necessita estar indexada a Git; s’ha autoritzat indexar només aquell JSON, sense commit.

```bash
unaltraweb-mcp --project "$PWD" mcp manual-practice-compose \
  --config practiques/pr1-project-setup/edition-2026-10-review-r1.json --dry-run
unaltraweb-mcp --project "$PWD" mcp manual-practice-compose \
  --config practiques/pr1-project-setup/edition-2026-10-review-r1.json
```

Aquestes ordres corresponen a la CLI del controlador complet compartit. La CLI lleugera de l’host no substitueix el runtime de composició. No s’ha implementat cap empaquetador o renderitzador alternatiu al consumidor.

El resultat i la comprovació posterior dels ZIP extrets es registren a `context/practiques/lliuraments.md`. Es preserven els runs, els PDF previs i les edicions; cap neteja és implícita.
