# PR1: inici d'un projecte municipal

Document d'autoria. El text del manual es desenvolupa als capítols 1–3; Moodle
conserva les condicions d'avaluació. Estat: revisió.

## Encàrrec i decisions editorials

L'enunciat aportat per l'autor demana un municipi escollit per l'estudiant,
un límit municipal seleccionat, exportat a un GeoPackage i carregat des d'aquest
contenidor, un projecte QGIS incrustat, una còpia externa `.qgz`, un WMS i uns
apunts breus en PDF amb explicacions i captures significatives. Els noms segueixen
la convenció `pr1-project-setup-cognom`; l'entrada incrustada s'anomena `pr1`.

Les ampliacions poden afegir fonts, simbologia, etiquetes, grups, mapes i
composicions. L'enunciat de Moodle distribueix la qualificació en 70% de requisits
imprescindibles, 20% d'ampliacions funcionals i 10% de documentació i organització.
Les ampliacions no substitueixen el nucli. Aquests percentatges no es traslladen
als capítols del manual.

El manual presentarà comprovacions, preguntes d'interpretació i una activitat
integradora. La comparació ICGC–CNIG és una ampliació resolta del mateix cas, no
un segon límit obligatori. Els apunts documenten decisions i resultats, amb
captures seleccionades; no són una transcripció de clics. La composició
`Recordatori` i els originals de classe continuen sota l'edició de l'autor.

## Entrades conservades

Les còpies d'entrada de `assets/projectes/vila-seca/pr1-aula/` són idèntiques als
fitxers aportats a `sandbox/`. El constructor d'inspecció rebutja qualsevol
modificació d'aquesta revisió; una versió nova s'ha de revisar explícitament.

| Fitxer | SHA-256 |
| --- | --- |
| `pr1-project-setup-zaragozi.gpkg` | `88075560914a0da195dab9540325a7390f49d6b6cdf237c72639e3271c0f7ad9` |
| `pr1-project-setup-zaragozi.qgz` | `7147be541f7da8f487ebb1e1d3ef3b9f1602f01a109f7c21e7468c161d4cc050` |

Són fonts documentals locals, excloses del lloc amb la resta de
`assets/projectes/vila-seca`. No són una nova solució generada ni un historial
d'execució. Les metadades dels projectes indiquen QGIS 3.40.10; la inspecció i les
captures es fan amb QGIS 3.44.11. Les dates internes de desament, 14 de setembre
de 2026, són diferents de la data d'adjunció de Moodle aportada per l'autor.

## Observacions comprovades

- El GeoPackage conté exactament l'entrada QGIS `pr1` i dues capes vectorials.
- `vilaseca_icgc_15000`: una entitat `MultiPolygon`, `EPSG:25831`,
  `CODIMUNI = '431711'`, `NOMMUNI = 'Vila-seca'`. El nom de taula és literal;
  el producte és a escala 1:5.000, no 1:15.000.
- `vilaseca_cnig`: una entitat `MultiPolygon`, `EPSG:25831`,
  `NATCODE = '34094343171'`, `NAMEUNIT = 'Vila-seca'`. No atribuir-hi l'esquema
  `nationalCode`/`text` de la distribució GML usada per un altre exemple.
- Les geometries no són buides i superen la validació GEOS. `integrity_check`
  retorna `ok`; `foreign_key_check` no retorna incidències.
- Les definicions de capes del projecte extern i de l'incrustat coincideixen.
  Tots dos apunten a `./pr1-project-setup-zaragozi.gpkg` per als vectors locals.
- Hi ha dues capes WMS, `ortofoto_25cm_color_2025` i
  `ortofoto_25cm_color_2024`, del servei Ortofoto Territorial de l'ICGC.
- La capa general `Municipis 1:5.000` usa OGR i `/vsicurl/https://…fgb`:
  és un FlatGeobuf remot. La descripció interna que parla de WFS no coincideix
  amb aquesta font desada; la documentació explica la discrepància.
- Totes dues representacions conserven la composició `Recordatori`.
- En muntar només les dues entrades en una ruta diferent i sense xarxa,
  QGIS obre tots dos projectes i resol les dues capes locals. Les tres fonts
  remotes no estan disponibles en aquesta prova; això no diagnostica una
  avaria dels servidors ni acredita el seu funcionament en línia.

Els camps i geometries de sortida no demostren per si sols la distribució,
la versió ni el CRS d'origen del CNIG. La reconstrucció del procediment ha de
distingir aquesta limitació de les propietats efectivament observades.

### Mesures complementàries d'autoria

Àrees planes calculades sobre les geometries en `EPSG:25831`, sense configuració
el·lipsoidal de QGIS: ICGC, 21.655.798,7752 m²; CNIG, 21.704.046,0248 m².
La diferència simètrica té 115.625,2926 m². Són controls d'aquesta revisió,
no llindars d'exactitud ni resultats exigibles a altres municipis. No equivalen
necessàriament al càlcul `$area` d'un projecte amb el·lipsoide configurat.

## Reproducció de la inspecció

Retenció inicial exclusiva, amb comprovació de hash i sense sobreescriptura:

```bash
python3 context/practiques/inspect_pr1_project.py --retain \
  --report tmp/pr1-project-setup/archive-inspection.json
```

La comprovació geomètrica i d'obertura usa la imatge ja preparada, sense xarxa.
El directori de les còpies s'ha de muntar també en una ruta nova per comprovar
que les fonts locals es resolen des d'aquesta ubicació:

```bash
docker run --rm --pull=never --network=none \
  --user "$(id -u):$(id -g)" \
  -e HOME=/tmp -e QT_QPA_PLATFORM=offscreen -e OGR_SQLITE_JOURNAL=OFF \
  -e GDAL_HTTP_TIMEOUT=5 -e GDAL_HTTP_CONNECTTIMEOUT=3 \
  --mount "type=bind,source=$PWD,target=/workspace,readonly" \
  --mount "type=bind,source=$PWD/assets/projectes/vila-seca/pr1-aula,target=/transport/pr1,readonly" \
  --entrypoint /usr/bin/python3 \
  qgis/qgis@sha256:e016b5296b99f0b07760b883888bc4ba615c0099feae9432374b4c83e8e073cc \
  /workspace/context/practiques/inspect_pr1_project.py \
  --input-root /transport/pr1 --qgis
```

## Intenció de les captures

La revisió de l'autor exigeix una seqüència guiada per a estudiants que tot
just comencen amb QGIS. La interfície ha de ser real i en català. Els controls
han d'estar emplenats amb les dades del cas i cada pas ha de tenir un resultat
visible. Les captures han de conservar prou context per orientar-se.

### Petició al director de la seqüència

Cal documentar la preparació d'un projecte de Vila-seca amb QGIS:

1. Mostrar el municipi ampliat al llenç sobre l'Ortofoto Territorial 2025
   carregada com a WMS. Identificar el WMS i el vector al panell de capes.
2. Mostrar Vila-seca seleccionat dins d'una capa que contingui també altres
   municipis. Obrir el menú contextual amb el botó dret i el submenú
   `Exporta > Desa les entitats seleccionades com a...`.
3. Mostrar el diàleg natiu d'exportació amb GeoPackage com a format, el fitxer
   de la pràctica com a destinació, un nom de capa ASCII amb guions baixos,
   només l'entitat seleccionada i `EPSG:25831` com a CRS de sortida.
4. Mostrar el resultat exportat, carregat des del GeoPackage, ampliat sobre
   el WMS. Comprovar la font i el recompte, distingint-lo de la capa general.
5. Mostrar com es crea o s'obre una connexió GeoPackage a l'Explorador i com
   s'escull el fitxer de la pràctica.
6. Mostrar el menú `Projecte > Desa a > GeoPackage` i el diàleg natiu en què
   s'escullen el contenidor i el nom de projecte `pr1`.
7. Mostrar l'acció d'actualitzar la connexió de l'Explorador després de crear
   capes o projectes. Després s'ha de veure el projecte `pr1` dins de la
   connexió, distingit de les capes vectorials.
8. Mostrar un segon projecte, `comparacio`, dins del mateix GeoPackage.
   Cal explicar que els projectes tenen noms diferents i poden compartir
   les mateixes dades; `pr1` identifica el projecte de treball del recorregut.

La demostració es reconstrueix en fitxers de treball separats a partir de fonts
verificades. Els originals de classe i la composició `Recordatori` queden com
a entrades conservades. No es dibuixen diàlegs ni es presenten camps o menús
inventats com si fossin captures. La preparació per PyQGIS i els passos de GUI
realment executats s'han d'identificar a l'evidència.

Els inventaris de fitxers i carpetes del text publicable es representaran amb
PlantUML i diavisuals. La documentació ha d'explicar la diferència entre el
fitxer GeoPackage, les capes i els projectes que conté, la connexió que el
mostra a l'Explorador i el projecte que està obert a QGIS.

## Seqüència nativa retinguda

La guia actual dels capítols 2–3 prové de `tmp/pr1-guided/run10/tig`.
`prepare_pr1_guided.py` prepara nou municipis de l'entorn a partir del
FlatGeobuf ICGC fixat; `capture_pr1_guided.py` executa els diàlegs natius.
El paquet és `assets/projectes/vila-seca/pr1-guia/` i conté l'extracte d'entrada,
el GeoPackage resultant, el `.qgz`, `provenance.json` i `validation.json`.

Les deu captures són, en ordre: `wms-overview`, `selected-municipality`,
`export-menu`, `export-dialog`, `wms-result`, `connect-dialog`,
`save-project-menu`, `save-project-dialog`, `refresh-connection` i
`projects-in-browser`. El prefix és `assets/img/qgis/qgis-pr1-` i cadascuna
conserva PNG i manifest. Els menús s'han retallat des de la GUI per millorar-ne
la lectura. No són les tres captures de la recepta MCP anterior,
`recipes/qgis-pr1-project-setup.yml`, que continua retinguda com a antecedent.

La selecció inicial es prepara amb PyQGIS. L'exportació, la connexió,
el desament de `pr1` i `comparacio` i el refresc de l'Explorador s'executen
als controls natius. Després de reobrir `pr1`, PyQGIS escriu la còpia externa;
no s'atribueix aquesta darrera operació a un clic de GUI. Les dues vistes
incrustades llegeixen la mateixa taula `municipi_vilaseca`.

`verify` va comprovar una entitat en EPSG:25831, el mateix codi i geometria
de l'entrada, els dos projectes i la reobertura externa. La signatura WKB és
`5465f4f9f08264b1c3dda94df031d8ad0f48e2e4b6b82faeb34d4eb50e683169`.
La prova independent en una ruta nova i sense xarxa és
`tmp/pr1-guided/relocation-run10.json`.

Per reproduir-la cal utilitzar la mateixa imatge QGIS indicada a la secció
d'inspecció, un directori d'escena nou i aquestes entrades executables:

1. `prepare_pr1_guided.py prepare --stage /workspace/tmp/pr1-guided/RUN/tig`,
   amb el repositori en lectura i només `tmp/pr1-guided` modificable.
2. Muntar l'escena a `/home/docent/tig`, iniciar Xvfb i QGIS amb
   `--code /workspace/context/practiques/capture_pr1_guided.py`, el perfil
   `pr1` i els fitxers d'autenticació temporals creats pel preparador.
   El patró complet de la invocació GUI és el de
   [la guia PR3](pr3-filtres-expressions.md#reproducció), canviant actor i perfil.
   La xarxa només s'utilitza per al WMS real.
3. `prepare_pr1_guided.py verify --stage /review --report /reports/pr1.json`,
   amb l'escena en una ruta nova, en lectura i sense xarxa.
4. `publish --stage ...` reté el paquet local sense sobreescriure cap fitxer
   existent; no desplega el lloc.

La GUI es configura en `ca_ES`; es conserven els controls encara en anglès.
La preparació utilitza un perfil dedicat, `auth/use_password_helper=false`
i `QGIS_AUTH_PASSWORD_FILE` temporal per evitar un diàleg de keyring aliè
al procediment. El paquet retingut no inclou aquest perfil ni la contrasenya.
