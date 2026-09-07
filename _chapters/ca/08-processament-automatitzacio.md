---
layout: manual-chapter
title: Síntesi, processament i automatització
description: Tancament del projecte municipal i ús d'historials, lots, models, SQL espacial i PyQGIS per repetir processos validats.
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

>>>>> En acabar el capítol, cal poder tancar el projecte municipal i, quan sigui útil, expressar una seqüència validada com un procés parametritzat, auditable i transferible.
>>>>>
>>>>> - Organitzar el GeoPackage, el projecte QGIS, els mapes, les exportacions i el diari com un producte final coherent.
>>>>> - Interpretar un algorisme a partir d'entrades, precondicions, paràmetres, context, destinacions, resultats i controls.
>>>>> - Distingir historial, execució per lots i graf de dependències, i decidir quins resultats són temporals o persistents.
>>>>> - Diferenciar reproductibilitat d'automatització i reconèixer els límits conceptuals de SQL espacial i PyQGIS.
>>>>> - Auditar i transportar el projecte, documentar-ne procedència i limitacions i preparar-ne l'explicació oral.

El marc de **Processament de QGIS** ofereix una interfície comuna per als algorismes natius i per a proveïdors com GDAL. L'historial, el processament per lots i el Dissenyador de models representen graus diferents de formalització. El mateix contracte es pot expressar després amb SQL espacial o PyQGIS, però el criteri geogràfic continua sent independent de la interfície o del llenguatge {% cite qgisUserGuide344 rouaultGDAL2026 %}. La secció següent és una ampliació opcional per formalitzar processos ja validats; el nucli obligatori del tancament comença a [Auditoria completa del projecte final](#auditoria-completa-del-projecte-final).

## Ampliació opcional: reproductibilitat i automatització

L'ampliació presenta historial, lots, models, SQL espacial i PyQGIS com a alternatives, no com a requisits acumulatius. Es pot ometre en una primera lectura orientada a la micropràctica 6 i reprendre-la quan hi hagi un flux estable que realment calgui repetir.

### Reproductibilitat no és automatització

En aquest manual, un procés és **repetible** quan es pot tornar a executar en el mateix entorn amb les mateixes entrades i decisions; és **reproduïble** quan una altra persona pot reconstruir-lo en una ubicació o un equip diferent i obtenir un resultat analíticament equivalent. La terminologia varia entre disciplines, però el criteri operatiu del curs és clar: les fonts es resolen, els paràmetres es coneixen, les dependències estan identificades i els controls tornen a complir-se.

L'**automatització** és la delegació d'una seqüència d'operacions a un lot, un model o un programa. Pot reforçar la reproductibilitat perquè fa explícit l'ordre i redueix variacions manuals, però no la garanteix. Un script amb una ruta personal, una consulta que depèn d'una taula que canvia o un model que utilitza una selecció activa no documentada són automatitzacions fràgils. A l'inrevés, una seqüència manual pot ser reproduïble si les entrades, els paràmetres, l'ordre, els controls i les sortides estan descrits amb precisió.

::: table "Formalització d'un procés i allò que conserva"
| Modalitat | Què fa explícit | Què pot continuar ocult | Ús adequat |
| --- | --- | --- | --- |
| Seqüència manual documentada | Decisions, ordre i controls descrits al diari | Clics accidentals, estat de la interfície o valors predeterminats no anotats | Aprendre, explorar i validar un cas inicial |
| Historial | Algorisme, paràmetres executats i missatges | Justificació, versió immutable de les entrades i part de l'estat del projecte | Reconstruir i diagnosticar execucions recents |
| Lot | Repetició del mateix contracte sobre diverses files | Dependències entre algorismes i validació global | Variar entrades o un paràmetre d'una sola operació |
| Model gràfic | Dependències i transformacions d'una seqüència | Fonts externes, entorn, supòsits i controls no representats | Reexecutar un flux estable i visualment inspeccionable |
| SQL espacial | Relacions i transformacions declaratives sobre dades de base | Preparació externa, dialecte, extensions i estat de la base | Consultes de conjunt i processos propers a les dades |
| PyQGIS | Paràmetres, lògica, bucles i controls programables | Entorn QGIS, paquets, dades i decisions mal documentades | Fluxos dinàmics, comprovacions i integració avançada |
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

Les **entrades** són capes, taules, bandes, camps, expressions o valors. Les **precondicions** indiquen què han de complir abans de començar: tipus geomètric, camps presents, identificadors únics, `CRS`, unitats, resolució, validesa o absència de filtres no previstos. Els **paràmetres** defineixen l'operació, per exemple distància, nombre de segments, predicat, llindar, extensió o mètode de remostreig. El **context** inclou transformacions, variables, tractament de geometries invàlides, seleccions, entorn temporal i altres configuracions. Les **destinacions** decideixen format, fitxer o taula, nom de capa i persistència.

::: table "Elements que cal fixar en un contracte de processament"
| Element | Exemple | Pregunta de control |
| --- | --- | --- |
| Proveïdor i identificador | `native:buffer` | S'ha utilitzat exactament l'algorisme previst? |
| Entrada | Capa `vies_principals` del GeoPackage | És la capa, la versió i el subconjunt correctes? |
| Esquema | Camp `codi_muni` de text i únic | El camp existeix, té el tipus esperat i conserva zeros? |
| Referència espacial | `EPSG:25831`, metres | El `CRS` és realment el de la capa i és adequat per a la mesura? |
| Paràmetre | `distancia_m = 200` | La unitat i la justificació són explícites? |
| Estat | Sense selecció; filtre documentat | L'entrada completa és la que s'ha volgut processar? |
| Destinació | `projecte_tig.gpkg`, capa `vies_buffer_200m` | El nom és únic i la sortida és persistent? |
| Postcondició | Àrea dissolta no superior a la suma individual | Quin resultat faria fallar la validació? |
:::

Per exemple, el contracte anterior no queda complet dient només «fer un buffer de 200 m». En QGIS 3.44, una execució persistent de `native:buffer` sobre línies ha de fixar almenys `INPUT = vies_principals`, `DISTANCE = 200`, `SEGMENTS = 10`, `END_CAP_STYLE = Round`, `JOIN_STYLE = Round`, `MITER_LIMIT = 2` i `DISSOLVE = True`. `OUTPUT` ha d'escriure el fitxer `dades_preparades/projecte_tig.gpkg` amb el nom de capa `vies_buffer_200m`. Els noms dels estils són els de la interfície; en una crida programada s'han de conservar també els codis enumerats corresponents. Abans cal exigir un `CRS` projectat en metres, geometries aptes i cap selecció imprevista; després, comprovar que la sortida és vàlida, no és buida i té una àrea no superior a la suma dels buffers individuals equivalents.

Els valors predeterminats també són paràmetres. Acceptar els segments d'un `buffer`, el tractament de geometries invàlides o la resolució suggerida per una eina és una decisió, encara que no s'hagi escrit res al quadre. Si el valor afecta el resultat, s'ha de registrar. Un model que confia en el predeterminat d'una versió pot canviar de comportament quan el proveïdor actualitza l'algorisme.

El `CRS` del projecte és principalment una configuració de visualització. Un algorisme pot treballar en el `CRS` de l'entrada, demanar-ne un de sortida o aplicar regles pròpies del proveïdor. Cada flux ha de fer explícites les unitats i les transformacions en lloc de confiar que el llenç mostra les capes alineades. El mateix criteri s'aplica als ràsters: compartir `CRS` no implica compartir origen, extensió ni cel·les.

Una selecció activa, un filtre de capa, una edició encara no desada, una variable de projecte, una relació temporal o una capa de memòria també formen part de l'estat. Si condicionen el resultat i no apareixen al contracte, la reexecució pot donar una sortida diferent sense cap error visible. Abans d'automatitzar convé materialitzar el subconjunt necessari o convertir el filtre en un paràmetre o pas explícit.

### Historial, registre i diagnòstic

L'**historial de processament** registra execucions recents, paràmetres i missatges. Permet consultar com es va cridar una eina, repetir-la o recuperar una representació de l'ordre. És especialment útil quan una sortida inesperada obliga a respondre si es va seleccionar una capa equivocada, si la distància era 200 o 2.000, o si l'eina va ometre geometries.

L'historial no conserva una còpia immutable de les entrades. Si `municipis_preparats` s'ha modificat després, repetir la mateixa ordre actua sobre l'estat actual. Tampoc explica per què es va triar un llindar ni demostra que s'hagi inspeccionat el resultat. Una entrada de l'historial pot dir que el procés va acabar sense excepció, però no que la capa tingui sentit territorial. Per això és una font per completar el diari, no un substitut del diari.

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

### El Dissenyador de models

Un model gràfic és un **graf dirigit de dependències**. Les entrades i els paràmetres alimenten algorismes; les sortides d'uns passos es converteixen en entrades dels següents. L'ordre visual de les caixes no determina l'execució: les connexions ho fan. Dues branques independents es poden resoldre sense seguir l'ordre d'esquerra a dreta, mentre que un node no pot començar fins que les dependències necessàries estiguin disponibles.

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
| 3 | `native:buffer` amb `DISTANCE = @distancia_marge_m`, `SEGMENTS = 10`, extrems i unions arrodonits, `MITER_LIMIT = 2` i `DISSOLVE = True` | ROI temporal o persistent, superfície superior a la municipal i distància mostrejada |
| 4 | `gdal:cliprasterbymasklayer` amb ROI, `CROP_TO_CUTLINE = True`, resolució de la font conservada, `NODATA` explícit i tipus de dada preservat | Ràster temporal no buit; resolució, origen, dimensions, `NoData` i rang comparats amb la font |
| 5 | `gdal:slope` sobre la banda 1, `SCALE = 1` si totes les unitats són metres, sortida en graus, fórmula fixada i `COMPUTE_EDGES = False` | GeoTIFF persistent `pendent_roi_graus.tif`, rang de 0° a 90° i vores `NoData` esperades |
| 6 | `native:zonalstatisticsfb` sobre el municipi original, banda 1 i prefix `slope_`, amb recompte, mitjana, desviació, mínim i màxim | Capa o taula persistent amb una fila municipal, recompte vàlid positiu i estadístics dins del rang del ràster |
:::

Els noms anteriors corresponen a QGIS 3.44. El model ha de conservar també tots els paràmetres no mostrats que el proveïdor exposa, encara que mantinguin un valor inicial: mètode de validesa, tractament d'errors, tipus de dada, fórmula de pendent i destinacions. `gdal:cliprasterbymasklayer` pot conservar la mida de cel·la sense garantir per si sol que l'origen coincideixi amb una graella externa; per això la postcondició compara la geotransformació amb la font. Si el cas exigeix una alineació comuna amb altres ràsters, abans cal aplicar el contracte de graella de l'anàlisi ràster.

El marge s'utilitza per calcular el pendent; les estadístiques s'obtenen sobre el polígon municipal original. Calcular-les sobre la ROI respondria una pregunta diferent. A la costa hi pot haver `NoData`, de manera que el recompte de píxels vàlids forma part del resultat. Una mitjana sense aquest denominador podria ocultar que només s'ha observat una part del terme.

La ROI pot ser una sortida persistent perquè fa visible l'àmbit de càlcul. El ràster retallat pot ser temporal si es regenera de manera segura i no és necessari per diagnosticar cap incidència. El GeoTIFF de pendent i la taula zonal són finals analítics; els controls i el diari són finals documentals. Aquesta selecció evita exposar totes les connexions internes sense convertir el procés en una caixa negra.

La prova manual i el model han de coincidir segons controls definits: una entitat municipal, mateixa extensió de ROI, mateixa mida i origen de cel·la, mateix recompte de valors vàlids i estadístiques equivalents dins de la precisió esperada. Si difereixen, cal revisar les seleccions, el tractament de `NoData`, les destinacions i els valors predeterminats. No s'ha de triar el resultat del model només perquè sembla més recent.

El cas és una pràctica per entendre dependències i no un requisit automàtic de la micropràctica final. Quan Moodle no exigeixi cap model, es pot completar com a exercici de laboratori i conservar-ne o no el `.model3` segons la seva utilitat. El tancament del projecte continua tenint com a objecte principal la síntesi verificada de les micropràctiques 1–5.

### Desar, versionar i transportar processos

QGIS permet conservar models al perfil d'usuari, exportar-los com a fitxers `.model3` i, segons el flux utilitzat, associar-los al projecte. Un model inclòs en un projecte viatja amb el `.qgz`, però no incorpora automàticament les fonts, els proveïdors, els complements ni les credencials. Un `.model3` facilita reutilització i comparació de versions, però manté les mateixes dependències externes.

Un model desat només al perfil personal pot desaparèixer del paquet encara que funcioni a l'ordinador d'origen. Si forma part del resultat, cal exportar-lo a la carpeta del projecte, donar-li un nom estable i registrar-ne la versió. El fitxer `.qgz` independent es conservarà encara que el projecte també s'hagi desat dins del GeoPackage, perquè permet revisar la seva estructura i recuperar-lo amb més facilitat.

Les rutes relatives funcionen quan el projecte i les dades mantenen una estructura comuna. No resolen dependències situades fora de l'arrel, connexions amb noms locals ni recursos disponibles només al perfil de QGIS. Abans d'empaquetar cal inventariar totes les fonts des de les propietats del projecte i decidir si cada una s'inclou, es pot tornar a obtenir o només serveix com a context remot. La llicència pot impedir redistribuir una entrada encara que tècnicament càpiga al ZIP.

La **prova de transport** no consisteix a moure només el `.qgz`. S'ha de copiar o comprimir el paquet complet, extreure'l en una carpeta nova que no comparteixi la ruta original i obrir-lo des d'allà. Si és possible, s'utilitzarà un altre perfil o equip. Durant la prova no s'han de reparar manualment les rutes sense registrar-ho, perquè això amagaria una dependència del paquet.

::: table "Protocol de prova de transport"
| Fase | Acció | Criteri d'acceptació |
| --- | --- | --- |
| Preparació | Tancar edicions, desar el `.qgz` i generar el paquet des de la carpeta canònica | No hi ha cap capa pendent ni fitxer temporal imprescindible |
| Aïllament | Extreure el paquet en una ruta nova | El projecte no pot resoldre fonts per coincidència amb la carpeta original |
| Obertura | Obrir el `.qgz` i revisar el registre de missatges | No hi ha fonts perdudes ni proveïdors imprescindibles desconeguts |
| Inventari | Obrir una capa de cada grup, les taules i els ràsters | Esquema, `CRS`, extensió, estils i valors continuen disponibles |
| Procés | Reexecutar una operació o model representatiu, si existeix | Les entrades es resolen i els controls semàntics coincideixen |
| Composició | Obrir i exportar el mapa final | Fonts, llegenda, escala, textos i recursos enllaçats es mantenen |
| Fitxers externs | Obrir l'exportació en un visor diferent | La peça és llegible i no depèn de la sessió de QGIS |
| Registre | Anotar entorn, incidències i resultat de la prova | Una altra persona pot saber què s'ha comprovat i què continua extern |
:::

La versió de QGIS, el sistema operatiu i els proveïdors es registraran quan puguin afectar l'execució. No cal prometre compatibilitat amb qualsevol versió futura, però sí identificar l'entorn validat. Si un model depèn d'un camp que no existeix al municipi següent, ha de fallar de manera interpretable o documentar la preparació necessària; adaptar l'esquema forma part de transferir el mètode, no és un detall aliè.

### Pràctiques de desenvolupament aplicades al projecte

Els fluxos de desenvolupament reproduïble aporten principis útils encara que no s'escrigui codi. El primer és separar entrades originals, dades preparades, resultats regenerables i productes finals. El segon és declarar les dependències: una sortida no apareix «després» d'una altra només pel seu nom, sinó perquè l'utilitza com a entrada. El tercer és corregir sempre la font canònica i tornar a generar els descendents.

Els **controls executables** són comprovacions que una eina podria repetir, com exigir 22 codis únics, una fila concreta de referència, cap geometria buida o una extensió dins d'un rang. No són exclusius de Python: molts es poden expressar amb estadístiques, consultes o expressions de QGIS i registrar en una taula. El valor metodològic és definir la condició abans d'interpretar la sortida i fer que una violació sigui visible.

Una comprovació coneguda o **cas sentinella** ajuda a detectar desplaçaments. Pot ser el codi i el nom d'un municipi, una geometria que ha de quedar dins de la ROI o una cel·la amb valor conegut. No valida tot el conjunt, però revela errors de columna, `CRS`, filtre o ordre. S'ha de combinar amb recomptes, distribucions i mostres, no utilitzar-se com a única prova.

L'automatització es justifica quan redueix una font identificada de variació o cost. Un model pot assegurar que tots els municipis reben el mateix ordre d'operacions; un lot pot evitar errors en trenta conversions; un script pot comprovar esquemes abans de processar. Afegir automatització només per mostrar codi crea una dependència que també s'ha de mantenir. El projecte final es valora per la coherència i l'explicació del procés, no pel nombre de tecnologies que incorpora.

### Límits conceptuals de SQL espacial

SQL descriu operacions sobre conjunts de files. Amb una extensió espacial com PostGIS, les files poden contenir geometries i les consultes poden aplicar predicats, mesures i transformacions. Aquesta aproximació és adequada quan les dades viuen en una base compartida, quan cal combinar filtres temàtics i espacials o quan una consulta s'ha de reutilitzar sense exportar moltes capes intermèdies.

Una consulta pot seleccionar municipis que intersecten almenys una regió d'interès:

::: listing "Predicat espacial expressat en SQL"
```sql
SELECT m.*
FROM municipis AS m
WHERE EXISTS (
    SELECT 1
    FROM roi AS r
    WHERE ST_Intersects(m.geom, r.geom)
);
```
:::

`ST_Intersects` avalua un predicat: retorna cert quan les geometries comparteixen almenys un punt, inclosos determinats contactes de frontera. No retalla la geometria municipal. Per crear la part comuna caldria una operació d'intersecció geomètrica i caldria decidir què fer amb geometries buides, fragments i atributs. La distinció entre seleccionar i transformar és la mateixa que al geoprocessament vectorial, encara que canviï la sintaxi {% cite ogcSimpleFeatures2011 %}.

L'ús de `EXISTS` evita duplicar una fila municipal si coincideix amb diverses files de `roi`. Una unió SQL ordinària podria produir una fila per cada coincidència, cosa que pot ser correcta per analitzar parelles però incorrecta per obtenir un conjunt únic de municipis. La cardinalitat continua sent una decisió analítica. SQL no elimina la necessitat d'entendre claus, nuls i múltiples correspondències.

Assignar un identificador de referència espacial a una geometria no transforma les coordenades. Les dues entrades han d'estar en referències compatibles i qualsevol transformació s'ha de fer explícita. Les mesures de distància i superfície depenen també del tipus geomètric, la projecció i les unitats. Una consulta sintàcticament correcta pot continuar responent una pregunta inadequada si tracta graus com metres o ignora una geometria invàlida.

PostGIS és una extensió de PostgreSQL amb el seu propi catàleg de funcions. Un GeoPackage és un contenidor basat en SQLite, però aquesta base comuna no implica que totes les funcions `ST_...` de PostGIS estiguin disponibles ni que tinguin exactament el mateix comportament. Les capes virtuals de QGIS, SQLite amb extensions espacials i altres motors tenen dialectes i capacitats diferents. Una consulta s'ha de documentar amb el motor i la versió on s'ha provat.

### Límits conceptuals de PyQGIS

PyQGIS és l'API de Python de QGIS. Permet accedir a projectes, capes, geometries, expressions, composicions i al marc de Processament. És útil quan el flux necessita bucles, condicions, validacions, integració amb altres operacions o una eina reutilitzable que el Dissenyador de models no expressa amb claredat. No és sinònim de Python geoespacial en general: el codi depèn de l'entorn i de les classes de QGIS.

Un fragment executable dins de la consola Python de QGIS, una vegada definida una capa `municipi` vàlida en un `CRS` mètric, pot escriure's així:

::: listing "Correspondència entre Processament i PyQGIS"
```python
from qgis import processing

resultat = processing.run(
    "native:buffer",
    {
        "INPUT": municipi,
        "DISTANCE": 500.0,
        "SEGMENTS": 10,
        "END_CAP_STYLE": 0,  # Round
        "JOIN_STYLE": 0,     # Round
        "MITER_LIMIT": 2.0,
        "DISSOLVE": True,
        "OUTPUT": "TEMPORARY_OUTPUT",
    },
)

buffer_roi = resultat["OUTPUT"]
if not buffer_roi.isValid() or buffer_roi.featureCount() == 0:
    raise RuntimeError("El buffer no ha produït cap geometria vàlida")
```
:::

El fragment és executable en l'entorn indicat, però no és un programa autònom: pressuposa que `municipi` identifica una entrada vàlida, no buida, sense selecció imprevista i en metres. El diccionari fa visibles tots els paràmetres geomètrics del buffer i la destinació temporal; `0` és el codi de l'estil arrodonit per a extrems i unions en QGIS 3.44. La comprovació només valida l'existència tècnica de la sortida. No explica per què s'han triat 500 m, no comprova el `CRS` ni demostra la distància sobre una mostra, de manera que el mètode continua necessitant les precondicions i postcondicions declarades fora del codi.

El codi pot versionar-se i comparar-se línia a línia, cosa que ajuda a revisar canvis. Aquesta propietat no incorpora automàticament les dades, la versió de QGIS, els complements ni les biblioteques. Una ruta absoluta dins del script és tan poc transportable com una ruta absoluta dins del `.qgz`. Cal separar configuració i lògica, utilitzar rutes relatives a una arrel coneguda i registrar l'entorn validat quan el procés s'hagi de compartir.

El Dissenyador de models és preferible quan la seqüència és un graf estable, visualment explicable i basat en algorismes disponibles. PyQGIS és preferible quan hi ha lògica iterativa, validacions complexes, noms dinàmics, tractament específic d'errors o integració que el model faria opaca. SQL és preferible quan la consulta de conjunt s'ha d'executar prop d'una base espacial compartida. Cap opció és un nivell obligatori de maduresa: són formes diferents d'expressar un problema.

## Auditoria completa del projecte final

El producte final ha de respondre la pregunta territorial formulada a l'inici i permetre reconstruir com s'ha arribat a la resposta. No és una acumulació de totes les capes creades durant el curs. Conserva les entrades necessàries, els resultats amb una funció clara i els intermedis imprescindibles per auditar decisions o incidències. La resta es pot eliminar del panell o del paquet només després de comprovar que és regenerable i no conté l'única evidència d'un pas crític.

### Pregunta, abast i inventari

La pregunta final ha d'identificar fenomen, municipi, període, unitat d'anàlisi i mesura o relació espacial. Pot haver evolucionat respecte de la proposta inicial, però el canvi s'ha de registrar. Una pregunta sobre «zones adequades» s'ha de reformular com a «zones que compleixen els criteris A, B i C» si no s'han incorporat tots els factors necessaris per afirmar adequació.

L'inventari relaciona cada peça amb una funció: font original, dada preparada, intermedi de diagnòstic, resultat analític, taula de control, mapa o documentació. Una capa sense funció identificable no s'ha de conservar només perquè existeix; una capa necessària no s'ha d'eliminar perquè no apareix al mapa final. El nom, la ubicació, el format, el productor i la dependència immediata han de permetre seguir-ne el llinatge.

::: table "Continuïtat de les micropràctiques dins del projecte final"
| Fase | Evidència acumulada | Pregunta d'auditoria final |
| --- | --- | --- |
| Micropràctica 1 | Pregunta, fonts, estructura, GeoPackage, `.qgz` i prova inicial de trasllat | Les fonts i l'àmbit continuen sent els que sostenen el resultat final? |
| Micropràctica 2 | Capes digitalitzades, esquemes, dominis i controls geomètrics o topològics | Les correccions posteriors conserven identificadors, autoria i regles de captura? |
| Micropràctica 3 | Expressions, extraccions, claus, unions i diagnòstic de nuls | Es poden reconstruir seleccions, cardinalitats i registres sense correspondència? |
| Micropràctica 4 | Criteris vectorials, buffers, superposicions, recomptes i superfícies | L'ordre, les unitats i els llindars continuen justificats i sense doble comptatge? |
| Micropràctica 5 | MDE, graelles, derivats, classes, màscares i estadístiques zonals | Resolució, alineació, `NoData`, referència vertical i sensibilitat estan documentats? |
| Micropràctica 6 | Síntesi, composició, exportació, limitacions i explicació | Cada afirmació final es pot seguir fins a les evidències anteriors? |
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

Si hi ha un lot, model, consulta o script, s'auditarà com una peça addicional, no com a substitut del resultat. Cal comprovar versió, dependències, paràmetres i prova de reexecució. Si no hi ha automatització perquè no era necessària o Moodle no la demana, el projecte pot ser igualment complet sempre que la seqüència manual sigui reconstruïble.

### Estat del projecte QGIS

El projecte `.qgz` ha d'obrir-se sense fonts perdudes. Els grups de capes han de separar originals o referències, dades preparades, resultats vectorials, ràsters i composicions. Les capes temporals, duplicades o descartades s'eliminaran del panell després d'assegurar que no són necessàries. Els noms visibles han de correspondre als noms del registre, encara que una etiqueta més llegible pugui complementar el nom tècnic.

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

Les peces finals tenen funcions complementàries. El GeoPackage reuneix capes vectorials i taules; els GeoTIFF conserven ràsters analítics; el `.qgz` registra organització, estils, relacions i composicions; les exportacions comuniquen una selecció; i el diari conserva decisions, controls i limitacions. Cap peça no substitueix les altres.

::: table "Peces del producte final"
| Peça | Funció i control final |
| --- | --- |
| GeoPackage | Capes i taules amb noms estables, `CRS` identificats, esquemes comprensibles, claus i geometries comprovades |
| Ràsters | GeoTIFF amb procedència, graella, tipus, unitat i `NoData` explícits |
| Projecte `.qgz` | Obertura sense fonts perdudes, grups i estils coherents, rutes transportables i composicions vinculades als resultats correctes |
| Mapes i resultats exportats | Pregunta, àmbit, fonts, unitats, període i interpretació llegibles fora de QGIS |
| Diari d'activitats | Fonts, operacions, paràmetres, incidències, controls, decisions, procedència i limitacions relacionats |
| Procés opcional | Historial, lot, `.model3`, consulta o script amb dependències i prova de reexecució, si s'ha desenvolupat o s'ha exigit |
| Explicació oral | Justificació d'una mostra del procés, diferència entre dades i inferències i resposta sobre autoria i límits |
:::

La neteja final es farà sobre una còpia controlada del projecte. Abans de descartar una capa cal comprovar que es pot regenerar, que no alimenta cap composició i que no és l'única evidència d'un pas. Després es repetirà l'inventari, es desaran totes les peces, es tancarà QGIS i s'executarà la prova de transport. Una capa que només existeix perquè continuava oberta a la memòria quedarà així detectada abans del lliurament.

## Activitats

### Comprovació: reconstruir una execució

Cal triar una operació de l'historial i reconstruir-ne el proveïdor i identificador, les entrades, les precondicions, els paràmetres, l'estat rellevant i la destinació. Després s'ha d'explicar quina informació necessària per interpretar el resultat no apareix al registre. La comprovació acaba repetint l'operació sobre una còpia i comparant un control semàntic, no només el nom del fitxer.

### Pràctica guiada opcional: manual, lot i model

Una extracció municipal s'executarà amb `native:extractbyexpression` sobre la capa preparada i el camp textual `codi_muni`. La primera execució usarà l'expressió `attribute(@feature, 'codi_muni') = '43171'`, una sortida persistent `municipi_43171` i el control d'una sola entitat. Després s'executarà per lots per a tres codis vàlids de la capa, amb una expressió i un nom de sortida únic a cada fila, i s'afegirà deliberadament un codi inexistent que s'ha de registrar com a resultat buit no validat. Finalment es construirà un model de pràctica amb `codi_municipi` com a paràmetre de text, la mateixa expressió i una postcondició d'una sola entitat. Cal comparar què expressa cada modalitat, com es generen els noms de sortida i quin mecanisme representa dependències. El model no forma automàticament part del lliurament final; serveix per aprendre a formalitzar una operació ja validada.

### Pràctica guiada: prova de transport adversa

Sobre una còpia del paquet es provocarà una dependència controlada, com una capa situada fora de l'arrel o un nom de camp no disponible. El projecte s'obrirà des d'una carpeta nova, es diagnosticarà el problema sense reconstruir-lo per intuïció i es corregirà a la font o al contracte. El diari registrarà símptoma, causa, correcció i controls repetits.

### Micropràctica 6: síntesi i tancament del projecte

La sisena micropràctica és la síntesi final de les cinc anteriors. El nucli obligatori és auditar, ordenar, interpretar, compondre i transportar el projecte acumulatiu. L'automatització només serà obligatòria si Moodle ho indica explícitament per al lliurament vigent.

::: table "Contracte de la micropràctica 6"
| Component | Requisit |
| --- | --- |
| Entrades | GeoPackage, projecte `.qgz`, diari i resultats conservats de les micropràctiques 1–5 |
| Operacions mínimes | Ordenar i netejar el projecte, auditar fonts i dependències, repetir els controls crítics, preparar la simbolització, compondre i exportar almenys un mapa i documentar les limitacions |
| Resultats | GeoPackage final, GeoTIFF necessaris, projecte `.qgz` transportable, mapes o resultats exportats i diari complet |
| Evidències del diari | Inventari i llinatge finals, relació entre pregunta i resultats, controls repetits, incidències, decisions de neteja, limitacions, prova de transport i guió breu de l'explicació oral |
| Comprovacions | Absència de fonts perdudes, esquemes i `CRS` identificats, resultats traçables, ràsters documentats, composició llegible i obertura correcta des d'una altra ubicació |
| Fitxers que cal conservar | GeoPackage, projecte `.qgz`, ràsters finals, exportacions, diari i, només si s'ha desenvolupat o requerit, model `.model3`, consulta o script |
:::

Quan Moodle no exigeixi automatització, no cal crear un model artificial per completar la micropràctica. Es pot conservar l'historial com a suport de documentació i utilitzar el model guiat del capítol com a exercici separat. La qualitat del tancament es demostrarà amb la cadena d'evidència, els controls, la composició, la prova de transport i l'explicació oral.

### Activitat integradora

Com a assaig de síntesi, es pot resoldre un cas que reuneixi les peces del curs: obtenir les capes oficials, delimitar una zona circular de 2 km al voltant d'un punt de referència de Vila-seca, digitalitzar a escala 1:500 una xarxa de carrils bici topològicament connectada i localitzar àrees candidates per a un equipament termal. El model de candidatura pot exigir una distància superior a 600 m de l'AP-7 i l'A-7, inferior a 50 m d'altres vies i inferior a 200 m d'assentaments, sempre com a criteris de l'exercici i no com a norma general.

El cas incorporarà un model d'elevacions i conservarà les capes vectorials i les taules en un únic GeoPackage. Els ràsters es mantindran com a GeoTIFF llevat que l'enunciat exigeixi i validi explícitament una cobertura ràster dins del GeoPackage. El projecte `.qgz` independent i una nota tècnica permetran revisar fonts, topologia, paràmetres, resultats i limitacions.

Com a ampliació, una part estable del flux es pot repetir amb un lot o un model, i els resultats s'han de contrastar amb la versió manual. Aquesta automatització és opcional tret que Moodle la converteixi explícitament en requisit. Moodle concretarà també si l'assaig forma part d'una prova, una pràctica o una activitat no avaluable; el manual conserva el cas com a síntesi transferible i no com a calendari de lliurament.
