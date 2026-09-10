---
layout: manual-chapter
title: Consultes i dades relacionals
description: Seleccions, filtres, expressions, claus, unions i relacions per interrogar dades territorials sense perdre'n l'estructura.
lang: ca
ref: manual-queries-relational-data
profiles: [unaltremanual]
content_status: draft
permalink: /ca/chapters/consultes-dades-relacionals/
weight: 60
part: Continguts
manual_references: true
---

Una capa pot contenir milers d'entitats, però una pregunta acostuma a referir-se a un subconjunt o a una relació concreta. Identificar els municipis d'una província, els centres educatius d'un terme o els registres sense codi exigeix convertir el criteri verbal en una expressió verificable. La consulta no modifica necessàriament les dades: defineix quines files compleixen una condició.

Les dades territorials també es reparteixen entre taules. Una geometria municipal pot contenir un codi estable i una taula estadística pot utilitzar el mateix codi per registrar població, habitatge o activitat. Relacionar-les correctament exigeix entendre tipus de dades, valors absents, claus i cardinalitats abans d'executar una unió {% cite longleyGeographicInformationScience2015 %}.

>>>>> En acabar el capítol, cal poder consultar i relacionar taules territorials amb expressions que produeixin resultats comprovables.
>>>>>
>>>>> - Construir condicions amb comparacions, lògica booleana i tractament explícit de `NULL`.
>>>>> - Distingir selecció, filtre, representació i extracció persistent.
>>>>> - Preparar claus estables i diagnosticar duplicats o registres sense correspondència.
>>>>> - Diferenciar unions 1:1 o N:1, relacions 1:N i unions espacials.

## Llegir l'esquema abans de consultar

Una taula d'atributs és una representació estructurada: cada fila correspon a una unitat d'observació i cada camp descriu una propietat definida per a aquesta unitat. En una capa municipal, una fila pot representar un municipi vigent en una data determinada; en una taula de centres, una fila pot representar un establiment; i en una sèrie temporal, una fila pot representar una combinació de municipi, any i variable. Si no es coneix què representa una fila, no es pot interpretar ni un recompte ni una coincidència.

L'**esquema** especifica els camps disponibles, el nom que els identifica, el tipus de dada, la possibilitat d'admetre valors nuls, les restriccions i, quan existeix, el domini de valors. L'àlies visible a QGIS pot ser més llegible que el nom físic, però les expressions acostumen a referir-se al nom real. També cal distingir un valor emmagatzemat d'un valor que QGIS presenta amb un formulari, una relació de valors o una unitat afegida a la interfície. La visualització pot traduir un codi sense modificar el contingut de la font.

Els noms de camps entre cometes dobles que apareixen a les expressions d'aquest capítol són **didàctics**. Serveixen per fer explícits els tipus i les operacions, però no anticipen l'esquema físic de cap producte oficial. Abans d'adaptar-los a una font descarregada cal inspeccionar l'edició concreta, identificar les capes i taules que conté i llegir els noms, tipus, dominis i definicions dels camps a les metadades disponibles.

::: table "Tipus d'atribut i decisions de consulta"
| Tipus | Valors que representa | Operacions coherents | Error habitual |
| --- | --- | --- | --- |
| Enter | Recomptes, ordres o codis estrictament numèrics | Comparació, suma, recompte i aritmètica | Utilitzar-lo per a codis amb zeros inicials |
| Decimal | Mesures que poden tenir fracció | Aritmètica, rangs, estadístiques i arrodoniment | Comparar-lo com si fos text o atribuir significat als decimals de presentació |
| Text | Noms, categories, identificadors i observacions | Coincidència, patrons, longitud, substitució i normalització | Ordenar nombres codificats com a text com si fossin magnituds |
| Booleà | Dos estats lògics, a més d'una possible absència | Condició directa, negació i combinació lògica | Confondre `FALSE`, `0`, cadena buida i `NULL` |
| Data | Dia del calendari | Comparació cronològica, extracció d'any o mes i intervals | Importar-la com a text amb ordre ambigu |
| Data i hora | Instant o marca temporal | Ordenació, durades i agrupació temporal | Ometre la zona horària o barrejar hores locals i UTC |
| Geometria | Posició i forma associades a la fila | Mesura, construcció i predicats espacials | Confondre el símbol visible amb la geometria real |
| Binari o estructurat | Documents, objectes o valors codificats | Funcions específiques del format | Tractar-lo com un text ordinari sense conèixer-ne l'estructura |
:::

En QGIS, l'esquema es comprova abans d'escriure cap expressió obrint la taula d'atributs: les capçaleres identifiquen camps i cada fila correspon a una entitat. La captura mostra també per què `codi_muni` s'ha de llegir com una clau textual i no com una magnitud.

![Taula d'atributs del límit municipal de Vila-seca amb una fila, el camp nom_muni i la clau codi_muni identificats]({{ site.baseurl }}/assets/img/qgis/qgis-attribute-table.png "La fila representa una entitat municipal; cada columna descriu una variable, i codi_muni actua com a clau de text per relacionar-la amb altres taules sense confondre-la amb una magnitud."){: data-figure-width-web="46rem" data-figure-width-pdf="95%"}

El tipus s'ha de triar pel significat, no per l'aparença. Un codi municipal format només per dígits continua sent un identificador si no té sentit sumar-lo, obtenir-ne una mitjana o ordenar-lo per magnitud. Conservar-lo com a text permet mantenir zeros inicials i comparar-lo amb la codificació oficial. En canvi, una població importada com a text no admet directament operacions aritmètiques fiables, encara que totes les cel·les semblin nombres.

Els dominis defineixen quins valors són admesos. Si el camp `estat` només pot contenir `actiu`, `inactiu` o `pendent`, les variants `Actiu`, `ACTIU`, `act.` i una cadena amb espais finals no són categories noves, sinó possibles incompliments del domini. Una consulta pot detectar-les, però la correcció exigeix saber quina forma és oficial i conservar la dada original o una traça de la transformació.

### Zero, cadena buida i valor absent

`NULL`
: Valor absent o desconegut dins del model de dades.

Zero
: Valor numèric que pot ser una observació vàlida, com cap centre comptat.

Cadena buida `''`
: Text present amb longitud zero.

Codi sentinella
: Literal com `-9999` que només indica absència quan el diccionari de la font ho declara.

El text `'NULL'` i una data fictícia tampoc no són valors nuls. Substituir indiscriminadament aquestes representacions altera el significat de la dada.

L'absència també pot tenir causes diferents. Un valor pot no haver-se observat, no ser aplicable, estar protegit per confidencialitat, haver fallat en una importació o quedar pendent d'actualització. Una sola marca nul·la no conserva aquestes causes. Si la distinció és analíticament necessària, convé afegir un camp d'estat o utilitzar els indicadors de qualitat que proporcioni la font, en lloc d'inventar una xifra que després entrarà en sumes i mitjanes.

## De la pregunta al predicat

Predicat
: Expressió que avalua una condició per a cada registre i retorna `TRUE`, `FALSE` o `NULL`.

Si $U$ és el conjunt de files disponibles i $P$ és el predicat, la selecció resultant és $S_P=\{r\in U\mid P(r)=\mathrm{TRUE}\}$. Només les files amb resultat `TRUE` entren a $S_P$.

Els operadors `AND`, `OR` i `NOT` tenen una lectura de conjunts. Per a predicats sense valors desconeguts, $S_{A\ \mathrm{AND}\ B}=S_A\cap S_B$, $S_{A\ \mathrm{OR}\ B}=S_A\cup S_B$ i $S_{\mathrm{NOT}\ A}=U\setminus S_A$. `AND` exigeix pertinença a tots dos conjunts, `OR` n'admet qualsevol i `NOT` demana el complement. La fórmula del complement necessita una precisió quan hi ha `NULL`, perquè negar un resultat desconegut no el converteix en cert.

::: listing "Primers predicats de consulta en QGIS"
```text
"nom_muni" = 'Vila-seca'

"poblacio" > 20000

"codi_prov" = '43'
AND "poblacio" > 20000

"nom_muni" IS NULL
```
:::

Les dues primeres expressions comparen un sol camp amb un literal. La tercera afegeix `AND` només després de provar per separat la província i el llindar de població. La quarta comprova una absència real; no compara el camp amb el text `'NULL'`. Cada pas s'ha de verificar amb el recompte seleccionat abans d'afegir una altra condició.

Els noms de camp de l'exemple són il·lustratius. Abans de reutilitzar una expressió cal inspeccionar l'esquema real, perquè `43` pot estar emmagatzemat com a text o com a enter i el nom municipal pot seguir una convenció diferent. Normalitzar majúscules i espais ajuda a explorar textos, però no substitueix una clau oficial.

Les expressions de QGIS s'assemblen a SQL, però no són sempre el mateix llenguatge. La selecció per expressió i la calculadora de camps utilitzen el motor de QGIS; un filtre de capa delegat a una base de dades pot aplicar el dialecte, les conversions i la semàntica del proveïdor. Cal conservar l'expressió exacta, l'eina, el proveïdor i el context on s'ha executat {% cite qgisUserGuide344 %}.

### Camps, literals, operadors i funcions

Una expressió combina referències a camps, literals, operadors i funcions.

A `round("superficie", 2)`, `"superficie"` és un camp, `2` és un literal enter i `round()` és una funció. A `"nom_muni" = 'Vila-seca'`, l'operador `=` compara el valor del camp amb un literal de text. Escriure `'nom_muni' = 'Vila-seca'` compararia dos textos constants i no consultaria cap columna.

::: table "Operadors habituals en una consulta atributiva"
| Família | Forma orientativa | Pregunta que expressa | Precaució |
| --- | --- | --- | --- |
| Igualtat | `"tipus" = 'residencial'` | El valor coincideix exactament? | Tipus, majúscules, accents i espais formen part de la comparació |
| Desigualtat | `"estat" != 'baixa'` | El valor conegut és diferent? | Els nuls no es converteixen en diferents |
| Ordre | `"places" >= 10` | El nombre arriba al llindar? | Sobre text, l'ordre és lexicogràfic, no numèric |
| Interval | `"valor" BETWEEN 10 AND 20` | El valor queda dins d'un interval inclusiu? | Cal declarar bé els extrems i tractar els nuls |
| Pertinença | `"ref" IN ('A', 'B', 'C')` | El valor pertany a una llista? | Tots els literals han de ser compatibles amb el camp |
| Patró | `"nom" LIKE 'Can %'` | El text segueix un patró sensible a majúscules? | `%` representa qualsevol seqüència i `_`, un caràcter |
| Patró sense caixa | `"nom" ILIKE 'can %'` | El patró ignora majúscules i minúscules? | No resol per si sol accents, abreviatures ni variants toponímiques |
| Absència | `"data_baixa" IS NULL` | Falta el valor? | `= NULL` no és una prova d'absència vàlida |
| Lògica | `NOT`, `AND`, `OR` | Com es neguen o combinen les condicions? | La precedència pot canviar el conjunt resultant |
:::

Una sintaxi vàlida no assegura una consulta correcta. `"ref" > '10'` pot executar-se sobre un camp de text i ordenar lexicogràficament, de manera que `'2'` pot quedar després de `'10'`. Convertir amb `to_int()` només és legítim si tots els valors que s'han de conservar representen enters i si els zeros inicials no tenen funció identificadora. La previsualització del constructor ajuda a detectar errors, però la decisió depèn del diccionari de dades.

### Una expressió de QGIS com a programa elemental

Una expressió és el nivell més elemental de programació dins de molts fluxos de QGIS. Rep **entrades** tipades —camps de la fila actual, literals, geometria i variables del context—, les transforma amb operadors i funcions, pot prendre una branca amb `CASE` i retorna un únic **valor de sortida**. En una selecció o un filtre de QGIS s'espera un resultat lògic; en la calculadora de camps, un valor compatible amb el tipus del camp; en una etiqueta, habitualment text. La mateixa sintaxi pot ser inadequada si canvien el tipus esperat o la unitat.

::: listing "Entrada, operació i sortida d'una expressió elemental"
```text
"places" > 0
```
:::

En aquest cas, `"places"` és l'entrada llegida de la fila actual, `0` és un literal, `>` és l'operació i el resultat és `TRUE`, `FALSE` o `NULL`. El **context d'expressió** determina quins camps i variables estan disponibles, però els primers exemples només necessiten camps de la fila i literals. La geometria, les variables locals, les agregacions i `@parent` s'introdueixen més endavant, quan la pregunta ja no es pot resoldre amb una comparació directa.

## Lògica de tres valors i `NULL`

En una lògica booleana ordinària, una proposició és certa o falsa. Una base de dades necessita un tercer resultat per a comparacions que no es poden decidir perquè falta una dada. Si `"places"` és `NULL`, tant `"places" > 0` com `"places" <= 0` retornen `NULL`: no hi ha evidència per afirmar cap de les dues condicions. Una selecció conserva les files en què el predicat és `TRUE`; les que produeixen `FALSE` o `NULL` queden sense seleccionar, encara que les causes siguin diferents.

En una conjunció, una condició falsa basta per saber que el conjunt és fals, encara que l'altra sigui desconeguda; per això `FALSE AND NULL` és `FALSE`. En una disjunció, una condició certa basta per saber que el conjunt és cert; per això `TRUE OR NULL` és `TRUE`. En canvi, `NOT NULL` continua sent `NULL`, perquè negar allò que es desconeix no aporta informació.

Si $N_A$ és el conjunt de files on $A$ retorna `NULL`, aleshores $S_{\mathrm{NOT}\ A}=U\setminus(S_A\cup N_A)$, no tot allò que ha quedat sense seleccionar amb $A$. Les files desconegudes no pertanyen ni a $S_A$ ni a $S_{\mathrm{NOT}\ A}$. Una partició exhaustiva exigeix tractar-les amb una branca explícita, per exemple `A IS NULL`, i decidir si formen un grup de revisió o tenen una interpretació definida pel model.

Comparar un nul amb qualsevol valor, inclòs un altre nul, no produeix una igualtat certa. Per comprovar absència s'utilitzen `IS NULL` i `IS NOT NULL`. Aquest comportament també explica un parany de `NOT IN`: si la llista conté un `NULL`, una fila que no coincideix amb cap valor conegut pot donar un resultat desconegut en lloc de `TRUE`. Les llistes de consulta han de contenir valors explícits i l'absència s'ha de tractar en una condició separada.

>>>> `NOT` no recupera les files amb valors nuls: `NOT ("estat" = 'actiu')` continua retornant `NULL` quan `"estat"` és `NULL`. Si els absents s'han d'incloure, cal afegir `OR "estat" IS NULL` i documentar que s'han agrupat els valors coneguts diferents amb els desconeguts.

`coalesce()` retorna el primer argument que no és nul. És adequat quan el model defineix una substitució real, com ara construir una etiqueta que mostri `'sense nom'` en lloc d'un buit. No converteix l'absència en una observació. Fer `coalesce("places", 0)` abans d'una suma afirma que tot valor absent equival a cap plaça; aquesta afirmació només és defensable si la font ho estableix. Si no, el càlcul amaga la diferència entre zero i desconegut.

::: table "Combinacions de la lògica de tres valors"
| A | B | `NOT A` | `A AND B` | `A OR B` |
| --- | --- | --- | --- | --- |
| `TRUE` | `TRUE` | `FALSE` | `TRUE` | `TRUE` |
| `TRUE` | `FALSE` | `FALSE` | `FALSE` | `TRUE` |
| `TRUE` | `NULL` | `FALSE` | `NULL` | `TRUE` |
| `FALSE` | `TRUE` | `TRUE` | `FALSE` | `TRUE` |
| `FALSE` | `FALSE` | `TRUE` | `FALSE` | `FALSE` |
| `FALSE` | `NULL` | `TRUE` | `FALSE` | `NULL` |
| `NULL` | `TRUE` | `NULL` | `NULL` | `TRUE` |
| `NULL` | `FALSE` | `NULL` | `FALSE` | `NULL` |
| `NULL` | `NULL` | `NULL` | `NULL` | `NULL` |
:::

### Exemple resolt: predir tres resultats

La taula següent és un conjunt didàctic, no un inventari territorial real. Conté expressament un zero, una cadena buida i valors nuls per poder resoldre les expressions fila per fila.

::: table "Registres sintètics per resoldre expressions amb valors absents"
| `id` | `nom` | `places` | `data_baixa` |
| --- | --- | ---: | --- |
| `A` | `Centre Nord` | `12` | `NULL` |
| `B` | `centre sud ` | `0` | `2026-06-30` |
| `C` | `NULL` | `NULL` | `NULL` |
| `D` | `''` | `8` | `NULL` |
:::

Per a `"places" > 0`, les files A i D donen `TRUE`, B dona `FALSE` i C dona `NULL`. Per a `"nom" IS NULL OR trim("nom") = ''`, A i B donen `FALSE`, mentre que C i D donen `TRUE`: la primera branca detecta el nul i la segona, el text de longitud zero. La distinció quedaria amagada si totes dues formes s'haguessin convertit prèviament al mateix literal.

La condició `"data_baixa" IS NULL AND "places" > 0` selecciona A i D. B dona `FALSE` perquè no compleix cap branca. C dona `NULL`: és cert que no consta una data de baixa, però no es pot determinar si les places superen zero. Si el criteri del projecte estableix que els registres sense nombre de places s'han de revisar separadament, aquesta fila no s'ha de forçar ni a la selecció ni a l'exclusió definitiva.

## Precedència i agrupació de condicions

Els operadors `NOT`, `AND` i `OR` neguen, combinen o ofereixen alternatives. La precedència habitual és `NOT`, després `AND` i finalment `OR`, però els parèntesis fan explícita la intenció i eviten lectures equivocades. Així, `A OR B AND C` s'avalua com `A OR (B AND C)`, no com `(A OR B) AND C`.

La diferència és territorial, no només sintàctica. Si A significa «és una biblioteca», B «és un centre cívic» i C «té accessibilitat verificada», la primera lectura accepta totes les biblioteques i només els centres cívics accessibles. La segona exigeix accessibilitat tant a biblioteques com a centres cívics. Cap versió és universalment correcta: la pregunta ha d'indicar quin criteri es vol aplicar.

::: listing "Dues consultes vàlides amb significats diferents"
```text
"tipus" = 'biblioteca'
OR ("tipus" = 'centre_civic' AND "accessible" = TRUE)

("tipus" IN ('biblioteca', 'centre_civic'))
AND "accessible" = TRUE
```
:::

Quan intervé `NULL`, la negació no recupera automàticament les files excloses. Si `"estat" != 'actiu'`, els estats nuls produeixen `NULL`, no `TRUE`. Per demanar explícitament «qualsevol registre que no consti com a actiu, inclosos els que no tenen estat», cal escriure una condició com `"estat" != 'actiu' OR "estat" IS NULL`. Aquesta formulació obliga a reconèixer que s'estan agrupant dues situacions diferents.

## Famílies d'expressions

El constructor de QGIS agrupa funcions per famílies, però una mateixa expressió en pot combinar diverses. No cal memoritzar-ne el catàleg: cal identificar el tipus d'entrada, el tipus de sortida, el tractament dels nuls i la unitat. La documentació vinculada des del mateix constructor permet comprovar la signatura i el comportament de cada funció en la versió utilitzada {% cite qgisUserGuide344 %}.

### Text, patrons i normalització

Les funcions de text serveixen per inspeccionar, netejar, etiquetar i preparar camps. `trim()` elimina espais inicials i finals; `upper()` i `lower()` canvien la caixa; `replace()` substitueix una seqüència; `length()` compta caràcters; i `regexp_replace()` permet aplicar un patró regular quan una substitució simple no basta. La concatenació amb `||` o amb una funció específica construeix etiquetes, però convé comprovar què passa quan algun component és nul.

::: listing "Patrons de text amb finalitats diferents"
```text
trim(upper(coalesce("nom_muni", '')))

"nom_muni" ILIKE 'vila%'

length(trim(coalesce("observacio", ''))) = 0

replace(trim("codi_font"), ' ', '')
```
:::

La primera expressió produeix una forma de comparació, però no hauria de sobreescriure automàticament el topònim oficial. `upper()` no elimina accents, `trim()` no corregeix espais dobles interiors i una substitució pot esborrar signes distintius. La pràctica més segura és conservar el camp original, crear una clau preparada en un camp nou i documentar les regles aplicades.

`LIKE` utilitza `%` per representar una seqüència de qualsevol longitud i `_` per representar un sol caràcter. Per tant, `'Vila%'` inclou qualsevol text que comenci així, no només Vila-seca. Un patró pot ser útil per descobrir variants, però no és una identificació inequívoca. Abans d'utilitzar-lo per extreure dades convé inspeccionar la llista de valors únics que compleixen la condició.

### Nombres, conversions i condicionals

Les expressions numèriques permeten calcular diferències, proporcions, densitats i classes. `abs()` elimina el signe, `round()` controla els decimals mostrats o emmagatzemats i `to_int()` o `to_real()` converteixen valors quan la conversió està justificada. Arrodonir no augmenta l'exactitud i convertir un text defectuós pot produir un nul; després de qualsevol conversió cal comptar quantes files no s'han pogut transformar.

Una expressió condicional defineix què passa en cada cas. `CASE` és preferible quan hi ha diverses branques o quan es vol fer visible el tractament d'absències i límits. L'ordre importa: s'avalua de dalt a baix i s'aplica la primera condició certa. Els intervals han de ser complets i no contradictoris, i la branca `ELSE` no s'ha d'utilitzar com una paperera per a valors que encara no s'han inspeccionat.

::: listing "Classificació que conserva els casos no avaluables"
```text
CASE
  WHEN "valor" IS NULL THEN NULL
  WHEN "valor" < 0 THEN 'revisar'
  WHEN "valor" < @llindar THEN 'per_sota'
  ELSE 'igual_o_per_sobre'
END
```
:::

### Dates, hores i períodes

Una data s'ha de comparar com a data, no com una cadena amb format ambigu. L'ordre lexicogràfic d'un text només coincideix amb l'ordre cronològic en formats controlats com l'ISO `AAAA-MM-DD`, i encara no converteix el camp en un tipus temporal. Funcions com `to_date()`, `year()`, `month()` i els operadors d'interval permeten treballar amb el calendari, sempre que la conversió i la zona temporal siguin conegudes.

::: listing "Consultes temporals amb límits explícits"
```text
"data_obs" >= to_date('2026-01-01')
AND "data_obs" < to_date('2027-01-01')

year("data_obs") = 2026

"data_alta" <= @data_referencia
AND ("data_baixa" IS NULL OR "data_baixa" > @data_referencia)
```
:::

La primera consulta utilitza un interval semiobert: inclou el primer dia de 2026 i exclou el primer de 2027. Aquest patró evita haver d'inventar l'última hora del darrer dia quan el camp conté data i hora. La tercera consulta defineix quins registres constaven actius en una data de referència; que no hi hagi `data_baixa` s'interpreta com a vigència oberta només perquè el model ho declara expressament.

### Geometria i context espacial

Les expressions espacials accedeixen a la geometria de la fila mitjançant `$geometry` i poden obtenir-ne mesures o relacions. `$area`, `$length`, `area()`, `length()`, `perimeter()`, `centroid()` o `point_on_surface()` responen preguntes diferents. En QGIS, les variables `$area`, `$length` i `$perimeter` utilitzen els paràmetres d'el·lipsoide i unitats del projecte, mentre que `area()`, `length()` i `perimeter()` calculen planarment sobre la geometria i en les unitats del seu CRS. Per això s'ha de conservar la funció exacta, el CRS, la configuració de mesura i la unitat resultant {% cite qgisUserGuide344 %}.

Els predicats `intersects()`, `within()`, `contains()`, `touches()`, `overlaps()` i `crosses()` comparen geometries i retornen un valor lògic. Una expressió també pot recuperar geometries d'una altra capa o fer una consulta de superposició, però aleshores el nom de la capa, el context, les coincidències múltiples i el cost de càlcul passen a formar part del procediment. El capítol següent desenvolupa la semàntica topològica d'aquests predicats.

## Seleccionar, filtrar o extreure

Una mateixa condició pot tenir efectes diferents segons on s'apliqui. Aquesta decisió afecta els recomptes, la visualització, les eines de processament i la persistència del resultat.

::: table "Efectes de diferents maneres d'aplicar una condició"
| Operació | Efecte | Persistència | Risc habitual |
| --- | --- | --- | --- |
| Selecció | Marca entitats dins del conjunt actiu de la capa | Temporal; un `.qgz` ordinari no en conserva de manera fiable la llista com a resultat | Un algorisme pot usar només la selecció sense que el criteri quedi documentat |
| Filtre de capa o del proveïdor | Limita les entitats que la capa exposa al projecte | Pot quedar configurat al projecte o a la definició de la font | Canvia recomptes i entrades posteriors, i pot usar un dialecte diferent del motor d'expressions de QGIS |
| Filtre de la taula | Limita les files visibles al panell d'atributs | Estat d'inspecció normalment temporal | Es pot confondre amb un filtre de capa encara que el mapa i els algorismes continuïn rebent totes les entitats |
| Regla de simbologia | Canvia l'aparença | Es conserva amb l'estil | Les entitats continuen existint encara que no siguin visibles |
| Extracció al GeoPackage | Crea una capa o taula nova amb el subconjunt | Persistent després de desar-la | Duplica dades i necessita nom, identificadors, procedència i controls propis |
:::

Abans d'interpretar un resultat cal comprovar el nombre total a la font, el nombre que exposa la capa, el nombre visible a la taula i el nombre seleccionat. Una selecció espacial o atributiva és una hipòtesi reversible; una extracció és un nou conjunt de dades que s'ha de documentar i validar.

### La selecció com a estat de treball

Una selecció marca files dins del conjunt que la capa exposa sense eliminar-les ni crear una font nova. Pot provenir d'un clic al mapa, d'una selecció per valor, d'una expressió o d'una relació espacial. Les modalitats manuals són adequades per inspeccionar un cas, però no constitueixen per si soles un criteri reproduïble. Si la selecció participa en un resultat, cal poder reconstruir-la mitjançant una expressió, una llista d'identificadors estables justificats o un procediment espacial documentat. Un filtre de capa previ pot impedir que determinades files arribin a ser candidates a la selecció.

### Filtre de capa, filtre de taula i simbologia

Un **filtre de capa** o subconjunt del proveïdor limita les entitats que la capa ofereix al projecte. Pot reduir transferència i processament quan la font l'executa de manera eficient, però també altera recomptes, valors únics, extensions i operacions posteriors. Segons el proveïdor, la condició pot ser una cadena de subconjunt amb sintaxi SQL pròpia, no una expressió de QGIS. El projecte ha de conservar-ne la definició exacta i la font on s'ha avaluat.

Un **filtre de la taula d'atributs** acostuma a controlar quines files es mostren al panell: totes, seleccionades, visibles al mapa o coincidents amb una expressió de cerca. La seva funció principal és inspeccionar. No s'ha de suposar que redueix les entitats renderitzades o l'entrada d'un algorisme; cal comprovar l'abast exacte de l'opció i la versió de QGIS.

>>>> Una taula filtrada no implica una capa filtrada. Abans d'informar un recompte o executar un procés cal comprovar separadament el mode de la taula, el filtre de capa i la selecció activa; el nombre de files visibles al panell no defineix necessàriament l'entrada de l'algorisme.

Una **regla de simbologia** decideix com es dibuixa una entitat i pot deixar-la sense símbol. Això no la treu de la taula, d'una selecció ni d'un càlcul. Fer transparent una categoria tampoc no l'exclou de l'anàlisi. Quan un mapa sembla mostrar el mateix subconjunt que un filtre, la comprovació decisiva és comparar el nombre d'entitats disponibles per a una eina, no només l'aparença del llenç.

### Extreure és crear una dada derivada

Una extracció materialitza les files que compleixen el criteri en una capa o taula nova. Quan forma part del projecte acumulatiu, la sortida s'ha de desar al mateix GeoPackage amb un nom intern estable, conservar l'identificador de l'entrada i registrar el criteri i el recompte; una sortida temporal no és un resultat retingut.

`Extract by expression` i `Extract by attribute` formalitzen criteris atributius. `Extract by selection` materialitza l'estat seleccionat, mentre que `Extract by location` aplica una relació espacial. Totes treballen dins del marc de Processament. Els noms visibles poden variar amb la llengua o la versió; el parell **proveïdor:identificador**, com `native:extractbyexpression`, identifica de manera més estable l'algorisme executat. Una sortida temporal continua sent derivada, però desapareixerà si no es desa; una sortida al GeoPackage necessita un nom, una procedència, un esquema i controls propis {% cite qgisUserGuide344 %}.

### Exemple resolt: una condició, cinc efectes

En una capa didàctica amb camps `tipus` i `estat_rev`, l'expressió `"tipus" = 'fanal' AND "estat_rev" = 'validat'` identifica les files que compleixen tots dos criteris. Com a selecció, aquestes files queden marcades dins del conjunt actiu. Com a filtre de capa, només les coincidències s'ofereixen al mapa i als processos posteriors. Com a filtre de taula, només se'n redueix la inspecció al panell. Com a regla de simbologia, es dibuixen les coincidències però les altres entitats continuen disponibles. Com a extracció desada al GeoPackage, es crea un conjunt persistent que conserva els identificadors d'origen i necessita un recompte propi.

## Claus i cardinalitats

Clau primària
: Identifica cada fila d'una taula de manera única, estable i no nul·la.

Clau forana
: Referencia la clau d'una altra taula i permet establir-hi una relació.

Clau candidata
: Camp o combinació de camps que podria identificar cada fila; una taula en pot tenir diverses.

Clau substituta
: Identificador creat pel sistema que simplifica referències internes, però no reemplaça necessàriament el codi oficial d'integració.

Per relacionar claus, els valors i els tipus han de ser compatibles: el text `'043'` no és equivalent automàticament a l'enter `43`. La clau candidata triada pel model esdevé la primària; les altres poden conservar una restricció d'unicitat.

No qualsevol camp compartit és una clau. `nom_muni` pot contenir homònims, variants lingüístiques, canvis històrics i errors tipogràfics; `codi_prov` es repeteix per a tots els municipis d'una província. Aquests camps poden servir per validar o agrupar, però no identifiquen necessàriament una fila. Una unió basada en un camp no únic pot triar una coincidència arbitrària, repetir files o perdre observacions segons l'eina.

Quan cap camp individual identifica la unitat, es pot definir una **clau composta**. En una taula anual municipal, la combinació `(codi_muni, any)` pot ser única encara que cada component es repeteixi. En una taula llarga multivariable pot caldre `(codi_muni, data_ref, variable)`. Abans de concatenar els components en un text, convé comprovar si el format o l'eina admeten relacions multicamp; si es concatena, cal usar separadors i formats que no produeixin col·lisions.

La **cardinalitat** descriu quantes files d'una taula poden correspondre a una fila de l'altra:

::: table "Cardinalitats i tractament adequat"
| Relació | Exemple | Tractament |
| --- | --- | --- |
| 1:1 | Un municipi i una fitxa vigent única | Unió directa si totes dues claus són úniques |
| N:1 | Molts centres i un municipi de pertinença | Afegir dades municipals a cada centre |
| 1:N | Un municipi i moltes observacions anuals | Relació pare-fills o agregació explícita |
| N:M | Equipaments que ofereixen diversos serveis compartits | Taula intermèdia amb les dues claus |
:::

Un **camp de grup** només indica quines files s'han de resumir juntes i es pot repetir legítimament. Abans de crear `clau_norm`, agregar per `codi_com` o unir dues taules, cal decidir si el camp ha d'identificar una fila, referenciar una altra taula o només formar un grup. Aquesta funció determina si els duplicats són errors o observacions esperades.

## Camps derivats i controls

La calculadora de camps permet crear claus preparades, classes, indicadors de validació i mesures. Un camp nou conserva l'entrada i permet comparar-la amb el resultat; sobreescriure el camp rebut elimina aquesta comprovació. La seqüència següent és acumulativa i utilitza noms didàctics: cada camp es calcula i es valida abans de servir d'entrada al següent.

### Una seqüència acumulativa de camps

El camp textual `clau_norm` conserva `codi_font` intacte, elimina només els espais perifèrics, unifica la caixa i valida el candidat amb una expressió regular. El domini didàctic admet lletres ASCII, dígits, guió i guió baix; una font real pot exigir una regla diferent i s'ha d'adaptar només després de llegir-ne l'esquema.

::: listing "Clau textual normalitzada i validada amb una expressió regular"
```text
with_variable(
  'candidat',
  upper(trim(coalesce(to_string("codi_font"), ''))),
  CASE
    WHEN @candidat = '' THEN NULL
    WHEN regexp_match(@candidat, '^[A-Z0-9_-]+$') THEN @candidat
    ELSE NULL
  END
)
```
:::

Retornar `NULL` per a un format no admès evita fabricar una clau aparentment vàlida, però no distingeix per si sol absència i format incorrecte. Cal comptar separadament els originals nuls o buits, els originals no buits que produeixen `NULL`, els duplicats de `clau_norm` i les col·lisions en què valors originals diferents generen la mateixa clau.

El camp de sortida `categoria_norm` aplica una recodificació condicional que conserva els absents i deixa visibles els valors no reconeguts. L'exemple següent només és correcte per a un domini didàctic on la documentació declara equivalents les parelles indicades:

::: listing "Recodificació condicional sense convertir absències en categories"
```text
CASE
  WHEN "categoria_font" IS NULL
    OR trim(to_string("categoria_font")) = ''
  THEN NULL
  WHEN upper(trim(to_string("categoria_font"))) IN ('A', 'ALTA')
  THEN 'alta'
  WHEN upper(trim(to_string("categoria_font"))) IN ('B', 'BAIXA')
  THEN 'baixa'
  ELSE 'revisar'
END
```
:::

El camp `area_km2` només s'ha de calcular sobre una capa poligonal preparada en un CRS projectat adequat per a l'àmbit, amb unitats mètriques i amb la justificació del mètode registrada. Assignar un CRS nou a coordenades existents no les transforma, i dividir una superfície expressada en graus quadrats per un milió no produeix quilòmetres quadrats. Un cop comprovada i, si cal, reprojectada la capa, `area()` calcula planarment en metres quadrats i la conversió és explícita:

::: listing "Superfície en quilòmetres quadrats en un CRS mètric justificat"
```text
CASE
  WHEN $geometry IS NULL OR is_empty($geometry) THEN NULL
  ELSE round(area($geometry) / 1000000.0, 6)
END
```
:::

Un camp de control no converteix les dades en correctes; resumeix proves reproduïbles perquè els casos pendents es puguin filtrar. Després de crear `clau_norm`, `categoria_norm` i `area_km2`, un `estat_validacio` didàctic pot separar les causes principals:

::: listing "Estat de validació derivat de controls explícits"
```text
CASE
  WHEN "clau_norm" IS NULL THEN 'revisar_clau'
  WHEN $geometry IS NULL
    OR is_empty($geometry)
    OR NOT is_valid($geometry)
  THEN 'revisar_geometria'
  WHEN "area_km2" IS NULL OR "area_km2" <= 0
  THEN 'revisar_area'
  WHEN "categoria_norm" IS NULL THEN 'sense_categoria'
  WHEN "categoria_norm" = 'revisar' THEN 'revisar_categoria'
  ELSE 'preparat'
END
```
:::

Una ràtio posterior ha de conservar els valors absents i rebutjar denominadors no vàlids. Zero pot ser una població observada vàlida, mentre que una població negativa o una superfície no positiva exigeixen revisió:

::: listing "Densitat amb control de valors absents i dominis"
```text
CASE
  WHEN "poblacio" IS NULL
    OR "poblacio" < 0
    OR "area_km2" IS NULL
    OR "area_km2" <= 0
  THEN NULL
  ELSE "poblacio" / "area_km2"
END
```
:::

Una densitat territorial agregada es calcula dividint la suma de població coneguda i compatible per la suma de la superfície corresponent; no és necessàriament la mitjana simple de les densitats municipals. El recompte de territoris amb població nul·la ha d'acompanyar el resultat perquè la cobertura no quedi amagada.

::: table "Controls després de la seqüència de càlcul"
| Camp | Controls mínims |
| --- | --- |
| `clau_norm` | Nuls d'origen, formats rebutjats, valors diferents, freqüència màxima, duplicats i col·lisions amb l'original |
| `categoria_norm` | Freqüència de cada categoria, nuls conservats i llista completa de casos `revisar` |
| `area_km2` | CRS i unitat documentats, geometries buides o invàlides, valors no positius, mínim, màxim i mostra recalculada |
| `estat_validacio` | Freqüència de cada estat i suma dels grups igual al nombre total de files |
| Densitat | Nuls, mínim, màxim, unitat, casos extrems i comprovació manual de numerador i denominador |
:::

### Crear o actualitzar un camp

La calculadora de camps pot crear un atribut o actualitzar-ne un d'existent. Crear un camp nou conserva l'entrada i permet comparar abans i després; actualitzar un camp substitueix valors i exigeix una justificació més estricta. Si l'opció de limitar l'actualització a les entitats seleccionades està activa, les files no seleccionades mantenen el valor anterior. Aquesta barreja pot ser correcta en una correcció local, però s'ha de comprovar expressament i no deduir-la del color de la selecció.

>>>> Abans d'actualitzar un camp cal comprovar si l'opció d'aplicar el càlcul només a la selecció està activa. Una selecció residual pot deixar el mateix camp amb valors calculats en moments o amb fórmules diferents; cal anul·lar-la o registrar explícitament l'abast i comparar els recomptes abans i després.

Abans de calcular cal definir el tipus de sortida. Una classificació textual no ha d'anar a un camp numèric, una divisió no s'ha de truncar en un enter i un identificador amb zeros inicials necessita text d'amplada suficient. Alguns formats antics limiten noms i longituds; el GeoPackage conserva una varietat més àmplia de tipus, però l'expressió encara pot produir un valor incompatible. La previsualització d'uns casos no substitueix comptar conversions fallides o textos truncats.

### Camp emmagatzemat o camp virtual

Un **camp emmagatzemat** escriu el resultat a la font. El valor queda congelat fins que es torna a calcular, encara que canviïn els camps d'entrada. És adequat per a una sortida que s'ha de compartir, auditar fora de QGIS o conservar com a estat d'una data concreta. Aquesta persistència també crea una responsabilitat: si canvia la geometria o un denominador, el camp derivat pot quedar obsolet.

Un **camp virtual** desa l'expressió al projecte i la reavalua quan QGIS necessita el valor. És útil per explorar classificacions, etiquetes o mesures que han de reflectir les edicions recents. No modifica necessàriament la font i pot dependre d'altres capes, variables o configuracions del projecte. En conjunts grans o expressions espacials costoses, aquesta reavaluació pot alentir la taula i la representació.

::: table "Decidir entre camp emmagatzemat i camp virtual"
| Criteri | Camp emmagatzemat | Camp virtual |
| --- | --- | --- |
| Persistència | Queda a la font compatible | Queda principalment a la configuració del projecte |
| Actualització | S'ha de recalcular de manera explícita | Es reavalua segons l'expressió i el context |
| Intercanvi | Altres programes poden llegir el valor | Pot desaparèixer fora del projecte QGIS |
| Rendiment | Lectura directa després del càlcul | Pot repetir operacions costoses |
| Traçabilitat | Necessita conservar l'expressió a part | Conserva l'expressió, però també les dependències del context |
| Ús adequat | Resultat publicable o estat temporal fixat | Exploració, etiquetatge o derivació dinàmica |
:::

Cap opció no és automàticament més reproduïble. Un valor emmagatzemat sense expressió documentada no es pot reconstruir; un camp virtual que depèn d'una capa anomenada `capa2`, d'una selecció o de la data actual tampoc no és autònom. El diari ha d'identificar el camp de sortida, el tipus, l'expressió, les unitats, l'abast de files i les dependències.

## Agregacions i operacions per grup

Una expressió ordinària transforma una fila a partir dels seus valors. Una **agregació** resumeix diverses files mitjançant un recompte, una suma, una mitjana, un mínim, un màxim, una mediana, una concatenació o una altra funció. El grup pot ser tota la capa, les files que comparteixen una categoria o les entitats relacionades espacialment. Abans de calcular-lo cal definir quina és la unitat que es resumeix i què passa amb els nuls.

QGIS ofereix estadístiques de camp i eines com `Statistics by categories`.

Entre les funcions d'expressió hi ha `aggregate()` i `relation_aggregate()`. Una eina que crea una taula resum produeix habitualment una fila per grup. Una expressió agregada dins de la capa original pot repetir el mateix total en totes les files del grup. Les dues representacions poden contenir la mateixa mesura, però només la primera canvia explícitament la unitat d'observació.

::: listing "Suma del grup de la fila actual en una expressió de QGIS"
```text
aggregate(
  layer := @layer,
  aggregate := 'sum',
  expression := "poblacio",
  filter := "codi_com" = attribute(@parent, 'codi_com')
)
```
:::

En avaluar l'expressió agregada, `@parent` permet referir-se a la fila exterior i comparar el seu `codi_com` amb les files candidates de la capa. La sintaxi i el context s'han de comprovar a la versió utilitzada. Si `codi_com` és nul, la comparació no defineix un grup ordinari; si hi ha codis mal formats, es crearan grups separats. Per això l'agregació arriba després del diagnòstic de claus i categories, no abans.

Sumar és adequat per a magnituds extensives compatibles, com recomptes referits al mateix període i cobertura. Una mitjana simple de percentatges o densitats dona el mateix pes a unitats de mides diferents i no reconstrueix necessàriament l'indicador del grup. Per obtenir densitat agregada cal sumar la població, sumar la superfície compatible i dividir els totals. Per obtenir un percentatge agregat cal sumar numeradors i denominadors abans de dividir-los.

Els nuls també canvien el denominador d'una mitjana i el significat d'un recompte. `count` pot comptar files, identificadors o valors no nuls segons l'expressió utilitzada. Una suma que ignora nuls no demostra que la cobertura sigui completa. El resultat ha d'anar acompanyat, quan sigui rellevant, del nombre de files totals, del nombre de valors vàlids i d'una mesura o indicador de cobertura.

Quan una taula detallada manté una relació 1:N amb els territoris, no s'ha d'unir directament com si aportés una sola fila per clau. Si la pregunta necessita un valor resumit, primer es crea una taula amb una fila per clau territorial, la mesura agregada, el nombre de registres totals i el nombre de valors vàlids. Només després de comprovar que aquesta clau és única es pot fer una unió 1:1 o N:1; la taula detallada es conserva per mantenir la relació i auditar el resum.

### Exemple resolt: resum o repetició del resum

En un conjunt sintètic hi ha tres observacions amb `grup = 'X'` i valors coneguts, i dues amb `grup = 'Y'`. `Statistics by categories` pot crear dues files, una per X i una per Y, amb les estadístiques triades. La funció `aggregate()` utilitzada a la capa d'observacions manté cinc files i escriu a cada una el resum del seu grup. Sumar després aquest camp repetit multiplicaria el total pel nombre de files del grup.

La comprovació consisteix a identificar la unitat de la sortida. Si la pregunta demana una fila per territori, convé crear una taula agregada o relacionar el resum amb una taula territorial única. Si la pregunta necessita que cada observació conegui el total del seu grup, la repetició pot ser intencionada, però el camp s'ha de descriure com un valor de context i no com una magnitud additiva.

## Comprovar la cardinalitat

![Esquemes de cardinalitat 1:1, N:1, 1:N i N:M entre municipis, fitxes, centres, observacions, equipaments i serveis]({{ site.baseurl }}/assets/quarto/05-consultes-dades-relacionals/join-cardinality.qmd "Una unió directa només és segura quan cada fila objectiu té com a màxim una candidata; les relacions amb diversos fills necessiten conservar-los, agregar-los explícitament o representar cada parella en una taula intermèdia."){: data-figure-width-web="56rem" data-figure-width-pdf="100%"}

La cardinalitat prevista es comprova comptant candidats per a **cada** fila objectiu, no observant només que aparegui algun camp nou:

::: table "Diagnòstic del nombre de coincidències"
| Coincidències candidates | Interpretació | Tractament |
| ---: | --- | --- |
| 0 | No hi ha cap correspondència segons la clau i l'àmbit utilitzats | Conservar la fila sense parella i investigar tipus, format, versió i cobertura |
| 1 | Hi ha una candidata única | Validar-ne el significat i incorporar-la si concorda amb la cardinalitat prevista |
| Més d'1 | La clau de la banda esperada com a única es repeteix o la relació és realment 1:N | Aturar la unió directa; completar la clau, definir una relació o agregar amb una regla explícita |
:::

La notació sempre necessita una direcció explícita. «Un municipi té molts centres» és 1:N des de municipis cap a centres i N:1 des de centres cap a municipis. Si es vol afegir el nom municipal a cada centre, la taula de centres és l'objectiu i cada fila busca una única fila municipal. Si es vol obrir des d'un municipi la llista dels seus centres, cal una relació pare-fills. La mateixa parella de taules admet operacions diferents segons quina unitat s'ha de conservar.

Una cardinalitat prevista no és una propietat que el programari pugui endevinar. S'ha de declarar a partir del model i verificar amb les dades. Si un codi municipal apareix dues vegades en una taula que havia de contenir una sola fitxa vigent, pot haver-hi un duplicat, dues dates, dues categories o un canvi de definició. El remei no és eliminar una fila automàticament, sinó identificar quina dimensió faltava a la clau o quina observació és incorrecta.

Una taula temporal o multivariable funciona millor en **format llarg**: cada fila representa una combinació d'unitat, data i variable. La geometria es conserva a la taula d'unitats espacials i les observacions s'hi relacionen mitjançant una clau. Això evita repetir el polígon per a cada any.

Aquest disseny separa entitats estables d'observacions repetides. La taula `municipis` pot tenir una fila per unitat i conservar la geometria, el codi i el nom; la taula `observacions` pot contenir moltes files per municipi amb període, variable, valor, unitat i font. Afegir una columna nova per a cada any crea una taula ampla que obliga a modificar l'esquema contínuament i dificulta filtrar períodes o comparar variables amb una mateixa operació.

La forma llarga no elimina la necessitat de definir la unitat d'observació. Una fila pot representar un valor municipal anual, una mesura mensual d'un sensor o una incidència individual. Barrejar aquests nivells en una sola taula produeix claus inconsistents i agregacions sense denominador clar. Les dimensions necessàries han d'aparèixer com a camps i la combinació que identifica una observació ha de poder comprovar-se.

### Normalització i dependències

La **normalització relacional** organitza les dades perquè cada fet s'emmagatzemi al lloc que li correspon i les dependències quedin explícites. En una taula rectangular, cada cel·la ha de contenir un valor atòmic per al model adoptat: una llista de codis separats per comes no és una clau forana operable. Si un equipament ofereix diversos serveis i un servei correspon a diversos equipaments, la relació N:M s'ha de representar amb una taula intermèdia que contingui una fila per parella.

Repetir el nom de comarca a cada observació municipal pot ser convenient en una exportació de lectura, però crea una dependència redundant si el codi municipal ja determina la comarca en la data de referència. Una correcció parcial podria deixar dos noms diferents per al mateix codi. En el model de treball, convé conservar les entitats territorials i les seves relacions en taules controlades; les taules planes enriquides es poden generar després com a resultats derivats.

Normalitzar tampoc significa fragmentar qualsevol informació fins a fer-la impracticable. L'objectiu és evitar anomalies d'actualització, inserció i eliminació i mantenir clara la unitat de cada taula. Una adreça completa pot conservar-se com a text de presentació i, alhora, disposar de camps separats quan carrer, número o codi postal s'han de consultar. El nivell adequat depèn de les operacions previstes i de la font.

Una exportació plana i una relació normalitzada poden coexistir. La primera és útil per a una anàlisi o un intercanvi concret; la segona conserva l'estructura mestra sense repetir geometries ni atributs estables. Cal identificar quina és la font de veritat i evitar editar independentment dues còpies que després ja no coincideixen.

Abans d'una unió cal comparar el nombre de files amb el nombre de claus diferents, identificar duplicats, nuls i valors sense correspondència. En una unió N:1, el nombre de files de la capa objectiu no ha d'augmentar. Si augmenta, probablement la taula que es considerava única conté més d'una coincidència.

## Unions i relacions no són intercanviables

Unió d'atributs
: Afegeix columnes d'una taula d'unió a les files d'una taula objectiu mitjançant camps compatibles; la geometria continua sent la de l'objectiu.

Relació
: Conserva les dues taules separades i permet navegar entre una fila pare i les files filles que en contenen la clau forana.

La unió és adequada per a 1:1 o N:1 quan cada fila objectiu troba com a màxim una fila a la banda que aporta els atributs. Si hi ha diverses candidates, una eina pot repetir la fila, conservar-ne una segons un ordre intern o informar del conflicte; cap d'aquests comportaments converteix la coincidència en analíticament única. La relació és adequada per a 1:N perquè no obliga a triar una sola observació ni a duplicar la geometria del pare. En QGIS pot alimentar formularis i expressions com `relation_aggregate()`, però les dues fonts, els identificadors de relació i el projecte formen part de les dependències.

En una relació N:M, una taula intermèdia conté com a mínim la clau de cada costat. Si els equipaments E1 i E2 ofereixen els serveis S1 i S2 en combinacions diferents, cada combinació vàlida ocupa una fila. Escriure `S1,S2` en un únic camp impedeix aplicar una clau forana ordinària, comptar sense analitzar cadenes i afegir atributs propis de la relació, com una data d'inici.

::: table "Unió, relació i agregació segons el resultat necessari"
| Necessitat | Estructura adequada | Què es conserva | Control determinant |
| --- | --- | --- | --- |
| Afegir una fitxa única a cada geometria | Unió 1:1 | Una fila objectiu i camps nous | Unicitat i cobertura a totes dues bandes |
| Afegir una categoria territorial a moltes entitats | Unió N:1 | Cada entitat objectiu | Una sola fila territorial per clau |
| Consultar totes les observacions d'una entitat | Relació 1:N | Pare i filles separats | Clau forana vàlida i fills orfes identificats |
| Resumir observacions per entitat | Agregació seguida d'una unió 1:1 | Una fila resum per pare | Definició de l'agregació i una clau única del resum |
| Associar múltiples elements de dos catàlegs | Relació N:M amb taula intermèdia | Cada parella admesa | Unicitat de la parella i integritat de les dues claus foranes |
:::

Una relació no afegeix automàticament els camps fills a cada pare. Una unió tampoc no resumeix múltiples fills. Si un municipi té diverses observacions anuals i es vol incorporar només un any, cal filtrar explícitament aquell període fins que la clau municipal sigui única. Si es vol un total o una mitjana, cal agregar amb una definició explícita i unir després la taula resum. «Agafar la primera coincidència» no és una regla analítica.

### Unió virtual o resultat materialitzat

Una unió configurada a les propietats de la capa és habitualment una vista del projecte. Permet consultar i simbolitzar camps relacionats sense reescriure la capa objectiu. La configuració ha de conservar la capa d'unió, els camps de correspondència, el prefix, la memòria cau si s'utilitza i el tractament d'edició. Si la taula canvia o deixa de carregar-se, els camps units poden desaparèixer.

Materialitzar una unió crea una capa o taula nova amb els camps incorporats. És útil per compartir un resultat autosuficient, congelar una versió o continuar un procés que no llegeix unions de projecte. També duplica dades i pot quedar obsoleta respecte de les fonts. El resultat ha de conservar els camps de clau originals, distingir les columnes de cada procedència i registrar la data o versió de la unió.

Els noms de camp coincidents necessiten prefixos o una selecció explícita de columnes. Si totes dues taules tenen `nom`, `data` i `font`, un resultat amb sufixos automàtics poc clars és difícil d'auditar. Convé decidir abans quins camps s'han d'incorporar i anomenar-los segons el significat, sense eliminar els identificadors que permeten comprovar la correspondència.

El tipus d'unió també determina què passa amb les files sense coincidència. Una unió esquerra conserva totes les files de l'objectiu i deixa nuls als camps afegits; una unió interna conserva només les coincidències. En una exploració de qualitat, la primera fa visibles els objectius sense parella. Una unió interna pot ser adequada per a una sortida concreta, però no s'ha d'utilitzar abans de comptar i documentar què exclou.

## Preparar claus sense perdre l'original

La compatibilitat d'una clau inclou tipus, longitud, caixa, espais, zeros inicials, signes, codificació i definició territorial o temporal. Dos camps anomenats `codi_muni` poden seguir versions diferents d'una classificació. La coincidència textual no prova equivalència semàntica, i una conversió que fa encaixar els valors no corregeix una delimitació històrica diferent.

La preparació s'ha de fer en camps nous, per exemple `clau_muni_norm`, mentre es conserven `codi_font_a` i `codi_font_b`. Això permet comparar el valor rebut amb el transformat i detectar col·lisions. La regla pot eliminar espais perifèrics, unificar caixa o completar zeros només si la documentació confirma el format de destinació.

::: listing "Preparació explícita d'una clau textual"
```text
CASE
  WHEN trim(to_string("codi_muni_font")) <> ''
   AND length(trim(to_string("codi_muni_font"))) <= 5
  THEN lpad(trim(to_string("codi_muni_font")), 5, '0')
  ELSE NULL
END
```
:::

Aquesta expressió converteix el valor a text, elimina espais perifèrics i completa fins a cinc caràcters. La cadena buida es rebutja abans d'aplicar `lpad()`, perquè altrament es convertiria en `00000`. La comprovació de longitud també és necessària perquè `lpad()` trunca els textos que superen l'amplada demanada; retornar nul fa visible l'anomalia en lloc de fabricar una clau aparentment vàlida. No és una recepta universal: només és correcta si la codificació esperada té cinc posicions i els valors d'entrada representen el mateix codi sense el farciment. Si el camp conté decimals introduïts per un full de càlcul, prefixos o codis de longitud superior, cal diagnosticar-los abans.

Quan la clau combina components, concatenar sense separador pot produir col·lisions: els parells (`1`, `23`) i (`12`, `3`) donarien el mateix text `123`. Una construcció amb amplades fixes documentades o un separador que no aparegui als components evita aquesta ambigüitat. Encara és millor mantenir els components en camps separats quan l'eina admet una clau composta.

Els noms propis només s'han d'utilitzar com a recurs secundari de diagnòstic. Normalitzar caixa i espais pot ajudar a proposar candidats, però els homònims i les variants impedeixen assumir una correspondència automàtica. Una taula de concordança revisada, amb codi d'origen, codi de destinació, mètode i observació, és preferible a una substitució opaca.

## Diagnosticar la correspondència

El diagnòstic ha de fer-se abans i després de la unió. Abans, cada banda necessita un perfil de clau: nombre de files, nuls, cadenes buides, nombre de valors diferents, freqüència màxima i llista de duplicats. Després, cal comptar coincidències, objectius sense parella, files de la taula d'unió no utilitzades i, quan sigui possible, correspondències múltiples.

::: table "Controls d'una unió per clau"
| Moment | Control | Interpretació d'una desviació |
| --- | --- | --- |
| Abans | Tipus i format dels dos camps | Una conversió o una classificació pot ser incompatible |
| Abans | Nuls i cadenes buides | Hi ha files que s'han d'excloure de la unió ordinària i diagnosticar per separat |
| Abans | Files i claus diferents a la banda esperada com a única | La diferència revela duplicats o una clau incompleta |
| Abans | Freqüència de cada clau | Permet confirmar la cardinalitat prevista |
| Després | Files de l'objectiu conservades | Una pèrdua pot indicar una unió interna o un filtre ocult |
| Després | Camps afegits nuls | Poden indicar una absència legítima o una clau sense correspondència |
| Després | Claus de l'altra taula no utilitzades | Revelen unitats fora de l'àmbit, versions diferents o errors |
| Després | Mostra de parelles i valors | Detecta coincidències formalment vàlides però semànticament errònies |
:::

Un nul en un camp afegit és ambigu. Pot significar que no hi ha cap fila relacionada o que sí que n'hi ha una i el seu atribut és nul. Per distingir els casos convé incorporar temporalment la clau de la taula d'unió o un indicador de coincidència. Comprovar només un atribut temàtic pot classificar erròniament una parella existent com a no coincident.

>>>> Una clau `NULL` no identifica cap entitat i, en la semàntica relacional ordinària, no ha d'establir una correspondència. El comportament concret pot variar amb l'algorisme i el proveïdor: `native:joinattributestable` de QGIS pot emparellar un `NULL` de l'objectiu amb un `NULL` de la taula d'unió. Abans de relacionar cal separar els nuls i les cadenes buides de totes dues bandes, registrar-ne el recompte i provar la semàntica de l'eina utilitzada {% cite qgisUserGuide344 %}.

Les files sense correspondència s'han d'examinar en les dues direccions. Un municipi objectiu sense estadística pot revelar una dada absent; una fila estadística sense geometria pot pertànyer a un altre àmbit, utilitzar una divisió antiga o contenir un codi defectuós. El segon conjunt no apareix en una unió esquerra ordinària sobre la geometria i s'ha de calcular amb una consulta inversa o una comparació de conjunts.

Els duplicats tampoc no s'han d'esborrar només per aconseguir una unió. Dues files idèntiques poden ser una duplicació accidental, però dues files amb la mateixa clau i anys diferents són observacions legítimes d'una relació 1:N. Cal comparar tots els camps que defineixen la unitat d'observació i decidir si falta una dimensió a la clau, si s'ha d'aplicar un filtre temporal o si cal agregar.

### Exemple resolt: una unió que no és encara N:1

En dues taules didàctiques, `municipis` conté les claus M01, M02 i M03, una vegada cadascuna. `observacions` conté M01 per a l'any A; M02 per als anys A i B; M04 per a l'any A; i una fila amb clau nul·la. No són resultats reals: el conjunt mínim serveix per diagnosticar la cardinalitat.

Unir directament `observacions` a `municipis` només per `codi_muni` no compleix el contracte N:1 perquè M02 té dues coincidències candidates. Filtrar explícitament l'any A i separar la fila nul·la deixa M01, M02 i M04 com a claus conegudes úniques. Una unió esquerra des de `municipis` conserva M01, M02 i M03: les dues primeres reben l'observació de l'any A i M03 queda sense parella. M04 és una observació no utilitzada perquè no existeix a l'objectiu.

Si la pregunta demana una sèrie temporal, filtrar un únic any destruiria informació necessària. El disseny adequat és una relació 1:N entre `municipis` i `observacions`, amb `(codi_muni, any)` com a clau candidata de l'observació. Si la pregunta demana un resum de tots els anys, cal definir abans l'agregació; una suma, una mitjana i el valor més recent responen preguntes diferents.

El diagnòstic final ha d'informar M03 com a objectiu sense observació, M04 com a observació sense pare, la fila nul·la separada com a no relacionable i M02 com a clau repetida abans del filtre o com a pare amb dos fills en el model temporal. Cap d'aquests casos no s'ha d'amagar perquè la capa resultant es dibuixi sense errors.

### Exemple resolt: una clau aparentment compatible

En un segon exemple, la capa geomètrica conserva els textos `'001'`, `'002'` i `'010'`, mentre que una importació de full de càlcul ha convertit els mateixos codis aparents en enters `1`, `2` i `10`. Convertir els enters a text dona `'1'`, `'2'` i `'10'`, que encara no coincideixen. Completar-los a tres posicions pot reconstruir els textos només si les metadades confirmen que els zeros són farciment i no s'ha perdut cap altre component.

La comprovació consisteix a mantenir el camp enter importat, crear una clau textual preparada, comparar-ne la longitud i els valors diferents i buscar col·lisions. Si dues files originals produeixen la mateixa clau preparada, la transformació no és injectiva i no es pot acceptar com a identificador sense resoldre el conflicte. La coincidència total després de completar zeros és una evidència tècnica, però encara cal confirmar que totes dues taules utilitzen la mateixa versió territorial.

## Unions espacials

Una **unió d'atributs** compara valors de clau compatibles; una **unió espacial** compara les geometries mitjançant un predicat. En tots dos casos hi ha una capa o taula objectiu, un conjunt candidat i una regla de correspondència, però només la unió espacial depèn de posició, frontera i validesa geomètrica. Una unió espacial habitual conserva la geometria completa de l'objectiu i hi afegeix atributs o files; combinar o tallar físicament geometries és una operació de geoprocessament diferent.

![Comparació d'una unió d'atributs per clau amb una unió espacial per relació geomètrica, inclosos els casos de zero, una i diverses coincidències]({{ site.baseurl }}/assets/quarto/05-consultes-dades-relacionals/attribute-vs-spatial-join.qmd "La unió d'atributs compara claus i la unió espacial avalua geometries; totes dues necessiten diagnosticar zero, una o diverses coincidències abans d'incorporar atributs."){: data-figure-width-web="52rem" data-figure-width-pdf="100%"}

Els predicats `intersects`, `within`, `contains` i `touches` no són equivalents. Un punt situat exactament sobre el límit pot intersectar dos municipis i no trobar-se estrictament dins de cap interior. El resultat s'ha de validar comptant quantes entitats obtenen zero, una o diverses coincidències {% cite ogcSimpleFeatures2011 %}.

Quan `intersects` s'utilitza per seleccionar o extreure per localització, una entitat que comparteix qualsevol punt amb la geometria de comparació compleix el criteri i es conserva **sencera**. Una línia que travessa un límit no queda retallada automàticament a la part interior. Obtenir només la porció comuna exigeix una operació com `Clip` o `Intersection`, que crea geometries noves i es tractarà al capítol següent.

Una taula pot convertir-se en punts si conté coordenades documentades. Abans cal identificar quina columna és X, quina és Y, quin separador decimal utilitzen i en quin CRS s'expressen. Crear punts amb el CRS equivocat pot produir una capa aparentment buida o desplaçada; assignar una altra referència sense conèixer la font no corregeix les coordenades.

Com en una unió per clau, la cardinalitat espacial s'ha de definir abans d'executar l'eina. Un punt ordinari situat a l'interior d'una partició municipal vàlida hauria de tenir una coincidència; un punt al límit, dos polígons superposats o una geometria duplicada poden produir-ne diverses. Una línia que travessa diversos municipis té legítimament més d'una correspondència. L'eina necessita una regla per crear una fila per coincidència, prendre una sola coincidència o agregar-ne els atributs, i cada opció respon una pregunta diferent.

Un resum espacial tampoc no queda definit només pel predicat. Si es compten centres per municipi, cal decidir si cada centre pot comptar en més d'un territori, què passa amb els punts al límit i si els centres sense geometria o sense coincidència entren al denominador de cobertura. Si se sumen capacitats, els nuls, els duplicats i les coincidències múltiples poden alterar el total. Els recomptes zero, un i més d'un per entitat objectiu funcionen com a diagnòstic inicial.

### Exemple resolt: un punt sobre una frontera

En un conjunt didàctic format per dos polígons adjacents A i B, un punt P situat estrictament a l'interior d'A compleix `within(P, A)` i només s'assigna a A amb aquest predicat. Un punt Q situat exactament sobre la frontera compartida intersecta A i B, però no queda dins de l'interior de cap dels dos segons `within`. Per tant, canviar `within` per `intersects` no «arregla» el punt: canvia la regla i pot generar dues coincidències.

La resolució depèn del model. Si el punt representa una adreça que hauria d'estar dins d'una parcel·la, pot revelar un error posicional i convé revisar la font. Si representa una fita situada realment al límit, la doble intersecció és correcta i pot requerir una relació N:M. Assignar sempre la primera coincidència faria desaparèixer aquesta diferència semàntica.

## Cas guiat acumulatiu amb fonts del CNIG

El cas reobre el mateix `projecte_tig.qgz` i el mateix `dades_preparades/projecte_tig.gpkg` creats al capítol 02 i ampliats als capítols 03 i 04. Les famílies previstes són les [divisions administratives](https://www.idee.es/csw-codsi-idee/srv/spa/catalog.search#/metadata/spaignLLM), les [poblacions](https://www.idee.es/csw-codsi-idee/srv/spa/catalog.search#/metadata/spaign_IGR_Poblaciones) i les [xarxes de transport](https://www.idee.es/csw-codsi-idee/srv/spa/catalog.search#/metadata/spaign_IGR_Transporte) de l'IGN/CNIG. Aquests noms només identifiquen famílies de productes: no permeten anticipar quins fitxers, capes, geometries o camps contindrà una descàrrega concreta. Per a cada edició cal inspeccionar el paquet i les metadades, registrar la data, el CRS i la unitat d'observació i identificar els noms físics, els tipus, els dominis i les claus abans d'escriure cap consulta.

La primera fase verifica la capa `municipi_treball` heretada. Se'n comproven la URI, el recompte d'una entitat, la identitat oficial, el `codi_muni` textual, l'esquema, el CRS, la geometria i l'extensió contra el diari i la font del capítol 02. Qualsevol discrepància obliga a aturar el capítol i corregir la preparació o el punt de control anterior; no es recrea ni se sobreescriu `municipi_treball` per fer coincidir la consulta actual.

Els camps derivats que el model justifiqui es calculen en una taula relacionada o una sortida de diagnòstic amb un nom diferent, sense substituir la geometria ni els identificadors de `municipi_treball`. La clau normalitzada es compara amb l'original i se'n comproven nuls, formats rebutjats, duplicats i col·lisions; `area_km2` només es calcula en el CRS mètric justificat; la recodificació conserva els valors no reconeguts; i l'estat de validació separa les causes pendents. Els recomptes per estat, els mínims, els màxims i una mostra manual queden registrats, de manera que els camps són resultats comprovats i no només columnes visibles.

La segona fase perfila l'edició descarregada de *Poblaciones* abans de relacionar-la. La unitat d'observació, la geometria, els identificadors i els atributs disponibles es dedueixen de l'esquema oficial, no dels noms didàctics d'aquest capítol. La correspondència espacial amb els territoris es classifica en zero, una i diverses coincidències. Les coincidències úniques, els registres sense correspondència i els casos múltiples es desen com a resultats diagnòstics separats o en una taula d'estat que permeti reconstruir el total processat; no s'assigna la primera candidata als casos ambigus.

Si la banda detallada manté diverses files per municipi, es conserva com una relació 1:N. Abans d'intentar incorporar-la als polígons mitjançant una unió d'atributs, es prepara una taula resum amb una fila per clau, les mesures justificades, el nombre de registres i el nombre de valors vàlids. La unicitat del resum es verifica abans d'unir-lo; les claus sense parella i les claus múltiples romanen en el diagnòstic. Així, la geometria municipal no es duplica i el resum es pot contrastar amb la taula detallada.

La tercera família, transport, es perfila amb el mateix criteri abans de qualsevol consulta. A partir dels atributs i les geometries realment disponibles, es defineix un predicat relacionat amb la pregunta del projecte i se'n conserven les entitats candidates al GeoPackage com a `transport_candidats_c06`, amb els identificadors d'origen i el criteri exacte. Si la selecció usa `intersects`, les geometries es retenen completes: el retall, les zones d'influència i les superposicions corresponen al capítol 06.

`municipi_treball` és l'entrada canònica creada al capítol 02; `transport_candidats_c06` i les taules de resum o diagnòstic són resultats nous d'aquest capítol. Cap d'aquests noms s'ha d'atribuir com si fos un nom físic dels productes del CNIG. En acabar, es desa el mateix `projecte_tig.qgz`, s'actualitza el punt de control incrustat `projecte_tig` al mateix GeoPackage i es reobre el conjunt per comprovar que la capa municipal continua intacta i que les noves sortides, relacions i identificadors estables continuen disponibles.

## Activitats

### Comprovació: predir abans d'executar

Cal preparar sis registres curts que incloguin text, nombres, cadena buida i `NULL`. Abans d'executar cada expressió s'ha de predir quines files retornaran `TRUE`, `FALSE` o `NULL`. La comparació entre predicció i resultat permet detectar errors de precedència i tractament dels absents.

### Pràctica guiada: de la condició al resultat retingut

El criteri verificat del municipi assignat s'aplicarà, per separat, com a selecció, filtre de capa o del proveïdor, filtre de taula i extracció de diagnòstic. Per a cada context es registraran l'expressió o consulta exacta, el llenguatge que l'avalua i els recomptes de font, capa, taula i selecció. La demostració persistent, si cal conservar-la, rebrà un nom inequívoc diferent de `municipi_treball`; també pot quedar temporal i eliminar-se després del control. En reobrir `projecte_tig.qgz` s'ha de poder distingir l'entrada canònica dels estats temporals i dels diagnòstics.

### Micropràctica 3: seleccions, filtres i relacions

::: table "Contracte de la micropràctica 3"
| Component | Requisit |
| --- | --- |
| Entrades | `projecte_tig.qgz` i `dades_preparades/projecte_tig.gpkg` existents, amb `municipi_treball`, les edicions descarregades i les metadades de les famílies de límits administratius, *Poblaciones* i transport del CNIG |
| Operacions mínimes | Verificar `municipi_treball` sense substituir-lo; inspeccionar els esquemes reals; executar consultes amb `AND`, `OR`, `NOT` i `NULL`; distingir filtres i selecció; comprovar el criteri municipal; calcular camps derivats en sortides diferenciades; perfilar claus i cardinalitats; preparar un resum abans d'unir una banda 1:N; i diagnosticar una correspondència espacial |
| Resultats | `municipi_treball` verificat i sense canvis, camps derivats comprovats en una taula o sortida diferenciada, taula resum amb clau única, registres sense correspondència o amb coincidència múltiple identificats i `transport_candidats_c06`, tot dins del mateix GeoPackage |
| Evidències del diari | Edició i esquema inspeccionats, expressions i contextos exactes, predicció i recompte observat, regles de normalització, CRS i unitats, perfil de claus, cardinalitat, diagnòstics i justificació del predicat espacial |
| Comprovacions | `municipi_treball` conserva URI, identitat, esquema, CRS, geometria i una entitat; recomptes reconstruïbles de zero/una/múltiples coincidències; absència de col·lisions de clau no resoltes; unicitat de la taula resum; mínim i màxim dels derivats; mostra manual i reobertura de totes les sortides |
| Fitxers que cal conservar | El mateix GeoPackage actualitzat amb el punt de control incrustat `projecte_tig`, `projecte_tig.qgz` actualitzat i diari amb expressions, recomptes i controls |
:::

La pràctica es considera completa quan les unions es poden tornar a executar a partir de les fonts preparades, la suma dels grups diagnòstics reconstrueix les entrades i els candidats de transport queden disponibles per al capítol 06. Els registres sense correspondència o amb més d'una candidata formen part del resultat observable i no s'han d'amagar perquè el mapa sembli complet.
