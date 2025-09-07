---
lang: es
permalink: /:title/es/
title: "Preparando el entorno SIG"
author: Benito Zaragozí
date: 2025-09-07
weight: 1
layout: chapter
mermaid: false
published: true
---

Un sistema de información geográfica (SIG) es la combinación de software, hardware, datos y conocimiento para capturar, almacenar, analizar y visualizar información geoespacial. En este curso utilizaremos QGIS como herramienta principal, pero el objetivo es más amplio: aprender a **organizar el trabajo** con criterio para que los proyectos sean trazables, repetibles y fáciles de compartir. Este primer capítulo se ocupa de eso: sistemas operativos y rutas, estructura de carpetas, criterios de nomenclatura, archivo de proyecto y gestión básica de comprimidos.

## Sistemas operativos y rutas

QGIS es multiplataforma: funciona en Windows, macOS y GNU/Linux. Windows utiliza rutas con barras invertidas (`C:\proyectos\sig\datos`), mientras que macOS y Linux usan barras normales (`/Users/usuario/proyecto` o `/home/usuario/proyecto`). macOS y Linux comparten raíces Unix y, a pesar de diferencias de interfaz y gestores de paquetes (en Linux hay múltiples distribuciones), tienen una lógica de archivos similar. Cuando un mismo proyecto se mueve entre equipos y sistemas diferentes, esta disparidad de rutas es una fuente típica de errores. Por eso es preferible configurar los proyectos para que apunten a **rutas relativas** desde la ubicación del `.qgz`.

Una **ruta absoluta** indica siempre la posición completa de un elemento dentro del sistema de archivos. En Windows comienza por la letra de la unidad (`C:\...`), mientras que en Linux y macOS comienza desde la raíz (`/`). Algunos ejemplos serían:

- Windows: `C:\Users\ana\Documents\proyecto-sig\data\municipios.shp`
- Linux: `/home/ana/proyecto-sig/data/municipios.shp`

En cambio, una **ruta relativa** describe el camino a un archivo en relación con la carpeta donde se encuentra el proyecto. Esta opción es la más práctica cuando trabajamos con QGIS porque permite mover la carpeta completa del proyecto sin romper los enlaces. Las rutas relativas se basan en símbolos especiales:

- `./` indica la carpeta actual. Por ejemplo, `./datos/municipios.shp` apunta a la subcarpeta `datos` dentro del proyecto.
- `../` indica la carpeta superior (ir "un nivel arriba"). Por ejemplo, si el proyecto está en `sandbox/balneario/`, la ruta `../data/municipios.shp` nos llevará a la carpeta `data` que está al mismo nivel que `sandbox`.
- Se pueden encadenar: `../../` significa "subir dos niveles".

Esto significa que si un archivo de proyecto `.qgz` está guardado en `sandbox/balneario/`, y la capa está en `sandbox/balneario/datos/edificios.shp`, la ruta relativa será simplemente `./datos/edificios.shp`. Si en cambio los datos están en la carpeta general `data/`, la ruta relativa podría ser `../../data/municipios.shp`.

> Activa y comprueba el uso de **rutas relativas** en el diálogo de propiedades del proyecto de QGIS. Así el proyecto se abrirá igual en Windows, macOS y Linux, sin importar dónde se guarden exactamente las carpetas.
{: .block-tip }


## Organización de carpetas

Trabajar con datos espaciales implica manejar muchos archivos. Una organización mínima y estable evita confusiones y pérdidas de tiempo. Por eso conviene separar claramente **orígenes**, **espacio de trabajo** y **salidas**. La carpeta `data/` debe contener los datos originales, descargados de fuentes oficiales o abiertas, que no se deben modificar nunca. La carpeta `sandbox/` es el espacio de trabajo activo: cada proyecto tiene su propia subcarpeta con el archivo de proyecto `.qgz` y los derivados temporales. Cuando un resultado se considera definitivo, pasa a `results/`, que actúa como almacén de capas y tablas consolidadas y reutilizables. Las salidas cartográficas finales, preparadas con el editor de composiciones, se guardan en `maps/` en formato PDF o imagen.

```bash
proyecto-sig/
├── data/       # datos originales (no modificar nunca)
├── sandbox/    # espacio de trabajo activo
│   ├── balneario/   # proyecto 1: .qgz + derivados temporales
│   └── movilidad/   # proyecto 2: estructura análoga
├── results/    # capas y tablas definitivas (reutilizables)
└── maps/       # salidas cartográficas finales (PDF/PNG)
```

Nombrar bien las carpetas y mantener coherencia es tan importante como su estructura. Si la carpeta se llama `balneario/` o `movilidad/`, queda claro a qué proyecto se refiere. Si en cambio se utilizan nombres como `proy1/` o `prueba/`, es fácil olvidar qué contienen. Lo mismo pasa con las subcarpetas: es recomendable utilizar nombres cortos, claros y sin espacios, como `datos/`, `salidas/`, `vector/` o `raster/`. De esta manera, escribir rutas relativas resulta más intuitivo y ahorra tiempo cada vez que buscamos un archivo.

También es útil recordar cómo funcionan las rutas relativas. Si el proyecto está guardado dentro de `sandbox/balneario/`, una capa almacenada en la subcarpeta `datos/` se puede escribir como `./datos/nombre_capa.shp`. Si la capa se encuentra en la carpeta general `data/`, la ruta relativa sería `../../data/nombre_capa.shp`, ya que hay que subir dos niveles para llegar a la raíz del proyecto. Cuando los nombres de carpetas son claros y consistentes, estas rutas se vuelven intuitivas y fáciles de recordar, y esto ahorra tiempo y esfuerzo en la gestión cotidiana.

> Conserva siempre los archivos originales en `data/` y trabaja con copias en `sandbox/`. Así puedes repetir procesos y auditar el flujo de trabajo sin riesgo de perder las fuentes.
{: .block-warning }

## Nombres de archivos

La nomenclatura es parte del método y forma parte de la organización del proyecto tanto como las carpetas. Poner buenos nombres ahorra problemas y facilita la colaboración. Cuando los nombres son claros y consistentes, cualquier persona que abra el proyecto puede entender inmediatamente qué contiene cada archivo, y cuando pasan meses también nos es más fácil recuperar la lógica de lo que habíamos hecho.

Hay que utilizar **minúsculas** y separadores sencillos (`_` o `-`), y evitar **espacios**, **acentos** y caracteres especiales (`ç, ñ, à, é, &, %...`). Esto no es una manía, sino una necesidad práctica: muchos programas antiguos de SIG, e incluso algunas utilidades actuales, no gestionan bien estos caracteres. Los espacios se pueden interpretar como separadores de órdenes en línea de comandos; los acentos y símbolos especiales pueden dar errores cuando el sistema espera solo caracteres básicos del conjunto ASCII. Hoy en día la mayoría de programas admiten codificaciones modernas como UTF-8, pero no todos los formatos las gestionan igual. El Shapefile, por ejemplo, tiene un soporte limitado para nombres con caracteres especiales y puede provocar problemas de compatibilidad entre sistemas.

Sobre los separadores, la diferencia entre `_` (guión bajo) y `-` (guión normal) depende del contexto. En nombres de archivos, la mayoría de sistemas operativos admiten ambos caracteres y por eso es habitual encontrar tanto `_` como `-`. Ahora bien, en bases de datos y en nombres de campos o columnas es mucho más seguro utilizar siempre `_`, ya que el guión `-` se puede interpretar como operador de resta y obligaría a poner comillas o escapes incómodos. Por eso, un campo llamado `nombre_municipio` es claro, compatible y fácil de utilizar en SQL, Python o R, mientras que `nombre-municipio` podría generar errores. En cambio, en entornos web es frecuente ver nombres con `-` porque se integran bien en las URL. En resumen: en proyectos SIG y en gestión de datos es preferible mantener `_` como separador para asegurar compatibilidad, y reservar `-` solo para casos específicos como nombres visibles en contextos web.

Ejemplos de nombres adecuados serían:
`usos_suelo_2023.gpkg`, `viario_municipal_utm31.gpkg`, `censo2021_municipios.shp`.

En cambio, nombres como `Mapa Final.shp`, `Parcelas_nuevas.shp` o `Datos nº1.shp` pueden parecer correctos a primera vista, pero tienen espacios, acentos o símbolos que pueden romper flujos de trabajo cuando se automatizan procesos o se comparte el proyecto con otros usuarios.

> Mantén un patrón de nombres estable (prefijos/abreviaturas coherentes) y documéntalo al inicio del proyecto para uso de tu equipo. Esto evita malentendidos y asegura la compatibilidad a largo plazo.
{: .block-tip }

## Archivo de proyecto de QGIS

QGIS guarda la configuración del trabajo en `.qgs` (XML legible) o `.qgz` (contenedor comprimido con el XML y recursos). El `.qgz` es la opción recomendada actualmente porque ocupa menos y puede incluir archivos auxiliares como miniaturas o anotaciones, pero en cualquier caso el archivo de proyecto **no contiene** los datos: solo guarda rutas, estilos y parámetros de visualización. Por eso es importante guardarlo siempre **dentro** de `sandbox/<nombre_proyecto>/` y comprobar que las capas se enlazan con rutas relativas. Evita acumular muchas copias con nombres confusos; si es necesario, haz snapshots fechados en momentos clave o bien utiliza control de versiones con Git.

Ahora bien, hay formatos que sí pueden autocontener datos y proyecto en un solo paquete. El ejemplo más claro es el **GeoPackage (.gpkg)**, un contenedor basado en SQLite que puede incluir múltiples capas vectoriales y raster, tablas e incluso estilos. QGIS permite guardar estilos dentro del mismo `.gpkg`, de manera que la información de representación viaja con los datos. Esto lo convierte en una alternativa mucho más robusta que el Shapefile y en un buen complemento a los archivos de proyecto. Aun así, el `.gpkg` no sustituye el `.qgz`: el proyecto continúa siendo el documento que enlaza todas las capas y define su organización. Lo que sí puedes hacer es reducir la dispersión de archivos: en lugar de tener veinte shapefiles separados, puedes concentrarlos en un único GeoPackage y enlazarlos desde el proyecto. Así el conjunto es más fácil de mover y compartir.

> Aunque existan contenedores como el GeoPackage, QGIS continúa necesitando un archivo de proyecto `.qgz` para guardar el estado general del trabajo. El `.gpkg` puede ser el almacén de los datos, mientras que el proyecto define su estructura y visualización.
{: .block-tip }

## Formatos de datos (recordatorio)

Del curso anterior conoces el **Shapefile**, un formato creado por ESRI a principios de los años 90. Durante muchos años fue el estándar de facto en el mundo de los SIG porque era ligero, relativamente sencillo y compatible con casi todos los programas existentes en aquella época, cuando los ordenadores personales eran mucho menos potentes que los actuales. Su estructura permitía almacenar geometrías y atributos de manera bastante eficiente, pero con el paso del tiempo sus limitaciones se han hecho muy evidentes. Un shapefile no es nunca un solo archivo, sino un conjunto de archivos que deben ir siempre juntos: como mínimo `.shp` (geometría), `.dbf` (tabla de atributos) y `.shx` (índice), y a menudo también `.prj` (sistema de referencia) y `.cpg` (codificación de caracteres).

Este diseño fragmentado provoca problemas: si falta uno de los archivos, la capa se puede corromper; el archivo `.dbf` tiene limitaciones históricas (nombres de campo de máximo 10 caracteres, tipos de atributo restringidos, problemas con caracteres no ASCII); y un shapefile solo puede contener una capa a la vez. Además, el límite de 2 GB de tamaño total y el número máximo de entidades pueden ser insuficientes para proyectos actuales. Estas restricciones se entienden por el contexto tecnológico de los años 90, pero hoy condicionan negativamente el uso profesional. Por eso muchas voces del sector promueven abandonarlo; un recurso conocido es la página [**"Why Shapefiles Are Bad"**](https://switchfromshapefile.org/), que recoge y explica de manera detallada todos estos inconvenientes.

Como alternativa moderna encontramos el **GeoPackage (.gpkg)**, un formato estandarizado por el OGC ([documento oficial del estándar](https://www.ogc.org/standards/geopackage)). El GeoPackage se basa en una base de datos SQLite y tiene la gran virtud de permitir almacenar múltiples capas vectoriales y raster, tablas e incluso estilos en un único archivo. Esto reduce drásticamente la dispersión de archivos y facilita compartir datos y proyectos. QGIS puede leer y escribir directamente en `.gpkg`, y muchos otros programas ya ofrecen compatibilidad.

Un ejemplo ayuda a ver la diferencia: si queremos trabajar con dos capas vectoriales en formato Shapefile (por ejemplo, municipios y carreteras), necesitaremos al menos estos archivos:

- `municipios.shp`
- `municipios.dbf`
- `municipios.shx`
- `municipios.prj`
- `carreteras.shp`
- `carreteras.dbf`
- `carreteras.shx`
- `carreteras.prj`
- y un archivo de proyecto de QGIS `.qgz` que las enlace.

En cambio, con GeoPackage podemos tener un único archivo `proyecto.gpkg` que contenga dos capas internas (`municipios` y `carreteras`) y el proyecto `.qgz` que apunte a él. Así el conjunto es mucho más compacto y manejable. Esta ventaja es especialmente importante cuando trabajamos en grupo o cuando tenemos que compartir los resultados con terceros.

Aunque en este capítulo seguiremos utilizando shapefiles para reforzar conceptos y mantener la compatibilidad con conocimientos previos, hay que tener presente que el futuro pasa por formatos más robustos y versátiles como el GeoPackage.

## Comprimir y descomprimir

Muchas fuentes oficiales distribuyen datos en `.zip`. Conviene **guardar el archivo original en `data/`**, descomprimirlo en una subcarpeta homónima y copiar los datos de trabajo a `sandbox/<proyecto>/`. En Windows puedes utilizar 7-Zip; en macOS y Linux tienes herramientas integradas suficientes para la mayoría de casos.

> Antes de empezar el trabajo, comprueba la versión exacta de QGIS (preferentemente LTR) y anótala en tu cuaderno de proyecto. Esto facilita reproducir procesos y resolver incidencias.
{: .block-tip }

## Interfaz básica de QGIS

![Interfaz básica de QGIS]({{ site.baseurl }}/images/qgis-gui-schema.png)

Cuando abrimos QGIS nos encontramos con una ventana que combina menús, barras de herramientas, paneles y el área principal de mapa. En la parte superior está la **Barra de menú**, con entradas como **Proyecto**, **Editar**, **Vista**, **Capa**, **Vector**, **Raster**, **Base de datos**, **Complementos** o **Ayuda**. Desde aquí podemos crear y guardar proyectos, añadir y eliminar capas, configurar el sistema de referencia, instalar complementos o acceder a la documentación oficial. Justo debajo encontramos las **Barras de herramientas**, con iconos que dan acceso directo a funciones habituales. Entre las más importantes están la navegación del mapa (Zoom +, Zoom −, Panorámica, Zoom a la capa activa), la consulta de información (Identificar entidad, Medir distancia y superficie), la selección de datos (por atributos o por localización), o la gestión de la edición (Añadir entidades, Mover, Dividir o Fusionar). También está la barra para abrir el **Editor de composiciones (Layout)**, que ya has utilizado para preparar mapas maquetados en el curso anterior.

A la izquierda de la interfaz aparecen los **Paneles laterales**, de los cuales dos son especialmente relevantes:

- el **Panel de capas**, donde se organizan todas las capas cargadas y donde podemos activar o desactivar su visibilidad, cambiar su orden y acceder a opciones rápidas; y
- el **Panel de navegador**, que nos permite explorar carpetas locales, bases de datos y servicios web como WMS o WFS.

Otro panel habitual es el de **Procesamiento**, donde se concentran todas las herramientas analíticas del programa y de los complementos. Si alguno de estos paneles no se muestra, lo puedes activar con el menú **Vista > Paneles** o haciendo clic derecho sobre una zona vacía de la interfaz. Lo mismo pasa con las barras de herramientas, que se pueden ocultar o mostrar según las necesidades.

En el centro de la ventana está el **Área de mapa (map canvas)**, que es donde se dibujan todas las capas y donde podemos interactuar directamente con los datos haciendo zoom, panorámicas o edición según la herramienta seleccionada. En la parte inferior se encuentra la **Barra de estado**, que muestra información en tiempo real: las coordenadas del puntero, la escala actual, el sistema de referencia espacial del proyecto (CRS), el progreso de carga o si el renderizado está activo. También ofrece acceso rápido a opciones para bloquear o desbloquear el renderizado y ver mensajes generados por los procesos o complementos.

Hay que tener presente que QGIS incorpora muchos **menús contextuales** que solo aparecen con el botón derecho del ratón sobre elementos concretos. Por ejemplo, haciendo clic derecho sobre una capa activa en el Panel de capas se accede a sus propiedades, estilos, exportación u opciones de zoom. Estos menús son muy útiles porque adaptan las opciones al contexto y permiten trabajar más rápidamente.

## Práctica

Esta práctica tiene el objetivo de refrescar conocimientos del curso anterior y consolidar los primeros pasos con el entorno y la organización del trabajo. Sigue los pasos con calma, recordando qué ya sabes hacer y fijándote en las novedades de metodología.

1. **Crea el árbol de carpetas recomendado.**
   En tu carpeta de trabajo crea `proyecto-sig/` y dentro `data/`, `sandbox/`, `results/` y `maps/`. En `sandbox/` crea la subcarpeta `balneario/`. Asegúrate de que tienes una estructura clara porque es la base de todo el proyecto.

2. **Descarga un Shapefile de referencia.**
   Ve al Centro de Descargas del CNIG o a un portal similar y baja una capa básica, como municipios. Guarda el archivo `.zip` dentro de `data/municipios/` para mantener intacta la versión original.

3. **Descomprime y copia a la sandbox.**
   Si el archivo es `.zip`, descomprímelo dentro de `data/municipios/`. Obtendrás un conjunto de archivos (`.shp`, `.dbf`, `.shx`, `.prj`, etc.). Copia esta carpeta entera a `sandbox/balneario/datos/`. Recuerda: **nunca** trabajamos directamente con `data/`.

4. **Abre QGIS y crea un proyecto nuevo.**
   Inicia QGIS, ve a **Proyecto > Nuevo** y guarda el proyecto inmediatamente como `sandbox/balneario/balneario.qgz`. Así estableces el punto de referencia desde el cual QGIS creará rutas relativas.

5. **Añade la capa y comprueba las rutas.**
   Carga el Shapefile que has copiado a `sandbox/balneario/datos/`. Abre las propiedades del proyecto y revisa que las rutas estén configuradas como relativas. De esta manera el proyecto será transportable entre ordenadores y sistemas operativos.

6. **Abre la tabla de atributos y explora los datos.**
   Haz clic derecho en la capa y selecciona **Abrir tabla de atributos**. Repasa los campos disponibles: códigos de municipio, nombres, población si la hay... Recuerda que el `.dbf` del Shapefile tiene limitaciones (por ejemplo, nombres de campo cortos).

7. **Aplica simbología básica.**
   Abre las propiedades de la capa y cambia la simbología: elige un relleno diferenciado, ajusta los contornos o aplica un color uniforme. Esto te permitirá reconocer mejor los datos en el mapa y empezar a trabajar la representación visual.

8. **Crea una composición (Layout).**
   Abre el editor de composiciones y prepara un mapa sencillo. Recuerda los elementos mínimos que siempre debe incluir una composición cartográfica:
   - Título claro y legible.
   - Leyenda con los símbolos utilizados.
   - Escala gráfica.
   - Flecha de norte.
   - Fuentes de datos y autoría.

   Puedes añadir también una cuadrícula de coordenadas si quieres practicar. Guarda la composición con un nombre descriptivo dentro del proyecto y expórtala a `maps/` como PDF.

9. **Guarda y cierra el proyecto.**
   Guarda los cambios y comprueba que el archivo `balneario.qgz` se ha actualizado. Este será tu primer proyecto bien organizado dentro de la estructura recomendada.

> Esta práctica es un punto de partida: organizar carpetas, trabajar con copias en la sandbox, cargar capas, aplicar simbología, explorar atributos y producir una primera composición. Conceptos que ya conocías, pero ahora integrados en una metodología más rigurosa que seguirás a lo largo del curso.
{: .block-tip }