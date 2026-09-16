---
layout: manual-chapter
title: Organització i documentació d'un projecte SIG
description: Organització, traçabilitat, comprovació i comunicació d'un projecte geogràfic reproduïble.
lang: ca
ref: manual-gis-project-documentation
profiles: [unaltremanual]
content_status: approved
permalink: /ca/chapters/sintesi-documentacio/
weight: 30
part: Continguts
manual_references: true
---

Un projecte SIG no és només el fitxer que QGIS obre. També inclou la pregunta, les dades originals, les transformacions, els paràmetres, els resultats i les decisions que permeten interpretar-los. Si una capa final no es pot relacionar amb una font i un procediment, el mapa pot semblar plausible però no constitueix una evidència verificable.

Aquest capítol inicia la **micropràctica 1** dins d'una estructura `tig/` que servirà per a tot el curs. La còpia de treball serà el projecte QGIS `pr1` incrustat a `sandbox/pr1-fonts-cognom.gpkg`; `cognom` s'ha de substituir pel cognom de l'estudiant i el mateix GeoPackage concentrarà les capes d'informació locals de la pràctica. El capítol crea l'estructura, obre el projecte, incorpora l'Ortofoto Territorial de 2025 de l'ICGC i prepara les dues fonts del límit municipal. El capítol 03 comprovarà els formats i els CRS, materialitzarà les dues extraccions municipals i crearà la versió externa lliurable.

>>>>> En acabar el capítol, cal poder iniciar un projecte SIG ordenat i explicar com les fonts es convertiran en capes comprovables i, més endavant, en lliurables.
>>>>>
>>>>> - Separar dades originals, preparades, resultats intermedis i lliurables dins de l'estructura `tig/`.
>>>>> - Crear `sandbox/pr1-fonts-cognom.gpkg` i desar-hi el projecte de treball `pr1`.
>>>>> - Incorporar el WMS d'ortofoto de 2025 i preparar les fonts municipals de l'ICGC i el CNIG sense confondre visualització, consulta i còpia local.
>>>>> - Documentar fonts, operacions, paràmetres, controls, incidències i limitacions.

El projecte incrustat i qualsevol còpia externa no se sincronitzen automàticament. Durant el treball s'ha d'obrir `pr1` des del GeoPackage de `sandbox/` i desar-hi els canvis. La representació `.qgz` que es crearà al final del capítol 03 compartirà el nom base `pr1-fonts-cognom`, però no substituirà el projecte incrustat que s'ha d'obrir per continuar treballant.

Organitzar no és embellir una carpeta després d'acabar. L'estructura del sistema de fitxers expressa quines entrades s'han rebut, quines còpies es poden modificar, quines sortides encara són provisionals i quins resultats sostenen la conclusió. Si aquests estats només existeixen a la memòria de qui ha executat el treball, una altra persona no podrà saber si `final_2.gpkg` és una font, una prova o el resultat acceptat.

La documentació tampoc no es limita a descriure programari. Ha d'enllaçar una pregunta amb fonts identificades, operacions concretes, paràmetres, incidències, controls i interpretacions. El treball del curs creixerà dins de la mateixa estructura; una decisió feble en aquesta fase es propaga a les activitats següents. Per això la transportabilitat, el llinatge i la recuperació es proven des del primer conjunt de capes, no només abans del lliurament.

## La cadena d'evidència

La **traçabilitat** és la possibilitat de reconstruir com s'ha obtingut un resultat. Comença amb una pregunta explícita i continua amb una cadena de peces relacionades: font, còpia original, preparació, operació, control, resultat i interpretació. Cada peça ha de conservar els identificadors necessaris per enllaçar amb l'anterior.

::: table "Cadena mínima d'evidència d'un projecte SIG"
| Fase | Evidència que cal conservar | Comprovació principal |
| --- | --- | --- |
| Pregunta | Objectiu, àmbit, període i unitat d'anàlisi | La pregunta es pot relacionar amb una mesura o una relació espacial |
| Fonts | Fitxa de procedència i paquet original o URL estable | Productor, versió, CRS, llicència i limitacions estan identificats |
| Preparació | Capa o taula derivada i registre de canvis | Els originals no s'han sobreescrit |
| Anàlisi | Operacions, paràmetres, entrades i sortides | El procediment es pot repetir sense decisions ocultes |
| Validació | Recomptes, mesures, contrastos i incidències | El resultat compleix controls definits abans d'interpretar-lo |
| Síntesi | Capa final, taula, mapa i text breu | La conclusió no va més enllà del que permeten les dades |
:::

La cadena no sempre és lineal. Un control pot revelar una clau duplicada, una geometria invàlida o una resolució insuficient i obligar a tornar a la preparació. Aquesta iteració s'ha de registrar: corregir una incidència forma part del mètode, mentre que ocultar-la impedeix entendre per què el resultat final difereix del primer intent.

Procedència
: Identifica d'on ve una entrada: productor, producte, versió, data, llicència, adreça i forma d'obtenció.

Llinatge de dades
: Descriu què li ha passat dins del projecte: quina capa en deriva, amb quina operació, quins paràmetres i quins controls.

La traçabilitat necessita totes dues dimensions. Un fitxer pot conservar perfectament la URL original i haver perdut la relació amb la capa final; també pot tenir un historial intern molt detallat i partir d'una font sense autoria o data.

Cada sortida ha de tenir antecedents identificables. Si `parceles_candidates` prové d'una intersecció, el diari ha d'indicar les dues entrades exactes, la versió del projecte, l'algorisme, el tractament d'entitats invàlides i el lloc on s'ha desat. Si una entrada es corregeix i l'operació es repeteix, la sortida anterior no s'ha de reetiquetar silenciosament: cal substituir-la de manera controlada o conservar-la com a resultat rebutjat amb la incidència documentada.

El llinatge forma una xarxa de dependències, no només una cronologia. Una mateixa capa preparada pot alimentar un mapa, una unió i una anàlisi de proximitat; una mateixa sortida pot dependre de tres fonts amb dates diferents. El diari pot explicar aquesta xarxa amb identificadors de fitxer i capa sense dibuixar-la. El criteri és que, començant pel resultat, es pugui retrocedir fins a cada original i, començant per una font, es pugui saber en quins resultats intervé.

La ramificació fa visible quines fonts alimenten cada resultat i com una validació pot obligar a revisar una preparació o repetir l'anàlisi.

![Dependències ramificades entre el límit municipal, les dades temàtiques, el WMS, les preparacions, l'anàlisi, el resultat, el mapa i la validació]({{ site.baseurl }}/assets/diagrams/ca/02-sintesi-documentacio/project-data-lineage.mmd "El límit municipal i les dades temàtiques alimenten preparacions que conflueixen en l'anàlisi; el resultat i el WMS de context alimenten el mapa, mentre que la validació pot retornar a la preparació o a l'anàlisi."){: data-figure-width-web="45rem" data-figure-width-pdf="95%"}

La validació també forma part de la cadena. Anotar només que una eina «ha funcionat» descriu l'estat de la interfície, no la qualitat de la sortida. Cal conservar el control aplicat i el seu resultat observat: recompte abans i després, presència de nuls, extensió, rang, geometries problemàtiques o contrast d'una mostra. Els valors reals s'han d'obtenir durant l'execució; una plantilla pot indicar quins controls cal fer, però no anticipar-ne les xifres.

## Organització de dades i resultats

Separar l'estat de les dades evita confondre una font amb una transformació. La còpia original es conserva tal com s'ha rebut o descarregat. Les dades preparades reutilitzables corregeixen estructura, tipus, CRS o àmbit sense perdre la relació amb l'original i serveixen més d'un exercici. Els resultats intermedis permeten diagnosticar un flux, i els finals responen directament una pregunta o alimenten una composició. Aquesta separació entre dades, codi, documentació i resultats redueix decisions implícites i facilita reprendre o transferir el treball {% cite wilsonGoodEnoughPractices2017 %}.

L'estructura comuna del curs és la següent. Els directoris expressen l'estat o la funció dels elements, mentre que el `README.md` i el diari descriuen el conjunt.

![Arbre de directoris i fitxers de l'estructura comuna del curs]({{ site.baseurl }}/assets/diagrams/ca/02-sintesi-documentacio/project-folder-tree.puml "L'arrel tig separa originals, preparacions reutilitzables, intermedis, treball actiu i lliurables; la primera pràctica treballa amb la parella pr1-fonts-cognom a sandbox i només en copia l'estat validat a dist."){: data-figure-width-web="16rem" data-figure-width-pdf="38%"}

L'arbre és el contracte comú de les micropràctiques. `data/raw` conserva allò que s'ha rebut del productor: els paquets i, quan cal obrir-los, una extracció íntegra que no s'edita. `data/processed` conté només preparacions derivades dels originals que s'han de reutilitzar en diversos exercicis, com un mosaic DEM combinat i retallat a l'àrea comuna. `data/interim` conserva sortides necessàries per comprovar o reprendre un procés. `sandbox` és l'espai de treball actiu de QGIS i `dist` queda reservat exclusivament per als fitxers validats que es lliuren.

La primera pràctica utilitza `sandbox/pr1-fonts-cognom.gpkg` com a contenidor i còpia de treball. El projecte que QGIS hi desa s'anomena internament `pr1`. En acabar el capítol 03, `sandbox` contindrà també `pr1-fonts-cognom.qgz`; després de validar la parella, tots dos fitxers es copiaran amb el mateix nom base a `dist/`. La carpeta `dist` no conté originals, proves ni l'única còpia del treball.

`data/raw` ha de preservar els noms i els bytes rebuts del productor; la normalització comença en una còpia i queda documentada. Aquesta còpia es treballa a `sandbox` mentre pertany a una micropràctica concreta. Només passa a `data/processed` quan el resultat és una preparació reutilitzable per a activitats diferents. Aquesta distinció evita convertir qualsevol exportació provisional en una dada comuna del curs.

La separació descriu **estats lògics**, no formats. Un GeoPackage pot contenir una capa preparada, una intermèdia i una final, però els noms interns han d'indicar-ne la funció. Un GeoTIFF pot ser una font original o un resultat. Desar tots els vectors en un únic contenidor redueix el nombre de fitxers, però no converteix automàticament totes les capes en una mateixa fase del procés.

La carpeta `sandbox` conserva els fitxers vius de la micropràctica i també pot contenir proves. No s'ha de convertir en un abocador permanent: una prova que no intervé en cap resultat es pot eliminar després de documentar la decisió que se n'ha extret. Una sortida intermèdia que permet comprovar una incidència o evita repetir una operació costosa s'ha de conservar a `data/interim` amb un nom i un antecedent clars. La decisió depèn de la possibilitat de reconstrucció, no d'una regla segons la qual cal guardar-ho tot.

Les capes temporals de QGIS exigeixen una decisió explícita. Mentre només són resultats temporals, poden desaparèixer en tancar la sessió i no són una evidència persistent. Si una selecció o una transformació alimentarà la micropràctica activa, es desa a `sandbox`; si cal compartir-la entre exercicis o reprendre'n el procés, pot passar a `data/processed` o `data/interim` segons la funció. `dist` només rep resultats finals validats. El diàleg de processament no pot decidir aquesta categoria a partir del nom de l'algorisme.

No totes les capes necessiten un fitxer separat. `pr1-fonts-cognom.gpkg` ha de contenir totes les capes d'informació locals de la primera micropràctica, amb noms que indiquin font i contingut. `municipality_icgc_5k` i `municipality_cnig` expliquen millor què representa cada límit que `capa1`, `final2` o `nova_definitiva`.

Els noms han de ser estables, breus i compatibles amb les eines utilitzades. Convé usar minúscules i unitats explícites quan siguin necessàries, com `vies_buffer_200m`. Les dates formen part del nom només quan distingeixen versions reals de les dades o del resultat; no substitueixen un registre de canvis.

### Convencions de noms, identificadors i esquemes

Un projecte combina almenys tres espais de noms: fitxers del sistema operatiu, capes dins d'un contenidor i camps dins d'una taula. `pr1-fonts-cognom.gpkg` identifica el contenidor i `codi_muni`, un camp. Una capa interna pot anomenar-se `municipality_cnig`. Repetir `pr1` a cada capa no aporta informació, mentre que usar `capa1` impedeix entendre-la fora de l'ordre del panell.

Els sistemes moderns admeten habitualment Unicode i espais, de manera que no és correcte afirmar que qualsevol accent farà fallar QGIS. Tanmateix, un nom com `parcel·les àmbit nord.gpkg` obliga a conservar exactament un espai, un punt volat i un accent, i sovint s'ha de citar entre cometes en una ordre. També pot passar per URL, scripts, SQL, eines antigues o sistemes que normalitzen Unicode de manera diferent. Una convenció conservadora per als **noms tècnics creats pel projecte** és escriure'ls en minúscules i amb caràcters ASCII i, quan no hi ha un vocabulari de projecte fixat, preferentment en anglès; per exemple, `northern-cadastral-parcels.gpkg`. Això redueix friccions i evita decidir com transliterar `ç`, `l·l` o cada vocal accentuada; no implica traduir títols, llegendes, metadades o textos destinats a persones. Els identificadors contractuals del manual, com `municipi_treball`, `codi_muni` i `vies_principals`, són excepcions explícites i s'han de conservar exactament.

Els guions i els guions baixos no es comporten igual en tots els contextos. En directoris i fitxers controlats, el guió separa paraules amb una lectura clara, com `land-use-2026.gpkg`, però un nom no ha de començar per `-` perquè moltes ordres l'interpretarien com una opció. En capes, taules, camps, variables i expressions convé `snake_case`, com `land_use` o `area_m2`: el guió es pot interpretar com una resta en Python i en expressions de QGIS, i obliga a citar molts identificadors SQL. El criteri més important és aplicar una regla explícita i consistent dins de cada espai de noms.

La convenció només s'aplica a allò que controla el projecte. Un paquet conservat a `data/raw` manté el nom rebut, i les peces d'un Shapefile no es reanomenen per separat. Si una còpia preparada rep un nom normalitzat, el diari o l'inventari ha de relacionar-lo amb l'original. Així, la portabilitat no es guanya a costa de perdre procedència.

Un bon nom expressa contingut i funció sense intentar codificar tot el llinatge. Per exemple, `carreteres_retallades` és més informatiu que `resultat3`.

`carreteres_retallades_cnig_2026_epsg25831_v2_definitiu` és un nom excessiu: acumula dades que pertanyen a les metadades i al diari. Les dates només s'afegeixen quan separen períodes reals del fenomen o versions que han de coexistir. Paraules com `nou`, `bo`, `final` o `definitiu2` depenen d'un moment i perden significat tan aviat com hi ha una revisió.

L'**esquema** defineix què significa cada fila i cada camp. Per a una capa preparada s'han de conservar el tipus geomètric, el CRS, l'identificador estable, els noms i tipus dels camps, les unitats, els dominis, el tractament dels nuls i les relacions amb altres taules. Canviar `codi_muni` de text a enter pot eliminar zeros inicials; convertir un nul en zero pot inventar una observació. Aquestes decisions no queden explicades pel nom del fitxer.

El `README.md` defineix el contracte d'entrada del projecte: n'explica la finalitat, identifica el GeoPackage i el projecte de treball incrustat, descriu les carpetes, enumera dependències, fonts i llicències, i indica com reconstruir o comprovar els productes. El diari compleix una funció diferent: registra l'evolució, les execucions, les incidències i les decisions observades. Un dels dos pot contenir el diccionari d'esquema de les capes centrals, però aquesta ubicació s'ha de declarar al `README.md`. No cal descriure camps auxiliars que no s'utilitzen, però sí els que intervenen en filtres, unions, càlculs, simbologia o interpretació. Quan es crea un camp derivat, cal indicar l'expressió, la unitat, les entrades i el significat. La taula final ha de poder llegir-se sense deduir les unitats a partir dels valors.

### Paquets comprimits i còpies originals

Moltes fonts distribueixen diversos fitxers dins d'un `.zip`, `.7z` o altre contenidor comprimit. El paquet és una unitat de distribució, no necessàriament una capa que s'hagi d'editar o obrir directament. Cal conservar-lo amb el nom rebut dins d'una subcarpeta identificable de `data/raw` i extreure-hi el contingut complet sense modificar-lo. Si el productor publica una suma de comprovació, es pot utilitzar per confirmar que la baixada no s'ha alterat.

L'extracció completa és important en formats compostos per diverses peces. Un Shapefile necessita, com a mínim, els fitxers que conserven geometria, índex i atributs, i pot dependre també del CRS i la codificació. Copiar només el `.shp` trenca el conjunt. Altres paquets inclouen metadades, llicències, estils, índexs o diversos fulls territorials; seleccionar-ne una peça abans de llegir l'inventari pot eliminar informació necessària per interpretar-la.

Algunes aplicacions poden llegir determinats recursos dins d'un comprimit, però aquesta capacitat no s'ha de convertir en la base del projecte. Una ruta virtual a l'interior d'un `.zip` pot no funcionar igual en totes les eines i dificulta inspeccionar què s'ha extret. La còpia de treball s'ha de crear després d'obrir i validar l'original, no modificant fitxers dins del paquet ni descomprimint versions diferents a la mateixa carpeta.

Descomprimir no és preparar les dades. Els fitxers extrets continuen sent originals del projecte mentre es mantenen sense canvis. Si cal reanomenar camps, transformar el CRS, reparar geometries o retallar l'àmbit per a la micropràctica activa, la sortida es desa a `sandbox` i el diari relaciona les dues versions. Només una preparació destinada a diversos exercicis passa a `data/processed`. Aquesta disciplina permet tornar a començar quan una preparació era incorrecta sense repetir la descàrrega ni perdre la font.

Abans de donar el paquet per bo s'ha de verificar que s'obre sense errors, que el contingut coincideix amb l'inventari del productor i que no hi ha una carpeta ni un arxiu inesperadament buits. També cal conservar la URL, la data d'accés i les condicions de redistribució. Mantenir el `.zip` original a `data/raw` no significa que es pugui copiar a `dist` si la llicència no ho autoritza.

## Projecte QGIS i transportabilitat

### El fitxer de projecte `.qgz`

El fitxer `.qgz` conserva referències a les fonts, l'ordre i els grups de capes, la simbologia, les etiquetes, les unions, les composicions i altres configuracions. Les dades ordinàries no queden incorporades automàticament al fitxer. Si les rutes apunten a una carpeta personal, el projecte pot obrir-se sense capes en un altre ordinador {% cite qgisUserGuide344 %}.

Un `.qgz` és un paquet comprimit que conté la definició del projecte i recursos auxiliars que QGIS pugui incorporar. La definició registra proveïdors i adreces de fonts, però no converteix qualsevol Shapefile, GeoTIFF, full de càlcul o servei remot en contingut incrustat. La mida petita del projecte no prova que les dades hi siguin. Per saber què necessita, cal inspeccionar les propietats de les capes i executar una prova fora de la ubicació original.

Projecte QGIS
: Document que conserva l'organització, la representació i part de l'estat de treball, però que normalment referencia les dades en lloc de contenir-les.

Capa de projecte
: Vista configurada d'un contingut geogràfic: té nom, estil, filtres i altres propietats dins del projecte i apunta a una font.

Font de dades
: Recurs tècnic que conté o serveix els valors, identificat per un camí, una URL o un identificador uniforme de recurs (URI). En un GeoPackage, la URI combina el fitxer contenidor amb la taula o capa interna.

Proveïdor de dades de QGIS
: Component de programari que sap llegir i, quan correspon, escriure un tipus de font, com OGR per a molts formats vectorials o GDAL per a molts ràsters.

Aquest **proveïdor de dades** no és necessàriament l'organisme productor o distribuïdor estudiat al capítol 01, ni tampoc un **proveïdor de Processament**, que agrupa algorismes. Qualificar el terme evita atribuir a una institució una funció interna de QGIS o confondre el lector de la font amb l'eina que la transforma.

Desar el projecte aviat fixa un punt de referència per a les rutes i evita acumular capes en un projecte sense nom. A la primera micropràctica, el projecte de treball es desa dins de `sandbox/pr1-fonts-cognom.gpkg` amb el nom intern `pr1` i es torna a obrir des d'aquest contenidor. Els canvis rellevants es documenten al diari o amb còpies de control deliberades, no amb una cadena de fitxers com `projecte_final_final2.qgz`.

El projecte conserva estils, filtres, unions i composicions que poden canviar el significat de la vista sense canviar les dades. Una capa oculta per un filtre no està buida; una unió dinàmica pot desaparèixer si falta la taula externa; un disseny pot dependre d'una imatge o una tipografia que no viatja amb la font geogràfica. La prova de transport ha d'incloure aquestes dependències i no només comprovar que el llenç mostra algun mapa.

### Rutes relatives i absolutes

Les **rutes relatives** descriuen la posició d'un fitxer respecte del projecte i permeten moure conjuntament la carpeta. Les rutes absolutes depenen d'una unitat, un nom d'usuari o una jerarquia concreta. Després de configurar les rutes relatives cal traslladar una còpia de la carpeta a una ubicació diferent, obrir el `.qgz` i comprovar que totes les fonts continuen resolent-se.

A Windows, `C:\Users\anna\tig\sandbox\pr1-fonts-anna.gpkg` és una ruta absoluta.

En GNU/Linux, `/home/anna/tig/sandbox/pr1-fonts-anna.gpkg` també és una ruta absoluta. Pot ser correcta a l'equip d'origen i inexistent en un altre sistema. En la versió lliurable, una ruta relativa pot expressar que `pr1-fonts-cognom.qgz` i `pr1-fonts-cognom.gpkg` són a la mateixa carpeta `dist`; mentre tots dos fitxers es moguin junts, aquesta relació es conserva.

Els segments `.` i `..` signifiquen, respectivament, la carpeta actual i la carpeta superior. Són útils per entendre la lògica, però una acumulació de `../../..` sol indicar que les dades han quedat fora de l'arrel transportable. La solució no és memoritzar el camí, sinó reunir dins d'un arbre comú les dependències que es poden copiar legalment. Un recurs compartit en una unitat de xarxa pot justificar una ruta absoluta en un entorn controlat, però aquesta decisió i el requisit de muntatge s'han de documentar.

QGIS permet definir si desa els camins de les fonts com a relatius o absoluts a les propietats generals del projecte. En un projecte extern, la ruta relativa es calcula respecte del fitxer `.qgz`. La `Carpeta inicial del projecte` és l'accés de conveniència que mostra l'`Explorador`, però es pot canviar sense rebasar les rutes de les fonts. Canviar l'opció no copia fitxers dins de l'arbre ni repara automàticament una font que ja no existeix; la versió de `dist` s'haurà d'obrir i comprovar amb la seva pròpia còpia de `pr1-fonts-cognom.gpkg` {% cite qgisUserGuide344 %}.

Les URL de WMS, WMTS, WFS o API no es converteixen en rutes locals relatives. Continuen depenent de xarxa, servidor i, si escau, autenticació. Tampoc no és segur compartir credencials dins del projecte. La transportabilitat ha de distingir capes locals que viatgen amb la carpeta, recursos remots que s'han de tornar a consultar i fonts restringides que cada usuari ha de configurar amb permisos propis.

Una ruta relativa només resol la **localització**. No resol llicències, formats no admesos, extensions de base de dades, tipografies absents, diferències de versió ni dependències de complements. Per això el projecte ha d'indicar la versió de QGIS quan sigui rellevant i sotmetre's a una obertura real en una ubicació neta. Veure la paraula «relatiu» al diàleg és una configuració; obrir totes les fonts després del trasllat és l'evidència.

### Abast del GeoPackage i projecte incrustat

GeoPackage és un estàndard OGC basat en SQLite. Pot contenir diverses taules d'entitats vectorials, taules d'atributs i piràmides de tessel·les, juntament amb metadades i extensions definides segons el cas {% cite ogcGeoPackage2024 %}. Aquesta capacitat el fa adequat per concentrar vectors i taules relacionats sense dispersar-los en molts fitxers. Cada capa continua tenint nom, geometria, CRS, esquema i llinatge propis.

No és una carpeta comprimida d'ús general. Un GeoTIFF analític, un `.zip` original o el PDF del diari no esdevenen capes interoperables pel fet d'introduir-los en una base. Encara que GeoPackage admet tessel·les ràster, això no equival a conservar qualsevol ràster analític de coma flotant amb la mateixa compatibilitat que un GeoTIFF. El projecte del curs mantindrà habitualment aquests ràsters com a fitxers externs dins de l'arbre.

QGIS permet **desar un projecte a un GeoPackage** i **obrir-lo des d'un GeoPackage** mitjançant les accions `Projecte > Desa a > GeoPackage` (*Save to GeoPackage*) i `Projecte > Obre des de > GeoPackage` (*Open from GeoPackage*), encara que la traducció o la posició exacta puguin variar entre versions. En tots dos casos se seleccionen un contenidor i un nom de projecte; no s'estan important o exportant les capes. Altres aplicacions poden llegir les taules geogràfiques i ignorar aquesta definició pròpia de QGIS {% cite qgisUserGuide344 %}.

Al curs, la primera entrada incrustada s'anomena exactament `pr1`. Per continuar la micropràctica s'obre `pr1` des de `sandbox/pr1-fonts-cognom.gpkg`, es treballa sobre les capes locals del mateix contenidor i es desen els canvis en aquesta representació. Després dels controls del capítol 03 se'n crea al mateix `sandbox` una representació externa `pr1-fonts-cognom.qgz`. Amb QGIS tancat, els dos fitxers validats es copien junts a `dist/`.

El projecte incrustat, el `.qgz` extern i les còpies de distribució són representacions independents. L'ordre **Desa** actualitza la representació que està oberta en aquell moment; no hi ha cap enllaç que propagui els canvis a les altres. Les versions de `sandbox` són les còpies de treball i les de `dist` descriuen el candidat de la revisió actual. L'estat lliurat és el paquet complet immutable que s'assembla separadament. Qualsevol diferència posterior ha de ser explicable al diari.

El projecte incrustat **no és una còpia de seguretat**. Comparteix `pr1-fonts-cognom.gpkg` amb les capes: si el contenidor es perd o es corromp, es poden perdre alhora les dades i el projecte. Una còpia de recuperació ha d'estar en una ubicació independent. La còpia situada a `dist` tampoc no substitueix una política de còpies de seguretat.

Els noms interns també s'han de gestionar. Esborrar o reanomenar una taula pot trencar les referències desades al projecte de treball, a la instantània incrustada o al `.qgz`; reemplaçar una capa amb una altra del mateix nom pot ocultar un canvi d'esquema. Després d'una importació s'han de revisar geometria, CRS, camps i recomptes, i després tornar a obrir separadament les representacions que s'han de conservar. El contenidor simplifica el transport físic, no la validació del contingut.

>>>> **Ni el projecte incrustat ni la carpeta `dist` substitueixen una còpia de seguretat independent.** Tots dos faciliten el treball o el lliurament, però no protegeixen per si sols contra la pèrdua del contenidor o de l'única ubicació de treball.

### Còpies de seguretat i control de versions

Còpia de seguretat
: Permet recuperar fitxers després d'una supressió, una avaria o una corrupció. Ha d'existir en una ubicació independent de la còpia de treball i s'ha de provar restaurant-ne contingut.

Control de versions
: Conserva canvis identificats i permet relacionar-los amb una decisió. És especialment útil per al `README.md`, el diari editable, les consultes, els scripts, els models i altres fonts textuals.

Una carpeta sincronitzada pot replicar també una supressió o un fitxer malmès; una còpia al mateix disc no protegeix contra la fallada del disc. Git pot guardar `.qgz`, `.gpkg` o GeoTIFF binaris, però no en pot comparar ni fusionar l'estructura interna com fa amb línies de text. Per això el control de versions no substitueix una còpia de seguretat ni resol automàticament la gestió de totes les geodades.

En un projecte docent es poden combinar còpies de recuperació del conjunt amb fites deliberades dels fitxers centrals. Abans d'una transformació difícil de revertir es crea una còpia tancada del GeoPackage; després es registra al diari què s'ha canviat i quin resultat s'ha validat. No cal conservar una còpia amb marca horària de cada clic. Cal conservar prou estats per recuperar-se i prou documentació per saber quin estat és coherent.

La carpeta `dist` contindrà **còpies de distribució** només quan es tanqui la micropràctica al capítol 03. Aleshores hi haurà `pr1-fonts-cognom.gpkg` i `pr1-fonts-cognom.qgz`; no s'hi copiaran memòries cau, temporals, credencials ni originals. Abans de lliurar-los, tots dos fitxers s'hauran de copiar junts a una ubicació neta i obrir-los sense dependre de `sandbox`. Fins a aquell moment, `dist` continua buit.

`dist` és el candidat pla d'una revisió, no l'arxiu de totes les versions. Si es detecta un error abans del lliurament, no se'n modifica el binari al lloc: es reconstrueix el candidat complet en un `dist` net a partir de les fonts canòniques, regenerant la fita afectada i totes les descendents. Un cop lliurat el paquet complet, es conserva immutable i identificat com una revisió. Qualsevol correcció posterior s'assembla en una carpeta separada com una revisió completa nova, que manté els noms contractuals a l'interior; no es barregen fitxers de revisions diferents ni s'altera el paquet anterior.

::: table "Cinc registres o còpies que no s'han de confondre"
| Peça | Funció | Prova necessària |
| --- | --- | --- |
| Inventari | Descriu les peces, la ubicació, la funció i les dependències de l'estat actual | Cada entrada existeix i es pot relacionar amb el projecte |
| Diari | Registra decisions, execucions, incidències, controls i interpretacions | Una altra persona pot reconstruir per què s'ha acceptat cada resultat |
| Estat de treball | Conserva el projecte incrustat i les capes locals de la micropràctica | `pr1` s'obre des de `sandbox/pr1-fonts-cognom.gpkg` i manté les fonts esperades |
| Còpia de seguretat | Permet recuperar-se d'una pèrdua o corrupció | Es troba en una ubicació independent i se n'ha provat la restauració |
| Còpia de distribució o transport | Trasllada només les peces redistribuïbles necessàries | Els dos fitxers de `dist` s'obren junts en una ruta neta sense dependre de la còpia de treball |
:::

### Configuració inicial a QGIS

En QGIS, la separació conceptual entre fonts, organització, representació i procés es tradueix en regions funcionals diferents: l'`Explorador` localitza fonts, el panell `Capes` les organitza, el llenç les representa, la caixa d'eines les transforma i la barra d'estat informa de l'escala, les coordenades i el CRS de la vista. La disposició concreta depèn de la versió i del perfil. Abans d'afegir capes cal crear l'arbre `tig/`, obrir un projecte nou i establir `EPSG:25831` com a CRS del projecte. El capítol 03 explicarà per què aquesta definició és adequada per al municipi assignat i com es diferencia del CRS de cada font.

En obrir-lo, la captura permet relacionar cada decisió del projecte amb el lloc on es comprova: les dependències a l'`Explorador`, l'ordre al panell `Capes`, el resultat visible al llenç i els algorismes a la caixa d'eines.

![Interfície de QGIS amb l'Explorador i el panell de Capes a l'esquerra, el llenç del mapa al centre, la Caixa d'eines de processament a la dreta i la barra d'estat amb el localitzador a la part inferior]({{ site.baseurl }}/assets/img/qgis/qgis-interface-overview.png "Interfície de QGIS 3.44.11 en català. La posició i la visibilitat dels panells i de les barres d'eines poden variar segons la versió i el perfil; les regions funcionals es mantenen."){: data-figure-width-web="56rem" data-figure-width-pdf="100%"}

A `Projecte > Propietats > General` es configura l'emmagatzematge de camins relatius i la `Carpeta inicial del projecte` s'estableix a l'arrel `tig/`. Al panell `Explorador`, el menú contextual de l'entrada `GeoPackage` permet crear una base de dades buida a `sandbox/pr1-fonts-cognom.gpkg`; no cal inventar una capa per crear el contenidor. A continuació s'utilitza `Projecte > Desa a > GeoPackage` per desar-hi el projecte amb el nom curt `pr1`. Des d'aquest moment, les sessions de treball s'han de reprendre amb `Projecte > Obre des de > GeoPackage`.

El context visual s'incorpora des del WMS de l'Ortofoto Territorial de l'ICGC. Cal seleccionar l'edició de 2025, donar a la capa un nom llegible com `ICGC Ortofoto territorial 2025` i mantenir-la separada de les entrades vectorials: continua sent una imatge remota de context i no una capa que s'hagi d'introduir al GeoPackage.

La primera font vectorial s'explora amb Open ICGC. Des de les divisions administratives 1:5.000 es carrega la capa de termes municipals, s'identifica el camp que conté el nom o codi oficial i se selecciona el municipi assignat. La selecció permet comprovar que hi ha una única entitat correcta, però encara no es desa: el capítol 03 fixarà el CRS de sortida i crearà `municipality_icgc_5k` dins de `pr1-fonts-cognom.gpkg` amb **Desa les entitats seleccionades com...**.

La segona font és la distribució GML actual del producte d'unitats administratives del CNIG, `LINEAS_LIMITE_GML.ZIP`. El paquet descarregat i el seu contingut complet es conserven a `data/raw` amb els noms rebuts. A QGIS es carrega el subconjunt municipal `AdministrativeUnit` de quart ordre, es localitza el municipi assignat i es comprova que la capa utilitzada declara `EPSG:4258`. Tampoc no es transforma encara: la diferència entre visualització al vol i reprojecció es resoldrà al capítol 03 abans de crear `municipality_cnig` en `EPSG:25831`.

El panell de capes es distribueix en grups que expressen funció, per exemple:

- `00_context`
- `10_originals_inspeccio`
- `20_preparades`
- `30_intermedies`
- `40_resultats`

Els prefixos són opcionals, però l'ordre no ha de dependre d'on ha quedat una capa després d'afegir-la. Les fonts remotes de context queden separades de les entrades analítiques i reben un nom que conserva productor i producte.

Abans de tancar la sessió, `pr1` ha de conservar el WMS de 2025, les dues fonts municipals encara sense harmonitzar i els grups inicials. Cal desar el projecte al GeoPackage, tancar-lo i tornar-lo a obrir explícitament des de `sandbox/pr1-fonts-cognom.gpkg`. El resultat del capítol és un estat de treball, no un lliurament: `dist` ha de continuar buit fins que les capes, el CRS i la composició s'hagin validat al capítol següent.

## El diari d'activitats

El diari ha de permetre entendre les decisions que no són visibles a les capes finals. No és una transcripció de cada clic. Una entrada útil relaciona objectiu, font, operació, paràmetres, incidència, control i interpretació. Una captura només s'hi incorpora quan prova una configuració, un error, una correcció o un resultat que no queda prou documentat d'una altra manera.

::: table "Contingut mínim d'una entrada del diari"
| Element | Pregunta que ha de respondre |
| --- | --- |
| Objectiu | Què es vol obtenir o comprovar? |
| Entrades | Quines capes, taules, bandes o seleccions s'han utilitzat? |
| Operació | Quin algorisme o transformació s'ha executat? |
| Paràmetres | Quins camps, distàncies, CRS, resolucions o llindars s'han fixat? |
| Incidències | Què no ha funcionat o ha produït un resultat inesperat? |
| Controls | Quins recomptes, mesures o contrastos confirmen el resultat? |
| Interpretació | Què permet afirmar la sortida i quina limitació conserva? |
| Fitxers | On s'han desat les entrades preparades i les sortides? |
:::

La versió de QGIS i els proveïdors de Processament s'han d'indicar quan poden alterar un algorisme o els seus paràmetres. També cal registrar els complements imprescindibles. Un projecte que depèn d'una selecció activa, una variable local o una capa temporal no documentades pot deixar de ser reproduïble encara que el fitxer `.qgz` s'obri.

Una entrada de qualitat comença per una decisió o una operació identificable, no per l'hora en què s'ha premut un botó. Pot indicar: objectiu de preparar el límit municipal; font ICGC o CNIG identificada; criteri aplicat al camp documentat; operació i paràmetres; sortida `municipality_icgc_5k` o `municipality_cnig`; controls de geometria, camps, CRS i extensió; i incidències. Aquesta estructura permet repetir el procés en una interfície lleugerament diferent perquè conserva el significat, no només el recorregut visual.

Una nota com «he retallat i ha sortit bé» no identifica entrada, màscara, opció ni prova. Una seqüència de captures de tots els diàlegs pot ser igualment insuficient si no explica per què s'han triat els valors. Les captures són útils quan demostren una configuració difícil de transcriure, un missatge d'error, una diferència abans-després o un control espacial. La resta es documenta millor com a text amb noms literals de capes, camps i paràmetres.

Els controls s'han d'escriure amb resultat, no només com a intenció. «Comprovar els nuls» és una tasca pendent; una entrada vàlida incorpora el recompte real, la capa i el camp examinats i la decisió adoptada. El manual no pot anticipar aquestes xifres perquè dependran del producte i de la versió descarregats. El diari ha de distingir el resultat esperat de l'observat quan no coincideixen.

Les incidències no són una confessió d'errors personals, sinó informació metodològica. Si una unió falla perquè una clau ha perdut zeros inicials, cal descriure el diagnòstic, la correcció del tipus i la repetició del control. Si una capa remota no respon, cal indicar si el document de capacitats era accessible i si es va utilitzar una còpia local autoritzada. Ometre el primer intent faria incomprensible una transformació que sí que apareix a la sortida final.

El diari també ha de distingir decisió i estat accidental. La capa activa, una selecció temporal, l'extensió actual del llenç o l'ordre d'obertura no són paràmetres reproduïbles si no es materialitzen o es documenten. Quan un algorisme utilitza «només els objectes seleccionats», cal conservar el criteri de selecció i el seu recompte observat. Quan una sortida és temporal, s'ha de desar abans que alimenti una altra fase o declarar que era una prova descartada.

## Diagnòstic de fonts i prova de transport

El diagnòstic de fonts ja és aplicable a l'estat de treball d'aquest capítol. La prova de transport, en canvi, es descriu com el protocol que s'executarà després de crear els dos fitxers de `dist` al final del capítol 03; no forma part encara de la primera fase de la micropràctica.

Una font trencada és un símptoma, no un diagnòstic. QGIS pot no trobar un fitxer, no reconèixer-ne el proveïdor, perdre una taula interna, no tenir permisos, rebre una resposta remota invàlida o obrir les dades en una posició inesperada. Cada causa exigeix una comprovació diferent. Canviar el CRS del projecte, tornar a instal·lar un connector o crear una capa duplicada pot ocultar el missatge sense restaurar la dependència original.

### Diagnosticar una font local

Quan QGIS mostra el gestor de capes no disponibles, el primer pas és conservar el nom de la capa i llegir l'adreça que esperava. Després cal comprovar al sistema de fitxers si el recurs existeix, si el nom coincideix exactament, incloses majúscules i minúscules en sistemes que les distingeixen, i si hi ha permisos de lectura. Si el projecte s'ha mogut, s'ha de comparar l'arbre real amb la ruta registrada abans de cercar còpies a tot l'ordinador.

En un conjunt multifitxer cal verificar totes les peces. Un `.shp` sense el seu índex o la taula associada no es repara indicant només un camí nou. En un GeoPackage, el fitxer pot existir i haver perdut o reanomenat la taula interna; la URI de la font identifica totes dues coses. En un CSV, una ruta correcta pot continuar produint una capa incorrecta si han canviat delimitador, codificació, camps de coordenades o definició del CRS.

La reparació ha d'apuntar la capa existent a la còpia correcta mitjançant l'opció de canviar o reparar la font. Afegir el mateix fitxer com una capa nova pot perdre estils, filtres, unions i referències de composició associades a l'anterior. Després de reparar s'han de revisar el proveïdor, la capa interna, el tipus geomètric, el CRS, els camps i els recomptes documentats. Que desaparegui la icona d'error només prova que QGIS ha pogut obrir alguna cosa.

Una capa que s'obre lluny de l'àmbit no és necessàriament una ruta trencada. Cal inspeccionar extensió i CRS declarats, i contrastar-los amb les metadades. Assignar un CRS diferent perquè el dibuix coincideixi visualment altera la interpretació de les coordenades i pot convertir un problema de referenciació en un error silenciós. El diagnòstic del CRS es desenvolupa al capítol següent, però la regla de conservació ja és aplicable: no es modifica l'original per fer-lo encaixar.

### Diagnosticar una font remota

En una capa WMS, WMTS o WFS cal separar el projecte de la connexió. Primer es prova l'adreça oficial o `GetCapabilities` fora de la capa, amb el navegador o amb la connexió del gestor de fonts. Si no respon, s'han de revisar connectivitat, certificat, servidor, proxy, autenticació i possible canvi d'adreça. Si respon, cal comprovar que la capa, la versió, el CRS i el format continuen anunciats.

Una imatge que no es dibuixa pot ser conseqüència de l'escala de visibilitat, l'extensió, un estil o un format, no d'una caiguda del servei. Un WFS pot retornar una capa buida perquè el filtre o l'extensió no contenen objectes, o pot truncar resultats segons els límits publicats. El registre de missatges de QGIS i les propietats de la font ajuden a distingir una resposta buida d'una petició fallida.

La memòria cau pot confondre la prova. Una tessel·la vista anteriorment pot continuar apareixent encara que el servidor no respongui; a l'inrevés, una resposta antiga pot persistir després d'una actualització. Cal fer la comprovació en una zona o escala no consultades, o aplicar el procediment de renovació adequat, abans de concloure que la connexió és actual. La memòria cau millora la navegació, però no és l'original ni una còpia de preservació.

Si una font remota és imprescindible per a l'anàlisi, el projecte ha d'explicar què passa quan no està disponible. Pot existir una extracció local autoritzada, una instrucció per repetir la consulta o una limitació que impedeixi el treball fora de línia. Un mapa base de context pot quedar temporalment absent sense invalidar els vectors analítics; una capa WFS utilitzada directament en un model pot impedir reproduir tot el resultat. Aquesta diferència s'ha de fer visible al diari.

### Protocol de prova de transport

Després de completar el capítol 03, la prova de transport crearà una situació en què les rutes personals deixin de funcionar. Amb QGIS tancat i els fitxers desats, els dos fitxers de `dist` es copiaran a una ubicació que no comparteixi el mateix camí, per exemple una carpeta temporal amb un altre nom o un altre equip. No s'ha de moure l'única còpia de treball ni esborrar l'origen per fer la prova.

Des de la còpia s'obre explícitament el projecte extern `pr1-fonts-cognom.qgz`, no un projecte de la llista de recents que podria apuntar a l'original. Abans d'acceptar cap reparació automàtica, s'observa si apareixen fonts no disponibles. Després es comproven els grups, la visibilitat, els estils, les etiquetes i la composició. Cada capa local s'ha de relacionar amb `pr1-fonts-cognom.gpkg` de la mateixa còpia, no amb `sandbox`, `Descàrregues` o l'escriptori.

Un cop registrada la prova del `.qgz`, es tanca sense introduir canvis i s'utilitza **Obre des de GeoPackage** sobre `pr1-fonts-cognom.gpkg` de la còpia. Se selecciona l'entrada `pr1` i es repeteixen els controls: fonts resoltes, grups, CRS, extensió, recomptes i composició. Aquesta segona obertura prova la instantània incrustada inclosa al lliurable, no la còpia de treball de `sandbox`, i no actualitza el projecte extern.

La validació utilitza els controls ja registrats. Les capes han de conservar els noms, tipus, CRS, camps i recomptes observats durant la preparació; els ràsters, les dimensions, bandes, resolució i `NoData` que corresponguin; i les composicions, els recursos necessaris. No s'introdueixen xifres de referència inventades: es comparen els valors de la prova amb els que el mateix projecte va documentar quan va crear les sortides.

Les fonts remotes es proven separadament. Amb connexió, cal confirmar que el servei encara respon i que el projecte n'identifica la dependència. Sense connexió, cal observar quina part del projecte continua disponible. L'objectiu no és que un WMS funcioni fora de línia, sinó que la seva absència no es confongui amb la pèrdua d'una entrada local i que cap anàlisi presentada com a reproduïble depengui d'una resposta efímera no documentada.

Una prova superada deixa una evidència breu: ubicació de la còpia, `.qgz` lliurable obert, entrada incrustada `pr1` oberta per separat, fonts resoltes, controls comparats, dependències remotes i incidències corregides. Si ha calgut cercar manualment una capa, si s'ha obert una font de l'arrel original o si no es pot identificar quina representació s'està comprovant, la prova no s'ha superat. Cal corregir la font canònica a `sandbox`, regenerar la fita afectada i les descendents, crear una còpia de prova nova i repetir totes dues obertures.

## Dos projectes organitzats de manera diferent

Un cas deficient pot semblar funcional a l'equip on s'ha creat. El `.qgz` és a l'escriptori; un límit municipal apunta a `Descàrregues`; el Shapefile s'ha separat del paquet; un ràster és en una memòria externa; i `final.gpkg` conté `capa1`, `capa1_nova` i `definitiva`. El WMS cadastral s'ha tractat com si fos la capa de parcel·les analítica. El diari conté captures dels menús, però no la versió, els filtres, les fonts ni els controls. Finalment, tota la carpeta s'ha comprimit al mateix disc i s'ha anomenat còpia de seguretat.

El projecte pot obrir-se perquè les rutes absolutes encara existeixen i perquè la memòria cau conserva el fons. No obstant això, no es pot saber quina capa interna sosté el resultat, no hi ha una còpia original íntegra i el paquet no inclou totes les dependències. Configurar rutes relatives en aquest moment no copiarà el contingut de `Descàrregues` ni la memòria externa. Reanomenar `definitiva` com `resultat_final` tampoc no reconstruirà el llinatge.

La resolució comença inventariant les fonts efectivament utilitzades. Els paquets originals autoritzats es tornen a obtenir o es recuperen íntegres i es desen a `data/raw`; les extraccions es mantenen separades. El GeoPackage de `sandbox` rep les capes de treball, i els ràsters analítics es copien dins de l'arbre si la llicència i la mida ho permeten. Una preparació només passa a `data/processed` si s'ha de reutilitzar en diversos exercicis. Cada capa interna rep un nom funcional i es relaciona amb l'original i l'operació que l'ha produïda. El WMS queda al grup de context, mentre que les parcel·les vectorials s'obtenen per una via adequada i documentada.

A continuació es repara cada font del projecte perquè no es perdin estils i composicions, es configuren els camins relatius i es tanquen les capes temporals o duplicades. El diari substitueix la cronologia de clics per entrades amb objectiu, entrades, operació, paràmetres, controls i incidències. Es crea una còpia de seguretat independent i es fa la prova de transport amb una còpia neta dels fitxers de `dist`. Només després d'aquesta prova el projecte es pot considerar reorganitzat.

En un cas ben dissenyat des de l'inici, totes les fonts locals pengen de `tig/`. Els paquets rebuts no es modifiquen; el GeoPackage concentra les capes locals de la pràctica i conserva el projecte incrustat `pr1`; els ràsters analítics tenen fitxers propis; els intermedis conservats expliquen dependències reals; i els lliurables no comparteixen noms amb proves descartades. Les capes remotes estan agrupades i documentades com a context o com a consultes reproduïbles.

La qualitat del cas ben organitzat no prové només de l'arbre. Cada sortida té una procedència, un esquema i controls; el `.qgz` i el projecte incrustat es tornen a obrir per separat després de copiar-los; `dist` exclou allò que no es pot redistribuir; i una còpia de recuperació existeix fora de la ubicació de treball. Si una font falla, el diari permet identificar quin resultat queda afectat i decidir si cal restaurar, reparar o repetir una operació.

## Validació i síntesi

Validar no és només observar que el mapa «té bona forma». Els controls s'han de definir segons l'operació: recomptes abans i després d'una unió, àrees després d'un retall, valors mínims i màxims d'un ràster, nombre d'errors topològics o contrast manual d'una mostra d'entitats. Els controls numèrics i la inspecció espacial es complementen.

La **síntesi** selecciona les evidències que responen la pregunta i les presenta amb el context necessari. Un mapa final ha d'indicar què representa, de quin període són les dades, quines unitats utilitza i quines fonts l'han fet possible. L'escala, l'orientació, la llegenda i altres elements s'incorporen quan ajuden a interpretar el producte, no com una llista decorativa obligatòria.

La conclusió ha de mantenir la diferència entre observació i inferència. Una àrea d'influència (`buffer`) de 200 m mostra una proximitat euclidiana definida pel model; no demostra que el recorregut sigui accessible. Una zona que compleix tres màscares és candidata segons els criteris introduïts; no és automàticament la millor localització. Documentar aquestes limitacions forma part del resultat.

## Activitats

### Inici de la micropràctica 1

La primera micropràctica comença en aquest capítol i acaba al final del capítol 03. Vila-seca serveix com a demostració; cada projecte s'ha d'aplicar al municipi assignat. En aquesta primera fase es prepara l'estructura, les fonts i el projecte de treball, però encara no es crea cap fitxer de lliurament.

::: table "Contracte de la primera fase de la micropràctica 1"
| Component | Requisit |
| --- | --- |
| Entrades | Ortofoto Territorial de 2025 de l'ICGC, divisions administratives 1:5.000 accessibles amb Open ICGC i distribució GML actual de les unitats administratives del CNIG per al municipi assignat |
| Operacions mínimes | Crear l'arbre `tig/`; iniciar un projecte en `EPSG:25831`; crear `sandbox/pr1-fonts-cognom.gpkg` i desar-hi `pr1`; afegir el WMS; localitzar i seleccionar el municipi a la font ICGC; descarregar, conservar i inspeccionar `LINEAS_LIMITE_GML.ZIP` i la capa `AdministrativeUnit` municipal |
| Estat al final del capítol | Projecte incrustat `pr1` reobert des del GeoPackage, WMS de 2025 visible, dues fonts municipals identificades i `dist` encara buit |
| Evidències del diari | Productor, producte, data, via d'accés, criteri de selecció municipal, CRS declarat per cada font, contingut del paquet CNIG i incidències observades |
| Comprovacions | Projecte en `EPSG:25831`; ortofoto identificada com a WMS; una única entitat municipal localitzada a cada font; capa `AdministrativeUnit` del GML en `EPSG:4258`; originals intactes a `data/raw` |
| Fitxers que cal conservar | `sandbox/pr1-fonts-cognom.gpkg`, paquet i extracció íntegra del CNIG a `data/raw`, `README.md` i diari actualitzat |
:::

En acabar aquesta fase no s'ha de copiar res a `dist`. Les seleccions i els CRS encara s'han d'interpretar amb els conceptes del capítol següent. El punt de continuïtat és `pr1` obert des de `sandbox/pr1-fonts-cognom.gpkg`, amb les fonts localitzades i els criteris necessaris per materialitzar les dues capes municipals sense alterar els originals.
