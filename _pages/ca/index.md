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

L'objectiu del curs **no és memoritzar una col·lecció d'eines**. Es tracta d'entendre com es representa un problema territorial mitjançant dades, com condicionen el resultat el **model vectorial** i el **model ràster**, quines operacions permeten respondre una pregunta i com es comprova que el procés és coherent. QGIS serà l'eina principal de les pràctiques, però els conceptes, els criteris i les operacions formen part del treball amb sistemes d'informació geogràfica en un sentit més ampli.

>>>>> En acabar aquest capítol, cal poder situar el paper del manual dins del curs i identificar com s'organitzen el treball, els dubtes i l'avaluació.
>>>>>
>>>>> - Explicar la relació entre teoria, pràctica i projecte acumulatiu.
>>>>> - Distingir quina informació correspon al manual, a Moodle i a la guia docent.
>>>>> - Formular un dubte tècnic amb prou informació per poder-lo reproduir.
>>>>> - Identificar les condicions generals de l'avaluació i de la recuperació.

El manual desenvolupa més exemples i activitats que els exigits per superar l'assignatura. Aquesta amplitud permet practicar una mateixa idea en contextos diferents, recuperar conceptes previs i explorar extensions com les consultes espacials, les tessel·les, els models de processament, SQL o PyQGIS. Les activitats lliurables estaran identificades de manera explícita; la resta serviran per preparar les sessions, comprovar la comprensió o ampliar el recorregut.

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

Les tecnologies de la informació geogràfica permeten capturar, organitzar, consultar, analitzar i comunicar informació vinculada al territori. En aquest curs s'aprofundirà en aquestes funcions a partir de preguntes que obliguen a relacionar la naturalesa de les dades amb les operacions aplicades. Caldrà decidir, per exemple, com es representa una xarxa de carrils bici, què significa cada columna d'una capa del CNIG, quin sistema de referència de coordenades (`CRS`) permet mesurar una distància o com canvia una estimació d'altitud quan varia la resolució d'un model digital d'elevacions.

L'assignatura continua coneixements introduïts anteriorment a Tècniques d'Informació Geogràfica i Turística. Es pressuposa una primera experiència amb fitxers, taules, capes, sistemes de coordenades, simbolització i composició cartogràfica. Aquests coneixements es recuperaran quan siguin necessaris, però ara s'utilitzaran per construir processos més complets, documentats i reproduïbles.

El treball pràctic seguirà un **projecte acumulatiu aplicat a un municipi**. Vila-seca i l'entorn de la Facultat serviran sovint com a demostració comuna perquè permeten relacionar les dades amb llocs recognoscibles. Els fanals del carrer de Joanot Martorell, els carrils bici, les edificacions, les plaques solars o els models d'elevacions poden convertir-se en geometries, atributs i criteris d'anàlisi. **El cas demostrat no substitueix l'aplicació al municipi de treball** i a les fonts que hi estiguin disponibles.

::: table "Fases del projecte acumulatiu"
| Fase | Pregunta principal | Resultat que es conserva |
| --- | --- | --- |
| Projecte i fonts | Quines dades permeten estudiar el municipi i amb quines condicions? | GeoPackage inicial, projecte QGIS i registre de fonts |
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

El projecte del curs es conservarà progressivament en un **GeoPackage acumulatiu**. També es mantindrà un projecte QGIS dins del GeoPackage i una còpia independent en format `.qgz`, d'acord amb les instruccions de cada activitat. El **diari d'activitats** documentarà les fonts, els passos, les eines, els paràmetres, les incidències, les decisions i els resultats. Les captures de pantalla s'hi incorporaran quan ajudin a demostrar una configuració, un error o una comprovació, no per reproduir cada clic.

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

Cal localitzar la guia docent vigent, l'espai Moodle de l'assignatura i el fòrum de dubtes. Per a cadascun, s'ha d'identificar una informació que només correspongui a aquell espai i explicar per què no convé buscar-la als altres dos.

### Preparar una consulta reproduïble

Es redactarà una consulta breu a partir d'una incidència real o hipotètica de QGIS. La consulta haurà d'indicar l'objectiu, les dades implicades, els passos seguits, el resultat esperat i el resultat obtingut. Si l'error depèn d'un CRS, un camp, una ruta o un paràmetre, aquesta informació haurà d'aparèixer explícitament.

### Anticipar el projecte municipal

Un cop assignat o seleccionat el municipi de treball, caldrà identificar una pregunta vectorial i una pregunta ràster que es podrien estudiar durant el curs. En aquesta activitat inicial no s'ha de resoldre l'anàlisi: només cal explicar quines dades serien necessàries, quin organisme podria proporcionar-les i quin resultat permetria respondre cada pregunta.
