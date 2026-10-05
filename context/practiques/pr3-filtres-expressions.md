# Capítol 5: recorregut de consultes amb dades del CNIG

Document d'autoria, en revisió. La reserva inicial és la del comentari
5962934449 de geourv/tig#21; la revisió pedagògica i les 32 addicions exactes
del comentari 5974923119 s'han acceptat al comentari 5978541431.
La seqüència d'exportacions natives afegeix els 30 camins del comentari
5979824558, acceptats al comentari 5979853676.

## Seqüència docent

1. Localitzar Vila-seca al mapa CNIG i seleccionar-lo amb un clic.
2. Clic dret a la capa activa, Filtre ressaltat i consulta provincial.
3. Taula: seleccionats, visibles al mapa i expressió amb zero seleccionats.
4. Eines de selecció, modificadors i contrast de mapa amb capçaleres de fila.
5. Menú i diàleg natius de selecció per expressió; mateix municipi inicial.
6. Selecció per ubicació, mapa de seleccionats, exportació nativa i reobertura
   de portals, illes contingudes i autovies/autopistes sobre el terme CNIG.
7. Calculadora: tipus, creació, actualització, ajuda nativa d'aggregate,
   comprovacions i etiquetes.

El text publicable és `_chapters/ca/05-consultes-dades-relacionals.md`.
Les expressions llegibles en captures no es repeteixen com a blocs previs.
La teoria apareix quan el cas la necessita: no hi ha un catàleg de funcions
desconnectat al començament.

## Fonts i referència espacial

`pr3-sources.yml` fixa les tres edicions d'Información Geográfica de Referencia
del Centre de Descàrregues del CNIG, els recursos del catàleg, els SHA-256,
el runtime QGIS i el proveïdor d'anotació. El protocol de descàrrega és el
botó oficial del navegador. El primer intent directe havia retornat HTML
amb extensió ZIP; les entrades vàlides són les de `tmp/pr3-guided/browser/`.

`prepare_pr3_guided.py download` rebutja tipus, hashes o edicions diferents.
La preparació extreu a `tmp/pr3-guided/inputs-exact/`, contrasta els CRC amb
el ZIP fixat i deixa els fitxers en lectura. L'extracció exploratòria anterior
a `inputs/` es conserva separada: OGR havia canviat metadades dels GeoPackage
encara que no s'editessin les entitats.

La referència de les consultes és **municipi_consulta**, exportada de la font
municipal CNIG amb `NATCODE=34094343171`, geometria completa i EPSG:25831.
`municipi_vilaseca` i `municipi_treball` conserven la geometria ICGC heretada
i no intervenen en aquestes seleccions. La concordança ICGC `431711` → `43171`
és explícita per a Vila-seca, no una regla general de truncament.

Controls de les edicions fixades amb la referència CNIG:

- 8.132 municipis a la font peninsular/balear; 184 amb CODNUT3=ES514.
- Quatre províncies catalanes i tres comunitats de context.
- 368.290 punts CartoCiudad: 364.921 Portal i 3.369 PK.
- 3.584 portals seleccionats tant amb intersecció com amb contenció.
- 28.459 illes originals de tipus Polygon: 285 contingudes, 318 que intersecten
  i 33 diferències. El resultat principal desa les 285 contingudes.
- 233.982 registres de transport originals; les dues classes d'autovia/autopista
  deixen 3.663 candidats provincials i 265 que intersecten Vila-seca.
- Els 265 registres contenen 185 valors diferents d'id_tramo. Entre els noms
  hi ha A-7, AP-7, E-15, el corredor TEN-T i trams classificats d'autovia de
  T-11 i N-340. No confondre files d'itineraris amb eixos viaris únics.
- Longitud el·lipsoidal sumada dels registres complets: 79,33703645114218 km.
- Àrea CNIG de Vila-seca: 21.704.046,024839967 m² plans i
  21.708.436,980199665 m² el·lipsoidals GRS80.
- Camp area_km2 actualitzat a sis decimals: 21,708437 per a Vila-seca.
- Suma de les 184 àrees actualitzades: 6.306,697054 km²; quota de Vila-seca
  0,34421245882155543%; les quotes sumen 100% dins la tolerància.
- Classes: 37 petit, 105 mitja i 42 gran.

Els valors anteriors de la revisió `run17` usaven ICGC com a referència espacial.
No es barregen amb aquests recomptes. Una signatura dels atributs originals
i de la geometria normalitzada contrasta cada exportació amb les entitats
font reprojectades. No s'ha aplicat cap retall, buffer o superposició geomètrica.
Els recomptes filtrats de GeoPackage es verifiquen per iteració, perquè el
recompte ràpid d'aquest proveïdor pot retenir el total anterior al filtre.

La selecció s'avalua a la font original, en EPSG:4258; després l'exportació
reprojecta a EPSG:25831. No s'han de barrejar recomptes reavaluats sobre una
altra representació de coordenades: a la frontera pot haver-hi sensibilitat
numèrica. El control final comprova explícitament que totes les illes desades
quedin dins del municipi i que tots els registres d'autovia exportats
l'intersectin també en el CRS de sortida.

## GUI i anotació

`capture_pr3_guided.py` és l'actor específic que prepara estats reals de QGIS
i executa clics, gestos, selecció per expressió, Processament i calculadora.
`pr3-captures.yml` declara les 27 captures i les intencions d'anotació;
l'estructura s'ha validat amb el MCP instal·lat d'unaltracaptura 0.3.0.
El motor publicat genera PNG anotada, SVG amb PNG original incrustada i
manifest. No es copia ni es modifica el seu codi.

El bridge del proveïdor és un executor d'una sola sessió i surt després de
renderitzar. Per això `prepare_pr3_guided.py capture` executa primer el
recorregut complet i després repeteix cada prefix en una còpia pròpia de la
llavor per lliurar-ne l'estat al bridge. Dues instàncies poden renderitzar
escenes amb camins i contenidors disjunts; l'assemblatge és serial.

Els rectangles surten de widgets visibles de la captura activa i de
`QMenu.actionGeometry`, no d'estimacions sobre la PNG. Els selectors de text
amplis poden trobar una acció pare; s'utilitzen rectangles Qt identificats
per a les accions de selecció i els controls repetits. L'expressió queda
associada al diàleg actual, perquè QGIS pot conservar controls homònims de
diàlegs anteriors ja tancats. La ubicació del clic manual es registra a partir
de l'esdeveniment real sobre el llenç.

Les etiquetes municipals es col·loquen dins del seu polígon. Les anotacions
eviten cobrir els noms i els controls. El panell de filtre d'expressió s'amplia
segons la mètrica real del text per mostrar tota la consulta. L'ajuda d'aggregate
és la nativa: es mostra la funció seleccionada, la signatura i l'inici dels
arguments, i el text explica que cal desplaçar-la per llegir-ne la resta.

La captura d'un diàleg prova la configuració. `gui-evidence.json` prova les
accions posteriors: mateix ID amb clic i expressió, tres seleccions espacials,
tres exportacions natives, creació i actualització de 184 àrees i 184 quotes.
La preparació conserva els resultats esperats a `controls/expected-exports.gpkg`,
separats del GeoPackage de treball. Les tres capes de destinació encara no
existeixen a la llavor: és el diàleg natiu el que les crea al contenidor existent.
L'actor contrasta cada capa afegida al mapa amb la signatura independent dels
atributs i de la geometria; `native_exports` conserva la prova i els paràmetres.

Les capes administratives i els camps complementaris es preparen amb PyQGIS;
el desament final de pr3 i del qgz també és PyQGIS. Les seleccions de punts,
illes i vies s'exporten realment amb la GUI, no es representen com a clics
uns fitxers ja preparats. Les capes de control no són dependències del resultat.

Les vistes de selecció i de resultat de portals, illes i viari comparteixen
l'extensió del terme municipal complet, ampliada pel mateix factor 1,25.
El contorn municipal queda visible per comprovar el conjunt dins i fora del
polígon, sense substituir aquesta vista per un zoom interior de barri.
Les illes desades tenen farciment blau i els portals, símbol taronja; el groc
es reserva a la selecció nativa. Es força el repintat després de canviar
l'estil perquè la memòria cau del llenç no mostri un color anterior. Al mapa
viari s'etiqueta un tram interior llarg d'A-7 i un d'AP-7 per evitar un cúmul
de noms repetits; els identificadors etiquetats queden al registre de la GUI.

## Reproducció i verificació

Cal disposar del runtime fixat, els tres ZIP comprovats i la guia PR1. La roda
publicada es descarrega amb `gh release download v0.3.0`, seleccionant només
`unaltracaptura_qgis-0.3.0-py3-none-any.whl`, i se'n comprova el SHA del catàleg.
La versió 0.3.0 del launcher requereix Python 3.11 o posterior.

Des de l'arrel del checkout, en un nom d'execució nou:

```bash
uv run --no-project --python /usr/bin/python3 --with PyYAML \
  python context/practiques/prepare_pr3_guided.py capture \
  --stage "$PWD/tmp/pr3-guided/revisio-nova" \
  --annotation-wheel /ruta/unaltracaptura_qgis-0.3.0-py3-none-any.whl
```

La sortida completa queda a `revisio-nova/main`; `seed` conserva l'estat inicial
i `frames` les sessions del proveïdor. El procés rebutja una escena existent,
una roda diferent, captures amb avisos, accions fallides o càlculs discrepants.
El perfil i l'autenticació són temporals i no es copien al paquet final.

La finalització tanca el diari WAL amb QGIS ja aturat. Després es munta `main`
en lectura a `/review` dins del runtime fixat, sense xarxa, i s'executa:

```text
prepare_pr3_guided.py check --stage /review --report /reports/validation.json
```

El report s'ha de desar com a `main/validation.json` des d'un muntatge d'informes
modificable. El control reobre les dues representacions del projecte, comprova
les nou capes locals, geometries, signatures, tipus/resultats, quotes, integritat
SQLite, camins relatius, evidència de les tres exportacions natives i els
27 conjunts PNG/SVG/manifest. La inspecció no pot
canviar els bytes verificats. El WMS continua sent una dependència de xarxa.

`publish --stage ...` reté els quatre fitxers de `pr3-guia` i les captures dins
del consumidor; no publica el web. Per a aquesta revisió demanada per l'autor,
`--replace-reviewed` conserva els artefactes locals anteriors a
`main/previous-retained/` abans de substituir-los. La publicació local comprova
novament els hashes i no obre els GeoPackage en escriptura.

`validation.json` inclou els controls i l'evidència de les captures; la lectura
del paquet final no depèn de conservar el camí temporal de l'execució. La
revisió del web i del PDF ha de comprovar especialment ordre, accés als menús,
ressaltats correctes, consulta completa i ajuda de funcions llegible.
