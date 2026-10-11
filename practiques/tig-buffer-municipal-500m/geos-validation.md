# Correcció de la hipòtesi de precisió del buffer

## Versió fixada i font immutable

El `probe-runtime` de la CLI comuna i el worker de càlcul indiquen
**GEOS 3.13.1-CAPI-1.19.2**, QGIS 3.44.11, en el motor
`sha256:1003721d96abe9607d8337b36851f9b29f84c2f8f92b377d1a73ff03c9d15cd2`.
El tag upstream `3.13.1` resol al commit immutable
`431568d6e311e0bbfb057b4ec3d44d0d3ba3335f`.

Fonts contrastades en aquest commit, sense usar la documentació dev com a contracte:

- [OffsetSegmentGenerator.cpp](https://github.com/libgeos/geos/blob/431568d6e311e0bbfb057b4ec3d44d0d3ba3335f/src/operation/buffer/OffsetSegmentGenerator.cpp),
  SHA-256 `d06e97bf975ba6537f6283ce4d6cb27e03d843a6e44fff46c4335afa5fe144b3`.
- [OffsetCurveBuilder.cpp](https://github.com/libgeos/geos/blob/431568d6e311e0bbfb057b4ec3d44d0d3ba3335f/src/operation/buffer/OffsetCurveBuilder.cpp),
  SHA-256 `6e5bf0740b1292e3e7e84f2e1a8ea66a44cfe332d0ec5aca763b8db996bd35e4`.
- [BufferInputLineSimplifier.cpp](https://github.com/libgeos/geos/blob/431568d6e311e0bbfb057b4ec3d44d0d3ba3335f/src/operation/buffer/BufferInputLineSimplifier.cpp),
  SHA-256 `6e6fd74e6bb6c05a28440d8c7756c3b36266ff0f1a58d120d141d28fd0a04bb3`.
- [BufferParameters.h](https://github.com/libgeos/geos/blob/431568d6e311e0bbfb057b4ec3d44d0d3ba3335f/include/geos/operation/buffer/BufferParameters.h),
  SHA-256 `bf07a097dd8b3a6059ad8a6055f312abb03d5316bf8719c999f92c67c2d9768a`.

No es copia ni s'implementa el buffer de GEOS al consumidor. El càlcul continua
essent `native:buffer` amb els mateixos paràmetres. Les construccions elementals
següents són oracles de verificació i testimonis geomètrics locals.

## Hipòtesi fallida conservada

Els intents `run-01` i `run-02` van mantenir el mínim exigit de **497 m**
(500 ± 3 m). El mínim mostrejat real és **495,0948411931408 m**. Es conserven
els jobs `practice-f7b14a7bbd3a442b83e85ca28568927c` i
`practice-e8e57180d04e41d9931f33f4c580483d`, els seus inputs, productes parcials
i diagnòstics. La prova aritmètica de regressió continua confirmant que aquesta
mostra falla el pressupost històric. No es reescriu aquest resultat com un PASS.

L'error conceptual era extrapolar la sageta d'un polígon regular de 32 costats,
`r·(1−cos(π/32)) = 2,407636664 m`, als arcs parcials d'un polígon arbitrari.

## Derivació independent de les mesures observades

En `addDirectedFillet`, amb `q` segments per quadrant:

```text
δ = π / (2q)
n = floor(θ / δ + 0.5)
increment = θ / n
```

Si `n ≥ 1`, `θ/δ < n + 1/2`, i per tant
`θ/n < δ·(1 + 1/(2n)) ≤ 3δ/2`. Si `n = 0`, els extrems connectats delimiten
un angle menor que `δ/2`, que també queda dins d'aquesta cota.

La cota superior de sageta d'aquest mecanisme és així:

```text
E_arc(r,q) = r·(1−cos(3π/(8q)))
E_arc(500,8) = 5,411745017609492 m
```

S'hi manté una tolerància numèrica separada de **0,01 m**, fixada abans dels runs.
El pressupost de validació de la versió de font `0.1.1` és
`E_arc + 0,01 = 5,421745017609492 m`, no un arrodoniment del dèficit observat.
La banda inferior exigida és **494,5782549823905 m** i la superior es manté en
**500,01 m**. El màxim mostrejat continua havent d'arribar a 500 ± 0,01 m.

## Atribució al tram real, inclòs el retall de la corda

El run causal, encara amb el pressupost antic de 3 m, es conserva a
`sandbox/qgis-practice-jobs/practice-9a407f15883047428b7c44c117159065/`.
El seu `compute-fb35aafa59e6/stdout.log` té SHA-256
`0695e7a51f9e337e007959d20f3a795e71a9cf4fbab4165206de668f4a64f5cc`.

El vèrtex original **93** de l'anell exterior és
`(343105.55557251733, 4554959.063200004)`. Els seus veïns originals immediats són
`(343096.34552661044, 4554957.343159551)` i
`(343106.3559261644, 4554958.986151639)`.

Les normals dels dos segments originals prediuen un angle de
**16,07732368108079°**, arrodonit a **un segment**. La corda completa calculada
analíticament uneix:

- `(343013.7641168917, 4555450.565314623)`;
- `(343153.4680201198, 4555456.762303243)`.

El tram observat de 121,1884 m és una **part d'aquesta corda** de 139,8413 m:
els dos extrems observats hi pertanyen amb error calculat **0 m**, però el segon
és un punt interior de la corda, no l'extrem circular original. Això explica
que un extrem observat estigui a 497,7344 m en lloc de radi 500 m.
La sageta analítica del fillet complet és **4,913033711533399 m**; la mostra de
495,094841 m és una posició pròxima al mínim continu, no el punt mitjà exacte.

Aquesta atribució usa els veïns originals immediats: **zero vèrtexs saltats**.
No cal atribuir el mínim detectat a la simplificació `distance/100`. Això no
demostra que la simplificació no intervingui en altres trams del resultat.

## Casos mínims persistits

Tres triangles convexos, amb girs de 10°, 15° i 17° en un vèrtex conegut,
s'han desat a `arc_probe_input.gpkg` i processat amb el mateix `native:buffer`.
No tenen concavitats somes per barrejar aquest mecanisme amb la simplificació.
L'oracle són les normals i la rotació trigonomètrica del radi, no un segon buffer.

| Gir | Segments previstos | Sageta analítica (m) | Sageta native mesurada (m) |
| --- | ---: | ---: | ---: |
| 10° | 1 | 1,9026509541272274 | 1,9026509542798635 |
| 15° | 1 | 4,2775693130948085 | 4,27756931316577 |
| 17° | 2 | 1,3749074502571457 | 1,3749074500649954 |

L'error entre els extrems de les cordes analítiques i persistides és 0 m en els
tres casos. El cas de 15° refuta per si mateix la cota anterior de 3 m; el salt
a dos segments del cas de 17° contrasta l'arrodoniment, sense ajustar res al
mínim de Vila-seca. Aquests productes són diagnòstics privats, fora de la closure
dels dos projectes de lliurament.

## Què garanteix el procediment acceptat

`OffsetCurveBuilder` també simplifica amb `distance/100`, i hi ha altres
heurístiques de construcció. **No se sumen 5 m a la tolerància ni s'afirma que
E_arc sigui una cota global incondicional del motor.** La versió concreta i els
casos mínims justifiquen corregir la hipòtesi d'arcs; l'acceptació del producte
complet exigeix, a més, verificació independent contra **la font original**:

1. Distància mínima contínua entre totes les parelles de segments dels dos
   contorns, amb interseccions i projeccions ortogonals. No depèn del pas de
   mostreig de 25 m.
2. Cota superior contínua: un tram queda certificat si hi ha un mateix segment
   original a distància ≤500,01 m dels dos extrems. La distància a un segment
   convex és convexa al llarg del tram, de manera que també limita tot l'interior.
   Si no hi ha aquest testimoni, es biseca el tram; hi ha límits explícits de
   profunditat/cel·les i s'atura sense acceptar si s'exhaureixen.
3. Es conserven el mostreig, cobertura, àrea, identitat, CRS, validesa i hashes.
   Qualsevol efecte de simplificació o altra causa que tregui el contorn de la
   banda exigida farà fallar els controls; no queda absorbit sense comprovar-lo.

Així, un producte que passi té el seu **contorn poligonal complet** certificat
dins de `[494,5782549823905; 500,01]` m respecte del contorn original, amb la
precisió aritmètica i toleràncies indicades. No és una promesa de distància exacta
500 m, ni d'exactitud cartogràfica del límit CNIG, ni de resultat vàlid per a
qualsevol altra entrada sense repetir les comprovacions.
