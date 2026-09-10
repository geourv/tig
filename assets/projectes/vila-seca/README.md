# Projecte TIG: punt de partida de Vila-seca

Aquest paquet proporciona una fita inicial, petita i transportable, per seguir el projecte acumulatiu del manual. No és una anàlisi acabada: només conté el fons remot de context, el límit municipal oficial preparat i les dues representacions del projecte QGIS.

## Contingut

- `dades_originals/vila-seca-cnig.geojson`: resposta de l'objecte `1172246` de l'API OGC Features de l'IGN/CNIG, reserialitzada de manera canònica sense alterar propietats ni coordenades.
- `dades_preparades/projecte_tig.gpkg`: GeoPackage amb la capa `municipi_treball` en `EPSG:25831` i la fita QGIS incrustada `projecte_tig`.
- `projecte_tig.qgz`: còpia externa canònica del projecte, amb camins relatius.
- `procedencia.yml`: productor, URLs, llicències, identificadors, transformacions i entorn de construcció.
- `SHA256SUMS`: sumes dels fitxers que formen el paquet, excepte el mateix inventari i el ZIP per evitar referències circulars.
- `build_project.py`: construcció i validació executades amb PyQGIS dins del runtime fixat.

El projecte separa el WMS `OI.OrthoimageCoverage` del PNOA, que només aporta context visual, de `municipi_treball`, que és l'entrada vectorial local. El WMS necessita xarxa per dibuixar-se; la capa municipal continua disponible sense connexió.

## Font i atribució

La unitat administrativa prové de l'objecte `1172246` de la col·lecció `administrativeunit` de l'API oficial de l'IGN/CNIG, consultat el 8 de setembre de 2026. La llicència enllaçada per la col·lecció és la llicència de productes i serveis de l'IGN, que adopta CC BY 4.0. L'atribució del vector preparat és:

> Obra derivada de la unitat administrativa 1172246 de l'IGN/CNIG, CC BY 4.0 ign.es.

El document `GetCapabilities` del WMS PNOA declara `CC BY 4.0 scne.es` a `AccessConstraints`.

## Normalització i preparació

El servidor alterna diverses serialitzacions JSON amb espais i ordre de claus diferents, tot i que el contingut analitzat és idèntic. El constructor llegeix la resposta, comprova `id = 1172246`, `nameunit = Vila-seca`, `nationallevelname = Municipio`, `nationalcode = 34094343171`, `country = ES`, `codnut3 = ES514` i una geometria `MultiPolygon`. Després ordena les claus, elimina espais no significatius, escriu UTF-8 amb un salt final i exigeix el SHA-256 canònic `abf389424da192263a1f44a569a8f5c9ffb6eeaec5245b22932fb0859831f321`.

`municipi_treball` transforma la geometria de `EPSG:4326` a `EPSG:25831`, conserva l'identificador de l'objecte i el codi oficial i deriva `codi_muni = 43171` amb la regla `right(nationalcode, 5)`. La transformació no repara ni simplifica la geometria.

QGIS genera alguns noms auxiliars, identificadors, colors i ordres d'atributs diferents a cada procés. Abans d'empaquetar, el constructor els substitueix per valors deterministes, fixa les marques temporals, normalitza els membres del QGZ i compacta el GeoPackage. La validació rebutja un projecte que no conservi aquesta serialització canònica.

## Reconstrucció

Des de l'arrel del repositori, la descàrrega declarada es prepara amb el proveïdor `unaltracaptura-qgis`:

```bash
unaltracaptura-qgis prepare-teaching-data --resource cnig-vila-seca-administrative-unit --operation download --overwrite
```

La construcció usa exclusivament QGIS 3.44.11 dins de la imatge fixada. La xarxa és necessària durant aquesta ordre només per validar la capa WMS remota:

```bash
docker run --rm --pull=never --network=bridge \
  --user "$(id -u):$(id -g)" \
  -e HOME=/tmp -e QT_QPA_PLATFORM=offscreen \
  --mount "type=bind,source=$PWD,target=/workspace" \
  -w /workspace --entrypoint /usr/bin/python3 \
  qgis/qgis@sha256:e016b5296b99f0b07760b883888bc4ba615c0099feae9432374b4c83e8e073cc \
  assets/projectes/vila-seca/build_project.py
```

La validació sense regeneració repeteix els controls de GeoJSON, SQLite, esquema, CRS, geometria, capes, grups, camins relatius, fita incrustada, sumes i prova de transport des del ZIP:

```bash
docker run --rm --pull=never --network=bridge \
  --user "$(id -u):$(id -g)" \
  -e HOME=/tmp -e QT_QPA_PLATFORM=offscreen \
  --mount "type=bind,source=$PWD,target=/workspace" \
  -w /workspace --entrypoint /usr/bin/python3 \
  qgis/qgis@sha256:e016b5296b99f0b07760b883888bc4ba615c0099feae9432374b4c83e8e073cc \
  assets/projectes/vila-seca/build_project.py --check
```

Les sumes també es poden comprovar des del directori del miniprojecte amb `sha256sum -c SHA256SUMS`. El SHA-256 del ZIP es publica a la sortida JSON del constructor perquè no es pot incloure dins del mateix arxiu sense crear una referència circular.

## Obertura i comprovació

La continuació ordinària del curs parteix de `projecte_tig.qgz`. La fita incrustada s'obre separadament amb `Projecte > Obre des de > GeoPackage`, seleccionant `dades_preparades/projecte_tig.gpkg` i el nom `projecte_tig`. Desar una representació no actualitza l'altra.

En totes dues obertures s'ha de trobar una entitat a `municipi_treball`, el CRS `EPSG:25831`, els grups funcionals i les mateixes dues capes. Una prova sense xarxa pot deixar el WMS indisponible, però no ha de trencar la font local del GeoPackage.
