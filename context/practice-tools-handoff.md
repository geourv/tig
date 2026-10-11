# TIG — retorn de les eines a l'autor

## Estat preservat

- Checkout: `/home/benizar/git/tig`.
- Branca: `integration/unaltraweb/25-v0.7.1-scaffold`.
- Base de la consolidació: `f5ddfabe650c95c10a99f3656a7cfc09e885dcbf`.
- Reserves: TIG #25 (controls/eines) i #26 (buffer). Es conserven els cinc controls
  Web 0.7.1 i totes les fonts, diagnòstics i productes retinguts.
- Prioritat actual: eines disponibles i retorn a l'autor. No s'ha de completar
  automàticament la docència ni recalcular el buffer per continuar les lectures.

## Estat actual de Web

1. **CLI candidata provada:** imatge
   `sha256:17ef0d24e8611a6802b3c01ff440e6e552eac728343733198056fdbc6cdf379e`.
   El dry-run de la lectura d'alumnat ha retornat `ok=true`, `state=planned`,
   `publishes=false`; fingerprint de lectura
   `d9d74815f742b4367dc2ef5641aaea5fc0198b96da5320dca5a152655923b7e2`.
   No ha creat el PDF. El contenidor exacte `fc3ec3c0177354de1db1b04eced81c531c97959dd2b2e4c2e03c9ae0105cbed1`
   s'ha retirat amb el reaper natiu (`resources_released=true`).
2. **Registre local recarregat:** `opencode.json`, només `$schema` i
   `mcp.unaltraweb`, amb `type: local`, argv, binding TIG, imatge immutable,
   `--managed --offline` i worker PDF explícit. Forma validada amb l'schema
   oficial `https://opencode.ai/config.json`.
   SHA-256: `7b947fb3ff7ae77e095cb0d118125b1dfe0a77f4912b8ff3b7cd0063816b55d1`.
   Només `/opencode.json` s'exclou localment a `.git/info/exclude`.
3. **MCP REAL recarregat i verificat:** una única crida `runtime_identity` a la
   connexió d'aquesta sessió ha retornat `ok=true`, `observation=live-serving-process`.
   Verificació registrada el **2026-10-09T22:02:34Z (UTC)**:
   - Consumidor, projecte efectiu, host i launcher: `/home/benizar/git/tig`;
     `project_id=5fb70984e2683ec7`.
   - Instància: `ad794e8d3a6b4083842de723c9205d85`.
   - Sessió: `2c1cb9fb9ab5af2c8fb502aa8f60dac1`.
   - Inici del procés: `2026-10-09T22:01:28.528099+00:00`.
   - Contenidor: `cb9563b8db7043cf4c42e9a3160c92dfbba1a47c7be8b97712aa3017b34c72fc`,
     `state=matched`, xarxa `none`.
   - Imatge seleccionada, esperada i observada:
     `sha256:17ef0d24e8611a6802b3c01ff440e6e552eac728343733198056fdbc6cdf379e`.
   - Fingerprint carregat i actual del controller:
     `sha256:5b8de154fc10665f71056b2887959d41a2a6f5fb5726611d1ee3482c7d7b3d36`;
     **`drift=false`**.
   - Worker PDF esperat i observat:
     `sha256:618163d3f924439792b2306617bd9612f566c5881166102fa544b4e782d569fa`,
     `state=matched`, amb la referència immutable `1bb3f2…` indicada més avall.
   - Connexió `connected`, `active_operation=null`, `queued_operations=0`.
   - Inventari de la sessió: **`manual_practice_pdf_build`** i
     **`manual_practice_compose`** presents; no s'han invocat.

El coordinador ha fet la recàrrega scoped amb el nou adapter host `2c9b0c21…`.
Aquest pin identifica el wheel host i és independent del fingerprint `5b8de154…`
observat al controller. La verificació anterior correspon al MCP real de la sessió.

## Seleccions i contractes

- Guia comuna: `/tmp/opencode/practice32-final-cohort.md`, SHA-256
  `6455db67fee9f13da172be810b6ea29d60b05ba2fba9d5f84038c1a47f95e7a2`.
- Web: `/tmp/opencode/practice32-web-candidate04/CONTRACT.md` i `ready.json`,
  SHA del marcador `ba9fbdb6170a0f51086bad310a636e8c3d2f93ea4317c106d313ab32f509718b`;
  els quatre fitxers inventariats s'han verificat.
- Adapter host Web: `/tmp/opencode/practice32-web-adapter-2c9b0c21cbdf7f226a76fd792b9a8fe31e51a525ad0e14398aa052b7a89e7a2a/venv/bin/unaltraweb-mcp-docker`.
  Pin del wheel: `2c9b0c21cbdf7f226a76fd792b9a8fe31e51a525ad0e14398aa052b7a89e7a2a`.
  Al mateix paquet públic, SHA de `ready.json`:
  `7c7f98fb11f0aaab827644c201a6b8527079ec8b26a96da3f346dbf861c2f9ec`;
  SHA de `manifest.json`: `0cc8e3735c960924e4698909367d01cf711d536eebda5fe068835d519b94f554`.
  Corregeix el fals refusal del reaper per l'ordre dels mounts. La identitat de
  l'adapter host és independent del fingerprint del controller. L'adapter anterior
  i el contracte original romanen immutables; els pins de controller/PDF es conserven.
  Ajust local comprovat: JSON vàlid, un únic executable substituït i resta de bytes
  de configuració idèntica. Les proves anteriors es conserven, sense nou dry-run.
- PDF: `ghcr.io/dosquartsdedocs/unaltraweb-manual-pdf@sha256:1bb3f2dafd741e96c28639ec1cc8ccaeb81cbaa73e649f787c0b4ef59997bd4b`,
  ID comprovat `sha256:618163d3f924439792b2306617bd9612f566c5881166102fa544b4e782d569fa`.
- QGIS: client únic `/tmp/opencode/practice32-qgis-client-1a7456c0b81e/env/bin/python`,
  package **0.6.0rc2**, revisió `sha256:5922d3dc411c14c7c3c2d9257a78b4d42f42fb1aae8451bcf245ca44a0e91992`.
  El seu `ready.json` té SHA `6a51f1f9c77a0a333623e8332b886651ea497895b1736165404e79d8905983bd`.
  No copiar, moure o reinstal·lar aquesta venv.

## Buffer ja produït

Base `B = sandbox/practiques/tig-buffer-municipal-500m/run-04-validated`.
**30 controls PASS**, mínim continu **495,0869662890991 m**, font preservada.
La prova causal i el control històric fallit de 497 m continuen a
`practiques/tig-buffer-municipal-500m/geos-validation.md` i als tres jobs fallits
conservats a `sandbox/qgis-practice-jobs/`.

| Fitxer relatiu a B | SHA-256 |
| --- | --- |
| `bundle.json` | `8bf979b7cc6c60312fb0a5421ab8a5f9b82bdd7d4cd128778e1ce73247dfcaff` |
| `payload/practice.json` | `1963edee0e1e96c266f85c2c9e5f96deca8b2198613991c70cfe358b68043fc8` |
| `payload/controls/calculation.json` | `b6c0129dd04f6c4145b6093ec433db00e776c6be55377dbc394fe64c1193c6a5` |
| `payload/controls/offline-reopen.json` | `6414440885bbedf15ee1f3eb745f30a1f6faec1f473387c17882db7d4069fd80` |
| `payload/projects/initial/initial.qgz` | `af2eb7b07c4da8d292f3078d69e44527b685f3a59fe6a39f3a292c22cd99ec9c` |
| `payload/projects/resolved/resolved.qgz` | `1d90d281a9590cf7db453b3742a5da68050dd93d57fc49dab89216143941087d` |
| `payload/captures/initial-project/overview.png` | `7a2ab436984fe8a9668a38a083814f3d7c1246a1f0af6f08670af3c838b1cd61` |
| `payload/captures/resolved-project/overview.png` | `d7b908dc9bf6451bdd255b1a22275e227c2c748e5b2ee1692e3d89bda3162ebe` |

Cada captura té també `overview.original.png`, `overview.annotations.svg` i
`overview.manifest.json` al mateix directori; els hashes complets són al bundle.
El productor ja ha fet **reobertura offline després de relocalització** dels
projectes externs i incrustats; `ok=true`, `container_absence_verified=true`.
Un `practice-check` nou, readonly, ha verificat els dos projectes i la closure de
cinc fitxers: dos GPKG, dos QGZ i la font DejaVu Sans.

## Invocacions copiables

Comprovació QGIS readonly, des del checkout autoritatiu:

```bash
P=/home/benizar/git/tig
env -u DOCKER_CONTEXT -u DOCKER_TLS_VERIFY -u DOCKER_CERT_PATH -u DOCKER_API_VERSION \
  -u UNALTRACAPTURA_QGIS_PROJECT_ID -u UNALTRACAPTURA_QGIS_JOB_REGISTRY \
  -u UNALTRACAPTURA_QGIS_JOB_REGISTRY_HOST -u UNALTRACAPTURA_QGIS_JOB_GRANT \
  DOCKER_HOST=unix:///var/run/docker.sock MCP_CONSUMER_WORKSPACE="$P" \
  UNALTRACAPTURA_QGIS_WORKSPACE="$P" UNALTRACAPTURA_QGIS_HOST_WORKSPACE="$P" \
  UNALTRACAPTURA_QGIS_HOST_UID="$(id -u)" UNALTRACAPTURA_QGIS_HOST_GID="$(id -g)" \
  /tmp/opencode/practice32-qgis-client-1a7456c0b81e/env/bin/python \
  -I -B -m veure_qgis_mcp.cli practice-check --workspace "$P" \
  --path sandbox/practiques/tig-buffer-municipal-500m/run-04-validated/bundle.json \
  --sha256 8bf979b7cc6c60312fb0a5421ab8a5f9b82bdd7d4cd128778e1ce73247dfcaff \
  --select initial-project --select resolved-project
```

Ordre del dry-run Web anterior, amb `CLIENT` actualitzat; no s'ha tornat a executar:

```bash
PROJECT=/home/benizar/git/tig
CLIENT=/tmp/opencode/practice32-web-adapter-2c9b0c21cbdf7f226a76fd792b9a8fe31e51a525ad0e14398aa052b7a89e7a2a/venv
IMAGE=sha256:17ef0d24e8611a6802b3c01ff440e6e552eac728343733198056fdbc6cdf379e
PDF_IMAGE=ghcr.io/dosquartsdedocs/unaltraweb-manual-pdf@sha256:1bb3f2dafd741e96c28639ec1cc8ccaeb81cbaa73e649f787c0b4ef59997bd4b
PROFILE="$("$CLIENT/bin/unaltraweb-mcp-docker" path)"
PROJECT_ID="$(/bin/sh "$PROFILE/scripts/unaltraweb-mcp-project-id.sh" "$PROJECT")"
SESSION="$(od -An -N16 -tx1 /dev/urandom | tr -d ' \n')"
PM="$(/bin/sh "$PROFILE/scripts/unaltraweb-docker-mount.sh" "$PROJECT" "$PROJECT")"
SOCKET="$(realpath /var/run/docker.sock)"
SM="$(/bin/sh "$PROFILE/scripts/unaltraweb-docker-mount.sh" "$SOCKET" /var/run/docker.sock)"
CID="$(docker --context default create --pull never --network none --init \
  --name "unaltraweb-stdio-$SESSION" --cpus 2 --memory 4g --pids-limit 512 \
  --label io.context.mcp-factory=unaltraweb --label io.context.mcp-role=stdio \
  --label "io.context.mcp-project=$PROJECT_ID" --label "io.context.mcp-session=$SESSION" \
  --user "$(id -u):$(id -g)" --group-add "$(stat -c %g "$SOCKET")" \
  --mount "$PM" --mount "$SM" -e HOME=/tmp -e "MCP_CONSUMER_WORKSPACE=$PROJECT" \
  -e "UNALTRAWEB_DOCKER_ROOT=$PROJECT" -e "UNALTRAWEB_RUNTIME_SESSION=$SESSION" \
  -e "MANUAL_PDF_IMAGE=$PDF_IMAGE" --entrypoint unaltraweb-mcp "$IMAGE" \
  --project "$PROJECT" mcp manual-practice-pdf-build \
  --source practiques/tig-buffer-municipal-500m/ca/alumnat/LLEGIU-ME.md \
  --version 0.1.1 --dry-run)" || exit 1
STATUS=0
docker --context default start --attach "$CID" || STATUS=$?
docker --context default wait "$CID"
DOCKER_CONTEXT=default "$CLIENT/bin/unaltraweb-mcp-docker" reap-session \
  --project "$PROJECT" --session-id "$SESSION" --container-id "$CID" && test "$STATUS" -eq 0
```

Amb la connexió real ja recarregada, `manual_practice_pdf_build` és disponible
amb aquests arguments MCP (referència, sense nova execució):

```json
{"source":"practiques/tig-buffer-municipal-500m/ca/alumnat/LLEGIU-ME.md","version":"0.1.1","dry_run":true}
```

## Contingut que reprendrà l'autor

La consolidació autoritzada guarda a Git les fonts, el codi de reproduïbilitat i
els manifests, amb les lectures en draft. `inputs/municipi-font.gpkg` queda al seu
lloc, exclòs pel path exacte; el README de la pràctica documenta la preparació
create-only i el hash que ja declara `activity.json`. L'índex
`context/practice-retention.json` referencia els artefactes i hashes retinguts.
La còpia durable de dades fora de Git i la instal·lació persistent de les eines
resten a càrrec del hub/owners. Els paths temporals del registre local continuen
operatius; el lliurament posterior a Moodle serà PDF i ZIP per activitat.

Les lectures `practiques/tig-buffer-municipal-500m/ca/alumnat/LLEGIU-ME.md` i
`.../docent/LLEGIU-ME.md` continuen en **draft**. Cal revisar-ne el contingut,
incorporar-hi les captures/links reals amb els bindings del contracte i preparar
una edició real indexada quan l'autor ho decideixi. No existeixen encara els
dos PDFs de pràctica, els dos ZIPs Moodle ni una config d'edició; el dry-run només
n'ha planificat una lectura. La verificació de bytes finals extrets dels ZIPs i
la seva reobertura específica també estan pendents.

La closure inicial no inclou resultats docents; els casos d'arcs són diagnòstics
privats, no dependències dels checkpoints. No usar els jobs privats per suplir
fitxers que faltin als ZIPs. Conservar dist, snapshots i intents fallits; una
exclusió Git/Jekyll no és permís de neteja. Publicació web i Moodle són separades.

La recàrrega scoped i la verificació del MCP real s'han completat. La sessió es
retorna **idle per a l'autor, amb la connexió oberta, sense drain**. Es mantenen
els límits i el contingut pendent descrits més amunt.
