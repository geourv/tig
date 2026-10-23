# Inventari local de paquets de pràctiques

Aquest registre identifica edicions locals, fonts, comprovacions i límits. Les setze lectures tenen aprovació de primera versió des del 18/10/2026. Els PDF i els bundles de pràctiques són recursos locals, exclosos del web; la seva distribució a Moodle es decideix separadament. La reserva i les seleccions de l’autor consten a [TIG #28](https://github.com/geourv/tig/issues/28).

## Manual aprovat i comprovat · 23/10/2026

`make test` amb el digest immutable de Web 0.7.1 ha completat el PDF, build
i auditoria HTML. El gate editorial de fonts i resultat renderitzat passa.
El manual aprovat té **325 pàgines**, sense ESBORRANY, SHA
`eb174bd4b8e61d092d7dfceca3b0884ecf2dc3f8969052a03bbc047a63daf9af`.
La còpia retinguda és
`sandbox/practiques/pr4-geoprocessament/manual-2026-10-vector-r2-approved-20261023/`.
El PDF HTTP coincideix; s'han revisat web d'escriptori/mòbil i pàgines del PDF.
Els detalls i avisos consten a `pr4-roi-geoprocessament.md`.

Els setze PDF de pràctiques i els deu bundles conserven l'estat i els hashes
de l'auditoria del 22/10. Aquesta validació del manual no aprova els quatre
esborranys PR4/Reus ni crea una edició de distribució de les pràctiques.

## Autorització de latest i estat de les lectures · 22/10/2026

L'autor aprova expressament publicar el manual actual, amb les captures d'atles
ajornades i els avisos de figures documentats. Autoritza commit de fonts, push,
PR, integració a `main` i desplegament. Les onze fonts públiques són `approved`.
Les quatre lectures PR4/Reus continuen **draft**, segons la seva selecció
«Conservar-les en esborrany»; els seus PDF, hashes i 91 pàgines no canvien.

La continuació de captures és [#37](https://github.com/geourv/tig/issues/37),
primera tasca de continguts quan el capturador i la família compatible estiguin
actualitzats. El sondeig no publicable s'ha retingut fora d'`assets/`, sense
alterar-ne els bytes ni el diagnòstic anterior. La publicació del manual actual
no acredita una captura o exportació d'atles que encara no s'ha executat a TIG.

## Preparació conjunta i estat de latest · 22/10/2026

L'autor demana acabar de preparar `latest` i deixar disponibles els materials
locals de pràctiques. També ha acceptat **preparar la migració** del consumidor
Web 0.7.1 al punt publicat 0.7.3, amb revisió prèvia dels conflictes.

### Materials verificats i índex vigent

- **16 PDF / 172 pàgines** concorden byte per byte amb els hashes retinguts:
  12 lectures v1 aprovades, 81 pàgines; 4 lectures PR4/Reus vector-r2 en draft,
  91 pàgines. Les fonts actuals coincideixen amb els snapshots dels jobs triats.
- Tots els artefactes dels rebuts, recompte de pàgines, A4 horitzontal, marca
  d'esborrany pertinent, seccions docents, logs i límits de text són correctes.
- **10 bundles GIS** acceptats pel `practice-check` públic 0.6.1, amb selecció
  `resolved-project` i dependències: vuit casos del recorregut, ROI 143 controls
  i Reus 80 controls. És verificació de segells/contractes, no una reexecució GIS.
- Els **set imports PR1** de l'edició Moodle confirmada mantenen els hashes.
- Informe create-only: `sandbox/practiques/materials-readiness-20261022-01.json`,
  SHA `02194000a197f06bd4fff2dcbc1e2dc7d79a846e28ffb4f60c79d23d4e038270`.
- `practiques/README.md` ofereix ara l'índex únic dels setze PDF vigents per a
  revisió. El report no és una edició PDF/ZIP ni aprova els quatre esborranys.
- Els setze enllaços, recomptes i fitxers de l'índex s'han contrastat amb
  l'informe. `prose_check` no admet aquest índex privat com a target editorial
  (`Editorial target must be reader-facing content or public metadata`);
  no es presenta aquesta exclusió com una comprovació de prosa superada.
- Les instruccions de correcció i la seva integració amb Unaltramesa es
  mantenen com a tasca d'autoria separada [#35](https://github.com/geourv/tig/issues/35).

### Capturador: implementat en local, encara no adoptable

El [retorn del proveïdor](https://github.com/dosquartsdedocs/unaltracaptura-qgis/issues/27#issuecomment-6329069144)
acredita una implementació local `0.7.0.dev0`, sense commit ni release:
401 tests, 43 Qt/QGIS, smoke, 22 conjunts forçats, dues captures del mateix
compositor i PDF de tres pàgines. Els exemples específics de Reus són a
`docs/tig-atlas-handoff.md` d'aquell checkout. Aquest retorn encara no és una
release que la sessió TIG pugui adoptar ni una execució sobre el cas real.

La connexió actual és QGIS MCP **0.6.1**, controller
`sha256:d06b742c3e7d2e9383cf8a1d22bce928dd806f316a0bcbb1f676f50e22e94b05`,
sense drift i amb el mateix worker QGIS 3.44.11. Web **0.7.3** declara v1/v2;
cal publicar el candidat i acceptar explícitament el nou perfil v3 a la família.

### Web i publicació

Web 0.7.3 està connectat a TIG, sense drift, controller
`sha256:0a5b91a4c1c8b3b0bd8d3c4160ed1e5b9ccc8ad3cd0abee67f621d8636d15bd6`.
És la selecció immutable del runtime; els pins del consumidor continuen a 0.7.1.
`site_check` passa i el PDF local de 327 pàgines continua `fresh`.

`build_site` i `manual_release_status(latest)` fallen pel socket exclòs
`.unaltramesa/project/operator.sock`; el candidat antic de `tmp/manual-release/latest`
no acredita aquesta revisió. La correcció del snapshot correspon a Web.

La [preparació de migració #36](https://github.com/geourv/tig/issues/36) reté el
pla `962d50d85c086182cc36a3e1f8a977a6eb9835136958bfc2406ed5db4794567d`:
Makefile, Gemfile, lock i scaffold; conciliació de `.gitignore` i del workflow
de fonts. El workflow publicat només canvia la versió del paquet 0.7.2→0.7.3.
S'ha detectat també que la plantilla de gem 0.7.3 es combina amb el commit
de core 3332e0… que declara 0.7.1. Cal un tuple coherent del proveïdor abans
de tornar a revisar/aplicar un pla CAS. No s'ha aplicat aquesta migració.

S'han tramès dos informes reproduïbles al proveïdor Web:
[snapshot i socket exclòs #114](https://github.com/dosquartsdedocs/unaltraweb/issues/114)
i [coherència del tuple gem/core #115](https://github.com/dosquartsdedocs/unaltraweb/issues/115).
Inclouen proves d'acceptació i preservació dels controls existents; són
incidències obertes, no reparacions ja implementades.

En aquesta fita de preparació encara es preveia completar l'atles abans de
publicar. L'autor n'ha autoritzat posteriorment l'ajornament a #37, tal com
recull l'apartat d'autorització. El workflow manté el requisit del SHA de
`main` revisat exacte. La connexió gaContExt de memòria no està disponible en aquesta
sessió; el seguiment nou queda en aquest dossier i a #36, sense afirmar una
persistència nova al servei de memòria.

## Reestructuració de PR4 i Reus · `2026-10-vector-r2`

L'autor ha rebutjat editorialment r1 i ha acceptat ampliar la reserva de #34
a 124 paths. El nou capítol integra concepte, eina, resultat i comprovació,
començant per envolupants i explicant distàncies abans de buffers. Les quatre
lectures PR4/Reus s'han adaptat després; totes continuen en `draft`.

La fita ROI `roi-run-20261020-04` té 143 controls, SHA
`b17cbbbfb9a9e23eca45a1f9c86f80f590ed14a87df37aa6dd2c5bf3b70e431d`.
La fita Reus `tesselles-run-20261020-04` té 80 controls, SHA
`be001fde84b38fe4315382e42e6fe23107713c9aaf3e3662bc8ed0cc1c2c4bb7`.
Les carpetes són sota `sandbox/practiques/` de cada pràctica; originals,
preparacions i runs previs es retenen. S'han regenerat 33 conjunts de captura
amb WMS real, contorns sense farciment i anotacions contrastades amb la recepta.

L'atlas té 82 cel·les, layout i iteració nativa comprovats. No hi ha encara
captura del compositor ni PDF multipàgina segellat; `atlas-configuracio`
mostra només el diàleg natiu d'exportació. La limitació del proveïdor és a
la nota `ead73d2cba6c4aa8b4381207fe8c6bc0` i al README del cas Reus.

### Lectures locals comprovades

Els quatre PDF sumen **91 pàgines**, A4 horitzontal i marca ESBORRANY. Jobs
sota `sandbox/practiques/<slug>/lectura-2026-10-vector-r2-ca-<destinatari>-<run>/`.
El fitxer és `outputs/LLEGIU-ME.pdf`; els snapshots i tots els artefactes
coincideixen amb les fonts actuals i els hashes dels rebuts.

| Pràctica i destinatari | Run | Pàgines | SHA-256 de la font | SHA-256 del PDF |
| --- | --- | ---: | --- | --- |
| PR4 alumnat | `revisio-02` | 27 | `006164aa43691254110618a7b385e445fd65537954ed3a1bfde5ae297ced11c5` | `4fb313cf07ea9f4b2b7a3765bdc28098c1dd43197b5c15a9057a8106ec744c04` |
| PR4 docent | `revisio-02` | 23 | `d0f4a81b9b3621d6b3241f24a7e81444337663c34812cac640d15685e22b0367` | `63c19959662fa8d2a4598a6254a06811c086ac80a5005af37377b30b29f6e871` |
| Reus alumnat | `revisio-01` | 23 | `3b403f80ace949262a1e01a6ff6bd465d7f24a580afcbf8924dc4363ed8f3e2d` | `f89245e5e1e59e00cb10a2e29bceb60b9b19d77fb78c8d446785fabe2b6c31a0` |
| Reus docent | `revisio-02` | 18 | `0916f3699342eed51e8fbad290364004f751fd2307e5caded92514b1dd06e93d` | `2eb92904ccc0a4ac29baad02cc129cd97e4bdbe9115549930cadc29c9a9a881d` |

Els primers runs es retenen. S'ha corregit un `Overfull` de 3,36 pt a PR4
alumnat i s'han compactat una taula i finals de referències de les guies
docents. Els logs finals no tenen desbordaments, caràcters absents ni
referències indefinides; el text queda dins de les pàgines. S'han inspeccionat
les figures i les pàgines de procediment, taules, atlas i tancament.

Sessions Web públiques, 0.7.2 sense drift, worker PDF immutable ja fixat:
`7af995b42a1048a7b54a3540c17a8fbb` (lot inicial) i
`045f6d6e95c142f0924ad144a7156484` (correccions). Totes les construccions
retornen `publishes: false`. La validació editorial no implica aprovació
humana; els PDF v1 i r1 continuen retinguts.

### Manual local de revisió

El PDF català té **327 pàgines**, 80.234.190 bytes i SHA-256
`86992d06368bb12be8c74a068c5892eeabd6ff66b5886f81a67f3db53cb9285b`.
`manual_pdf_preview_prepare` retorna `publishes: false` i rebut
`6da6ad367b29c6b5af98afe6580f73be7fed4f9d28b44477c94b4926ee93283e`.
S'han conservat còpies dels set fitxers de sortida natius a
`sandbox/practiques/pr4-geoprocessament/manual-2026-10-vector-r2-revisio-01/`,
`manual-2026-10-vector-r2-revisio-02/` i `manual-2026-10-vector-r2-revisio-03/`;
la tercera correspon al PDF final. Són snapshots de revisió, no bundles GIS
segellats ni edicions publicades.

La inspecció ha corregit al Markdown les línies que desbordaven el bloc de
text del capítol. El cos passa el control de marges; queda una observació
tipogràfica de l'URL QGIS a la bibliografia generada, uns 4 pt més enllà del
bloc estimat però dins de la pàgina. Les 29 captures PNG referenciades són
opaques; els sis avisos restants d'aquest capítol corresponen als SVG
conceptuals previs. La comprovació general que exhaureix pressupost s'ha
complementat amb `image_background_check` acotat al capítol.

## Antecedent rebutjat editorialment · `2026-10-roi-r1`

Les comprovacions següents corresponen a la fita r1. L'autor en va rebutjar
l'ordre i la inserció de captures el 20/10/2026; els hashes i les proves es
conserven com a historial, sense donar per aprovades les fonts actuals.

Reserva acceptada a [TIG #34](https://github.com/geourv/tig/issues/34).
L'autor ha precisat que l'Explorador ha de mostrar les connexions als tres
GeoPackage i que el WMS IGN/PNOA ha d'aparèixer sota els vectors. S'han
renderitzat 20 conjunts PNG/SVG/manifest amb el MCP QGIS 0.6.0 en mode
`offscreen`, sense avisos. Les fonts del capítol 6, la continuïtat del 8 i
les dues lectures PR4 són `draft`; aquesta revisió no és una edició aprovada.

| Font relativa a `practiques/` | Pàgines | SHA-256 de la font en revisió | SHA-256 del PDF |
| --- | ---: | --- | --- |
| `pr4-geoprocessament/ca/alumnat/LLEGIU-ME.md` | 21 | `483cbc44f68b13431df970819eb9900a79b3e928b899a4e97aa89f1e9dbf3471` | `371061a52c983ff4d1d5480912b8b1eb4539b7a2d24c64f8e45ad8a77f4b63f2` |
| `pr4-geoprocessament/ca/docent/LLEGIU-ME.md` | 18 | `10964606e85ca08a7a3dd917d5ba80fa02e1ae18c2220d6079e52eb80c919c9a` | `0071cd1a3bed4e7c29b5bec28b3e4bc54f6f0cefb186b43ca1cf2a74d36eceb1` |

Jobs sota `sandbox/practiques/pr4-geoprocessament/`:
`lectura-2026-10-roi-r1-ca-alumnat-revisio-01` i
`lectura-2026-10-roi-r1-ca-docent-revisio-02`. La primera construcció docent
es reté: tenia un desbordament d'una expressió inline, corregit al Markdown.
Les fonts finals coincideixen amb els snapshots, els artefactes coincideixen
amb els rebuts i els PDF són A4 horitzontals amb marca ESBORRANY. Els logs
finals no tenen `Overfull`, caràcters absents ni referències indefinides.

El cas científic complementari és
`sandbox/practiques/pr4-geoprocessament/roi-run-20261019-03/bundle.json`, amb
segell `3960e5e074f50d6c40bf2d7c00305b96dc1fc480691b35200b76d59c9375601f`.
`practice-check` confirma l'arbre, la selecció del projecte resolt i els 131
controls. Els tres originals conserven els seus hashes després de les captures.
La primera versió i els vuit casos anteriors continuen retinguts.

El [registre de treball](pr4-roi-geoprocessament.md) identifica les sessions,
els controls, el preview i les limitacions del build web. La comprovació
d'imatges acotada al capítol confirma opacitat de les 14 captures PNG noves
referenciades al manual; els avisos de transparència corresponen a les figures
conceptuals anteriors. La inspecció general havia exhaurit el pressupost abans
d'arribar a aquestes imatges, motiu pel qual s'ha fet el control acotat.

El manual PDF local revisat té 329 pàgines, SHA-256
`a4f513ebf22dc4fe4e95fc3cf3b990347a7ddadbae2e494eb7d64da1b98f9c50`.
El preview etiquetat ha servit el capítol i aquest PDF, amb comprovació visual
d'escriptori i mòbil. `build_site` continua bloquejat pel socket privat
`.unaltramesa/project/operator.sock`; queda registrat com a incidència del
proveïdor, sense aturar Unaltramesa ni modificar-ne les dades. El contingut
continua en esborrany per a la revisió de l'autor.

## Primera versió aprovada · `2026-10-v1`

L’autor ha aprovat totes les activitats com a primera versió i ha autoritzat integrar les fonts pendents a Git: [registre del vistiplau i de l’abast](https://github.com/geourv/tig/issues/28#issuecomment-6253787193). També ha confirmat publicar `latest` a Pages quan passin les comprovacions i la integració a `main`. L’actualització tècnica del scaffold 0.7.1→0.7.2 queda ajornada expressament.

Les dues lectures PR1 s’han harmonitzat amb `tig/pr1-moodle`, edició `moodle-confirmed-2026-10-18`: GPKG, projecte incrustat/extern, WMS i apunts PDF són bàsics; la composició és opcional. La font CNIG, l’EPSG i un segon PDF pertanyen al recorregut ampliat, no s’afegeixen al mínim de la micropràctica. La rúbrica manté tres blocs globals de 70/20/10 sobre 100, equivalents a 7/2/1 sobre 10, sense subpesos. S’han contrastat els set fitxers importats amb `import-manifest.json`: tots conserven els bytes i hashes confirmats.

En aquella fita, les setze lectures eren `content_status: approved`. Els altres catorze cossos Markdown coincidien amb r4; només canviava l’estat editorial. Els PDF es van construir amb la versió **`2026-10-v1`**, run **`primera-01`**, a `sandbox/practiques/<slug>/lectura-2026-10-v1-ca-<destinatari>-primera-01/outputs/LLEGIU-ME.pdf`. Són **108 pàgines**, A4 horitzontals i sense marca ESBORRANY. `practiques/README.md` continua enllaçant els setze resultats retinguts.

| Font relativa a `practiques/` | Pàgines | SHA-256 de la font aprovada | SHA-256 del PDF |
| --- | ---: | --- | --- |
| `pr1-project-setup/ca/alumnat/LLEGIU-ME.md` | 8 | `9a827f7b26c48f7b688df19b743c1e621c1e832f2c2043fbc0e1daebf42cea93` | `6694c9684f4f9a2328961d34e27e0c42d97e29929d4e641b3780cf99374e05a1` |
| `pr1-project-setup/ca/docent/LLEGIU-ME.md` | 9 | `616be6f15862b22f60fa7d8c352df725a3dfc8056c6664f420d8921949ee04f2` | `6756eb0594ae50d34c245b3d7320332cf6e3b91c650ab9f7bc67b1da051627bb` |
| `pr2-digitalitzacio/ca/alumnat/LLEGIU-ME.md` | 6 | `f8001e17c90d6c2dad2c4e901320f2e3e1d1bab09dc8ed8bb2fec2a38d4bdd70` | `3590e891e61020ab931c2ecf84830a4dae9d0181dbc09950df162cecc8a27068` |
| `pr2-digitalitzacio/ca/docent/LLEGIU-ME.md` | 6 | `4eca83af1a4d6520bb6c76922ed97cd6bb88e15b0d673e14fb478ad0defdb827` | `72e03659dab50047a66f16c91c22f48ca8f25b4a5bf7e40c1209e02f3f59208d` |
| `pr3-consultes/ca/alumnat/LLEGIU-ME.md` | 7 | `396824d1e5155b2822a5165f8c0aa024e54ffc3a7ac0006a4e9ca782d251640c` | `8998ef8da0b76d0c303869f084248362e6dab115a862f1fd0b224057e5a043c1` |
| `pr3-consultes/ca/docent/LLEGIU-ME.md` | 8 | `0054b8a8709587c4fca97e60716f1dbac19f7e58f09c25a0ced6a91cb21f0871` | `c24f7a43d168d6668da8e16e92f9be7946f7f94dde71dd7852fcf578db1848b6` |
| `pr4-geoprocessament/ca/alumnat/LLEGIU-ME.md` | 7 | `f964e9392a4e909dfb5525e03976d186281c8a13b956a4437faf2550c2481a6b` | `672c8f21ff096f48dee1b4b5851f52cd0298fb6ec093bfbd5089b3ecbb917cbf` |
| `pr4-geoprocessament/ca/docent/LLEGIU-ME.md` | 7 | `30abdb03177ac16ab46f2c2f358678c5fa593bab65e892bb7b1ea5bbae12c378` | `acd5c03201aedc08abb79bff9323b837862a51e6436ae10bc7d1e65b3803edd2` |
| `pr4-tessellacions-reus/ca/alumnat/LLEGIU-ME.md` | 6 | `4d9b219f5b4a40e147d86e6afb603cd3d322b11aeefe775054cecd1ff9b661e7` | `12ede4f83866f40af72014c9e214d1e4ade0cbeff0e0d92c144880604afc3d47` |
| `pr4-tessellacions-reus/ca/docent/LLEGIU-ME.md` | 7 | `4316c6ad7eb6006243813bef112da1c96382d2278e1e853f1469206157a7072e` | `f37cb095d574ad27dff414a7f72238de1f302ee631fef9c0787067ecc8c418d3` |
| `pr5-raster/ca/alumnat/LLEGIU-ME.md` | 7 | `7d3886a975d0b41068ac8c08ab03c1405dd849e3fd2dd570396142ca040d959d` | `cc6a7c803493488e2b73af0213be50978aad05ac04d9015ef04b1881c3e16911` |
| `pr5-raster/ca/docent/LLEGIU-ME.md` | 7 | `2f383f6ba0b58e15b00cb4bc88e1ea57e991ab2cf9cc88a18bf0d44cf05ffd60` | `d31c5a8e35c816a234a62e53329f9132107c294bb53eaf8d462b8ae933179f43` |
| `pr6-sintesi/ca/alumnat/LLEGIU-ME.md` | 6 | `d548b08d65aa88a05ca4f03180e75a71044afb7ce5b8119324fa177a9dc7eea6` | `00b88e000999a85e573a422217d938815e0ecc0cf56ca6933a77f27ed265fedf` |
| `pr6-sintesi/ca/docent/LLEGIU-ME.md` | 7 | `12eba00f33bab87f1f78723a333e58e2884422208d6cfc6f02a88a0ae243da28` | `649d94536bf49e097bcf85d3236d3c7ca4f1036e6da843ec3b82c065d2ae3230` |
| `bonus-pyqgis-sql/ca/alumnat/LLEGIU-ME.md` | 5 | `f0129271d3a4e3cf6403afb43daf0f0b5edd7837fb568711cc4596832266a132` | `e6175eeb6344198a3b482c3a7d606fe32da3e56fb313ba6bf506e7f05f856939` |
| `bonus-pyqgis-sql/ca/docent/LLEGIU-ME.md` | 5 | `597ab28691081ed7990c67edf84f34d441c7a8bc91d3ab193675324bf0185519` | `0c56e2dd0feb1730e3ef24eb1382cd85c832bd7d4993b35afe2e47d021164fa4` |

### Verificació de les lectures i conservació

`prose_check` final cobreix les setze fonts aprovades, sense omissions, findings ni avisos. La comprovació dels PDF contrasta els hashes retornats pel productor, tots els artefactes dels rebuts, els snapshots de font, dimensions, pàgines i text dins dels límits. Les dues lectures PR1 s’han obert i llegit després de l’harmonització; els altres catorze textos mantenen el cos revisat a r4. Els logs no tenen `Overfull`, caràcters absents ni referències indefinides; resten els dos `Underfull` menors coneguts i avisos de plantilla. També s’han comprovat sintaxi Python, requests JSON i XML del model.

La lectura PR1 d’alumnat s’ha construït a la sessió MCP integrada. La resta utilitza la sessió serial `c67fddea72164210b8e12e948438f01f`, contenidor `f48d865f22a95137ded2b4b84cbb8974292627561925f835a737c34d6f78ad0b`, Web 0.7.2 sense drift i worker PDF fixat. `session-status` acredita aturada i recursos alliberats. Totes les construccions retornen `publishes: false`.

Les fonts PR1 ICGC `activity.json`, `compute.py`, `prepare_inputs.py` i `edition-2026-10-review-r1.json` es conserven i es versionen deliberadament com a antecedents, segons el README de PR1. El descriptor antic no és una edició activa ni s’hi substitueixen els hashes per aprovar les lectures noves. Els vuit bundles docents i els intents històrics conserven els seus segells. Les dades, els PDF i els paquets continuen ignorats i retinguts.

### Manual públic i primera publicació latest

L’inventari editorial públic observa onze fonts aprovades i cap font pendent. `editorial_publication_check` passa; manté els avisos previs de prosa. L’autor ha confirmat expressament conservar les imatges actuals malgrat els avisos de transparència i d’opacitat no verificable, i ajornar-ne la revisió. El seguiment de figures queda obert a la memòria del projecte, nota `2c77ebaa862c44e2a6c718e9f86f1124`; no és una certificació d’opacitat.

La comprovació local executada és:

```bash
MCP_IMAGE=sha256:576dcd772f2c345fa2021745f975f8392568d8d2783f7a66ba41a3521b3bd546 make test
```

Ha acabat correctament: preparació del PDF, `site_check` abans de Jekyll, build i auditoria HTML. La fase Jekyll informa 173,684 segons. L’override immutable del runtime queda documentat; els pins persistents del consumidor no s’han migrat. El PDF `tmp/manual-pdf/ca/manual-ca.pdf` té **311 pàgines**, 43.589.176 bytes i SHA-256 `e4b464a77f7ed666c2565696c98ae0a5f1e1c0683d22671b7060c15bd55b2d04`. Portada: `c931baab15348e839a9ec560e22a432e3af37c364a88c819702265920d4a42c1`. El rebut de preview és `ce338dbb6c70824b2db93081701d9b37f8704e5cacd140a40e0c91dd20f3cf0e`; `manual_pdf_status` observa `fresh`, `ready_to_publish` i selector `latest`.

El canal MCP integrat ha esgotat el temps en arrencar el preview, tot i completar-ne el servidor. S’ha preservat el resultat i s’ha recuperat la revisió amb el llançador públic: sessió `62ea8c8df127490d84f33dae8585b4ab`, contenidor `14b427040f56b8ec759066e2e4a9071a4280398f18b12b94255877fd6e95a42e`. S’han comprovat HTTP 200, portada, canal `latest`, capítol de síntesi i PDF complet, i s’ha inspeccionat la captura d’escriptori. La prova mòbil amb emulació CDP, sessió `6288995a981248ca954c001df1fee4e3`, verifica `innerWidth=430` i `scrollWidth=430` al capítol de consultes. El primer retall per mida de finestra de Chrome no equivalia a aquesta emulació i no es compta com a prova responsive. Els previews es tanquen amb l’eina del propietari.

La publicació és un pas posterior al commit i a la integració via PR. El workflow exigeix un `reviewed_sha` igual al commit seleccionat de `main`. La confirmació del desplegament i el seu SHA es registraran a la issue; no es declara publicada cap execució local.

## Antecedent de revisió docent i Moodle · `2026-10-r4`

Continuació de la reserva acceptada, 15 d’octubre de 2026. S’ha adaptat el patró de les guies locals de Geodisseny —especialment xarxa vectorial i estadística de Constantí, vinculades a [Geodisseny #11](https://github.com/geourv/geodisseny/issues/11)— a les vuit pràctiques TIG. Les fonts de Geodisseny s’han consultat només en lectura. El criteri durador és a `context/writing-profile.md`.

Aquella revisió té **16 PDF, 106 pàgines i els mateixos 8 bundles GIS docents**. Cada guia docent inclou preparació i durada orientativa, conducció i aturades de control, passos de Moodle i un enunciat per copiar fins al final de «Qualificació». Les lectures d’alumnat comparteixen el criteri i les propostes d’ampliació. L’índex vigent de la primera versió és `practiques/README.md`.

Els màxims són **7 punts de treball bàsic, 2 d’ampliacions i 1 de documentació**. El professor selecciona els obligatoris a classe i els recull a Moodle; la lectura sencera no és una llista automàtica de requisits. Reus s’integra a PR4 i el bonus contribueix al 20% de la pràctica indicada, sense doble recompte. A PR6 es diferencia la síntesi guiada de la funcionalitat pròpia addicional. La documentació també pot augmentar la nota sobre el bloc bàsic.

### Lectures i identitats de revisió

Jobs sota `sandbox/practiques/<slug>/lectura-2026-10-r4-ca-<destinatari>-<run>/`, amb PDF a `outputs/LLEGIU-ME.pdf`. Run **`moodle-01`**, excepte **PR1 docent, PR4 docent i bonus docent: `moodle-02`**. Cada job reté fonts, preview, informes, logs i `receipt.json`; les versions anteriors es conserven intactes.

| Font relativa a `practiques/` | Pàgines | SHA-256 de la font | SHA-256 del PDF |
| --- | ---: | --- | --- |
| `pr1-project-setup/ca/alumnat/LLEGIU-ME.md` | 7 | `14d08c9bea28fa913143ca39ffbad97d31ebe3da7496b1826704fadb7ea8a367` | `02c34c6321e3b80e6024f76347e4044f50f819f7b69e5ad3ea6af4c32b7cb951` |
| `pr1-project-setup/ca/docent/LLEGIU-ME.md` | 8 | `d727442b9ebc353f3e879f9910f1ed6cdf4e889195907c5b1215aa33fed82d08` | `6d1f55d4327e61e3ca186c5f4f58a3db998f5d81d37078c44d941595a5af9586` |
| `pr2-digitalitzacio/ca/alumnat/LLEGIU-ME.md` | 6 | `df3e6b5d8bc9ba3bebfaa257735c099e93ad5393e422c5978c2bf59d3c2ac157` | `e134a103e4229c95cabeb278ae64cfc3a0a90aba807e6e95ee277673d20c9ac9` |
| `pr2-digitalitzacio/ca/docent/LLEGIU-ME.md` | 6 | `5fa7a1b04c6a76d94c44cc0c3cc4ace3615097cffa7d5d38b349c6afbb99fa2e` | `2bbd8d3bc8a3194dd880ed724240cc213563f4848fb97e75b08dc1fdc8ce6031` |
| `pr3-consultes/ca/alumnat/LLEGIU-ME.md` | 7 | `9cfd0c0ee6cb90e89f63d95fbda5b9f8ea52e3538693c9490dc5809811b0cf9e` | `ad624cf7379ebd4894e3689bfcef90ca3954e4e4349edd674a7484d4a1192034` |
| `pr3-consultes/ca/docent/LLEGIU-ME.md` | 8 | `8b0bd408d0a2727d190a3f0dde689a1fb7468cbc048a69cb14921ab6300d0f28` | `3b0be4dfdbfce3cc4768e55c89ab87db1f419d0dd4f620ed919dfd256f022c6d` |
| `pr4-geoprocessament/ca/alumnat/LLEGIU-ME.md` | 7 | `8ab3bb42c62bda9470020ab3c7da63dd3907b2f2677321da6fa4a1162aa89b03` | `2a8600d729ca2414b57af82abadfe4c69605f83a4567621ba2fd19ec306edac8` |
| `pr4-geoprocessament/ca/docent/LLEGIU-ME.md` | 7 | `c6fa623fe12d3405441efa7ea6c37771a8827859401d89e74970e320dc5d4d78` | `7a689cb36ba80fff18165c6a0e677658a7cb66e02f3a630a1fa8ba98bf350abf` |
| `pr4-tessellacions-reus/ca/alumnat/LLEGIU-ME.md` | 6 | `815492b3caed2461bb453ab104d7e4c5c79fdb6b38905a1b793de4c85834dc9e` | `14de3e9e8d31d17be938333d08a199b85e39779b9dd99ab258506a4f666b0581` |
| `pr4-tessellacions-reus/ca/docent/LLEGIU-ME.md` | 7 | `e7d83dc302b82d8b397d73d8ca9e5456bb562aafffa1251c0832fe58642273ce` | `8c365a9fab09864e5760b5e0bc8d85fa22f83673aeab9d7560b5228989bf45b9` |
| `pr5-raster/ca/alumnat/LLEGIU-ME.md` | 7 | `788ea9b2a9bba42b9b73c2b7ab42e64a18bfe0e326c253b8cda9158fb653bd48` | `f38438a82bbe6490837f3094525f9d39fdf01256c23ec000f076137db292834c` |
| `pr5-raster/ca/docent/LLEGIU-ME.md` | 7 | `d96debabb9ffcde15e75b312761f131ef5d200259e92d648a5bcf9e4f443d35f` | `063108da628d76af2b1add39c6ad7786781115777151c1ecd4682fa94bffa62e` |
| `pr6-sintesi/ca/alumnat/LLEGIU-ME.md` | 6 | `3b866d4e066c30b691ee027431239aa9221cb01978bda3055bec3849cc9021b5` | `654763122c090aa0d4da72561e3e9cd461825807e09eb79f198eb4e2e2cd0e73` |
| `pr6-sintesi/ca/docent/LLEGIU-ME.md` | 7 | `5f9b1e8915a137f245345b828643fc4a01eeef326269403d91f55ee2b86d4b8a` | `627d3fb97d30eae7c3f30bf98eaadfc21b8fdfa0e64e487cc6b0d5d22f18226d` |
| `bonus-pyqgis-sql/ca/alumnat/LLEGIU-ME.md` | 5 | `17d18ffd9ab15f472f2d34cb5f3ef19fe58a963b8733e04a1b72db88caa5a55b` | `dc9fc2503f5b0a95d0e847a66c893d3dc864bc3274e576b2b658d7d144914588` |
| `bonus-pyqgis-sql/ca/docent/LLEGIU-ME.md` | 5 | `bafcb861751cf0530c7e32c9d824d7b70aaeb900c765c693b3128d31621a989f` | `f4b0099e5d15d05a23cad77cba23bf88d70a8e71925e57a62e227eb3bfe34954` |

Les setze fonts finals passen `prose_check`, amb cobertura explícita, català, cap omissió, finding ni avís. S’han obert i llegit els setze PDF i revisat les portades, taules, expressions i seccions noves. La revisió ha corregit una taula de durades partida a PR1 docent, un títol aïllat a PR4 docent i una referència sola a l’última pàgina del bonus docent. Els tres primers jobs es retenen; les correccions provenen del Markdown, no de sortides editades.

Una comprovació independent de lectura ha contrastat els 16 hashes PDF amb els retornats pel productor, cada artefacte dels rebuts i els snapshots amb les fonts actuals. També comprova recompte de pàgines, A4 horitzontal, marca ESBORRANY, presència de les seccions docents i text dins dels límits de pàgina. Els logs finals no tenen `Overfull`, caràcters absents ni referències indefinides. Es mantenen dos `Underfull` menors a Reus alumnat i PR5 alumnat, i els avisos de plantilla TU/captions. El primer intent de comprovació textual no normalitzava Unicode; s’ha corregit el lector de prova, sense alterar els PDF.

### Execució i comprovacions de l’entorn

Les construccions utilitzen `manual_practice_pdf_build` per MCP públic, serialment, amb Web 0.7.2 i el mateix worker PDF fixat; totes retornen `ok: true` i `publishes: false`. Les tres sessions de renderització són:

| Lot | Sessió | Contenidor exacte |
| --- | --- | --- |
| Vuit guies docents | `326d740963ad42e3a077f098618d50e6` | `4a40effbf8d6b956bd2076923af552bb9e3e6423c16163e39c30b9026e55a142` |
| Vuit lectures d’alumnat | `b4d91544000b434d963ff1679ab1da36` | `7c97381cbc03caf95a846dcbe05773d17f131e4c3b68ad06566e9ba07a11e0b9` |
| Tres correccions de paginació | `fe57e82e4b934b8fabcb3bda4706e49a` | `1caf99666699c9b30f63224f2805d28ae68972df6840a903f85f0fe4eed34645` |

La consulta nativa `session-status`, amb IDs exactes contrastats als esdeveniments Docker, retorna `stopped` i `resources_released: true` per a aquestes tres sessions i les sis de descoberta, context, política i comprovacions. Els jobs romanen retinguts. Un primer intent de renderitzar les correccions amb els arguments del client puntual mal ordenats es va aturar al parser abans d’obrir sessió; l’execució posterior és la de la taula.

`site_check` retorna `ok: true`, amb els avisos preexistents de llegibilitat de figures i prosa del manual. Sessió `e62921bb753a43c8a74b524a821edb10`, contenidor `9f5098b393eee632c2674c6f96a9c96f77b942dfb3c14c41b5b145274e8fba3e`, aturada i alliberada. `site_doctor` manté les divergències dels pins/scaffold 0.7.1 respecte del runtime 0.7.2; no s’han migrat. La comprovació privada de lectures no es presenta com un nou build web del manual.

El preflight de continuació ha informat `dirty-checkout` pels canvis propis ja reservats. `_config.yml` conserva `26c5b2947af97a0eeef000d1cc2ee8ed34e8673e67a4a49ae4c084c02d4de342`; `opencode.json`, `6729127ba04083f690d8e42f2458ee4ea87f0c8abe34cd9e03e255693f4b79b0`. La branca continua sent `content/28-practiques-municipals`; només el JSON d’edició r1 històric està indexat.

### Simplificació de la retenció a Git

Les 33 exclusions d’inputs individuals s’han substituït per tres carpetes: `practiques/tig-buffer-municipal-500m/inputs/`, `practiques/pr1-project-setup/inputs/` i `practiques/recorregut-municipal/inputs/`. Es mantenen els roots de dades de `.unaltraweb/source-checks.json`. `git check-ignore` confirma la cobertura d’inputs i artefactes i deixa visibles Markdown, Python, SQL, JSON d’autoria i `.model3`. No hi ha inputs indexats ni inputs nous visibles fora de la ignoració.

Les reserves exactes i els hashes continuen als plans i manifests; el patró d’ignoració és independent d’aquella reserva. No s’ha esborrat ni traslladat cap dada, job o edició. Els vuit casos GIS i les seves limitacions continuen sent els documentats a continuació. L’autor encara ha de revisar els textos i seleccionar l’edició; no s’ha fet commit, push, publicació ni pujada a Moodle.

## Bundles GIS vigents i lectures antecedents · `2026-10-r3`

L’autor ha demanat revisar el conjunt complet i ha acceptat explícitament la reserva de **16 fonts i 29 inputs**: [registre de reserva](https://github.com/geourv/tig/issues/28#issuecomment-6175858065). L’índex vigent és `practiques/README.md`; les fonts de càlcul i reproducció són a `practiques/recorregut-municipal/`.

Aquella preparació reunia **16 lectures, 89 pàgines i 8 bundles docents**, amb originals, fonts de càlcul, projectes externs/incrustats, mapes, captures i proves. Les lectures r3 queden com a antecedent; els vuit bundles continuen vigents. No s’ha seleccionat cap hash com a aprovació de l’autor ni s’ha creat una nova edició de distribució. L’alumnat descarrega i prepara les dades; aquests paquets són casos docents de revisió i possibles exemples resolts.

### Bundles vigents i selecció docent comprovada

Els paths següents són relatius a `sandbox/practiques/`. Els fitxers i bytes de la selecció inclouen projecte resolt, mapa, font/llicència i originals pertinents; no són la mida de tota la carpeta privada d’evidència.

| Cas | Bundle | Controls | Fitxers seleccionats | Bytes seleccionats |
| --- | --- | ---: | ---: | ---: |
| PR1 | `pr1-project-setup/run-cnig-01/bundle.json` | 20 | 11 | 259.684.581 |
| PR2 sintètica | `pr2-digitalitzacio/run-cnig-01/bundle.json` | 27 | 12 | 258.330.688 |
| PR3 | `pr3-consultes/run-cnig-02/bundle.json` | 46 | 13 | 482.222.627 |
| PR4 | `pr4-geoprocessament/run-cnig-03/bundle.json` | 71 | 13 | 483.267.771 |
| Reus | `pr4-tessellacions-reus/run-cnig-04/bundle.json` | 31 | 8 | 330.408.127 |
| PR5 | `pr5-raster/run-cnig-02/bundle.json` | 125 | 31 | 492.021.108 |
| PR6 | `pr6-sintesi/run-cnig-01/bundle.json` | 127 | 28 | 489.243.338 |
| Bonus | `bonus-pyqgis-sql/run-cnig-02/bundle.json` | 144 | 31 | 489.305.824 |

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

Els vuit casos s’han executat amb `practice-run`, QGIS 3.44.11 i el productor 0.6.0 fixats. La comprovació pública final `practice-check` ha verificat **8/8 arbres complets** amb els hashes rebuts i les seleccions docents. Les reobertures natives de cada execució inclouen els dos projectes externs i els incrustats, amb només les dependències locals i xarxa desactivada. S’han llegit els vuit mapes PDF; la revisió ha corregit la mida dels portals de PR3, l’ordre de dibuix de PR4 i la clau de colors de Reus.

Les arrels seleccionades són `resolved-project`, `map-pdf`, `font-licence` i els IDs d’originals i fonts pertinents disponibles al cas. S’ha comprovat positivament el transport de `limits-original`, els originals CartoCiudad/transport/MDT i els inputs `roi-model`, `bonus-code`, `bonus-sql` i `postgis-source`. El model extern i el codi són **inputs d’autoria retinguts i seleccionables**, sense fer-los passar per formats de `NativeData` que no els corresponen. Això no acredita un model incrustat al projecte ni una execució PostGIS.

La cadena de dades utilitza les fites numèriques identificades a cada request. Els primers runs vàlids de PR3 i PR4 continuen com a inputs immutables; les revisions cartogràfiques posteriors conserven les mateixes dades analítiques. Els bundles retenen el seu propi snapshot de `compute.py`, de manera que una reproducció exacta parteix del `rebuild.json` del candidat, no d’una font canònica que s’hagi ampliat després.

### Lectures r3 conservades i hashes

Jobs sota `sandbox/practiques/<slug>/`, amb patró `lectura-2026-10-r3-ca-<destinatari>-<run>/`. El PDF és `outputs/LLEGIU-ME.pdf`; cada job conserva preview, fonts, logs i rebut. Run `conjunta-01`, excepte PR2 docent i les dues lectures PR4, que utilitzen **`conjunta-02`** després de corregir desbordaments de noms llargs. PR6 docent també utilitza **`conjunta-02`**, amb la correspondència explícita entre els IDs interns del model i els noms del guió.

| Font relativa a `practiques/` | Pàgines | SHA-256 de la font | SHA-256 del PDF |
| --- | ---: | --- | --- |
| `pr1-project-setup/ca/alumnat/LLEGIU-ME.md` | 7 | `4ed378156e3768ac46ec1e7cb039476875d1353753467a011077c4a14d305340` | `7fc02da6b2a463278d5fe18e6dada44401d65b0be01d79a226d388dfae39917d` |
| `pr1-project-setup/ca/docent/LLEGIU-ME.md` | 7 | `e62d48c59d816e5c28e9dc9e0aefd15e52c8c9e3434f17146269e814bf92096d` | `d984de497394720bce7fd240796b4859e05c3bd0b590ea3175578e2d951057c1` |
| `pr2-digitalitzacio/ca/alumnat/LLEGIU-ME.md` | 5 | `8c82080ac80870d0ab16e0aae21229f6d8a19528eedd51c5a3fc4bcb6ab84432` | `54b1f0f60f3d2175ece2cd105c84daaf1914c8922713f6b063f3f415d1d23596` |
| `pr2-digitalitzacio/ca/docent/LLEGIU-ME.md` | 4 | `c12ba502ede0b8f55196874c35915f17fd868eb941af7e432973105ab0066aaa` | `cdcee0b7371457a27bd6edf4ef5c1b625802341b4278c953466d45a7526f9c78` |
| `pr3-consultes/ca/alumnat/LLEGIU-ME.md` | 6 | `93174edf4d3951f2f65cfe96cf9de02ed45cc339d051fbb19eaf1a4819526e7f` | `f18826ca2b1ef66a029ee777abadfe6e4cea0b4264b4d2e91087416ae76437bd` |
| `pr3-consultes/ca/docent/LLEGIU-ME.md` | 6 | `cf4fd6cb2c8e8f2426372dcf17634c39a82ff11e2ab5b0a71f9e6bf5d08db3d1` | `206e45124ed6d90706aa23b9d3b2077743d29202ca295b69ba99ee983791c737` |
| `pr4-geoprocessament/ca/alumnat/LLEGIU-ME.md` | 6 | `adc3ded658f4f981bc58d0a44223fa9ddc48178371408b0eaa2f7f58151185f3` | `a326d3ad9ec13173fece1d350ae624e7ea26724395eebbe76edd6d60abcb6474` |
| `pr4-geoprocessament/ca/docent/LLEGIU-ME.md` | 6 | `b0a786ef3a1d93326f6d1b3790f8eb9a3b90a10a8d5f8bcc71c17a1e63cb7f39` | `4f2dc6efa57f060b76e2a094fbacc7c867ce39664065124c936b5713c6dcf2e0` |
| `pr4-tessellacions-reus/ca/alumnat/LLEGIU-ME.md` | 5 | `a0d32ab5253ece631f663a87917b82be955ef9e3f07c1ac1f0c5289c51ba964e` | `6ffccc42463677b29bf84b9ce1142f13920f9c8eaf177ff2c9b8ce23c0440487` |
| `pr4-tessellacions-reus/ca/docent/LLEGIU-ME.md` | 5 | `d76f9351dee71ed8f700f7d7c00e2c2f64e8a467d62fee112012d91df37e22ee` | `110053182f610652cf02d8c4dc112a43e5b49d0dc95bfb947cb7ad0dafbd1bde` |
| `pr5-raster/ca/alumnat/LLEGIU-ME.md` | 7 | `14cbd6daf9ea8693e505fc514e5df8c9a99c04aa43db60ad7d71a0dbf4a64ac2` | `5421ae582e27853d62641ac93aae0a38b88452266e133faf7429edd94447daf5` |
| `pr5-raster/ca/docent/LLEGIU-ME.md` | 6 | `b114176ab756af6a3bbfc7cc4f944b83f1ce1de1d198d4e7a4fed20df2ff8225` | `251ac954f4152c87df7bf5969aba649d4b7fcd23ddc9307069b1d6c8e3ab5f24` |
| `pr6-sintesi/ca/alumnat/LLEGIU-ME.md` | 5 | `e2e597b947f89b5166f0dce1ea35469f4ef1a29292b6957200c5aa4515b72ec2` | `4c80c379a7ae07034c43030dc7becc80d6b3a23d8399f774cf6ff3df6bee2c6b` |
| `pr6-sintesi/ca/docent/LLEGIU-ME.md` | 5 | `8f688dea7b70010377eba35c68ed550e597f33f66256b1aef5e8291332dc8fe2` | `3c6e83ad2f4d1273f830c6a5512e6fa1768672313148fc918afa67696b51afb3` |
| `bonus-pyqgis-sql/ca/alumnat/LLEGIU-ME.md` | 5 | `a0d91994f2e31c1f088c719681180fd44e49aef3aedf485dbc31e1d21737f076` | `1b999e9e9d26b2e249ef1f4dc4f32a0944cd10731946cb3f6e3a16246e03a7bd` |
| `bonus-pyqgis-sql/ca/docent/LLEGIU-ME.md` | 4 | `528372168acc6245e17eb257c74abc7686bc57e3a8899aa5b9909b9ac221c20d` | `5e1eb6fa8b285f2d1d9a2b3c176078fd7898cc46cb5a82252232805fa4b8711a` |

Les setze fonts finals passen `prose_check` per selecció explícita, sense omissions, findings ni avisos. S’han obert i llegit els setze PDF vigents, inclosos codis, taules, fórmules, numeració i portades. Els tres `Overfull` inicials s’han corregit a les fonts; els candidats vigents no presenten desbordaments, caràcters absents ni referències indefinides. Es conserven dos avisos `Underfull` menors, a Reus alumnat i PR5 alumnat, i els avisos de la plantilla sobre codificació/captions no utilitzats. Els bytes dels PDF concorden amb els hashes retornats pel productor.

La sessió MCP Web del lot conjunt és `fcd6a3caeb27ef2b7b73cf7de67e1a28`, contenidor `f458c9a2d47b8a6429694fde219726732f0ce4b8f7da18e8fc4854b28d03afe5`. La correcció tipogràfica utilitza `d4161c6cdd38f96ce1b20071a49dc2bd`, contenidor `ee9585a7eecbf3682059e5a7aeae263236d473c64abacf81c81b4ed36c9cb98e`. `session-status` retorna `stopped` i `resources_released: true` per a totes dues, amb els jobs conservats. El runtime Web, el worker PDF i el verificador són els mateixos pins ja documentats. El canal integrat havia respost a les consultes inicials, però es va tornar a tancar; les construccions s’han fet amb sessions MCP reals del llançador públic.

La precisió de PR6 docent es renderitza a la sessió `705f5970cf5fc8e53f7776d453a9f424`, contenidor `9a28005eb1c56a205cbcb8f81d2b2f01dbc523ebfe454f23b7a15bc52d2fed5f`, també aturada amb recursos alliberats. El seu rebut és `1383eb6ebeb09b99207b9a6f8915811c06876286e78d55a580d7a937eca513e9`.

Al tancament, `_config.yml` conserva `26c5b2947af97a0eeef000d1cc2ee8ed34e8673e67a4a49ae4c084c02d4de342`. S’ha observat un canvi extern a `opencode.json`, fora dels fitxers editats per aquesta preparació: SHA-256 actual `6729127ba04083f690d8e42f2458ee4ea87f0c8abe34cd9e03e255693f4b79b0`, deployment `290fdcccfa368782d68b2714de5950e318bfd71b0e51dc3dd7b05cbe4759c372`. Les quatre connexions continuen vinculades explícitament a TIG. Es conserva aquesta configuració de sessió; el hash anterior dels registres històrics no s’atribueix a l’estat actual.

### Incidències i abast

Es conserven els jobs refusats PR4 `practice-13e85a744b53488dae2dfdfed5ed3f6f`, PR5 `practice-5b50a5376799464cbf0a7edb0ce71327`, Reus `practice-d43b40cd9ef043deb5658ca01819755a` i bonus `practice-0b14e618629d4ab288aaa990be11dc46`. Les causes i correccions són al README del recorregut: arrodoniment de superposicions lineals, condicionament angular float32, idempotència del renderitzador categòric i conversió de tuples SQLite a atributs PyQGIS. També es mantenen els runs previs vàlids que es van revisar cartogràficament.

El conjunt declara explícitament els límits de les composicions natives, la naturalesa sintètica de PR2, el model extern sense acreditació d’incrustació, PostGIS sense execució i les fonts cadastral/inundabilitat encara no incorporades. Són candidats per a la revisió conjunta demanada, no una aprovació editorial ni un lliurament Moodle. Només el JSON r1 antic continua indexat; no s’ha fet commit ni push.

## Criteri actual de preparació i distribució

L’autor ha precisat que l’alumnat obté les dades originals del CNIG i les prepara, amb instruccions als PDF. A PR1 crea el projecte i resol el municipi propi amb almenys una composició cartogràfica editable i exportada a PDF. El paquet preparat es destina al professorat i ha de conservar originals, preparacions identificades, projecte resolt, mapa i controls. El cas resolt de Vila-seca es pot compartir amb l’alumnat com a exemple explícit del resultat esperat.

La nova preparació deixa de preveure un ZIP inicial d’alumnat com a entrada ordinària. Les dues fonts PR1 s’han reescrit amb descàrrega pròpia, CNIG/PNOA, reprojecció i composició obligatòria. El registre històric següent conserva els textos seleccionats aleshores i els seus artefactes; els hashes antics no aproven les lectures actuals.

La reserva conjunta posterior ha permès construir els vuit casos CNIG i comprovar la selecció dels originals. La composició cartogràfica completa i les altres limitacions es mantenen explícites a l’índex vigent. La selecció de textos i una nova configuració d’edició distribuïble es decidiran després de la revisió conjunta.

## Antecedent PR1 · lectures CNIG `2026-10-r2`

**Estat: PDF de revisió, sense nova edició de dades.** Les fonts expliquen com cada estudiant descarrega el ZIP del CNIG, conserva els components i les metadades, inspecciona EPSG:4258, connecta PNOA i exporta el seu municipi a EPSG:25831. La composició és obligatòria i es comprova al PDF i a les dues representacions desades del projecte. El suport docent inclou originals i cas resolt; aquest últim es pot compartir explícitament com a exemple.

Jobs vigents sota `sandbox/practiques/pr1-project-setup/`:

- Alumnat: `lectura-2026-10-r2-ca-alumnat-cnig-autonomia-02/`.
- Docent: `lectura-2026-10-r2-ca-docent-cnig-autonomia-03/`.

Cada job conserva el PDF a `outputs/LLEGIU-ME.pdf`, preview, snapshots, logs i `receipt.json`. Tots dos PDF tenen **7 pàgines**, són A4 horitzontals amb la plantilla compartida i mantenen ESBORRANY. `manual_practice_pdf_build` retorna `ok: true` i `publishes: false`.

| Destinatari | SHA-256 de la font actual | SHA-256 del PDF retornat pel productor |
| --- | --- | --- |
| Alumnat | `4ed378156e3768ac46ec1e7cb039476875d1353753467a011077c4a14d305340` | `30cc93f7b9a30037347577922b50f759bef8c7e20725b96f455af56f91c0db21` |
| Docent | `e62d48c59d816e5c28e9dc9e0aefd15e52c8c9e3434f17146269e814bf92096d` | `50f9df82b029d678191fad96ee14ed777c74ed986999ed01d33f68f6cf66ccda` |

Rebuts: alumnat `87b3938b409af38e9b791db3de67b929b6682f366fdb586ec6807b4d93d1509d`; docent `61eeb4fd50e24936260adc598a472bf825aca815102493cd5ceab341df77aba5`. Els bytes dels PDF s’han contrastat amb els hashes retornats. Aquests valors identifiquen els candidats per revisar; **no són una selecció ni una aprovació de l’autor**.

`prose_check` cobreix les dues lectures per selecció explícita, català, cap omissió, finding, error ni avís. S’han obert els PDF i revisat el text de totes les pàgines, les portades, les taules, les rutes, els codis i la numeració. La primera renderització es conserva: la revisió va motivar integrar el nom del Shapefile en prosa i introduir els tres estats de la demostració per evitar un títol aïllat. La guia docent final descriu la selecció per `CODNUT2` i `ES51` en prosa, sense presentar una abreviació com a expressió executable. Els logs finals no tenen `Overfull`, `Underfull`, errors ni referències indefinides; conserven avisos de codificació TU i de captions no utilitzats.

### Disponibilitat Web comprovada

El 14 d’octubre de 2026, el llançador públic `unaltraweb-mcp-docker` ha respost a `check` amb **0.7.2** i ha superat `smoke`. El canal Web no figura en la descoberta de recursos d’aquesta conversa, però una connexió MCP efímera al `serve` públic ha inicialitzat correctament, ha llistat eines i ha respost a `runtime_identity`, `site_context`, `site_doctor`, `language_policy`, capacitats i polítiques editorials.

El binding observat és `/home/benizar/git/tig`, perfil `unaltremanual`, llengua `ca`; controlador `sha256:576dcd772f2c345fa2021745f975f8392568d8d2783f7a66ba41a3521b3bd546`, versió carregada 0.7.2, revisió `sha256:3c83ed6071e2fedcf75c2d5cc6b428292c703ef5da2717d23072d90c192a93d2`. Worker PDF i verificador QGIS seleccionats: `matched`. El doctor conserva els diagnòstics preexistents dels pins/scaffold 0.7.1; no s’ha migrat el consumidor ni s’ha executat un nou build públic del lloc.

La construcció s’ha fet amb crides MCP reals a `manual_practice_pdf_build`, serials, amb imatges preparades i xarxa desactivada. El client utilitza la biblioteca MCP disponible a l’entorn QGIS per connectar-se al llançador Web; no importa una implementació Web privada ni modifica cap instal·lació. La venv lleugera Web no inclou aquesta biblioteca de client. No s’han llegit els helpers instal·lats del llançador després de la denegació d’accés.

La inspecció pública de les sessions de renderització `155b68f6e77e12091b69db0772f46f95`, `9f4598a13df89651586da4a1b75c86d9` i `4245470e55aeb12d70b8ec2c4021a8d6`, amb els seus IDs exactes de contenidor, retorna `state: stopped`, `resources_released: true`, sense recursos ni xarxes retinguts. Els jobs PDF continuen conservats. La configuració persistent manté els hashes previs i només el JSON r1 antic continua indexat.

## PR1 · `2026-10-review-r1`

**Estat: edició superada; no és la base docent de TIG.** L’autor ha aclarit que les pràctiques es basen en CNIG i que l’ICGC només havia estat una via puntual i opcional d’accés a recursos WFS. La preparació d’aquesta edició sobre municipis i ortofoto ICGC va ser una interpretació incorrecta de l’encàrrec. També queda superat el model de distribució d’un projecte inicial preparat a l’alumnat. La validació tècnica següent continua sent evidència del que es va construir, però no n’acredita l’adequació docent. Es prepara una edició nova CNIG i es preserven intactes aquests fitxers, rebuts i proves.

Unaltraweb 0.7.2 va produir el PDF independent i el ZIP de cada destinatari amb la plantilla compartida A4 horitzontal. Els PDF conserven la marca ESBORRANY.

Directori d’edició: `dist/practiques/pr1-project-setup/2026-10-review-r1/ca/`.

| Destinatari | Producte | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| Alumnat | `pr1-project-setup-2026-10-review-r1-ca.pdf` | 2.068.586 | `877e503a11f182a474d23770b858f635b3efecab2d364b14337c144f568efbc7` |
| Alumnat | `pr1-project-setup-2026-10-review-r1-ca.zip` | 24.087.430 | `914935f4c1c5a594a70299a775bf39460bb674060aedf1b27d120de2f8e1a8ab` |
| Docent | `pr1-project-setup-docent-2026-10-review-r1-ca.pdf` | 4.093.359 | `013752f831f4392c24928d8707ab873106418f312b8ff8c9f22250ada3158375` |
| Docent | `pr1-project-setup-docent-2026-10-review-r1-ca.zip` | 43.543.645 | `944c5eda43711edaee916beeab5a8622d9202fe7e17531f5a5d5dd96f12252e9` |

Els dos PDF, de 7 i 9 pàgines, coincideixen byte per byte amb els previews seleccionats per l’autor. Cada ZIP conté el mateix PDF com a `LLEGIU-ME.pdf`; els rebuts externs no s’insereixen al paquet docent o d’alumnat. `edition.json` té SHA-256 `7b60ceb91fd9d8d117f7389f1d016840ae7e38f0c941193229ca55f3d514270d`.

### Contingut

- **Alumnat:** set fitxers GIS/recursos més la lectura PDF, vuit membres en total. Catàleg de 947 municipis ICGC, taula de procedència, projecte extern `initial.qgz` i projecte incrustat `inicial`, ortofoto local de context, font i llicència, captura inicial. El GeoPackage inicial no conté les capes municipals resoltes ni la composició docent.
- **Docent:** deu fitxers GIS/recursos més la lectura PDF, onze membres en total. Inclou l’estat inicial i el GeoPackage resolt amb el catàleg físic, `municipi_treball`, `municipi_cnig`, procedència i projectes `pr1`/`comparacio`; projecte extern homònim, captura resolta i PDF de la base de composició.

La base cartogràfica `Base municipal` és editable i té mapes a 1:60.000 i 1:400.000, amb text de fonts. La llegenda nativa i l’escala gràfica es completen a QGIS; el productor 0.6.0 encara no verifica aquests tipus d’item. El context d’ortofoto és un extracte local, no cobertura de tot Catalunya ni producte analític a 25 cm. El WMS s’ensenya separadament i no és dependència d’obertura dels paquets.

### Fonts i selecció confirmada

Configuració d’autoria: `practiques/pr1-project-setup/edition-2026-10-review-r1.json`. L’autor ha confirmat aquestes dues fonts exactes per a l’edició local de revisió:

- Alumnat: `078d84585c127ae8862e209abacb56667628408b97ea78e0b63f1f28dd0996ec`.
- Docent: `a52fb84d19ed036edac9e5077827c02da6e9ebe320461267a4557d0659b0b11f`.

El camp contractual `approved_sha256` vincula aquesta selecció; no s’ha canviat `content_status: draft` ni s’ha concedit aprovació de publicació. Només la configuració d’edició s’ha indexat a Git, segons l’autorització, sense commit.

Productor: `unaltracaptura-qgis` 0.6.0, activitat PR1 0.1.1. Bundle: `sandbox/practiques/pr1-project-setup/run-02/bundle.json`, SHA-256 `e0d3b9d3a591b0566fdd6cef3afbc65cdc91856f8c89cf92017f3ac6d9e321dc`. Job: `sandbox/qgis-practice-jobs/practice-eeaa699be9bb44deb029cfc921c8cc98`.

El model executa quatre exportacions natives i 35 controls sobre les dades persistides. Es comproven els 947 IDs, atributs i geometries, validesa, identitat i geometria de la selecció, la còpia CNIG, el ràster, la font/llicència i la conservació dels inputs. Les reobertures del productor observen també projectes incrustats, temes i marcs de composició.

### Prova sobre els ZIP finals

Evidència create-only: `sandbox/practiques/pr1-project-setup/zip-review-01/`.

1. La comprovació usa els hashes de ZIP/PDF retornats pel compositor, no un hash recalculat per acceptar una modificació posterior.
2. La selecció i la closure provenen de `practice-check`, la interfície pública del productor. Es verifica que el ZIP contingui exactament aquella closure i `LLEGIU-ME.pdf`, amb paths únics, fitxers regulars, mides i hashes correctes.
3. Es conserva l’extracció exacta a `alumnat/package/` i `docent/package/`. Les fonts/control del productor no són membres d’aquests ZIP.
4. El verificador requereix el segell complet. Es prepara un receptor privat amb l’evidència no seleccionada, però **tots els fitxers GIS seleccionats provenen dels bytes del ZIP extret**. El receptor no és el paquet que es distribueix.
5. `practice-reopen` reobre el projecte inicial amb la seva closure de quatre fitxers i els dos projectes docents amb la closure GIS corresponent. El motor rep el paquet seleccionat, sense muntar el run privat com a font alternativa.

Les dues proves retornen `ok: true`, `network: none` i `container_absence_verified: true`. La prova d’alumnat observa 947 municipis, l’ortofoto RGB de 1.600 × 1.200 píxels i el projecte incrustat `inicial`. La docent reobre també `pr1` i `comparacio`, amb els dos límits d’una entitat i el catàleg de 947, a més de les representacions externes.

| Evidència | SHA-256 |
| --- | --- |
| `zip-review-01/summary.json` | `491bd7b25e60803e3e2db98d59c11190303cd430878f9fbd1c440f8e6f26d415` |
| `zip-review-01/alumnat/native-reopen.json` | `b37a39d3234da3d0f5477c55b0740f03855a90638be44526885ba0014e32dc30` |
| `zip-review-01/docent/native-reopen.json` | `dd522f5222f19ea20a2091f950c017fbde01642a4591821a8f1aa660a3a3c82d` |

El script puntual d’acceptació es conserva a `zip-review-01/verification-script.py`, SHA-256 `38d323117c23b890cd11e0f751bf578608aa7083c5f1e7da6411c3ae3e3a835d`. Només comprova aquesta edició i crida el verificador/reobridor públics; no implementa un parser QGIS ni un empaquetador alternatiu.

### Retenció i límits

Els PDF previs, el primer job refusat per una aresta excessiva de dependència i el run segellat es conserven. Les fonts originals no s’han sobreescrit. Els artefactes de `dist/` i `sandbox/` continuen ignorats i exclosos de Jekyll; ignorar-los no n’autoritza la neteja.

Els quatre productes del directori d’edició identifiquen el resultat històric; les carpetes de proves són evidència separada. L’edició superada es conserva i no es proposa com a lliurament actual. El destí de retenció durable externa i la pujada a Moodle encara s’han d’acordar. Qualsevol nova edició es crearà en una revisió separada, sense sobreescriure `2026-10-review-r1`.

## Continuació

| Unitat | Pas següent de preparació |
| --- | --- |
| PR2 | Partir de la base PR1, preparar esquemes inicials i separar l’inventari observat dels casos sintètics; verificar herència i reobertura |
| PR3 | Reconstruir la base acumulativa amb PR2 i les fonts CNIG/Cadastre, amb seleccions i resultats per destinatari |
| PR4 | Executar buffers, superposicions, recompte de solapaments i ROI amb controls específics |
| Reus | Preparar generadors i entorn; executar Delaunay/Voronoi, revisar casos ambigus i contrast independent |
| PR5 | Preparar mosaics/retalls i la comparació de graelles; verificar els deu GeoTIFF i els projectes |
| PR6 i bonus | Construir i executar el model; provar el suport del productor per transportar models/codi abans de segellar edicions |

La taula anterior recull els objectius de preparació de la seqüència. La revisió conjunta descrita al començament ja disposa dels vuit casos executats i dels setze PDF harmonitzats. Els punts que continuen oberts es presenten a `practiques/README.md`; els plans detallats i la seva evolució es conserven a `sequencia-pr1-pr4.md` i `continuacio-tesselles-raster-models.md`.
