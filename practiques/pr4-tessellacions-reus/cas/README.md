# Reus: malles, graf de proximitat, Voronoi postal i atlas

Fonts d'autoria de [TIG #34](https://github.com/geourv/tig/issues/34), dins
de l'ampliació exacta de 50 paths acceptada per l'autor. El productor públic
és `unaltracaptura-qgis 0.6.0`, perfil `qgis-practice-v2`, QGIS 3.44.11,
worker `sha256:1003721d96abe9607d8337b36851f9b29f84c2f8f92b377d1a73ff03c9d15cd2`.
El consumidor defineix models, controls i composició. El productor executa,
inspecciona, reobre i segella; no s'ha afegit un motor GUI/exportador alternatiu.

## Fita científica retinguda

- Activitat 0.1.1, **80 controls**.
- Bundle: `sandbox/practiques/pr4-tessellacions-reus/tesselles-run-20261020-04/bundle.json`.
- SHA-256: `be001fde84b38fe4315382e42e6fe23107713c9aaf3e3662bc8ed0cc1c2c4bb7`.
- Request SHA-256: `b7c768bf953ccc4359713fa9b95c20beaee166aff5d7547d6b1250d42600fadf`.
- Job: `sandbox/qgis-practice-jobs/practice-b9eb392bfb4e47c399cb0993f39acc87`.
- Inicial: `payload/data/inicial.gpkg`, incrustat `inicial`, i `payload/projects/inicial.qgz`.
- Resolt: `payload/data/reus-tesselles.gpkg`, incrustat `reus`, i `payload/projects/reus-tesselles.qgz`.
- Fonts exactes executades a `payload/sources/`; reconstrucció a `rebuild.json`.

El domini és la bbox CNIG de Reus, marge mínim 1.500 m i extrems arrodonits
exteriorment a 1.000 m, en EPSG:25831. S'hi conserven tots els portals, no
només els atribuïts municipalment a Reus. Coincidències per coordenada exacta,
ID estable derivat de la coordenada binària i correspondència amb les files
originals; `cod_postal` és textual, amb categories explícites per manca/conflicte.

| Resultat | Valor |
| --- | ---: |
| Portals | 35.190 |
| Generadors | 34.614 |
| Triangles | 69.195 |
| Arestes úniques | 103.808 |
| Cel·les Voronoi retallades | 17.318 |
| Categories postals | 15 |
| Cel·les d'atlas | 82 |

| Llindar | Arestes | Components | Aïllats |
| --- | ---: | ---: | ---: |
| 25 m | 53.237 | 6.810 | 5.074 |
| 50 m | 78.132 | 3.098 | 2.355 |
| 100 m | 92.649 | 1.323 | 916 |

## Reproducció nova

`activity.json` fixa els dos originals i els seus hashes. Es reutilitzen
CartoCiudad Tarragona 04/2026 i els límits CNIG de juliol de 2026 retinguts a
`practiques/recorregut-municipal/inputs/`. Preparació i output han de ser nous:

```bash
python3 -B practiques/pr4-tessellacions-reus/cas/compute.py prepare sandbox/practiques/pr4-tessellacions-reus/tesselles-inputs-repro-01
unaltracaptura-qgis practice-run --workspace /home/benizar/git/tig --request sandbox/practiques/pr4-tessellacions-reus/tesselles-inputs-repro-01/activity.json --output sandbox/practiques/pr4-tessellacions-reus/tesselles-run-repro-01
```

La preparació comprova i copia originals, request i codi; no executa GIS al
host. Cal usar la instal·lació pública fixada i el worker ja preparat, sense
pull implícit. Per reproduir la fita exacta es parteix del snapshot del bundle,
no del callback de composició online ampliat posteriorment.

## Controls i límits científics

- Hashes d'originals, validesa, CRS, identitats i preservació d'entrades.
- Quadrícules 500/1.000 m: cobertura, àrees, recompte d'ubicacions i suma de portals.
- Arestes: parelles úniques, IDs, longituds i correspondència amb els triangles.
- Components: contrast independent amb totes les parelles dins del radi,
  cercades amb `cKDTree`, i components de SciPy; inclou aïllats.
- QGIS DBSCAN amb `MIN_SIZE=1`, `EPS=50`, DBSCAN* desactivat coincideix amb
  els components de 50 m. No és una equivalència amb altres paràmetres DBSCAN.
- Voronoi i dissolució: cobertura municipal i interiors disjunts. No s'ha
  executat aquí una validació postal independent ni una nova prova de marge ampli.
- Atlas: 82 cel·les completes d'1 km, ordre, noms únics, iteració nativa,
  marc de 200×200 mm i footprints coincidents amb cada cel·la a 1:5.000.

Els hexàgons es proposen com a comparació docent, sense atribuir-los resultats
calculats en aquest bundle. El cas antic `run-cnig-04`, amb 31 controls,
manté la partició de validació i el 83,94% com a experiment separat; no és
la precisió del nou model complet de 15 categories.

## Captures i límit actual d'atlas

`project.yml` i `captures.yml` defineixen català, backend `offscreen`, les
tres connexions GeoPackage i WMS IGN/PNOA real. `compose_online` prepara
contorns sense farciment i estils de dades, sense alterar el bundle offline.
La recepta té **10 captures**; `tig-c06-reus-tesselles.atlas-configuracio`
executa la seqüència completa. Cada conjunt conserva PNG, SVG amb fons
original incrustat i manifest. Les anotacions es contrasten amb la recepta:
`warnings: []` no garanteix que no s'hagi omès un text massa llarg.

`atlas-configuracio` mostra el diàleg real `native:atlaslayouttopdf`, amb el
layout, cobertura i ordre emplenats. **No és una captura del compositor ni
prova d'exportació.** `exports: []` declara que no hi ha PDF d'atlas segellat.
El sondeig `qgis-c06-atlas-pagina` no és apte com a figura docent. Els tres
fitxers s'han retingut fora dels actius públics, byte per byte, a
`sandbox/practiques/pr4-tessellacions-reus/unpublished-atlas-probe-20261022/`.
La seqüència validada continua tenint deu captures. La figura definitiva es
completarà a [TIG #37](https://github.com/geourv/tig/issues/37), primera tasca
després de l'actualització del capturador, segons la decisió de l'autor.

Els primers sondeigs del compositor amb el productor 0.6.0 havien observat:

- `open_menu_path: [Projecte, Dissenys]` coincideix abans amb «Gestor de dissenys…».
  El codi públic `menu_action` usa la primera coincidència parcial bidireccional.
- `trigger_visible_menu_action` no troba el layout; `trigger_action` pel nom
  o per «tessel·les» no acredita l'obertura tot i no retornar avisos.
- `inspect_ui` no observa `QgsLayoutDesignerDialog`; el target estricte falla
  amb `selector did not match a visible widget`.
- L'exportador natiu v2 públic utilitza `exportToPdf` de layout estàtic, sense
  iteració atlas. QGIS disposa de l'algorisme d'atlas, però no s'ha substituït
  la mecànica compartida amb un exportador privat al consumidor.

Limitació del proveïdor registrada a gaContExt, candidate/open:
`ead73d2cba6c4aa8b4381207fe8c6bc0`. Cal una ruta pública comprovada d'obertura,
navegació i exportació abans de presentar aquestes evidències com a completes.
La guia desenvolupa els passos del compositor i el control del PDF esperat,
sense afirmar que una captura de paràmetres acrediti la seva execució.

### Sondeig i encàrrec de reparació del 21/10

L'autor demana que es vegi la tessel·la que guia una sèrie de mapes amb la
mateixa composició i ha autoritzat preparar un prompt per reparar el core.
L'[encàrrec complet](prompt.md#encàrrec-de-reparació-per-a-unaltracaptura-qgis)
inclou reproducció, causes comprovades, abast i proves d'acceptació.

S'ha aconseguit obrir `QgsLayoutDesignerDialog` discriminant el submenú
`Dissenys` i l'acció del layout respecte de l'acció contextual d'atles.
El bloqueig següent és de finestra: QGIS crea el compositor sense pare i
les accions/panells del capturador cerquen sota `iface().mainWindow()`.
La darrera captura mesura 651×390 píxels lògics i no acredita encara una
sèrie llegible. La ruta experimental s'ha retirada de la recepta docent.

El sondeig complet es reté a
`sandbox/practiques/pr4-tessellacions-reus/atlas-probe-20261021-01/`, incloent
recepta, config, PNG/SVG/manifest i sortida d'inspecció. Sessió
`22c94409-be4b-4a65-969a-fd4fd0f23734`, instance
`02cbf5ef-1ceb-4fd5-8fee-6c2e987055ed`; lifecycle final sense workers actius.
Els paths dels fitxers copiats corresponen al context original: la carpeta
és evidència de diagnòstic, no un bundle portable.

## Historial i retenció

La prova 01 va fallar `edge-lengths`: el provider de memòria exportava camps
double amb cinc decimals. S'ha declarat `double(24,10)`, mantenint el control
independent de distància. Els runs 02/03, amb 77/79 controls, es conserven;
03 afegeix ordre/footprints i 04 afegeix DBSCAN min1. Inputs, jobs, PDFs i
bundles ignorats es retenen. Les fonts de les guies estan en `draft` fins a
la revisió humana; aquesta fita no publica ni aprova continguts.
