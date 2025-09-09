---
lang: es
permalink: /:title/es/
title: "Sistemas de Referencia de Coordenadas (SRC)"
author: Benito Zaragozí
date: 2025-09-07
weight: 3
layout: chapter
mermaid: true
published: true
---

Los conjuntos de datos espaciales necesitan situarse en un sistema de coordenadas que permita interpretarlos correctamente sobre la superficie terrestre. Esta referencia la proporcionan los **Sistemas de Referencia de Coordenadas (SRC)**, que establecen cómo se representan las posiciones geográficas en dos dimensiones.

En este capítulo utilizaremos el término **Sistemas de Referencia de Coordenadas (SRC)** como traducción del inglés *Coordinate Reference System (CRS)*, que es la denominación formal adoptada por la [ISO 19111](https://www.iso.org/standard/74039.html) y por el [OGC](https://www.ogc.org/standard/ct/), y también la que aparece en QGIS. En algunos manuales o programas, especialmente en bases de datos como [PostGIS](https://postgis.net/docs/using_postgis_dbmanagement.html#spatial_ref_sys), también se utiliza el término **SRS (Spatial Reference System)**. Ambos hacen referencia al mismo concepto: el conjunto de definiciones (elipsoide, datum, proyección y sistema de coordenadas) que permiten interpretar correctamente las coordenadas en el espacio. Desarrollamos más este concepto en este capítulo.

Ahora repasaremos conceptos que ya introdujimos durante el curso anterior, los ampliaremos y los conectaremos con la práctica en QGIS. La cartografía debe afrontar un reto fundamental: **representar la superficie curva e irregular de la Tierra en un plano**. La Tierra no es una esfera perfecta, sino un cuerpo ligeramente achatado por los polos y con irregularidades debidas a la distribución de masas (montañas, océanos). Por ello, se han definido diferentes modelos matemáticos que permiten describir y simplificar esta forma para tener modelos *útiles* de la superficie terrestre.

## El geoide y el elipsoide

### El geoide

El **geoide** es la superficie que coincide con el nivel medio de los océanos prolongado bajo los continentes. Es una construcción teórica pero muy real, ya que describe cómo actúa la gravedad en nuestro planeta. Si pudiéramos verlo representado, no sería una esfera ni un elipsoide regular: tendría ondulaciones de hasta decenas de metros debidas a la distribución irregular de masas dentro de la Tierra.

Cuando hay grandes cordilleras, el peso de la roca hace que el campo gravitatorio local se incremente y el geoide se eleve. En cambio, en cuencas oceánicas profundas o zonas de materiales menos densos, el geoide se deprime. También influyen factores como la circulación oceánica, la salinidad y temperatura del agua, o procesos de largo plazo como el levantamiento isostático tras una glaciación.

Por eso no existe **un único geoide inmutable**, sino diferentes **modelos de geoide** calculados en cada momento histórico con datos específicos. Los primeros modelos se basaron en mediciones clásicas de gravimetría y nivelación, mientras que hoy en día misiones satelitales como **[GRACE](https://grace.jpl.nasa.gov/)** o **GOCE** han permitido cartografiar el geoide global con precisión centimétrica. Además, muchos países mantienen modelos nacionales para afinar mejor la conversión de alturas.

![Representación esquemática del geoide como superficie equipotencial irregular. Geoide terrestre: superficie irregular que representa el nivel medio del mar equipotencial. Fuente: nosmienten.com vía Wikimedia Commons, File:Geoide.jpg (CC BY-SA 4.0).]({{ site.baseurl }}/images/geoid.png){: .center width="100%"}

### El elipsoide

Si el geoide refleja la realidad física de la Tierra, el **elipsoide de revolución** es su simplificación matemática. Se trata de un cuerpo regular, ligeramente achatado por los polos, que sirve como aproximación útil para cálculos y representaciones. Gracias a su simplicidad, las ecuaciones de coordenadas son viables y permiten establecer sistemas de referencia a escala global o regional.

A lo largo del tiempo se han definido diversos elipsoides, cada uno ajustado a diferentes zonas del mundo. Por ejemplo, el **Clarke 1866** se utilizó ampliamente en Norteamérica, mientras que el **GRS80** y el **WGS84** son los más comunes actualmente. El WGS84 es el elipsoide de referencia del sistema GPS y por eso es universalmente reconocido.

![Comparación de dos elipsoides regionales (NAD27 y ED50) respecto al centro de masa de la Tierra {% cite JanvanSickle15 %}.]({{ site.baseurl }}/images/two-regional-ellipsoids.png){: .center width="80%"}

La relación entre geoide y elipsoide es clave: el geoide es el modelo físico que nos dice cómo es realmente la Tierra, con todas sus irregularidades, mientras que el elipsoide es el modelo matemático que simplifica esa complejidad y nos permite hacer cálculos y mapas. En geodesia y cartografía siempre trabajamos combinándolos: un **datum** es, precisamente, la forma de ajustar un elipsoide a un geoide y fijarlo a un territorio.

Los estudios globales utilizan WGS84, pero en Europa el más recomendado es **ETRS89/GRS80**, porque está fijo a la placa euroasiática y evita los desplazamientos que genera la tectónica si solo se trabaja con WGS84.

## Alturas: ortométrica vs. elipsoidal

Un punto sobre la superficie de la Tierra puede describirse con coordenadas horizontales (latitud y longitud) y también con una **altura**. Es necesario diferenciar dos tipos de altura:

- **Altura ortométrica**: Es la altura medida respecto al geoide, es decir, respecto al nivel medio del mar. Es la que se utiliza en cartografía oficial, ingeniería y estudios hidrológicos, porque corresponde a la realidad física del terreno.
- **Altura elipsoidal**: Es la altura medida respecto a un elipsoide (por ejemplo, el WGS84). Es la que retorna un receptor GPS, ya que el cálculo se realiza directamente sobre el modelo matemático.

La diferencia entre ambas, llamada **ondulación del geoide (N)**, puede alcanzar fácilmente los 40 o 50 metros dependiendo de la región. Por eso, cuando utilizamos GPS en trabajos de ingeniería, siempre es necesario aplicar un modelo de geoide que permita convertir alturas elipsoidales en ortométricas.

Su importancia práctica es enorme. Por ejemplo, las alturas que da el GPS son **elipsoidales** (respecto a WGS84), mientras que las alturas oficiales en cartografía e ingeniería son **ortométricas**, es decir, respecto al geoide. Sin aplicar la corrección adecuada, la diferencia puede ser de varios metros. Para trabajos topográficos y de ingeniería es imprescindible utilizar un modelo de geoide local para convertir las alturas GPS en alturas ortométricas útiles.

![Comparación entre el geoide y el elipsoide WGS84, con las ondulaciones geoidales y fórmulas de altura ortométrica. Fuente: geologician, “Earth's Geoid compared with WGS84 ellipsoid”, Wikimedia Commons (cc by-sa 4.0)]({{ site.baseurl }}/images/geoid-vs-ellipsoid.png)

En QGIS y otros programas, estas conversiones se pueden configurar con transformaciones oficiales si disponemos del modelo de geoide adecuado (por ejemplo, EGM2008 o el geoide de España calculado por el IGN).

## Los datums

El **datum** es el elemento que conecta el mundo teórico (geoide y elipsoide) con la realidad cartográfica. En términos sencillos, un datum es la forma de **anclar un elipsoide a la Tierra real**, definiendo su posición, orientación y los puntos de control que le dan estabilidad.

Un datum establece:

- qué elipsoide se utiliza (GRS80, WGS84, Clarke, etc.)
- dónde se coloca el centro de ese elipsoide respecto al centro de masas de la Tierra
- cómo se relaciona con puntos físicos medidos sobre el territorio (redes geodésicas)

Por eso decimos que el datum es la **traducción práctica** de la teoría a la realidad cartográfica de un país o continente.

### Datums locales y globales

Históricamente, cada región utilizaba su propio datum local, ajustado a las necesidades de precisión de un territorio concreto. Por ejemplo:

- **ED50** (European Datum 1950), muy utilizado en Europa hasta finales del siglo XX
- **NAD27** en Norteamérica

Con la irrupción de la navegación por satélite y la globalización de datos, se impuso la necesidad de datums globales:

- **WGS84**, definido para el sistema GPS, es hoy el más universal
- **ETRS89** (European Terrestrial Reference System 1989) es la versión europea, fijada a la placa euroasiática para evitar los desplazamientos tectónicos respecto a WGS84

Aunque WGS84 y ETRS89 coincidían prácticamente en 1989, con el paso del tiempo la placa euroasiática se ha ido desplazando. Así, actualmente existen diferencias de más de 80 cm que seguirán aumentando. Por eso, en trabajos oficiales en Europa siempre se debe utilizar ETRS89.

### Ejemplos en QGIS

Cuando abrimos las propiedades de una capa en QGIS y vemos un SRC como **EPSG:25831**, en realidad estamos hablando de un **datum (ETRS89)**, un **elipsoide (GRS80)** y una **proyección (UTM 31N)** combinados en un solo código.

![Ejemplo de definición de un SRC en QGIS mostrando el datum, el elipsoide y la proyección]({{ site.baseurl }}/images/crs-selection-in-qgis.png){: .center width="100%"}

Esta información proviene de la base de datos **EPSG Geodetic Parameter Dataset**, mantenida por la [International Association of Oil & Gas Producers (IOGP)](https://epsg.org/), que es el estándar mundial.

> **¿Por qué son tan importantes los datums?** La correcta elección de un datum evita desplazamientos de decenas o cientos de metros entre capas. Un archivo histórico en ED50 superpuesto a uno en ETRS89 mostrará un desfase visible, aunque los datos sean correctos por separado. Saber identificar y, si es necesario, **reproyectar** capas entre datums es una competencia fundamental en SIG. Por ejemplo, si trabajas con datos de España anteriores al año 2000, debes comprobar si están en ED50. Muchos mapas menos actuales y *shapefiles* antiguos aún utilizan este datum y necesitan ser reproyectados a ETRS89.
{: .block-warning }

## Proyecciones cartográficas

Una vez definidas las superficies de referencia (geoide y elipsoide) y los datums que las fijan, aún queda un paso fundamental: **cómo representar la Tierra en un mapa plano**. Ninguna proyección es neutra: siempre habrá deformaciones, ya sea en distancias, en áreas o en ángulos. El arte de la cartografía consiste en **elegir la proyección que más convenga según la finalidad del mapa**.

### Superficies de proyección

La forma clásica de explicarlo es imaginar que proyectamos la Tierra sobre una superficie geométrica sencilla, que después podemos desplegar:

- **Cilindro** → proyecciones cilíndricas (ej.: Mercator)
- **Cono** → proyecciones cónicas (ej.: Lambert Cónica Conforme)
- **Disco o plano** → proyecciones azimutales (ej.: Estereográfica, Azimutal equidistante)

![Superficies de proyección: plano (azimutal), cilindro (cilíndrica) y cono (cónica) aplicados conceptualmente al elipsoide. Fuente: Charles Preppernau (2022), “The three developable projection surfaces: cylinder, cone and plane”, licencia CC BY 4.0. ]({{ site.baseurl }}/images/projection-surfaces.png){: .center width="70%"}

Cada superficie puede tocar el elipsoide en una línea (proyección tangente) o en dos (secante). Donde hay contacto, la deformación es mínima; a medida que nos alejamos, aumenta.

### Tipos principales de proyecciones

- **Conformes**: conservan los ángulos y las formas locales, ideales para cartografía topográfica y navegación. Ejemplo: Mercator
- **Equivalentes**: conservan las áreas, útiles para mapas temáticos (ej.: población, uso del suelo). Ejemplo: Albers
- **Equidistantes**: conservan distancias sólo en determinadas direcciones. Ejemplo: Azimutal equidistante
- **Compromiso**: buscan un equilibrio entre deformaciones. Ejemplo: Robinson o Winkel-Tripel, usadas en mapas mundiales

![Comparación de proyecciones: Mercator (conforme) y Albers (equiárea). Fuente: Tobias Jung, map-projections.net (CC BY-SA 4.0).]({{ site.baseurl }}/images/map-projections-comparison-mercator-albers.png){: .center width="100%"}

La indicatriz de Tissot es un método clásico para visualizar las distorsiones que introducen las proyecciones cartográficas. Consiste en dibujar círculos iguales sobre la superficie de la Tierra y observar cómo se deforman al proyectarse en el mapa. Si la proyección conserva las formas locales (proyección conforme), los círculos se mantienen como círculos pero pueden variar de tamaño; si conserva las áreas (proyección equiárea), los círculos pueden transformarse en elipses pero con la misma superficie; y en proyecciones de compromiso, aparecen distorsiones tanto en forma como en tamaño. En la imagen, la proyección cilíndrica equiárea de Behrmann muestra cómo los círculos se deforman progresivamente en elipses más achatadas a medida que nos alejamos del ecuador, evidenciando la variación de escala y distorsión según la latitud.

![Indicatriz de Tissot sobre proyección cilíndrica igual-área (Behrmann), que muestra cómo distancias y superficies se distorsionan con la latitud — utilizado aquí como analogía para el sistema de coordenadas geográfico WGS84 sin proyección directa (Plate Carrée), donde las distorsiones son similares en tendencia.]({{ site.baseurl }}/images/tissot-behrmann.png){: .center width="80%"}

> **Consejo**: No existe proyección perfecta. La clave es preguntarse: ¿qué queremos preservar? Si necesitamos calcular áreas, elegiremos una proyección equivalente; si nos interesa la navegación o la geometría local, una conforme.
{: .block-tip }

## Sistemas de coordenadas: geográficos y proyectados

Al representar un punto sobre la Tierra necesitamos dos cosas: un **sistema de referencia** y un **sistema de coordenadas** que nos permita describir su posición. Los más habituales son los **geográficos** y los **proyectados**, cada uno con ventajas y limitaciones.

### Sistemas de coordenadas geográficos

En un sistema geográfico, un punto se expresa mediante **latitud y longitud**, es decir, los ángulos que definen su posición respecto al ecuador y al meridiano de Greenwich.

- La **latitud** se expresa en grados norte o sur (de −90° a +90°)
- La **longitud** se expresa en grados este u oeste (de −180° a +180°)

Estos sistemas son universales e intuitivos: cualquier GPS nos da coordenadas en WGS84 geográfico (EPSG:4326). Pero tienen un inconveniente: **las distancias y superficies no se pueden calcular directamente**. Un grado de longitud no equivale siempre al mismo número de kilómetros; en el ecuador son unos 111 km, pero a medida que nos acercamos a los polos esa distancia se reduce hasta cero.

![Diagrama detallado del sistema de coordenadas geográficas: latitud y longitud representados sobre un globo con ángulos etiquetados. Fuente: Djexplo (2011), “Latitude and Longitude of the Earth” (CC0, dominio público).]({{ site.baseurl }}/images/geographic-coordinates-systems.png){: .center width="800%"}

Si trabajamos con datos globales o compartimos información en servicios web, la opción más habitual es un **sistema geográfico** como WGS84 (EPSG:4326).

Así, los sistemas geográficos son ideales para almacenar y compartir datos globales, pero no para realizar cálculos precisos de distancia o superficie.

### Sistemas de coordenadas proyectados

Para poder trabajar con **unidades lineales** (metros, pies), transformamos la superficie curva de la Tierra a un **plano** mediante una proyección cartográfica. El resultado es un sistema de coordenadas proyectado.

Aquí las coordenadas ya no son ángulos, sino valores en metros sobre ejes X y Y. Esto permite medir distancias, calcular superficies o generar buffers con precisión. Pero, a cambio, la proyección sólo es válida dentro de un **ámbito concreto**: a medida que nos alejamos del centro o huso de proyección, las deformaciones aumentan.

Si queremos calcular áreas, distancias o hacer geoprocesos precisos, necesitamos un **sistema proyectado**, como las proyecciones UTM.

> **¡Atención!** QGIS puede reproyectar "al vuelo" las capas geográficas a proyectadas para visualizarlas juntas, pero para hacer **análisis espacial** es esencial que todos los datos estén en el mismo sistema proyectado.
{: .block-danger }

## El sistema UTM

Uno de los sistemas de coordenadas proyectados más utilizados en todo el mundo es el **UTM (Universal Transversa de Mercator)**. Su popularidad se debe a que ofrece coordenadas en metros, es conforme (preserva ángulos y formas locales) y cubre prácticamente todo el planeta de forma homogénea.

### ¿Cómo funciona?

La Tierra se divide en **60 husos de 6° de longitud cada uno**, numerados de oeste a este desde el meridiano de 180°. Cada huso se proyecta de forma independiente mediante una proyección **cilíndrica transversa de Mercator**: en vez de un cilindro alrededor del ecuador, se utiliza un cilindro “girando” que toca la Tierra en un **meridiano central**. Esto minimiza las deformaciones dentro de cada huso, pero limita el alcance: un sistema UTM solo es válido dentro de su huso.

![Mapa mundial con la división en 60 husos UTM. Fuente: [maptools.com.](https://maptools.com/tutorials/grid_zone_details)]({{ site.baseurl }}/images/utm-grid.png){: .center width="100%"}

### El caso de España y Catalunya

La Península Ibérica se reparte entre tres husos UTM:  

- **29N**: el oeste de Galicia, al oeste del meridiano 12° O  
- **30N**: el resto de Galicia, Castilla y León, Madrid, Extremadura, Andalucía y parte de Aragón  
- **31N**: Cataluña, Comunidad Valenciana, Baleares y Aragón oriental  

Las Islas Canarias se sitúan en los husos **27N** y **28N**.

En la práctica, en Cataluña trabajamos con **ETRS89 / UTM zona 31N (EPSG:25831)**. Si el proyecto abarca Castilla o Andalucía, se debe utilizar **ETRS89 / UTM zona 30N (EPSG:25830)**. Un criterio a seguir es usar el huso que cubre más superficie en nuestra zona de estudio.

![Mapa de los husos UTM en España (30N y 31N) y bandas latitudinales. Fuente: [maptools.com](https://maptools.com/tutorials/grid_zone_details).]({{ site.baseurl }}/images/utm-zone.png){: .center width="50%"}

> **¡Atención!** Si cargas en un mismo proyecto datos del huso 30N y del 31N, QGIS puede **reproyectar al vuelo**, pero para **análisis espacial** es imprescindible que todas las capas sean coherentes en un **único SRC** (mismo huso/zona y mismo datum).
{: .block-warning }

### Coordenadas geográficas vs UTM: ejemplo con Vila-seca

Para entender la diferencia entre coordenadas **geográficas** (lat/long, grados) y **UTM** (easting/northing, metros), veamos el municipio de **Vila-seca (Tarragonès)**:

- **Geográficas (ETRS89 / lat, lon)**  
  Latitud ≈ **41.110° N**  
  Longitud ≈ **1.144° E**

- **UTM (ETRS89 / UTM 31N, metros)**  
  **Easting ≈ 344 500 m**  
  **Northing ≈ 4 553 000 m**

Como se ve, el sistema geográfico expresa posiciones con **ángulos** (grados), mientras que UTM las da en **distancias lineales** (metros), muy útil para calcular **áreas y distancias** con precisión dentro del huso.

En QGIS podemos comprobar fácilmente si trabajamos en coordenadas geográficas o en coordenadas proyectadas fijándonos en la **barra de estado** (parte inferior derecha de la ventana). Cuando el proyecto está configurado en un sistema geográfico como **EPSG:4326 (WGS84)**, las coordenadas del puntero aparecen en grados de **latitud y longitud**. En cambio, si utilizamos un sistema proyectado como **EPSG:25831 (ETRS89 / UTM zona 31N)**, las coordenadas se muestran en **metros de easting y northing**. Esta diferencia visual permite identificar en qué sistema estamos trabajando y evitar confusiones en los cálculos.

![Comparación de la misma ubicación en QGIS con dos sistemas de coordenadas diferentes: arriba, geográficas (EPSG:4326) en grados de latitud/longitud; abajo, proyectadas UTM (EPSG:25831) en metros de easting y northing.]({{ site.baseurl }}/images/qgis-geographic-utm-coordinates.png){: .center width="100%"}

## Los códigos EPSG

Los códigos EPSG identifican de manera inequívoca cada sistema de referencia espacial. Provienen de la base de datos mantenida por el antiguo **European Petroleum Survey Group (EPSG)**, hoy dentro de la **International Association of Oil & Gas Producers (IOGP)**. Esta base de datos se creó para garantizar la coherencia y compatibilidad de los sistemas de coordenadas en contextos internacionales.

El **EPSG Geodetic Parameter Dataset** se ha convertido en el referente global y es utilizado por la mayoría de programas SIG. Se puede consultar libremente en: [https://epsg.io/](https://epsg.io/).

Cuando seleccionamos un SRC en QGIS (reproyección *al vuelo* en la barra de estado), suele aparecer una descripción textual que proviene de esta base. Por ejemplo, para **EPSG:25831 (ETRS89 / UTM zona 31N)**, QGIS muestra:

```bash
+proj=utm +zone=31 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs
```

Esta cadena describe la proyección, el huso, el elipsoide y los parámetros de transformación.

En la siguiente tabla encontrarás los códigos EPSG más utilizados según el área de estudio:

| **Código EPSG** | **Nombre**                              | **Tipo**     | **Uso recomendado** |
|-----------------|-----------------------------------------|--------------|---------------------|
| 4326            | WGS84 (geográficas)                     | Geográfico   | Datos globales, GPS, servicios web |
| 4258            | ETRS89 (geográficas)                    | Geográfico   | Estándar europeo |
| 3857            | Pseudo-Mercator (Web Mercator)          | Proyectado   | Mapas web (Google, OSM, Bing) |
| 25830           | ETRS89 / UTM huso 30N                   | Proyectado   | España occidental |
| 25831           | ETRS89 / UTM huso 31N                   | Proyectado   | Cataluña, Comunidad Valenciana, Baleares |
| 32631           | WGS84 / UTM huso 31N                    | Proyectado   | Usos internacionales (datum WGS84) |
| 23030           | ED50 / UTM huso 30N (obsoleto)          | Proyectado   | Cartografía histórica en España |
| 23031           | ED50 / UTM huso 31N (obsoleto)          | Proyectado   | Cartografía histórica en Cataluña |

El código más relevante para nuestro curso es el **EPSG:25831** → ETRS89 / UTM zona 31N. Puedes comprobar las diferentes distorsiones que se ven si elegimos entre dos sistemas de coordenadas de referencia. Por ejemplo, a escala global las diferencias entre elegir **25831** o **4326** son bastante evidentes.

![Comparación de proyecciones WGS84 (EPSG:4326) y ETRS89/UTM 31N (EPSG:25831)]({{ site.baseurl }}/images/wgs84-etrs89utm-comparison.png){: .center width="100%"}

También existen variantes en WGS84, como EPSG:32630 o EPSG:32631, habituales en datos GPS y servicios internacionales. Mención especial merece la proyección **Web Mercator** o **Pseudo-Mercator** (EPSG:3857), desarrollada por Google para sus mapas web y adoptada posteriormente por la mayoría de servicios similares (OpenStreetMap, Bing Maps, etc.). Esta proyección es una variante simplificada de la clásica proyección de Mercator que utiliza el elipsoide WGS84 pero lo trata como si fuera una esfera perfecta. Esto permite cálculos más rápidos y una implementación más sencilla en aplicaciones web, pero introduce pequeñas distorsiones adicionales, especialmente a latitudes altas. A pesar de sus limitaciones técnicas, la Web Mercator se ha convertido en el estándar de facto para la visualización de mapas en internet gracias a su rapidez de renderizado y compatibilidad universal.

## Práctica

1. **Verificar el SRC del proyecto.** En QGIS, abre `Propiedades del proyecto > SRC` y comprueba que está configurado en ETRS89 / UTM 31N (EPSG:25831)
2. **Comprobar el SRC de una capa.** Haz clic derecho → `Propiedades` → pestaña `Información`
3. **Reproyectar capas.** Exporta la capa con `Exportar > Guardar como...` y selecciona otro EPSG
4. **Visualizar los husos UTM.** Descarga y carga en QGIS un shapefile de husos UTM (CNIG). Identifica si tu zona cae en el 30N o 31N
5. **Comparar representaciones.** Carga una capa en EPSG:4326 y otra en EPSG:25831 y observa las diferencias
6. **Encontrar el SRC adecuado para otras regiones europeas.** Utiliza [epsg.io](https://epsg.io/) para determinar cuál sería el sistema de coordenadas más adecuado para:
   - Calcular áreas de parques urbanos en Roma (Italia)
   - Medir distancias entre ciudades en Francia
   - Analizar la red de transporte en Alemania
7. **Investigar sistemas nacionales.** Consulta la documentación oficial de los institutos geográficos nacionales y averigua:
   - ¿Qué sistema oficial utiliza Francia para la cartografía nacional?
   - ¿Qué sistemas recomendados utiliza el Institut Cartogràfic i Geològic de Catalunya (ICGC)?
   - ¿Cómo se denomina el sistema de coordenadas oficial de Italia?
8. **Ejercicio práctico internacional.** Descarga datos vectoriales de OpenStreetMap de dos ciudades europeas diferentes (por ejemplo, Lisboa y Varsovia). Identifica en qué SRC llegan los datos y determina a qué sistema deberías reproyectarlos para hacer cálculos precisos de área en cada caso.
9. **Análisis crítico.** Explica por qué no es recomendable utilizar WGS84 geográfico (EPSG:4326) para calcular el área de un bosque en Cataluña. ¿Qué diferencias esperas encontrar si comparas los resultados con ETRS89/UTM 31N?
