---
lang: en
permalink: /:title/en/
title: Course presentation
author: Benito Zaragozí
date: 2025-09-02
weight: 0
layout: chapter
mermaid: false
---

This manual is part of the subject **Geographic Information Technologies (GIT)**, taught in the [Bachelor’s Degree in Geography, Territorial Analysis and Sustainability](https://www.urv.cat/en/studies/bachelors-offered/geography-territorial-analysis-sustainability/) at the Faculty of Tourism and Geography of the URV.

This section provides the main information and practical details for following the course.

| **Course code**          | 21234114 |
| **Credits**              | 4 ECTS |
| **Type**                 | Compulsory |
| **Cycle**                | 1st |
| **Term**                 | 1Q |
| **Course coordinator**   | Benito Zaragozí ([benito.zaragozi@urv.cat](mailto:benito.zaragozi@urv.cat)) |
| **Department**           | Geography |
| **Official course guide**| [See here](https://guiadocent.urv.cat/docnet/guia_docent/index.php?centre=21&ensenyament=2123&assignatura=21234114&any_academic=2025_26&any_academic=2025_26) |

Information management, digital submissions, and communication will take place through the [Moodle URV](https://moodle.urv.cat/) platform.

The main objective of the course is to introduce GIT and provide students with basic competences for their professional use. Specifically, it aims to:

- Provide theoretical and practical knowledge on GIS and other relevant GIT, with special emphasis on QGIS.  
- Develop autonomy and critical analytical skills in territorial analysis.  
- Encourage the application of knowledge to real-world cases and datasets.  
- Train students to download, prepare, and manage public geographic data.  

## What are GIT? Difference with GIS

**Geographic Information Technologies (GIT)** encompass the set of technologies, methodologies, and digital resources aimed at managing, analyzing, and visualizing spatial information.  
**Geographic Information Systems (GIS)**, such as [QGIS](https://qgis.org/en/site/), are the main tool in the course, but other technologies are also introduced, such as geographic databases, remote sensing, web mapping, among others.

> ##### Note
>
> The course does not include fieldwork or practical GPS use, but it does provide a theoretical introduction to the role of geolocation in territorial analysis.
{: .block-tip }


The mastery of GIT is fundamental for professional practice in geography. Nowadays, many job offers, both in the public and private sectors, value knowledge of GIS and GIT. These skills allow students to:

- Work in **public administrations** in areas such as territorial planning, urbanism, or environmental management.  
- Join **consulting firms and private companies**, supporting environmental impact studies, logistics, mobility, or market analysis.  
- Carry out tasks in **NGOs and third-sector organizations** in cooperation projects, natural resource management, or social cartography.  
- Participate in **research and academic teams**, in diverse fields such as urban geography, climatology, health, or history.  

In short, GIT facilitate the understanding of spatial relationships and decision-making in planning, sustainability, environmental management, tourism, and many other fields.

## Methodology and functioning

The course is structured according to the **flipped classroom** model. This means that:

- Students are required to prepare theory and practice before face-to-face sessions (manual + Moodle).  
- Participation is encouraged at the beginning of each class with presentations of concepts, questions, practical results, or queries.  
- Classroom sessions are dedicated to solving difficulties, group work, case discussions, and project development.  
- Students will often be asked to come to the teacher’s computer to demonstrate processes or solve small tasks in front of the group.  
- Teaching is aimed at facilitating learning, proposing challenges, providing guidance, and fostering collaboration.  

The [Moodle URV](https://moodle.urv.cat/) platform is used for:

- Access to materials.  
- Submission of exercises and projects.  
- Communications and announcements.  

The **final grade** is structured as follows:

| **Element**                        | **Description**                                                               | **Weight** |
|-----------------------------------|-------------------------------------------------------------------------------|-----------|
| **Continuous assessment**          | Self-assessment questionnaires on Moodle, mandatory for follow-up, not graded | 0% (*) |
| **Participation at the beginning of class** | Presentation of concepts, questions, or practical results to the group       | 10% |
| **Final theoretical exam**         | Written test on basic GIT/GIS concepts                                        | 20% |
| **Final practical exam**           | QGIS-based problem-solving with a different municipality, independent reproduction and resolution | 30% |
| **Final integrative project**      | Complete location study with knowledge integration and justification          | 40% |

(*) Moodle questionnaires are mandatory for course progress but do not contribute to the final grade.

The central course project (integrative project) consists of the **optimal location of a spa or wellness center**, using real data from Vilaseca (Tarragona) for explanations. Alternative application cases may be proposed if agreed with the instructor. Students may also select other municipalities for their practical work, thus connecting with diverse contexts.

This project carries a **very significant weight in the evaluation (40%)** and represents the opportunity to put into practice all the knowledge acquired during the course. If developed well, it may become a **valuable portfolio** to showcase in job or internship interviews.

In addition to the technical part, students will be asked to reflect as geographers would when choosing a location for a spa: selecting a place that is well connected but quiet, free from noise, with pleasant visual basins, adequate proximity and distance to natural resources such as the sea or protected areas, availability and size of the plot, and compatibility with current urban planning.

Finally, the **learning outcomes** or competences of this course are specified in the [official guide](https://guiadocent.urv.cat/docnet/guia_docent/index.php?centre=21&ensenyament=2123&assignatura=21234114&any_academic=2025_26&any_academic=2025_26). This manual details the following practical objectives:

- Explain the fundamental concepts of GIT and GIS.  
- Apply basic and advanced procedures in QGIS for spatial analysis.  
- Download, prepare, and integrate public data from various sources.  
- Carry out practical territorial analysis projects.  
- Critically assess the tools and methodologies used.  

## Resources and data

The resources and data used in the course are mainly **open and public**, with licenses that allow reuse in teaching, professional, or research contexts. GIS software (such as **QGIS**, **SAGA**, or **GRASS GIS**) is distributed under the **GNU General Public License (GPL)**, which authorizes use, modification, and redistribution of the code. Official **CNIG/IGN** data are published under the **Reuse of Public Sector Information License (RISP)**, which allows free use provided the source is cited. In the case of **OpenStreetMap**, information is protected by the **Open Database License (ODbL)**, which guarantees freedom of use and adaptation with attribution and share-alike. Other open data portals (such as **ICGC**, **Idescat**, or the **Catalan Government**) often use **Creative Commons licenses** (e.g., **CC BY** or **CC BY-SA**), which also facilitate reuse with explicit attribution. For commercial purposes, restrictions of these licenses must be checked.

### Software (QGIS, SAGA, GRASS and plugins)

To ensure compatibility and access to necessary tools, it is recommended to:

- **QGIS**: install the **latest Long Term Release (LTR)** or the **latest stable version**. At the start of the course, reference versions are **QGIS 3.40.x (LTR)** and **QGIS 3.44.x (stable)**. Avoid very old versions (e.g., 3.4) due to limitations and fixed bugs.  
  - Download the official installer from the [QGIS downloads page](https://qgis.org/en/site/forusers/download.html).  
- **Complementary installation**: the QGIS package usually includes **[SAGA GIS](http://www.saga-gis.org/)** and **[GRASS GIS](https://grass.osgeo.org/)**, which are very useful tools for advanced analysis. It is recommended to install them together, as QGIS can integrate them directly as additional algorithm providers.  
- **File system and formats**: we will preferably work with **GeoPackage (.gpkg)** as the main data container for the project. The QGIS project file (**.qgz**) and its associated GeoPackage must be stored in an **organized folder structure**.  
- **Recommended plugins** (installation via *Plugins → Manage and Install Plugins…*):  
  - **QuickMapServices** (background maps)  
  - **qgis2web** (basic export to web maps)  
  - **MMQGIS** (additional vector utilities)  
  - **DataPlotly** (charts from tables and fields)  
  - **Profile Tool** or alternatives for profiles (if needed in exercises)  
  - **Semi-Automatic Classification Plugin** (basic remote sensing; activated if required)  

This is **cross-platform software**, working stably on **Windows, macOS, and Linux**, so each student can use their preferred operating system. An interesting competence in the course is learning to **adapt to small differences** that the software may present depending on the version or system used.

> ##### Note
>
> some of these plugins will be used optionally. Specific indication will be given for each practice.
{: .block-tip }

### Public and open data

Students are encouraged to **search, download, and explore as many geospatial data sources as possible on their own initiative**. This autonomous exploration helps to understand the diversity of formats, the variable quality of sources, and their limitations. In this course, we will focus only on some main and complementary resources, which will serve as a starting point to develop these skills.

| **Resource** | **What you can find** |
|--------------|------------------------|
| [CNIG – National Geographic Information Centre](https://www.cnig.es/) and [Download Centre](https://centrodedescargas.cnig.es/CentroDescargas/) | National base cartography, orthophotos, digital terrain models |
| [General Directorate of Cadastre](https://www.sedecatastro.gob.es/) | Cadastral and parcel information |
| [ICGC – Cartographic and Geological Institute of Catalonia](https://www.icgc.cat/en/) | Cartography and geographic information of Catalonia |
| [Idescat – Statistical Institute of Catalonia](https://www.idescat.cat/) | Territorial and demographic statistics |
| [OpenStreetMap](https://www.openstreetmap.org/) | Global collaborative cartography |
| [Government of Catalonia Open Data Catalogue](https://dadesobertes.gencat.cat/) | Thematic open data of Catalonia |

### Additional resources (other datasets and web services)

| **Resource** | **What you can find** |
|--------------|------------------------|
| [Natural Earth](https://www.naturalearthdata.com/) | Global cartography at small scales |
| [Geofabrik](https://download.geofabrik.de/) | OSM extracts by regions and countries |
| [Overpass Turbo](https://overpass-turbo.eu/) | Advanced OSM data queries via API |
| [IDEE – Spanish Spatial Data Infrastructure](https://www.idee.es/) | Access to SDI services and catalogs at the national level |
| [IGN-CNIG web services](https://www.ign.es/web/ign/portal/servicios-web) | WMS/WMTS/WFS services of cartography and orthophotos |
| [ICGC – Geoservices](https://www.icgc.cat/en/administracio-i-empresa/serveis/geoserveis) | WMS/WMTS/WFS services of Catalonia |
| [Iberpix](https://www.ign.es/iberpix2/visor/) | IGN cartographic viewer |
| [Copernicus Browser](https://browser.dataspace.copernicus.eu/) | Sentinel and Landsat imagery |
| [USGS EarthExplorer](https://earthexplorer.usgs.gov/) | Satellite imagery download (Landsat, ASTER, etc.) |
| [Eurostat GISCO](https://ec.europa.eu/eurostat/web/gisco) | Administrative and statistical units of the EU |
| [CartoCiudad](https://www.cartociudad.es/) | Urban cartography and road networks of Spain |
| [CNIG Digital Photographic Library](https://fototeca.cnig.es/) | Historical aerial imagery |

## Recommendations

To make the most of the course, it is recommended to:

- Check [Moodle](https://moodle.urv.cat/) regularly for notifications and submissions.  
- Prepare theory and practice before face-to-face sessions.  
- Actively participate at the beginning of each class, raising questions or presenting results.  
- Maintain **strict order in folders and filenames**, since it is very easy to get lost without a proper methodology.  
- Develop **good working habits** from day one: saving versions, documenting steps, using consistent names, and making backups.  
- Use the manual resources, data sources, and bibliography to deepen understanding.  

The instructor will emphasize these aspects during the course, but it is the student’s responsibility to acquire and consolidate these habits in order to successfully complete the subject.

In addition to the course materials, students are encouraged to read, follow specialized channels, and explore all kinds of resources about GIT. Regarding manuals, even though some references are several years old, it should be remembered that many fundamental concepts of GIT and geographic information science change very slowly, or not at all, over decades. This makes them a **worthwhile investment** to build a solid theoretical foundation on which to develop more current practical skills.

A classic and highly recommended example is the book {% cite Longley:2015:GIS:2809188 %}, available at the CRAI, which offers a complete and rigorous overview of the fundamentals of the discipline.
