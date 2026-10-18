---
title: "Bonus opcional · Reproduir una operació amb PyQGIS o SQL"
lang: ca
recipient: alumnat
content_status: approved
subject: "Tecnologies de la Informació Geogràfica"
subject_code: "21234114"
author: "Benito Zaragozí"
institution: "Universitat Rovira i Virgili"
---

# Encàrrec i lloc dins del recorregut

El bonus reprodueix una operació ja compresa i validada a les pràctiques: un filtre, un resum, un retall o la construcció de la ROI. La pregunta és què aporta expressar el procediment com a codi i com es comprova que conserva el mateix significat.

Es pot triar **PyQGIS** o **SQL**, segons l’entorn disponible. És una ampliació opcional posterior al model gràfic de Processament; no substitueix PR1–PR6 ni exigeix aprendre dues vies alhora. El resultat inclou codi explicat, entrades identificades, una sortida comprovable i la comparació amb el procediment conegut.

Moodle identifica la pràctica a què contribueix el bonus, habitualment PR6. La qualificació d’aquella pràctica manté **70% treball bàsic, 20% ampliacions i 10% documentació**, màxims de **7, 2 i 1 punts**. El bonus pot contribuir als 2 punts d’ampliacions; no afegeix punts per sobre de 10 ni modifica els obligatoris seleccionats pel professor.

# Punt de partida

Cal treballar amb una còpia identificada del projecte validat, conservar-ne els originals i fixar una destinació nova. El registre ha d’indicar QGIS, proveïdors o motor SQL, versions, CRS i unitats.

Les entrades són les que cada estudiant ha obtingut i preparat durant el recorregut. El PDF proporciona el contracte i fragments explicats; el codi resolt de Vila-seca, si es comparteix, és una referència per comparar amb el procediment propi.

Una expressió QGIS, una consulta SQLite de GeoPackage i una sentència PostGIS no comparteixen necessàriament funcions. El mateix nom d’una taula tampoc no garanteix que s’hagi obert la mateixa base de dades.

# Via A: PyQGIS dins de QGIS

## Inspeccionar l’entorn i la capa

La consola Python integrada de QGIS dona accés al projecte obert. Un intèrpret Python qualsevol del sistema no té necessàriament aquest entorn. El primer fragment identifica la sessió i les capes sense modificar les dades:

```python
from qgis.core import QgsProject

projecte = QgsProject.instance()
print(projecte.fileName())
for capa in projecte.mapLayers().values():
    print(capa.name(), capa.crs().authid())
```

Abans de processar `municipi_treball`, cal comprovar una única capa amb aquell nom, una entitat vàlida, EPSG:25831 i absència de filtres o seleccions residuals. Si aquestes precondicions no es compleixen, es diagnostica la causa abans de continuar.

## Reproduir una operació coneguda

El cas de la ROI reutilitza els dos algorismes de PR6: buffer i caixa envolupant. Cal consultar l’ajuda de la versió instal·lada:

```python
from qgis import processing

processing.algorithmHelp("native:buffer")
processing.algorithmHelp("native:boundingboxes")
```

El codi propi ha de vincular la capa comprovada a l’entrada i declarar 500 m, 8 segments/quadrant, extrems i unions arrodonits, límit de mitra 2 i dissolució desactivada. La caixa utilitza la sortida del buffer, no el municipi directament.

Una primera prova pot utilitzar sortides temporals per entendre el diccionari de paràmetres i el retorn de `processing.run()`. El resultat final del bonus s’exporta a una destinació nova, es reobre i es compara amb el de PR6. Una capa temporal visible al llenç no constitueix per si sola un lliurament reproduïble.

# Via B: SQL i SQL espacial

## Començar amb una consulta tabular coneguda

En una connexió SQLite al GeoPackage, es pot reproduir el recompte de portals per codi postal. El fragment pressuposa una taula local `portals_municipi` que conserva `cod_postal`; si el projecte té un altre nom físic, cal identificar-lo abans d’adaptar la consulta.

```sql
SELECT cod_postal, COUNT(*) AS n_portals
FROM portals_municipi
GROUP BY cod_postal
ORDER BY cod_postal;
```

La suma dels grups ha de coincidir amb el nombre de files de la taula. Els nuls formen un grup que s’ha d’interpretar, no eliminar silenciosament. El resultat compta registres de portals, no persones, edificis ni ubicacions geomètriques úniques.

## Reproduir la ROI amb PostGIS

L’exemple espacial següent necessita **PostgreSQL amb PostGIS habilitat**. Pressuposa `projecte.municipi_treball`, una sola geometria vàlida a la columna `geom`, SRID 25831 i el camp `codi_muni`. No és una consulta que es pugui enganxar indistintament al GeoPackage SQLite.

```sql
WITH marge AS (
    SELECT
        codi_muni,
        ST_Buffer(
            geom, 500,
            'quad_segs=8 endcap=round join=round mitre_limit=2'
        ) AS geom
    FROM projecte.municipi_treball
)
SELECT codi_muni, ST_Envelope(geom) AS geom
FROM marge;
```

La consulta calcula el buffer i després la caixa alineada als eixos. El resultat d’un `SELECT` no crea una taula persistent: cal desar el text SQL i exportar la sortida a una capa nova si ha d’alimentar el projecte. Assignar un SRID tampoc no transforma coordenades; la preparació mètrica és una precondició.

# Comparar i interpretar

| Aspecte | Comparació amb el resultat conegut |
| --- | --- |
| Entrades | Mateixa font, entitats i preparació |
| Paràmetres | Mateix radi, segments, estil i graf d’operacions |
| Geometria | CRS, recompte, validesa, extrems, àrea i diferència espacial |
| Taules | Mateixa unitat, claus, grups, nuls i totals |
| Entorn | Motor, versió i proveïdors registrats |
| Persistència | Sortida reoberta i sense sobreescriure la referència |

Table: Evidències mínimes del bonus.

Dos programes poden retornar representacions binàries diferents d’una geometria equivalent. A l’inrevés, una àrea igual no demostra igualtat de forma. Cal declarar el control i la tolerància abans d’interpretar una discrepància.

# Fitxers i enunciat de lliurament

El bonus conserva un fitxer `.py` o `.sql`, una còpia nova del resultat i una explicació breu als apunts. Cal poder relacionar cada part del codi amb una entrada, una operació o un control. El model gràfic i els resultats obligatoris del curs continuen conservats.

Una aportació pot parametritzar municipi i radi, provar dos valors i una entrada inadequada i contrastar-los amb el model gràfic. En SQL, es poden comparar files, categories i IDs únics, mantenint el grup nul i la conservació dels totals. La via PostGIS necessita una execució real sobre l’entorn anunciat; el text de la consulta no acredita un resultat.

El 20% valora la pregunta, la correspondència entre procediments, els controls i la interpretació. L’explicació, les captures i l’organització contribueixen al 10% documental de la pràctica principal. Cap aportació es compta dues vegades; presentar més codi o dues vies alhora no garanteix nota ni substitueix els obligatoris.

# Referències

- [Ampliacions SQL i PyQGIS del manual TIG](https://geourv.github.io/tig/ca/chapters/processament-automatitzacio/).
- [Processament des de la consola, QGIS 3.44](https://docs.qgis.org/3.44/en/docs/user_manual/processing/console.html).
- [ST_Buffer, documentació PostGIS](https://postgis.net/docs/ST_Buffer.html).
- [ST_Envelope, documentació PostGIS](https://postgis.net/docs/ST_Envelope.html).
