---
layout: manual-home
title: Tecnologies de la Informació Geogràfica
description: Manual de teoria aplicada, pràctiques i criteris per analitzar informació territorial amb sistemes d'informació geogràfica.
lang: ca
ref: home
profiles: [unaltremanual]
content_status: draft
permalink: /ca/
nav: false
show_chapter_index: true
figure_captions: true
manual_references: false
---

Aquest manual forma part de l'assignatura **Tecnologies de la Informació Geogràfica**, del segon curs del Grau en Geografia, Anàlisi Territorial i Sostenibilitat de la Universitat Rovira i Virgili. L'assignatura és obligatòria, té una càrrega de 4 ECTS i es desenvolupa durant el primer quadrimestre. La [guia docent del curs 2026–27](https://guiadocent.urv.cat/docnet/guia_docent/index.php?centre=21&ensenyament=2123&assignatura=21234114&any_academic=2026_27) n'estableix els resultats d'aprenentatge, els continguts, les metodologies i les condicions generals d'avaluació.

L'objectiu del curs **no és memoritzar una col·lecció d'eines**. Es tracta d'entendre com es representa un problema territorial mitjançant dades, com condicionen el resultat el **model vectorial** i el **model ràster**, quines operacions permeten respondre una pregunta i com es comprova que el procés és coherent. [QGIS](https://qgis.org/) és una aplicació lliure i multiplataforma de sistema d'informació geogràfica (SIG) i serà l'eina principal de les pràctiques. El programa permet organitzar, representar, consultar i transformar dades geogràfiques, però els conceptes, els criteris i les operacions no depenen del nom d'un botó ni d'una aplicació concreta.

>>>>> En acabar aquest capítol, cal poder situar el paper del manual dins del curs i identificar com s'organitzen el treball, els dubtes i l'avaluació.
>>>>>
>>>>> - Explicar la relació entre teoria, pràctica i projecte acumulatiu.
>>>>> - Distingir quina informació correspon al manual, a Moodle i a la guia docent.
>>>>> - Formular un dubte tècnic amb prou informació per poder-lo reproduir.
>>>>> - Identificar les condicions generals de l'avaluació i de la recuperació.

El manual desenvolupa més exemples i activitats que els exigits per superar l'assignatura. Aquesta amplitud permet practicar una mateixa idea en contextos diferents, recuperar conceptes previs i explorar extensions com les consultes espacials, les tessel·les de mapes web, els models de processament, el llenguatge de consulta SQL o la interfície de programació de QGIS amb Python, anomenada PyQGIS. Les activitats lliurables estaran identificades de manera explícita; la resta serviran per preparar les sessions, comprovar la comprensió o ampliar el recorregut.

::: table "Dades identificatives de l'assignatura"
| Camp | Valor |
| --- | --- |
| Assignatura | Tecnologies de la Informació Geogràfica |
| Codi | `21234114` |
| Ensenyament | Grau en Geografia, Anàlisi Territorial i Sostenibilitat |
| Curs i període | Segon curs, primer quadrimestre |
| Caràcter | Obligatòria |
| Crèdits | 4 ECTS |
| Guia docent | [Curs 2026–27](https://guiadocent.urv.cat/docnet/guia_docent/index.php?centre=21&ensenyament=2123&assignatura=21234114&any_academic=2026_27) |
:::

## Què s'aprendrà durant el curs

Les tecnologies de la informació geogràfica permeten capturar, organitzar, consultar, analitzar i comunicar informació vinculada al territori. En aquest curs s'aprofundirà en aquestes funcions a partir de preguntes que obliguen a relacionar la naturalesa de les dades amb les operacions aplicades. Caldrà decidir, per exemple, com es representa una xarxa de carrils bici, què significa cada columna d'una capa distribuïda pel Centro Nacional de Información Geográfica (CNIG), quin sistema de referència de coordenades (`CRS`) permet mesurar una distància o com canvia una estimació d'altitud quan varia la resolució d'un model digital d'elevacions.

L'assignatura continua el recorregut iniciat a [Tècniques d'Informació Geogràfica i Turística (TIGIT)](https://guiadocent.urv.cat/docnet/guia_docent/index.php?centre=21&ensenyament=2123&assignatura=21234003). És possible que ja resultin familiars l'obertura de capes vectorials i taules, les unions mitjançant un camp comú, la taula d'atributs, la simbologia temàtica i la preparació d'una composició cartogràfica. Aquesta experiència pot variar segons el curs i no es dona per consolidada. El manual recupera les nocions necessàries i explica des del principi les operacions essencials, inclosos els sistemes de referència, el geoprocessament i les dades ràster, de manera que també es pot seguir sense haver cursat TIGIT.

### Mapa de dependències conceptuals

El recorregut és acumulatiu: cada bloc aporta les decisions necessàries per entendre el següent. Aquesta seqüència funciona com un mapa de prerequisits i permet tornar al punt on s'ha originat un dubte, en lloc de tractar cada eina com una recepta aïllada.

::: table "Dependències entre els conceptes principals del curs"
| Punt de partida | Concepte que s'hi construeix | Què permet fer després |
| --- | --- | --- |
| Pregunta territorial i unitat d'observació | Evidència necessària, àmbit, període i mesura | Cercar i descartar fonts amb criteri |
| Font, producte, capa i via d'accés | Procedència, escala o resolució, llicència i aptitud d'ús | Organitzar entrades fiables dins d'un projecte |
| Projecte, capa configurada i font de dades | Dependències, rutes, formats i traçabilitat | Traslladar i reconstruir el treball |
| Model, estructura, format i `CRS` | Diferència entre entitats vectorials i cel·les ràster | Triar una representació i unes unitats coherents |
| Geometria, atributs, identificadors i topologia | Esquema vectorial i regles de qualitat | Digitalitzar, consultar i relacionar taules |
| Condicions lògiques, claus i relacions espacials | Seleccions, unions i correspondències comprovables | Construir geoprocessaments vectorials |
| Distància, superposició i àrea d'influència (`buffer`) | Geometries derivades i criteris d'inclusió o exclusió | Combinar condicions territorials i provar-ne la sensibilitat |
| Cel·la, banda, resolució i valor sense dades (`NoData`) | Graella ràster i significat dels valors | Calcular relleu, distàncies, reclassificacions i superposicions ràster |
| Procés manual validat i controls | Contracte d'un algorisme i graf de dependències | Repetir per lots, construir un model i, opcionalment, utilitzar SQL o PyQGIS |
:::

El treball pràctic construirà **un únic projecte QGIS acumulatiu aplicat al municipi assignat**. Començarà amb un servei web de mapes (WMS) com a fons visual i un límit municipal oficial del CNIG, i conservarà els resultats de cada fase per utilitzar-los en les següents. Vila-seca i l'entorn de la Facultat seran el cas de demostració a l'aula perquè permeten relacionar les dades amb llocs recognoscibles. Els fanals del carrer de Joanot Martorell, els carrils bici, les edificacions, les plaques solars o els models d'elevacions poden convertir-se en geometries, atributs i criteris d'anàlisi. **El cas demostrat no substitueix l'aplicació al municipi assignat** ni la comprovació de les fonts que hi estiguin disponibles.

::: table "Fases del projecte acumulatiu"
| Fase | Pregunta principal | Resultat que es conserva |
| --- | --- | --- |
| Projecte i fonts | Quines dades permeten estudiar el municipi i amb quines condicions? | Inventari de fonts, connexió WMS, límit municipal preparat, `projecte_tig.qgz` i primera fita incrustada al GeoPackage |
| Digitalització | Com es converteix una observació o una font visual en entitats fiables? | Capa pròpia amb geometries, atributs i controls topològics |
| Consultes | Quines entitats compleixen un criteri alfanumèric? | Expressions, seleccions, filtres i camps derivats comprovats |
| Anàlisi vectorial | Quines zones compleixen relacions de distància, contacte o superposició? | Capes intermèdies, resultat multicriteri i mesures interpretades |
| Anàlisi ràster | Com condicionen la resolució i les cel·les el resultat territorial? | Ràsters preparats, estadístiques i comparacions documentades |
| Síntesi final | Com es converteixen les anàlisis acumulades en un producte traçable i comunicable? | GeoPackage i projecte revisats, mapes exportats, diari complet i preparació de l'explicació oral |
:::

## Com es relacionen la teoria i la pràctica

**La teoria i la pràctica estudien el mateix problema des de dues perspectives complementàries.** La teoria explica què representa una dada, quins supòsits introdueix un model, com funciona una operació i quins errors poden invalidar-ne el resultat. La pràctica obliga a traslladar aquests criteris a capes concretes, paràmetres, noms de camps, distàncies, resolucions i fitxers de sortida.

Quan s'estudiï una àrea d'influència, per exemple, no n'hi haurà prou amb localitzar l'eina de buffer. Caldrà determinar què representa la distància, comprovar que el CRS utilitza unitats adequades, decidir si les geometries resultants s'han de dissoldre i validar que la superfície obtinguda correspon a la pregunta. La mateixa lògica s'aplicarà a una intersecció de dos buffers, a la connexió topològica d'una xarxa, a una unió d'atributs o al retall d'un ràster.

Els exemples es resoldran principalment amb QGIS, però el manual introduirà primer el model conceptual i el criteri de decisió. Aquesta separació permet reconèixer una mateixa operació en altres programes SIG i evita confondre el nom d'un botó amb el significat geogràfic del procediment.

## Com s'utilitzarà el manual

Cada capítol combina explicació conceptual, exemples, procediments, criteris de comprovació i activitats. Abans d'una sessió pràctica convé identificar la pregunta plantejada, les dades necessàries i el resultat esperat. Durant l'activitat, el manual servirà per consultar el perquè de cada operació i els controls que cal aplicar. En acabar, s'haurà de comprovar que els fitxers es tornen a obrir, que les fonts continuen disponibles i que el resultat es pot explicar sense dependre de la memòria de qui l'ha produït.

Tots els capítols de contingut acabaran amb activitats. Algunes seran preguntes de comprensió o exercicis breus; altres desenvoluparan una pràctica guiada, proposaran una aplicació al municipi propi o ampliaran el contingut. Només les activitats identificades com a **micropràctica lliurable** formaran part del treball continuat obligatori. Moodle publicarà l'enunciat vigent, el termini i les condicions concretes de cada lliurament.

La còpia de treball canònica serà el projecte extern **`projecte_tig.qgz`**. El GeoPackage acumulatiu contindrà les capes vectorials i les taules adequades i, en les fites indicades, una representació incrustada del projecte amb el nom **`projecte_tig`**. Totes dues representacions són independents: desar el `.qgz` no actualitza el projecte incrustat, ni desar o obrir el projecte incrustat modifica automàticament el `.qgz`. A cada fita es desarà primer la còpia canònica, s'actualitzarà expressament la representació incrustada i es provaran totes dues després de copiar l'arbre del projecte. El **diari d'activitats** documentarà les fonts, les operacions, els paràmetres, les incidències, les decisions, els controls i els resultats. Les captures de pantalla s'hi incorporaran quan ajudin a demostrar una configuració, un error o una comprovació, no per reproduir cada clic.

## Com es planteja un dubte

Els dubtes formen part del procés de treball i convé plantejar-los quan apareixen. Al començament de les sessions es podran comentar qüestions sorgides durant la lectura, la preparació de les dades o l'activitat anterior. Una dificultat compartida pot revelar un problema de concepte, de dades o de procediment que sigui útil discutir amb tot el grup.

Quan el dubte no quedi resolt a l'aula, el canal preferent serà el fòrum de Moodle. La pregunta i la resposta podran ajudar altres persones que es trobin amb la mateixa incidència. Si la consulta inclou informació individual o fitxers que no convé publicar, es podrà utilitzar el correu institucional i, si cal, acordar una tutoria.

**Una pregunta tècnica ha de permetre reconstruir el problema.** Un missatge com «no funciona» no identifica la causa ni el moment en què apareix. Una consulta útil ha d'incloure, segons el cas:

- l'objectiu que es vol assolir;
- la font i el nom de les capes implicades;
- la versió de QGIS i el sistema operatiu;
- el CRS de les entrades i del projecte;
- l'eina, els paràmetres i l'ordre dels passos;
- el resultat esperat i el resultat obtingut;
- el text exacte de l'error;
- una captura o un fragment del projecte que aporti informació diagnòstica.

Abans d'enviar la consulta cal tornar a llegir el missatge i comprovar que una altra persona podria localitzar la incidència. Aprendre a descriure un error amb precisió és també una competència de treball amb informació geogràfica.

## Manual, Moodle i guia docent

El curs distribueix la informació entre tres espais amb funcions diferents. Consultar l'espai adequat evita que una explicació conceptual es confongui amb una instrucció administrativa o que una data antiga prevalgui sobre l'enunciat vigent. L'accés als avisos, enunciats i lliuraments es farà mitjançant [Moodle URV](https://moodle.urv.cat/).

::: table "On es troba cada tipus d'informació"
| Espai | Funció |
| --- | --- |
| Manual | Teoria, exemples, procediments, activitats i criteris per comprovar els resultats |
| Moodle | Calendari, avisos, enunciats vigents, fitxers, lliuraments, accés a les proves i qualificacions |
| Guia docent | Resultats d'aprenentatge, continguts, metodologies i condicions oficials de l'assignatura |
:::

**La guia docent és la referència normativa.** Moodle concreta les dates, els enunciats i les instruccions operatives dins d'aquest marc. Si una indicació de Moodle sembla contradir un percentatge, un requisit o una condició d'avaluació de la guia docent vigent, cal demanar-ne l'aclariment al professorat; la guia docent preval mentre la discrepància no s'hagi corregit formalment.

## Avaluació i recuperació

L'avaluació combina el treball continuat amb una prova de continguts teòrics i conceptuals i una prova pràctica. Les tres parts valoren dimensions diferents: el seguiment d'un procés acumulatiu, la comprensió dels conceptes i la capacitat de resoldre un problema SIG de manera individual.

::: table "Blocs d'avaluació del curs 2026–27"
| Bloc | Pes | Evidència principal |
| --- | --- | --- |
| Treball continuat | 35% | Micropràctiques acumulatives aplicades al municipi de treball, amb GeoPackage i diari d'activitats |
| Continguts teòrics i conceptuals | 30% | Prova sobre els principals blocs conceptuals de l'assignatura |
| Prova pràctica | 35% | Resolució individual d'un cas amb gestió de dades, operacions vectorials i ràster, simbolització i interpretació |
:::

El manual organitza el treball continuat en sis micropràctiques que avancen des de la preparació de les fonts fins a la síntesi final del projecte municipal. Per superar l'assignatura, la qualificació final ponderada ha de ser igual o superior a 5 sobre 10 i cal assolir un nivell mínim suficient en els continguts teòrics i pràctics. **No es pot calcular la mitjana si alguna activitat o prova principal té una qualificació inferior a 4 sobre 10.** Moodle identificarà quins lliuraments i proves tenen caràcter principal o obligatori.

Per acollir-se a l'avaluació continuada cal seguir regularment les sessions i lliurar les micropràctiques, evidències o versions intermèdies indicades a Moodle. Cal assistir almenys al 80% de les sessions pràctiques presencials o justificar adequadament les absències. La manca de seguiment pot afectar l'avaluació del treball continuat perquè una part del procés es desenvolupa i es verifica durant les sessions.

La prova de continguts teòrics i conceptuals tractarà els principals blocs del curs. Les instruccions publicades per a cada convocatòria concretaran el format, la durada, el canal de realització i els materials permesos.

La prova pràctica plantejarà un problema integrador semblant als treballats durant el curs. Podrà exigir gestionar capes i taules, comprovar sistemes de referència, construir consultes, derivar geometries, combinar criteris vectorials, tractar dades ràster, calcular estadístiques zonals, simbolitzar i interpretar els resultats. Les instruccions de la convocatòria indicaran les condicions concretes de realització i els materials permesos.

En segona convocatòria caldrà recuperar les activitats, proves o blocs no superats d'acord amb les indicacions publicades a Moodle. Les qualificacions de les parts aprovades es conservaran quan permetin verificar adequadament els resultats d'aprenentatge corresponents. Si el treball continuat no s'ha superat, es podrà exigir completar, corregir o tornar a lliurar el GeoPackage, el diari i els resultats derivats que s'indiquin.

Els lliuraments han de permetre verificar l'autoria i reconstruir el procés. El professorat podrà demanar una defensa oral presencial o en línia, fitxers intermedis o altres evidències per aclarir el procediment i concretar la qualificació del treball. Quan una activitat admeti l'ús d'eines d'intel·ligència artificial generativa, aquest ús s'haurà de declarar d'acord amb les instruccions de Moodle i no podrà substituir la realització, comprovació i explicació del treball propi.

## Activitats

### Reconèixer els espais del curs

El resultat conservat serà una fitxa breu amb l'enllaç a la guia docent vigent, l'espai Moodle de l'assignatura i el fòrum de dubtes. Per a cadascun, la fitxa identificarà una informació que només correspongui a aquell espai i explicarà per què no convé buscar-la als altres dos.

### Preparar una consulta reproduïble

El resultat conservat serà una consulta breu i reproduïble sobre una incidència real o hipotètica de QGIS. Inclourà l'objectiu, les dades implicades, els passos seguits, el resultat esperat i el resultat obtingut. Si l'error depèn d'un CRS, un camp, una ruta o un paràmetre, aquesta informació hi apareixerà explícitament.

### Anticipar el projecte municipal

Un cop assignat el municipi de treball, el diari conservarà una pregunta vectorial i una pregunta ràster que es puguin estudiar durant el curs. Per a cadascuna s'hi registraran les dades necessàries, l'organisme que podria proporcionar-les i el resultat observable que permetria respondre-la. Aquesta activitat inicial no resol l'anàlisi ni dona per verificada cap font.
