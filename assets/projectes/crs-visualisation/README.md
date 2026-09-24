# Entrades de les captures de CRS del capítol 3

Aquestes entrades s'utilitzen amb `unaltracaptura-qgis-crs.yml` i
`recipes/qgis-crs-visualisation.yml`. Les captures es generen exclusivament
amb el MCP unaltracaptura-qgis, amb la imatge QGIS 3.44.11 fixada pel projecte.

## Fonts

- `icgc-orthophoto-2025.xml` és un descriptor GDAL del WMS oficial de l'ICGC:
  <https://geoserveis.icgc.cat/servei/catalunya/orto-territorial/wms>, capa
  `ortofoto_25cm_color_2025`, resposta en `EPSG:25831`. L'extensió sobre Vila-seca
  és `[339500, 4547500, 349900, 4555300]`, amb una graella de 1600 × 1200 píxels.
  Atribució: ICGC, Ortofoto Territorial 2025, CC BY 4.0.
- `openstreetmap.xml` és un descriptor GDAL del servei XYZ
  <https://tile.openstreetmap.org/{z}/{x}/{y}.png>. La font es manté en
  `EPSG:3857` en les dues vistes. Atribució:
  [© OpenStreetMap contributors](https://www.openstreetmap.org/copyright).
- `world-extent.geojson` fixa l'enquadrament mundial de la vista geogràfica:
  longituds −180–180 i latituds aproximades −85,05–85,05 en WGS 84, segons la
  cobertura Web Mercator de les tessel·les. No inclou els pols.
- `world-view-25831.csv` i `world-view-25831.vrt` defineixen un marc de càmera
  sintètic en metres per a la prova mundial en `EPSG:25831`: est −17.000.000 a
  18.000.000 i nord −20.500.000 a 20.500.000. Aquesta geometria auxiliar oculta
  només serveix per enquadrar la demostració fora de l'àrea d'ús. No és el
  domini vàlid del CRS ni la transformació d'un límit geogràfic mundial.
- Els dos fitxers `.xml.aux.xml` són metadades PAM generades per GDAL en obrir
  els descriptors: conserven el camí relatiu de la memòria cau i estadístiques
  aproximades de les bandes. Formen part del paquet generat de les captures
  i s'han de regenerar amb el renderitzador, sense editar-los manualment.

Els descriptors són fitxers de dades, segons la
[documentació pública del controlador WMS de GDAL](https://gdal.org/en/stable/drivers/raster/wms.html).
El MCP els obre amb `load_raster`; el controlador accedeix als serveis reals.
No s'utilitzen imatges substitutives ni es modifica el proveïdor de captures.

## Enquadrament i xarxa

La recepta carrega primer l'enquadrament local i només sol·licita les imatges
necessàries per a les vistes. OpenStreetMap queda limitat al nivell 3, amb un
User-Agent identificable, dues connexions simultànies i una memòria cau de set
dies sota `tmp/`. No es distribueix cap arxiu de tessel·les ni es prepara una
descàrrega fora de línia. Les dues captures comparteixen la font mundial;
cadascuna utilitza un enquadrament expressat en les unitats del seu CRS.

La comparació és expressament global. `EPSG:25831` és un CRS regional del fus
UTM 31N: en aplicar-lo al món apareixen deformacions extremes i discontinuïtats.
Els buits polars de la font són una limitació diferent, pròpia de les tessel·les
Web Mercator. Els peus de figura expliquen aquestes dues limitacions.

La configuració específica habilita la xarxa per a aquestes captures. La
configuració general `unaltracaptura-qgis.yml` manté la xarxa desactivada.
Els serveis en línia poden canviar: els PNG, SVG i manifests conservats són
l'evidència de la renderització revisada.

## Captures del MCP

Amb `config="unaltracaptura-qgis-crs.yml"`, els identificadors de captura són:

- `qgis-crs-visualisation.project-crs-icgc-2025`
- `qgis-crs-visualisation.osm-crs-4326`
- `qgis-crs-visualisation.osm-crs-25831`

Cal validar la recepta, executar `render_recipe` i revisar els resultats abans
d'actualitzar les figures del capítol. Les crides «Reprojecció al vol» indiquen
el codi i nom del CRS i utilitzen el selector real
`mOntheFlyProjectionStatusButton`; no s'editen manualment les imatges.
