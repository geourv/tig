# Preparació del buffer municipal TIG

Font de domini/docència de `tig-buffer-municipal-500m`, reservada a geourv/tig#26
sota la coordinació gaContExt #32. Estat: **run-04 acceptat pel productor,
amb 30 controls i reobertura offline correctes; lectures en draft**.
El bundle retingut és `sandbox/practiques/tig-buffer-municipal-500m/run-04-validated/bundle.json`,
SHA-256 `8bf979b7cc6c60312fb0a5421ab8a5f9b82bdd7d4cd128778e1ce73247dfcaff`.
La versió de font `0.1.1` de
`activity.json` corregeix el pressupost d'arcs després del contraexemple real;
no identifica una edició de PDF/ZIP ni una aprovació docent. Els tres intents anteriors
amb el pressupost de 3 m es conserven com a evidència fallida. La derivació,
l'atribució causal i els casos mínims són a `geos-validation.md`.

## Interfície utilitzada

La font és un únic `compute.py`, amb `compute(context)`, `verify(context)` i
`compose(project, project_id, parameters, products)`, segons l'exemple públic
lliurat amb unaltracaptura-qgis 0.6.0rc2. La request és `activity.json`, perfil
`qgis-practice-request-v2`. El proveïdor executa, inspecciona, desa els checkpoints,
calcula la closure, captura i segella; Web compon les lectures i els lliuraments.

Selecció pública comprovada:

- Lliurament: `/tmp/opencode/practice32-qgis-0.6.0rc2-round32-n1/`.
- `ready.json`: `49a8887587eb5942aae7aa76b678acd617cec799294c350fe5fc6d344d881a1a`.
- Wheel: `1a7456c0b81e0a4729b702b60d9340456efea9a88b9f5c21b97c8ff4823d09bf`.
- Revisió: `sha256:5922d3dc411c14c7c3c2d9257a78b4d42f42fb1aae8451bcf245ca44a0e91992`.
- Motor: `sha256:1003721d96abe9607d8337b36851f9b29f84c2f8f92b377d1a73ff03c9d15cd2`.
- Schema v2: `528c8be229c72c346f134ffaa60094f94224094a25b6fb11bcc87802ddc7fffb`.

No hi ha launcher, instal·lador, empaquetador ni executable de render local en
aquesta pràctica. La selecció final i la invocació comuna són les de
`/tmp/opencode/practice32-final-cohort.md`, SHA-256
`6455db67fee9f13da172be810b6ea29d60b05ba2fba9d5f84038c1a47f95e7a2`.

La CLI comuna posterior ja lliurada és
`/tmp/opencode/practice32-qgis-client-1a7456c0b81e/env/bin/python`, amb prefix
`-I -B -m veure_qgis_mcp.cli`; marcador `ready.json` amb SHA-256
`6a51f1f9c77a0a333623e8332b886651ea497895b1736165404e79d8905983bd`.
S'ha de seguir el seu `USAGE.md`: els tres bindings de workspace han d'identificar
TIG, el daemon és `unix:///var/run/docker.sock` i cal aplicar els unsets declarats
de context/TLS/API i grants W1. Aquesta font no instal·la ni copia la venv compartida.

## Entrada i recursos

`inputs/municipi-font.gpkg` és una còpia binària de
`assets/projectes/vila-seca/dades_preparades/projecte_tig.gpkg`: **139.264 bytes**,
SHA-256 `46aa316b88ec9f6eac559ca4f2037f1e142a997d3c0722febb8912a9a03654dd`.
La còpia no és un derivat GIS i conserva també els membres històrics de la font.
El càlcul només exporta `municipi_treball`; no copia el projecte històric amb WMS
als productes docents.

La còpia local és necessària per mantenir una request relativa i transportable:
rc2 resol `script` i `inputs[].path` respecte del directori de la request i rebutja
els segments `..`. No s'utilitzen rutes absolutes de l'ordinador ni symlinks.

El GPKG d'entrada és un recurs **local, exclòs de Git pel seu path exacte**.
`activity.json` versiona el path relatiu i el hash que exigeix el model; aquest
README conserva la procedència i la preparació. Des de l'arrel del checkout,
amb la font històrica disponible o restaurada amb el mateix hash, es pot preparar
la còpia sense executar QGIS ni descarregar dades:

```bash
python3 -B - <<'PY'
import hashlib
import json
from pathlib import Path

activity = Path("practiques/tig-buffer-municipal-500m")
request = json.loads((activity / "activity.json").read_text())
item = next(item for item in request["inputs"] if item["id"] == "municipi-source")
source = Path("assets/projectes/vila-seca/dades_preparades/projecte_tig.gpkg")
target = activity / item["path"]
data = source.read_bytes()
if len(data) != 139264 or hashlib.sha256(data).hexdigest() != item["sha256"]:
    raise SystemExit("La font no correspon als bytes declarats; cal restaurar-la.")
if target.is_symlink():
    raise SystemExit("La destinació no pot ser un symlink.")
if target.exists():
    if target.read_bytes() != data:
        raise SystemExit("La destinació existent difereix; es conserva sense sobreescriure.")
else:
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("xb") as output:
        output.write(data)
print("Entrada local verificada:", target, item["sha256"])
PY
```

La còpia també és dins del bundle segellat, a
`payload/sources/inputs/inputs/municipi-font.gpkg`, amb el mateix hash.
La retenció durable fora de Git es tancarà amb el hub; mentrestant es conserven
la font, la còpia local i el bundle. Les dades històriques ja versionades a
`assets/` no es modifiquen en aquesta consolidació de fonts.

Identitat esperada: una entitat `MULTIPOLYGON`, EPSG:25831, `nom_muni=Vila-seca`,
`codi_muni=43171`, `codi_oficial=34094343171`, `id_origen=1172246`.
La procedència original es manté a
`assets/projectes/vila-seca/procedencia.yml`: IGN/CNIG, API OGC Features,
[objecte 1172246](https://api-features.ign.es/collections/administrativeunit/items/1172246?f=json),
consulta del 8 de setembre de 2026, CC BY 4.0 ign.es. El GeoJSON canònic i el QGZ
original amb WMS es conserven a la seva ubicació.

La presentació usa **DejaVu Sans**. `font-regular` declara la còpia del TTF real
que conté el motor pinat, també inclòs al fixture rebut: SHA-256
`ae7b7855e115a5966d8b1b3f80f254ccc117ec86f9965e202ee2940453837280`.
`compute` exigeix aquest hash abans de copiar-lo al producte declarat; `fonts`
vincula el fitxer a la família. Es conserven les metadades de drets del TTF;
[llicència DejaVu/Bitstream Vera](https://dejavu-fonts.github.io/License.html).
Cap símbol SVG extern, raster, WMS, WFS, tema o layout addicional intervé en el cas.

## Càlcul i controls previstos

`native:savefeatures` materialitza una entrada inicial neta. `native:buffer`
produeix una sortida persistent de 500 m, vuit segments per quadrant, extrems i
unions arrodonits, límit de mitra 2, sense dissolució ni separació de parts.
`verify` reobre les capes persistides i no crida Processament.

Controls numèrics previstos:

- Una entitat a font, inicial i buffer; CRS EPSG:25831, identitat municipal i
  geometries vàlides/no buides. La geometria inicial ha de ser igual a la font.
- Àrea municipal perduda respecte del buffer: 0 m², tolerància 0,01 m².
- Augment d'àrea estrictament positiu i no superior a `r·P + n·π·r²`, amb el
  perímetre planar de totes les vores de la font i `n` parts poligonals. És un
  límit superior, no la fórmula d'igualtat d'un polígon convex aplicada a la costa.
- Mostreig de **tots** els contorns del resultat: vèrtexs, punts mitjans i
  subdivisions amb separació màxima de 25 m. Màxim 20.000 mostres i 10.000 segments.
- Distància de cada mostra al segment més proper de qualsevol anell original,
  calculada per projecció euclidiana elemental. No s'utilitza ni un segon buffer
  ni la distància GEOS com a substitut d'aquesta comprovació.
- Sageta d'arcs parcials: `500·(1−cos(3π/64)) = 5,411745017609492 m`, derivada
  de l'arrodoniment de GEOS 3.13.1, més 0,01 m numèric. Es comprova el mínim
  continu entre tots els segments i una cota superior contínua per intervals
  convexos, contra els segments originals. Banda exigida:
  `[494,5782549823905; 500,01]` m. El màxim mostrejat ha d'arribar a 500 ± 0,01 m.
  La simplificació no rep una tolerància addicional ni es pressuposa inofensiva;
  qualsevol desviació fora de banda refusa el resultat.
- Bytes d'entrada i font tipogràfica contrastats amb els hashes declarats.

El schema de checks representa comparacions simètriques `actual/expected/tolerance`.
Les identitats i desigualtats estrictes es retornen com 0/1; el límit d'augment
d'àrea es representa amb centre `U/2` i tolerància `U/2`, més el check positiu separat.
Els valors mesurats del segon intent es conserven al diagnòstic del productor:

- Àrea municipal: 21.704.046,024839967 m².
- Àrea del buffer: 40.285.984,76858085 m²; augment 18.581.938,74374088 m².
- Pèrdua de cobertura: 0 m².
- 663 segments originals, 588 segments del buffer i 2.692 mostres.
- Distància mínima: **495,0948411931408 m**, inferior al límit fix de 497 m.
- Distància màxima: 500,00000000133866 m, dins de la tolerància fixada.
- 21 dels 22 controls dins dels límits; falla només `contour-min-distance`.

La mostra mínima és `(343086.40574131894, 4555453.787553297)` en EPSG:25831.
El segment del buffer que la conté mesura 121,1884256197147 m i les distàncies dels
seus extrems a la font són 500,00000000002854 i 497,7343569566893 m. Això no és el
cas ideal de dues puntes a radi 500 m separades exactament per un angle de π/16.
La sageta nominal del polígon regular no ha resultat una cota global suficient
per a aquest contorn calculat. L'intent causal posterior identifica la part d'un
fillet original de 16,0773° subdividit en un segment, i les proves convexes
independents refuten la hipòtesi regular inicial. La revisió autoritzada de la
validació és analítica i queda documentada a `geos-validation.md`; es conserva
el control històric fallit de 497 m com a diagnòstic, sense convertir-lo en PASS.

Evidència retinguda del segon intent:
`sandbox/qgis-practice-jobs/practice-e8e57180d04e41d9931f33f4c580483d/compute-35d0a887f622/`
(`stdout.log`, `stderr.log`, `execution.json`) i productes parcials a `work/data/`
del mateix job. El primer intent es conserva a
`sandbox/qgis-practice-jobs/practice-f7b14a7bbd3a442b83e85ca28568927c/`.
Els dos witnesses confirmen motor pinat, xarxa desactivada i absència final del
contenidor exacte. El run-04 de la versió `0.1.1` ja ha completat l'acceptació del
productor i la reobertura offline. Els productes parcials dels intents fallits
no substitueixen el bundle acceptat ni els lliuraments encara pendents.

`test_controls.py` comprova només l'aritmètica amb coordenades analítiques,
inclosos radi incorrecte i arcs més grossos. No importa QGIS ni executa l'activitat.

La validació JSON Schema de la request no substitueix l'execució: `scene` admet
propietats obertes al schema públic i la comprovació semàntica de capes, widgets,
fonts i dependències es va completar amb el productor al run-04. En la connexió
publicada Web 0.7.1 anterior,
`prose_check` rebutja aquests paths privats amb `editorial_input` i comprova zero
fitxers; no és un PASS de prosa. Les lectures tenen revisió manual i validació de
front matter. La passada editorial automatitzada privada s'ha executat amb la CLI
del candidat final Web `sha256:17ef0d24e8611a6802b3c01ff440e6e552eac728343733198056fdbc6cdf379e`:
les dues lectures retornen `ok: true`, un fitxer comprovat cadascuna i cap finding.
Això no valida els resultats científics ni concedeix aprovació d'autor; continuen
en `draft`. No s'han traslladat a una col·lecció pública per eludir l'antic límit.

## Productes i captura

`initial-data` conté només la capa municipal i el projecte incrustat `inicial`.
`buffer-data` conté el buffer i el projecte `resolt`, que depèn també d'`initial-data`.
Els membres i els rols dels dos GeoPackage són explícits. L'inicial no conté
cap resultat resolt; la closure del resolt inclou les dues bases locals i la font.
Els productes `arc-probe-input` i `arc-probe-buffer` contenen els tres casos
convexos de control i no són dependències dels projectes destinats a l'alumnat
o al docent.

Els checkpoints externs són `initial-project` i `resolved-project`. Cada un té
una captura real `overview` declarada a `projects[].scene`: selecció de capa,
enquadrament, controls visibles i etiquetes vinculades a les capes natives.
Es reprenen els conceptes de `recipes/qgis-vector-workflows.yml#buffer-dialog`,
però no la digitalització/ortofoto dels passos previs ni els seus outputs públics.
El productor ja ha generat les dues captures reals dins del bundle del run-04.
Les lectures no incorporen una captura antiga ni un enllaç fictici a una imatge:
el compositor hi vincularà els fitxers reals seleccionats del descriptor segellat.

La request de productes és autònoma respecte del catàleg general:
`unaltracaptura-qgis.yml` continua sent la configuració principal i declara l'entrada
docent. El motor d'aquesta activitat el fixa `activity.json`, sense reconfigurar
les captures històriques del manual.

## Lectures, metadades i conservació

Fonts en català/draft: `ca/alumnat/LLEGIU-ME.md` i `ca/docent/LLEGIU-ME.md`.
Assignatura: Tecnologies de la Informació Geogràfica, **21234114**, URV,
Facultat de Turisme i Geografia, Benito Zaragozí. La plantilla final no presenta
el curs acadèmic al header; la composició encara depèn de la selecció final Web.

- `practiques/tig-buffer-municipal-500m/`: fonts versionades; l'entrada binària
  verificada es conserva localment fora de Git, amb exclusió exacta. Conservació
  `never` per a neteges automàtiques.
- `sandbox/practiques/tig-buffer-municipal-500m/`: execucions, snapshots, controls
  i proves ignorats; conservació `explicit`, inclosos runs fallits amb evidència.
- `sandbox/qgis-practice-jobs/`: staging propietat del productor rc2; mateixa
  conservació explícita. El consumidor no en fa neteges genèriques.
- `dist/practiques/tig-buffer-municipal-500m/`: edicions finals ignorades,
  conservació `explicit`; manifests/receipts externs als ZIPs. Una edició segellada
  no se sobreescriu ni s'elimina perquè sigui ignorada.

El run acceptat i els paths/hashes retinguts consten a
`context/practice-retention.json`; l'estat de les eines és a
`context/practice-tools-handoff.md`. No hi ha cap configuració d'edició amb hashes
provisionals ni els dos PDFs/ZIPs finals. A Git es conserven les fonts i el codi de
reproduïbilitat; dades, PDF i ZIP es retenen fora de Git per al lliurament posterior
a Moodle. Publicació del manual i pujada Moodle són operacions separades.
Els recursos actuals d'`assets/` i els cinc controls Web 0.7.1 es preserven.
