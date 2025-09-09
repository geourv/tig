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

Spatial datasets need to be placed within a coordinate system that allows them to be correctly interpreted on the surface of the Earth. This reference is provided by **Coordinate Reference Systems (CRS)**, which establish how geographical positions are represented in two dimensions.

In this chapter, we will use the term **Coordinate Reference System (CRS)**, the formal designation adopted by [ISO 19111](https://www.iso.org/standard/74039.html) and the [OGC](https://www.ogc.org/standard/ct/), and the terminology found in QGIS. In some manuals or programmes, especially in databases such as [PostGIS](https://postgis.net/docs/using_postgis_dbmanagement.html#spatial_ref_sys), you may also encounter **SRS (Spatial Reference System)**. Both refer to the same concept: the set of definitions (ellipsoid, datum, projection, and coordinate system) that allow us to correctly interpret coordinates in space. We will develop this concept further in this chapter.

We will now review concepts introduced in the previous course, expand on them, and connect them to practical usage in QGIS. Cartography faces a fundamental challenge: **representing the curved, irregular surface of the Earth on a flat plane**. The Earth is not a perfect sphere, but is slightly flattened at the poles and has irregularities due to the distribution of mass (mountains, oceans). For this reason, various mathematical models have been defined to describe and simplify this shape so that we have *useful* models of the Earth's surface.

## The geoid and the ellipsoid

### The geoid

The **geoid** is the surface that coincides with the mean sea level extended beneath the continents. It is a theoretical construction, but very real, because it describes how gravity acts on our planet. If we could see it represented, it would not be a sphere or a regular ellipsoid: it would have undulations of up to tens of metres due to the irregular distribution of mass within the Earth.

Where there are large mountain ranges, the weight of the rock increases the local gravitational field and the geoid rises. In contrast, in deep ocean basins or areas of less dense material, the geoid is depressed. Other factors also play a role, such as ocean circulation, water salinity and temperature, and long-term processes like isostatic uplift after a glaciation.

There is, therefore, **no single immutable geoid**, but different **geoid models** calculated at different times with specific data. The earliest models were based on classical gravimetric and levelling measurements, while today satellite missions like **[GRACE](https://grace.jpl.nasa.gov/)** or **GOCE** have mapped the global geoid with centimetre precision. Many countries also maintain national models for more accurate conversion of heights.

![Schematic representation of the geoid as an irregular equipotential surface. Terrestrial geoid: irregular surface representing mean sea level. Source: nosmienten.com via Wikimedia Commons, File:Geoide.jpg (CC BY-SA 4.0).]({{ site.baseurl }}/images/geoid.png){: .center width="100%"}

### The ellipsoid

If the geoid reflects the physical reality of the Earth, the **ellipsoid of revolution** is its mathematical simplification. It is a regular body, slightly flattened at the poles, serving as a useful approximation for calculations and representations. Thanks to its simplicity, coordinate equations are workable and allow reference systems to be established at global or regional scale.

Over time, several ellipsoids have been defined, each tailored to different parts of the world. For example, **Clarke 1866** was widely used in North America, while **GRS80** and **WGS84** are the most common today. WGS84 is the reference ellipsoid for the GPS system and is therefore universally recognised.

![Comparison of two regional ellipsoids (NAD27 and ED50) with respect to the Earth's centre of mass {% cite JanvanSickle15 %}.]({{ site.baseurl }}/images/two-regional-ellipsoids.png){: .center width="80%"}

The relationship between the geoid and the ellipsoid is key: the geoid is the physical model that tells us how the Earth truly is, with all its irregularities, while the ellipsoid is the mathematical model that simplifies this complexity and allows us to make calculations and maps. In geodesy and cartography, we always work by combining them: a **datum** is, precisely, the way to fit an ellipsoid to a geoid and anchor it to a territory.

Global studies use WGS84, but in Europe the recommended system is **ETRS89/GRS80**, because it is fixed to the Eurasian Plate and avoids the displacement caused by tectonics when only using WGS84.

## Heights: orthometric vs. ellipsoidal

A point on the Earth's surface can be described by horizontal coordinates (latitude and longitude) and also by a **height**. It is important to distinguish between two types of height:

- **Orthometric height**: This is the height measured from the geoid, i.e., mean sea level. It is used in official cartography, engineering, and hydrological studies because it corresponds to the physical reality of the terrain.
- **Ellipsoidal height**: This is the height measured from an ellipsoid (e.g., WGS84). It is returned by a GPS receiver, as the calculation is carried out directly on the mathematical model.

The difference between the two, called **geoid undulation (N)**, can easily reach 40 or 50 metres depending on the region. Therefore, when using GPS for engineering work, it is always necessary to apply a geoid model to convert ellipsoidal heights to orthometric heights.

This has significant practical importance. For example, the heights provided by GPS are **ellipsoidal** (relative to WGS84), while the official heights in cartography and engineering are **orthometric**, i.e., relative to the geoid. Without applying the correct correction, the difference may be several metres. For surveying and engineering work it is essential to use a local geoid model to convert GPS heights into usable orthometric heights.

![Comparison between the geoid and the WGS84 ellipsoid, with geoidal undulations and orthometric height formulas. Source: geologician, “Earth's Geoid compared with WGS84 ellipsoid”, Wikimedia Commons (cc by-sa 4.0)]({{ site.baseurl }}/images/geoid-vs-ellipsoid.png)

In QGIS and other programmes, these conversions can be configured with official transformations if the appropriate geoid model is available (e.g., EGM2008 or the Spanish geoid calculated by IGN).

## Datums

The **datum** is the element that connects the theoretical world (geoid and ellipsoid) to cartographic reality. Simply put, a datum is a way of **anchoring an ellipsoid to the real Earth**, defining its position, orientation, and the control points that provide stability.

A datum establishes:

- which ellipsoid is used (GRS80, WGS84, Clarke, etc.)
- where the centre of this ellipsoid is placed with respect to the Earth's centre of mass
- how it relates to physical points measured on the territory (geodetic networks)

That is why we say the datum is the **practical translation** of theory into the cartographic reality of a country or continent.

### Local and global datums

Historically, each region used its own local datum, tailored to the precision requirements of a specific territory. For example:

- **ED50** (European Datum 1950), widely used in Europe until the late 20th century
- **NAD27** in North America

With the advent of satellite navigation and the globalisation of data, the need for global datums became clear:

- **WGS84**, defined for the GPS system, is the most universal today
- **ETRS89** (European Terrestrial Reference System 1989) is the European version, fixed to the Eurasian Plate to avoid tectonic shifts relative to WGS84

Although WGS84 and ETRS89 were virtually identical in 1989, over time the Eurasian Plate has shifted. Today, differences exceed 80 cm and will continue to grow. Therefore, for official work in Europe, ETRS89 must always be used.

### Examples in QGIS

When we open the properties of a layer in QGIS and see a CRS such as **EPSG:25831**, we are actually referring to a **datum (ETRS89)**, an **ellipsoid (GRS80)**, and a **projection (UTM 31N)** combined in a single code.

![Example of a CRS definition in QGIS showing the datum, ellipsoid and projection]({{ site.baseurl }}/images/crs-selection-in-qgis.png){: .center width="100%"}

This information comes from the **EPSG Geodetic Parameter Dataset**, maintained by the [International Association of Oil & Gas Producers (IOGP)](https://epsg.org/), the global standard.

> **Why are datums so important?** Choosing the correct datum avoids shifts of tens or hundreds of metres between layers. A historic file in ED50 overlaid on one in ETRS89 will show a visible mismatch, even though the data are correct individually. Being able to identify and, if needed, **reproject** layers between datums is a fundamental GIS skill. For example, when working with Spanish data from before 2000, you must check if they are in ED50. Many older maps and shapefiles still use this datum and need to be reprojected to ETRS89.
{: .block-warning }

## Map projections

Once we have defined reference surfaces (geoid and ellipsoid) and the datums that fix them, we still need to take a fundamental step: **how to represent the Earth on a flat map**. No projection is neutral: there will always be distortions, whether in distances, areas, or angles. The art of cartography consists in **choosing the projection that best suits the map's purpose**.

### Projection surfaces

The classical way to explain this is to imagine projecting the Earth onto a simple geometric surface, which we can then unfold:

- **Cylinder** → cylindrical projections (e.g., Mercator)
- **Cone** → conical projections (e.g., Lambert Conformal Conic)
- **Disc or plane** → azimuthal projections (e.g., Stereographic, Azimuthal Equidistant)

![Projection surfaces: plane (azimuthal), cylinder (cylindrical) and cone (conic) conceptually applied to the ellipsoid. Source: Charles Preppernau (2022), “The three developable projection surfaces: cylinder, cone and plane”, CC BY 4.0. ]({{ site.baseurl }}/images/projection-surfaces.png){: .center width="70%"}

Each surface can touch the ellipsoid on one line (tangent projection) or two (secant). Where there is contact, distortion is minimal; as we move away, it increases.

### Main types of projections

- **Conformal**: preserves angles and local shapes, ideal for topographic mapping and navigation. Example: Mercator
- **Equal-area**: preserves areas, useful for thematic maps (e.g., population, land use). Example: Albers
- **Equidistant**: preserves distances only in certain directions. Example: Azimuthal Equidistant
- **Compromise**: seeks a balance between distortions. Example: Robinson or Winkel-Tripel, often used for world maps

![Comparison of projections: Mercator (conformal) and Albers (equal-area). Source: Tobias Jung, map-projections.net (CC BY-SA 4.0).]({{ site.baseurl }}/images/map-projections-comparison-mercator-albers.png){: .center width="100%"}

The Tissot indicatrix is a classic method for visualising the distortions introduced by map projections. It consists of drawing equal circles on the Earth's surface and observing how they are distorted when projected onto the map. If the projection preserves local shapes (conformal projection), the circles remain circles but may vary in size; if it preserves areas (equal-area projection), the circles may become ellipses but retain the same surface area; and in compromise projections, both shape and size distortions occur. In the image, the Behrmann equal-area cylindrical projection shows how circles become increasingly flattened ellipses as we move away from the equator, making scale and distortion variation by latitude evident.

![Tissot indicatrix on Behrmann equal-area cylindrical projection, showing how distances and areas are distorted with latitude — used here as an analogy for the WGS84 geographic coordinate system without direct projection (Plate Carrée), where distortions are similar in trend.]({{ site.baseurl }}/images/tissot-behrmann.png){: .center width="80%"}

> **Tip**: There is no perfect projection. The key is to ask: what do we want to preserve? If we need to calculate areas, we choose an equal-area projection; if we are interested in navigation or local geometry, a conformal one.
{: .block-tip }

## Coordinate systems: geographic and projected

To represent a point on the Earth, we need two things: a **reference system** and a **coordinate system** to describe its location. The most common are **geographic** and **projected**, each with advantages and limitations.

### Geographic coordinate systems

In a geographic system, a point is expressed by **latitude and longitude**, i.e., the angles that define its position relative to the equator and the Greenwich meridian.

- **Latitude** is expressed in degrees north or south (from −90° to +90°)
- **Longitude** is expressed in degrees east or west (from −180° to +180°)

These systems are universal and intuitive: any GPS provides coordinates in geographic WGS84 (EPSG:4326). However, they have a drawback: **distances and areas cannot be directly calculated**. One degree of longitude does not always equal the same number of kilometres; at the equator it is about 111 km, but as we approach the poles this distance decreases to zero.

![Detailed diagram of the geographic coordinate system: latitude and longitude represented on a globe with labelled angles. Source: Djexplo (2011), “Latitude and Longitude of the Earth” (CC0, public domain).]({{ site.baseurl }}/images/geographic-coordinates-systems.png){: .center width="800%"}

If we work with global data or share information in web services, the most usual choice is a **geographic system** such as WGS84 (EPSG:4326).

Thus, geographic systems are ideal for storing and sharing global data, but not for making precise calculations of distance or area.

### Projected coordinate systems

To work with **linear units** (metres, feet), we transform the curved surface of the Earth onto a **plane** using a map projection. The result is a projected coordinate system.

Here, coordinates are no longer angles, but values in metres on X and Y axes. This allows us to measure distances, calculate areas, or generate buffers precisely. However, the projection is only valid within a **specific area**: as we move away from the centre or zone of projection, distortions increase.

If we want to calculate areas, distances, or perform precise geoprocessing, we need a **projected system**, such as UTM projections.

> **Attention!** QGIS can reproject geographic layers "on the fly" into projected ones for visualisation, but for **spatial analysis** it is essential that all data are in the same projected system.
{: .block-danger }

## The UTM system

One of the most widely used projected coordinate systems worldwide is **UTM (Universal Transverse Mercator)**. Its popularity stems from the fact that it provides coordinates in metres, is conformal (preserves angles and local shapes), and covers almost the entire planet in a homogeneous manner.

### How does it work?

The Earth is divided into **60 zones, each 6° of longitude wide**, numbered west to east from the 180° meridian. Each zone is projected independently using a **transverse Mercator cylindrical projection**: instead of a cylinder around the equator, a “rotating” cylinder touches the Earth at a **central meridian**. This minimises distortions within each zone, but limits the extent: a UTM system is only valid within its zone.

![World map with division into 60 UTM zones. Source: [maptools.com.](https://maptools.com/tutorials/grid_zone_details)]({{ site.baseurl }}/images/utm-grid.png){: .center width="100%"}

### The case of Spain and Catalonia

The Iberian Peninsula is divided between three UTM zones:  

- **29N**: western Galicia, west of the 12° W meridian  
- **30N**: the rest of Galicia, Castile and León, Madrid, Extremadura, Andalusia, and part of Aragón  
- **31N**: Catalonia, Valencian Community, Balearic Islands, eastern Aragón  

The Canary Islands are in zones **27N** and **28N**.

In practice, in Catalonia we work with **ETRS89 / UTM zone 31N (EPSG:25831)**. If the project covers Castile or Andalusia, use **ETRS89 / UTM zone 30N (EPSG:25830)**. A good rule of thumb is to use the zone that covers the largest area of your study region.

![Map of UTM zones in Spain (30N and 31N) and latitude bands. Source: [maptools.com](https://maptools.com/tutorials/grid_zone_details).]({{ site.baseurl }}/images/utm-zone.png){: .center width="50%"}

> **Attention!** If you load data from both zone 30N and 31N in the same project, QGIS can **reproject on the fly**, but for **spatial analysis** all layers must be consistent in a **single CRS** (same zone and datum).
{: .block-warning }

### Geographic coordinates vs UTM: example with Vila-seca

To understand the difference between **geographic** coordinates (lat/long, degrees) and **UTM** (easting/northing, metres), let’s look at the municipality of **Vila-seca (Tarragonès)**:

- **Geographic (ETRS89 / lat, lon)**  
  Latitude ≈ **41.110° N**  
  Longitude ≈ **1.144° E**

- **UTM (ETRS89 / UTM 31N, metres)**  
  **Easting ≈ 344,500 m**  
  **Northing ≈ 4,553,000 m**

As seen, the geographic system gives positions in **angles** (degrees), while UTM provides **linear distances** (metres), which is very useful for calculating **areas and distances** accurately within the zone.

In QGIS, you can easily check whether you are working in geographic or projected coordinates by looking at the **status bar** (lower right of the window). When the project is set to a geographic system such as **EPSG:4326 (WGS84)**, pointer coordinates appear in degrees of **latitude and longitude**. If using a projected system such as **EPSG:25831 (ETRS89 / UTM zone 31N)**, coordinates are shown in **metres of easting and northing**. This visual difference allows you to immediately identify the system in use and avoid confusion in calculations.

![Comparison of the same location in QGIS with two different coordinate systems: above, geographic (EPSG:4326) in degrees of latitude/longitude; below, UTM projected (EPSG:25831) in metres of easting and northing.]({{ site.baseurl }}/images/qgis-geographic-utm-coordinates.png){: .center width="100%"}

## EPSG codes

EPSG codes uniquely identify each spatial reference system. They come from the database maintained by the former **European Petroleum Survey Group (EPSG)**, now part of the **International Association of Oil & Gas Producers (IOGP)**. This database was created to ensure consistency and compatibility of coordinate systems in international contexts.

The **EPSG Geodetic Parameter Dataset** has become the global standard and is used by most GIS programmes. You can consult it freely at: [https://epsg.io/](https://epsg.io/).

When selecting a CRS in QGIS (on-the-fly reprojection in the status bar), you will often see a textual description from this database. For example, for **EPSG:25831 (ETRS89 / UTM zone 31N)**, QGIS shows:

```bash
+proj=utm +zone=31 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs
```

This string describes the projection, zone, ellipsoid, and transformation parameters.

The table below lists the most used EPSG codes for different areas of study:

| **EPSG Code** | **Name**                               | **Type**      | **Recommended use** |
|---------------|----------------------------------------|---------------|---------------------|
| 4326          | WGS84 (geographic)                     | Geographic    | Global data, GPS, web services |
| 4258          | ETRS89 (geographic)                    | Geographic    | European standard |
| 3857          | Pseudo-Mercator (Web Mercator)         | Projected     | Web maps (Google, OSM, Bing) |
| 25830         | ETRS89 / UTM zone 30N                  | Projected     | Western Spain |
| 25831         | ETRS89 / UTM zone 31N                  | Projected     | Catalonia, Valencian Community, Balearic Islands |
| 32631         | WGS84 / UTM zone 31N                   | Projected     | International uses (WGS84 datum) |
| 23030         | ED50 / UTM zone 30N (obsolete)         | Projected     | Historic mapping in Spain |
| 23031         | ED50 / UTM zone 31N (obsolete)         | Projected     | Historic mapping in Catalonia |

The most relevant code for our course is **EPSG:25831** → ETRS89 / UTM zone 31N. You can check the different distortions that occur when switching between two coordinate reference systems. For example, at global scale the differences between choosing **25831** or **4326** are quite evident.

![Comparison of projections WGS84 (EPSG:4326) and ETRS89/UTM 31N (EPSG:25831)]({{ site.baseurl }}/images/wgs84-etrs89utm-comparison.png){: .center width="100%"}

There are also WGS84 variants, such as EPSG:32630 or EPSG:32631, common in GPS data and international services. Special mention must be made of the **Web Mercator** or **Pseudo-Mercator** projection (EPSG:3857), developed by Google for its web maps and later adopted by most similar services (OpenStreetMap, Bing Maps, etc.). This projection is a simplified variant of the classic Mercator projection that uses the WGS84 ellipsoid but treats it as a perfect sphere. This allows faster calculations and simpler implementation in web applications but introduces small additional distortions, especially at high latitudes. Despite its technical limitations, Web Mercator has become the de facto standard for online map visualisation thanks to its rendering speed and universal compatibility.

## Practice

1. **Check the project's CRS.** In QGIS, open `Project Properties > CRS` and confirm it is set to ETRS89 / UTM 31N (EPSG:25831)
2. **Check a layer's CRS.** Right-click → `Properties` → `Information` tab
3. **Reproject layers.** Export the layer with `Export > Save As...` and select another EPSG
4. **Visualise UTM zones.** Download and load a UTM zone shapefile (CNIG) in QGIS. Identify if your area falls in 30N or 31N
5. **Compare representations.** Load a layer in EPSG:4326 and another in EPSG:25831 and observe the differences
6. **Find the appropriate CRS for other European regions.** Use [epsg.io](https://epsg.io/) to determine the most suitable coordinate system for:
   - Calculating park areas in Rome (Italy)
   - Measuring distances between cities in France
   - Analysing the transport network in Germany
7. **Investigate national systems.** Consult the official documentation of national geographic institutes and find out:
   - What official system does France use for national mapping?
   - What systems are recommended by the Institut Cartogràfic i Geològic de Catalunya (ICGC)?
   - What is the official coordinate system of Italy called?
8. **International practical exercise.** Download vector data from OpenStreetMap for two different European cities (e.g., Lisbon and Warsaw). Identify the CRS in which the data arrives and determine to which system you should reproject them to make precise area calculations in each case.
9. **Critical analysis.** Explain why it is not advisable to use geographic WGS84 (EPSG:4326) to calculate the area of a forest in Catalonia. What differences would you expect if you compare results with ETRS89/UTM 31N?
