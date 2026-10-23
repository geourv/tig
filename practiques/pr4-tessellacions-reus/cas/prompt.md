# Fil docent de les tessel·lacions de Reus

Utilitzar els mateixos generadors CartoCiudad al llarg de malles regulars,
Delaunay i distàncies, Voronoi postal i atlas. Explicar cada concepte abans
de l'eina i relacionar-ne resultat, control i límits al mateix bloc.

Conservar originals, entorn municipal, coordenades reprojectades, identitats
i correspondència entre registres i ubicacions. Els codis postals són text;
les coincidències/conflictes no es resolen movent punts. El model complet
no es redueix silenciosament als blocs d'entrenament del cas antic.

Les malles fixen mida i origen, conserven cel·les buides i separen nombre de
generadors i nombre de portals. Les arestes de Delaunay conserven IDs i
longitud; no són totes les parelles. Els components per llindar mantenen
aïllats i expliquen cadena, sensibilitat i barreres. Voronoi i dissolució
produeixen una zonificació estimada, no fronteres oficials.

L'atlas utilitza quadrats complets d'1 km, ID estable i ordre explícit.
Relacionar el mapa de 200×200 mm amb l'escala 1:5.000, demostrar control
per atlas, navegar pàgines i comprovar l'exportació. Distingir configuració,
iteració científica, captura de compositor i PDF reobert. Si manca suport
del proveïdor, documentar-ho fora del text publicable i no simular una prova.

Les vistes generals mostren l'Explorador amb els GeoPackage del projecte,
CartoCiudad i viari, i WMS IGN/PNOA sota contorns sense farciment. Comparar
arestes i llindar amb el mateix enquadrament. Els punters s'ancoren a caixes
o cercles petits visibles sobre controls reals; textos breus i comprovació
que cap anotació prevista s'hagi omès. Reutilitzar les figures pertinents
al capítol i a les dues guies. Moodle selecciona els obligatoris i manté
70/20/10 sense doble recompte.

## Encàrrec de reparació per a unaltracaptura-qgis

**Destinació:** una sessió al checkout principal de
`dosquartsdedocs/unaltracaptura-qgis`. Aquest encàrrec repara el proveïdor;
la integració posterior de les captures al consumidor TIG és una altra fase.
L'autor ha demanat preparar aquest prompt expressament, després de precisar:
«cal ver alguna captura on es vegi que la tessela és la que guia la generació
de múltiples mapes amb la mateixa composició, una serie».

### Objectiu observable

Implementar una via pública, declarativa i reproduïble per obrir el compositor
QGIS, mostrar la cobertura i el mapa controlat per atles, previsualitzar una
entitat determinada i passar a una altra. Cal produir **dues captures reals
de la mateixa composició**, amb tessel·les diferents i enquadraments diferents,
però mateix format, marc de mapa, escala, llegenda/fonts i posició dels textos.
La relació «una entitat de cobertura → un mapa de la sèrie» ha de ser visible.

No basta un diàleg d'exportació, una captura del llenç principal ni el text
«82 pàgines». La prova ha de mostrar la finestra real del compositor i
l'estat natiu de l'atles. Completar també la via nativa d'exportació de la
sèrie, diferenciada del layout estàtic, amb un PDF reobert i comprovat.

### Contracte de treball

1. Llegir `AGENTS.md`, contribució i política de releases del proveïdor;
   verificar arrel, branca i preflight. Treballar en un sol checkout, sense
   worktrees ni edició simultània de TIG.
2. Consultar gaContExt per a `unaltracaptura-qgis`, especialment la nota oberta
   `ead73d2cba6c4aa8b4381207fe8c6bc0`, inclòs el feedback més recent. Les notes
   són context, no autorització d'operacions.
3. Identificar i reservar els paths exactes de la correcció i de les proves
   segons el contracte del repositori. Partir del codi vigent, preservant
   l'aïllament de pantalla de 0.6.1; no pedaçar una instal·lació ni una imatge.
4. Mantenir la vinculació per `MCP_CONSUMER_WORKSPACE`, els límits de recursos,
   el cicle de vida de sessió i els inputs de només lectura. Les proves no
   utilitzen ni interfereixen amb l'escriptori personal.
5. El renderer i l'actor GUI compartits continuen al proveïdor. No traslladar
   automatització Qt/PyQGIS al callback cartogràfic del consumidor, ni afegir
   macros o accions executables als projectes per esquivar aquesta mancança.

### Entorn i diagnòstic observats

El cas TIG usa MCP **0.6.0**, perfil `qgis-practice-v2`, QGIS **3.44.11** i
worker immutable:

`sha256:1003721d96abe9607d8337b36851f9b29f84c2f8f92b377d1a73ff03c9d15cd2`.

El controller 0.6.0 és
`sha256:1fe4a54a42cbac4a6eea596be73425985ab3bca5f28f5871d2fa66d7c0a05f8b`.
S'ha consultat la release pública **0.6.1** i el seu diff: incorpora pantalla
privada i comprovacions addicionals, però les funcions d'accions/panells
observades continuen cercant sota la finestra principal. Reconfirmar-ho al
codi vigent abans de desenvolupar.

Problemes concrets al codi públic `bridge/qgis_bridge.py`:

- `menu_action` retorna la primera coincidència de `ui_text_matches`, que
  permet inclusió bidireccional. `Projecte > Dissenys` selecciona abans
  «Gestor de dissenys…». S'ha obert el submenú amb la consulta discriminant
  `"Dissenys >"`; és un sondeig, no una API que es vulgui imposar al consumidor.
- `trigger_action` amb el nom del layout també pot trobar abans l'acció de
  capa «Set as Atlas Feature for …». Aquesta acció necessita una entitat:
  executar-ne el `QAction.trigger()` genèric no equival a obrir el compositor.
  `"Atlas de tessel·les de Reus >"`, després de poblar el menú, evita aquella
  coincidència en el sondeig.
- `find_action`, `show_panel`, `hide_panel` i `show_toolbar` cerquen sota
  `iface().mainWindow()`. **El compositor no n'és fill**: a QGIS 3.44.11,
  `QgisApp::openLayoutDesignerDialog` crea `QgsLayoutDesignerDialog(nullptr)`.
  Per això una finestra que es pot capturar no té necessàriament les seves
  accions accessibles als passos actuals.
- `mActionAtlasPreview`, `mActionAtlasSettings`, `mActionAtlasNext` i
  `mActionAtlasLast` existeixen al compositor, però `trigger_action` no les
  troba amb aquella cerca limitada. La pantalla completa del compositor
  també és inaccessible per aquesta ruta; no s'ha d'activar la de QGIS per
  error quan els noms de les accions coincideixen.
- La captura inicial del compositor arrossegava menús de la finestra
  principal: les superfícies retingudes a `MANAGED_MENUS` es componien sobre
  una altra finestra. `close_transients` els esborra, però el seu criteri
  de nom que conté `Dialog` també tanca el compositor, que és un `QMainWindow`.
- Els sondeigs amb els menús separats de les toolbuttons i reobertura han
  donat `ok:true`, però la finestra final era de **651×390 píxels lògics**,
  amb una pàgina minúscula i sense el panell de cobertura llegible. No són
  una solució docent ni una prova suficient de navegació.
- `practice/native_worker.py` exporta el layout estàtic amb
  `QgsLayoutExporter(layout).exportToPdf(...)`. No s'ha observat una declaració
  pública equivalent per a la iteració completa de l'atles. QGIS disposa de
  `native:atlaslayouttopdf`; l'existència de l'algorisme no acredita que el
  productor l'hagi executat o retingut com a sèrie.

### Correcció requerida

Escollir una ampliació petita que encaixi amb el disseny del proveïdor. Els
noms de passos següents són orientatius, no imposen una API nova concreta:

- Obertura d'un layout per nom/identitat inequívoca, amb postcondició de
  finestra visible i layout correcte.
- Àmbit explícit de finestra per resoldre accions, menús, panells, toolbars,
  elements i anotacions. Prioritzar object names i coincidències exactes;
  una ambigüitat ha de diagnosticar-se, no activar silenciosament el primer
  candidat. Preservar/documentar la compatibilitat de receptes anteriors.
- Mida de finestra o maximització determinista a la pantalla aïllada, amb
  dimensions efectives observades. Per a la demostració cal espai suficient
  perquè es llegeixin alhora pàgina, cobertura i controls.
- Mostrar el panell d'atles, seleccionar l'element de mapa i fer visible
  **Controlat per atles**, cobertura, escala fixa i nom de pàgina.
- Activar/desactivar preview i anar a una entitat per ID estable o a un
  índex de pàgina validat; navegar a següent/anterior/primera/última.
  Esperar la renderització nativa i observar l'entitat i l'enquadrament reals.
- Tancar només popups quan es demani això, sense destruir el compositor;
  limitar la composició de menús i anotacions a la finestra capturada.
  Un selector absent, ocult o fora de la regió capturada ha de fallar clarament.
- Exportació d'atles opt-in, amb la mecànica nativa de QGIS, sense convertir
  l'exportació estàtica existent en una sèrie de manera implícita. Retenir
  ordre, identitats, paràmetres, fitxer i proves dins del contracte natiu;
  mantenir compatibles els projectes i bundles anteriors.

### Proves d'acceptació

Preparar una fixture local sintètica amb almenys **tres quadrats adjacents**
identificats, geometries recognoscibles diferents en cada quadrat i un sol
layout. Les proves bàsiques han de funcionar sense WMS ni xarxa.

1. Obrir el layout per la via pública en una sessió aïllada. Comprovar que
   el target és `QgsLayoutDesignerDialog` i que la mida efectiva és adequada.
2. Capturar la primera pàgina amb cobertura i mapa controlat per atles
   visibles. Les anotacions són caixes/cercles sobre controls reals.
3. Canviar a la segona pàgina de **la mateixa instància/layout** i capturar-la.
   Canvien ID, número i extensió del mapa; es mantenen paper, geometria física
   del marc, escala, estils i posicions dels elements. Comprovar-ho amb estat
   natiu, no només amb diferències de píxels o amb un títol modificat.
4. Revisar PNG i SVG a mida final; cap menú aliè, cap etiqueta prevista omesa,
   cap panell fora de pantalla ni pàgina reduïda a una miniatura il·legible.
5. Exportar un PDF natiu de la fixture: tres pàgines, IDs/ordre correctes,
   extents diferents i composició constant. Reobrir-lo i comprovar-lo.
   Retenir també el projecte editable i verificar el bundle/selecció.
6. Provar layout inexistent, nom ambigu, element de mapa absent, cobertura
   buida/incorrecta i índex fora de rang. Cap cas ha de produir una captura
   aparentment correcta de la finestra principal o de la pàgina anterior.
7. Regressions: dues finestres amb noms d'acció repetits; `Dissenys` i
   `Gestor de dissenys`; acció d'atles amb i sense context d'entitat;
   `close_popups` preserva el compositor; canvi de finestra no reutilitza
   rectangles de menús. Passar les comprovacions exigides pel proveïdor.

### Cas real per a la integració posterior

El projecte TIG és `/home/benizar/git/tig`, branca `content/34-roi-cnig-captures`,
issue https://github.com/geourv/tig/issues/34. No modificar-lo des d'aquesta
sessió de core. Les dades reals serveixen com a referència, no com a dependència
obligatòria dels tests sintètics del proveïdor.

- Fonts d'autoria: `practiques/pr4-tessellacions-reus/cas/`.
- Bundle retingut: `sandbox/practiques/pr4-tessellacions-reus/tesselles-run-20261020-04/bundle.json`.
- SHA-256: `be001fde84b38fe4315382e42e6fe23107713c9aaf3e3662bc8ed0cc1c2c4bb7`.
- Projecte: `payload/projects/reus-tesselles.qgz`.
- Layout: **Atlas de tessel·les de Reus**.
- Cobertura: `cobertura_atlas`, 82 quadrats complets d'1 km; ID `id_cella`,
  ordre ascendent `pagina`, de nord a sud i d'oest a est.
- Mapa: `mapa_atlas`, 200×200 mm, escala fixa 1:5.000, EPSG:25831,
  rotació zero, dins d'A4 vertical. 200 mm × 5.000 = 1.000 m.
- El cas té 80 controls, inclosos ordre, noms únics i footprints de la
  iteració. Això no substitueix la prova de compositor ni del PDF final.
- Sondeig retingut: `sandbox/practiques/pr4-tessellacions-reus/atlas-probe-20261021-01/`:
  còpia de recepta/config, PNG, SVG, manifest i `ui-probe.txt`.
  Són còpies de diagnòstic amb paths del context original, no un bundle
  portable ni una recepta llesta per executar des de la carpeta copiada.

### Lliurament de la reparació

Retornar el canvi del proveïdor, les proves executades i les dues captures
revisades de la fixture; exemples de recepta pública per configuració,
canvi de pàgina i exportació; i els rebuts/identitats del runtime i dels
productes. Actualitzar el feedback de la nota amb l'evidència real, separant
allò resolt del pendent.

Indicar la release immutable necessària i la compatibilitat amb la família
MCP. Web 0.7.2 declara QGIS MCP 0.6.0 en el recorregut actual: no esquivar
aquesta dependència ni modificar pins de TIG des del core. Seguir les
autoritzacions de commit/PR/release del repositori; preparar el retorn perquè
la sessió TIG pugui integrar el proveïdor publicat i substituir el sondeig
per dues captures definitives, amb revisió humana de web i PDF.
