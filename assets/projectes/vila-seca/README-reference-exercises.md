# Projectes QGIS de referència de Vila-seca

Aquests artefactes resolen tres contractes docents acotats. No són lliuraments que
l'estudiant hagi de copiar i no substitueixen l'aplicació al municipi assignat.
Cada GeoPackage conté un únic projecte QGIS incrustat i té un `.qgz` homònim amb
camins locals relatius.

## Inventari

| Exemple | Projecte incrustat | Finalitat |
| --- | --- | --- |
| `pr1-fonts-vila-seca` | `pr1` | Comparar els límits municipals oficials de l'ICGC i del CNIG sobre l'Ortofoto Territorial 2025 |
| `pr2-digitalitzacio-vila-seca` | `pr2` | Inspeccionar esquemes de punt, línia i polígon, identificadors estables i ajust a vèrtexs |
| `ex05-seleccions-jerarquiques-vila-seca` | `ex05` | Comparar seleccions jeràrquiques per atribut amb seleccions per relació espacial |

PR2 conserva `municipality_icgc_5k` i `municipality_cnig`, en deriva
`municipi_treball` i afegeix `fanals`, `carrils_bici` i `plaques_solars`. Totes
les geometries d'aquestes tres últimes capes són **fixtures didàctiques
sintètiques**. No provenen de camp, inventari ni ortofoto, i el camp `estat_rev`
les marca com a `no_apte_per_analisi`.

`ex05` és un exemple de selecció, no una versió reduïda de la micropràctica 3.
Conserva la base completa de 947 municipis de l'ICGC, les seleccions per
`CODIPROV`, `CODIVEGUE`, `CODICOMAR` i `CODIMUNI`, una selecció espacial
equivalent per a Tarragona, basada en un punt interior de cada municipi, i els
municipis que toquen Vila-seca.

## Fonts ignorades

El constructor no publica els originals. Abans d'executar-lo, cal desar-los a
`tmp/reference-exercises/sources/` i comprovar-ne els resums:

```bash
mkdir -p tmp/reference-exercises/sources
curl --fail --location --output \
  tmp/reference-exercises/sources/divisions-administratives-v2r2-municipis-5000-20260120.fgb \
  https://datacloud.icgc.cat/datacloud/divisions-administratives/fgb_unzip_EPSG25831/divisions-administratives-v2r2-municipis-5000-20260120.fgb
curl --fail --location --request POST \
  --data 'secDescDirLA=12408588&secuencial=12408588&codSerie=LILIM' \
  --output tmp/reference-exercises/sources/lineas_limite_gml.zip \
  https://centrodedescargas.cnig.es/CentroDescargas/descargaDir
sha256sum tmp/reference-exercises/sources/*
```

Resums esperats:

```text
069f755f253f7af969e80403f6e81fa2cadefbd4c40ffd2f825f30e167bf2b2d  divisions-administratives-v2r2-municipis-5000-20260120.fgb
5bd73c530af995c05da8d9ff4e3d293f62d0dc91c5e48ee773fe881716c108a6  lineas_limite_gml.zip
```

## Llicències i atribució

Les divisions administratives i l'Ortofoto Territorial de l'ICGC s'utilitzen
sota la llicència [CC BY 4.0 de l'ICGC](https://www.icgc.cat/ca/LICGC/Informacio-publica/Transparencia/Reutilitzacio-de-la-informacio).
La [fitxa oficial de les divisions administratives](https://www.icgc.cat/ca/Geoinformacio-i-mapes/Dades-i-productes/Geoinformacio-cartografica/Divisions-administratives)
confirma aquesta llicència per a l'edició utilitzada. L'atribució és «Institut
Cartogràfic i Geològic de Catalunya (ICGC), CC BY 4.0».

Les unitats administratives del CNIG s'utilitzen sota les
[condicions de llicència de l'IGN](https://www.ign.es/resources/licencia/Condiciones_licenciaUso_IGN.pdf),
que adopten CC BY 4.0.

## Construcció i comprovació

Un cop preparats i verificats els dos originals de l'apartat anterior, la
construcció utilitza QGIS 3.44.11 dins de la imatge fixada i sense xarxa. El
constructor valida la configuració declarada de la capa WMS, però no en requereix
la disponibilitat remota. La connexió només és necessària per dibuixar aquest
context quan s'obre el projecte.

```bash
docker run --rm --pull=never --network=none \
  --user "$(id -u):$(id -g)" \
  -e HOME=/tmp -e QT_QPA_PLATFORM=offscreen \
  --mount "type=bind,source=$PWD,target=/workspace" \
  -w /workspace --entrypoint /usr/bin/python3 \
  qgis/qgis@sha256:e016b5296b99f0b07760b883888bc4ba615c0099feae9432374b4c83e8e073cc \
  assets/projectes/vila-seca/build_reference_exercises.py
```

La validació sense regeneració substitueix l'última línia per:

```text
assets/projectes/vila-seca/build_reference_exercises.py --check
```

El constructor verifica fonts, esquemes, recompte, CRS, geometries, topologia de
la fixture lineal, ajust del projecte, composicions, camins relatius, equivalència
entre projectes externs i incrustats, integritat SQLite, els tres informes de
`informes/` i `SHA256SUMS-reference-exercises`.

## Obertura

Es pot obrir el `.qgz` des del directori `assets/projectes/vila-seca/` o el
projecte incrustat des del GeoPackage corresponent de `dades_preparades/`. En
tots dos casos s'han de resoldre les mateixes capes locals. La capa WMS de PR1 i
PR2 és context visual remot i no participa en cap selecció ni derivació.
