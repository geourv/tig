---
title: "Àrea d’influència municipal de 500 m"
lang: ca
recipient: alumnat
content_status: draft
subject: "Tecnologies de la Informació Geogràfica"
subject_code: "21234114"
author: "Benito Zaragozí"
institution: "Universitat Rovira i Virgili"
---

## Pregunta territorial i teoria precedent

Quin àmbit resulta d'afegir un marge de 500 m al terme de Vila-seca? Aquesta
activitat aplica els conceptes del capítol 6 del manual: distància, àrea
d'influència i diferència entre una capa d'entrada i una geometria derivada.

Un buffer positiu d'un polígon comprèn el polígon i les posicions exteriors
que queden a la distància fixada o més a prop. Per això la seva superfície ha
de ser superior a la municipal. El valor de 500 m és un escenari docent per
contrastar el càlcul; no representa una franja legal ni un temps de recorregut.

La distància es calcula en el pla de les coordenades de la capa. L'entrada
treballa en ETRS89 / UTM zona 31N, **EPSG:25831**, amb unitats mètriques. Els
arcs s'aproximen amb segments rectes: vuit segments per quadrant equivalen
a 32 segments en una circumferència completa.

>>>>> En acabar l'activitat, cal poder:
>>>>>
>>>>> - Executar un buffer amb paràmetres i destinació explícits.
>>>>> - Distingir el terme municipal de la seva àrea d'influència.
>>>>> - Comprovar recompte, CRS, geometria i distàncies del resultat.
>>>>> - Reobrir el projecte amb totes les dependències locals disponibles.

## Dades i condicions d'ús

La capa `municipi_treball` conté una sola entitat, identificada per
`codi_muni = 43171` i `nom_muni = Vila-seca`. Deriva de la
[unitat administrativa 1172246 de l'IGN/CNIG](https://api-features.ign.es/collections/administrativeunit/items/1172246?f=json),
consultada el 8 de setembre de 2026 i preparada en EPSG:25831. Atribució:
**obra derivada de la unitat administrativa 1172246 de l'IGN/CNIG,
CC BY 4.0 ign.es**. El codi identifica el municipi; no és una mesura.

El projecte inicial és local i es pot treballar sense WMS. El marge calculat
hereta l'escala, la data i les limitacions del límit administratiu utilitzat.
Una distància de càlcul precisa no converteix aquesta font en una delimitació
de precisió cadastral.

## Preparar el projecte

Cal conservar el paquet rebut i treballar en una còpia completa de la seva
carpeta. S'obre `initial.qgz`, mantenint la disposició relativa de dades i
recursos. A la taula d'atributs s'ha de trobar una entitat de Vila-seca; a les
propietats de la capa, EPSG:25831. El projecte inclou el mateix estat inicial
incrustat al GeoPackage, amb el nom `inicial`.

Abans de processar, cal retirar qualsevol filtre o selecció accidental i
identificar la destinació nova. La capa municipal original s'utilitza com a
entrada i es conserva per comparar-la amb el resultat.

## Executar el buffer a QGIS

Des de la caixa d'eines de Processament es localitza **Buffer**,
identificat com `native:buffer`. El diàleg ha de tenir aquesta configuració:

::: table "Paràmetres del buffer municipal"
| Paràmetre | Valor |
| --- | --- |
| Entrada | `municipi_treball` |
| Distància | 500 m |
| Segments per quadrant | 8 |
| Estil dels extrems i de les unions | Arrodonit |
| Límit de mitra | 2 |
| Dissoldre el resultat | Desactivat |
| Separar parts disjuntes | Desactivat |
| Sortida | Capa persistent `municipi_buffer_500m`, en un GeoPackage nou |
:::

La destinació ha de quedar dins de la carpeta de treball i tenir un nom
diferent de l'entrada. Després d'executar, cal comprovar el registre de
Processament i carregar la capa desada. El terme municipal es representa
amb un contorn magenta i el buffer, amb farciment blau, de manera que es
puguin distingir la frontera original i el marge exterior.

## Comprovar i interpretar

La taula de la sortida ha de contenir una entitat amb els identificadors
municipals. Cal comprovar el CRS, validar la geometria i comparar l'extensió
i la superfície amb l'entrada. El municipi ha de quedar cobert pel buffer,
però el contorn del buffer ha de ser diferent del límit municipal.

Convé mesurar algunes distàncies en trams rectes i en cantonades, utilitzant
mesura plana en EPSG:25831. La distància pertinent és la més curta fins al
límit original; una línia obliqua dibuixada arbitràriament pot ser més llarga.
Als arcs aproximats, el punt mitjà d'un segment pot quedar lleugerament per
sota dels 500 m. Aquesta diferència geomètrica s'ha de distingir de la
incertesa de la font cartogràfica.

Amb vuit segments per quadrant no s'obté una distància exacta de 500 m en
tots els punts: els arcs parcials poden tenir una subdivisió diferent de
la d'una circumferència regular. El control d'aquesta activitat exigeix
que tot el contorn quedi entre aproximadament **494,578 m i 500,01 m** del
contorn original, i en comprova els segments complets. Aquesta és la
precisió acceptada del procediment contrastat, no la precisió topogràfica
del límit municipal.

## Errors freqüents i evidències

Cal revisar especialment una entrada en graus, una selecció no prevista,
una sortida temporal, la confusió entre canviar el CRS de la vista i
reprojectar dades, o el desament sobre la capa original. Un mapa que sembla
correcte pot continuar depenent d'una capa temporal o d'una ruta externa.

Els apunts han de recollir la pregunta, la font, els paràmetres i les
comprovacions. Una captura inicial ha de mostrar la capa i el municipi;
una captura posterior, la capa desada i el seu marge. La captura del diàleg
configurat ajuda a documentar la decisió, però cal acompanyar-la del resultat
real. També s'han de registrar els recomptes, les mesures contrastades i les
dificultats trobades.

Finalment es desa un projecte de resultat amb un nom nou. Cal tancar QGIS i
reobrir la carpeta completa des d'una ubicació diferent, comprovant que les
dues capes continuen disponibles. Els identificadors interns, les dades i
els recursos tipogràfics han de viatjar junts. La conclusió ha d'explicar què
representa el marge de 500 m i quines afirmacions sobre accessibilitat o
protecció territorial no es poden deduir només d'aquest buffer.
