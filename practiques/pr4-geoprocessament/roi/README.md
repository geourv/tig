# Cas docent de ROI CNIG

Fonts d'autoria de la revisió [TIG #34](https://github.com/geourv/tig/issues/34).
El càlcul utilitza el productor públic `unaltracaptura-qgis 0.6.0`, perfil
`qgis-practice-v2`, amb QGIS 3.44.11. La composició i els controls científics són
del consumidor; execució, inspecció nativa, reobertura i segell són del productor.

## Resultat retingut

- Bundle: `sandbox/practiques/pr4-geoprocessament/roi-run-20261020-04/bundle.json`.
- SHA-256: `b17cbbbfb9a9e23eca45a1f9c86f80f590ed14a87df37aa6dd2c5bf3b70e431d`.
- Activitat 0.2.0, 143 controls; 34 capes vectorials al GeoPackage resolt, procedència i resum de mesures.
- La fita afegeix `municipi_caixa`, `municipi_rectangle_orientat`, `municipi_cercle_minim` i `municipi_convexa`, sobre el terme original, amb `qgis:minimumboundinggeometry`. La ROI continua essent la caixa del buffer de 500 m; no se substitueix per una envolupant del municipi sense marge.
- Projectes externs `inicial.qgz` i `pr4-roi-exemple.qgz`; projectes incrustats `inicial` i `pr4_roi` als respectius GeoPackage.
- Les fonts exactes executades són al `payload/sources/` del bundle. La composició online ha evolucionat després al codi canònic; no es modifica el snapshot executat.

És un cas complementari de demostració. No substitueix les sis instantànies
de l'alumnat ni incorpora per si sol les capes heretades de PR1–PR3.

## Preparar i executar una reproducció nova

`activity.json` és el request d'autoria. `compute.py prepare` comprova els tres
originals declarats a `parameters.sources`, en reté còpies i copia el request i
el codi a un directori nou ignorat. Els paths d'entrada del request són relatius
a aquesta preparació. No s'executa directament contra una carpeta `inputs/`
inexistent al costat d'aquest README.

```bash
python3 -B practiques/pr4-geoprocessament/roi/compute.py prepare sandbox/practiques/pr4-geoprocessament/roi-inputs-repro-01
unaltracaptura-qgis practice-run --workspace /home/benizar/git/tig --request sandbox/practiques/pr4-geoprocessament/roi-inputs-repro-01/activity.json --output sandbox/practiques/pr4-geoprocessament/roi-run-repro-01
```

Cal emprar una instal·lació pública fixada i el motor ja preparat, sense pull
implícit. La destinació ha de ser nova. Una reproducció byte per byte de la fita
04 parteix del seu `rebuild.json` i de la seva font retinguda, no d'una còpia
canònica ampliada posteriorment.

## Captures amb context real

`project.yml` i `captures.yml` defineixen la sessió MCP: català, backend
`offscreen`, connexions GeoPackage explícites i xarxa per al WMS IGN/PNOA.
`compose_capture`, invocat a través del callback públic de composició, afegeix
els originals locals i una capa real amb provider `wms`, no una imatge local.
La recepta obre el projecte verificat sense desar un nou checkpoint offline.

Els paths `/workspace/` són els de la vinculació Docker del MCP al checkout
TIG seleccionat. Abans de renderitzar, `runtime_identity` ha de confirmar
aquesta vinculació, les imatges fixades i l'absència de drift. Les captures es
fan a través del MCP; no es reenvia la pantalla personal de l'autor.

La recepta conté 23 captures. `render_recipe` amb
`tig-c06-roi-cnig.punts-resultat` executa la seqüència completa. Cada sortida
conserva PNG anotat, SVG amb el fons original incrustat i manifest. Un timeout
del client no acredita una fallada del worker: primer s'observa el lifecycle
i els resultats; no s'inicia una execució duplicada sobre el mateix destí.

Els polígons de context no tenen farciment i els callouts utilitzen caixes
visibles. La comprovació compara les anotacions declarades amb les del
manifest: el productor pot ometre una etiqueta massa llarga sense avís.
S'han escurçat els textos afectats i regenerat les sortides des de la recepta.

## Controls i límits

Es comproven hashes, identitats, geometries completes dels candidats, CRS,
validesa, correspondència dels retalls, camps, àrees i longituds, diferències,
conservació de cobertura en separar parts i posicions dels punts derivats.
El control de distància del buffer és mostrejat; no es presenta com el
certificat continu del pilot anterior.

`terra_roi` és cobertura administrativa. `mar_complement` conserva els cinc
components de la diferència; `mar_context` en selecciona dos amb punts marins
de contrast del cas. Les peces entre buffers viaris no són illes urbanes
oficials. Els vèrtexs poden repetir coordenades i els centroides poden quedar
fora de la geometria.

La primera prova conserva la hipòtesi fallida de distància regular al job
`practice-3f4ae00f3b154aa58844eb0f9b644475`. La cota d'arcs parcials es documenta
a `practiques/tig-buffer-municipal-500m/geos-validation.md`. La fita 02 també
es reté: només seleccionava el component marí major. La fita 03 conserva els
dos components vinculats amb els punts marins de contrast, sense eliminar
el complement complet. Cap d'aquestes dades ni dels renders s'ha de netejar
pel fet d'estar ignorat a Git.

La revisió editorial r1 va ser rebutjada per ordre i inserció de captures.
La nova seqüència integra envolupants, distàncies, buffer i ROI abans de
seleccions, superposicions i punts. Els PDF i el bundle r1 es conserven com
a antecedents, sense atribuir-los aprovació docent.
