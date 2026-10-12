---
title: "Buffer municipal de 500 m: guia docent i controls"
lang: ca
recipient: docent
content_status: draft
subject: "Tecnologies de la Informació Geogràfica"
subject_code: "21234114"
author: "Benito Zaragozí"
institution: "Universitat Rovira i Virgili"
---

## Propòsit i teoria precedent

L'activitat concreta la secció d'àrees d'influència del capítol 6 i prepara
la lectura del contracte d'un algorisme de Processament del capítol 8.
Relaciona una pregunta territorial, un sistema de referència mètric, una
transformació geomètrica i unes comprovacions independents.

La pregunta és quin àmbit resulta d'afegir 500 m al terme de Vila-seca.
El buffer positiu inclou el polígon municipal i el marge exterior. El llindar
és docent: no s'ha de presentar com una franja normativa ni com accessibilitat
en temps. La distància és plana en EPSG:25831 i les corbes s'aproximen amb
segments; cap d'aquestes decisions millora l'exactitud de la font original.

## Entrada, llicència i estats del projecte

L'entrada preparada és `municipi_treball`: una entitat MULTIPOLYGON,
EPSG:25831, `nom_muni = Vila-seca`, `codi_muni = 43171`,
`codi_oficial = 34094343171` i `id_origen = 1172246`.
Prové de la [unitat 1172246 de l'API IGN/CNIG](https://api-features.ign.es/collections/administrativeunit/items/1172246?f=json),
consultada el 8 de setembre de 2026. Atribució: obra derivada de la unitat
administrativa 1172246 de l'IGN/CNIG, **CC BY 4.0 ign.es**.

El projecte `initial.qgz` i el projecte incrustat `inicial` mostren només el
límit local. El checkpoint `resolved.qgz` i el projecte incrustat `resolt`
mostren el municipi i la capa persistent `municipi_buffer_500m`. El resultat
depèn de les dues bases locals i de DejaVu Sans, declarada entre els recursos.
Cal conservar la carpeta completa: el QGZ no incorpora automàticament les dades.
El projecte històric amb WMS és un antecedent de les fonts, no una dependència
del cas offline.

## Demostració amb QGIS

La demostració comença obrint l'estat inicial i contrastant el registre
municipal, el CRS i l'absència de filtres o seleccions. S'obre **Buffer** a
Processament (`native:buffer`) i es fixa la distància en 500 m, amb vuit
segments per quadrant, extrems i unions arrodonits, límit de mitra 2,
dissolució desactivada i separació de parts desactivada.

La sortida es desa en una capa nova del GeoPackage de resultat. Després es
comparen el contorn magenta del municipi i el farciment blau del buffer,
es llegeix la taula i es revisen els controls. La captura del resultat ha
de correspondre a aquesta capa reoberta, no només al diàleg emplenat.

## Resultats esperats i criteris d'acceptació

::: table "Controls sobre les dades persistides"
| Control | Resultat esperat |
| --- | --- |
| Recompte | Una entitat a la font, a l'inicial i al buffer |
| CRS i identitat | EPSG:25831 i els identificadors municipals indicats |
| Geometria | Poligonal, vàlida i no buida; inicial equivalent a la font |
| Cobertura | Àrea municipal fora del buffer igual a 0, amb tolerància 0,01 m² |
| Superfície | Augment estrictament positiu i dins del límit superior derivat de la font |
| Distància mínima contínua | Com a mínim 494,5782549823905 m, segons la cota d'arcs parcials i la tolerància numèrica |
| Cota superior contínua | Tot el contorn a distància no superior a 500,01 m |
| Distància màxima mostrejada | 500 m, amb tolerància 0,01 m |
| Dependències | Projectes inicial/resolt reoberts amb totes les fonts locals resoltes |
:::

La superfície exacta i els extrems mesurats s'han de llegir al registre de
l'execució contrastada. No hi ha una fórmula de polígon convex que permeti
substituir la comprovació d'aquest terme costaner. Un límit superior útil
per a l'augment és $rP + n\pi r^2$, on $P$ és el perímetre planar de totes
les vores, $n$ el nombre de parts poligonals de la font i $r = 500$ m.
Aquest límit s'acompanya del requisit separat d'augment positiu.

## Comprovació independent de distàncies

El control reobre la sortida i mostreja tots els seus anells: vèrtexs,
punts mitjans i subdivisions separades com a màxim 25 m. Per a cada mostra
es calcula la distància euclidiana al segment més proper de qualsevol
anell del municipi original, mitjançant projecció sobre el segment i
comprovació dels extrems. No es construeix un segon buffer per donar per
bo el primer.

La sageta d'una circumferència regular de 32 costats és aproximadament
2,4076 m, però no descriu tots els arcs parcials. En
[GEOS 3.13.1](https://github.com/libgeos/geos/blob/431568d6e311e0bbfb057b4ec3d44d0d3ba3335f/src/operation/buffer/OffsetSegmentGenerator.cpp),
el nombre de segments d'un fillet s'arrodoneix al més proper. Si el quantum
és $\delta=\pi/(2q)$, l'increment pot acostar-se a $3\delta/2$.
La cota d'aquest mecanisme és $r(1-\cos(3\pi/(8q)))$: **5,411745 m** amb
$r=500$ i $q=8$, més 0,01 m de tolerància numèrica separada.

El criteri inicial de 497 m es va rebutjar amb una mostra a 495,094841 m.
El tram correspon a una part d'un fillet de 16,0773° amb un segment; els
seus extrems no són tots dos els extrems circulars originals. Tres casos
convexos coneguts de 10°, 15° i 17° contrasten independentment la subdivisió
en un, un i dos segments. La correcció de la cota prové del mecanisme i
d'aquesta derivació, no d'arrodonir el dèficit observat.

El motor també pot simplificar l'entrada. Per això la cota d'arcs no es
presenta com una garantia global del motor per a qualsevol polígon. El
control calcula el mínim entre totes les parelles de segments originals
i de resultat. Per al màxim, cada interval es certifica amb un segment
original situat com a màxim a 500,01 m dels seus dos extrems; la convexitat
de la distància a aquell segment limita també l'interior. Els intervals
sense testimoni es subdivideixen i es refusen si s'exhaureix el límit de
comprovació. El màxim mostrejat ha d'arribar a 500 ± 0,01 m.

Un resultat acceptat té així el contorn complet comprovat dins de la banda
indicada respecte de la font original. La tolerància no expressa l'error
posicional de la cartografia. Qualsevol efecte de simplificació o una altra
causa que superi la banda farà fallar l'acceptació.

## Errors, evidències i interpretació docent

Cal contrastar errors com un CRS geogràfic, una selecció residual, una
sortida temporal, un radi incorrecte o una aproximació amb menys segments.
També convé distingir una mesura obliqua dibuixada al mapa de la distància
mínima fins a la frontera. Les mesures de revisió han de ser planes en
el mateix CRS que el buffer.

L'evidència mínima combina paràmetres registrats, dades persistides,
controls, captures reals inicial/resultat i reobertura independent. Una
captura antiga del diàleg només acredita la configuració visible en aquell
moment. La lectura de l'alumnat ha de conduir a una explicació pròpia del
resultat i dels seus límits, més enllà de repetir els clics.

Com a discussió final, es pot preguntar per què no canvia el llindar de
500 m en acostar el zoom, per què un polígon multipart pot ser una sola
entitat i per què un marge euclidià no equival a 500 m de recorregut viari.
Una ampliació posterior pot estudiar la sensibilitat al nombre de segments
o a una altra distància, amb destinacions noves i sense substituir aquesta fita.
