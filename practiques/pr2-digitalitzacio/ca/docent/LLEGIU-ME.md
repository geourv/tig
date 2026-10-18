---
title: "PR2 · Guia docent de la captura i la topologia d’edició"
lang: ca
recipient: docent
content_status: approved
subject: "Tecnologies de la Informació Geogràfica"
subject_code: "21234114"
author: "Benito Zaragozí"
institution: "Universitat Rovira i Virgili"
---

# Finalitat i resultats d’aprenentatge

La pràctica relaciona model conceptual, esquema i captura. La demostració ha de justificar per què un fanal es representa amb un punt, un carril amb una línia i una superfície de panells amb un polígon. L’ajust facilita la captura de coincidències, però no decideix quins objectes estan connectats ni valida la interpretació territorial.

Les tres capes són resultats persistents de PR2 i entrades heretades de PR3–PR4. En particular, `fanals` conserva `id_fanal`: el recompte de generadors dels buffers posteriors dependrà d’aquesta identitat, no dels FID de sortida.

# Preparació i conducció de la sessió

| Component | Durada orientativa |
| --- | --- |
| Aula, esquemes i captura guiada | 120–150 min |
| Treball autònom i apunts | 120–180 min |
| Preparació docent | 30–45 min |

Table: Estimació de PR2 per a un sector reduït amb tres tipus de geometria.

Estimació pendent de contrast amb alumnat, amb PR1 validada i sector localitzat. La visita de camp i els desplaçaments s’han de planificar separadament; la manca d’una font adequada pot obligar a canviar de sector. La quantitat d’objectes es fixa segons l’àmbit observable, no segons el joc sintètic.

La preparació comprova la PR1, el detall real de PNOA i un exemple d’objecte inequívoc i un d’ambigu. A classe es valida primer una entitat de cada tipus abans d’ampliar la captura. Les aturades són esquema i dominis, connexions després de desar i reobertura del conjunt. Convé preguntar què demostra una geometria vàlida i què queda per contrastar al terreny; una revisió entre parelles pot detectar diferències de criteri.

# Preparar Moodle

1. Crear una **Tasca** anomenada **PR2 · Digitalització i control de qualitat**.
2. Copiar l’enunciat següent a **Descripció**, fins al final de «Qualificació». Concretar el sector, les activitats obligatòries i el criteri de revisió anunciat a classe, preservant els tres esquemes de continuïtat.
3. Adjuntar a **Fitxers addicionals** el PDF d’alumnat. Si es comparteix l’exemple sintètic, identificar-ne la funció de demostració i conservar-ne els marcadors de procedència.
4. Configurar dates, tramesa del conjunt complet i mida suficient; establir màxim 10 i blocs 7/2/1. La planificació indica quan es fa el contrast de camp.
5. Revisar la **vista d’estudiant** i els adjunts. El paquet docent es conserva per preparar esquemes, controls i demostració.

## Enunciat per copiar a la descripció

**Dades i objectiu.** Cal continuar la PR1 pròpia i capturar fanals, carrils bici i plaques solars en un sector del municipi escollit. La base procedeix del CNIG i el context, d’IGN/PNOA; les observacions de camp o altres contrastos es documenten. La font ha de permetre reconèixer els objectes amb el detall necessari.

**Treball bàsic —70%.** El professor indica a classe i recull en aquesta Tasca els apartats obligatoris de disseny d’esquemes, captura, ajust i control. Cal conservar els tres tipus de capa, IDs estables, procedència i estat de revisió, amb les dades heretades de PR1. Es comproven dominis, geometries i nodes previstos; un objecte no identificable es registra com a incidència. La guia completa no converteix totes les variants de captura en requisits.

**Ampliacions —20%.** Es pot aprofundir en una pregunta que no estigui ja inclosa en els obligatoris:

- Fins a quin punt coincideixen dos inventaris independents del mateix tram? Comparar IDs, posicions i atributs sobre una mostra delimitada, distingir omissions de desacords i explicar la font usada per resoldre’ls.
- Quina tolerància d’ajust evita microbuits sense unir trams que no corresponen? Provar dues configuracions sobre còpies del mateix cas, comprovar coordenades compartides i localitzar falses connexions. No modificar l’inventari de referència durant la prova.
- Què protegeix realment un formulari de captura? Afegir una regla de domini o restricció, provar un valor admès i un de rebutjat i reobrir la taula fora del projecte per comprovar l’abast del mecanisme.

**Documentació i lliurament —10%.** La base és `pr2-digitalitzacio-cognom`: GeoPackage amb principal `pr2`, `.qgz`, mapa i apunts PDF. Cal explicar unitats d’observació, fonts, ajust amb unitats, recomptes, incidències i controls. Les captures mostren decisions i correccions; el mapa diferencia observacions, interpretacions i dades sintètiques. El conjunt es prova en una carpeta nova.

**Qualificació.** Fins a **7 punts** pels apartats bàsics seleccionats, correctes i comprovats; **2 punts** per una ampliació amb pregunta, referència i interpretació; **1 punt** per apunts, captures, mapa i organització. Els punts són màxims, no una recompensa per quantitat d’entitats. Les ampliacions no substitueixen els obligatoris; la documentació també pot augmentar la nota sobre el bloc bàsic.

# Punt de partida i dades

El cas de classe se situa a Joanot Martorell i a l’entorn de la Facultat, sobre la base municipal CNIG i el context oficial IGN/PNOA, amb observacions contrastables. Cal comprovar data i detall de la imatge i delimitar el tram i la unitat dels polígons. Cada estudiant parteix de la seva PR1 i crea els esquemes de captura; les fonts locals es reorienten al nou GeoPackage.

Existeix un exemple d’esquemes amb **3 punts, 3 trams i 2 polígons**, però les seves geometries són sintètiques. Els camps `font`, `observacio` i `estat_rev=no_apte_per_analisi` ho declaren. No és un inventari dels fanals ni una digitalització observada de les plaques de la Facultat.

Aquest exemple permet demostrar restriccions, ajust i reobertura. Si s’utilitza per estudiar solapaments a PR4, es presenta com un escenari sintètic separat. Una solució territorial docent requereix les observacions de classe i la seva revisió; no es crea substituint el marcador de qualitat de l’exemple.

El projecte de referència conserva els tres punts, tres línies i dos polígons amb els atributs originals, sobre el límit CNIG. El context PNOA local té aproximadament **6,59 m per píxel**: situa l’exemple i permet obrir-lo sense xarxa, però no té el detall necessari per digitalitzar peus de fanal o vores de panells. La captura territorial es fa amb una font adequada i contrast de camp quan calgui.

# Procediment de demostració

## Fixar la unitat i l’esquema

| Capa | Camps específics | Camps de procedència i revisió |
| --- | --- | --- |
| `fanals`, punt | `id_fanal`, `tipus`, `estat`, `data_obs` | `font`, `observacio`, `estat_rev` |
| `carrils_bici`, línia | `id_tram`, `tipus`, `continu`, `data_font` | `font`, `observacio`, `estat_rev` |
| `plaques_solars`, polígon | `id_placa`, `tipus`, `estat`, `data_obs` | `font`, `observacio`, `estat_rev` |

Table: Esquema de referència que es manté durant la transferència.

Els IDs són text únic, estable i no nul; les dates són dates i `continu` és enter amb domini 0/1/nul documentat. Els altres dominis s’expliquen abans de capturar. Un valor predeterminat de procedència pot agilitzar el lot; un estat operatiu predeterminat podria inventar una observació.

Convé provar la inserció d’un ID repetit i d’un valor incompatible amb el domini, i reobrir la capa fora del projecte per comprovar l’abast de les restriccions. El giny de QGIS i una restricció de SQLite no són mecanismes equivalents.

## Diferenciar captura, ajust i topologia

La captura puntual comença per la convenció del peu del suport i per un cas ambigu. Cal explicar què s’ha observat, què s’ha inferit i què queda desconegut. Una base ocultada no es resol situant un punt sobre l’ombra.

La captura lineal mostra tres situacions: un extrem que ha de connectar, un objecte pròxim que no és una destinació d’ajust i una connexió sobre un segment que exigeix un node. L’exemple històric configura ajust a vèrtexs sobre `carrils_bici` amb 10 píxels; és un valor d’interacció per provar, no una tolerància territorial universal.

Després de desar, cal comprovar les coordenades compartides. El ressaltat d’ajust durant el clic és evidència de la interacció, no una prova suficient de la xarxa final. El traçat reutilitza un recorregut i l’edició topològica ajuda a mantenir coincidències; cap dels dos inventa una connectivitat funcional.

La captura poligonal distingeix panell, agrupació contínua i instal·lació. Es fixa una unitat abans del primer anell i es manté. Un polígon rectangular ideal pot il·lustrar l’eina, però no es presenta com a contorn observat de la coberta.

## Revisar i persistir

La demostració separa desar les edicions, desar `pr2` incrustat i crear el `.qgz` extern homònim. Les capes locals apunten al contenidor de PR2. Les vistes incrustades heretades només es mantenen si se n’han revisat les fonts.

Amb QGIS tancat, es comprova l’estat estable del GeoPackage i se’n reobre una còpia en una ruta nova. No s’elimina un journal o un WAL per fer veure que el fitxer està llest. Una inspecció amb l’original disponible no acredita la independència de la còpia.

# Comprovacions i interpretació

| Dimensió | Prova docent | Resultat que no acredita per si sola |
| --- | --- | --- |
| Esquema | Tipus, dominis, nuls i unicitat | Veracitat de l’atribut observat |
| Geometria | Tipus correcte, no buida i vàlida | Posició correcta al terreny |
| Topologia | Nodes esperats compartits i excepcions documentades | Connectivitat funcional de qualsevol encreuament |
| Procedència | Font, data i mètode per lot o entitat | Exactitud més gran que la font |
| Persistència | Reobertura amb les capes i recomptes esperats | Funcionament d’un WMS sense xarxa |

Table: Controls complementaris de PR2.

No s’imposa el recompte 3/3/2 del joc sintètic com a resultat de Joanot Martorell o de l’altre municipi. El recompte esperat d’un inventari real ha de provenir de l’àmbit i de les observacions revisades. Les incidències es documenten amb entitat, causa, correcció o limitació conservada.

# Aplicació al municipi escollit

La transferència exigeix el mateix esquema i criteri de captura, amb adaptacions justificades del sector. La revisió ha d’incloure almenys un exemple ben identificat i un cas que hagi requerit contrast o correcció. L’absència real d’un tipus d’element s’ha de distingir d’una cerca incompleta o d’una font inadequada.

Els mapes i apunts han de separar dades observades, interpretades i sintètiques. Un estat `revisat` descriu el control aplicat i no converteix una interpretació d’ortofoto en una observació de camp.

# Fitxers i evidències

La instantània és `pr2-digitalitzacio-cognom.gpkg`, amb principal `pr2` i `.qgz` homònim. La composició i el PDF cartogràfic mostren el sector, les tres geometries i el seu estat de revisió.

Els apunts es desen com `pr2-digitalitzacio-cognom-apunts.pdf`. L’inventari de tancament registra capes heretades, noves capes, recomptes i IDs; servirà per comprovar que PR3 no perd la digitalització.

El PDF guia l’alumnat en la creació dels esquemes i la captura sobre la seva base. El paquet docent conserva originals, procedència, esquemes, dades de demostració, projecte i mapa. El cas sintètic compartit s’identifica com a exemple per estudiar l’edició i els controls; l’inventari territorial requereix observacions revisades.

# Referències

- [Model vectorial i digitalització, manual TIG](https://geourv.github.io/tig/ca/chapters/model-vectorial-digitalitzacio/).
- [Edició de geometries i atributs, QGIS 3.44](https://docs.qgis.org/3.44/en/docs/user_manual/working_with_vector/editing_geometry_attributes.html).
