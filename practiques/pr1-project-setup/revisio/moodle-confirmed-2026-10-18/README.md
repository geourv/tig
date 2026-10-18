---
lang: ca
content_status: draft
---

# Revisió de la micropràctica Moodle PR1

Aquesta edició conserva la definició confirmada pel docent el **18 d’octubre de 2026**. La data identifica aquella confirmació. Els set fitxers importats es mantenen byte per byte; les empremtes i l’origen són a `import-manifest.json`.

| Selecció | Valor |
| --- | --- |
| Activitat | `tig/pr1-moodle` |
| Edició | `moodle-confirmed-2026-10-18` |
| Part assignada | `micropractice` |
| Recepta | `tig-pr1-moodle-confirmed-2026-10-18` |
| Empremta efectiva validada | `7c899db02195a75c76cb5217cfcab13fc5c017b4ae98ab99ddcc4b23dba09d1e` |

La rúbrica té tres blocs: `BASIC` fins a **70**, `EXTENSIONS` fins a **20** i `DOCUMENTATION` fins a **10**. Les comprovacions i preguntes aporten evidència al bloc corresponent; no introdueixen subpesos ni quotes per tipus d’ampliació.

Les composicions són ampliacions opcionals. Aquesta micropràctica no exigeix descàrrega CNIG, municipi docent, EPSG fix ni PDF de mapa separat. Un únic PDF d’apunts satisfà el tipus documental obligatori. La pauta exacta de noms de classe queda pendent de context docent. El recorregut CNIG ampliat del manual i la recepta de referència `tig/pr1` són definicions diferents.

## Fonts i responsabilitats

- [Enunciat confirmat](statement.md) i [procedència](provenance.json).
- [Manifest d’activitat](activitat.yml), [recepta](recipe.yml), [rúbrica](rubric.yml) i [protocol de revisió](guide.yml).
- [Validació sintètica d’origen](validation.json), conservada com a antecedent; el seu camp `report` es refereix al repositori Unaltramesa.
- [Validació d’aquesta integració](integration-validation.json), amb runtime, empremtes i comprovacions locals.

TIG conserva la definició docent. El motor, els checks, la pseudonimització, les evidències i l’ODS pertanyen a **Unaltramesa**. No s’ha copiat codi del motor. La guia operativa d’origen és `/home/benizar/git/unaltramesa/docs/tig-pr1-vscode.md`; el flux per a exportacions noves és a `docs/manual-review-workflow.md` del mateix proveïdor.

La integració només utilitza fixtures sintètiques. No selecciona una cohort real ni aprova la privacitat dels lliuraments. Les instruccions següents queden preparades per al terminal del docent; la revisió humana d’aquest document continua pendent.

## Validar la definició sense lliuraments

Amb el MCP Unaltramesa vinculat a l’arrel de TIG, cal executar:

```json
{
  "tool": "plan_activity_review",
  "arguments": {
    "source": "practiques/pr1-project-setup/revisio/moodle-confirmed-2026-10-18",
    "edition": "moodle-confirmed-2026-10-18",
    "required_parts": ["micropractice"]
  }
}
```

El resultat ha de ser `ok: true`, amb l’empremta efectiva indicada i només els tres criteris 70/20/10. Aquesta operació valida la definició, sense preparar ni llegir lliuraments. Qualsevol canvi normatiu posterior necessita una altra edició.

## Preparació del terminal docent

Les ordres d’operador s’executen fora d’una sessió d’agent amb accés als originals. El terminal integrat de VS Code o VSCodium és adequat. En cada invocació es declara el directori de dades mitjançant `MCP_CONSUMER_WORKSPACE`; no s’ha d’executar l’operador sobre l’arrel del repositori TIG.

```bash
TIG_ROOT='/home/benizar/git/tig'
MESA_ROOT='/home/benizar/git/unaltramesa'
ACTIVITY_SOURCE="$TIG_ROOT/practiques/pr1-project-setup/revisio/moodle-confirmed-2026-10-18"
export UNALTRAMESA_IMAGE='sha256:e4e0edeed0f159e5968f7435d32dc4eeb8b80c6b5071879b5952c4e12163867c'
docker image inspect "$UNALTRAMESA_IMAGE" >/dev/null
```

És la imatge local validada d’Unaltramesa **0.10.0**, pipeline documental 2 i política de preparació 3. El llançador usa `--pull=never`. Si la imatge no existeix, cal obtenir del proveïdor el runtime verificat; no substituir el pin per una etiqueta mutable. `ACTIVITY_SOURCE` ha de continuar fora del sandbox de lliuraments.

### Exportació ja preparada

Aquest camí requereix originals, mapa privat, clau i staging previs. Cal situar el terminal a l’arrel d’aquella exportació, dins de `TIG/sandbox/`, i conservar els aliases existents. El recompte 30 és el del conjunt previst i es comprova explícitament; si la cohort és una altra, cal revisar la selecció.

```bash
EXPORT_ROOT="$PWD"
EXPECTED_SUBMISSIONS=30
MCP_CONSUMER_WORKSPACE="$EXPORT_ROOT" \
UNALTRAMESA_ACTIVITY_SOURCE="$ACTIVITY_SOURCE" \
"$MESA_ROOT/scripts/run-operator.sh" bind-existing-export \
  --activity-root /activity-input \
  --edition moodle-confirmed-2026-10-18 --part micropractice \
  --cohort tig-pr1 --run revisio-2026-10-18 \
  --expected-submissions "$EXPECTED_SUBMISSIONS"
```

La vinculació congela la definició i revoca l’autoritat de revisió anterior. No aprova ni requalifica. Cal previsualitzar la migració i revisar-ne el resultat:

```bash
MCP_CONSUMER_WORKSPACE="$EXPORT_ROOT" \
"$MESA_ROOT/scripts/run-operator.sh" migrate-preparation \
  tig-pr1-moodle-confirmed-2026-10-18 . \
  --generation pr1-moodle-v3 --expected-submissions "$EXPECTED_SUBMISSIONS"
```

Després de comprovar la previsualització, l’operador executa explícitament:

```bash
MCP_CONSUMER_WORKSPACE="$EXPORT_ROOT" \
"$MESA_ROOT/scripts/run-operator.sh" migrate-preparation \
  tig-pr1-moodle-confirmed-2026-10-18 . \
  --generation pr1-moodle-v3 --expected-submissions "$EXPECTED_SUBMISSIONS" --execute
STATE_ROOT="$EXPORT_ROOT/.unaltramesa/generations/pr1-moodle-v3"
```

La generació anterior, les propostes i les graelles es conserven. Una generació existent no se sobreescriu. Si falten mapa, clau o staging previs, cal utilitzar el flux d’exportació nova.

### Exportació nova

El docent prepara un directori nou i hi extreu les carpetes Moodle directament dins d’`originals/`. L’estructura prevista és `sandbox/revisions/pr1-moodle/tig-2026-27/run-01/originals/`. No s’ha de copiar la definició docent a aquest sandbox ni fusionar-lo amb un run anterior.

```bash
EXPORT_ROOT="$TIG_ROOT/sandbox/revisions/pr1-moodle/tig-2026-27/run-01"
test -d "$EXPORT_ROOT/originals"
MCP_CONSUMER_WORKSPACE="$EXPORT_ROOT" \
UNALTRAMESA_ACTIVITY_SOURCE="$ACTIVITY_SOURCE" \
"$MESA_ROOT/scripts/run-operator.sh" pilot-review-run \
  --activity-root /activity-input --manifest activitat.yml \
  --edition moodle-confirmed-2026-10-18 --part micropractice \
  --cohort tig-2026-27 --run run-01 --scope tig-2026-27-pr1-moodle
STATE_ROOT="$EXPORT_ROOT/.unaltramesa"
```

Aquesta ordre congela la selecció, pseudonimitza i verifica. Repetir exactament la selecció audita l’estat existent; no el substitueix. L’àmbit de pseudonimització identifica el curs i l’activitat i s’ha de conservar en les continuacions.

## Auditoria i aprovació visual

Cal obtenir `approval_ready: true` i comparar personalment els documents preparats amb els originals: identitats, text, captures, llegibilitat i fidelitat. Els bloquejos de format o processament es resolen amb Unaltramesa; no són errors acadèmics ni zeros de l’estudiant. Un comptador de progrés no acredita l’auditoria.

Només després d’aquesta inspecció, el docent executa:

```bash
MCP_CONSUMER_WORKSPACE="$EXPORT_ROOT" \
"$MESA_ROOT/scripts/run-operator.sh" approve-review-run --confirm-visual-review
```

Si hi ha pèrdues de fidelitat declarades, `--confirm-fidelity-review` exigeix una comparació personal addicional. No s’ha d’afegir per ometre un bloqueig i no converteix l’evidència degradada en una revisió completa.

## Correcció assistida i revisió docent

L’agent revisor necessita una sessió limitada a l’staging aprovat i la safata de propostes. El muntatge del MCP no inclou mapes d’identitat ni informes nominals. Les eines genèriques de fitxers i terminal del client necessiten una frontera de sistema de fitxers pròpia: obrir una carpeta nova no demostra aïllament.

Amb aquesta frontera comprovada, es pot obrir `"$STATE_ROOT/staging"` en una finestra nova (`code --new-window` o `codium --new-window`) i reconnectar el MCP. Cal comprovar `runtime_identity`, `describe_workspace`, `list_catalog.selected_recipe` i `get_activity("tig/pr1-moodle")`. La recepta seleccionada ha de ser `tig-pr1-moodle-confirmed-2026-10-18`, amb la mateixa empremta efectiva.

Petició preparada per a la sessió revisora:

> Usa exclusivament l’activitat seleccionada `tig/pr1-moodle`, edició `moodle-confirmed-2026-10-18`. Per cada carpeta `stu-…`, executa els checks de la recepta, recupera tots els lots de text i inspecciona les pàgines i figures pertinents. Declara si tens visió operativa. Separa fets, interpretacions i incerteses, cita les evidències i desa una proposta amb `save_review_proposal` als tres blocs 70/20/10. No introdueixis subpesos, CNIG, EPSG fix, composició obligatòria ni segon PDF. Deixa pendents els judicis no comprovables i la pauta de noms de classe desconeguda. Contrasta les propostes amb la mateixa rúbrica, sense corba ni rànquing. La puntuació final i les decisions d’integritat corresponen al docent.

Convé revisar el primer resultat abans d’estendre la correcció a tota la cohort. Els checks aporten evidència i la IA proposa; el docent confirma cada bloc i completa els controls d’obertura, municipi, funcionalitat i interpretació.

Des del terminal docent, es poden generar els dos ODS fins i tot amb propostes pendents:

```bash
MCP_CONSUMER_WORKSPACE="$EXPORT_ROOT" \
"$MESA_ROOT/scripts/run-operator.sh" run-operation worksheets
```

La vista pseudònima és `"$STATE_ROOT/reports/review-proposals.ods"` i la nominal editable, `"$STATE_ROOT/reports/teacher-workbook.ods"`. Cal tancar el llibre abans d’actualitzar-lo. El refresc conserva decisions i anotacions, reté la versió anterior i refusa canvis d’assignació o evidència. L’ODS nominal no s’introdueix al context de l’agent.

## Exclusió de l’estat privat

Tota execució real es manté sota `sandbox/`; tots els fitxers d’identitat, claus, auditories, staging, propostes i ODS romanen dins de `.unaltramesa/` del run. Aquests directoris estan exclosos de Git. `_config.yml` exclou `sandbox/`, `dist/`, `practiques/` i `.unaltramesa/`, inclosos els estats imbricats.

Els paquets d’alumnat es componen amb les seleccions explícites d’Unaltraweb i les dependències declarades del productor QGIS. La definició de revisió i l’estat privat no són productes seleccionables de PR1. No s’ha de comprimir recursivament `practiques/`, `sandbox/` o l’exportació Moodle per distribuir-los. El paquet nominal es conserva només a la banda docent.

Ignorar fitxers evita incorporacions ordinàries a Git; no autoritza a esborrar-los ni substitueix l’aïllament de la sessió revisora. Les proves d’exclusió d’aquesta integració utilitzen marcadors sintètics i no llegeixen lliuraments reals.

## Repetir les comprovacions

Des de l’arrel de TIG, amb les tres imatges locals fixades al verificador:

```bash
python3 practiques/pr1-project-setup/revisio/moodle-confirmed-2026-10-18/verify_integration.py --write-report
```

`verify_integration.py` només munta la definició i una carpeta temporal de fixtures. No munta el repositori complet ni cap exportació Moodle real. Verifica els set fitxers importats, la selecció 70/20/10, els casos amb un PDF, amb un PDF addicional i sense apunts, i el rebuig d’una edició incorrecta. Executa els 14 checks d’Unaltramesa sobre el cas sintètic; això no acredita correcció geogràfica, obertura real a QGIS ni qualitat visual.

Les proves d’exclusió comproven vuit rutes privades a Git i deu marcadors amb Jekyll 4.4.1. La prova Jekyll utilitza les exclusions reals de TIG, amb contingut sintètic i el tema i els plugins desactivats; no reconstrueix el web complet. El compositor d’Unaltraweb crea un ZIP només amb el fitxer seleccionat i refusa tres seleccions de productes docents, fonts o controls. L’informe registra les imatges i els hashes de configuració i del verificador.

En aquesta integració, `site_check` retorna `ok: true`. Manté 90 avisos previs sobre imatges amb fons transparent o no verificable i avisos editorials dels capítols existents. No s’han modificat aquestes imatges ni els capítols. `prose_check` del runtime actiu refusa aquesta guia perquè només admet contingut públic; la guia queda revisada localment, amb els enllaços i els vuit blocs d’ordres comprovats, i pendent de revisió humana.
