-- Optional PostGIS example. It is not executable in plain GeoPackage SQLite.
-- Requires an explicitly imported municipal table, one valid polygonal feature,
-- SRID 25831, a geometry column geom and the documented text field codi_muni.
-- The joint review does not claim a PostgreSQL/PostGIS execution of this file.
WITH marge AS (
    SELECT codi_muni,
           ST_Buffer(geom, 500,
                     'quad_segs=8 endcap=round join=round mitre_limit=2') AS geom
    FROM projecte.municipi_treball
)
SELECT codi_muni, ST_Envelope(geom) AS geom
FROM marge;
