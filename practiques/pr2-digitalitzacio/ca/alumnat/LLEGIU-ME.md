---
title: "PR2 · Digitalització de fanals, carrils bici i plaques solars"
lang: ca
recipient: alumnat
content_status: approved
subject: "Tecnologies de la Informació Geogràfica"
subject_code: "21234114"
author: "Benito Zaragozí"
institution: "Universitat Rovira i Virgili"
---

# Finalitat i resultats d’aprenentatge

Com es transforma una observació del carrer o d’una ortofoto en dades que es puguin consultar i analitzar? La pràctica construeix tres capes diferents: punts per als fanals, línies per als carrils bici i polígons per a les plaques solars. Cada geometria respon a una unitat d’observació i necessita atributs, procedència i controls propis.

El cas de classe se situa al carrer de Joanot Martorell i a l’entorn de la Facultat de Turisme i Geografia de Vila-seca. El treball propi aplica els mateixos criteris a un sector del municipi escollit. En acabar, cal poder justificar l’esquema, capturar entitats amb ajust quan correspongui, comprovar-ne la qualitat i conservar-les al GeoPackage que heretaran PR3 i PR4.

El professor indica a classe els apartats obligatoris del **70% bàsic** i els recull a Moodle, amb el sector i els controls seleccionats. La guia completa inclou variants que no són totes obligatòries. Els tres esquemes i la traça de les dades es conserven per continuar el recorregut.

# Punt de partida i dades

Amb QGIS tancat, es copia el GeoPackage validat de PR1 a `sandbox/pr2-digitalitzacio-cognom.gpkg`. Les capes i taules heretades s’han de trobar físicament dins del contenidor nou. El `.qgz` de PR1 no es copia ni es reanomena: s’obrirà la vista incrustada, es comprovaran i reorientaran les fonts i es desarà el principal nou com a `pr2`.

El punt de partida és la **PR1 pròpia**, preparada amb originals CNIG. El projecte i les capes de captura treballen en **EPSG:25831**. El context visual es consulta al servei oficial IGN/PNOA, complementat amb observacions quan calgui. Cal registrar la imatge que realment cobreix el sector, la llicència i les dates d’imatge, captura i visita.

La connexió WMS es prepara com a PR1, amb `https://www.ign.es/wms-inspire/pnoa-ma?` i la capa `OI.OrthoimageCoverage`. La capa `OI.MosaicElement` permet consultar data i resolució als punts d’interès. Cada estudiant comprova que el detall i l’actualitat siguin suficients per reconèixer els objectes; una còpia de context d’un exemple docent pot tenir una mida de píxel inadequada per digitalitzar.

Un objecte difícil de reconèixer no s’inventa. Si no es pot determinar el peu d’un fanal o la vora d’un panell, cal registrar la incertesa o contrastar una altra font. Una ombra no és la base del fanal; una coberta semblant a una placa no n’acredita la funció ni l’estat operatiu.

# Procediment

## Definir les tres capes

Cada estudiant crea les taules de captura dins del seu GeoPackage de PR2 i n’estableix tipus i dominis a partir de l’esquema següent. Les capes heretades es conserven. Els identificadors són text estable, no el número de fila ni un `fid` regenerable.

| Capa | Geometria i unitat d’observació | Identificador |
| --- | --- | --- |
| `fanals` | `Point`; un suport de fanal identificat | `id_fanal` |
| `carrils_bici` | `LineString`; un tram entre extrems o nodes definits | `id_tram` |
| `plaques_solars` | `Polygon`; una superfície contínua de panells segons el criteri de captura | `id_placa` |

Table: Esquema geomètric de PR2, en EPSG:25831.

`fanals` i `plaques_solars` incorporen `tipus`, `estat`, `data_obs`, `font`, `observacio` i `estat_rev`. `carrils_bici` incorpora `tipus`, `continu`, `font`, `data_font`, `observacio` i `estat_rev`. Les dates es desen com a dates; `continu` és enter, amb 1 per a continuïtat comprovada, 0 per a una discontinuïtat identificada i nul quan no s’ha pogut valorar.

La font i l’identificador són obligatoris. `NULL` expressa una absència justificada, no zero ni un estat operatiu presumit. `estat_rev` permet distingir una captura pendent de comprovació d’una de revisada; les geometries de demostració sintètica es mantenen identificades com a tals i no es converteixen en observacions canviant-ne l’etiqueta.

Abans de capturar tot el sector, cal provar una entitat de cada tipus, un identificador repetit i un valor fora del domini. Convé comprovar quines restriccions són del projecte QGIS i quines viatgen amb el GeoPackage.

## Capturar els fanals

El sector de classe és el tram de Joanot Martorell de l’entorn de la Facultat. Cal definir-ne els extrems i la convenció de posició: preferentment el peu del suport identificat, no el centre del símbol ni la punta de l’ombra. S’activa l’edició de `fanals`, es capturen els punts i s’emplenen els atributs mentre la font encara és visible.

La posició i l’estat del fanal són observacions diferents. L’ortofoto pot ajudar a localitzar un objecte, però no prova que funcioni. Si l’estat és desconegut, es conserva com a desconegut o nul segons el domini definit. Cal revisar coincidències de coordenades i d’identificadors abans de considerar dues files com a dos fanals.

## Capturar els carrils amb autoensamblat

Es fa visible la barra d’**Autoensamblat** i s’especifica la capa de destinació de l’ajust: `carrils_bici`. Per connectar trams consecutius es comprova l’ajust a vèrtexs; si s’utilitzen segments, cal valorar si la connexió exigeix també inserir un node o partir el tram receptor.

La tolerància s’expressa amb les seves unitats. Una prova inicial de 10 píxels serveix per observar el comportament interactiu, però s’ha d’ajustar a la densitat, l’escala i la pantalla. No equival a 10 m ni a una exactitud posicional de la font.

Cada tram ha de seguir una convenció d’eix i de sentit. Els extrems que representen una connexió han de coincidir geomètricament; els encreuaments a diferent nivell no es connecten només perquè es toquin al mapa. Cal comprovar l’indicador d’ajust abans de confirmar el vèrtex i revisar els nodes després de desar.

## Capturar els polígons de plaques solars

Es delimita cada superfície contínua de panells identificable sobre la coberta de la Facultat en el cas de classe. El criteri d’agrupació es manté durant tota la captura: una fila no pot significar una placa en un lloc i tota una instal·lació en un altre.

Les geometries han de tenir anells tancats, sense autointerseccions ni solapaments accidentals. Les eines de digitalització avançada poden ajudar a imposar paral·lelisme o perpendicularitat quan la font ho justifiqui. No cal afegir vèrtexs a un contorn borrós per aparentar més precisió.

La superfície digitalitzada és una superfície en planta. No determina la potència, la producció elèctrica ni l’àrea inclinada dels panells sense informació addicional. Cal conservar aquestes limitacions a la interpretació.

# Comprovacions i interpretació

| Capa o aspecte | Comprovació |
| --- | --- |
| Totes les capes | Geometria del tipus previst, no buida, CRS correcte i procedència explícita |
| Identificadors | Cap nul ni duplicat a la clau estable |
| Fanals | Convenció de posició coherent; coincidències revisades; estat no inferit de la imatge |
| Carrils | Nodes previstos coincidents; microbuits, duplicats i discontinuïtats documentats |
| Plaques | Polígons vàlids; unitat d’observació constant; límits visibles i justificats |
| Herència | Capes municipals i noves taules al GeoPackage de PR2 |

Table: Controls de la captura abans de continuar.

La validesa geomètrica no demostra exactitud territorial. Una línia pot ser vàlida i estar al carrer equivocat; dos trams poden ser vàlids però no connectar. Les eines de validació s’acompanyen de la revisió de la font i de les regles de cada capa.

# Aplicació al municipi escollit

Cal delimitar un sector equivalent amb fanals, trams ciclistes i superfícies de panells observables. Es manté l’esquema i es justifica qualsevol adaptació de la unitat d’observació. Si un tipus d’element no es pot identificar, s’ha de documentar la limitació i acordar un sector adequat; copiar els objectes de Vila-seca no resol aquella absència.

Un conjunt sintètic proporcionat per estudiar topologia o buffers es conserva separat de l’inventari propi. Els resultats d’aquell conjunt només descriuen l’escenari geomètric construït.

# Fitxers i evidències

La composició cartogràfica mostra el sector de captura, les tres geometries amb símbols llegibles i les fonts. Cal distingir-hi observacions, interpretacions i exemples sintètics. Es desa al projecte i s’exporta com `pr2-digitalitzacio-cognom-mapa.pdf` per comprovar la lectura a mida final.

Es desen les edicions, el projecte incrustat `pr2` i un `.qgz` nou `pr2-digitalitzacio-cognom.qgz`, amb fonts relatives cap al GeoPackage homònim. Cal comprovar també les altres vistes incrustades que es mantinguin. Després de tancar QGIS i estabilitzar la base, es prepara la còpia de `dist/` i es reobre des d’una ubicació neta.

Es conserven `pr2-digitalitzacio-cognom.gpkg`, `.qgz`, el mapa i `pr2-digitalitzacio-cognom-apunts.pdf`. Els apunts inclouen sector, fonts, esquema, configuració d’ajust amb unitats, exemples de captura, recomptes, incidències i controls. PR3 heretarà les tres capes, encara que les primeres consultes tractin altres dades.

# Ampliacions i qualificació

Es pot aprofundir en una pregunta addicional al treball seleccionat:

- **Dos inventaris del mateix tram:** comparar una mostra capturada independentment, relacionar objectes, posicions i atributs i separar omissions de desacords. Cal explicar com es resolen amb una font o observació de contrast.
- **Sensibilitat de l’ajust:** provar dues configuracions sobre còpies de les mateixes línies, comprovar nodes compartits i localitzar connexions indegudes. La tolerància porta unitats i no s’interpreta com a exactitud territorial.
- **Abast d’una restricció:** afegir una regla de domini, provar un valor admès i un de rebutjat i reobrir la taula fora del projecte. Cal distingir què controla QGIS i què protegeix el GeoPackage.

La qualificació és **70% treball bàsic, 20% ampliacions i 10% documentació**, fins a **7, 2 i 1 punts**. Es valoren els obligatoris correctes i comprovats, la pregunta i validació de l’ampliació i la claredat d’apunts, captures, mapa i organització. Els màxims no són automàtics; més entitats no impliquen més nota. Les ampliacions no substitueixen els obligatoris i la documentació té puntuació pròpia.

# Referències

- [Model vectorial i digitalització, manual TIG](https://geourv.github.io/tig/ca/chapters/model-vectorial-digitalitzacio/).
- [Edició de geometries i atributs, QGIS 3.44](https://docs.qgis.org/3.44/en/docs/user_manual/working_with_vector/editing_geometry_attributes.html).
