---
lang: en
permalink: /:title/en/
title: "Setting up the GIS environment"
author: Benito Zaragozí
date: 2025-09-07
category: guide
weight: 1
layout: chapter
mermaid: false
---

A geographic information system (GIS) is the combination of software, hardware, data and knowledge to capture, store, analyse and visualise geospatial information. In this course we will use QGIS as our main tool, but the objective is broader: learning to **organise work** with criteria so that projects are traceable, repeatable and easy to share. This first chapter deals with precisely that: operating systems and paths, folder structure, naming criteria, project files and basic management of compressed files.

## Operating systems and paths

QGIS is cross-platform: it works on Windows, macOS and GNU/Linux. Windows uses paths with backslashes (`C:\projects\gis\data`), whilst macOS and Linux use forward slashes (`/Users/user/project` or `/home/user/project`). macOS and Linux share Unix roots and, despite interface differences and package managers (Linux has multiple distributions), they have similar file logic. When the same project moves between different equipment and systems, this disparity of paths is a typical source of errors. Therefore it is preferable to configure projects so they point to **relative paths** from the location of the `.qgz`.

An **absolute path** always indicates the complete position of an element within the file system. On Windows it starts with the drive letter (`C:\...`), whilst on Linux and macOS it starts from the root (`/`). Some examples would be:

- Windows: `C:\Users\anna\Documents\gis-project\data\municipalities.shp`
- Linux: `/home/anna/gis-project/data/municipalities.shp`

In contrast, a **relative path** describes the route to a file in relation to the folder where the project is located. This option is the most practical when working with QGIS because it allows moving the complete project folder without breaking the links. Relative paths are based on special symbols:

- `./` indicates the current folder. For example, `./data/municipalities.shp` points to the `data` subfolder within the project.
- `../` indicates the parent folder (going "one level up"). For example, if the project is at `sandbox/spa/`, the path `../data/municipalities.shp` will take us to the `data` folder that is at the same level as `sandbox`.
- They can be chained: `../../` means "go up two levels".

This means that if a project file `.qgz` is saved at `sandbox/spa/`, and the layer is at `sandbox/spa/data/buildings.shp`, the relative path will simply be `./data/buildings.shp`. If instead the data is in the general `data/` folder, the relative path could be `../../data/municipalities.shp`.

> Activate and check the use of **relative paths** in the QGIS project properties dialogue. This way the project will open the same in Windows, macOS and Linux, regardless of where exactly the folders are saved.
{: .block-tip }


## Folder organisation

Working with spatial data involves handling many files. A minimal and stable organisation avoids confusion and waste of time. Therefore it is advisable to clearly separate **sources**, **workspace** and **outputs**. The `data/` folder should contain the original data, downloaded from official or open sources, which should never be modified. The `sandbox/` folder is the active workspace: each project has its own subfolder with the project file `.qgz` and temporary derivatives. When a result is considered definitive, it moves to `results/`, which acts as a store for consolidated and reusable layers and tables. Final cartographic outputs, prepared with the composition editor, are saved to `maps/` in PDF or image format.

```bash
gis-project/
├── data/       # original data (never modify)
├── sandbox/    # active workspace
│   ├── spa/         # project 1: .qgz + temporary derivatives
│   └── mobility/    # project 2: analogous structure
├── results/    # definitive layers and tables (reusable)
└── maps/       # final cartographic outputs (PDF/PNG)
```

Naming folders well and maintaining coherence is as important as their structure. If the folder is called `spa/` or `mobility/`, it becomes clear which project it refers to. If instead names like `proj1/` or `test/` are used, it is easy to forget what they contain. The same applies to subfolders: it is advisable to use short, clear names without spaces, such as `data/`, `outputs/`, `vector/` or `raster/`. This way, writing relative paths becomes more intuitive and saves time every time we look for a file.

It is also useful to remember how relative paths work. If the project is saved within `sandbox/spa/`, a layer stored in the `data/` subfolder can be written as `./data/layer_name.shp`. If the layer is found in the general `data/` folder, the relative path would be `../../data/layer_name.shp`, since you need to go up two levels to reach the project root. When folder names are clear and consistent, these paths become intuitive and easy to remember, and this saves time and effort in daily management.

> Always preserve the original files in `data/` and work with copies in `sandbox/`. This way you can repeat processes and audit the workflow without risk of losing the sources.
{: .block-warning }

## File names

Nomenclature is part of the method and forms part of project organisation as much as folders. Using good names saves problems and facilitates collaboration. When names are clear and consistent, anyone opening the project can immediately understand what each file contains, and when months pass it is also easier for us to recover the logic of what we had done.

You should use **lowercase** and simple separators (`_` or `-`), and avoid **spaces**, **accents** and special characters (`ç, ñ, à, é, &, %...`). This is not a quirk, but a practical necessity: many old GIS programmes, and even some current utilities, do not handle these characters well. Spaces can be interpreted as command separators in command lines; accents and special symbols can give errors when the system expects only basic characters from the ASCII set. Today most programmes support modern encodings like UTF-8, but not all formats handle them equally. The Shapefile, for example, has limited support for names with special characters and can cause compatibility problems between systems.

Regarding separators, the difference between `_` (underscore) and `-` (hyphen) depends on the context. In file names, most operating systems support both characters and therefore it is common to find both `_` and `-`. However, in databases and in field or column names it is much safer to always use `_`, since the hyphen `-` can be interpreted as a subtraction operator and would require awkward quotes or escapes. Therefore, a field called `municipality_name` is clear, compatible and easy to use in SQL, Python or R, whilst `municipality-name` could generate errors. In contrast, in web environments it is common to see names with `-` because they integrate well into URLs. In summary: in GIS projects and data management it is preferable to maintain `_` as a separator to ensure compatibility, and reserve `-` only for specific cases such as visible names in web contexts.

Examples of suitable names would be:
`land_use_2023.gpkg`, `municipal_roads_utm31.gpkg`, `census2021_municipalities.shp`.

In contrast, names like `Final Map.shp`, `New Parcels.shp` or `Data nº1.shp` may seem correct at first glance, but they have spaces, accents or symbols that can break workflows when processes are automated or the project is shared with other users.

> Maintain a stable naming pattern (coherent prefixes/abbreviations) and document it at the beginning of the project for your team's use. This avoids misunderstandings and ensures long-term compatibility.
{: .block-tip }

## QGIS project file

QGIS saves the work configuration in `.qgs` (readable XML) or `.qgz` (compressed container with XML and resources). The `.qgz` is the currently recommended option because it takes up less space and can include auxiliary files like thumbnails or annotations, but in any case the project file **does not contain** the data: it only saves paths, styles and visualisation parameters. Therefore it is important to always save it **within** `sandbox/<project_name>/` and check that the layers are linked with relative paths. Avoid accumulating many copies with confusing names; if necessary, make dated snapshots at key moments or use version control with Git.

However, there are formats that can indeed self-contain data and project in a single package. The clearest example is **GeoPackage (.gpkg)**, a container based on SQLite that can include multiple vector and raster layers, tables and even styles. QGIS allows saving styles within the same `.gpkg`, so that representation information travels with the data. This makes it a much more robust alternative than Shapefile and a good complement to project files. Even so, the `.gpkg` does not replace the `.qgz`: the project continues to be the document that links all layers and defines their organisation. What you can do is reduce file dispersion: instead of having twenty separate shapefiles, you can concentrate them in a single GeoPackage and link them from the project. This way the set is easier to move and share.

> Even though containers like GeoPackage exist, QGIS still needs a project file `.qgz` to save the general state of work. The `.gpkg` can be the data store, whilst the project defines its structure and visualisation.
{: .block-tip }

## Data formats (reminder)

From the previous course you know the **Shapefile**, a format created by ESRI in the early 1990s. For many years it was the de facto standard in the GIS world because it was lightweight, relatively simple and compatible with almost all existing programmes at that time, when personal computers were much less powerful than current ones. Its structure allowed storing geometries and attributes quite efficiently, but over time its limitations have become very evident. A shapefile is never a single file, but a set of files that must always go together: at minimum `.shp` (geometry), `.dbf` (attribute table) and `.shx` (index), and often also `.prj` (reference system) and `.cpg` (character encoding).

This fragmented design causes problems: if one of the files is missing, the layer can become corrupted; the `.dbf` file has historical limitations (field names of maximum 10 characters, restricted attribute types, problems with non-ASCII characters); and a shapefile can only contain one layer at a time. Additionally, the 2 GB total size limit and maximum number of entities can be insufficient for current projects. These restrictions are understandable from the technological context of the 1990s, but today they negatively condition professional use. Therefore many voices in the sector promote abandoning it; a well-known resource is the [**"Why Shapefiles Are Bad"**](https://switchfromshapefile.org/) page, which collects and explains all these drawbacks in detail.

As a modern alternative we find **GeoPackage (.gpkg)**, a format standardised by the OGC ([official standard document](https://www.ogc.org/standards/geopackage)). GeoPackage is based on an SQLite database and has the great virtue of allowing multiple vector and raster layers, tables and even styles to be stored in a single file. This drastically reduces file dispersion and makes it easier to share data and projects. QGIS can read and write directly to `.gpkg`, and many other programmes already offer compatibility.

An example helps to see the difference: if we want to work with two vector layers in Shapefile format (for example, municipalities and roads), we will need at least these files:

- `municipalities.shp`
- `municipalities.dbf`
- `municipalities.shx`
- `municipalities.prj`
- `roads.shp`
- `roads.dbf`
- `roads.shx`
- `roads.prj`
- and a QGIS project file `.qgz` that links them.

In contrast, with GeoPackage we can have a single `project.gpkg` file that contains two internal layers (`municipalities` and `roads`) and the `.qgz` project that points to them. This way the set is much more compact and manageable. This advantage is especially important when working in groups or when we have to share results with third parties.

Although in this chapter we will continue using shapefiles to reinforce concepts and maintain compatibility with previous knowledge, it should be borne in mind that the future lies with more robust and versatile formats like GeoPackage.

## Compress and decompress

Many official sources distribute data in `.zip`. It is advisable to **save the original file to `data/`**, decompress it in a homonymous subfolder and copy the working data to `sandbox/<project>/`. On Windows you can use 7-Zip; on macOS and Linux you have integrated tools sufficient for most cases.

> Before starting work, check the exact version of QGIS (preferably LTR) and note it in your project notebook. This makes it easier to reproduce processes and resolve incidents.
{: .block-tip }

## Basic QGIS interface

![Basic QGIS interface]({{ site.baseurl }}/images/qgis-gui-schema.png)

When we open QGIS we find a window that combines menus, toolbars, panels and the main map area. At the top there is the **Menu bar**, with entries like **Project**, **Edit**, **View**, **Layer**, **Vector**, **Raster**, **Database**, **Plugins** or **Help**. From here we can create and save projects, add and remove layers, configure the reference system, install plugins or access official documentation. Just below we find the **Toolbars**, with icons that give direct access to common functions. Among the most important are map navigation (Zoom In, Zoom Out, Pan, Zoom to Active Layer), information query (Identify Features, Measure Distance and Area), data selection (by attributes or by location), or editing management (Add Features, Move, Split or Merge). There is also the toolbar to open the **Composition Editor (Layout)**, which you have already used to prepare laid-out maps in the previous course.

To the left of the interface appear the **Side panels**, of which two are especially relevant:

- the **Layers panel**, where all loaded layers are organised and where we can activate or deactivate their visibility, change their order and access quick options; and
- the **Browser panel**, which allows us to explore local folders, databases and web services like WMS or WFS.

Another common panel is **Processing**, where all the analytical tools of the programme and plugins are concentrated. If any of these panels is not shown, you can activate it with the **View > Panels** menu or by right-clicking on an empty area of the interface. The same applies to toolbars, which can be hidden or shown according to needs.

In the centre of the window there is the **Map area (map canvas)**, which is where all layers are drawn and where we can interact directly with the data by zooming, panning or editing according to the selected tool. At the bottom is the **Status bar**, which shows real-time information: pointer coordinates, current scale, the project's spatial reference system (CRS), loading progress or whether rendering is active. It also offers quick access to options to lock or unlock rendering and view messages generated by processes or plugins.

It should be noted that QGIS incorporates many **context menus** that only appear with the right mouse button over specific elements. For example, right-clicking on an active layer in the Layers panel accesses its properties, styles, export or zoom options. These menus are very useful because they adapt options to the context and allow working more quickly.

## Practice

This practice has the objective of refreshing knowledge from the previous course and consolidating the first steps with the environment and work organisation. Follow the steps calmly, remembering what you already know how to do and paying attention to methodological novelties.

1. **Create the recommended folder tree.**
   In your working folder create `gis-project/` and inside it `data/`, `sandbox/`, `results/` and `maps/`. In `sandbox/` create the `spa/` subfolder. Make sure you have a clear structure because it is the basis of the entire project.

2. **Download a reference Shapefile.**
   Go to the CNIG Download Centre or a similar portal and download a basic layer, such as municipalities. Save the `.zip` file within `data/municipalities/` to keep the original version intact.

3. **Decompress and copy to the sandbox.**
   If the file is `.zip`, decompress it within `data/municipalities/`. You will get a set of files (`.shp`, `.dbf`, `.shx`, `.prj`, etc.). Copy this entire folder to `sandbox/spa/data/`. Remember: **never** work directly with `data/`.

4. **Open QGIS and create a new project.**
   Start QGIS, go to **Project > New** and immediately save the project as `sandbox/spa/spa.qgz`. This way you establish the reference point from which QGIS will create relative paths.

5. **Add the layer and check the paths.**
   Load the Shapefile you have copied to `sandbox/spa/data/`. Open the project properties and check that the paths are configured as relative. This way the project will be portable between computers and operating systems.

6. **Open the attribute table and explore the data.**
   Right-click on the layer and select **Open Attribute Table**. Review the available fields: municipality codes, names, population if available... Remember that the Shapefile's `.dbf` has limitations (for example, short field names).

7. **Apply basic symbology.**
   Open the layer properties and change the symbology: choose a differentiated fill, adjust outlines or apply a uniform colour. This will allow you to better recognise the data on the map and start working on visual representation.

8. **Create a composition (Layout).**
   Open the composition editor and prepare a simple map. Remember the minimum elements that a cartographic composition should always include:
   - Clear and readable title.
   - Legend with symbols used.
   - Scale bar.
   - North arrow.
   - Data sources and authorship.

   You can also add a coordinate grid if you want to practice. Save the composition with a descriptive name within the project and export it to `maps/` as PDF.

9. **Save and close the project.**
   Save changes and check that the `spa.qgz` file has been updated. This will be your first well-organised project within the recommended structure.

> This practice is a starting point: organising folders, working with copies in the sandbox, loading layers, applying symbology, exploring attributes and producing a first composition. Concepts you already knew, but now integrated into a more rigorous methodology that you will follow throughout the course.
{: .block-tip }