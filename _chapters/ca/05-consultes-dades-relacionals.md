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

El tipus s'ha de triar pel significat, no per l'aparença. Un codi municipal format només per dígits continua sent un identificador si no té sentit sumar-lo, obtenir-ne una mitjana o ordenar-lo per magnitud. Conservar-lo com a text permet mantenir zeros inicials i comparar-lo amb la codificació oficial. En canvi, una població importada com a text no admet directament operacions aritmètiques fiables, encara que totes les cel·les semblin nombres.

Els dominis defineixen quins valors són admesos. Si el camp `estat` només pot contenir `actiu`, `inactiu` o `pendent`, les variants `Actiu`, `ACTIU`, `act.` i una cadena amb espais finals no són categories noves, sinó possibles incompliments del domini. Una consulta pot detectar-les, però la correcció exigeix saber quina forma és oficial i conservar la dada original o una traça de la transformació.

### Zero, cadena buida i valor absent

`NULL` representa un valor absent o desconegut dins del model de dades. No és el nombre zero, la cadena buida `''`, el text `'NULL'`, una data fictícia ni un codi com `-9999`. Zero pot ser una observació vàlida, per exemple cap centre comptat; una cadena buida és un text de longitud zero; i un codi sentinella només indica absència si el diccionari de la font ho declara. Substituir-los indiscriminadament altera el significat de la dada.

L'absència també pot tenir causes diferents. Un valor pot no haver-se observat, no ser aplicable, estar protegit per confidencialitat, haver fallat en una importació o quedar pendent d'actualització. Una sola marca nul·la no conserva aquestes causes. Si la distinció és analíticament necessària, convé afegir un camp d'estat o utilitzar els indicadors de qualitat que proporcioni la font, en lloc d'inventar una xifra que després entrarà en sumes i mitjanes.

## De la pregunta al predicat

Un **predicat** és una expressió que avalua una condició per a cada registre. Una comparació pot produir `TRUE`, `FALSE` o `NULL` quan el valor és desconegut. Aquesta lògica de tres valors explica per què una expressió aparentment completa pot deixar fora registres amb dades absents.

Els operadors `NOT`, `AND` i `OR` neguen, combinen o ofereixen alternatives. La precedència habitual és `NOT`, després `AND` i finalment `OR`, però els parèntesis fan explícita la intenció i eviten lectures equivocades.

::: listing "Expressions bàsiques de consulta en QGIS"
```sql
"nom_muni" = 'Vila-seca'

"codi_prov" IN ('43', '25')
AND "poblacio" > 20000

trim(upper(coalesce("nom_muni", ''))) LIKE 'VILA%'

"nom_muni" IS NULL
OR trim("nom_muni") = ''
```
:::

Els noms de camp de l'exemple són il·lustratius. Abans de reutilitzar una expressió cal inspeccionar l'esquema real, perquè `43` pot estar emmagatzemat com a text o com a enter i el nom municipal pot seguir una convenció diferent. Normalitzar majúscules i espais ajuda a explorar textos, però no substitueix una clau oficial.

Les expressions de QGIS s'assemblen a SQL, però no són sempre el mateix llenguatge. La selecció per expressió i la calculadora de camps utilitzen el motor de QGIS; un constructor de consultes sobre una base de dades pot delegar el filtre al proveïdor i aplicar-ne el dialecte. Cal conservar l'expressió exacta i el context on s'ha executat {% cite qgisUserGuide344 %}.

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

## Lògica de tres valors i `NULL`

En una lògica booleana ordinària, una proposició és certa o falsa. Una base de dades necessita un tercer resultat per a comparacions que no es poden decidir perquè falta una dada. Si `"places"` és `NULL`, tant `"places" > 0` com `"places" <= 0` retornen `NULL`: no hi ha evidència per afirmar cap de les dues condicions. Una selecció conserva les files en què el predicat és `TRUE`; les que produeixen `FALSE` o `NULL` queden sense seleccionar, encara que les causes siguin diferents.

::: table "Combinacions bàsiques de la lògica de tres valors"
| A | B | `A AND B` | `A OR B` |
| --- | --- | --- | --- |
| `TRUE` | `TRUE` | `TRUE` | `TRUE` |
| `TRUE` | `FALSE` | `FALSE` | `TRUE` |
| `TRUE` | `NULL` | `NULL` | `TRUE` |
| `FALSE` | `FALSE` | `FALSE` | `FALSE` |
| `FALSE` | `NULL` | `FALSE` | `NULL` |
| `NULL` | `NULL` | `NULL` | `NULL` |
:::

La taula respon a una idea concreta. En una conjunció, una condició falsa basta per saber que el conjunt és fals, encara que l'altra sigui desconeguda; per això `FALSE AND NULL` és `FALSE`. En una disjunció, una condició certa basta per saber que el conjunt és cert; per això `TRUE OR NULL` és `TRUE`. En canvi, `NOT NULL` continua sent `NULL`, perquè negar allò que es desconeix no aporta informació.

Comparar un nul amb qualsevol valor, inclòs un altre nul, no produeix una igualtat certa. Per comprovar absència s'utilitzen `IS NULL` i `IS NOT NULL`. Aquest comportament també explica un parany de `NOT IN`: si la llista conté un `NULL`, una fila que no coincideix amb cap valor conegut pot donar un resultat desconegut en lloc de `TRUE`. Les llistes de consulta han de contenir valors explícits i l'absència s'ha de tractar en una condició separada.

`coalesce()` retorna el primer argument que no és nul. És adequat quan el model defineix una substitució real, com ara construir una etiqueta que mostri `'sense nom'` en lloc d'un buit. No converteix l'absència en una observació. Fer `coalesce("places", 0)` abans d'una suma afirma que tot valor absent equival a cap plaça; aquesta afirmació només és defensable si la font ho estableix. Si no, el càlcul amaga la diferència entre zero i desconegut.

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
```sql
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
```sql
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
```sql
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
```sql
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

Una mateixa condició pot tenir efectes diferents segons on s'apliqui. Aquesta decisió afecta els recomptes, la visualització i les eines de processament.

::: table "Efectes de diferents maneres d'aplicar una condició"
| Operació | Efecte | Persistència | Risc habitual |
| --- | --- | --- | --- |
| Selecció | Marca entitats dins de la capa | Temporal; un `.qgz` ordinari no en serialitza els identificadors seleccionats | Un algorisme pot usar només la selecció sense que quedi documentat |
| Filtre de capa | Limita el conjunt actiu | Es pot conservar al projecte | Es pot interpretar erròniament com si les altres files s'haguessin eliminat |
| Filtre de taula | Limita la inspecció visible | Normalment temporal | No sempre afecta el mapa ni el processament |
| Regla de simbologia | Canvia l'aparença | Es conserva amb l'estil | Les entitats continuen existint encara que no siguin visibles |
| Extracció | Crea una capa nova amb el subconjunt | Persistent si es desa | Duplica dades i necessita procedència i nom propis |
:::

Abans d'interpretar un resultat cal comprovar el nombre total, el nombre seleccionat i l'estat dels filtres. Una selecció espacial o atributiva és una hipòtesi reversible; una extracció és un nou conjunt de dades que s'ha de documentar.

### La selecció com a estat de treball

Una selecció marca files dins del conjunt actiu sense eliminar-les ni crear una font nova. Pot provenir d'un clic al mapa, d'una selecció per valor, d'una expressió o d'una relació espacial. Les modalitats manuals són adequades per inspeccionar un cas, però no constitueixen per si soles un criteri reproduïble. Si la selecció participa en un resultat, cal poder reconstruir-la mitjançant una expressió, una llista d'identificadors justificats o un procediment espacial documentat.

### Tres filtres que no fan la mateixa feina

Un **filtre de capa** o subconjunt del proveïdor limita les entitats que la capa ofereix al projecte. Pot reduir transferència i processament quan la font o el proveïdor l'executen de manera eficient. També altera recomptes, valors únics, extensions i operacions posteriors. El projecte ha de conservar-ne la definició, però una persona que examini només el mapa podria no advertir que la font conté més files.

Un **filtre de la taula d'atributs** acostuma a controlar quines files es mostren al panell: totes, seleccionades, visibles al mapa o coincidents amb una expressió de cerca. La seva funció principal és inspeccionar. No s'ha de suposar que redueix les entitats renderitzades o l'entrada d'un algorisme; cal comprovar l'abast exacte de l'opció i la versió de QGIS.

Una **regla de simbologia** decideix com es dibuixa una entitat i pot deixar-la sense símbol. Això no la treu de la taula, d'una selecció ni d'un càlcul. Fer transparent una categoria tampoc no l'exclou de l'anàlisi. Quan un mapa sembla mostrar el mateix subconjunt que un filtre, la comprovació decisiva és comparar el nombre d'entitats disponibles per a una eina, no només l'aparença del llenç.

### Extreure és crear una dada derivada

Una extracció materialitza les files que compleixen el criteri en una capa o taula nova.

`Extract by expression` i `Extract by attribute` formalitzen criteris atributius. `Extract by selection` materialitza l'estat seleccionat, mentre que `Extract by location` aplica una relació espacial. Totes treballen dins del marc de Processament. Una sortida temporal continua sent derivada, però desapareixerà si no es desa; una sortida al GeoPackage necessita un nom, una procedència, un esquema i controls propis {% cite qgisUserGuide344 %}.

### Exemple resolt: una condició, quatre efectes

En una capa didàctica amb camps `tipus` i `estat_rev`, l'expressió `"tipus" = 'fanal' AND "estat_rev" = 'validat'` identifica les files que compleixen tots dos criteris. Com a selecció, aquestes files queden marcades i la resta continua disponible. Com a filtre de capa, només les coincidències formen el conjunt actiu. Com a regla de simbologia, es dibuixen les coincidències però les altres files continuen entrant en una eina. Com a extracció, es crea una capa nova que conté les coincidències i que s'ha de relacionar amb l'entrada mitjançant l'identificador.

## Camps derivats i controls

La calculadora de camps permet crear identificadors, classes i mesures. Un camp virtual es recalcula segons l'expressió i el context; un camp emmagatzemat conserva el valor calculat fins que es torna a actualitzar. La tria depèn de si cal una vista dinàmica o una dada persistent.

Una ràtio ha de controlar valors absents i denominadors no vàlids:

::: listing "Densitat amb control de valors absents"
```sql
CASE
  WHEN "poblacio" IS NULL
    OR "superficie_km2" IS NULL
    OR "superficie_km2" <= 0
  THEN NULL
  ELSE "poblacio" / "superficie_km2"
END
```
:::

Després del càlcul cal revisar nuls, mínim, màxim, unitat i alguns casos manuals. Una densitat territorial agregada es calcula dividint la suma de població per la suma de superfície; no és necessàriament la mitjana simple de les densitats municipals.

### Crear o actualitzar un camp

La calculadora de camps pot crear un atribut o actualitzar-ne un d'existent. Crear un camp nou conserva l'entrada i permet comparar abans i després; actualitzar un camp substitueix valors i exigeix una justificació més estricta. Si l'opció de limitar l'actualització a les entitats seleccionades està activa, les files no seleccionades mantenen el valor anterior. Aquesta barreja pot ser correcta en una correcció local, però s'ha de comprovar expressament i no deduir-la del color de la selecció.

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
```sql
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

### Exemple resolt: resum o repetició del resum

En un conjunt sintètic hi ha tres observacions amb `grup = 'X'` i valors coneguts, i dues amb `grup = 'Y'`. `Statistics by categories` pot crear dues files, una per X i una per Y, amb les estadístiques triades. La funció `aggregate()` utilitzada a la capa d'observacions manté cinc files i escriu a cada una el resum del seu grup. Sumar després aquest camp repetit multiplicaria el total pel nombre de files del grup.

La comprovació consisteix a identificar la unitat de la sortida. Si la pregunta demana una fila per territori, convé crear una taula agregada o relacionar el resum amb una taula territorial única. Si la pregunta necessita que cada observació conegui el total del seu grup, la repetició pot ser intencionada, però el camp s'ha de descriure com un valor de context i no com una magnitud additiva.

## Claus, unions i relacions

Una **clau primària** identifica cada fila d'una taula de manera única, estable i no nul·la. Una **clau forana** referencia la clau d'una altra taula. Per relacionar-les, els valors i els tipus han de ser compatibles: el text `'043'` no és equivalent automàticament a l'enter `43`.

Una taula pot tenir diverses **claus candidates**, és a dir, camps o combinacions que podrien identificar-ne cada fila. La que el model tria com a identificador principal és la clau primària; les altres continuen podent tenir una restricció d'unicitat. Un identificador creat pel sistema és una **clau substituta**. Pot simplificar referències internes, però no reemplaça necessàriament el codi oficial que permet integrar la taula amb fonts externes.

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

Una **unió d'atributs** afegeix columnes d'una taula d'unió a les files d'una taula objectiu mitjançant camps compatibles. La geometria, si n'hi ha, continua sent la de l'objectiu. És una representació adequada per a 1:1 o N:1: cada fila objectiu ha de trobar com a màxim una fila a la banda que aporta els atributs. L'operació no crea una correspondència fiable si aquesta banda conté diverses coincidències.

Una **relació** conserva les dues taules separades i permet navegar entre una fila pare i les files filles que en contenen la clau forana. És adequada per a 1:N perquè no obliga a triar una sola observació ni a duplicar la geometria del pare. En QGIS, una relació definida al projecte pot alimentar formularis i expressions com `relation_aggregate()`, però les dues fonts, els identificadors de relació i el projecte formen part de les dependències.

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
```sql
CASE
  WHEN length(trim(to_string("codi_muni_font"))) <= 5
  THEN lpad(trim(to_string("codi_muni_font")), 5, '0')
  ELSE NULL
END
```
:::

Aquesta expressió converteix el valor a text, elimina espais perifèrics i completa fins a cinc caràcters. La comprovació prèvia de longitud és necessària perquè `lpad()` també trunca els textos que superen l'amplada demanada; retornar nul fa visible l'anomalia en lloc de fabricar una clau aparentment vàlida. No és una recepta universal: només és correcta si la codificació esperada té cinc posicions i els valors d'entrada representen el mateix codi sense el farciment. Si el camp conté decimals introduïts per un full de càlcul, prefixos o codis de longitud superior, cal diagnosticar-los abans.

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

En el model relacional ordinari, un nul no identifica una clau i no s'ha d'utilitzar per establir una correspondència. L'algorisme `native:joinattributestable` de QGIS, però, pot emparellar un `NULL` de l'objectiu amb un `NULL` de la taula d'unió. Per conservar la semàntica declarada, abans d'executar-lo cal filtrar o extreure a banda els nuls i les cadenes buides de totes dues entrades i informar-ne el recompte {% cite qgisUserGuide344 %}.

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

Una unió per clau utilitza valors d'atribut; una **unió espacial** utilitza una relació geomètrica. Assignar cada centre educatiu al municipi que el conté és una unió espacial. Combinar físicament dos polígons mitjançant una operació geomètrica `union` és una operació diferent que es tractarà al capítol següent.

Els predicats `intersects`, `within`, `contains` i `touches` no són equivalents. Un punt situat exactament sobre el límit pot intersectar dos municipis i no trobar-se estrictament dins de cap interior. El resultat s'ha de validar comptant quantes entitats obtenen zero, una o diverses coincidències {% cite ogcSimpleFeatures2011 %}.

Un CSV de centres educatius pot convertir-se en punts si conté coordenades. Abans cal identificar quina columna és X, quina és Y, quin separador decimal utilitzen i en quin CRS s'expressen. Crear punts amb el CRS equivocat pot produir una capa aparentment buida o desplaçada; assignar una altra referència sense conèixer la font no corregeix les coordenades.

Com en una unió per clau, la cardinalitat espacial s'ha de definir abans d'executar l'eina. Un punt ordinari situat a l'interior d'una partició municipal vàlida hauria de tenir una coincidència; un punt al límit, dos polígons superposats o una geometria duplicada poden produir-ne diverses. Una línia que travessa diversos municipis té legítimament més d'una correspondència. L'eina necessita una regla per crear una fila per coincidència, prendre una sola coincidència o agregar-ne els atributs, i cada opció respon una pregunta diferent.

Un resum espacial tampoc no queda definit només pel predicat. Si es compten centres per municipi, cal decidir si cada centre pot comptar en més d'un territori, què passa amb els punts al límit i si els centres sense geometria o sense coincidència entren al denominador de cobertura. Si se sumen capacitats, els nuls, els duplicats i les coincidències múltiples poden alterar el total. Els recomptes zero, un i més d'un per entitat objectiu funcionen com a diagnòstic inicial.

### Exemple resolt: un punt sobre una frontera

En un conjunt didàctic format per dos polígons adjacents A i B, un punt P situat estrictament a l'interior d'A compleix `within(P, A)` i només s'assigna a A amb aquest predicat. Un punt Q situat exactament sobre la frontera compartida intersecta A i B, però no queda dins de l'interior de cap dels dos segons `within`. Per tant, canviar `within` per `intersects` no «arregla» el punt: canvia la regla i pot generar dues coincidències.

La resolució depèn del model. Si el punt representa una adreça que hauria d'estar dins d'una parcel·la, pot revelar un error posicional i convé revisar la font. Si representa una fita situada realment al límit, la doble intersecció és correcta i pot requerir una relació N:M. Assignar sempre la primera coincidència faria desaparèixer aquesta diferència semàntica.

## Cas guiat amb divisions administratives

La pràctica guiada utilitza una capa oficial de divisions administratives. Primer se'n revisen els camps, els tipus i les metadades. Després es construeixen consultes successives per seleccionar Catalunya, una província, un conjunt de municipis i finalment el municipi de treball. Els codis oficials s'utilitzen per validar els noms, i els noms s'utilitzen per interpretar els codis.

La progressió permet comparar coincidència exacta, pertinença a un conjunt, patrons de text i condicions compostes. També mostra per què `codi_prov = '43'` representa la província de Tarragona i no una regió funcional com el Camp de Tarragona. Les unitats territorials analítiques s'han de definir, no inferir d'un codi administratiu diferent.

En una segona fase, una taula de dades obertes amb centres educatius es converteix en punts i s'assigna als municipis. Els recomptes resultants es contrasten amb la taula original, els punts sense coincidència i una mostra situada prop dels límits.

El cas es resol en passos que deixen un control després de cada transformació. Primer es registra l'esquema de la capa administrativa i es confirma quin camp identifica cada nivell. Després es comparen els resultats d'una coincidència exacta, d'un `IN` i d'una condició composta amb parèntesis. Cada selecció es valida amb el nombre de files, els codis diferents i una inspecció dels noms; només el subconjunt necessari es materialitza al GeoPackage.

La taula de centres es perfila abans de crear punts: identificador, coordenades absents, parells duplicats, rang dels eixos i CRS declarat. Després de la unió espacial es crea un indicador de correspondència i es separen els casos amb zero, una o múltiples coincidències. La suma d'aquests grups ha de permetre reconstruir el nombre de centres processats, tenint en compte si una sortida crea una fila per coincidència.

Finalment, una taula temàtica amb clau municipal es relaciona amb els polígons. La banda que ha de ser única es comprova per codi; les claus es preparen en camps nous; i les absències s'examinen en ambdues direccions. Un camp derivat només es calcula després de confirmar numerador, denominador i unitat. El resultat conserva els codis originals, les claus preparades i prou evidència per repetir la consulta sense dependre d'una selecció activa.

## Activitats

### Comprovació: predir abans d'executar

Cal preparar sis registres curts que incloguin text, nombres, cadena buida i `NULL`. Abans d'executar cada expressió s'ha de predir quines files retornaran `TRUE`, `FALSE` o `NULL`. La comparació entre predicció i resultat permet detectar errors de precedència i tractament dels absents.

### Pràctica guiada: quatre subconjunts

Una mateixa condició s'aplicarà com a selecció, filtre de capa, regla de simbologia i extracció. Cal comparar mapa, taula, recompte i comportament d'un algorisme de processament. La conclusió ha d'indicar quines operacions només canvien l'estat del projecte i quina crea dades noves.

### Micropràctica 3: seleccions, filtres i relacions

::: table "Contracte de la micropràctica 3"
| Component | Requisit |
| --- | --- |
| Entrades | Capa administrativa oficial i una taula temàtica o CSV amb una clau o coordenades documentades |
| Operacions mínimes | Consultes simples i compostes, diagnòstic de `NULL`, extracció, preparació de clau i unió tabular o espacial |
| Resultats | Subconjunt municipal, taula relacionada i camps derivats dins del GeoPackage |
| Evidències del diari | Expressions exactes, esquema de claus, duplicats, registres sense correspondència i justificació del predicat espacial |
| Comprovacions | Recomptes abans i després, claus úniques quan correspongui, mínim i màxim dels derivats i revisió manual d'una mostra |
| Fitxers que cal conservar | GeoPackage actualitzat, projecte `.qgz` i diari amb expressions i controls |
:::

La pràctica es considera completa quan la relació es pot tornar a executar a partir de les fonts preparades i quan els registres que no han coincidit queden identificats, no amagats.
