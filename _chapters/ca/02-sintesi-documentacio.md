---
layout: manual-chapter
title: Organització i documentació d'un projecte SIG
description: Organització, traçabilitat, comprovació i comunicació d'un projecte geogràfic reproduïble.
lang: ca
ref: manual-gis-project-documentation
profiles: [unaltremanual]
content_status: draft
permalink: /ca/chapters/sintesi-documentacio/
weight: 30
part: Continguts
manual_references: true
---

Un projecte SIG no és només el fitxer que QGIS obre. També inclou la pregunta, les dades originals, les transformacions, els paràmetres, els resultats i les decisions que permeten interpretar-los. Si una capa final no es pot relacionar amb una font i un procediment, el mapa pot semblar plausible però no constitueix una evidència verificable.

Aquest capítol crea per primera vegada la base del **projecte QGIS acumulatiu**: el fitxer extern `projecte_tig.qgz`, el GeoPackage `dades_preparades/projecte_tig.gpkg` i la capa canònica `municipi_treball`. Els capítols posteriors reobriran i ampliaran aquestes mateixes peces; no les recrearan en un projecte paral·lel. La còpia de treball canònica serà el `.qgz`; el GeoPackage concentrarà les capes vectorials i les taules quan sigui adequat i contindrà, en punts de control explícits, una representació incrustada del mateix projecte amb el nom `projecte_tig`. Els ràsters analítics es conservaran habitualment com a GeoTIFF i el **diari d'activitats** relacionarà totes les peces.

>>>>> En acabar el capítol, cal poder preparar un projecte SIG transportable i explicar el recorregut complet des de les fonts fins als resultats.
>>>>>
>>>>> - Separar dades originals, preparades, resultats intermedis i resultats finals.
>>>>> - Crear `municipi_treball`, mantenir el `.qgz` canònic i actualitzar una representació incrustada identificable del mateix punt de control.
>>>>> - Documentar fonts, operacions, paràmetres, controls, incidències i limitacions.
>>>>> - Sintetitzar un resultat sense ocultar els supòsits ni la qualitat de les entrades.

El projecte extern i l'incrustat no se sincronitzen automàticament. Desar el `.qgz` no actualitza l'entrada del GeoPackage, i desar un projecte obert des del GeoPackage no modifica el `.qgz`. Aquesta independència permet conservar fites deliberades, però obliga a saber sempre quina representació està oberta i a actualitzar l'altra només després dels controls indicats.

Organitzar no és embellir una carpeta després d'acabar. L'estructura del sistema de fitxers expressa quines entrades s'han rebut, quines còpies es poden modificar, quines sortides encara són provisionals i quins resultats sostenen la conclusió. Si aquests estats només existeixen a la memòria de qui ha executat el treball, una altra persona no podrà saber si `final_2.gpkg` és una font, una prova o el resultat acceptat.

La documentació tampoc no es limita a descriure programari. Ha d'enllaçar una pregunta amb fonts identificades, operacions concretes, paràmetres, incidències, controls i interpretacions. El projecte acumulatiu creixerà durant tot el curs; una decisió feble en aquesta fase es propaga a les activitats següents. Per això la transportabilitat, el llinatge i la recuperació es proven des del primer conjunt de capes, no només abans del lliurament.

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

Separar l'estat de les dades evita confondre una font amb una transformació. La còpia original es conserva tal com s'ha rebut o descarregat. Les dades preparades corregeixen estructura, tipus, CRS o àmbit sense perdre la relació amb l'original. Els resultats intermedis permeten diagnosticar un flux, i els finals responen directament una pregunta o alimenten una composició.

Una estructura possible és la següent. Els directoris expressen l'estat lògic de les dades, mentre que el `.qgz`, el diari i el fitxer de presentació queden a l'arrel transportable.

![Arbre de directoris i fitxers del projecte acumulatiu]({{ site.baseurl }}/assets/diagrams/ca/02-sintesi-documentacio/project-folder-tree.puml "L'arrel projecte_tig separa originals, dades preparades, treball, resultats intermedis i resultats finals, i conserva el projecte QGIS, el diari i el README al primer nivell."){: data-figure-width-web="12.5rem" data-figure-width-pdf="30%"}

L'arbre és orientatiu, però les funcions no són intercanviables. `dades_originals` conserva allò que s'ha rebut del productor: els paquets i, quan cal obrir-los, una extracció íntegra que no s'edita. `dades_preparades` conté còpies que ja han passat per decisions com seleccionar camps, corregir tipus, retallar l'àmbit o materialitzar un CRS. `treball` admet proves que encara es poden descartar. `resultats_intermedis` conserva sortides necessàries per explicar o repetir una cadena, i `resultats` queda reservat per als productes validats que responen la pregunta.

La separació descriu **estats lògics**, no formats. Un GeoPackage pot contenir una capa preparada, una intermèdia i una final, però els noms interns han d'indicar-ne la funció. Un GeoTIFF pot ser una font original o un resultat. Desar tots els vectors en un únic contenidor redueix el nombre de fitxers, però no converteix automàticament totes les capes en una mateixa fase del procés.

La carpeta `treball` no ha de convertir-se en un abocador permanent. Una prova que no intervé en cap resultat es pot eliminar després de documentar la decisió que se n'ha extret. Una sortida intermèdia que permet comprovar una incidència o evita repetir una operació costosa s'ha de conservar amb un nom i un antecedent clars. La decisió depèn de la possibilitat de reconstrucció, no d'una regla segons la qual cal guardar-ho tot.

Les capes temporals de QGIS exigeixen una decisió explícita. Mentre només són resultats temporals, poden desaparèixer en tancar la sessió i no són una evidència persistent. Si una selecció o una transformació alimentarà una activitat posterior, s'ha de desar a `dades_preparades`, `resultats_intermedis` o `resultats` segons la funció. El diàleg de processament no pot decidir aquesta categoria a partir del nom de l'algorisme.

No totes les capes necessiten un fitxer separat. Un únic `projecte_tig.gpkg` pot contenir capes vectorials, taules i resultats relacionats, amb noms que indiquin funció i no només l'ordre accidental de creació. Els noms `municipis_font`, `municipis_preparats` i `municipis_pendent` expliquen millor el recorregut que `capa1`, `final2` o `nova_definitiva`.

Els noms han de ser estables, breus i compatibles amb les eines utilitzades. Convé usar minúscules, guions baixos i unitats explícites quan siguin necessàries, com `vies_buffer_200m`. Les dates formen part del nom només quan distingeixen versions reals de les dades o del resultat; no substitueixen un registre de canvis.

### Noms, identificadors i esquemes

Un projecte combina almenys tres espais de noms: fitxers del sistema operatiu, capes dins d'un contenidor i camps dins d'una taula. `projecte_tig.gpkg` identifica el contenidor i `codi_muni`, un camp. Una taula o capa interna pot anomenar-se `municipis_preparats`. Repetir `projecte_tig` a cada capa no aporta informació, mentre que usar `capa1` impedeix entendre-la fora de l'ordre del panell.

Els sistemes moderns admeten habitualment Unicode i espais, de manera que no és correcte afirmar que qualsevol accent farà fallar QGIS. Tanmateix, un patró conservador amb minúscules, caràcters ASCII i guions baixos redueix friccions quan els noms passen per SQL, scripts, eines antigues, sistemes operatius diferents o ordres de terminal. La regla s'aplica sobretot als identificadors tècnics; el títol visible d'una capa o d'un mapa pot conservar la llengua i els accents necessaris.

Un bon nom expressa contingut i funció sense intentar codificar tot el llinatge. Per exemple, `carreteres_retallades` és més informatiu que `resultat3`.

`carreteres_retallades_cnig_2026_epsg25831_v2_definitiu` és un nom excessiu: acumula dades que pertanyen a les metadades i al diari. Les dates només s'afegeixen quan separen períodes reals del fenomen o versions que han de coexistir. Paraules com `nou`, `bo`, `final` o `definitiu2` depenen d'un moment i perden significat tan aviat com hi ha una revisió.

L'**esquema** defineix què significa cada fila i cada camp. Per a una capa preparada s'han de conservar el tipus geomètric, el CRS, l'identificador estable, els noms i tipus dels camps, les unitats, els dominis, el tractament dels nuls i les relacions amb altres taules. Canviar `codi_muni` de text a enter pot eliminar zeros inicials; convertir un nul en zero pot inventar una observació. Aquestes decisions no queden explicades pel nom del fitxer.

El `README.md` o el diari pot actuar com a diccionari d'esquema per a les capes centrals. No cal descriure camps auxiliars que no s'utilitzen, però sí els que intervenen en filtres, unions, càlculs, simbologia o interpretació. Quan es crea un camp derivat, cal indicar l'expressió, la unitat, les entrades i el significat. La taula final ha de poder llegir-se sense deduir les unitats a partir dels valors.

### Paquets comprimits i còpies originals

Moltes fonts distribueixen diversos fitxers dins d'un `.zip`, `.7z` o altre contenidor comprimit. El paquet és una unitat de distribució, no necessàriament una capa que s'hagi d'editar o obrir directament. Cal conservar-lo a `dades_originals/paquets` amb el nom rebut i extreure'n el contingut complet a una subcarpeta identificable de `dades_originals/extrets`. Si el productor publica una suma de comprovació, es pot utilitzar per confirmar que la baixada no s'ha alterat.

L'extracció completa és important en formats compostos per diverses peces. Un Shapefile necessita, com a mínim, els fitxers que conserven geometria, índex i atributs, i pot dependre també del CRS i la codificació. Copiar només el `.shp` trenca el conjunt. Altres paquets inclouen metadades, llicències, estils, índexs o diversos fulls territorials; seleccionar-ne una peça abans de llegir l'inventari pot eliminar informació necessària per interpretar-la.

Algunes aplicacions poden llegir determinats recursos dins d'un comprimit, però aquesta capacitat no s'ha de convertir en la base del projecte acumulatiu. Una ruta virtual a l'interior d'un `.zip` pot no funcionar igual en totes les eines i dificulta inspeccionar què s'ha extret. La còpia de treball s'ha de crear després d'obrir i validar l'original, no modificant fitxers dins del paquet ni descomprimint versions diferents a la mateixa carpeta.

Descomprimir no és preparar les dades. Els fitxers extrets continuen sent originals del projecte mentre es mantenen sense canvis. Si cal reanomenar camps, transformar el CRS, reparar geometries o retallar l'àmbit, la sortida es desa a `dades_preparades` i el diari relaciona les dues versions. Aquesta disciplina permet tornar a començar quan una preparació era incorrecta sense repetir la descàrrega ni perdre la font.

Abans de donar el paquet per bo s'ha de verificar que s'obre sense errors, que el contingut coincideix amb l'inventari del productor i que no hi ha una carpeta ni un arxiu inesperadament buits. També cal conservar la URL, la data d'accés i les condicions de redistribució. Incloure el `.zip` original al projecte de treball no significa que es pugui incloure al paquet final si la llicència no ho autoritza.

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

Desar el projecte aviat fixa un punt de referència per a les rutes i evita acumular capes en un projecte sense nom. El nom estable `projecte_tig.qgz` identifica la còpia canònica i la continuïtat acumulativa: és el fitxer que s'obre per reprendre el treball i el que es desa abans de crear una fita incrustada. Els canvis rellevants es documenten al diari o amb còpies de control deliberades, no amb una cadena de `projecte_final_final2.qgz`.

El projecte conserva estils, filtres, unions i composicions que poden canviar el significat de la vista sense canviar les dades. Una capa oculta per un filtre no està buida; una unió dinàmica pot desaparèixer si falta la taula externa; un disseny pot dependre d'una imatge o una tipografia que no viatja amb la font geogràfica. La prova de transport ha d'incloure aquestes dependències i no només comprovar que el llenç mostra algun mapa.

### Rutes relatives i absolutes

Les **rutes relatives** descriuen la posició d'un fitxer respecte del projecte i permeten moure conjuntament la carpeta. Les rutes absolutes depenen d'una unitat, un nom d'usuari o una jerarquia concreta. Després de configurar les rutes relatives cal traslladar una còpia de la carpeta a una ubicació diferent, obrir el `.qgz` i comprovar que totes les fonts continuen resolent-se.

A Windows, `C:\Users\anna\projecte_tig\dades_preparades\projecte_tig.gpkg` és una ruta absoluta.

En GNU/Linux, `/home/anna/projecte_tig/dades_preparades/projecte_tig.gpkg` també és una ruta absoluta. Pot ser correcta a l'equip d'origen i inexistent en un altre sistema. Una ruta relativa expressa la relació dins de l'arbre, com `dades_preparades/projecte_tig.gpkg`; mentre el `.qgz` i la carpeta es moguin junts mantenint la jerarquia, la relació es conserva.

Els segments `.` i `..` signifiquen, respectivament, la carpeta actual i la carpeta superior. Són útils per entendre la lògica, però una acumulació de `../../..` sol indicar que les dades han quedat fora de l'arrel transportable. La solució no és memoritzar el camí, sinó reunir dins d'un arbre comú les dependències que es poden copiar legalment. Un recurs compartit en una unitat de xarxa pot justificar una ruta absoluta en un entorn controlat, però aquesta decisió i el requisit de muntatge s'han de documentar.

QGIS permet definir si desa els camins de les fonts com a relatius o absoluts a les propietats generals del projecte. En un projecte desat com a `.qgz`, la ruta relativa es calcula respecte del fitxer de projecte. La `Carpeta inicial del projecte` és l'accés de conveniència que mostra l'`Explorador`: per defecte coincideix amb la carpeta del `.qgz`, però es pot canviar sense rebasar les rutes de les fonts. Per això cal desar primer el `.qgz`, configurar els camins relatius i tornar a afegir o revisar qualsevol capa carregada abans. Canviar l'opció no copia fitxers externs dins de l'arbre ni repara automàticament una font que ja no existeix {% cite qgisUserGuide344 %}.

Les URL de WMS, WMTS, WFS o API no es converteixen en rutes locals relatives. Continuen depenent de xarxa, servidor i, si escau, autenticació. Tampoc no és segur compartir credencials dins del projecte. La transportabilitat ha de distingir capes locals que viatgen amb la carpeta, recursos remots que s'han de tornar a consultar i fonts restringides que cada usuari ha de configurar amb permisos propis.

Una ruta relativa només resol la **localització**. No resol llicències, formats no admesos, extensions de base de dades, tipografies absents, diferències de versió ni dependències de complements. Per això el projecte ha d'indicar la versió de QGIS quan sigui rellevant i sotmetre's a una obertura real en una ubicació neta. Veure la paraula «relatiu» al diàleg és una configuració; obrir totes les fonts després del trasllat és l'evidència.

### Abast del GeoPackage i projecte incrustat

GeoPackage és un estàndard OGC basat en SQLite. Pot contenir diverses taules d'entitats vectorials, taules d'atributs i piràmides de tessel·les, juntament amb metadades i extensions definides segons el cas {% cite ogcGeoPackage2024 %}. Aquesta capacitat el fa adequat per concentrar vectors i taules relacionats sense dispersar-los en molts fitxers. Cada capa continua tenint nom, geometria, CRS, esquema i llinatge propis.

No és una carpeta comprimida d'ús general. Un GeoTIFF analític, un `.zip` original o el PDF del diari no esdevenen capes interoperables pel fet d'introduir-los en una base. Encara que GeoPackage admet tessel·les ràster, això no equival a conservar qualsevol ràster analític de coma flotant amb la mateixa compatibilitat que un GeoTIFF. El projecte del curs mantindrà habitualment aquests ràsters com a fitxers externs dins de l'arbre.

QGIS permet **desar un projecte a un GeoPackage** i **obrir-lo des d'un GeoPackage** mitjançant les accions `Projecte > Desa a > GeoPackage` (*Save to GeoPackage*) i `Projecte > Obre des de > GeoPackage` (*Open from GeoPackage*), encara que la traducció o la posició exacta puguin variar entre versions. En tots dos casos se seleccionen un contenidor i un nom de projecte; no s'estan important o exportant les capes. Altres aplicacions poden llegir les taules geogràfiques i ignorar aquesta definició pròpia de QGIS {% cite qgisUserGuide344 %}.

Al curs, l'entrada incrustada s'anomena exactament `projecte_tig`. Per crear o renovar un punt de control, s'obre el `projecte_tig.qgz` extern, es desen els canvis canònics, s'executen els controls previstos i només aleshores es desa una representació d'aquell estat al GeoPackage amb aquest nom. Després es tanca la representació incrustada i es torna a obrir explícitament el `.qgz` abans de continuar treballant. Així s'evita que una ordre **Desa** posterior actualitzi només l'entrada incrustada per error.

Les dues representacions són independents. L'ordre **Desa** actualitza la que està oberta en aquell moment; no hi ha cap enllaç que propagui els canvis a l'altra. La data de la fita i els controls que la justifiquen han de quedar al diari. Una diferència posterior pot ser correcta si el `.qgz` ha avançat des de l'última fita, però ha de ser explicable.

El projecte incrustat **no és una còpia de seguretat**. Comparteix el mateix fitxer `projecte_tig.gpkg` que les capes: si el contenidor es perd o es corromp, es poden perdre alhora les dades i el projecte incrustat. Una còpia de recuperació ha d'estar en una ubicació independent i incloure també el `.qgz`, els ràsters i la documentació necessaris.

Els noms interns també s'han de gestionar. Esborrar o reanomenar una taula pot trencar tant la referència del `.qgz` com la de la fita incrustada; reemplaçar una capa amb una altra del mateix nom pot ocultar un canvi d'esquema. Després d'una importació s'han de revisar geometria, CRS, camps i recomptes, i després tornar a obrir totes dues representacions des d'una còpia del projecte. El contenidor simplifica el transport físic, no la validació del contingut.

>>>> **Ni el projecte incrustat ni un `.zip` substitueixen una còpia de seguretat independent.** Tots dos poden facilitar una fita o un lliurament, però no protegeixen per si sols contra la pèrdua del contenidor o de l'única ubicació de treball.

### Còpies de seguretat i control de versions

Còpia de seguretat
: Permet recuperar fitxers després d'una supressió, una avaria o una corrupció. Ha d'existir en una ubicació independent de la còpia de treball i s'ha de provar restaurant-ne contingut.

Control de versions
: Conserva canvis identificats i permet relacionar-los amb una decisió. És especialment útil per al `README.md`, el diari editable, les consultes, els scripts, els models i altres fonts textuals.

Una carpeta sincronitzada pot replicar també una supressió o un fitxer malmès; una còpia al mateix disc no protegeix contra la fallada del disc. Git pot guardar `.qgz`, `.gpkg` o GeoTIFF binaris, però no en pot comparar ni fusionar l'estructura interna com fa amb línies de text. Per això el control de versions no substitueix una còpia de seguretat ni resol automàticament la gestió de totes les geodades.

En un projecte docent es poden combinar còpies de recuperació del conjunt amb fites deliberades dels fitxers centrals. Abans d'una transformació difícil de revertir es crea una còpia tancada del GeoPackage; després es registra al diari què s'ha canviat i quin resultat s'ha validat. No cal conservar una còpia amb marca horària de cada clic. Cal conservar prou estats per recuperar-se i prou documentació per saber quin estat és coherent.

El paquet `.zip` del lliurament és una **còpia de distribució**. Pot servir també per fer la prova de transport, però no és l'única còpia de seguretat ni l'historial de treball. Abans de comprimir s'han d'excloure memòries cau, temporals, credencials i originals que no es puguin redistribuir; després s'ha d'extreure el paquet en una carpeta nova i obrir-ne el contingut. Que la compressió acabi sense error no prova que el projecte sigui complet.

::: table "Cinc registres o còpies que no s'han de confondre"
| Peça | Funció | Prova necessària |
| --- | --- | --- |
| Inventari | Descriu les peces, la ubicació, la funció i les dependències de l'estat actual | Cada entrada existeix i es pot relacionar amb el projecte |
| Diari | Registra decisions, execucions, incidències, controls i interpretacions | Una altra persona pot reconstruir per què s'ha acceptat cada resultat |
| Punt de control | Identifica un estat validat i coherent del `.qgz` extern i de la seva representació incrustada | Les dues representacions s'obren per separat i compleixen els mateixos controls declarats |
| Còpia de seguretat | Permet recuperar-se d'una pèrdua o corrupció | Es troba en una ubicació independent i se n'ha provat la restauració |
| Paquet de distribució o transport | Trasllada només les peces redistribuïbles necessàries | S'extreu en una ruta neta i s'obre sense dependre de la còpia original |
:::

### Configuració inicial a QGIS

En QGIS, la separació conceptual entre fonts, organització, representació i procés es tradueix en regions funcionals diferents: l'`Explorador` localitza fonts, el panell `Capes` les organitza, el llenç les representa, la caixa d'eines les transforma i la barra d'estat informa de l'escala, les coordenades i el CRS de la vista. La disposició concreta depèn de la versió i del perfil. La configuració ha de començar fora del llenç: primer es crea l'arbre del projecte i es desa `projecte_tig.qgz` a l'arrel.

>>> **Miniprojecte de Vila-seca.** Després de construir la base pròpia, es pot [descarregar el paquet de referència](https://geourv.github.io/tig/assets/projectes/vila-seca/projecte-tig-vila-seca.zip), extreure'l en una carpeta nova i comparar-ne l'organització i els controls. Inclou `municipi_treball`, el WMS PNOA de context, la representació incrustada `projecte_tig`, la procedència, les sumes SHA-256 i un constructor escrit amb la interfície Python de QGIS (PyQGIS) per publicar la demostració; l'estudiant no ha d'executar aquest constructor ni presentar Vila-seca com a resultat propi.

En obrir-lo, la captura permet relacionar cada decisió del projecte amb el lloc on es comprova: les dependències a l'`Explorador`, l'ordre al panell `Capes`, el resultat visible al llenç i els algorismes a la caixa d'eines.

![Interfície de QGIS amb l'Explorador i el panell de Capes a l'esquerra, el llenç del mapa al centre, la Caixa d'eines de processament a la dreta i la barra d'estat amb el localitzador a la part inferior]({{ site.baseurl }}/assets/img/qgis/qgis-interface-overview.png "Interfície de QGIS 3.44.11 en català. La posició i la visibilitat dels panells i de les barres d'eines poden variar segons la versió i el perfil; les regions funcionals es mantenen."){: data-figure-width-web="56rem" data-figure-width-pdf="100%"}

A `Projecte > Propietats > General` es configura l'emmagatzematge de camins relatius. També es revisa la `Carpeta inicial del projecte`, que pot apuntar a l'arrel per agilitzar la navegació, però no substitueix la carpeta del `.qgz` com a base de les rutes desades. Només llavors s'afegeixen les còpies preparades o els originals en mode d'inspecció, de manera que les referències neixen dins d'una estructura coneguda.

El GeoPackage inicial es pot crear des del panell `Explorador` o en desar la primera capa preparada. El contenidor es desa a `dades_preparades/projecte_tig.gpkg`. El paquet del límit municipal candidat del CNIG es conserva íntegre a `dades_originals`; després de comprovar-ne peces, metadades, CRS, camps i cobertura, la selecció del municipi assignat s'importa al GeoPackage amb el nom intern exacte `municipi_treball`. La capa conserva l'identificador oficial rebut, un `codi_muni` textual derivat amb una regla documentada, el nom, una sola entitat i un identificador intern estable. L'original no es reemplaça: la capa de treball i el diari conserven la relació amb la font.

El panell de capes es distribueix en grups que expressen funció, per exemple:

- `00_context`
- `10_originals_inspeccio`
- `20_preparades`
- `30_intermedies`
- `40_resultats`

Els prefixos són opcionals, però l'ordre no ha de dependre d'on ha quedat una capa després d'afegir-la. Les fonts remotes de context queden separades de les entrades analítiques i reben un nom que conserva productor i producte.

Abans de tancar la primera sessió, el `.qgz` ha de conservar el WMS de context, `municipi_treball` dins de `dades_preparades/projecte_tig.gpkg` i els grups inicials. Després de comprovar que cap resultat necessari continua sent temporal i documentar l'identificador oficial, `codi_muni`, els camps, el CRS, l'extensió, la geometria i el recompte observats, es crea la primera representació incrustada del punt de control amb el nom `projecte_tig`. QGIS es tanca i el `.qgz` canònic es torna a obrir explícitament; la prova de transport comprovarà després les dues representacions.

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

Una entrada de qualitat comença per una decisió o una operació identificable, no per l'hora en què s'ha premut un botó. Pot indicar: objectiu de preparar el límit municipal; entrada `municipis_font` procedent del paquet identificat; filtre aplicat al camp documentat; algorisme i paràmetres; sortida `municipi_treball`; controls de geometria, camps, CRS i extensió; i incidències. Aquesta estructura permet repetir el procés en una interfície lleugerament diferent perquè conserva el significat, no només el recorregut visual.

Una nota com «he retallat i ha sortit bé» no identifica entrada, màscara, opció ni prova. Una seqüència de captures de tots els diàlegs pot ser igualment insuficient si no explica per què s'han triat els valors. Les captures són útils quan demostren una configuració difícil de transcriure, un missatge d'error, una diferència abans-després o un control espacial. La resta es documenta millor com a text amb noms literals de capes, camps i paràmetres.

Els controls s'han d'escriure amb resultat, no només com a intenció. «Comprovar els nuls» és una tasca pendent; una entrada vàlida incorpora el recompte real, la capa i el camp examinats i la decisió adoptada. El manual no pot anticipar aquestes xifres perquè dependran del producte i de la versió descarregats. El diari ha de distingir el resultat esperat de l'observat quan no coincideixen.

Les incidències no són una confessió d'errors personals, sinó informació metodològica. Si una unió falla perquè una clau ha perdut zeros inicials, cal descriure el diagnòstic, la correcció del tipus i la repetició del control. Si una capa remota no respon, cal indicar si el document de capacitats era accessible i si es va utilitzar una còpia local autoritzada. Ometre el primer intent faria incomprensible una transformació que sí que apareix a la sortida final.

El diari també ha de distingir decisió i estat accidental. La capa activa, una selecció temporal, l'extensió actual del llenç o l'ordre d'obertura no són paràmetres reproduïbles si no es materialitzen o es documenten. Quan un algorisme utilitza «només els objectes seleccionats», cal conservar el criteri de selecció i el seu recompte observat. Quan una sortida és temporal, s'ha de desar abans que alimenti una altra fase o declarar que era una prova descartada.

## Diagnòstic de fonts i prova de transport

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

### Executar una prova de transport

La prova de transport crea una situació en què les rutes personals deixen de funcionar. Amb QGIS tancat i els fitxers desats, es copia l'arrel completa a una ubicació que no comparteixi el mateix camí, per exemple una carpeta temporal amb un altre nom o un altre equip. No s'ha de moure l'única còpia de treball ni esborrar l'origen per fer la prova. Si el lliurament serà un `.zip`, la còpia es comprimeix i s'extreu en aquesta ubicació neta.

Des de la còpia s'obre explícitament `projecte_tig.qgz`, no un projecte de la llista de recents que podria apuntar a l'original. Abans d'acceptar cap reparació automàtica, s'observa si apareixen fonts no disponibles. Després es comproven els grups, la visibilitat, els estils, les etiquetes, les unions, les relacions, els models i les composicions que formin part de l'activitat. Cada capa local s'ha de relacionar amb un fitxer o una taula interna de la còpia, no amb `Descàrregues`, l'escriptori o l'arrel anterior.

Un cop registrada la prova del `.qgz`, es tanca sense introduir canvis i s'utilitza **Obre des de GeoPackage** sobre el `projecte_tig.gpkg` de la còpia. Se selecciona l'entrada `projecte_tig` i es repeteixen els controls corresponents a la fita: fonts resoltes, grups, CRS, extensió, recompte i elements de projecte esperats. Aquesta segona obertura prova la fita incrustada; no la converteix en còpia canònica ni l'actualitza perquè coincideixi amb canvis posteriors del `.qgz`.

La validació utilitza els controls ja registrats. Les capes han de conservar els noms, tipus, CRS, camps i recomptes observats durant la preparació; els ràsters, les dimensions, bandes, resolució i `NoData` que corresponguin; i les composicions, els recursos necessaris. No s'introdueixen xifres de referència inventades: es comparen els valors de la prova amb els que el mateix projecte va documentar quan va crear les sortides.

Les fonts remotes es proven separadament. Amb connexió, cal confirmar que el servei encara respon i que el projecte n'identifica la dependència. Sense connexió, cal observar quina part del projecte continua disponible. L'objectiu no és que un WMS funcioni fora de línia, sinó que la seva absència no es confongui amb la pèrdua d'una entrada local i que cap anàlisi presentada com a reproduïble depengui d'una resposta efímera no documentada.

Una prova superada deixa una evidència breu: ubicació de la còpia, `.qgz` canònic obert, entrada incrustada `projecte_tig` oberta per separat, fonts resoltes, controls comparats, dependències remotes i incidències corregides. Si ha calgut cercar manualment una capa, si s'ha obert una font de l'arrel original o si no es pot identificar quina representació s'està comprovant, la prova no s'ha superat. Cal corregir l'arbre o la referència, renovar la fita si correspon, tornar a copiar i repetir totes dues obertures.

## Dos projectes organitzats de manera diferent

Un cas deficient pot semblar funcional a l'equip on s'ha creat. El `.qgz` és a l'escriptori; un límit municipal apunta a `Descàrregues`; el Shapefile s'ha separat del paquet; un ràster és en una memòria externa; i `final.gpkg` conté `capa1`, `capa1_nova` i `definitiva`. El WMS cadastral s'ha tractat com si fos la capa de parcel·les analítica. El diari conté captures dels menús, però no la versió, els filtres, les fonts ni els controls. Finalment, tota la carpeta s'ha comprimit al mateix disc i s'ha anomenat còpia de seguretat.

El projecte pot obrir-se perquè les rutes absolutes encara existeixen i perquè la memòria cau conserva el fons. No obstant això, no es pot saber quina capa interna sosté el resultat, no hi ha una còpia original íntegra i el paquet no inclou totes les dependències. Configurar rutes relatives en aquest moment no copiarà el contingut de `Descàrregues` ni la memòria externa. Reanomenar `definitiva` com `resultat_final` tampoc no reconstruirà el llinatge.

La resolució comença inventariant les fonts efectivament utilitzades. Els paquets originals autoritzats es tornen a obtenir o es recuperen íntegres i es desen a `dades_originals`; les extraccions es mantenen separades. El GeoPackage `dades_preparades/projecte_tig.gpkg` rep les capes de treball, i el ràster es copia dins de l'arbre si la llicència i la mida ho permeten. Cada capa interna rep un nom funcional i es relaciona amb l'original i l'operació que l'ha produïda. El WMS queda al grup de context, mentre que les parcel·les vectorials s'obtenen per una via adequada i documentada.

A continuació es repara cada font del `.qgz` existent perquè no es perdin estils i composicions, es configuren els camins relatius i es tanquen les capes temporals o duplicades. El diari substitueix la cronologia de clics per entrades amb objectiu, entrades, operació, paràmetres, controls i incidències. Es crea una còpia de seguretat independent i es fa la prova de transport des d'un `.zip` extret en una ubicació nova. Només després d'aquesta prova el projecte es pot considerar reorganitzat.

En un cas ben dissenyat des de l'inici, `projecte_tig.qgz` i totes les fonts locals pengen d'una mateixa arrel. Els paquets rebuts no es modifiquen; el GeoPackage concentra vectors i taules preparats i conserva la fita incrustada `projecte_tig`; els ràsters analítics tenen fitxers propis; els intermedis conservats expliquen dependències reals; i els resultats finals no comparteixen noms amb proves descartades. Les capes remotes estan agrupades i documentades com a context o com a consultes reproduïbles.

La qualitat del cas ben organitzat no prové només de l'arbre. Cada sortida té una procedència, un esquema i controls; el `.qgz` i la fita incrustada es tornen a obrir per separat després de copiar-los; el paquet de distribució exclou allò que no es pot redistribuir; i una còpia de recuperació existeix fora de la ubicació de treball. Si una font falla, el diari permet identificar quin resultat queda afectat i decidir si cal restaurar, reparar o repetir una operació.

## Validació i síntesi

Validar no és només observar que el mapa «té bona forma». Els controls s'han de definir segons l'operació: recomptes abans i després d'una unió, àrees després d'un retall, valors mínims i màxims d'un ràster, nombre d'errors topològics o contrast manual d'una mostra d'entitats. Els controls numèrics i la inspecció espacial es complementen.

La **síntesi** selecciona les evidències que responen la pregunta i les presenta amb el context necessari. Un mapa final ha d'indicar què representa, de quin període són les dades, quines unitats utilitza i quines fonts l'han fet possible. L'escala, l'orientació, la llegenda i altres elements s'incorporen quan ajuden a interpretar el producte, no com una llista decorativa obligatòria.

La conclusió ha de mantenir la diferència entre observació i inferència. Una àrea d'influència (`buffer`) de 200 m mostra una proximitat euclidiana definida pel model; no demostra que el recorregut sigui accessible. Una zona que compleix tres màscares és candidata segons els criteris introduïts; no és automàticament la millor localització. Documentar aquestes limitacions forma part del resultat.

## Activitats

### Informe de la prova de transport

El resultat conservat serà un informe breu de la còpia traslladada. Identificarà la ubicació neta, l'obertura explícita de `projecte_tig.qgz`, l'obertura separada de l'entrada `projecte_tig` mitjançant **Obre des de GeoPackage**, les fonts locals resoltes, les dependències remotes i els controls comparats. També explicarà per què una capa que encara apunti a una carpeta de descàrregues invalida la prova, encara que aparegui a l'equip d'origen.

### Micropràctica 1: projecte, pregunta i fonts

La primera micropràctica lliurable prepara la base que utilitzaran les activitats posteriors. El cas de Vila-seca serveix com a demostració; el lliurament s'ha d'adaptar al municipi assignat i a la disponibilitat real de dades.

::: table "Contracte de la micropràctica 1"
| Component | Requisit |
| --- | --- |
| Entrades | Pregunta territorial, inventari inicial, connexió WMS de context i candidatura del límit municipal oficial del CNIG per al municipi assignat |
| Operacions mínimes | Crear l'arbre, desar `projecte_tig.qgz`, obtenir i conservar íntegre el paquet del CNIG, validar i importar el límit com a `municipi_treball`, documentar les fonts i crear la representació incrustada `projecte_tig` |
| Resultats | WMS de context i `municipi_treball` visibles, `dades_preparades/projecte_tig.gpkg` amb una entitat municipal i la representació incrustada, `projecte_tig.qgz` canònic i inventari de fonts |
| Evidències del diari | Pregunta, unitat d'anàlisi, fitxa de cada font, contingut del paquet, arbre de fitxers, controls de `municipi_treball`, data del punt de control i informe de transport |
| Comprovacions | Identificador oficial conservat, `codi_muni` textual, CRS, extensió, geometria i recompte d'una entitat; rutes relatives; originals intactes; `.qgz` i entrada incrustada reoberts per separat des de la còpia |
| Fitxers que cal conservar | Paquet original autoritzat del CNIG, `projecte_tig.gpkg`, `projecte_tig.qgz`, inventari i diari actualitzat |
:::

El lliurament només es considera reproduïble si les dues representacions tornen a obrir-se des d'una ubicació diferent, si la comprovació identifica quina és la còpia canònica i si cada capa es pot relacionar amb una font, una data i una llicència. L'entrada incrustada no s'ha de presentar com a còpia de seguretat perquè comparteix el contenidor amb les dades. Moodle concretarà el format de tramesa i el termini.
