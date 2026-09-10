---
layout: manual-chapter
title: Síntesi, processament i automatització
description: Tancament del projecte municipal amb Processament de QGIS, execució per lots i construcció i validació d'un model; SQL, PostGIS i PyQGIS com a ampliació opcional.
lang: ca
ref: manual-processing-automation
profiles: [unaltremanual]
content_status: draft
permalink: /ca/chapters/processament-automatitzacio/
weight: 90
part: Continguts
manual_references: true
---

El tram final del projecte converteix els resultats acumulats en un producte coherent i revisable. Cal ordenar el GeoPackage, netejar el projecte QGIS, comprovar les dependències, preparar la simbolització i les composicions necessàries, exportar els resultats i explicar-ne les limitacions abans de donar el treball per acabat. Tancar no significa amagar el procés: significa separar allò que respon la pregunta d'allò que només ha servit per explorar, i conservar prou evidència per reconstruir les decisions.

Executar una eina una vegada resol una operació; construir un flux permet repetir-la, revisar-la i aplicar-la a un altre territori. L'automatització no consisteix només a estalviar clics. Obliga a convertir decisions implícites en entrades, paràmetres, dependències, sortides i controls, però només té sentit després d'haver validat el procés. Un error automatitzat continua sent un error i pot afectar moltes més sortides abans de ser detectat.

>>>>> En acabar el capítol, cal poder tancar el projecte municipal, executar manualment i per lots un procés de QGIS i construir i validar un model parametritzat, auditable i transferible.
>>>>>
>>>>> - Organitzar el GeoPackage, el projecte QGIS, els mapes, les exportacions i el diari com un producte final coherent.
>>>>> - Interpretar un algorisme a partir d'entrades, precondicions, paràmetres, context, destinacions, resultats i controls.
>>>>> - Utilitzar l'historial i el processament per lots per repetir un contracte validat amb paràmetres i destinacions diferents.
>>>>> - Construir, desar i validar un model QGIS `.model3`; situar SQL, PostGIS i PyQGIS exclusivament com a ampliacions opcionals.
>>>>> - Auditar i transportar el projecte, documentar-ne procedència i limitacions i preparar-ne l'explicació oral.

## Processament i automatització amb QGIS

El marc de **Processament de QGIS** ofereix una interfície comuna per als algorismes natius i per a proveïdors com GDAL. Interpretar-ne el contracte, validar una execució manual, comparar distàncies mitjançant un lot i construir i validar un model al Dissenyador formen el recorregut obligatori del capítol. L'historial, el processament per lots i el graf del model representen graus diferents de formalització, però el criteri geogràfic continua sent independent de la interfície {% cite qgisUserGuide344 rouaultGDAL2026 %}. SQL, PostGIS i PyQGIS es reserven per a l'ampliació opcional situada al final de les activitats.

### Reproductibilitat no és automatització

Procés repetible
: Es pot tornar a executar en el mateix entorn amb les mateixes entrades i decisions.

Procés reproduïble
: Una altra persona el pot reconstruir en una ubicació o un equip diferent i obtenir un resultat analíticament equivalent.

Automatització
: Delegació d'una seqüència d'operacions a un lot, un model o un programa.

La terminologia varia entre disciplines, però el criteri operatiu del curs és clar: les fonts es resolen, els paràmetres es coneixen, les dependències estan identificades i els controls tornen a complir-se. Automatitzar pot reforçar la reproductibilitat perquè explicita l'ordre i redueix variacions manuals, però no la garanteix. Un script amb una ruta personal, una consulta dependent d'una taula mutable o un model que utilitza una selecció no documentada continuen sent fràgils. A l'inrevés, una seqüència manual pot ser reproduïble si està descrita amb precisió.

::: table "Formalització d'un procés i allò que conserva"
| Modalitat | Què fa explícit | Què pot continuar ocult | Ús adequat |
| --- | --- | --- | --- |
| Seqüència manual documentada | Decisions, ordre i controls descrits al diari | Clics accidentals, estat de la interfície o valors predeterminats no anotats | Aprendre, explorar i validar un cas inicial |
| Historial | Algorisme, paràmetres executats i missatges | Justificació, versió immutable de les entrades i part de l'estat del projecte | Reconstruir i diagnosticar execucions recents |
| Lot | Repetició del mateix contracte sobre diverses files | Dependències entre algorismes i validació global | Variar entrades o un paràmetre d'una sola operació |
| Model gràfic | Dependències i transformacions d'una seqüència | Fonts externes, entorn, supòsits i controls no representats | Reexecutar un flux estable i visualment inspeccionable |
| SQL tabular o espacial (ampliació opcional) | Filtres, relacions, agregacions i transformacions declaratives sobre dades de base | Preparació externa, dialecte, extensions i estat de la base | Consultes de conjunt i processos propers a les dades |
| PyQGIS (ampliació opcional) | Paràmetres, lògica, bucles i controls programables | Entorn QGIS, paquets, dades i decisions mal documentades | Fluxos dinàmics, comprovacions i integració avançada |
:::

![Flux reproduïble que relaciona entrades, paràmetres i entorn amb el procés, les sortides, els registres, els controls i la repetició correctiva]({{ site.baseurl }}/assets/diagrams/ca/08-processament-automatitzacio/reproducible-processing.mmd "De la pregunta i les fonts documentades es passa a explicitar entrades, paràmetres, entorn i procés; els resultats i registres se sotmeten a controls i, si fallen, es corregeix i es repeteix. Automatitzar aquest circuit no en garanteix la correcció."){: data-figure-width-web="49rem" data-figure-width-pdf="100%"}

La modalitat més formal no és sempre la més adequada. Automatitzar una operació que només s'executarà una vegada, encara s'està explorant i canvia a cada prova pot costar més que documentar-la bé. En canvi, repetir trenta retalls amb la mateixa regla justifica un lot, i encadenar preparació, retall, derivació i resum justifica un model. La decisió s'ha de basar en estabilitat, repetició, risc d'error i necessitat d'auditoria, no en la impressió que programar sempre és més avançat.

### Processament de QGIS i contracte d'algorisme

La caixa d'eines de Processament reuneix algorismes de proveïdors diferents sota una interfície semblant. Un algorisme natiu de QGIS, un programa de GDAL i una eina aportada per un complement poden tenir noms pròxims però comportaments, paràmetres i requisits diferents. El **proveïdor** i l'**identificador**, com `native:buffer`, formen part del mètode. El nom traduït i la posició dins del menú ajuden a localitzar l'eina, però poden canviar amb l'idioma o la versió.

Un algorisme es pot descriure amb una estructura general:

::: listing "Contracte general d'un algorisme de processament"
```text
identificador + entrades + precondicions + paràmetres + context + destinacions
  -> resultats + missatges + controls
```
:::

Entrades
: Capes, taules, bandes, camps, expressions o valors que consumeix l'algorisme.

Precondicions
: Requisits que s'han de complir abans de començar, com el tipus geomètric, els camps, els identificadors, el `CRS`, les unitats, la resolució o la validesa.

Paràmetres
: Decisions que defineixen l'operació, com una distància, un predicat, un llindar, una extensió o un mètode de remostreig.

Context
: Transformacions, variables, tractament de geometries invàlides, seleccions, entorn temporal i altres configuracions que poden alterar el resultat.

Destinacions
: Format, fitxer o taula, nom de capa i persistència de cada sortida.

::: table "Elements que cal fixar en un contracte de processament"
| Element | Exemple | Pregunta de control |
| --- | --- | --- |
| Proveïdor i identificador | `native:buffer` | S'ha utilitzat exactament l'algorisme previst? |
| Entrada | Capa preparada `vies_principals` del GeoPackage, amb una fila per segment | És la capa, la versió i el subconjunt correctes? |
| Esquema | Camp preparat `id_tram` únic, no nul i estable; `codi_muni` de text pot repetir-se | Es pot seguir cada segment després del procés sense tractar el municipi com una clau de tram? |
| Referència espacial | `EPSG:25831`, metres | El `CRS` és realment el de la capa i és adequat per a la mesura? |
| Paràmetre | `distancia_m = 200` | La unitat i la justificació són explícites? |
| Estat | Sense selecció; filtre documentat | L'entrada completa és la que s'ha volgut processar? |
| Destinació | `projecte_tig.gpkg`, capa `vies_buffer_200m` | El nom és únic i la sortida és persistent? |
| Postcondició | Àrea dissolta no superior a la suma individual | Quin resultat faria fallar la validació? |
:::

>>> **Contracte complet d'un buffer.** Dir només «fer un buffer de 200 m» no basta. En QGIS 3.44, una execució persistent de `native:buffer` sobre línies ha de fixar almenys `INPUT = vies_principals`, `DISTANCE = 200`, `SEGMENTS = 10`, `END_CAP_STYLE = Round`, `JOIN_STYLE = Round`, `MITER_LIMIT = 2`, `DISSOLVE = True` i `SEPARATE_DISJOINT = False`. `OUTPUT` ha d'identificar tant el fitxer `dades_preparades/projecte_tig.gpkg` com el nom intern `vies_buffer_200m`. Els noms dels estils són els de la interfície; en una crida programada s'han de conservar també els codis enumerats corresponents.

Abans del buffer cal exigir un `CRS` projectat en metres, geometries aptes, cap selecció imprevista i un identificador estable per segment. `codi_muni` agrupa potencialment molts segments i, per tant, no és una clau única de la xarxa. El nom `id_tram` designa el camp verificat o creat a la capa preparada del projecte; no pressuposa cap nom físic concret a la descàrrega original. Després cal comprovar que la sortida és vàlida, no és buida i té una àrea no superior a la suma dels buffers individuals equivalents.

Els valors predeterminats també són paràmetres. Acceptar els segments d'un `buffer`, el tractament de geometries invàlides o la resolució suggerida per una eina és una decisió, encara que no s'hagi escrit res al quadre. Si el valor afecta el resultat, s'ha de registrar. Un model que confia en el predeterminat d'una versió pot canviar de comportament quan el proveïdor actualitza l'algorisme.

El `CRS` del projecte és principalment una configuració de visualització. Un algorisme pot treballar en el `CRS` de l'entrada, demanar-ne un de sortida o aplicar regles pròpies del proveïdor. Cada flux ha de fer explícites les unitats i les transformacions en lloc de confiar que el llenç mostra les capes alineades. El mateix criteri s'aplica als ràsters: compartir `CRS` no implica compartir origen, extensió ni cel·les.

Una selecció activa, un filtre de capa, una edició encara no desada, una variable de projecte, una relació temporal o una capa de memòria també formen part de l'estat. Si condicionen el resultat i no apareixen al contracte, la reexecució pot donar una sortida diferent sense cap error visible. Abans d'automatitzar convé materialitzar el subconjunt necessari o convertir el filtre en un paràmetre o pas explícit.

### Programació visual: QGIS i ArcGIS

Un diagrama de processament és un programa visual: les caixes representen entrades, paràmetres o algorismes, i les connexions indiquen quina sortida alimenta el pas següent. En un primer model municipal, `municipi_treball` i `distancia_m` alimenten `Buffer`, que produeix una regió d'interès (`ROI`). L'ordre d'execució no depèn de la posició esquerra-dreta de les caixes, sinó d'aquestes dependències.

En QGIS 3.44, el recorregut `Procés > Model Designer...` obre el **Dissenyador de models**. La pestanya `Entrades` defineix els valors que es demanaran en executar el model; `Toolbox` conté els algorismes; i el llenç mostra els nodes i les connexions. La captura situa aquestes regions abans de construir cap model i evita confondre el diagrama amb una capa o un mapa {% cite qgisUserGuide344 %}.

![Dissenyador de models de QGIS amb el panell d'entrades, el llenç de dependències i el botó d'execució identificats]({{ site.baseurl }}/assets/img/qgis/qgis-model-designer.png "En el Dissenyador de models, primer es defineixen les entrades, després s'afegeixen algorismes des de Toolbox i es connecten al llenç. El botó d'execució només s'utilitza quan el graf i els paràmetres ja s'han validat."){: data-figure-width-web="43rem" data-figure-width-pdf="90%"}

Per construir el cas mínim, s'afegeix una entrada de capa vectorial, una entrada numèrica descrita en metres i l'algorisme `native:buffer`; la capa i la distància es vinculen als paràmetres corresponents i la sortida del buffer es marca com a sortida del model. El fitxer `.model3` o el model desat al projecte conserva el graf, però no incorpora automàticament les fonts externes, la justificació de la distància ni els controls. Abans de reutilitzar-lo cal comparar-ne una execució amb el procediment manual conegut.

ArcGIS Pro ofereix el mateix paradigma amb **ModelBuilder**, que la seva [documentació oficial descriu com un llenguatge de programació visual](https://pro.arcgis.com/en/pro-app/latest/help/analysis/geoprocessing/modelbuilder/what-is-modelbuilder-.htm). Les variables i dades alimenten eines de geoprocessament, els connectors expressen dependències i el model es pot executar per passos o publicar com una eina. El concepte es transfereix entre QGIS i ArcGIS, però els formats, els identificadors d'algorisme, els paràmetres i els entorns no són interoperables: un model s'ha de reconstruir i validar al programa de destinació, no només copiar-ne el diagrama.

### Historial, registre i diagnòstic

L'**historial de processament** conserva les crides recents als algorismes, amb els paràmetres i una representació de l'ordre que es pot copiar o repetir. És especialment útil quan una sortida inesperada obliga a respondre si es va seleccionar una capa equivocada o si la distància era 200 o 2.000.

L'historial no conserva una còpia immutable de les entrades. Si `municipis_preparats` s'ha modificat després, repetir la mateixa ordre actua sobre l'estat actual. Tampoc explica per què es va triar un llindar ni demostra que s'hagi inspeccionat el resultat. Una entrada de l'historial pot dir que el procés va acabar sense excepció, però no que la capa tingui sentit territorial. Per això és una font per completar el diari, no un substitut del diari.

El panell **Registre de missatges** compleix una altra funció: reuneix avisos i errors emesos per QGIS i pels proveïdors durant la sessió, com geometries omeses, problemes de connexió o dependències absents. No és una recepta completa ni substitueix els paràmetres de l'historial. Per diagnosticar una execució cal relacionar tots dos registres amb la sortida i amb l'estat de les entrades.

Els missatges mereixen una lectura completa. Un avís sobre geometries omeses, un sistema de referència desconegut, una capa sense índex o una sortida parcial pot quedar amagat si només es comprova que ha aparegut una capa al panell. Cal diferenciar tres estats: execució completada i validada; execució completada amb avisos pendents; i execució fallida o parcial. Només el primer estat pot alimentar silenciosament el pas següent.

### Resultats temporals, intermedis i persistents

Els resultats temporals són útils per explorar i per connectar passos interns sense omplir el projecte de fitxers. Poden desaparèixer quan es tanca la sessió, quan es neteja l'espai temporal o quan el procés que els manté deixa d'estar disponible. No constitueixen una evidència durable ni una entrada segura per a un projecte que s'ha de transportar.

::: table "Funció de cada tipus de sortida"
| Tipus | Ús | Criteri de conservació |
| --- | --- | --- |
| Temporal | Prova o connexió interna entre passos | Es pot regenerar i no cal inspeccionar-la després de tancar el flux |
| Intermèdia de diagnòstic | Comprovar una transformació decisiva | Es conserva si permet localitzar un error o justificar una decisió |
| Intermèdia reutilitzable | Alimentar diverses branques costoses | Es conserva si regenerar-la és lent o depèn d'una font canviant |
| Final analítica | Respondre la pregunta o alimentar una decisió | Té nom, format, procedència, unitats i destinació explícits |
| Final documental | Taula de controls, mapa, registre o resum | Permet revisar i comunicar la conclusió |
:::

No s'han d'exposar totes les sortides d'un model. Massa resultats finals dificulten identificar quins tenen valor analític i augmenten el risc d'utilitzar una versió intermèdia. Alhora, ocultar l'única capa que permet comprovar un retall o una reclassificació fa que el flux sigui opac. La decisió s'ha de prendre segons la funció de cada pas i el cost de reconstruir-lo.

Les sortides persistents necessiten destinacions no ambigües. En un GeoPackage cal indicar tant el fitxer `.gpkg` com el nom de taula o capa. Reutilitzar un nom pot fallar, sobreescriure una capa o deixar una versió antiga segons el proveïdor i l'opció triada. Abans d'executar un lot o un model cal decidir si una sortida existent bloquejarà el procés, es reemplaçarà de manera controlada o rebrà un identificador diferent.

El GeoPackage és adequat per reunir vectors i taules amb integritat transaccional, però no converteix automàticament totes les escriptures simultànies en un procés segur. Diverses branques que intenten modificar el mateix contenidor poden trobar bloqueigs o noms en conflicte. Cal tancar edicions pendents, utilitzar noms únics i comprovar que totes les capes esperades existeixen després de l'execució. Els ràsters analítics continuaran habitualment en GeoTIFF, tal com estableix l'organització del projecte {% cite ogcGeoPackage2024 %}.

### Processament per lots

El **processament per lots** executa el mateix algorisme diverses vegades amb combinacions de paràmetres. Cada fila és una execució independent: pot canviar l'entrada, un camp, una distància o la destinació. És adequat per retallar una mateixa capa per diversos municipis, reprojectar una col·lecció de fitxers o generar tres escenaris de distància amb una regla idèntica.

Un lot no representa dependències entre algorismes. Si cada retall ha d'alimentar una intersecció i després una agregació, ja no n'hi ha prou amb files independents d'una sola eina. Es podria executar un lot per cada etapa, però la relació entre sortides i entrades quedaria repartida en diversos registres; un model gràfic o un script pot expressar millor el graf complet.

La primera fila s'ha de resoldre i validar manualment abans de llançar la resta. Aquesta prova confirma el tipus d'entrada, les unitats, el nom de sortida i els controls. Copiar trenta vegades un contracte erroni només multiplica l'error. També convé provar una fila que representi un cas límit, per exemple un municipi costaner amb `NoData`, un codi amb zero inicial o una geometria multipart.

Cada destinació ha de ser única i reconstruïble. Un patró com `municipi_<codi>_retall` és preferible a `output_1`, però el codi s'ha de normalitzar sense perdre zeros i s'han d'evitar caràcters que el format no admeti. Si dues files produeixen el mateix nom, el lot no ha de continuar confiant que el darrer resultat és el correcte. La comprovació prèvia de noms i col·lisions forma part del contracte.

Els lots poden acabar parcialment. Una fila pot fallar per una geometria invàlida o una ruta, mentre que les altres es completen. El recompte de fitxers no basta perquè també hi pot haver sortides buides. En acabar cal contrastar files previstes, files completades, files amb avisos, files fallides i resultats validats. Les fallades es corregiran a la causa i només es repetiran les files afectades, sense ocultar que hi va haver una primera execució.

La idea d'una taula **llarga** o de registres és útil per auditar el lot. Cada fila descriu una observació d'execució en lloc d'afegir una columna per a cada prova. Això permet comparar territoris, resolucions o distàncies sense mantenir capes amb esquemes incompatibles.

::: table "Registre mínim d'un lot"
| `execucio_id` | `entrada_id` | `parametre` | `sortida` | `estat` | `control` |
| --- | --- | --- | --- | --- | --- |
| `buf_001` | `vies_43171` | `200 m` | `vies_43171_buffer_200m` | `validat` | `area_m2` i entitats sense sortida |
| `buf_002` | `vies_43004` | `200 m` | `vies_43004_buffer_200m` | `pendent` | Missatge per revisar |
| `buf_003` | `vies_43123` | `500 m` | `vies_43123_buffer_500m` | `fallit` | Geometria d'entrada no acceptada |
:::

### Dissenyar i validar un model

El diagrama creat al Dissenyador és un **graf dirigit de dependències**. Les entrades i els paràmetres alimenten algorismes; les sortides d'uns passos es converteixen en entrades dels següents. L'ordre visual de les caixes no determina l'execució: les connexions ho fan. Dues branques independents es poden resoldre sense seguir l'ordre d'esquerra a dreta, mentre que un node no pot començar fins que les dependències necessàries estiguin disponibles.

El disseny comença amb una pregunta ja resolta i validada manualment. Després s'identifica què varia entre execucions, què és una constant metodològica i què és un resultat intern. La capa municipal, el codi, el model d'elevacions i la distància de marge poden ser entrades; l'algorisme de pendent i la unitat en graus poden formar part del mètode fix; la taula zonal i el GeoTIFF final són sortides. Exposar-ho tot com a paràmetre trasllada decisions sense orientar-les, mentre que ocultar una decisió que ha de variar fa el model poc reutilitzable.

Els noms dins del model han de descriure funció i unitat. `municipis`, `codi_municipi`, `mdt`, `distancia_marge_m` i `pendent_graus` són més clars que `input`, `number`, `raster2` i `result`. La descripció de cada paràmetre ha d'indicar tipus, domini i condició: codi de text corresponent a una única entitat, distància no negativa en metres o MDE amb `NoData` definit. El valor inicial és una proposta per al cas guiat, no una norma territorial.

Un model verificable ha d'explicitar sis dimensions:

1. Entrades amb tipus, esquema i restriccions clares.
2. Paràmetres amb unitats i valors inicials justificats.
3. Algorismes identificats, constants i dependències entre nodes.
4. Resultats temporals, intermedis i finals distingits.
5. Fonts, `CRS`, resolucions, referència vertical i `NoData` necessaris.
6. Controls i condicions de fallada aplicables a cada sortida final.

El model ha de tenir un propòsit cohesionat. Un únic diagrama que descarrega fonts, corregeix totes les capes del curs, calcula vectors i ràsters, crea mapes i empaqueta el lliurament és difícil d'entendre i de provar. Convé separar preparació, anàlisi i publicació quan tenen cicles o responsables diferents. Una sortida estable d'un model pot ser l'entrada documentada del següent sense convertir tota la vida del projecte en una sola caixa negra.

Validar l'estructura del model només comprova que les connexions i els paràmetres són formalment admissibles. No demostra que la pregunta, el `CRS`, la distància, la resolució o la regla de `NoData` siguin correctes. Cal executar-lo sobre un cas conegut i comparar-lo amb el procediment manual. La prova ha de revisar valors i geometries, no només que els dos processos creen capes amb el mateix nom.

### Dependències, noms i errors

Una **dependència** és qualsevol element extern sense el qual el procés no es pot interpretar o executar. Inclou fitxers i capes, però també camps, `CRS`, transformacions, proveïdors, complements, versions de QGIS, fonts tipogràfiques, expressions, variables, connexions a bases de dades i serveis remots. Un `.model3` pot conservar els nodes i continuar sense funcionar perquè falta el proveïdor que implementa un algorisme.

La nomenclatura relaciona dependències i resultats. Els noms de capes han d'incloure fenomen, operació i paràmetre que distingeix la versió, com `assentaments_buffer_200m` o `pendent_25m_graus`. El nom d'un camp ha de distingir unitat i estadístic quan no siguin evidents, com `area_m2` o `slope_max`; només s'utilitzarà `slope_p90` si s'ha fixat un algorisme que calculi explícitament aquest percentil. Un nom llarg no compensa un registre de procedència, però un nom genèric obliga a obrir moltes propietats per saber què és cada objecte.

Les dates s'incorporen quan identifiquen el període de les dades o una edició real, no com una successió improvisada de còpies. `cobertes_2020` i `cobertes_2025` poden ser dues fonts temporals; `final_2`, `final_bo` i `final_ara_si` només documenten indecisió. Per a proves de paràmetres, la taula de registre o el model ha de conservar la relació entre variant i decisió acceptada.

Els errors es poden ordenar per fase. Aquesta classificació orienta la correcció cap a la causa en lloc de retocar la sortida.

::: table "Errors de processament i punt de diagnòstic"
| Fase | Exemple | Senyal | Correcció adequada |
| --- | --- | --- | --- |
| Entrada | Capa equivocada, camp absent o font modificada | Esquema o recompte no coincideix amb el contracte | Aturar, identificar i preparar l'entrada correcta |
| Geometria | Autointersecció o objecte buit | Avís, entitat omesa o superposició fallida | Diagnosticar i corregir només les geometries afectades |
| Referència | Distància aplicada en graus o graelles desalineades | Extensió, unitat o dimensió incoherent | Reprojectar o alinear explícitament abans de repetir |
| Paràmetre | `AND` en lloc d'`OR`, llindar o banda incorrectes | Resultat plausible però contrari a la predicció | Revisar la pregunta i el contracte, no la simbologia |
| Destinació | Nom duplicat, ruta no accessible o fitxer bloquejat | Sortida absent, antiga o parcial | Corregir destinació i comprovar totes les files afectades |
| Execució | Proveïdor desactivat o memòria insuficient | Excepció o finalització parcial | Registrar entorn, simplificar o canviar estratègia justificadament |
| Validació | Capa creada però buida o amb valors impossibles | Un control posterior incompleix el criteri esperat | Considerar l'execució fallida encara que no hi hagi excepció |
| Interpretació | Proximitat descrita com accessibilitat | Conclusió excedeix el model | Reescriure l'abast o incorporar les dades que falten |
:::

Un procés fiable ha de **fallar de manera visible** quan no es compleix una precondició. Si la consulta del codi municipal retorna zero o dues entitats en lloc d'una, el model no hauria de continuar produint una ROI sense advertència. Quan el Dissenyador no permet expressar directament una comprovació, aquesta s'ha de fer abans, després o en un pas auxiliar documentat. Crear una capa buida i continuar no és una forma acceptable de gestionar l'error.

La correcció s'aplica al primer punt incorrecte i obliga a repetir els resultats dependents. Si una clau estava truncada abans d'una unió, no s'omplen manualment els nuls a la capa final; es corregeix la clau, es repeteix la unió, es tornen a executar els geoprocessaments i s'actualitzen mapes i controls. Aquest recorregut segueix el graf de dependències encara que s'hagi executat manualment.

### Cas guiat: una regió d'interès per a Vila-seca

El model guiat delimita una **regió d'interès** (ROI) lleugerament més gran que Vila-seca per analitzar el relleu sense perdre veïnatge a les vores. Les entrades són una capa municipal, un codi oficial, un model digital del terreny (MDT o MET segons la nomenclatura del producte) i una distància de marge. El valor inicial del marge és 500 m, però queda exposat com a paràmetre perquè la seva funció es pugui discutir. No és un valor universal ni demostra per si sol que tot el context hidrològic o de visibilitat sigui suficient.

Abans d'executar, el contracte exigeix que el codi sigui text i identifiqui una sola entitat; que la geometria tingui el `CRS` conegut; que el MDT cobreixi la ROI prevista; i que la resolució, la referència vertical i `NoData` estiguin documentats. El marge s'expressa en metres i necessita un `CRS` projectat adequat. Si alguna precondició falla, cal aturar la seqüència abans de crear resultats derivats.

::: table "Seqüència del model integrat"
| Pas | Algorisme o decisió | Sortida i control |
| --- | --- | --- |
| 1 | `native:extractbyexpression` amb `EXPRESSION = attribute(@feature, 'codi_muni') = @codi_municipi` i sortida temporal | Una sola entitat, codi i nom comprovats; zero o més d'una fan fallar el flux |
| 2 | `native:checkvalidity` amb mètode GEOS i, només si cal, `native:reprojectlayer` amb `TARGET_CRS = EPSG:25831` | Cap entitat invàlida ni error; geometria apta, extensió plausible i unitats mètriques explícites |
| 3 | `native:buffer` amb `DISTANCE = @distancia_marge_m`, `SEGMENTS = 10`, extrems i unions arrodonits, `MITER_LIMIT = 2`, `DISSOLVE = True` i `SEPARATE_DISJOINT = False` | ROI temporal o persistent, una sola entitat eventualment multipart, superfície superior a la municipal i distància mostrejada |
| 4 | `gdal:cliprasterbymasklayer` amb ROI, `CROP_TO_CUTLINE = True`, resolució de la font conservada, `NODATA` explícit i tipus de dada preservat | Ràster temporal no buit; resolució, origen, dimensions, `NoData` i rang comparats amb la font |
| 5 | `gdal:slope` sobre la banda 1, `SCALE = 1` si totes les unitats són metres, sortida en graus, fórmula fixada i `COMPUTE_EDGES = False` | GeoTIFF persistent `pendent_roi_graus.tif`, rang de 0° a 90° i vores `NoData` esperades |
| 6 | `native:zonalstatisticsfb` sobre el municipi original, banda 1 i prefix `slope_`, amb recompte, mitjana, desviació, mínim i màxim | Capa o taula persistent amb una fila municipal, recompte vàlid positiu i estadístics dins del rang del ràster |
:::

Els noms anteriors corresponen a QGIS 3.44. El model ha de conservar també tots els paràmetres no mostrats que el proveïdor exposa, encara que mantinguin un valor inicial: mètode de validesa, tractament d'errors, tipus de dada, fórmula de pendent i destinacions. `gdal:cliprasterbymasklayer` pot conservar la mida de cel·la sense garantir per si sol que l'origen coincideixi amb una graella externa; per això la postcondició compara la geotransformació amb la font. Si el cas exigeix una alineació comuna amb altres ràsters, abans cal aplicar el contracte de graella de l'anàlisi ràster.

El marge s'utilitza per calcular el pendent; les estadístiques s'obtenen sobre el polígon municipal original. Calcular-les sobre la ROI respondria una pregunta diferent. A la costa hi pot haver `NoData`, de manera que el recompte de píxels vàlids forma part del resultat. Una mitjana sense aquest denominador podria ocultar que només s'ha observat una part del terme.

La ROI pot ser una sortida persistent perquè fa visible l'àmbit de càlcul. El ràster retallat pot ser temporal si es regenera de manera segura i no és necessari per diagnosticar cap incidència. El GeoTIFF de pendent i la taula zonal són finals analítics; els controls i el diari són finals documentals. Aquesta selecció evita exposar totes les connexions internes sense convertir el procés en una caixa negra.

La prova manual i el model han de coincidir segons controls definits: una entitat municipal, mateixa extensió de ROI, mateixa mida i origen de cel·la, mateix recompte de valors vàlids i estadístiques equivalents dins de la precisió esperada. Si difereixen, cal revisar les seleccions, el tractament de `NoData`, les destinacions i els valors predeterminats. No s'ha de triar el resultat del model només perquè sembla més recent.

El cas integrat permet entendre dependències d'una branca llarga, però la micropràctica final no exigeix convertir necessàriament els sis passos en un sol model. El requisit mínim és construir, validar i conservar el `.model3` `municipi_treball + distancia_m -> ROI` de la pràctica guiada; el model es pot ampliar amb passos d'aquest cas sempre que es tornin a validar. El tancament del projecte continua tenint com a objecte principal la síntesi verificada de les micropràctiques 1–5.

### Desar, versionar i transportar processos

QGIS permet conservar models al perfil d'usuari, exportar-los com a fitxers `.model3` i, segons el flux utilitzat, associar-los al projecte. Un model inclòs en un projecte viatja amb el `.qgz`, però no incorpora automàticament les fonts, els proveïdors, els complements ni les credencials. Un `.model3` facilita reutilització i comparació de versions, però manté les mateixes dependències externes.

Un model desat només al perfil personal pot desaparèixer del paquet encara que funcioni a l'ordinador d'origen. Com que el model validat forma part del resultat obligatori, cal exportar-lo com a `.model3` a la carpeta del projecte, donar-li un nom estable i registrar-ne la versió. El fitxer `.qgz` independent es conservarà encara que el projecte també s'hagi desat dins del GeoPackage, perquè permet revisar la seva estructura i recuperar-lo amb més facilitat.

Les rutes relatives funcionen quan el projecte i les dades mantenen una estructura comuna. No resolen dependències situades fora de l'arrel, connexions amb noms locals ni recursos disponibles només al perfil de QGIS. Abans d'empaquetar cal inventariar totes les fonts des de les propietats del projecte i decidir si cada una s'inclou, es pot tornar a obtenir o només serveix com a context remot. La llicència pot impedir redistribuir una entrada encara que tècnicament càpiga al ZIP.

La **prova de transport** no consisteix a moure només el `.qgz`. S'ha de copiar o comprimir el paquet complet, extreure'l en una carpeta nova que no comparteixi la ruta original i obrir-lo des d'allà. Si és possible, s'utilitzarà un altre perfil o equip. Durant la prova no s'han de reparar manualment les rutes sense registrar-ho, perquè això amagaria una dependència del paquet.

::: table "Protocol de prova de transport"
| Fase | Acció | Criteri d'acceptació |
| --- | --- | --- |
| Preparació | Tancar edicions, actualitzar el `.qgz` extern i el projecte incrustat al GeoPackage, i generar el paquet des de la carpeta canònica | No hi ha cap capa pendent ni fitxer temporal imprescindible, i les dues representacions parteixen del mateix estat validat |
| Aïllament | Extreure el paquet en una ruta nova | El projecte no pot resoldre fonts per coincidència amb la carpeta original |
| Obertura | Obrir per separat el `.qgz` i el projecte incrustat, tancant QGIS entre proves, i revisar el registre de missatges | No hi ha fonts perdudes ni proveïdors imprescindibles desconeguts en cap representació |
| Inventari | Obrir una capa de cada grup, les taules i els ràsters | Esquema, `CRS`, extensió, estils i valors continuen disponibles |
| Procés | Reexecutar el model QGIS obligatori i una operació representativa | Les entrades es resolen i els controls semàntics coincideixen |
| Composició | Obrir i exportar el mapa final | Fonts, llegenda, escala, textos i recursos enllaçats es mantenen |
| Fitxers externs | Obrir l'exportació en un visor diferent | La peça és llegible i no depèn de la sessió de QGIS |
| Registre | Anotar entorn, incidències i resultat de la prova | Una altra persona pot saber què s'ha comprovat i què continua extern |
:::

La versió de QGIS, el sistema operatiu i els proveïdors es registraran quan puguin afectar l'execució. No cal prometre compatibilitat amb qualsevol versió futura, però sí identificar l'entorn validat. Si un model depèn d'un camp que no existeix al municipi següent, ha de fallar de manera interpretable o documentar la preparació necessària; adaptar l'esquema forma part de transferir el mètode, no és un detall aliè.

### Pràctiques de desenvolupament aplicades al projecte

Els fluxos de desenvolupament reproduïble aporten principis útils encara que no s'escrigui codi. El primer és separar entrades originals, dades preparades, resultats regenerables i productes finals. El segon és declarar les dependències: una sortida no apareix «després» d'una altra només pel seu nom, sinó perquè l'utilitza com a entrada. El tercer és corregir sempre la font canònica i tornar a generar els descendents.

Control executable
: Comprovació que una eina pot repetir, com exigir 22 codis únics, cap geometria buida o una extensió dins d'un rang.

Cas sentinella
: Comprovació coneguda que ajuda a detectar desplaçaments, com el codi i el nom d'un municipi, una geometria dins de la ROI o una cel·la amb valor esperat.

Els controls executables no són exclusius de Python: molts es poden expressar amb estadístiques, consultes o expressions de QGIS i registrar en una taula. Un cas sentinella no valida tot el conjunt, però revela errors de columna, `CRS`, filtre o ordre. S'ha de combinar amb recomptes, distribucions i mostres.

## Auditoria completa del projecte final

El producte final ha de respondre la pregunta territorial formulada a l'inici i permetre reconstruir com s'ha arribat a la resposta. No és una acumulació de totes les capes creades durant el curs. Conserva les entrades necessàries, els resultats amb una funció clara i els intermedis imprescindibles per auditar decisions o incidències. La resta es pot eliminar del panell o del paquet només després de comprovar que és regenerable i no conté l'única evidència d'un pas crític.

### Pregunta, abast i inventari

La pregunta final ha d'identificar fenomen, municipi, període, unitat d'anàlisi i mesura o relació espacial. Pot haver evolucionat respecte de la proposta inicial, però el canvi s'ha de registrar. Una pregunta sobre «zones adequades» s'ha de reformular com a «zones que compleixen els criteris A, B i C» si no s'han incorporat tots els factors necessaris per afirmar adequació.

L'inventari relaciona cada peça amb una funció: font original, dada preparada, intermedi de diagnòstic, resultat analític, taula de control, mapa o documentació. Una capa sense funció identificable no s'ha de conservar només perquè existeix; una capa necessària no s'ha d'eliminar perquè no apareix al mapa final. El nom, la ubicació, el format, el productor i la dependència immediata han de permetre seguir-ne el llinatge.

::: table "Continuïtat de les micropràctiques dins del projecte final"
| Fase | Entrada canònica | Sortida persistent | Consumidor següent |
| --- | --- | --- | --- |
| Micropràctica 1 | Pregunta territorial, límit municipal oficial, paquets originals autoritzats i metadades de les fonts | `municipi_treball` creat amb una sola entitat validada, capes inicials al GeoPackage, inventari, diari i punt de control format per `projecte_tig.qgz` i el projecte QGIS incrustat | Preparació de capes, consultes i totes les branques analítiques posteriors |
| Micropràctica 2 | Punt de control de la micropràctica 1 i fonts de captura documentades | Capes digitalitzades al GeoPackage amb identificadors estables, esquema, dominis i controls de geometria o topologia | Branca de geoprocessament vectorial i auditoria d'autoria |
| Micropràctica 3 | `municipi_treball` creat a la micropràctica 1 i capes i taules preparades del GeoPackage | `municipi_treball` verificat sense substituir-lo, atributs derivats en sortides diferenciades, subconjunts materialitzats, claus preparades, unions o relacions i diagnòstic de nuls | Micropràctiques 4 i 5, composicions i auditoria final |
| Micropràctica 4 | `municipi_treball`, xarxa i equipaments preparats i una capa capturada | Capes persistents de cada criteri vectorial i resultat combinat al GeoPackage, amb mesures recalculades | Composició analítica i reexecució de control de la micropràctica 6 |
| Micropràctica 5 | `municipi_treball` i MDE oficial documentat amb marge | GeoTIFF finals i taula zonal o comparativa al GeoPackage | Composició comparativa i reexecució de control de la micropràctica 6 |
| Micropràctica 6 | Sortides canòniques de les micropràctiques 1–5, diari i les dues representacions del projecte QGIS | GeoPackage i GeoTIFF auditats, `.model3` validat, `.qgz` extern i projecte incrustat actualitzats deliberadament i amb la coherència verificada, exportacions finals i diari complet | Prova de transport, lliurament i explicació oral |
:::

### Fonts, llicències i procedència

Cada font necessita productor, producte, edició o data, cobertura, escala o resolució, `CRS`, llicència, via d'accés i limitacions. La data de descàrrega no substitueix la data del fenomen. Un connector de QGIS tampoc no és la font: només és una via d'accés. Si una dada remota no s'inclou al paquet, el registre ha d'indicar com es pot recuperar i què passa si el servei canvia.

Els originals es mantenen sense modificar. Una dada preparada ha de declarar la transformació que l'ha generat i conservar un identificador que permeti contrastar-la. Si la llicència no permet redistribuir l'original, el paquet pot incloure metadades, instruccions d'obtenció i derivats permesos, però no ha d'ocultar aquesta dependència. La prova de transport distingirà entre projecte completament local i projecte que necessita accés extern.

La procedència no acaba amb una citació al mapa. Una capa derivada pot combinar límits del CNIG, elevacions de l'ICGC i geometries capturades durant el curs. El registre ha de separar la font de cada component i explicar quina operació els relaciona. «Elaboració pròpia» identifica l'autoria de la síntesi, no converteix les dades d'origen en pròpies.

### Vectors, taules i relacions

Les capes vectorials s'auditen per tipus geomètric, `CRS`, extensió, nombre d'entitats, identificadors, camps obligatoris, nuls, duplicats, geometries buides o invàlides i regles topològiques que depenen de la finalitat. Una geometria vàlida pot continuar sent posicionalment incorrecta o massa generalitzada; per això cal mantenir una mostra contrastada amb la font.

Les unions es revisen per cardinalitat. Cal saber quantes claus són úniques, quantes es dupliquen, quants registres coincideixen i quins queden sense correspondència a cada costat. Els camps derivats han de conservar expressió, tipus, unitat i rang. Si una intersecció ha fragmentat polígons, les àrees i longituds s'han de recalcular i els atributs extensius no es poden sumar sense examinar si s'han duplicat.

Les seleccions i els filtres són estat del projecte fins que es materialitzen. L'auditoria es farà amb totes les seleccions netejades i amb cada filtre documentat. Una capa que mostra només tres entitats perquè en queden seleccionades no equival a una extracció persistent de tres entitats. Els estils basats en regles tampoc no substitueixen la consulta que defineix el subconjunt analític.

### Ràsters i superfícies

Cada ràster final ha d'identificar font, banda, tipus, `CRS`, referència vertical si correspon, extensió, origen, mida de cel·la, files, columnes, `NoData`, remostreig i derivació. Els ràsters que es combinen han d'estar alineats, no només visualment superposats. Les classes necessiten taula de codis i els derivats del terreny, algorisme i unitats.

Els controls inclouen rang, quantils, recompte vàlid, patró de buits, vores i costures. Les estadístiques zonals han d'indicar la regla de pertinença de cel·les i el denominador vàlid. La comparació de 25 m i 200 m conservarà la taula preregistrada i distingirà resultats observats d'hipòtesis. Una diferència de resolució no s'ha de descriure com una diferència d'exactitud sense punts de control independents.

Els GeoTIFF finals es conservaran fora del GeoPackage llevat que un requisit explícit i provat indiqui una altra cosa. Les piràmides i auxiliars necessaris han de viatjar amb el fitxer; les memòries cau regenerables es poden excloure si no contenen l'única còpia d'una metadada. Obrir els ràsters des del paquet nou confirma que la decisió era correcta.

### Operacions, resultats i controls

Cada resultat analític s'ha de relacionar amb entrades, algorisme, paràmetres, context i destinació. El diari no necessita transcriure cada clic, però sí les decisions que poden canviar la resposta: distàncies, predicats, ordre de superposició, dissolució, remostreig, llindars, tractament de nuls i `NoData`. Els valors predeterminats rellevants també s'hi inclouen.

La validació s'ha de fer després de cada transformació decisiva i repetir-se al final. Es compararan recomptes, superfícies, rangs, esquemes i una mostra espacial. Un resultat no queda validat perquè el pas següent l'ha acceptat com a entrada. Si una incidència es va corregir, el registre ha d'indicar la causa, la modificació i quins descendents es van regenerar.

El lot i el model QGIS obligatoris s'auditaran com a peces addicionals, no com a substituts dels resultats. Cal comprovar-ne versió, dependències, paràmetres, destinacions i prova de reexecució. Les consultes SQL o PostGIS i els scripts PyQGIS són ampliacions opcionals i, si s'incorporen, s'auditen i es conserven separadament.

### Estat del projecte QGIS

El punt de control del curs té dues representacions del mateix projecte QGIS: `projecte_tig.qgz` a l'arrel i el projecte incrustat a `dades_preparades/projecte_tig.gpkg`. El `.qgz` ha d'obrir-se sense fonts perdudes i continua sent la referència més fàcil de revisar i recuperar. La còpia incrustada també s'ha d'actualitzar expressament; no canvia només perquè s'hagi desat el fitxer extern.

Després de netejar el panell i validar les sortides, cal desar el `.qgz` i actualitzar el projecte incrustat des del mateix estat de la sessió. Tot seguit es tanca QGIS i es prova cada representació per separat, obrint-la des de la seva ubicació i no des de la llista de projectes recents. En totes dues s'han de contrastar fonts, grups, noms de capa, filtres, estils, composicions i una mostra de recomptes o valors; no n'hi ha prou que el llenç tingui una aparença semblant.

>>>> **Desar una representació no refresca l'altra.** Si el `.qgz` conté la composició nova però el projecte incrustat encara mostra una capa anterior, el punt de control és incoherent encara que tots els fitxers existeixin. Cal tornar a l'estat validat, actualitzar totes dues representacions i repetir-ne les obertures independents abans d'empaquetar.

Els grups de capes han de separar originals o referències, dades preparades, resultats vectorials, ràsters i composicions. Les capes temporals, duplicades o descartades s'eliminaran del panell després d'assegurar que no són necessàries. Els noms visibles han de correspondre als noms del registre, encara que una etiqueta més llegible pugui complementar el nom tècnic.

Cal revisar filtres, seleccions, mode d'edició, unions temporals, formularis, variables, estils, ordre de dibuix i visibilitat dependent de l'escala. El `CRS` del projecte serà adequat per a la composició, però cada capa conservarà el seu `CRS` real. Una capa que només encaixa gràcies a una assignació incorrecta no s'ha de dissimular amb reprojecció al vol.

Les composicions han de referenciar les capes finals, no proves que tenen una aparença semblant. Si hi ha diverses composicions, el nom ha d'identificar la seva funció i suport. Els textos dinàmics, escales i llegendes es revisaran després de netejar el projecte perquè una capa eliminada o rebatejada pot deixar una peça incompleta sense afectar el llenç principal.

## Preparació cartogràfica i exportació

La síntesi cartogràfica selecciona només els resultats necessaris per explicar la conclusió. Un mapa de context situa l'àmbit; un mapa analític mostra el patró o la coincidència; una taula o anotació pot donar els valors de control. Afegir totes les capes creades durant el curs no demostra més feina i pot ocultar la relació territorial principal.

Abans de simbolitzar cal identificar variable, tipus, unitat, període i absències. Una categoria necessita colors diferenciables i etiquetes; una magnitud ordenada, una seqüència coherent; una màscara, una distinció visible entre fals, cert i no avaluat. Les classes del mapa han de coincidir amb la reclassificació analítica o explicar qualsevol simplificació cartogràfica. Canviar només la llegenda no canvia els valors de la capa.

La composició s'ha de dissenyar per a un suport i una mida. Títol, extensió, escala, llegenda, fonts, unitats, notes i orientació s'incorporen quan permeten interpretar la pregunta. Una barra d'escala només és útil si el mapa manté proporció i el `CRS` és adequat; un nord decoratiu no corregeix una orientació confusa; una font en cos il·legible no compleix la funció d'atribució.

Els mapes amb dues resolucions conservaran extensió, escala, dimensions dels marcs, intervals i colors comuns. Els mapes de distàncies o candidats indicaran el llindar i les unitats. La simbologia no ha d'ocultar cel·les `NoData`, zones excloses ni fragments petits que modifiquen la interpretació. Si s'utilitza transparència sobre una ortofoto, també es provarà sense la base per comprovar que el resultat analític continua llegible.

PDF i SVG poden conservar geometries i textos vectorials, però també poden contenir imatges ràster incrustades. L'extensió no garanteix la naturalesa interna. Les ortofotos, ombrejats i altres superfícies continuaran sent ràster dins d'un PDF; les línies, símbols i textos haurien de mantenir-se nítids i, quan el flux ho permeti, seleccionables. En una exportació PNG cal fixar dimensions o resolució segons la mida d'ús, no confiar en el zoom del visor.

La sortida es revisarà fora de QGIS. Cal comprovar pàgina, retall, fonts, accents, transparències, gruixos, llegenda, escala, resolució de les imatges i objectes fora del marc. Una exportació pot semblar correcta al compositor i fallar en un visor diferent per substitució tipogràfica o recursos enllaçats. Qualsevol correcció que alteri geometries, valors, classes o etiquetes vinculades a dades s'ha de fer al projecte i tornar a exportar, no retocar-se només al fitxer final.

::: table "Auditoria del mapa o exportació final"
| Dimensió | Pregunta de revisió |
| --- | --- |
| Focus | La pregunta i el resultat principal es poden identificar sense obrir el projecte? |
| Territori | Àmbit, escala, orientació i context són suficients i no enganyosos? |
| Variable | Nom, unitat, període, classes i absències estan definits? |
| Coherència | La capa i el camp del compositor són exactament els resultats validats? |
| Llegibilitat | Text, símbols i patrons funcionen a la mida i al suport finals? |
| Integritat | La simbologia no amaga `NoData`, nuls, incertesa o zones no analitzades? |
| Procedència | Fonts de dades, geometria i elaboració es poden distingir? |
| Exportació | El fitxer s'obre fora de QGIS amb pàgina, fonts i recursos complets? |
:::

## Procedència i limitacions

La **procedència** o llinatge connecta cada resultat amb la font i les transformacions. Es pot representar com una taula amb una fila per objecte: identificador, nom de capa o fitxer, funció, entrada immediata, operació, paràmetres principals, responsable, data, ubicació i control. Una capa que combina dues fonts necessitarà dues relacions d'entrada o una nota que les identifiqui clarament.

El diari desenvolupa allò que la taula no pot resumir: per què es va triar un criteri, quina incidència va aparèixer, com es va corregir i què permet afirmar el resultat. Les captures només provaran configuracions o errors que no quedin visibles en l'historial, el model o la taula. Una successió de pantalles de cada clic fa més difícil trobar les decisions realment rellevants.

Les limitacions han de ser específiques. «Les dades poden contenir errors» no indica com afecta la conclusió. En canvi, explicar que el MDT és anterior a una obra, que el recompte de fanals no mesura il·luminància, que el `buffer` ignora barreres o que la cel·la de 200 m generalitza una franja estreta identifica mecanisme, abast i possible conseqüència. La limitació s'ha de situar prop del resultat que restringeix i també al diari si condiciona el projecte complet.

Convé distingir limitacions de font, representació, mètode i interpretació. Una cobertura incompleta és un límit de font; rasteritzar una línia a 200 m, de representació; aplicar distància euclidiana, de mètode; afirmar accessibilitat real a partir d'aquesta distància, d'interpretació. Aquesta classificació ajuda a saber si el problema es pot corregir amb una dada millor, una altra graella, un altre algorisme o una conclusió més acotada.

La incertesa no s'ha d'utilitzar per invalidar qualsevol resultat ni per protegir-lo de la crítica. Cal indicar quines conclusions es mantenen davant de les proves de sensibilitat i quines depenen d'un llindar, una resolució o una font. Si no hi ha dades per resoldre una limitació, aquesta queda com a pregunta oberta; no s'omple amb una estimació inventada.

## Preparar l'explicació oral

L'explicació oral demostra que el projecte no és només un conjunt de fitxers. Ha de permetre seguir una decisió des de la pregunta fins a l'evidència i distingir què prové d'una font, què s'ha derivat i què s'interpreta. Enumerar menús o llegir el diari no substitueix aquesta cadena.

Un guió breu pot seguir sis moviments:

1. Formular la pregunta, l'àmbit, el període i la unitat d'anàlisi.
2. Presentar les fonts principals i una limitació que en condicioni l'ús.
3. Explicar per què el model vectorial o ràster i les operacions escollides responen la pregunta.
4. Justificar dos paràmetres determinants, com una distància i una resolució.
5. Mostrar un control que podria haver refutat o obligat a corregir el resultat.
6. Interpretar la sortida principal i acotar què no permet afirmar.

La presentació ha d'estar preparada per abandonar l'ordre previst. Es pot demanar obrir una capa, identificar-ne la font, explicar un camp, reconstruir una expressió, mostrar el `NoData` d'un ràster o justificar per què una sortida és temporal. Poder seguir una peça triada a l'atzar fins a l'entrada immediata és una prova pràctica de traçabilitat.

Les incidències són part legítima de l'explicació. Descriure un error de `CRS`, una clau sense correspondència o una vora ràster, la manera com es va detectar i els resultats que es van regenerar mostra comprensió del procés. Ocultar-lo i presentar només una seqüència perfecta elimina una evidència útil d'autoria i control.

Quan el treball s'ha fet en equip, cada participant ha de poder explicar les decisions centrals i la seva contribució, no només la peça que va editar. El diari pot identificar responsabilitats sense fragmentar l'autoria del resultat. Utilitzar un model, SQL o codi d'una altra font exigeix atribució i comprensió: executar-lo no demostra per si sol que se'n coneguin les precondicions o els límits.

## Tancament del producte final SIG

Les peces finals tenen funcions complementàries. El GeoPackage reuneix capes vectorials i taules; els GeoTIFF conserven ràsters analítics; el `.qgz` registra organització, estils, relacions i composicions; el `.model3` conserva el procés QGIS parametritzat; les exportacions comuniquen una selecció; i el diari conserva decisions, controls i limitacions. Cap peça no substitueix les altres.

::: table "Peces del producte final"
| Peça | Funció i control final |
| --- | --- |
| GeoPackage | Capes i taules amb noms estables, `CRS` identificats, esquemes comprensibles, claus i geometries comprovades |
| Ràsters | GeoTIFF amb procedència, graella, tipus, unitat i `NoData` explícits |
| Projectes QGIS | `.qgz` extern i projecte incrustat al GeoPackage actualitzats des del mateix estat, oberts per separat sense fonts perdudes i amb grups, estils, rutes i composicions coherents |
| Mapes i resultats exportats | Pregunta, àmbit, fonts, unitats, període i interpretació llegibles fora de QGIS |
| Diari d'activitats | Fonts, operacions, paràmetres, incidències, controls, decisions, procedència i limitacions relacionats |
| Processament de QGIS | Historial revisat, registre del lot i `.model3` obligatori amb dependències, paràmetres, destinacions i prova de reexecució documentats |
| Ampliació opcional | Consultes SQL o PostGIS i scripts PyQGIS amb entorn i dependències documentats, conservats separadament del procés QGIS obligatori |
| Explicació oral | Justificació d'una mostra del procés, diferència entre dades i inferències i resposta sobre autoria i límits |
:::

La neteja final es farà sobre una còpia controlada del projecte. Abans de descartar una capa cal comprovar que es pot regenerar, que no alimenta cap composició i que no és l'única evidència d'un pas. Després es repetirà l'inventari, es desaran totes les peces, es tancarà QGIS i s'executarà la prova de transport. Una capa que només existeix perquè continuava oberta a la memòria quedarà així detectada abans del lliurament.

## Activitats

### Comprovació: reconstruir una execució

Cal triar una operació de l'historial i reconstruir-ne el proveïdor i identificador, les entrades, les precondicions, els paràmetres, l'estat rellevant i la destinació. Després s'ha d'explicar quina informació necessària per interpretar el resultat no apareix al registre. La comprovació acaba repetint l'operació sobre una còpia i comparant un control semàntic, no només el nom del fitxer.

### Pràctica guiada: execució manual, lot i model

Primer s'executarà manualment `native:buffer` sobre `municipi_treball`, sense seleccions ni filtres imprevistos i en un `CRS` projectat en metres. Amb `DISTANCE = 500`, els paràmetres geomètrics fixats al contracte del capítol i la destinació d'auditoria `roi_manual_500m_auditoria`, cal comprovar que la sortida té una geometria vàlida, no buida, una sola entitat eventualment multipart i una superfície superior a la municipal. L'entrada `municipi_treball` no s'ha de modificar ni utilitzar mai com a destinació.

Després s'executarà el mateix buffer per lots amb les distàncies diferenciades de 250, 500 i 750 m. Cada fila tindrà una destinació pròpia, com `roi_lot_250m_auditoria`, `roi_lot_500m_auditoria` i `roi_lot_750m_auditoria`, o una sortida temporal inequívoca equivalent. Cal revisar totes les files, comparar l'evolució de l'extensió i la superfície i contrastar la fila de 500 m amb la sortida manual validada; una sortida buida, repetida o escrita sobre una altra fila invalida el lot.

Finalment es construirà i es desarà un model QGIS `.model3` amb el graf `municipi_treball + distancia_m -> ROI`: una entrada vectorial, un paràmetre numèric en metres i `native:buffer` amb els mateixos paràmetres fixos. Una execució amb 500 m s'escriurà a `roi_model_500m_auditoria`, mai sobre l'entrada ni sobre les sortides manual o de lot. El model es considerarà validat quan coincideixin amb `roi_manual_500m_auditoria` el `CRS`, el recompte, la validesa, l'extensió, la superfície i la diferència espacial dins de la tolerància documentada.

### Pràctica guiada: prova de transport adversa

Sobre una còpia del paquet es provocarà una dependència controlada, com una capa situada fora de l'arrel o un nom de camp no disponible. El projecte s'obrirà des d'una carpeta nova, es diagnosticarà el problema sense reconstruir-lo per intuïció i es corregirà a la font o al contracte. El diari registrarà símptoma, causa, correcció i controls repetits.

### Micropràctica 6: síntesi i tancament del projecte

La sisena micropràctica és la síntesi final de les cinc anteriors. El nucli obligatori és auditar, ordenar, interpretar, compondre i transportar el projecte acumulatiu, executar i documentar el lot de buffers, conservar el model QGIS `.model3` validat i reexecutar una branca que ja alimenta un resultat final. No s'obre una segona pregunta territorial ni es crea un projecte paral·lel. SQL, PostGIS i PyQGIS continuen sent ampliacions opcionals.

::: table "Contracte de la micropràctica 6"
| Component | Requisit |
| --- | --- |
| Entrades | Sortides canòniques de les micropràctiques 1–5, `municipi_treball`, `dades_preparades/projecte_tig.gpkg`, `projecte_tig.qgz`, projecte incrustat al GeoPackage i diari acumulatiu |
| Operacions mínimes | Completar una auditoria integrada; executar i validar el buffer manual; comparar distàncies amb el lot; construir, desar i validar el model `municipi_treball + distancia_m -> ROI`; reexecutar des de l'entrada canònica una branca vectorial o ràster existent i comparar-la amb el resultat conservat; repetir els controls crítics; preparar la simbolització; compondre i exportar almenys un mapa; documentar les limitacions; i actualitzar deliberadament les dues representacions del projecte |
| Resultats | Auditoria integrada, GeoPackage i GeoTIFF finals auditats, `.model3` validat, `.qgz` extern i projecte incrustat amb la coherència verificada, almenys un mapa exportat i diari complet |
| Evidències del diari | Inventari i llinatge finals, contractes i comparacions de l'execució manual, el lot, el model i la branca reexecutada, relació entre pregunta i resultats, incidències, decisions de neteja, limitacions, prova de les dues representacions, prova neta del paquet i guió de la defensa oral |
| Comprovacions | Equivalència del model amb el buffer manual i de la branca reexecutada amb el resultat canònic dins de les toleràncies declarades; cap sobreescriptura de `municipi_treball`; absència de fonts perdudes; esquemes i `CRS` identificats; resultats traçables; ràsters documentats; mapa llegible; i obertura independent correcta de les dues representacions des del paquet extret |
| Fitxers que cal conservar | GeoPackage amb el projecte incrustat actualitzat, `.qgz` extern, model QGIS `.model3`, ràsters finals, mapa exportat, paquet final i diari |
| Paquet final i prova neta | Crear el paquet final, extreure'l en una carpeta neta que no comparteixi la ruta original i comprovar-hi l'obertura del `.qgz`, del projecte incrustat, de les dades, del `.model3` i del mapa exportat sense reparar dependències de manera implícita |
| Defensa oral | Fer una defensa oral breu que relacioni pregunta, fonts, model, paràmetres, un control, resultat, autoria i limitacions |
| Ampliacions opcionals | Les consultes SQL o PostGIS i els scripts PyQGIS no formen part del nucli obligatori; si es presenten, els fitxers corresponents s'han de conservar separadament i documentar-ne l'entorn |
:::

El model obligatori és deliberadament petit: formalitza un buffer ja validat sense convertir tota l'anàlisi acumulada en un diagrama artificial. La seva evidència és la comparació controlada amb la sortida manual; la reexecució de la branca acumulada comprova, de manera separada, que el resultat final continua derivant de les entrades canòniques.

### Activitat integradora: reexecutar una branca acumulada

Cal escollir una branca que ja intervingui en la conclusió del projecte: per exemple, un criteri vectorial de la micropràctica 4 que parteixi de `municipi_treball` i de capes preparades, o la seqüència de pendent, reclassificació i resum zonal de la micropràctica 5. La taula de continuïtat n'identifica l'entrada canònica, la sortida persistent i el consumidor. La reexecució parteix exactament d'aquesta entrada; no torna a descarregar una edició diferent ni inicia un altre cas d'estudi.

Abans d'executar es reconstrueixen des del diari el proveïdor i l'identificador de cada algorisme, els paràmetres, el `CRS`, les seleccions o filtres, la versió de l'entorn i la destinació. La sortida de prova serà temporal o rebrà un nom inequívoc d'auditoria; no reemplaçarà el resultat canònic. En una branca vectorial es compararan esquema, identificadors d'origen, nombre d'entitats, geometries buides, àrea o longitud i diferència espacial. En una branca ràster es compararan dimensions, geotransformació, `NoData`, rang, recompte vàlid i estadístiques zonals sense arrodonir.

La mateixa activitat inclou la reexecució del `.model3` `municipi_treball + distancia_m -> ROI` amb la distància de 500 m i una destinació d'auditoria nova, diferent de les sortides manual i de lot. La comparació amb `roi_manual_500m_auditoria` repetirà els controls de `CRS`, recompte, validesa, extensió, superfície i diferència espacial; ni aquesta prova ni la branca acumulada no poden sobreescriure `municipi_treball`.

Si les reexecucions són equivalents dins de les toleràncies declarades, el diari registra els controls i les sortides de prova es poden descartar quan no aporten cap diagnòstic. Si difereixen, cal localitzar el primer pas divergent, corregir l'entrada o el contracte que pertoqui i regenerar-ne els descendents; no s'edita manualment el resultat final per fer-lo coincidir. Finalment s'actualitzen deliberadament la composició afectada, `projecte_tig.qgz` i el projecte incrustat al GeoPackage, se'n verifica la coherència, es crea el paquet final i se'n repeteixen les obertures després d'una extracció neta.

### Ampliació opcional: SQL i PyQGIS

SQL
: Llenguatge declaratiu per consultar i transformar conjunts de files dins d'un sistema de bases de dades. El dialecte i les funcions disponibles depenen del motor.

PostGIS
: Extensió espacial de PostgreSQL que incorpora tipus geomètrics, índexs i funcions SQL per treballar amb dades geogràfiques.

PyQGIS
: Interfície de programació de QGIS per a Python. Dona accés al projecte, les capes, les geometries i el marc de Processament dins d'un entorn QGIS compatible.

Una expressió de QGIS és el primer nivell reproduïble per formular un filtre, una classe o un camp derivat. SQL aplica la mateixa disciplina a conjunts de files dins d'una base de dades, i PyQGIS permet encadenar expressions, capes i algorismes amb comprovacions programables. Són nivells addicionals de formalització, no substituts de perfilar les dades, comprovar claus, inspeccionar geometries ni validar les sortides.

#### SQL tabular en un GeoPackage

L'entorn d'execució dels exemples següents és la finestra SQL del **Gestor de bases de dades de QGIS 3.44**, amb la connexió SQLite oberta directament sobre `dades_preparades/projecte_tig.gpkg`. No és una capa virtual ni una connexió PostgreSQL. Les dues primeres consultes utilitzen la capa real del miniprojecte; després s'introdueixen dues taules didàctiques petites per practicar nuls i unions sense atribuir aquests camps a cap producte oficial.

::: listing "Primera lectura SQL de la capa municipal real"
```sql
SELECT codi_muni, nom_muni
FROM municipi_treball;

SELECT codi_muni, nom_muni
FROM municipi_treball
WHERE codi_muni = '43171';
```
:::

Cada sentència s'executa per separat. `SELECT` tria les columnes, `FROM` identifica la taula i `WHERE` restringeix les files. La primera sentència ha de retornar l'única entitat del miniprojecte de Vila-seca; la segona comprova la clau textual `43171`. Si el resultat és zero o més d'una fila, no cal afegir més SQL: primer s'ha de revisar que la connexió, la taula i la còpia del projecte siguin les previstes.

::: table "Taules genèriques per introduir SQL tabular"
| Taula | Una fila representa | Camps de l'exemple |
| --- | --- | --- |
| `municipis_exemple` | Un municipi del conjunt didàctic | `muni_id` com a clau, `nom` i `actiu` amb valors 0/1 |
| `observacions_exemple` | Una observació per municipi i any | `obs_id` com a clau, `muni_id` com a referència, `any_ref` i `valor`, que pot ser nul |
:::

Les taules temporals següents permeten practicar consultes sense modificar les capes persistents del projecte. S'han de crear a la mateixa connexió SQLite abans dels exemples i desapareixen en tancar-la. Si la finestra SQL no executa tot el bloc alhora, cal executar cada sentència acabada en `;` per ordre i mantenir oberta la connexió. L'observació amb `muni_id = 'M04'` queda sense municipi deliberadament per comprovar una clau òrfena.

::: listing "Dades temporals per executar els exemples SQLite"
```sql
DROP TABLE IF EXISTS temp.municipis_exemple;
DROP TABLE IF EXISTS temp.observacions_exemple;

CREATE TEMP TABLE municipis_exemple (
    muni_id TEXT PRIMARY KEY,
    nom TEXT NOT NULL,
    actiu INTEGER NOT NULL CHECK (actiu IN (0, 1))
);

CREATE TEMP TABLE observacions_exemple (
    obs_id INTEGER PRIMARY KEY,
    muni_id TEXT,
    any_ref INTEGER NOT NULL,
    valor REAL
);

INSERT INTO municipis_exemple (muni_id, nom, actiu) VALUES
    ('M01', 'Alfa', 1),
    ('M02', 'Beta', 1),
    ('M03', 'Gamma', 1);

INSERT INTO observacions_exemple (obs_id, muni_id, any_ref, valor) VALUES
    (1, 'M01', 2025, 12.5),
    (2, 'M02', 2024, 8.0),
    (3, 'M02', 2025, NULL),
    (4, 'M04', 2025, 7.0);
```
:::

Un cop comprovats `SELECT`, `FROM` i `WHERE`, la consulta següent deriva una etiqueta amb `CASE`. El llindar de 10 només serveix per mostrar la sintaxi i no és un criteri territorial.

::: listing "Selecció i classificació tabular amb SQLite"
```sql
SELECT
    obs_id,
    muni_id,
    valor,
    CASE
        WHEN valor IS NULL THEN 'sense dada'
        WHEN valor >= 10 THEN 'deu o més'
        ELSE 'menys de deu'
    END AS classe
FROM observacions_exemple
WHERE any_ref = 2025
ORDER BY obs_id;
```
:::

La consulta següent parteix de tots els municipis actius, hi associa les observacions de 2025 amb una `LEFT JOIN` i calcula una fila per municipi amb `GROUP BY`.

::: listing "Unió esquerra i resum per municipi amb SQLite"
```sql
SELECT
    m.muni_id,
    m.nom,
    COUNT(o.obs_id) AS n_observacions,
    COUNT(o.valor) AS n_valors,
    AVG(o.valor) AS valor_mitja
FROM municipis_exemple AS m
LEFT JOIN observacions_exemple AS o
    ON o.muni_id = m.muni_id
   AND o.any_ref = 2025
WHERE m.actiu = 1
GROUP BY m.muni_id, m.nom
ORDER BY m.muni_id;
```
:::

La condició de l'any queda a `ON` perquè els municipis actius sense observacions de 2025 continuïn presents. `COUNT(o.obs_id)` retorna zero en aquests casos; `COUNT(*)` retornaria una fila produïda per la unió. `AVG(o.valor)` ignora els nuls, de manera que el recompte i el nombre de valors no nuls s'han d'interpretar conjuntament. Abans d'utilitzar el resum cal contrastar claus duplicades, municipis sense parella i observacions que no troben municipi.

>>>> **La connexió i la quadrícula de resultats no són detalls.** Si la capçalera del Gestor no mostra el GeoPackage previst, la consulta s'executa contra un altre motor o una altra base. Un `SELECT` completat només mostra un resultat; no crea una taula persistent. Cal desar el text SQL i, si el resultat ha d'alimentar el projecte, exportar-lo explícitament a una taula amb nom estable i tornar-la a obrir abans de considerar-la una sortida.

#### SQL espacial amb PostGIS

L'exemple espacial utilitza un entorn diferent: la finestra SQL del Gestor de bases de dades sobre una connexió **PostgreSQL amb PostGIS habilitat**. Pressuposa `projecte.municipis_exemple`, amb `muni_id` únic i geometria poligonal, i `projecte.vies_exemple`, amb `id_tram` únic i geometria lineal. Les dues geometries són vàlides, tenen SRID 25831 i emmagatzemen coordenades en metres; `codi_muni`, si existeix a les vies, pot repetir-se i no intervé com a identificador de segment.

::: listing "Longitud viària dins d'un municipi amb PostGIS"
```sql
WITH fragments AS (
    SELECT
        m.muni_id,
        v.id_tram,
        ST_CollectionExtract(
            ST_Intersection(v.geom, m.geom), 2
        ) AS geom
    FROM projecte.municipis_exemple AS m
    JOIN projecte.vies_exemple AS v
      ON ST_Intersects(v.geom, m.geom)
    WHERE m.muni_id = 'M01'
)
SELECT muni_id, id_tram, geom, ST_Length(geom) AS longitud_m
FROM fragments
WHERE NOT ST_IsEmpty(geom)
ORDER BY id_tram;
```
:::

`ST_Intersects` filtra parelles candidates que comparteixen algun punt; `ST_Intersection` construeix la part comuna; `ST_CollectionExtract(..., 2)` conserva només components lineals, i `ST_Length` els mesura en metres sota els supòsits declarats. Així, un simple contacte puntual no es converteix en longitud. Si només calgués seleccionar municipis sense duplicar-los, una subconsulta amb `EXISTS` seria preferible a retornar una fila per cada tram coincident. La distinció entre seleccionar i transformar continua sent la mateixa que al geoprocessament vectorial {% cite ogcSimpleFeatures2011 %}.

Assignar un SRID no transforma coordenades. Si les columnes no comparteixen una referència adequada, cal verificar-ne primer el SRID i aplicar `ST_Transform` explícitament a la geometria que correspongui. Aquestes funcions i la qualificació `esquema.taula` són pròpies de l'entorn PostGIS de l'exemple; un GeoPackage basat en SQLite no ofereix necessàriament el mateix catàleg ni el mateix comportament.

>>>> **`no such function` sol assenyalar l'entorn abans que la geometria.** Enganxar la consulta PostGIS a la connexió SQLite del GeoPackage pot fallar encara que les taules tinguin noms semblants. Cal registrar motor, extensió i versió, i comprovar la connexió activa abans de canviar la consulta o les dades.

#### Primers passos amb PyQGIS

L'entorn d'execució d'aquests fragments és la **consola Python integrada de QGIS 3.44**, amb `projecte_tig.qgz` obert i les capes del projecte ja resoltes. No són programes destinats a l'intèrpret Python del sistema. El primer contacte només llegeix l'estat del projecte i escriu informació a la consola; no modifica cap capa.

::: listing "Primer contacte amb el projecte des de la consola PyQGIS"
```python
from qgis.core import QgsProject

projecte = QgsProject.instance()
print(projecte.fileName())

for capa in projecte.mapLayers().values():
    print(capa.name())
```
:::

`QgsProject.instance()` retorna el projecte obert, `fileName()` permet comprovar quina còpia s'està utilitzant i `mapLayers()` dona accés a les capes carregades. El resultat esperat inclou `municipi_treball`; si no apareix, cal resoldre el projecte abans de continuar. El pas següent obté aquesta capa sense confiar que el nom visible sigui únic, en comprova l'esquema i inspecciona les entitats.

::: listing "Obtenir, inspeccionar i seleccionar una capa amb PyQGIS"
```python
from qgis.core import QgsProject

coincidencies = QgsProject.instance().mapLayersByName("municipi_treball")
if len(coincidencies) != 1:
    raise RuntimeError(
        f"S'esperava una capa municipi_treball i se n'han trobat {len(coincidencies)}"
    )

municipi = coincidencies[0]
if not municipi.isValid():
    raise RuntimeError("La capa municipi_treball no es pot llegir")
if "codi_muni" not in {camp.name() for camp in municipi.fields()}:
    raise RuntimeError("Falta el camp preparat codi_muni")

ids_valids = []
for entitat in municipi.getFeatures():
    geometria = entitat.geometry()
    if geometria.isNull() or geometria.isEmpty():
        raise RuntimeError("municipi_treball conté una geometria absent o buida")
    print(entitat["codi_muni"], geometria.area())
    ids_valids.append(entitat.id())

if len(ids_valids) != 1:
    raise RuntimeError("municipi_treball ha de contenir una sola entitat")
municipi.selectByIds(ids_valids)
```
:::

El bucle llegeix un atribut amb `entitat['codi_muni']`, obté la geometria amb `geometry()` i utilitza els identificadors interns per crear una selecció temporal. Aquests identificadors de proveïdor són adequats per a `selectByIds()` dins de la sessió, però no substitueixen la clau estable de la taula. L'àrea impresa s'expressa en les unitats de la capa i només es pot interpretar com a metres quadrats després de comprovar un `CRS` projectat en metres. El fragment següent neteja la selecció abans de processar perquè no quedi com a estat implícit.

La primera crida a Processament pot mantenir la sortida en memòria i mostrar només el contracte mínim. El fragment reutilitza la variable `municipi` comprovada a l'exemple anterior:

::: listing "Primer algorisme de Processament amb PyQGIS"
```python
from qgis import processing

resultat = processing.run(
    "native:buffer",
    {
        "INPUT": municipi,
        "DISTANCE": 500,
        "SEGMENTS": 8,
        "DISSOLVE": True,
        "OUTPUT": "TEMPORARY_OUTPUT",
    },
)

buffer_prova = resultat["OUTPUT"]
print(buffer_prova.featureCount())
```
:::

Aquesta prova encara confia en alguns valors predeterminats i desapareix en tancar la sessió. És adequada per entendre `processing.run()`, el diccionari de paràmetres i la sortida retornada, no com a resultat final. La versió següent explicita més precondicions i paràmetres, deriva un camp sense modificar l'entrada i escriu una capa persistent amb un nom controlat.

Per derivar atributs no cal obrir una edició i canviar files casualment dins del bucle. La Calculadora de camps de la interfície o `native:fieldcalculator` fan explícites l'expressió, el tipus i la destinació, i poden crear una capa nova sense modificar l'entrada. El fragment següent afegeix una àrea a una sortida temporal i executa després un buffer persistent amb nom de capa explícit.

::: listing "Calcular un camp i escriure un buffer en una capa GeoPackage"
```python
from pathlib import Path

from qgis import processing
from qgis.core import (
    Qgis,
    QgsProcessingOutputLayerDefinition,
    QgsProject,
    QgsVectorLayer,
)

if municipi.crs().isGeographic() or municipi.crs().mapUnits() != Qgis.DistanceUnit.Meters:
    raise RuntimeError("El CRS de municipi_treball no té unitats mètriques")
municipi.removeSelection()
if "area_m2" in {camp.name() for camp in municipi.fields()}:
    raise RuntimeError("El camp area_m2 ja existeix a la capa d'entrada")

municipi_area = processing.run(
    "native:fieldcalculator",
    {
        "INPUT": municipi,
        "FIELD_NAME": "area_m2",
        "FIELD_TYPE": 0,
        "FIELD_LENGTH": 20,
        "FIELD_PRECISION": 2,
        "FORMULA": "area($geometry)",
        "OUTPUT": "TEMPORARY_OUTPUT",
    },
)["OUTPUT"]
if not municipi_area.isValid() or "area_m2" not in {
    camp.name() for camp in municipi_area.fields()
}:
    raise RuntimeError("No s'ha creat correctament el camp area_m2")

arrel = Path(QgsProject.instance().homePath())
gpkg = arrel / "dades_preparades" / "projecte_tig.gpkg"
if not gpkg.is_file():
    raise RuntimeError(f"No s'ha trobat el GeoPackage: {gpkg}")

nom_sortida = "municipi_buffer_500m_auditoria"
uri_sortida = f"{gpkg}|layername={nom_sortida}"
if QgsVectorLayer(uri_sortida, nom_sortida, "ogr").isValid():
    raise RuntimeError(f"La capa de sortida ja existeix: {nom_sortida}")

destinacio = QgsProcessingOutputLayerDefinition(
    f"ogr:dbname='{gpkg.as_posix()}' table=\"{nom_sortida}\" (geom) sql="
)

processing.run(
    "native:buffer",
    {
        "INPUT": municipi_area,
        "DISTANCE": 500.0,
        "SEGMENTS": 10,
        "END_CAP_STYLE": 0,
        "JOIN_STYLE": 0,
        "MITER_LIMIT": 2.0,
        "DISSOLVE": True,
        "SEPARATE_DISJOINT": False,
        "OUTPUT": destinacio,
    },
)

buffer_roi = QgsVectorLayer(uri_sortida, nom_sortida, "ogr")
if not buffer_roi.isValid() or buffer_roi.featureCount() != 1:
    raise RuntimeError("La capa de buffer persistent no és vàlida o no té una fila")
if any(f.geometry().isNull() or f.geometry().isEmpty() for f in buffer_roi.getFeatures()):
    raise RuntimeError("La capa de buffer conté una geometria absent o buida")
```
:::

El codi evita modificar `municipi_treball`, rebutja un camp `area_m2` preexistent per no substituir-lo silenciosament, calcula una àrea plana en les unitats quadrades del CRS mètric comprovat i valida el resultat intermedi. Després atura l'execució si el nom de sortida ja existeix. La destinació OGR identifica explícitament el GeoPackage, la taula nova i la columna geomètrica; passar només el camí del contenidor podria fer que l'escriptura el tractés com un fitxer que cal reemplaçar. `uri_sortida` identifica la mateixa capa per tornar-la a obrir. Per reemplaçar-la caldria aplicar una política explícita i documentada, no confiar en una sobreescriptura implícita que pugui eliminar altres taules.

>>>> **Consola, versió i destinació formen un sol entorn d'execució.** Un error `No module named qgis` sol indicar que el fragment s'ha executat fora de QGIS; un paràmetre desconegut pot indicar una altra versió o un altre proveïdor; i una capa absent després d'una execució correcta sol exigir revisar el fitxer `.gpkg` i el `layername`, no només el panell de capes. La informació de l'algorisme de la versió instal·lada permet confirmar els noms i els codis enumerats.
