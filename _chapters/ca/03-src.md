---
lang: ca
permalink: /:title/ca/
title: "Sistemes de referència de coordenades (SRC)"
author: Benito Zaragozí
date: 2025-09-07
weight: 3
layout: chapter
mermaid: true
published: true
---

Els conjunts de dades espacials necessiten situar-se en un sistema de coordenades que permeti interpretar-los correctament sobre la superfície de la Terra. Aquesta referència la proporcionen els **Sistemes de Referència Espacial** o **Sistemes de Referència de Coordenades (SRC)**, que estableixen com es representen les posicions geogràfiques en dues dimensions.

En aquest capítol utilitzarem el terme **Sistemes de Referència Espacial (SRC)** com a traducció de l’anglès *Coordinate Reference System (CRS)*, que és la denominació formal adoptada per la [ISO 19111](https://www.iso.org/standard/74039.html) i per l’[OGC](https://www.ogc.org/standard/ct/), i també la que apareix a QGIS. En alguns manuals o programes, especialment en bases de dades com [PostGIS](https://postgis.net/docs/using_postgis_dbmanagement.html#spatial_ref_sys), també es fa servir el terme **SRS (Spatial Reference System)**. Tots dos fan referència al mateix concepte: el conjunt de definicions (el·lipsoide, datum, projecció i sistema de coordenades) que permeten interpretar correctament les coordenades en l’espai. Desenvolupem més el concepte en aquest capítol.

Ara repassarem conceptes que ja vam introduir durant el curs anterior, els ampliarem i els connectarem amb la pràctica a QGIS. La cartografia ha d'afrontar un repte fonamental: **representar la superfície corba i irregular de la Terra en un pla**. La Terra no és una esfera perfecta, sinó un cos lleugerament aplanat pels pols i amb irregularitats degudes a la distribució de masses (muntanyes, oceans). Per això, s'han definit diferents models matemàtics que permeten descriure i simplificar aquesta forma per a tenir models *útils* de la superfície terrestre.

## El geoide i l'esferoide

### El geoide

El **geoide** és la superfície que coincideix amb el nivell mitjà dels oceans prolongat sota els continents. És una construcció teòrica però alhora molt real, perquè descriu com actua la gravetat en el nostre planeta. Si poguérem veure'l representat, no seria una esfera ni un el·lipsoide regular: tindria ondulacions de fins a desenes de metres degudes a la distribució irregular de masses dins de la Terra.

Quan hi ha grans serralades, el pes de la roca fa que el camp gravitatori local s'incremente i el geoide s'eleve. En canvi, en conques oceàniques profundes o zones de materials menys densos, el geoide es deprimeix. També hi influeixen factors com la circulació oceànica, la salinitat i temperatura de l'aigua, o processos de llarg termini com l'aixecament isostàtic després d'una glaciació.

Per això no hi ha **un únic geoide immutable**, sinó diferents **models de geoide** calculats en cada moment històric amb dades específiques. Els primers models es van basar en mesures clàssiques de gravimetria i nivellació, mentre que avui dia missions satèl·litals com **[GRACE](https://grace.jpl.nasa.gov/)** o **GOCE** han permès cartografiar el geoide global amb una precisió centimètrica. A més, molts països mantenen models nacionals per afinar millor la conversió d'altures.

La seva importància pràctica és enorme: les altures que dóna el GPS són **el·lipsoïdals** (respecte a WGS84), mentre que les altures oficials en cartografia i enginyeria són **ortomètriques**, és a dir, respecte al geoide. Sense aplicar la correcció adequada, la diferència pot ser de diversos metres. Per treballs topogràfics i d'enginyeria és imprescindible utilitzar un model de geoide local per convertir les altures GPS en altures ortomètriques útils.

![Esquema del geoide i les seves ondulacions respecte a l'el·lipsoide]({{ site.baseurl }}/images/placeholder.png){: .center width="80%"}

### L'esferoide o el·lipsoide

Si el geoide reflecteix la realitat física de la Terra, l'**esferoide o el·lipsoide de revolució** és la seva simplificació matemàtica. Es tracta d'un cos regular, lleugerament aplanat pels pols, que serveix com a aproximació útil per a càlculs i representacions. Gràcies a la seva simplicitat, les equacions de coordenades són viables i permeten establir sistemes de referència a escala global o regional.

Al llarg del temps s'han definit diversos el·lipsoides, cadascun ajustat a diferents zones del món. Per exemple, el **Clarke 1866** es va utilitzar àmpliament a Amèrica del Nord, mentre que el **GRS80** i el **WGS84** són els més comuns actualment. El WGS84 és l'el·lipsoide de referència del sistema GPS i per això és universalment reconegut.

![Representació de l'esferoide o el·lipsoide de revolució com a aproximació matemàtica al geoide]({{ site.baseurl }}/images/placeholder.png){: .center width="70%"}

La relació entre geoide i el·lipsoide és clau: el geoide és el model físic que ens diu com és realment la Terra, amb totes les seves irregularitats, mentre que l'el·lipsoide és el model matemàtic que simplifica aquella complexitat i ens permet fer càlculs i mapes. En geodèsia i cartografia treballem sempre combinant-los: un **datum** és, precisament, la manera d'ajustar un el·lipsoide a un geoide i fixar-lo a un territori.

Els estudis globals utilitzen WGS84, però a Europa el més recomanat és **ETRS89/GRS80**, perquè està fixat a la placa eurasiàtica i evita els desplaçaments que genera la tectònica si només es treballa amb WGS84.

## Altures: ortomètrica vs. el·lipsoïdal

Un punt sobre la superfície de la Terra pot descriure's amb coordenades horitzontals (latitud i longitud) i també amb una **altura**. Cal diferenciar clarament dos tipus d'altura:

- **Altura ortomètrica**: És l'altura mesurada respecte al geoide, és a dir, respecte al nivell mitjà del mar. És la que s'utilitza en cartografia oficial, enginyeria i estudis hidrològics, perquè correspon a la realitat física del terreny.
- **Altura el·lipsoïdal**: És l'altura mesurada respecte a un el·lipsoide (per exemple, el WGS84). És la que retorna un receptor GPS, perquè el càlcul es fa directament sobre el model matemàtic.

La diferència entre totes dues, anomenada **ondulació del geoide (N)**, pot arribar fàcilment als 40 o 50 metres depenent de la regió. Per això, quan utilitzem GPS en treballs d'enginyeria, sempre cal aplicar un model de geoide que permeti convertir altures el·lipsoïdals en ortomètriques.

![Esquema de les altures: el·lipsoïdal (h), ortomètrica (H) i ondulació del geoide (N)]({{ site.baseurl }}/images/placeholder.png){: .center width="70%"}

En QGIS i altres programes, aquestes conversions es poden configurar amb transformacions oficials si tenim disponible el model de geoide adequat (per exemple, EGM2008 o el geoide d'Espanya calculat per l'IGN).

## Els datums

El **datum** és l'element que connecta el món teòric (geoide i el·lipsoide) amb la realitat cartogràfica. En termes senzills, un datum és la manera d'**anclar un el·lipsoide a la Terra real**, definint-ne la posició, l'orientació i els punts de control que li donen estabilitat.

Un datum estableix:

- quin el·lipsoide es fa servir (GRS80, WGS84, Clarke, etc.)
- on es col·loca el centre d'aquest el·lipsoide respecte al centre de masses de la Terra
- com es relaciona amb punts físics mesurats sobre el territori (xarxes geodèsiques)

Per això diem que el datum és la **traducció pràctica** de la teoria a la realitat cartogràfica d'un país o d'un continent.

### Datums locals i globals

Històricament, cada regió utilitzava el seu propi datum local, ajustat a les necessitats de precisió en un territori concret. Per exemple:

- **ED50** (European Datum 1950), molt utilitzat a Europa fins a finals del segle XX
- **NAD27** a Amèrica del Nord

Amb la irrupció de la navegació per satèl·lit i la globalització de dades, es va imposar la necessitat de datums globals:

- **WGS84**, definit per al sistema GPS, és avui el més universal
- **ETRS89** (European Terrestrial Reference System 1989) és la versió europea, fixada a la placa eurasiàtica per evitar els desplaçaments tectònics respecte al WGS84

Encara que WGS84 i ETRS89 coincideixen pràcticament en l'any 1989, amb el pas del temps la placa euroasiàtica s'ha anat desplaçant. Així, a dia d'avui, hi ha diferències de més de 80 cm que continuaran creixent. Per això, en treballs oficials a Europa sempre s'ha d'utilitzar ETRS89.

### Exemples en QGIS

Quan obrim les propietats d'una capa a QGIS i veiem un SRC com **EPSG:25831**, en realitat estem parlant d'un **datum (ETRS89)**, un **el·lipsoide (GRS80)** i una **projecció (UTM 31N)** combinats en un sol codi.

![Exemple de definició d'un SRC en QGIS mostrant el datum, l'el·lipsoide i la projecció]({{ site.baseurl }}/images/placeholder.png){: .center width="80%"}

Aquesta informació prové de la base de dades **EPSG Geodetic Parameter Dataset**, mantinguda per l'[International Association of Oil & Gas Producers (IOGP)](https://epsg.org/), que és l'estàndard mundial.

### Per què els datum son tan importants?

La correcta elecció d'un datum evita desplaçaments de desenes o centenars de metres entre capes. Un arxiu històric en ED50 sobreposat a un en ETRS89 mostrarà un desajust visible, tot i que les dades siguin correctes cadascuna per separat. Saber identificar i, si cal, **reprojectar** capes entre datums és una competència fonamental en SIG. Per exemple, si treballes amb dades d'Espanya anteriors als anys 2000, cal comprovar si estan en ED50. Moltes cartografies menys actuals i *shapefiles* antics encara utilitzen aquest datum i necessiten ser reprojectats a ETRS89.

## Projeccions cartogràfiques

Un cop definides les superfícies de referència (geoide i el·lipsoide) i els datums que les fixen, encara ens queda un pas fonamental: **com representar la Terra en un mapa pla**. Cap projecció és neutra: sempre hi haurà deformacions, ja sigui en distàncies, en àrees o en angles. L'art de la cartografia consisteix a **escollir la projecció que més convingui segons la finalitat del mapa**.

### Superfícies de projecció

La manera clàssica d'explicar-ho és imaginar que projectem la Terra sobre una superfície geomètrica senzilla, que després podem desplegar:

- **Cilindre** → projeccions cilíndriques (ex.: Mercator)
- **Con** → projeccions còniques (ex.: Lambert Cònica Conforme)
- **Disc o pla** → projeccions azimutals (ex.: Estereogràfica, Azimutal equidistant)

![Superfícies de projecció: cilindre, con i pla aplicats a l'el·lipsoide]({{ site.baseurl }}/images/placeholder.png){: .center width="80%"}

Cada superfície pot tocar l'el·lipsoide en una línia (projecció tangent) o en dues (secant). Allà on hi ha contacte, la deformació és mínima; a mesura que ens allunyem, augmenta.

### Tipus principals de projeccions

- **Conformes**: conserven els angles i les formes locals, ideals per a cartografia topogràfica i navegació. Exemple: Mercator
- **Equivalents**: conserven les àrees, útils per a mapes temàtics (ex.: població, ús del sòl). Exemple: Albers
- **Equidistants**: conserven distàncies només en determinades direccions. Exemple: Azimutal equidistant
- **Compromís**: busquen un balanç entre deformacions. Exemple: Robinson o Winkel-Tripel, usades sovint en mapes mundials

![Comparació de projeccions: Mercator (conforme), Albers (equivalent) i Robinson (compromís)]({{ site.baseurl }}/images/placeholder.png){: .center width="100%"}

> **Consell**: No hi ha projecció perfecta. La clau és preguntar-se: què volem preservar? Si necessitem calcular àrees, escollirem una projecció equivalent; si ens interessa la navegació o la geometria local, una conforme.
{: .block-tip }

## Sistemes de coordenades: geogràfics i projectats

Quan representem un punt sobre la Terra necessitem dues coses: un **sistema de referència** i un **sistema de coordenades** que ens permeti descriure la seva posició. Els més habituals són els **geogràfics** i els **projectats**, cadascun amb virtuts i limitacions.

### Sistemes de coordenades geogràfics

En un sistema geogràfic, un punt s'expressa mitjançant **latitud i longitud**, és a dir, els angles que defineixen la seva posició respecte a l'equador i al meridià de Greenwich.

- La **latitud** s'expressa en graus nord o sud (de −90° a +90°)
- La **longitud** s'expressa en graus est o oest (de −180° a +180°)

Aquests sistemes són universals i molt intuïtius: qualsevol GPS ens dóna coordenades en WGS84 geogràfic (EPSG:4326). Però tenen un inconvenient: **les distàncies i superfícies no es poden calcular directament**. Un grau de longitud no equival sempre al mateix nombre de quilòmetres; a l'equador són uns 111 km, però a mesura que ens apropem als pols aquesta distància es redueix fins a zero.

![Mapa en WGS84 geogràfic on les distàncies i superfícies es distorsionen]({{ site.baseurl }}/images/placeholder.png){: .center width="80%"}

Si treballem amb dades globals o compartim informació en serveis web, l'opció més habitual és un **sistema geogràfic** com WGS84 (EPSG:4326).

Així, els sistemes geogràfics són ideals per emmagatzemar i compartir dades globals, però no per fer càlculs precisos de distància o superfície.

### Sistemes de coordenades projectats

Per poder treballar amb **unitats lineals** (metres, peus), transformem la superfície corba de la Terra a un **pla** mitjançant una projecció cartogràfica. El resultat és un sistema de coordenades projectat.

Aquí les coordenades ja no són angles, sinó valors en metres sobre eixos X i Y. Això ens permet mesurar distàncies, calcular superfícies o generar buffers amb precisió. Però a canvi, la projecció només és vàlida dins d'un **àmbit concret**: a mesura que ens allunyem del centre o fus de projecció, les deformacions augmenten.

![Mapa projectat en UTM (ETRS89/UTM 31N) on les coordenades són en metres]({{ site.baseurl }}/images/placeholder.png){: .center width="80%"}

Si volem calcular àrees, distàncies o fer geoprocessaments precisos, necessitem un **sistema projectat**, com ara les projeccions UTM.

> **Atenció!** QGIS pot reprojectar "al vol" les capes geogràfiques a projectades per visualitzar-les juntes, però per fer **anàlisi espacial** és essencial que totes les dades estiguin en el mateix sistema projectat.
{: .block-danger }

## El sistema UTM

Un dels sistemes de coordenades projectats més utilitzats arreu del món és el **UTM (Universal Transversa de Mercator)**. La seva popularitat es deu al fet que ofereix coordenades en metres, és conforme (preserva els angles i les formes locals) i cobreix pràcticament tot el planeta de manera homogènia.

### Com funciona?

La Terra es divideix en **60 fusos de 6° de longitud cadascun**, numerats d'oest a est des del meridià de 180°. Cada fus es projecta de manera independent mitjançant una projecció **cilíndrica transversa de Mercator**: en lloc d'un cilindre al voltant de l'equador, s'utilitza un cilindre "girant" que toca la Terra en un meridià central.

Aquesta tècnica minimitza les deformacions dins de cada fus, però limita l'abast: un sistema UTM és vàlid només dins del fus per al qual ha estat definit.

![Mapa mundial amb la divisió en 60 fusos UTM]({{ site.baseurl }}/images/placeholder.png){: .center width="80%"}

### El cas d'Espanya i Catalunya

La Península Ibèrica es reparteix entre dos fusos UTM:

- **30N**: Galícia, Castella, Andalusia i part d'Extremadura
- **31N**: Catalunya, País Valencià, Balears i Aragó oriental

Les Illes Canàries queden en els fusos 27N i 28N.

A la pràctica, a Catalunya treballem amb **ETRS89 / UTM zona 31N (EPSG:25831)**. En canvi, si el projecte abasta Castella o Andalusia caldrà utilitzar l'**ETRS89 / UTM zona 30N (EPSG:25830)**.

![Mapa dels fusos UTM a Espanya: 30N i 31N]({{ site.baseurl }}/images/placeholder.png){: .center width="80%"}

> **Atenció!** si carregues en un mateix projecte dades del fus 30N i del 31N, QGIS pot reprojectar-les *al vol*, però per fer anàlisi espacial cal que totes les capes siguin coherents en un únic SRC.
{: .block-warning }

## Els codis EPSG

Els codis EPSG identifiquen de manera inequívoca cada sistema de referència espacial. Provenen de la base de dades mantinguda per l'antic **European Petroleum Survey Group (EPSG)**, avui dins de l'**International Association of Oil & Gas Producers (IOGP)**. Aquesta base de dades es va crear per garantir la coherència i compatibilitat dels sistemes de coordenades en contextos internacionals.

La **EPSG Geodetic Parameter Dataset** s'ha convertit en el referent global i és utilitzada per la majoria de programes SIG. Es pot consultar lliurement a: [https://epsg.io/](https://epsg.io/).

Quan seleccionem un SRC a QGIS, sovint apareix una descripció textual que prové d'aquesta base. Per exemple, per a **EPSG:25831 (ETRS89 / UTM zona 31N)**, QGIS mostra:

```bash
+proj=utm +zone=31 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs
```

Aquesta cadena descriu la projecció, el fus, l'el·lipsoide i els paràmetres de transformació.

### Codis EPSG més habituals

A la taula següent trobaràs els codis EPSG més utilitzats segons l'àrea d'estudi:

| **Codi EPSG** | **Nom**                               | **Tipus**     | **Ús recomanat** |
|---------------|---------------------------------------|---------------|------------------|
| 4326          | WGS84 (geogràfiques)                  | Geogràfic     | Dades globals, GPS, serveis web |
| 4258          | ETRS89 (geogràfiques)                 | Geogràfic     | Estàndard europeu |
| 3857          | Pseudo-Mercator (Web Mercator)        | Projectat     | Mapes web (Google, OSM, Bing) |
| 25830         | ETRS89 / UTM fus 30N                  | Projectat     | Espanya occidental |
| 25831         | ETRS89 / UTM fus 31N                  | Projectat     | Catalunya, País Valencià, Balears |
| 32631         | WGS84 / UTM fus 31N                   | Projectat     | Usos internacionals (datum WGS84) |
| 23030         | ED50 / UTM fus 30N (obsolet)          | Projectat     | Cartografia històrica a Espanya |
| 23031         | ED50 / UTM fus 31N (obsolet)          | Projectat     | Cartografia històrica a Catalunya |

Els codis més rellevants per al nostre curs són:

- **EPSG:25830** → ETRS89 / UTM zona 30N
- **EPSG:25831** → ETRS89 / UTM zona 31N

També existeixen variants en WGS84, com EPSG:32630 o EPSG:32631, habituals en dades GPS i serveis internacionals.

![Comparació de projeccions WGS84 (EPSG:4326) i ETRS89/UTM 31N (EPSG:25831)]({{ site.baseurl }}/images/placeholder.png){: .center width="100%"}

Una menció especial mereix la projecció **Web Mercator** o **Pseudo-Mercator** (EPSG:3857), desenvolupada per Google per als seus mapes web i adoptada posteriorment per la majoria de serveis similars (OpenStreetMap, Bing Maps, etc.).

Aquesta projecció és una variant simplificada de la clàssica projecció de Mercator que utilitza l'el·lipsoide WGS84 però el tracta com si fos una esfera perfecta. Això permet càlculs més ràpids i una implementació més senzilla en aplicacions web, però introdueix petites distorsions addicionals, especialment a latituds altes.

Tot i les seves limitacions tècniques, la Web Mercator s'ha convertit in l'estàndard de facto per a la visualització de mapes a internet gràcies a la seva rapidesa de renderitzat i compatibilitat universal.

## Pràctica

1. **Verificar el SRC del projecte.** A QGIS, obre `Propietats del projecte > SRC` i comprova que estigui configurat a ETRS89 / UTM 31N (EPSG:25831)
2. **Comprovar el SRC d'una capa.** Fes clic dret → `Propietats` → pestanya `Informació`
3. **Reprojectar capes.** Exporta la capa amb `Exporta > Desa com...` i selecciona un altre EPSG
4. **Visualitzar els fusos UTM.** Desa i carrega en QGIS un shapefile de fusos UTM (CNIG). Identifica si la teva zona cau en el 30N o 31N
5. **Comparar representacions.** Carrega una capa en EPSG:4326 i una altra en EPSG:25831 i observa les diferències
6. **Trobar el SRC adequat per a altres regions europees.** Utilitza [epsg.io](https://epsg.io/) per determinar quin seria el sistema de coordenades més adequat per a:
   - Calcular superfícies de parcs urbans a Roma (Itàlia)
   - Mesurar distàncies entre ciutats a França
   - Analitzar la xarxa de transport a Alemanya
7. **Investigar sistemes nacionals.** Consulta la documentació oficial dels instituts geogràfics nacionals i descobreix:
   - Quin sistema oficial utilitza França per a la cartografia nacional?
   - Quins sistemes recomanats utilitza l'Institut Cartogràfic i Geològic de Catalunya (ICGC)?
   - Com es denomina el sistema de coordenades oficial d'Itàlia?
8. **Exercici pràctic internacional.** Descarrega dades vectorials d'OpenStreetMap de dues ciutats europees diferents (per exemple, Lisboa i Varsòvia). Identifica en quin SRC arriben les dades i determina a quin sistema les hauríeu de reprojectar per fer càlculs precisos d'àrea en cada cas.
9. **Anàlisi crítica.** Explica per què no és recomanable utilitzar WGS84 geogràfic (EPSG:4326) per calcular l'àrea d'un bosc a Catalunya. Quines diferències esperes trobar si compares els resultats amb ETRS89/UTM 31N?
