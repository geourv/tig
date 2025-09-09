---
lang: en
permalink: /:title/en/
title: "Coordinate Reference Systems (CRS)"
author: Benito Zaragozí
date: 2025-09-07
weight: 3
layout: chapter
mermaid: true
published: true
---

Spatial datasets need to be situated in a coordinate system that enables correct interpretation on the Earth’s surface. This reference is provided by **Spatial Reference Systems** or **Coordinate Reference Systems (CRS)**, which establish how geographical positions are represented in two dimensions.

In this chapter, we shall use the term **Cpatial Reference System (CRS)**, the formal designation adopted by [ISO 19111](https://www.iso.org/standard/74039.html) and the [OGC](https://www.ogc.org/standard/ct/), and also the one appearing in QGIS. Some manuals or programmes, especially databases such as [PostGIS](https://postgis.net/docs/using_postgis_dbmanagement.html#spatial_ref_sys), use the term **SRS (Spatial Reference System)**. Both refer to the same concept: the set of definitions (ellipsoid, datum, projection and coordinate system) that allow coordinates in space to be interpreted correctly. We will explore this concept further in this chapter.

We will revisit concepts already introduced in the previous course, expand on them, and connect them with practical applications in QGIS. Cartography must tackle a fundamental challenge: **representing the curved and irregular surface of the Earth on a plane**. The Earth is not a perfect sphere, but a body slightly flattened at the poles and with irregularities caused by the distribution of mass (mountains, oceans). For this reason, various mathematical models have been defined to describe and simplify this shape, allowing us to create *useful* models of the Earth's surface.

## The Geoid and the Spheroid

### The Geoid

The **geoid** is the surface that coincides with the mean sea level extended beneath the continents. It is a theoretical yet very real construction, as it describes how gravity acts on our planet. If we could see it depicted, it would not be a sphere or a regular ellipsoid: it would have undulations of up to tens of metres, owing to the irregular distribution of mass within the Earth.

Where there are large mountain ranges, the weight of the rock increases the local gravitational field and the geoid rises. Conversely, in deep ocean basins or areas of less dense materials, the geoid is depressed. Factors such as ocean circulation, water salinity and temperature, or long-term processes like isostatic uplift after a glaciation also influence it.

Thus, there is **no single immutable geoid**, but rather different **geoid models** computed at each historical moment with specific data. Early models were based on classic gravimetric and levelling measurements, while today satellite missions such as **[GRACE](https://grace.jpl.nasa.gov/)** or **GOCE** have enabled global mapping of the geoid with centimetre-level precision. Additionally, many countries maintain national models to better refine height conversions.

Its practical importance is enormous: GPS heights are **ellipsoidal** (relative to WGS84), while official heights in cartography and engineering are **orthometric**, i.e., relative to the geoid. Without applying the correct adjustment, the difference may be several metres. For surveying and engineering work, it is essential to use a local geoid model to convert GPS heights into useful orthometric heights.

![Diagram of the geoid and its undulations relative to the ellipsoid]({{ site.baseurl }}/images/placeholder.png){: .center width="80%"}

### The Spheroid or Ellipsoid

If the geoid reflects the physical reality of the Earth, the **spheroid or ellipsoid of revolution** is its mathematical simplification. It is a regular body, slightly flattened at the poles, serving as a practical approximation for calculations and representations. Thanks to its simplicity, coordinate equations are feasible and allow reference systems to be established at a global or regional scale.

Over time, various ellipsoids have been defined, each adjusted to different parts of the world. For example, **Clarke 1866** was widely used in North America, while **GRS80** and **WGS84** are the most common today. WGS84 is the reference ellipsoid for the GPS system and is thus universally recognised.

![Representation of the spheroid or ellipsoid of revolution as a mathematical approximation to the geoid]({{ site.baseurl }}/images/placeholder.png){: .center width="70%"}

The relationship between geoid and ellipsoid is key: the geoid is the physical model that tells us what the Earth is really like, with all its irregularities, while the ellipsoid is the mathematical model that simplifies that complexity and enables calculations and mapping. In geodesy and cartography, we always work by combining them: a **datum** is precisely the way to adjust an ellipsoid to a geoid and anchor it to a territory.

Global studies use WGS84, but in Europe the recommended standard is **ETRS89/GRS80**, as it is fixed to the Eurasian plate and avoids the tectonic shifts that occur if only WGS84 is used.

## Heights: Orthometric vs. Ellipsoidal

A point on the Earth's surface can be described with horizontal coordinates (latitude and longitude) and also with a **height**. It is important to clearly distinguish between two types of height:

- **Orthometric height**: The height measured relative to the geoid, i.e., the mean sea level. This is used in official cartography, engineering and hydrological studies, as it corresponds to the physical reality of the terrain.
- **Ellipsoidal height**: The height measured relative to an ellipsoid (e.g., WGS84). This is what a GPS receiver returns, as calculations are made directly on the mathematical model.

The difference between the two, called **geoid undulation (N)**, can easily reach 40 or 50 metres depending on the region. Therefore, when using GPS in engineering work, it is always necessary to apply a geoid model to convert ellipsoidal heights into orthometric heights.

![Diagram of heights: ellipsoidal (h), orthometric (H) and geoid undulation (N)]({{ site.baseurl }}/images/placeholder.png){: .center width="70%"}

In QGIS and other programmes, these conversions can be set up using official transformations if the appropriate geoid model is available (for example, EGM2008 or the Spanish geoid calculated by the IGN).

## Datums

A **datum** is the element that connects the theoretical world (geoid and ellipsoid) with cartographic reality. Put simply, a datum is the way to **anchor an ellipsoid to the real Earth**, defining its position, orientation and control points that provide stability.

A datum establishes:

- which ellipsoid is used (GRS80, WGS84, Clarke, etc.)
- where the centre of this ellipsoid is located relative to the Earth's centre of mass
- how it relates to physical points measured on the ground (geodetic networks)

For this reason, we say that the datum is the **practical translation** from theory to the cartographic reality of a country or continent.

### Local and Global Datums

Historically, each region used its own local datum, adjusted to the precision needs of a specific territory. For example:

- **ED50** (European Datum 1950), widely used in Europe until the end of the twentieth century
- **NAD27** in North America

With the advent of satellite navigation and the globalisation of data, the need for global datums arose:

- **WGS84**, defined for the GPS system, is now the most universal
- **ETRS89** (European Terrestrial Reference System 1989) is the European version, fixed to the Eurasian plate to avoid tectonic movements with respect to WGS84

Although WGS84 and ETRS89 were practically coincident in 1989, over time the Eurasian plate has moved. Thus, today there are differences of more than 80 cm that will continue to grow. For this reason, official work in Europe should always use ETRS89.

### Examples in QGIS

When we open the properties of a layer in QGIS and see a CRS such as **EPSG:25831**, we are actually dealing with a **datum (ETRS89)**, an **ellipsoid (GRS80)** and a **projection (UTM 31N)**, all combined in a single code.

![Example of a CRS definition in QGIS showing datum, ellipsoid and projection]({{ site.baseurl }}/images/placeholder.png){: .center width="80%"}

This information comes from the **EPSG Geodetic Parameter Dataset**, maintained by the [International Association of Oil & Gas Producers (IOGP)](https://epsg.org/), which is the global standard.

### Why are datums so important?

The correct choice of datum avoids shifts of tens or hundreds of metres between layers. A historical file in ED50 overlaid on one in ETRS89 will show a visible mismatch, even though the data are correct separately. Knowing how to identify and, if necessary, **reproject** layers between datums is a fundamental skill in GIS. For example, if working with Spanish data prior to 2000, you must check if they are in ED50. Many older maps and shapefiles still use this datum and need to be reprojected to ETRS89.

## Map Projections

Once the reference surfaces (geoid and ellipsoid) and the datums anchoring them are defined, a further fundamental step remains: **how to represent the Earth on a flat map**. No projection is neutral: there will always be distortions, be it in distances, areas or angles. The art of cartography is to **choose the projection that best suits the purpose of the map**.

### Projection Surfaces

The classic way to explain this is to imagine projecting the Earth onto a simple geometric surface, which we can then unfold:

- **Cylinder** → cylindrical projections (e.g., Mercator)
- **Cone** → conic projections (e.g., Lambert Conformal Conic)
- **Disc or plane** → azimuthal projections (e.g., Stereographic, Azimuthal Equidistant)

![Projection surfaces: cylinder, cone and plane applied to the ellipsoid]({{ site.baseurl }}/images/placeholder.png){: .center width="80%"}

Each surface may touch the ellipsoid along one line (tangent projection) or two (secant). Where there is contact, distortion is minimal; as we move away, it increases.

### Main Types of Projection

- **Conformal**: preserves angles and local shapes, ideal for topographic mapping and navigation. Example: Mercator
- **Equal-area**: preserves areas, useful for thematic maps (e.g., population, land use). Example: Albers
- **Equidistant**: preserves distances only in certain directions. Example: Azimuthal Equidistant
- **Compromise**: seeks a balance between distortions. Example: Robinson or Winkel-Tripel, often used in world maps

![Comparison of projections: Mercator (conformal), Albers (equal-area) and Robinson (compromise)]({{ site.baseurl }}/images/placeholder.png){: .center width="100%"}

> **Tip**: There is no perfect projection. The key is to ask yourself: what do I want to preserve? If you need to calculate areas, choose an equal-area projection; if navigation or local geometry matters, use a conformal one.
{: .block-tip }

## Coordinate Systems: Geographic and Projected

To represent a point on the Earth, we need two things: a **reference system** and a **coordinate system** to describe its position. The most common are **geographic** and **projected** systems, each with their advantages and limitations.

### Geographic Coordinate Systems

In a geographic system, a point is expressed by **latitude and longitude**, i.e., the angles defining its position relative to the equator and Greenwich meridian.

- **Latitude** is expressed in degrees north or south (from −90° to +90°)
- **Longitude** is expressed in degrees east or west (from −180° to +180°)

These systems are universal and intuitive: any GPS provides coordinates in geographic WGS84 (EPSG:4326). However, they have a drawback: **distances and areas cannot be calculated directly**. One degree of longitude does not always equal the same number of kilometres; at the equator it is about 111 km, but as you approach the poles this distance reduces to zero.

![Map in geographic WGS84 where distances and areas are distorted]({{ site.baseurl }}/images/placeholder.png){: .center width="80%"}

For global datasets or sharing information in web services, a **geographic system** such as WGS84 (EPSG:4326) is most commonly used.

Thus, geographic systems are ideal for storing and sharing global data, but not for precise distance or area calculations.

### Projected Coordinate Systems

To work with **linear units** (metres, feet), we transform the Earth's curved surface onto a **plane** using a map projection. The result is a projected coordinate system.

Here, coordinates are no longer angles, but values in metres along X and Y axes. This lets us measure distances, calculate areas or generate buffers accurately. However, the projection is only valid within a **specific area**: distortion increases as we move away from the centre or zone of projection.

![Map projected in UTM (ETRS89/UTM 31N) where coordinates are in metres]({{ site.baseurl }}/images/placeholder.png){: .center width="80%"}

If you want to calculate areas, distances or perform accurate geoprocessing, you need a **projected system**, such as UTM projections.

> **Warning!** QGIS can reproject geographic layers “on the fly” to projected ones for display, but for **spatial analysis** it is essential that all data be in the same projected system.
{: .block-danger }

## The UTM System

One of the most widely used projected coordinate systems worldwide is **UTM (Universal Transverse Mercator)**. Its popularity is due to the fact that it offers coordinates in metres, is conformal (preserves angles and local shapes), and covers almost the entire planet uniformly.

### How does it work?

The Earth is divided into **60 zones of 6° longitude each**, numbered west to east from the 180th meridian. Each zone is projected independently using a **Transverse Mercator cylindrical projection**: instead of a cylinder around the equator, a “rotating” cylinder touches the Earth at a central meridian.

This technique minimises distortion within each zone, but limits the extent: a UTM system is only valid within the zone for which it has been defined.

![World map with division into 60 UTM zones]({{ site.baseurl }}/images/placeholder.png){: .center width="80%"}

### The case of Spain and Catalonia

The Iberian Peninsula is split between two UTM zones:

- **30N**: Galicia, Castile, Andalusia and part of Extremadura
- **31N**: Catalonia, Valencian Community, Balearic Islands and eastern Aragon

The Canary Islands are within zones 27N and 28N.

In practice, in Catalonia we use **ETRS89 / UTM zone 31N (EPSG:25831)**. If the project covers Castile or Andalusia, **ETRS89 / UTM zone 30N (EPSG:25830)** should be used.

![Map of UTM zones in Spain: 30N and 31N]({{ site.baseurl }}/images/placeholder.png){: .center width="80%"}

> **Warning!** If you load data from both zones 30N and 31N in the same project, QGIS can reproject them *on the fly*, but for spatial analysis all layers must be consistent in a single CRS.
{: .block-warning }

## EPSG Codes

EPSG codes uniquely identify each spatial reference system. They come from the database maintained by the former **European Petroleum Survey Group (EPSG)**, now part of the **International Association of Oil & Gas Producers (IOGP)**. This database was created to ensure consistency and compatibility of coordinate systems in international contexts.

The **EPSG Geodetic Parameter Dataset** has become the global reference and is used by most GIS programmes. It is freely available at: [https://epsg.io/](https://epsg.io/).

When selecting a CRS in QGIS, a textual description usually appears from this database. For example, for **EPSG:25831 (ETRS89 / UTM zone 31N)**, QGIS displays:

```bash
+proj=utm +zone=31 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs
```

This string describes the projection, zone, ellipsoid and transformation parameters.

### Most Common EPSG Codes

The following table lists the most widely used EPSG codes according to study area:

| **EPSG Code** | **Name**                                 | **Type**      | **Recommended Use** |
|---------------|------------------------------------------|---------------|--------------------|
| 4326          | WGS84 (geographic)                       | Geographic    | Global data, GPS, web services |
| 4258          | ETRS89 (geographic)                      | Geographic    | European standard   |
| 3857          | Pseudo-Mercator (Web Mercator)           | Projected     | Web maps (Google, OSM, Bing) |
| 25830         | ETRS89 / UTM zone 30N                    | Projected     | Western Spain       |
| 25831         | ETRS89 / UTM zone 31N                    | Projected     | Catalonia, Valencian Community, Balearic Islands |
| 32631         | WGS84 / UTM zone 31N                     | Projected     | International uses (WGS84 datum) |
| 23030         | ED50 / UTM zone 30N (obsolete)           | Projected     | Historical cartography in Spain |
| 23031         | ED50 / UTM zone 31N (obsolete)           | Projected     | Historical cartography in Catalonia |

The most relevant codes for our course are:

- **EPSG:25830** → ETRS89 / UTM zone 30N
- **EPSG:25831** → ETRS89 / UTM zone 31N

There are also WGS84 variants, such as EPSG:32630 or EPSG:32631, commonly found in GPS data and international services.

![Comparison of WGS84 (EPSG:4326) and ETRS89/UTM 31N (EPSG:25831) projections]({{ site.baseurl }}/images/placeholder.png){: .center width="100%"}

A special mention deserves the **Web Mercator** or **Pseudo-Mercator** projection (EPSG:3857), developed by Google for its web maps and subsequently adopted by most similar services (OpenStreetMap, Bing Maps, etc.).

This projection is a simplified variant of the classic Mercator projection that uses the WGS84 ellipsoid but treats it as if it were a perfect sphere. This allows for faster calculations and simpler implementation in web applications, but introduces additional minor distortions, especially at high latitudes.

Despite its technical limitations, Web Mercator has become the de facto standard for online map visualisation, thanks to its rendering speed and universal compatibility.

## Practical Exercises

1. **Check the CRS of the project.** In QGIS, open `Project Properties > CRS` and check it is set to ETRS89 / UTM 31N (EPSG:25831)
2. **Check the CRS of a layer.** Right-click → `Properties` → `Information` tab
3. **Reproject layers.** Export the layer using `Export > Save As...` and select another EPSG
4. **Visualise UTM zones.** Download and load a UTM zone shapefile (CNIG) in QGIS. Identify if your area falls in 30N or 31N
5. **Compare representations.** Load a layer in EPSG:4326 and another in EPSG:25831 and observe the differences
6. **Find the suitable CRS for other European regions.** Use [epsg.io](https://epsg.io/) to determine which coordinate system is most appropriate for:
   - Calculating areas of urban parks in Rome (Italy)
   - Measuring distances between cities in France
   - Analysing the transport network in Germany
7. **Investigate national systems.** Consult the official documentation of national geographic institutes and discover:
   - What is the official system used by France for national cartography?
   - Which recommended systems does the Institut Cartogràfic i Geològic de Catalunya (ICGC) use?
   - What is the name of Italy’s official coordinate system?
8. **International practical exercise.** Download vector data from OpenStreetMap for two different European cities (for example, Lisbon and Warsaw). Identify the CRS in which the data arrives and determine which system you should reproject to for accurate area calculations in each case.
9. **Critical analysis.** Explain why it is not advisable to use geographic WGS84 (EPSG:4326) to calculate the area of a forest in Catalonia. What differences would you expect if you compare results with ETRS89/UTM 31N?
