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

El projecte acumulatiu inclourà un **GeoPackage**, un projecte QGIS i un **diari d'activitats**. El GeoPackage concentrarà les capes vectorials i les taules quan sigui adequat; els ràsters analítics es conservaran habitualment com a GeoTIFF; i el fitxer `.qgz` registrarà l'organització de capes, estils, consultes, models i composicions. Cap d'aquestes peces substitueix les altres.

>>>>> En acabar el capítol, cal poder preparar un projecte SIG transportable i explicar el recorregut complet des de les fonts fins als resultats.
>>>>>
>>>>> - Separar dades originals, preparades, resultats intermedis i resultats finals.
>>>>> - Utilitzar noms i rutes que permetin traslladar el projecte a un altre equip.
>>>>> - Documentar fonts, operacions, paràmetres, controls, incidències i limitacions.
>>>>> - Sintetitzar un resultat sense ocultar els supòsits ni la qualitat de les entrades.

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

La **procedència** identifica d'on ve una entrada: productor, producte, versió, data, llicència, adreça i forma d'obtenció. El **llinatge de dades** descriu què li ha passat dins del projecte: quina capa en deriva, amb quina operació, quins paràmetres i quins controls. La traçabilitat necessita totes dues dimensions. Un fitxer pot conservar perfectament la URL original i haver perdut la relació amb la capa final; també pot tenir un historial intern molt detallat i partir d'una font sense autoria o data.

Cada sortida ha de tenir antecedents identificables. Si `parceles_candidates` prové d'una intersecció, el diari ha d'indicar les dues entrades exactes, la versió del projecte, l'algorisme, el tractament d'entitats invàlides i el lloc on s'ha desat. Si una entrada es corregeix i l'operació es repeteix, la sortida anterior no s'ha de reetiquetar silenciosament: cal substituir-la de manera controlada o conservar-la com a resultat rebutjat amb la incidència documentada.

El llinatge forma una xarxa de dependències, no només una cronologia. Una mateixa capa preparada pot alimentar un mapa, una unió i una anàlisi de proximitat; una mateixa sortida pot dependre de tres fonts amb dates diferents. El diari pot explicar aquesta xarxa amb identificadors de fitxer i capa sense dibuixar-la. El criteri és que, començant pel resultat, es pugui retrocedir fins a cada original i, començant per una font, es pugui saber en quins resultats intervé.

Aquesta xarxa fa visibles tant el recorregut principal com els controls que poden obligar a revisar una dada preparada o una sortida.

![Xarxa de llinatge entre fonts, preparació, operacions, controls, resultats i interpretació]({{ site.baseurl }}/assets/diagrams/ca/02-sintesi-documentacio/project-data-lineage.mmd "El llinatge connecta cada resultat amb les fonts, les transformacions i els controls dels quals depèn, i permet recórrer la cadena en tots dos sentits."){: data-figure-width-web="45rem" data-figure-width-pdf="95%"}

La validació també forma part de la cadena. Anotar només que una eina «ha funcionat» descriu l'estat de la interfície, no la qualitat de la sortida. Cal conservar el control aplicat i el seu resultat observat: recompte abans i després, presència de nuls, extensió, rang, geometries problemàtiques o contrast d'una mostra. Els valors reals s'han d'obtenir durant l'execució; una plantilla pot indicar quins controls cal fer, però no anticipar-ne les xifres.

## Organització de dades i resultats

Separar l'estat de les dades evita confondre una font amb una transformació. La còpia original es conserva tal com s'ha rebut o descarregat. Les dades preparades corregeixen estructura, tipus, CRS o àmbit sense perdre la relació amb l'original. Els resultats intermedis permeten diagnosticar un flux, i els finals responen directament una pregunta o alimenten una composició.

Una estructura possible és la següent:

::: listing "Estructura orientativa del projecte acumulatiu"
```filetree
projecte_tig/
|-- README.md
|-- dades_originals/
|   |-- paquets/
|   `-- extrets/
|-- dades_preparades/
|   `-- projecte_tig.gpkg
|-- treball/
|-- resultats_intermedis/
|-- resultats/
|   |-- raster/
|   `-- mapes/
|-- projecte_tig.qgz
`-- diari.pdf
```
:::

L'arbre és orientatiu, però les funcions no són intercanviables. `dades_originals` conserva allò que s'ha rebut del productor: els paquets i, quan cal obrir-los, una extracció íntegra que no s'edita. `dades_preparades` conté còpies que ja han passat per decisions com seleccionar camps, corregir tipus, retallar l'àmbit o materialitzar un CRS. `treball` admet proves que encara es poden descartar. `resultats_intermedis` conserva sortides necessàries per explicar o repetir una cadena, i `resultats` queda reservat per als productes validats que responen la pregunta.

La separació descriu **estats lògics**, no formats. Un GeoPackage pot contenir una capa preparada, una intermèdia i una final, però els noms interns han d'indicar-ne la funció. Un GeoTIFF pot ser una font original o un resultat. Desar tots els vectors en un únic contenidor redueix el nombre de fitxers, però no converteix automàticament totes les capes en una mateixa fase del procés.

La carpeta `treball` no ha de convertir-se en un abocador permanent. Una prova que no intervé en cap resultat es pot eliminar després de documentar la decisió que se n'ha extret. Una sortida intermèdia que permet comprovar una incidència o evita repetir una operació costosa s'ha de conservar amb un nom i un antecedent clars. La decisió depèn de la possibilitat de reconstrucció, no d'una regla segons la qual cal guardar-ho tot.

Les capes temporals de QGIS exigeixen una decisió explícita. Mentre només són resultats temporals, poden desaparèixer en tancar la sessió i no són una evidència persistent. Si una selecció o una transformació alimentarà una activitat posterior, s'ha de desar a `dades_preparades`, `resultats_intermedis` o `resultats` segons la funció. El diàleg de processament no pot decidir aquesta categoria a partir del nom de l'algorisme.

No totes les capes necessiten un fitxer separat. Un únic `projecte_tig.gpkg` pot contenir capes vectorials, taules i resultats relacionats, amb noms que indiquin funció i no només l'ordre accidental de creació. Els noms `municipis_font`, `municipis_preparats` i `municipis_pendent` expliquen millor el recorregut que `capa1`, `final2` o `nova_definitiva`.

Els noms han de ser estables, breus i compatibles amb les eines utilitzades. Convé usar minúscules, guions baixos i unitats explícites quan siguin necessàries, com `buffer_200_m`. Les dates formen part del nom només quan distingeixen versions reals de les dades o del resultat; no substitueixen un registre de canvis.

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

Desar el projecte aviat fixa un punt de referència per a les rutes i evita acumular capes en un projecte sense nom. El fitxer independent també permet revisar l'estructura encara que el projecte es desi addicionalment dins del GeoPackage. El nom estable `projecte_tig.qgz` identifica la continuïtat acumulativa; els canvis rellevants es documenten al diari o amb còpies de control deliberades, no amb una cadena de `projecte_final_final2.qgz`.

El projecte conserva estils, filtres, unions i composicions que poden canviar el significat de la vista sense canviar les dades. Una capa oculta per un filtre no està buida; una unió dinàmica pot desaparèixer si falta la taula externa; un disseny pot dependre d'una imatge o una tipografia que no viatja amb la font geogràfica. La prova de transport ha d'incloure aquestes dependències i no només comprovar que el llenç mostra algun mapa.

### Rutes relatives i absolutes

Les **rutes relatives** descriuen la posició d'un fitxer respecte del projecte i permeten moure conjuntament la carpeta. Les rutes absolutes depenen d'una unitat, un nom d'usuari o una jerarquia concreta. Després de configurar les rutes relatives cal traslladar una còpia de la carpeta a una ubicació diferent, obrir el `.qgz` i comprovar que totes les fonts continuen resolent-se.

A Windows, `C:\Users\anna\projecte_tig\dades_preparades\projecte_tig.gpkg` és una ruta absoluta.

En GNU/Linux, `/home/anna/projecte_tig/dades_preparades/projecte_tig.gpkg` també és una ruta absoluta. Pot ser correcta a l'equip d'origen i inexistent en un altre sistema. Una ruta relativa expressa la relació dins de l'arbre, com `dades_preparades/projecte_tig.gpkg`; mentre el `.qgz` i la carpeta es moguin junts mantenint la jerarquia, la relació es conserva.

Els segments `.` i `..` signifiquen, respectivament, la carpeta actual i la carpeta superior. Són útils per entendre la lògica, però una acumulació de `../../..` sol indicar que les dades han quedat fora de l'arrel transportable. La solució no és memoritzar el camí, sinó reunir dins d'un arbre comú les dependències que es poden copiar legalment. Un recurs compartit en una unitat de xarxa pot justificar una ruta absoluta en un entorn controlat, però aquesta decisió i el requisit de muntatge s'han de documentar.

QGIS permet definir si desa els camins de les fonts com a relatius o absoluts a les propietats generals del projecte. En un projecte desat com a `.qgz`, la ruta relativa es calcula respecte del fitxer de projecte. La `Carpeta inicial del projecte` és l'accés de conveniència que mostra l'`Explorador`: per defecte coincideix amb la carpeta del `.qgz`, però es pot canviar sense rebasar les rutes de les fonts. Per això cal desar primer el `.qgz`, configurar els camins relatius i tornar a afegir o revisar qualsevol capa carregada abans. Canviar l'opció no copia fitxers externs dins de l'arbre ni repara automàticament una font que ja no existeix {% cite qgisUserGuide344 %}.

Les URL de WMS, WMTS, WFS o API no es converteixen en rutes locals relatives. Continuen depenent de xarxa, servidor i, si escau, autenticació. Tampoc no és segur compartir credencials dins del projecte. La transportabilitat ha de distingir capes locals que viatgen amb la carpeta, recursos remots que s'han de tornar a consultar i fonts restringides que cada usuari ha de configurar amb permisos propis.

Una ruta relativa només resol la **localització**. No resol llicències, formats no admesos, extensions de base de dades, tipografies absents, diferències de versió ni dependències de complements. Per això el projecte ha d'indicar la versió de QGIS quan sigui rellevant i sotmetre's a una obertura real en una ubicació neta. Veure la paraula «relatiu» al diàleg és una configuració; obrir totes les fonts després del trasllat és l'evidència.

### Abast i límits del GeoPackage

QGIS també pot desar un projecte dins d'un GeoPackage. Aquesta opció és convenient per agrupar peces, però no s'ha de confondre amb una garantia d'interoperabilitat: altres aplicacions poden llegir les taules del GeoPackage i ignorar l'estat propi de QGIS. Durant el curs es conservarà també un `.qgz` independent per facilitar la revisió de l'estructura i la recuperació del projecte {% cite qgisUserGuide344 %}.

GeoPackage és un estàndard OGC basat en SQLite. Pot contenir diverses taules d'entitats vectorials, taules d'atributs i piràmides de tessel·les, juntament amb metadades i extensions definides segons el cas {% cite ogcGeoPackage2024 %}. Aquesta capacitat el fa adequat per concentrar vectors i taules relacionats sense dispersar-los en molts fitxers. Cada capa continua tenint nom, geometria, CRS, esquema i llinatge propis.

No és una carpeta comprimida d'ús general. Un GeoTIFF analític, un `.zip` original, un PDF del diari o qualsevol document no s'hi ha d'introduir com si l'estàndard els convertís en capes interoperables. Encara que GeoPackage admet tessel·les ràster, això no equival a conservar qualsevol ràster analític de coma flotant amb la mateixa compatibilitat que un GeoTIFF. El projecte del curs mantindrà habitualment aquests ràsters com a fitxers externs dins de l'arbre.

QGIS pot desar-hi estils i projectes mitjançant estructures o extensions pròpies. Altres aplicacions poden ignorar-les sense deixar de llegir les capes estàndard. Per això «tot és dins del `.gpkg`» no és una afirmació suficient: cal especificar quines taules són dades interoperables i quins elements depenen de QGIS. El `.qgz` independent conserva una via clara d'obertura i revisió.

Agrupar moltes capes en un sol fitxer redueix la dispersió, però també concentra el risc de pèrdua. Un GeoPackage no és una còpia de seguretat de si mateix. Abans d'una edició extensa convé tancar operacions pendents, crear una còpia coherent i evitar editar el mateix fitxer simultàniament des de processos o ubicacions sincronitzades que puguin entrar en conflicte. Una transacció pot agrupar escriptures de manera coherent, però no substitueix una estratègia de recuperació.

Els noms interns també s'han de gestionar. Esborrar o reanomenar una taula pot trencar la referència del `.qgz`; reemplaçar una capa amb una altra del mateix nom pot ocultar un canvi d'esquema. Després d'una importació s'han de revisar geometria, CRS, camps i recomptes, i després tornar a obrir el projecte. El contenidor simplifica el transport físic, no la validació del contingut.

>>>> **Una còpia comprimida no és documentació ni còpia de seguretat suficient.** Un paquet `.zip` pot simplificar un lliurament, però no explica les dependències, no permet comparar decisions i no protegeix per si sol contra la pèrdua de totes les còpies.

### Còpies de seguretat i control de versions

Una **còpia de seguretat** permet recuperar fitxers després d'una supressió, una avaria o una corrupció. Ha d'existir en una ubicació independent de la còpia de treball i s'ha de provar restaurant-ne contingut. Una carpeta sincronitzada pot replicar també una supressió o un fitxer malmès; una còpia al mateix disc no protegeix contra la fallada del disc. La freqüència i el nombre de còpies depenen del cost de repetir el treball, però almenys una no ha de compartir el mateix punt de fallada.

El **control de versions** conserva canvis identificats i permet relacionar-los amb una decisió. És especialment útil per al `README.md`, el diari en format editable, consultes, scripts, models o altres fonts textuals. Git no interpreta l'estructura interna d'un `.qgz`, un `.gpkg` o un GeoTIFF com interpreta línies de text; pot guardar versions binàries, però comparar-les, fusionar-les i contenir-ne el creixement és més difícil. Per això no s'ha de presentar Git com a substitut d'una còpia de seguretat ni com una solució automàtica per a totes les geodades.

En un projecte docent es poden combinar còpies de recuperació del conjunt amb fites deliberades dels fitxers centrals. Abans d'una transformació difícil de revertir es crea una còpia tancada del GeoPackage; després es registra al diari què s'ha canviat i quin resultat s'ha validat. No cal conservar una còpia amb marca horària de cada clic. Cal conservar prou estats per recuperar-se i prou documentació per saber quin estat és coherent.

El paquet `.zip` del lliurament és una **còpia de distribució**. Pot servir també per fer la prova de transport, però no és l'única còpia de seguretat ni l'historial de treball. Abans de comprimir s'han d'excloure memòries cau, temporals, credencials i originals que no es puguin redistribuir; després s'ha d'extreure el paquet en una carpeta nova i obrir-ne el contingut. Que la compressió acabi sense error no prova que el projecte sigui complet.

### Configuració inicial a QGIS

Tot i que la disposició concreta depèn de la versió i del perfil, la interfície manté unes regions funcionals estables: menús i barres d'eines per activar ordres, `Explorador` per localitzar fonts, `Capes` per organitzar-les, llenç del mapa per representar-les i barra d'estat per llegir l'escala, les coordenades i altres estats de la vista. La captura antiga, amb etiquetes en anglès, és orientativa; els panells visibles i la seva posició poden variar.

![Esquema de la interfície de QGIS amb menús, barres d'eines, explorador, capes, llenç del mapa i barra d'estat]({{ site.baseurl }}/assets/img/qgis/qgis-gui-schema.png "Captura històrica anotada del material docent predecessor; les regions funcionals orienten la configuració inicial, però no constitueixen un contracte exacte de la interfície actual."){: data-figure-width-web="48rem" data-figure-width-pdf="100%"}

La configuració ha de començar fora del llenç. Primer es crea l'arbre del projecte i es desa `projecte_tig.qgz` a l'arrel.

A `Projecte > Propietats > General` es configura l'emmagatzematge de camins relatius. També es revisa la `Carpeta inicial del projecte`, que pot apuntar a l'arrel per agilitzar la navegació, però no substitueix la carpeta del `.qgz` com a base de les rutes desades. Només llavors s'afegeixen les còpies preparades o els originals en mode d'inspecció, de manera que les referències neixen dins d'una estructura coneguda.

El GeoPackage inicial es pot crear des del panell `Explorador` o en desar la primera capa preparada. El contenidor es desa a `dades_preparades/projecte_tig.gpkg`; cada importació rep un nom intern descriptiu i es comprova abans de continuar. L'original no s'arrossega ni es reemplaça: una exportació crea la capa de treball i el diari registra font, operació, CRS i camps conservats.

El panell de capes es distribueix en grups que expressen funció, per exemple:

- `00_context`
- `10_originals_inspeccio`
- `20_preparades`
- `30_intermedies`
- `40_resultats`

Els prefixos són opcionals, però l'ordre no ha de dependre d'on ha quedat una capa després d'afegir-la. Les fonts remotes de context queden separades de les entrades analítiques i reben un nom que conserva productor i producte.

Abans de tancar la primera sessió, cal desar, tancar QGIS i tornar a obrir el `.qgz`. Aquesta primera reobertura comprova que cap resultat necessari continua sent temporal, que el GeoPackage no està bloquejat per una operació pendent i que les capes resolen les rutes previstes. Els recomptes, camps i extensions observats es documenten amb els valors reals de la sessió; el simple retorn de la simbologia no substitueix aquests controls.

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

La versió de QGIS i els proveïdors de processament s'han d'indicar quan poden alterar un algorisme o els seus paràmetres. També cal registrar els complements imprescindibles. Un projecte que depèn d'una selecció activa, una variable local o una capa temporal no documentades pot deixar de ser reproduïble encara que el fitxer `.qgz` s'obri.

Una entrada de qualitat comença per una decisió o una operació identificable, no per l'hora en què s'ha premut un botó. Pot indicar: objectiu de preparar el límit municipal; entrada `municipis_font` procedent del paquet identificat; filtre aplicat al camp documentat; algorisme i paràmetres; sortida `municipi_preparat`; controls de geometria, camps, CRS i extensió; i incidències. Aquesta estructura permet repetir el procés en una interfície lleugerament diferent perquè conserva el significat, no només el recorregut visual.

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

Des de la còpia s'obre el `.qgz`, no un projecte de la llista de recents que podria apuntar a l'original. Abans d'acceptar cap reparació automàtica, s'observa si apareixen fonts no disponibles. Després es comproven els grups, la visibilitat, els estils, les etiquetes, les unions, les relacions, els models i les composicions que formin part de l'activitat. Cada capa local s'ha de relacionar amb un fitxer o una taula interna de la còpia, no amb `Descàrregues`, l'escriptori o l'arrel anterior.

La validació utilitza els controls ja registrats. Les capes han de conservar els noms, tipus, CRS, camps i recomptes observats durant la preparació; els ràsters, les dimensions, bandes, resolució i `NoData` que corresponguin; i les composicions, els recursos necessaris. No s'introdueixen xifres de referència inventades: es comparen els valors de la prova amb els que el mateix projecte va documentar quan va crear les sortides.

Les fonts remotes es proven separadament. Amb connexió, cal confirmar que el servei encara respon i que el projecte n'identifica la dependència. Sense connexió, cal observar quina part del projecte continua disponible. L'objectiu no és que un WMS funcioni fora de línia, sinó que la seva absència no es confongui amb la pèrdua d'una entrada local i que cap anàlisi presentada com a reproduïble depengui d'una resposta efímera no documentada.

Una prova superada deixa una evidència breu: ubicació de la còpia, projecte obert, fonts resoltes, controls comparats, dependències remotes i incidències corregides. Si ha calgut cercar manualment una capa, la prova no s'ha superat encara. Cal corregir l'arbre o la referència al projecte original, tornar a copiar i repetir l'obertura fins que la resolució sigui explicable.

## Dos projectes organitzats de manera diferent

Un cas deficient pot semblar funcional a l'equip on s'ha creat. El `.qgz` és a l'escriptori; un límit municipal apunta a `Descàrregues`; el Shapefile s'ha separat del paquet; un ràster és en una memòria externa; i `final.gpkg` conté `capa1`, `capa1_nova` i `definitiva`. El WMS cadastral s'ha tractat com si fos la capa de parcel·les analítica. El diari conté captures dels menús, però no la versió, els filtres, les fonts ni els controls. Finalment, tota la carpeta s'ha comprimit al mateix disc i s'ha anomenat còpia de seguretat.

El projecte pot obrir-se perquè les rutes absolutes encara existeixen i perquè la memòria cau conserva el fons. No obstant això, no es pot saber quina capa interna sosté el resultat, no hi ha una còpia original íntegra i el paquet no inclou totes les dependències. Configurar rutes relatives en aquest moment no copiarà el contingut de `Descàrregues` ni la memòria externa. Reanomenar `definitiva` com `resultat_final` tampoc no reconstruirà el llinatge.

La resolució comença inventariant les fonts efectivament utilitzades. Els paquets originals autoritzats es tornen a obtenir o es recuperen íntegres i es desen a `dades_originals`; les extraccions es mantenen separades. El GeoPackage `dades_preparades/projecte_tig.gpkg` rep les capes de treball, i el ràster es copia dins de l'arbre si la llicència i la mida ho permeten. Cada capa interna rep un nom funcional i es relaciona amb l'original i l'operació que l'ha produïda. El WMS queda al grup de context, mentre que les parcel·les vectorials s'obtenen per una via adequada i documentada.

A continuació es repara cada font del `.qgz` existent perquè no es perdin estils i composicions, es configuren els camins relatius i es tanquen les capes temporals o duplicades. El diari substitueix la cronologia de clics per entrades amb objectiu, entrades, operació, paràmetres, controls i incidències. Es crea una còpia de seguretat independent i es fa la prova de transport des d'un `.zip` extret en una ubicació nova. Només després d'aquesta prova el projecte es pot considerar reorganitzat.

En un cas ben dissenyat des de l'inici, `projecte_tig.qgz` i totes les fonts locals pengen d'una mateixa arrel. Els paquets rebuts no es modifiquen; el GeoPackage concentra vectors i taules preparats; els ràsters analítics tenen fitxers propis; els intermedis conservats expliquen dependències reals; i els resultats finals no comparteixen noms amb proves descartades. Les capes remotes estan agrupades i documentades com a context o com a consultes reproduïbles.

La qualitat del cas ben organitzat no prové només de l'arbre. Cada sortida té una procedència, un esquema i controls; el `.qgz` torna a obrir-se després de copiar-lo; el paquet de distribució exclou allò que no es pot redistribuir; i una còpia de recuperació existeix fora de la ubicació de treball. Si una font falla, el diari permet identificar quin resultat queda afectat i decidir si cal restaurar, reparar o repetir una operació.

## Validació i síntesi

Validar no és només observar que el mapa «té bona forma». Els controls s'han de definir segons l'operació: recomptes abans i després d'una unió, àrees després d'un retall, valors mínims i màxims d'un ràster, nombre d'errors topològics o contrast manual d'una mostra d'entitats. Els controls numèrics i la inspecció espacial es complementen.

La **síntesi** selecciona les evidències que responen la pregunta i les presenta amb el context necessari. Un mapa final ha d'indicar què representa, de quin període són les dades, quines unitats utilitza i quines fonts l'han fet possible. L'escala, l'orientació, la llegenda i altres elements s'incorporen quan ajuden a interpretar el producte, no com una llista decorativa obligatòria.

La conclusió ha de mantenir la diferència entre observació i inferència. Un `buffer` de 200 m mostra una proximitat euclidiana definida pel model; no demostra que el recorregut sigui accessible. Una zona que compleix tres màscares és candidata segons els criteris introduïts; no és automàticament la millor localització. Documentar aquestes limitacions forma part del resultat.

## Activitats

### Comprovació: prova de trasllat

Cal crear un projecte breu amb dues capes locals, configurar rutes relatives, tancar QGIS i moure tota la carpeta. La comprovació consisteix a obrir el projecte des de la nova ubicació, verificar que no hi ha fonts perdudes i explicar quina diferència hi hauria si una capa continués apuntant a una carpeta de descàrregues.

### Micropràctica 1: projecte, pregunta i fonts

La primera micropràctica lliurable prepara la base que utilitzaran les activitats posteriors. El cas de Vila-seca serveix com a demostració; el lliurament s'ha d'adaptar al municipi assignat i a la disponibilitat real de dades.

::: table "Contracte de la micropràctica 1"
| Component | Requisit |
| --- | --- |
| Entrades | Una pregunta territorial, una capa administrativa oficial, una font temàtica i una font ràster o servei d'imatge |
| Operacions mínimes | Identificar les fonts, conservar els originals, incorporar-les a QGIS i definir l'estructura del projecte |
| Resultats | GeoPackage inicial, projecte `.qgz` transportable i inventari de fonts |
| Evidències del diari | Pregunta, unitat d'anàlisi, fitxa de cada font, arbre de fitxers i prova de trasllat |
| Comprovacions | Les capes s'obren, el CRS està identificat, les rutes són relatives i els originals no s'han modificat |
| Fitxers que cal conservar | Paquets originals autoritzats, `projecte_tig.gpkg`, `projecte_tig.qgz` i diari actualitzat |
:::

El lliurament només es considera reproduïble si el projecte torna a obrir-se des d'una ubicació diferent i si cada capa es pot relacionar amb una font, una data i una llicència. Moodle concretarà el format de tramesa i el termini.
