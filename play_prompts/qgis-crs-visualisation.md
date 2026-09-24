# CRS del projecte i visualització al vol a QGIS

Cal preparar tres captures reals de la interfície de QGIS per al capítol 3 del
manual TIG. La interfície i les anotacions han d'estar en català. S'ha d'utilitzar
QGIS 3.44.11 amb la imatge fixada a la configuració del consumidor i conservar
visibles la finestra principal, el panell de capes, el llenç i la barra d'estat.

## Primera captura: ortofoto i CRS del projecte

Nom de sortida: qgis-project-crs-icgc-2025.

El llenç ha de mostrar el WMS oficial de l'Ortofoto Territorial 2025 de l'ICGC,
capa ortofoto_25cm_color_2025, sobre Vila-seca. El servei és
https://geoserveis.icgc.cat/servei/catalunya/orto-territorial/wms.
El CRS del projecte ha de ser EPSG:25831. L'extensió de referència en aquest CRS
és 339500,4547500,349900,4555300.

Cal ressaltar amb una crida el control real del CRS del projecte a la barra
d'estat. La crida ha de dir «Reprojecció al vol» i identificar «EPSG:25831 ·
UTM 31N». La finalitat és explicar on es
controla la referència del llenç i distingir-la del CRS de les fonts. No s'ha
d'inventar un interruptor de reprojecció al vol ni modificar gràficament el text
de la interfície. Aquesta captura serà la subfigura a, al costat de la captura
existent assets/img/qgis/qgis-crs-selection.png com a subfigura b.

## Segona i tercera captures: comparació amb OpenStreetMap

Noms de sortida: qgis-osm-crs-4326 i qgis-osm-crs-25831.

Cal carregar el mapa XYZ d'OpenStreetMap de
https://tile.openstreetmap.org/{z}/{x}/{y}.png i obtenir dues vistes mundials,
amb la mateixa mida de finestra i els mateixos panells. La vista geogràfica
comprèn totes les longituds i la cobertura de les tessel·les fins a aproximadament
85 graus nord i sud. La primera vista utilitza EPSG:4326 com a CRS del projecte;
la segona, EPSG:25831. La font XYZ continua en EPSG:3857 en tots dos casos.

La vista EPSG:25831 és una demostració expressa fora de l'àrea d'ús del fus UTM
31N. Ha de mostrar les deformacions i els talls reals que produeix QGIS en
intentar representar el mapa mundial amb aquest CRS regional; no s'ha de
presentar com una projecció global adequada. El marc de càmera en metres és
només un recurs d'enquadrament, no una extensió geogràfica vàlida del CRS.

Cal assenyalar el control real del CRS a la barra d'estat amb una crida
«Reprojecció al vol» i el codi i nom del CRS de cada vista. S'ha de conservar
l'atribució d'OpenStreetMap i deixar
el llenç lliure d'etiquetes explicatives llargues. Les dues captures formaran
una figura independent amb disposició a+b en una mateixa fila.

## Condicions de captura

Cal esperar que les imatges remotes s'hagin dibuixat abans de capturar. Una vista
buida, un error de xarxa o una capa local substitutiva no satisfan la petició.
Les anotacions han d'utilitzar selectors de widgets reals, sense coordenades
inventades. Cal conservar PNG, SVG anotat i manifest de cada captura.
