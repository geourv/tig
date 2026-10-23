# Revisió de ROI, geoprocessament i captures · TIG #34

## Validació per a publicació · 23/10/2026

El circuit públic del consumidor ha passat amb la imatge immutable de 0.7.1:
`make test MCP_IMAGE=ghcr.io/dosquartsdedocs/unaltraweb-mcp@sha256:6aa20cff86c3891a876e37ba0548fa36f3c5633c9f22ba672e9f50123d677cf6`.
Inclou preparació de PDF, `site-check-native`, build Jekyll i auditoria HTML.
El gate editorial sobre fonts i `_site` retorna `ok:true`, sense errors.

El manual aprovat té **325 pàgines**, 80.233.796 bytes, sense ESBORRANY,
SHA `eb174bd4b8e61d092d7dfceca3b0884ecf2dc3f8969052a03bbc047a63daf9af`.
La còpia completa dels set outputs queda retinguda a
`sandbox/practiques/pr4-geoprocessament/manual-2026-10-vector-r2-approved-20261023/`.
El PDF servit per HTTP concorda amb aquest hash. S'han revisat portada i
pàgines de figures, límits de text i marges del cos del capítol 6. Es conserva
l'observació menor de l'URL de bibliografia generada, dins de la pàgina.

La revisió Chrome comprova les 29 captures inserides en escriptori de 1440 px
i mòbil de 430 px, amb imatges carregades i sense desbordament horitzontal.
El preview etiquetat s'ha aturat després de la revisió. Les crides MCP de
preview havien expirat; la CLI pública del mateix runtime ha permès preparar
el preview i comprovar-lo des del host, sense alterar el motor.

L'auditoria confirma 121 paths de la reserva, 33 conjunts complets sense
anotacions omeses i tres originals intactes. Les quatre guies mantenen els
hashes aprovats per a revisió en draft; l'índex conserva 16 PDF/172 pàgines.
Els directoris privats i `opencode.json` no apareixen a `_site`.

Es documenten els avisos de transparència preexistents i el límit d'inspecció
global d'imatges; una imatge no inspeccionada no es declara opaca. El gate
editorial conserva l'avís preexistent «la la» del capítol 7, fora de la reserva,
i el fals positiu «de DE» de «Les nou interseccions de DE-9IM». Cap d'aquests
avisos constitueix un error bloquejant del circuit.

El control d'espais de les fonts passa. `git diff --cached --check` detecta
una línia buida amb dos espais en tretze SVG natius sense callouts; es conserven
els bytes del productor, sense retocar sortides gestionades. Aquesta observació
de format no modifica els píxels ni els controls de captura.

## Decisió de publicació de l'autor · 22/10/2026

L'autor ha demanat publicar el manual actual a GitHub Pages, com a `latest`,
ajornant les captures pendents. Ha confirmat «Sí, publicar l'estat actual»
amb aprovació del manual, dels avisos de figures coneguts i de commit, push,
PR, integració a `main` i desplegament. Els capítols 6 i 8 passen a `approved`;
les onze fonts públiques del manual estan aprovades.

Per a les quatre guies PR4/Reus ha triat «Conservar-les en esborrany»:
es versionen com a fonts de treball i els PDF locals mantenen ESBORRANY.
Es conserven l'índex local de 16 lectures/172 pàgines i els deu bundles verificats.

La [tasca #37](https://github.com/geourv/tig/issues/37) és la **primera tasca
de continguts després d'actualitzar unaltracaptura**: dues pàgines del mateix
atles, tessel·la activa i composició constant, exportació i revisió real de Reus.
El sondeig `qgis-c06-atlas-pagina` s'ha traslladat byte per byte a
`sandbox/practiques/pr4-tessellacions-reus/unpublished-atlas-probe-20261022/`;
la còpia de diagnòstic anterior també es conserva. No s'inclou als actius
publicables. La unitat actual de Git és de 121 paths de la reserva de #34.

La publicació utilitza el circuit normal Make/CI del consumidor i el workflow
reutilitzable sobre el SHA de `main` revisat. El defecte de snapshot de
`build_site` continua registrat a Web #114 i no es declara reparat. La migració
#36 i la coherència de pins de Web #115 continuen com a seguiment independent.
El reinici dels MCP i d'OpenCode es farà després del retorn de publicació.

## Estat comprovat el 22/10/2026

La reparació del compositor té [acceptació local al proveïdor #27](https://github.com/dosquartsdedocs/unaltracaptura-qgis/issues/27#issuecomment-6329069144),
però continua com a `0.7.0.dev0` sense commit ni release. El runtime connectat
és QGIS 0.6.1 amb Web 0.7.3; encara no inclou aquella reparació ni el perfil v3.
La integració/captura real a TIG queda pendent de publicació i adopció de família.

L'autor ha acceptat preparar la migració del web: [pla #36](https://github.com/geourv/tig/issues/36).
El dry-run està bloquejat pels dos conflictes locals i s'ha documentat una
incoherència addicional entre la gem proposada i el SHA de core. No s'han
aplicat canvis als controls gestionats. `site_check` passa; `build_site` i
`manual_release_status(latest)` continuen bloquejats pel socket privat exclòs.

L'auditoria de materials locals confirma **16 PDF / 172 pàgines i 10 bundles**,
amb fonts i segells concordants; 12 lectures aprovades i 4 en esborrany.
L'índex vigent és `practiques/README.md` i l'evidència és a
`sandbox/practiques/materials-readiness-20261022-01.json`, SHA
`02194000a197f06bd4fff2dcbc1e2dc7d79a846e28ffb4f60c79d23d4e038270`.
El detall dels punts de retorn i les aprovacions pendents és a `lliuraments.md`.
Els bloquejos Web tenen ara informes al proveïdor:
[socket privat #114](https://github.com/dosquartsdedocs/unaltraweb/issues/114)
i [tuple gem/core #115](https://github.com/dosquartsdedocs/unaltraweb/issues/115).

## Reserva i antecedents

Reserva inicial exacta de 74 paths acceptada per l'autor a
[TIG #34](https://github.com/geourv/tig/issues/34), amb
[registre de l'acceptació](https://github.com/geourv/tig/issues/34#issuecomment-6277221637).
Branca `content/34-roi-cnig-captures`, base `124a51824860249fc24dcc29f5015c5c3dab4011`.
Un únic editor, al checkout principal; sense worktrees. L'ampliació de 50 paths
ha estat [acceptada explícitament](https://github.com/geourv/tig/issues/34#issuecomment-6300133559).
La reserva vigent cobreix **124 paths: 22 fonts/referències i 34 conjunts**
PNG/SVG/manifest, enumerats a la issue. La fita r2 utilitza 121 paths.
El sondeig posterior de `qgis-c06-atlas-pagina` ocupava els tres restants,
però s'ha retingut fora dels actius públics abans de preparar la publicació.
Els 33 conjunts inclosos són figures docents validades.

## Encàrrec de reparació del compositor · 21/10/2026

L'autor ha precisat que la captura ha de mostrar la tessel·la com a guia
d'una sèrie de mapes amb composició constant. Després del diagnòstic ha
autoritzat preparar el prompt per reparar `unaltracaptura-qgis`.
L'[encàrrec complet](../../practiques/pr4-tessellacions-reus/cas/prompt.md#encàrrec-de-reparació-per-a-unaltracaptura-qgis)
és per a una sessió al checkout del proveïdor: finestres independents,
selecció exacta d'accions, popups, mida llegible, navegació d'atles i
exportació nativa de sèrie, amb proves positives i negatives.

S'ha obert el compositor real amb consultes discriminants de menú/acció.
La causa restant és comprovable al codi: QGIS crea el compositor sense pare
i el capturador cerca accions/panells sota la finestra principal. El sondeig
final retorna `ok:true`, però només mostra una finestra de 651×390 píxels
lògics i no compleix l'evidència docent demanada. No s'ha donat per acabada
la captura de la sèrie.

Evidència completa retinguda a
`sandbox/practiques/pr4-tessellacions-reus/atlas-probe-20261021-01/`.
La recepta activa s'ha restaurat a les deu captures Reus validades; les
23 ROI continuen correctes. L'auditoria confirma els 33 conjunts, totes
les anotacions, originals intactes i 124 paths dins de reserva. S'ha
actualitzat la nota de proveïdor `ead73d2cba6c4aa8b4381207fe8c6bc0` amb
aquest diagnòstic i la preferència de sèrie `2fbb05460c89404080b7653ba07f629f`.
La correcció del core i les captures definitives són el pas següent.

## Rebuig de r1 i nova revisió `2026-10-vector-r2`

La revisió r1 va ser **rebutjada editorialment** per l'autor el 20/10/2026.
Les proves tècniques descrites més avall són històriques i no constitueixen
aprovació docent. S'ha refet el capítol 6 i s'han adaptat després les quatre
guies PR4/Reus, totes en `draft`, amb aquest fil:

1. Envolupants del municipi i selector de tipus de la mateixa eina.
2. Distàncies, CRS, buffer i caixa ROI del buffer.
3. Preparació, selecció, superposicions, diferències i parts.
4. Punts derivats amb traça.
5. Malles regulars, Delaunay i llindars, Voronoi postal de Reus.
6. Cobertura regular i pràctica guiada d'atlas.

Les figures s'han integrat al concepte/pas corresponent. Els polígons de
context no tenyeixen el WMS i els callouts s'ancoren a caixes visibles.
L'auditoria ha detectat cinc captures amb textos llargs omesos pel renderer
tot i `warnings: []`; s'han escurçat a la font i regenerat. La comprovació
final de recepta contra manifest confirma **totes les anotacions previstes**.

### Noves fites científiques i captures

- ROI: `sandbox/practiques/pr4-geoprocessament/roi-run-20261020-04/bundle.json`,
  SHA `b17cbbbfb9a9e23eca45a1f9c86f80f590ed14a87df37aa6dd2c5bf3b70e431d`,
  **143 controls**, 34 capes; afegeix les quatre envolupants del terme sense
  canviar la ROI de continuïtat. [Fonts i reproducció](../../practiques/pr4-geoprocessament/roi/README.md).
- Reus: `sandbox/practiques/pr4-tessellacions-reus/tesselles-run-20261020-04/bundle.json`,
  SHA `be001fde84b38fe4315382e42e6fe23107713c9aaf3e3662bc8ed0cc1c2c4bb7`,
  **80 controls**. Generadors complets, malles 500/1.000 m, graf, llindars,
  Voronoi postal i atlas natiu. [Fonts i límits](../../practiques/pr4-tessellacions-reus/cas/README.md).
- **33 conjunts de captura**: 23 ROI i 10 Reus, PNG/SVG/manifest, WMS real,
  tres connexions GeoPackage, EPSG:25831, backend `offscreen`, sense avisos.
- Lot final ROI: instance `835c4f1f-8cf0-4983-9893-3899ed41e384`, session
  `16c6267c-bdaf-4318-b3e5-4a48fede3098`.
- Lot final Reus: instance `ed8dadda-2fe2-4562-98e7-895e25b3da47`, session
  `2e0af235-bc15-4355-8634-f48d54878106`.
- Tots dos lifecycle finals: zero workers actius, `ready_to_detach: true`;
  clients tancats normalment. Els tres originals conserven els hashes.
- Auditoria read-only de 121 paths dins la reserva, zero staging, `.gitignore`
  aliè de quatre línies preservat i `git diff --check` correcte.

### Evidència d'atlas disponible i pendent

El layout, la cobertura de **82 cel·les completes d'1 km**, l'ordre, els noms
i els footprints del mapa de 200×200 mm a 1:5.000 estan comprovats per iteració
nativa. La figura `atlas-configuracio` mostra `native:atlaslayouttopdf` amb
paràmetres, no un compositor o PDF simulats.

L'accés al compositor amb el capturador 0.6.0 continua sense acreditar:
la coincidència parcial de `Dissenys` selecciona abans `Gestor de dissenys`;
les altres rutes provades no obren `QgsLayoutDesignerDialog`. L'exportador
natiu v2 observat és de layout estàtic, sense iteració. No hi ha PDF d'atlas
multipàgina segellat. Limitació registrada al proveïdor, candidate/open:
`ead73d2cba6c4aa8b4381207fe8c6bc0`. La guia explica navegació i exportació
amb controls explícits, sense atribuir-los una execució no feta.

### Revisió local de PDF i web

Les quatre lectures `2026-10-vector-r2` sumen **91 pàgines**: PR4 alumnat 27,
PR4 docent 23, Reus alumnat 23 i Reus docent 18. Els paths i hashes són a
`lliuraments.md` i els enllaços a `practiques/README.md`. Fonts, snapshots,
artefactes i rebuts coincideixen; A4 horitzontal i ESBORRANY. S'ha corregit
un desbordament inline i dos finals de referències; els logs finals no tenen
`Overfull`, caràcters absents ni referències indefinides.

El manual català té **327 pàgines**, 80.234.190 bytes, SHA
`86992d06368bb12be8c74a068c5892eeabd6ff66b5886f81a67f3db53cb9285b`;
rebut de preview `6da6ad367b29c6b5af98afe6580f73be7fed4f9d28b44477c94b4926ee93283e`.
Les tres passades del manual es retenen com a snapshots separats; les
correccions provenen de la font Markdown. El text no surt de les pàgines;
el control addicional del bloc de text del capítol deixa només una observació
de l'URL de la bibliografia generada, documentada a l'inventari.

`prose_check` passa el capítol 6 i les quatre guies sense findings; el capítol
8 conserva diagnòstics informatius de longitud. `site_check` passa. La prova
del build per snapshot continua fallant pel mateix socket privat, sense
alterar Unaltramesa. La comprovació acotada d'imatges acredita opacitat de
29 PNG; els sis SVG conceptuals anteriors mantenen els seus avisos.

El navegador ha comprovat els quatre blocs visuals de la revisió a 1440 px
(scroll 1425) i 430 px (scroll 430), sense desbordament de la pàgina. La
revisió inclou envolupants, arestes/llindar, codis postals i exportació d'atlas.

El primer preview viu actualitzava HTML però conservava un PDF anterior a
`_site/`. S'ha aturat exclusivament amb `preview_stop` de la seva sessió
`ca1aecde947b474a8116d1e018824b93` i s'ha reobert al mateix port. El nou
preview, sessió `fda5c20dc7ce4c8daa08d4c7ba3547f0`, contenidor
`0a23e86075a0ea220313055521ea71d0d00407bb0d3c66a3f8e67b4a80d5305a`,
serveix el capítol i el PDF final amb HTTP 200 i hash concordant. Es deixa
actiu per a la revisió de l'autor a `http://127.0.0.1:32777/tig/ca/`.
La comprovació desktop/mòbil s'ha repetit sobre aquesta sessió final.

El seguiment del proveïdor conserva tres notes obertes addicionals:
`ead73d2cba6c4aa8b4381207fe8c6bc0` (compositor/exportació d'atlas),
`3f00ce82d3e14785be95adaaac2fa929` (omissió silenciosa de callouts) i
`e14875777f3c41848c5349d1e328fc33` (PDF obsolet al preview viu).
El bloqueig de `build_site` pel socket continua a
`a0a6b3dd81ca46fa94242a8116a055c5`. La idea del projecte sobre atlas i
agrupacions manté estat `planned`, amb la implementació parcial i les proves
registrades; no es dona per resolta ni aprovada docentment.

## Antecedent retingut: revisió r1

## Criteris de l'autor

CNIG com a base; ROI no orientada sobre el buffer municipal de 500 m, desada
com `roi`; preparació de punts, línies i polígons; diferències, parts i punts
derivats abans de les tessel·lacions. Les captures importants es reutilitzen
entre capítol i pràctica.

L'autor va aturar la primera passada perquè faltaven les connexions i el
context. La correcció exigeix l'Explorador amb els GeoPackage del projecte,
CartoCiudad i viari, i el WMS IGN/PNOA real sota els vectors. La represa va ser
autoritzada explícitament: «OK, torna a provar amb aquestes puntualitzacions».

## Execució científica

Bundle `sandbox/practiques/pr4-geoprocessament/roi-run-20261019-03/bundle.json`,
segell `3960e5e074f50d6c40bf2d7c00305b96dc1fc480691b35200b76d59c9375601f`.
Productor 0.6.0, QGIS 3.44.11,
`sha256:1003721d96abe9607d8337b36851f9b29f84c2f8f92b377d1a73ff03c9d15cd2`.
131 controls i reobertura nativa dels projectes. Els inputs originals i els
runs 01/02 es conserven. El README del cas n'explica reproducció i límits.

## Captures

Les 20 captures s'han renderitzat amb el MCP, backend `offscreen`, locale
`ca_ES`, tres connexions GeoPackage i provider `wms` real sobre
`https://www.ign.es/wms-inspire/pnoa-ma?`, capa `OI.OrthoimageCoverage`.
La composició es fa amb el callback públic d'autoria; no s'ha copiat cap
motor al consumidor ni s'ha modificat el projecte científic segellat.

El primer lot complet va superar el termini del client integrat; el worker
va acabar i es van conservar els 20 conjunts. La revisió va detectar una
anotació amb selector ambigu al menú del filtre: s'ha eliminat la fletxa i
s'ha fixat l'acció real `Filtre`, ressaltada pel menú natiu.

El lot final ha retornat `ok: true`, 20/20 renders i cap avís mitjançant un
client MCP puntual del llançador públic, amb termini de client de 900 s.
Sessió `e508cdce-d6bb-44fe-a64a-5b00af057e2c`, instance
`5e58e6b7-59bc-458b-b8af-b37c382d77cc`; controller
`sha256:1fe4a54a42cbac4a6eea596be73425985ab3bca5f28f5871d2fa66d7c0a05f8b`.
La consulta lifecycle final informa cap operació ni worker actiu i
`ready_to_detach: true`. El client ha tancat la sessió normalment.

S'han inspeccionat la vista general, el menú, el filtre corregit, els diàlegs
de selecció/intersecció/buffer/parts/extrems i els mapes de retalls, mar,
peces i punts. Els diàlegs són configuracions natives; els càlculs i els
resultats persistits tenen les proves pròpies del bundle.

## Edició i revisió

Capítols 6 i 8 i lectures PR4 tornen a `draft`. El capítol 8 harmonitza el
model de dos nodes, buffer i caixa, amb 8 segments per quadrant; els deu
GeoTIFF heretats i el contracte de fitxers es mantenen. Els resultats 2026-10-v1
continuen retinguts com a primera versió aprovada. Aquesta revisió requereix
revisió humana de web i PDF abans d'aprovació, integració o publicació.

El preflight inicial era elegible a la branca acceptada. A la represa informa
`dirty-checkout` pels canvis de treball; també s'ha observat un diff aliè de
quatre línies a `.gitignore`, relatiu a Unaltramesa. No forma part de la reserva
de #34 i es conserva sense reinterpretar-ne l'autoria.

### Resultats de la revisió local

- `prose_check` cobreix els dos capítols i les dues lectures. Les lectures no
  tenen findings ni avisos; els capítols conserven diagnòstics informatius de
  longitud de frases i taules.
- L'auditoria dels 20 conjunts comprova PNG, SVG amb fons incrustat, manifests,
  backend, CRS, les tres connexions i el WMS visible i vàlid. Els tres originals
  conserven els hashes; `practice-check` torna a validar el segell i els 131 controls.
- Els PDF PR4 `2026-10-roi-r1` tenen 21 pàgines d'alumnat i 18 de docent, amb
  hashes a `lliuraments.md`. Fonts, snapshots i tots els artefactes dels rebuts
  coincideixen. Els logs finals no tenen desbordaments ni referències indefinides.
- El manual PDF local té 329 pàgines i 61.112.633 bytes; SHA-256
  `a4f513ebf22dc4fe4e95fc3cf3b990347a7ddadbae2e494eb7d64da1b98f9c50`.
  S'han corregit al Markdown dues cadenes llargues que desbordaven el capítol 6.
  La comprovació final no detecta paraules fora dels límits de pàgina. S'han
  revisat visualment el cas, els mapes, els diàlegs i la continuïtat del model.
- `manual_pdf_preview_prepare` retorna `publishes: false`; rebut
  `8827b3d7288d1230b426a0567f9bf7511657e13167d9284e9337e222941a532a`.
  El selector tècnic és `latest`, però el document és un esborrany local.
- `site_check` passa abans del build. La comprovació acotada d'imatges observa
  opacitat de les 14 captures noves del capítol; els avisos restants corresponen
  a figures conceptuals prèvies.
- El preview natiu ha construït i servit el capítol actualitzat i el PDF amb
  HTTP 200. La sessió final és `4e30adf06b27413e9a0eff75a50846b7`. La revisió
  de navegador verifica 14 figures, amplada 1440/scroll 1425 a escriptori i
  amplada 430/scroll 430 al mòbil. La prova mòbil carrega una pestanya nova
  amb el viewport fixat abans de navegar i tanca el menú si està desplegat;
  no confon l'estat heretat d'una finestra d'escriptori amb la vista mòbil inicial.
  `preview_stop` confirma l'aturada del contenidor propi.
- Els roots privats de pràctiques, execució, context i Unaltramesa estan absents
  del lloc generat.

### Bloqueig pendent del build per snapshot

`build_site` retorna `Could not snapshot safe manual build inputs: Release trees
cannot contain special files: .unaltramesa/project/operator.sock`. El socket
continua existint, encara que `_config.yml` exclou explícitament l'arbre privat.
No s'ha tocat el servei ni les seves dades. El preview etiquetat i el PDF han
permès completar la revisió local, però això no converteix aquell build fallit
en una comprovació superada.

Incidència registrada al backlog del proveïdor `unaltraweb`, nota
`a0a6b3dd81ca46fa94242a8116a055c5`, candidate/open. La correcció correspon al
core. Aquesta sessió utilitza l'override immutable Web 0.7.2
`sha256:576dcd772f2c345fa2021745f975f8392568d8d2783f7a66ba41a3521b3bd546`;
la migració dels pins/scaffold del consumidor continua ajornada segons la
decisió anterior de l'autor.
