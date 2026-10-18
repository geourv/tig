# Recorregut municipal: casos docents de revisió

Fonts d’autoria i requests del conjunt PR1–PR6, Reus i bonus. Reserva exacta acceptada a [TIG #28](https://github.com/geourv/tig/issues/28#issuecomment-6175858065). L’[índex de revisió](../README.md) reuneix les lectures i els paquets.

L’alumnat descarrega i prepara les seves dades amb les instruccions del recorregut ampliat. Aquests casos serveixen al professorat i es poden compartir com a exemples identificats. L’autor ha aprovat la primera versió de les activitats el 18/10/2026; els límits científics i tècnics dels casos es mantenen explícits. PR1 diferencia aquesta via de la micropràctica Moodle confirmada.

## Entrades i responsabilitats

- `prepare_inputs.py` verifica i reté còpies create-only dels originals, adquireix explícitament el context PNOA i materialitza els requests a partir de l’especificació del cas.
- `compute.py` conté el càlcul, les comprovacions independents de dades persistides i les decisions cartogràfiques. Les fases tenen requests separats; la font comuna evita divergències en l’herència i en els paràmetres.
- `pr6_roi_municipal.model3`, `bonus_roi.py`, `bonus_portals.sql` i `bonus_postgis.sql` són fonts d’exemple identificades. El model extern, PyQGIS i SQLite s’han executat al cas; PostGIS és una font opcional sense execució acreditada aquí.
- El productor compartit `unaltracaptura-qgis` executa, captura, exporta els mapes, comprova les dependències, reobre els projectes sense xarxa i segella els bundles. No hi ha empaquetador ni verificador GIS alternatius al consumidor.
- `unaltraweb` construeix els PDF de lectura. Les setze fonts aprovades i els PDF `2026-10-v1` estan identificats a l’inventari; la composició d’un ZIP de distribució necessita la seva selecció explícita de productes.

Les lectures Markdown, els scripts Python/SQL, el model `.model3` i els requests JSON són fonts versionables. `inputs/` s’ignora com a carpeta completa, igual que els jobs sota `sandbox/` i els productes sota `dist/practiques/`. La reserva exacta de cada entrada i els seus hashes continuen als plans i manifests; no cal una regla de `.gitignore` per fitxer. Els originals, les dades preparades, els PDF i els paquets es retenen: ignorar-los no n’autoritza la neteja.

## Preparar els originals

Des de l’arrel de TIG:

```bash
python3 -B practiques/recorregut-municipal/prepare_inputs.py originals --dry-run
python3 -B practiques/recorregut-municipal/prepare_inputs.py originals
python3 -B practiques/recorregut-municipal/prepare_inputs.py pnoa --dry-run
python3 -B practiques/recorregut-municipal/prepare_inputs.py pnoa
```

Les nou fonts locals es contrasten amb hashes fixats: tres ZIP CNIG, dos GeoPackage extrets, tres MDT i l’original sintètic PR2. Un input existent diferent es refusa. Els ZIP i els originals històrics no se sobreescriuen.

L’adquisició PNOA conserva PNG, GetCapabilities i procedència amb peticions, respostes de metadades, mides, hashes i data d’accés. La consulta del 14/10/2026 reté una imatge de 2.048 × 2.048 píxels sobre 13.500 × 13.500 m, EPSG:25831: **6,591796875 m per píxel**. Les tres consultes puntuals del mosaic indiquen juliol de 2024 i 0,25 m de la font. Aquesta resolució original no s’atribueix a l’extracte reescalat, que és context i no suport de digitalització fina.

La font PR2 històrica conserva també altres capes i un projecte antic. El càlcul només en reutilitza `fanals`, `carrils_bici` i `plaques_solars`, amb geometries, atributs i `no_apte_per_analisi` intactes. La base municipal dels projectes nous és CNIG. Cal aportar observacions revisades per disposar d’un inventari territorial real.

## Executar els casos

El motor preparat és QGIS 3.44.11, imatge `sha256:1003721d96abe9607d8337b36851f9b29f84c2f8f92b377d1a73ff03c9d15cd2`. El productor és 0.6.0, perfil `qgis-practice-v2`, revisió `sha256:4dcd2c40bca4836a202c0c5cc400553b0f134925023b7300e0c0ff2fff1d8492`.

```bash
python3 -B practiques/recorregut-municipal/prepare_inputs.py request --stage pr1 --write-request
unaltracaptura-qgis practice-run --workspace "$PWD" \
  --request practiques/recorregut-municipal/pr1.json \
  --output sandbox/practiques/pr1-project-setup/run-nou
```

El destí ha de ser nou. La seqüència és PR1 → PR2 → PR3 → PR4 → PR5 → PR6 → bonus; Reus és un cas independent del bloc PR4. Cada fase posterior pren una còpia verificada de la fita precedent. La còpia es prepara amb `retain --source … --name … --sha256 …`, utilitzant el hash retornat pel productor o la seva selecció pública. Els requests no es materialitzen amb entrades inexistents ni hashes ficticis.

Els requests `.json` es materialitzen amb el generador; si ja existeixen i difereixen, la preparació s’atura perquè es revisi la font. El model es pot serialitzar amb `prepare_inputs.py model` en un Python amb les biblioteques públiques de QGIS. La serialització observada utilitza QGIS 3.34.4; **l’execució i la verificació del model són les del motor fixat 3.44.11**. La generació del XML no es compta com a execució científica.

## Candidats conservats

Els destins de la taula són relatius a `sandbox/practiques/`.

| Cas | Request | Bundle de revisió | Controls |
| --- | --- | --- | ---: |
| PR1 | `pr1.json` | `pr1-project-setup/run-cnig-01/bundle.json` | 20 |
| PR2 sintètica | `pr2.json` | `pr2-digitalitzacio/run-cnig-01/bundle.json` | 27 |
| PR3 | `pr3.json` | `pr3-consultes/run-cnig-02/bundle.json` | 46 |
| PR4 | `pr4.json` | `pr4-geoprocessament/run-cnig-03/bundle.json` | 71 |
| Reus | `reus.json` | `pr4-tessellacions-reus/run-cnig-04/bundle.json` | 31 |
| PR5 | `pr5.json` | `pr5-raster/run-cnig-02/bundle.json` | 125 |
| PR6 | `pr6.json` | `pr6-sintesi/run-cnig-01/bundle.json` | 127 |
| Bonus | `bonus.json` | `bonus-pyqgis-sql/run-cnig-02/bundle.json` | 144 |

Són 591 controls d’entrades, conservació, identitats, geometries, càlcul i graelles. El recompte no substitueix la revisió científica ni l’aprovació de l’autor. Cada bundle reté les observacions natives de les capes, els projectes, les composicions i la reobertura.

| Cas | SHA-256 del bundle retornat pel productor |
| --- | --- |
| PR1 | `2fdbd4d06815f3e5934ee8ff02f9c507cbd0548def53ca4b2487dd683921860b` |
| PR2 | `137448f1ba2a3bbb4c1c3d2673f1671d380c3834cebfb0006ef03027bec9eb94` |
| PR3 | `c6a9e862187fa11ef9ea44ba63f7e05ea6d38176116054f1dc21564a6c7c95d1` |
| PR4 | `132c8fef06138443bee23cfa0a5458a4dca11f1ae19e4a04d65a8a5058266d10` |
| Reus | `a73d572ec4904e4bc3ade8e226f7bef24cc57ed3c4f5cbaeb501caa551168c09` |
| PR5 | `4892b850db89ea02efb56f99ce053c98a81541b227cb1b68590a9ca96e3b22da` |
| PR6 | `a5248469426f73b1dc2b954203f21c4ea0bf176a1c3d8064e393cbabb28d8250` |
| Bonus | `4cac11de2ea29779a687efff1822053131dfbfdafb00b9703033257cc3659561` |

## Obrir i revisar

Cal conservar **tota la carpeta del bundle**. El projecte resolt és a `payload/projects/`, les dades i dependències a `payload/data/`, el mapa a `payload/figures/mapa-revisio.pdf` i la captura a `payload/captures/resolved-project/overview.png`. Les tipografies i llicències acompanyen el projecte; en un altre equip cal comprovar que QGIS disposi de DejaVu Sans.

Els originals i les fonts exactes executades són a `payload/sources/`. El manifest associa IDs a paths i hashes; el descriptor és `payload/practice.json`. Per reproduir exactament un candidat, s’utilitza el seu `payload/sources/rebuild.json` en un destí nou, amb el productor i el motor declarats. Això evita confondre el snapshot executat amb revisions posteriors de `compute.py`.

Els primers candidats numèrics de PR3 i PR4 es mantenen com a inputs de la cadena. Les revisions cartogràfiques posteriors corregeixen la mida dels punts, l’ordre de dibuix o les claus de color; conserven les mateixes capes analítiques. Els hashes d’herència reals consten en cada request i bundle, sense reescriure les còpies anteriors.

`practice-check --path … --sha256 … --select …` retorna la selecció i totes les seves dependències. S’ha comprovat expressament la selecció de `roi-model` i `limits-original` juntament amb el projecte PR6: el model extern i el ZIP original són inputs retinguts i seleccionables, sense falsejar-ne el format com a productes GIS.

## Resultats i límits de la revisió

- **PR3:** 3.584 portals, 285 illes contingudes, 318 intersectants, 265 registres d’autovies/autopistes amb 185 IDs de tram; el segon grup cartogràfic té 388 carreteres convencionals i 150 multicarrils. Es conserva tota la digitalització PR2.
- **PR4:** variants de buffers, peces exclusives amb multiplicitat 1/2/3, conservació ponderada d’àrea, retall/intersecció/diferència i quatre envolupants. El cercle és una aproximació poligonal de 720 segments; el control del radi teòric es diferencia de la discretització.
- **Reus:** 47.862 portals d’entorn, 23.968 generadors principals, 37.156 d’entorn ampli, 47.918 triangles, 13.198 cel·les retallades i 14 categories. La validació espacial reserva 4.092 ubicacions; 3.435 coincideixen amb el codi observat, 83,94%. No és validació de límits postals oficials.
- **PR5:** graelles comunes 25/200 m, deu GeoTIFF, cinc ràsters de demostració, zones de cota baixa i estadístiques. Les mitjanes aritmètiques d’angles i codis es retenen com a diagnòstic de l’eina, no com a direccions mitjanes o elevacions; les lectures n’expliquen la interpretació.
- **PR6:** model extern real de dos nodes, manual/lot/model equivalents i transferència a Reus. Els deu ràsters PR5 es conserven byte per byte; el pendent es reexecuta des dels MDT originals. La representació del model dins del projecte no queda acreditada per aquesta execució externa.
- **Bonus:** s’executen PyQGIS i SQLite i es comproven la ROI i els 3.584 portals resumits. El fitxer PostGIS és una font explicada, sense prova de servidor en aquest paquet.
- Les composicions natives són bases editables amb mapes i text. El perfil encara no admet llegenda nativa ni escala gràfica; no es presenten com a mapes finals complets. PR5 té dos marcs comparables i Reus una clau textual de colors.
- La captura territorial real de PR2, una descàrrega cadastral nova i la capa específica d’inundabilitat de la Pineda no s’han inventat ni substituït per les dades sintètiques o els llindars del MDT.

## Incidències conservades

Els intents refusats i els candidats previs continuen retinguts. PR4 va revelar que la diferència simètrica exacta de línies és inadequada davant d’arrodoniments d’intersecció: es va substituir per conservació de longitud per ID i suport mètric d’1 mm, no per una tolerància de centenars de metres. PR5 va requerir propagar l’error float32 del gradient a l’angle d’orientació en terreny no pla. Reus va requerir fer idempotent l’autoria d’un renderitzador categòric; el bonus, adaptar tuples SQLite a la llista d’atributs PyQGIS.

L’inventari general de retenció, l’aprovació de la primera versió i els PDF vigents són a `context/practiques/lliuraments.md`. La publicació del manual a Pages i la distribució dels materials de pràctiques per Moodle tenen circuits diferents.
