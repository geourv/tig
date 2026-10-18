---
title: "Bonus opcional · Guia docent de reproducció amb PyQGIS i SQL"
lang: ca
recipient: docent
content_status: approved
subject: "Tecnologies de la Informació Geogràfica"
subject_code: "21234114"
author: "Benito Zaragozí"
institution: "Universitat Rovira i Virgili"
---

# Propòsit i enunciat

El bonus ha de reforçar una operació del curs i introduir una altra manera de formalitzar-la. L’alumnat tria una via executable en el seu entorn, explica el codi i compara el resultat amb una referència ja validada. L’objectiu és reproducció i diagnòstic, no quantitat de línies.

El model gràfic de Processament continua sent contingut obligatori. PyQGIS i SQL es presenten després, com a alternatives opcionals. Una activitat petita sobre la ROI, un recompte de portals o un retall conegut és més fàcil de comprovar que un script que intenti automatitzar tot el curs.

# Preparació i conducció del taller

| Component | Durada orientativa |
| --- | --- |
| Aula o taller opcional | 60–90 min |
| Treball autònom i explicació | 90–150 min |
| Preparació docent | 30–45 min |

Table: Estimació per a una sola via i una operació coneguda.

Estimació pendent de contrast amb alumnat, després del model gràfic i amb QGIS funcional. No inclou instal·lar un servidor PostGIS; aquella via només es proposa amb l’entorn disponible. És una dedicació opcional addicional a la pràctica on s’avaluï l’aportació.

La preparació comprova els fragments sobre una còpia i conserva la referència. A classe es relaciona cada paràmetre amb el diàleg conegut abans d’executar el codi. Les aturades són identificació d’entrada, resultat persistent i comparació. Convé demanar quin canvi faria fallar un control i provar-lo sobre una còpia: una excepció entenedora pot ser el resultat correcte d’una entrada inadequada.

# Preparar Moodle

1. Afegir **Bonus opcional · PyQGIS o SQL** a la **Tasca de PR6**, o a la pràctica que el professor indiqui expressament.
2. Copiar el bloc següent a **Descripció** fins al final de «Qualificació». Indicar la pràctica a la qual contribueix i una sola via inicial; no crear una obligació de programació per a tot l’alumnat.
3. Adjuntar a **Fitxers addicionals** el PDF d’alumnat del bonus. Si s’ofereix codi resolt, identificar-ne procedència i supòsits i adjuntar només l’exemple i les dependències necessàries.
4. Coordinar data, tramesa de `.py` o `.sql` i mida amb la pràctica principal. El bonus contribueix al seu 20% d’ampliacions; no afegeix punts per sobre de 10 ni una segona qualificació pel mateix resultat.
5. Revisar la **vista d’estudiant** i comprovar que es pot seguir la via escollida amb l’entorn anunciat. El paquet docent conserva codi, referència i controls per preparar el taller.

## Enunciat per copiar a la descripció

**Objectiu i dades.** Es pot reproduir amb PyQGIS o SQL una operació ja validada sobre les dades pròpies. Cal triar una via compatible amb l’entorn, conservar la referència i explicar com cada fragment correspon a una entrada, una operació o un control.

**Treball de l’ampliació.** La proposta identifica pregunta, motor, versions, paràmetres i destinació nova. Cal executar el codi, desar la sortida, reobrir-la i comparar-la amb QGIS. El model gràfic i els apartats bàsics de la pràctica principal continuen sent els seleccionats pel professor i recollits a Moodle.

**Idees per desenvolupar el 20%.** Una d’aquestes aportacions pot ser suficient si està ben contrastada:

- PyQGIS: parametritzar municipi i radi del buffer → caixa, provar dos radis i una entrada incorrecta i comparar les sortides amb el model gràfic. Cal separar buffer i ROI i justificar la tolerància geomètrica.
- SQLite: resumir portals per codi, incloure el grup nul i comparar files, categories i identificadors únics amb l’agregació de QGIS. Explicar quina unitat compta cada consulta i comprovar la conservació del total.
- PostGIS, amb entorn disponible: reproduir buffer → caixa amb els mateixos paràmetres, comprovar SRID i geometries i comparar amb QGIS. La consulta s’ha d’executar realment; un text SQL sense resultat no acredita la reproducció.

**Documentació i lliurament.** Cal conservar `.py` o `.sql`, resultat nou i explicació als apunts de la pràctica principal, amb comparació, incidències i captures significatives. El codi rebut com a exemple s’atribueix i les adaptacions pròpies s’identifiquen. Més línies o dues vies alhora no constitueixen per si soles una aportació millor.

**Qualificació.** La pràctica principal manté **70% treball bàsic, 20% ampliacions i 10% documentació**, màxims de **7, 2 i 1 punts**. Aquest bonus pot contribuir als **2 punts d’ampliacions** i la seva explicació, al bloc documental, sense duplicar la mateixa aportació. És opcional, no substitueix els obligatoris i no garanteix puntuació automàtica.

# Entrades i selecció del cas

La còpia de treball parteix d’un resultat anterior amb font, paràmetres i controls documentats. La referència es conserva intacta i cada prova té una destinació nova. Cal identificar l’edició de les dades i no tornar a descarregar una font diferent durant la comparació.

| Via | Cas inicial adequat | Entorn que cal explicitar |
| --- | --- | --- |
| PyQGIS | Inspecció de capa i buffer → caixa envolupant | Consola o entorn QGIS compatible i proveïdor natiu |
| SQLite tabular | Recompte de portals per codi, nuls i grups | Connexió GeoPackage del Gestor de bases de dades |
| PostGIS espacial | Buffer → caixa, o retall vectorial conegut | PostgreSQL amb PostGIS, esquema, geometria i SRID comprovats |

Table: Tres contextos que no s’han d’intercanviar per semblança de sintaxi.

Per a la ROI es mantenen EPSG:25831, una entitat municipal, 500 m, 8 segments/quadrant i les mateixes opcions geomètriques de PR6. Un altre nombre de segments o una altra font invalidaria la comparació controlada encara que la caixa resultés visualment semblant.

# Progressió PyQGIS

La demostració comença llegint el nom del projecte, les capes i els CRS. Es comprova que `municipi_treball` sigui inequívoca i vàlida abans de mostrar `processing.run()`. La selecció o un filtre residual s’han de tractar com a part de l’estat d’entrada.

L’ajuda d’algorisme permet relacionar el diàleg de QGIS amb el diccionari de paràmetres. El buffer alimenta la caixa envolupant i la sortida retornada es distingeix de la capa afegida al projecte. Una prova temporal facilita l’aprenentatge; el resultat conservat s’ha de desar i reobrir.

El codi propi incorpora controls proporcionats: nombre de capes candidates, nombre d’entitats, CRS, geometria no buida i destinació nova. Una excepció interpretable és preferible a una execució que continua amb una capa equivocada. No cal introduir classes o infraestructures de programació que no ajudin a resoldre el cas.

# Progressió SQL

La via SQL comença amb un resum de files al GeoPackage i pot continuar amb una operació geomètrica en PostGIS. Cada pas identifica la connexió i les funcions disponibles abans d’interpretar el resultat.

## Consulta tabular sobre GeoPackage

El recompte per `cod_postal` reprèn PR3 i l’activitat de Reus. Cal comprovar nom físic de la taula, unitat d’observació i nuls. `COUNT(*)` compta files; `COUNT(cod_postal)` exclou nuls; `COUNT(DISTINCT cod_postal)` compta categories no nul·les. Cap d’aquests valors és automàticament un nombre d’ubicacions úniques.

La quadrícula de resultats del Gestor no és una taula desada. Si la consulta alimenta una conclusió, es conserven text SQL, resultat i comprovació dels totals. Es pot contrastar amb l’agregació equivalent de QGIS.

## Consulta espacial en un entorn preparat

PostGIS és una via opcional quan l’entorn estigui disponible. La consulta de la lectura d’alumnat pressuposa una taula poligonal pròpia amb SRID 25831 i calcula `ST_Buffer` seguit de `ST_Envelope`. Cal verificar el motor, la columna geomètrica, el nombre d’entitats i la validesa abans d’executar-la.

La comparació manté explícits els segments per quadrant i els estils. Les versions de QGIS, PostGIS i GEOS poden introduir diferències numèriques; els controls comparen significat i geometria amb tolerància declarada, no només hashes ni noms de capa.

Una consulta espacial que falla amb `no such function` en SQLite no demostra un defecte de les dades. Primer cal identificar la connexió i les extensions disponibles. No es presenta un GeoPackage com si incorporés tot el catàleg PostGIS ni s’imposa una instal·lació de servidor com a prerequisit del curs.

# Controls i interpretació

El recompte tabular es contrasta amb les files d’entrada i la distribució dels nuls. La ROI es contrasta amb les sortides manual i del model: CRS, recompte, validesa, extrems, àrea i diferència espacial. Per a un retall, s’afegeix traça d’IDs i recàlcul de longitud o superfície.

Cal comprovar que la referència continuï intacta, que la sortida nova es reobri i que l’explicació identifiqui cada operació. Un codi executat sense error pot estar calculant una altra capa, un altre radi o un altre subconjunt.

El cas resolt executa el fragment PyQGIS sobre el municipi CNIG i obté buffer i caixa equivalents al model de PR6. La consulta SQLite agrupa els **3.584 registres** de portals municipals i en conserva el total. La font PostGIS es proporciona com a exemple per a aquell entorn; aquests dos contrastos no acrediten una execució en PostgreSQL/PostGIS.

Si s’exporta automàticament un model com a algorisme Python, el fitxer generat és un punt de partida per llegir i comprendre. No acredita per si sol autoria de la lògica ni validació de la seva reexecució. La procedència del codi i les adaptacions s’han d’explicar.

# Paquets i revisió

L’alumnat treballa sobre les seves entrades ja preparades i segueix les instruccions d’entorn del PDF. El suport docent conserva l’entrada de referència, el codi resolt, els resultats i els controls. Si es comparteixen scripts o consultes, s’identifiquen com a exemples i s’explica quines parts cal adaptar al municipi propi.

La correcció valora precondicions, correspondència entre codi i procediment, persistència, comparació i explicació dels errors. Parametrització, lots o diagnòstics poden reforçar l’aportació, que continua sent opcional. Moodle identifica la pràctica a què s’imputa dins del 20% d’ampliacions i evita comptar-la dues vegades.

# Referències

- [Processament i ampliacions opcionals, manual TIG](https://geourv.github.io/tig/ca/chapters/processament-automatitzacio/).
- [Processament des de la consola, QGIS 3.44](https://docs.qgis.org/3.44/en/docs/user_manual/processing/console.html).
- PostGIS: [ST_Buffer](https://postgis.net/docs/ST_Buffer.html) i [ST_Envelope](https://postgis.net/docs/ST_Envelope.html).
