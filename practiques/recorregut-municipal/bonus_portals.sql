-- SQLite / GeoPackage: rows of portals, not people or unique locations.
-- NULL is deliberately retained as its own group.
SELECT cod_postal, COUNT(*) AS n_portals
FROM portals_municipi
GROUP BY cod_postal
ORDER BY cod_postal;
