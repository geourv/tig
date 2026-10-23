# Escena docent de geoprocessament CNIG

Cal mostrar a QGIS 3.44 en català el recorregut del capítol 6 i PR4. Començar
per les quatre envolupants del municipi original i el selector de tipus de
`qgis:minimumboundinggeometry`. Explicar distància, CRS i aproximació abans
del diàleg de buffer de 500 m. Sobre aquest buffer, calcular la caixa no
orientada desada com `roi`. Continuar amb preparació i superposició de punts,
línies i polígons, diferències, parts i punts derivats.

La vista general ha de mostrar l'Explorador amb les connexions al GeoPackage
del projecte i als originals de CartoCiudad i del viari CNIG. Les capes
`portalpk_publi`, `manzana` i `rt_tramo_vial` han de conservar la procedència.
Cal carregar el WMS oficial IGN/PNOA com a capa QGIS de context sota els vectors,
amb contorns sense farciment que conservin els colors de l'ortofoto.
Una imatge descarregada no s'ha de presentar com aquesta connexió WMS.

La vista general precedeix els menús i diàlegs. Les captures importants es
reutilitzen al manual i als PDF de pràctica amb peus adequats. Els controls
de CRS, geometria i font es comproven també sobre les dades; l'ortofoto és
un contrast visual, no una prova completa d'exactitud posicional.

Els punters s'ancoren a una caixa destacada o un cercle petit visible sobre
el control real. Els textos són breus; s'ha de comprovar que tots apareguin
al PNG/SVG i al manifest. Cada captura acompanya la seva explicació i el
control del resultat, sense galeria tardana desconnectada de la teoria.

La captura es fa amb el MCP i una superfície gràfica aïllada de l'escriptori
de l'autor. Els resultats GIS verificats continuen al bundle local; l'escena
amb WMS requereix xarxa i no es presenta com un projecte portable offline.
