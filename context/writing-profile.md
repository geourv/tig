# Perfil de redacció del manual TIG

Aquest document defineix els criteris editorials duradors del manual de Tecnologies de la Informació Geogràfica. La versió catalana és l'única font de treball mentre el contingut estigui en revisió.

## Públic i coneixements previs

- El manual s'adreça principalment a estudiants de segon curs del Grau en Geografia, Anàlisi Territorial i Sostenibilitat.
- L'alumnat pot haver tingut una primera experiència amb dades territorials, taules, mapes i QGIS a l'assignatura TIGIT, especialment amb unions, simbologia temàtica, composició i exportació. Aquesta exposició pot variar segons el curs i no s'ha de tractar com un domini consolidat.
- Els conceptes previs necessaris s'han de recordar quan condicionin una decisió. El manual ha de començar des dels significats essencials, especialment en sistemes de referència, geoprocessament, dades ràster i control de qualitat, sense repetir innecessàriament tot el curs anterior.
- El text també ha de poder servir com a manual introductori de consulta fora de l'assignatura. Cap explicació essencial no pot dependre d'haver seguit una demostració presencial.

## Finalitat del manual

- El manual és principalment un text de teoria aplicada. Ha d'explicar models, conceptes, criteris i conseqüències abans de presentar una seqüència de programari.
- La teoria i la pràctica formen un únic recorregut: cada operació ha de respondre una pregunta geogràfica, utilitzar dades adequades i produir un resultat que es pugui comprovar i interpretar.
- El manual pot incloure més exemples i activitats que els exigits per l'avaluació. Els capítols presenten comprovacions, preguntes i activitats integradores; Moodle identifica quines s'avaluen i concreta els requisits i els percentatges. No cal etiquetar les activitats del manual com a avaluades.
- La guia docent és el marc normatiu de l'assignatura. Moodle concreta el calendari, els enunciats, els fitxers, els lliuraments i les qualificacions.
- Les dates o condicions operatives de Moodle no han d'organitzar l'índex ni quedar repetides en diversos capítols.

## Veu i llengua

- S'ha d'utilitzar català estàndard, amb terminologia geogràfica i informàtica consistent.
- La veu ha de ser clara, precisa i exigent, però accessible. Cal prioritzar la prosa narrativa i explicativa sobre les enumeracions.
- No s'ha d'adreçar directament al lector en segona persona. Cal preferir formes com `cal`, `convé`, `s'ha de` o la descripció directa d'una acció.
- No s'ha d'utilitzar la primera persona del plural per simular una comunitat entre autoria i lector. Només és acceptable quan descriu una decisió real del curs.
- No cal incloure informació biogràfica ni una presentació del professorat. Les responsabilitats es poden descriure mitjançant les sessions, la docència, Moodle, el fòrum, el correu institucional i les tutories.
- Cada paràgraf ha de tenir una funció principal i una continuïtat concreta amb el següent. S'han d'evitar autoresums, frases buides i afirmacions genèriques sobre la importància de la tecnologia.

## Seqüència pedagògica

Quan el contingut ho permeti, l'explicació seguirà aquest ordre:

1. Formular una pregunta, necessitat o decisió territorial.
2. Explicar el model o concepte geogràfic necessari.
3. Delimitar les dades, els supòsits i els criteris de qualitat.
4. Presentar l'operació de manera independent del programari.
5. Mostrar-ne una aplicació principal amb QGIS.
6. Comprovar el resultat amb recomptes, mesures, contrastos o inspecció documentada.
7. Interpretar què permet afirmar el resultat i quines limitacions conserva.
8. Proposar una activitat que transfereixi el procediment a un altre territori o conjunt de dades.

No cal forçar tots els moviments en cada paràgraf. La seqüència serveix per evitar tant la teoria desconnectada com les receptes de botons sense criteri.

## Programari i transferència

- QGIS és l'eina principal del curs i el programari amb què es desenvoluparan els procediments complets.
- Els models de dades, les relacions espacials, les operacions i els criteris de validació s'han d'explicar de manera aplicable a qualsevol SIG.
- Les rutes de menú, els noms de paràmetres i les particularitats de QGIS han d'aparèixer després de l'explicació conceptual, no substituir-la.
- No cal documentar totes les alternatives de programari. Només s'han d'esmentar quan ajudin a distingir un estàndard, un format interoperable o una limitació pròpia de QGIS.
- Els connectors de Cadastre, ICGC, QuickMapServices i altres complements s'han de presentar com a vies d'accés convenients, no com a substituts de la font, les metadades o la llicència.
- Les captures de la interfície només s'han d'utilitzar quan la disposició visual sigui necessària per executar o diagnosticar una tasca. Cal indicar la versió de QGIS quan una diferència d'interfície pugui afectar el procediment.
- En els casos inicials cal mostrar una seqüència guiada completa: mapa amb el WMS i el vector a una escala útil, estat de selecció, menú contextual, diàleg emplenat i resultat reobert. Les captures de controls aïllats no substitueixen aquest recorregut. Els detalls de diàlegs o menús es poden retallar quan la vista de context ja s'ha mostrat i el retall en millora la lectura.
- Cal ensenyar explícitament la connexió a un GeoPackage, el desament de projectes, l'actualització de la connexió de l'Explorador i la diferència entre capes i projectes. Es mostrarà que un GeoPackage pot conservar diversos projectes amb noms diferents sobre les mateixes dades.

## Dades i casos docents

- Les dades principals procediran del CNIG. L'ICGC, el Cadastre i altres fonts oficials o obertes s'utilitzaran quan el cas ho requereixi.
- Cada font s'ha de valorar per autoria, data, escala o resolució, CRS, llicència, unitat d'observació, esquema i limitacions.
- Les taules d'atributs reals s'han de llegir amb les metadades disponibles i amb raonament explícit sobre el significat, el tipus i el domini de cada camp.
- El recorregut pràctic comença amb un municipi escollit per l'estudiant, un WMS i un límit municipal seleccionat d'una font documentada, exportat a un GeoPackage i carregat des d'aquest contenidor. Vila-seca i l'entorn de la Facultat són el cas de demostració. L'Ortofoto Territorial 2025 de l'ICGC és el fons del cas resolt; la comparació ICGC–CNIG, altres WMS i les composicions són ampliacions del nucli inicial.
- Els fanals del carrer de Joanot Martorell, els carrils bici, les plaques solars i altres elements recognoscibles són casos adequats quan permeten comprovar el resultat sobre el terreny.
- Les activitats han d'ajudar a transferir el procediment al municipi escollit. No s'ha de confondre el cas resolt a classe amb la resposta que correspon conservar i, si escau, lliurar.
- Els fitxers reals de classe s'inspeccionen abans de reconstruir-ne el procediment. Cal conservar noms, esquemes i valors observats, distingir-los de les propietats desconegudes de l'origen i documentar qualsevol normalització posterior. Els projectes d'inspecció i les captures es preparen sobre còpies identificades; la composició del cas PR1 correspon a l'autor.
- Les distàncies, llindars i criteris d'una anàlisi multicriteri s'han de justificar com a decisions del cas, no presentar-se com a valors universals.

## Estructura comuna i evidències

- El curs utilitza una única estructura de carpetes `tig/` i sis instantànies encadenades del projecte. Cada fase ha d'identificar inequívocament els seus fitxers, el municipi escollit i el punt de partida heretat.
- Cal distingir dades originals, derivats preparats reutilitzables, resultats intermedis i resultats finals. Les fonts originals no s'han de sobreescriure. `data/processed/` es reserva per a preparacions derivades de `data/raw/` que s'han de reutilitzar en diversos exercicis, com un mosaic DEM combinat i retallat a l'àrea de treball.
- `sandbox/` és sempre l'espai de treball actiu. La primera pràctica crea `pr1-project-setup-cognom.gpkg`; les següents copien el GeoPackage validat de la predecessora i el reanomenen `pr2-digitalitzacio-cognom.gpkg`, `pr3-consultes-cognom.gpkg`, `pr4-geoprocessament-cognom.gpkg`, `pr5-raster-cognom.gpkg` i `pr6-sintesi-cognom.gpkg`. `pr6` copia també a `sandbox/` els deu GeoTIFF externs heretats de `pr5`. No es copia ni es reanomena el `.qgz` anterior.
- El resultat inicial combina el GeoPackage amb el projecte incrustat `pr1`, el `.qgz` homònim i uns apunts breus en PDF. Els apunts documenten passos importants, decisions, comprovacions i problemes amb captures significatives. Els noms interns dels límits poden diferir segons el cas; les fases següents conserven les capes realment preparades i identifiquen quina alimenta `municipi_treball`.
- Cada GeoPackage nou conté físicament les capes i taules locals heretades, no enllaços al contenidor predecessor. Abans de continuar s'han de reorientar les fonts locals al GeoPackage homònim i comprovar que no depenen de `dist/`, d'una altra pràctica ni d'una ruta personal.
- Cada instantània identifica un projecte principal, anomenat `pr1` fins a `pr6`. El GeoPackage pot conservar altres vistes amb noms diferents; totes les que es mantinguin han de tenir les fonts comprovades i adequades a la instantània. Després de validar el projecte principal es crea a `sandbox/` un `.qgz` nou amb el mateix nom base que el GeoPackage i camins relatius cap als fitxers que l'acompanyen.
- Amb QGIS tancat, els fitxers nous de la pràctica es copien al `dist/` pla de la revisió actual sense canviar-ne els noms i es proven des d'una ubicació neta. Les dependències de fases anteriors es verifiquen i no se sobreescriuen. Si es detecta un error abans del lliurament, es reconstrueix el candidat complet en un `dist/` net i es regeneren la fita afectada i les descendents; no es pedaça cap sortida. Un paquet ja lliurat és immutable: qualsevol correcció posterior crea una revisió completa en una carpeta d'assemblatge separada, amb els mateixos noms contractuals a l'interior, i conserva intacte el paquet anterior.
- A `pr5` i `pr6`, els GeoTIFF analítics es mantenen com a fitxers germans del GeoPackage i del `.qgz`. `pr6` copia sense reanomenar els GeoTIFF lliurats per `pr5` de `dist/` a `sandbox/` i hi apunta localment. En distribuir `pr6`, aquestes còpies es verifiquen byte per byte, no se sobreescriuen a `dist/` i s'incorporen al paquet complet des d'una carpeta d'assemblatge separada.
- El projecte incrustat, el projecte extern i qualsevol còpia de distribució són representacions independents: desar-ne una no actualitza les altres.
- Les rutes, els noms de capes, els camps, els CRS i les dependències han de permetre obrir i diagnosticar el projecte en un altre equip.
- El diari ha d'explicar l'objectiu, les fonts, les operacions, els paràmetres, les incidències, les correccions, els resultats i les limitacions.
- Les captures han de provar una decisió, una configuració, una incidència o un resultat. No s'ha de convertir el diari en una seqüència de captures de cada clic.
- Una activitat només es pot considerar reproduïble si els fitxers es tornen a obrir, les fonts es resolen i el resultat es pot relacionar amb les entrades i els paràmetres documentats.
- Les activitats s'han de formular com a resultats observables que queden incorporats al projecte, al GeoPackage, a l'inventari o al diari, no com una successió d'accions efímeres.

## Estructura dels capítols i activitats

- Cada capítol ha de començar amb una introducció breu que situï la pregunta i la seva utilitat territorial.
- Els objectius d'aprenentatge s'han de limitar normalment a tres o cinc resultats observables dins d'un únic callout `>>>>>`.
- Els conceptes s'han d'introduir quan siguin necessaris per entendre una decisió; no s'ha d'obrir sistemàticament amb un glossari.
- Els títols de secció han d'anomenar el concepte, la relació, el problema o el resultat que s'hi explica. Cal evitar fórmules com «X abans de Y», «altres aspectes» o «detalls» quan només anuncien un ordre de treball i amaguen el contingut. Una secció breu que defineix vocabulari ha de fer recognoscibles els termes des de l'índex.
- Els exemples han d'arribar precedits pel problema o la distinció que ajuden a comprendre.
- Al capítol 3, els nivells conceptual, lògic i físic s'han de presentar amb tres il·lustracions de la mateixa escena realista, amb anotacions breus al costat dels objectes. Cal mostrar significats, geometries i atributs, i decisions de desament; evitar taules de registres, coordenades de l'inventari, esquemes relacionals detallats, SQL i programació en aquesta introducció. Les definicions de formats i de CRS es poden il·lustrar amb fragments textuals quan ajudin a llegir les dades.
- Cada capítol de contingut ha d'acabar amb una secció `## Activitats`.
- Les activitats poden incloure comprovacions conceptuals, exercicis breus, pràctiques guiades, aplicacions al municipi propi, una activitat integradora final i ampliacions.
- Cada activitat integradora ha d'indicar entrades, operacions essencials, resultats esperats, evidències del diari, comprovacions i fitxers que cal conservar. Les ampliacions no substitueixen els resultats essencials. L'avaluació, les dates i la configuració concreta del lliurament pertanyen a Moodle.
- Els capítols poden tenir una extensió desigual quan el desenvolupament conceptual ho exigeixi, però una acumulació de preguntes independents indica que cal separar-los.

## Terminologia i format tècnic

- Cal introduir sistema de referència de coordenades (`CRS`) en la primera aparició i utilitzar `CRS` de manera consistent després, d'acord amb la terminologia visible a QGIS.
- Cal distingir una unió d'atributs basada en una clau d'una unió espacial basada en una relació geomètrica.
- Cal distingir topologia d'edició, predicats topològics i geoprocessament; no són sinònims.
- Els noms de programari, organismes i formats consolidats, com QGIS, CNIG, ICGC i GeoPackage, s'escriuen sense format especial.
- El codi en línia es reserva per a noms literals de camps, expressions, funcions, extensions com `.gpkg` o `.qgz`, paràmetres i rutes de menú.
- Els identificadors interns prescrits pel curs utilitzen caràcters ASCII i `snake_case` i conserven el vocabulari fixat, com `municipi_treball`, `codi_muni` i `vies_principals`. Els noms de fonts dels casos reals es transcriuen literalment: el cas PR1 de classe conté `vilaseca_icgc_15000` i `vilaseca_cnig`; els exemples reconstruïts anteriors utilitzen `municipality_icgc_5k` i `municipality_cnig`. No cal reanomenar una capa existent només per uniformar els exemples; cal documentar-ne la correspondència i mantenir les referències del projecte.
- Els anglicismes només s'han d'utilitzar quan no hi hagi una forma catalana prou precisa. La primera aparició pot indicar el terme original entre parèntesis.

## Figures, taules i diagrames

- Les figures, taules i diagrames només s'han d'incorporar quan fan visible una relació que la prosa no explica amb la mateixa claredat.
- Els recursos visuals s'han de concebre com a figures de llibre de text integrades en l'argument, no com a diapositives autònomes.
- Les comparacions entre models han de representar el mateix escenari amb geometries, àmbit i colors corresponents, perquè es pugui seguir la transposició entre representacions. Les graelles ràster s'han de dibuixar amb cel·les quadrades per defecte; qualsevol proporció diferent ha de respondre a una propietat explícita de les dades.
- Dins de cada nivell de modelització, tots els objectes del mateix tipus han de repetir les mateixes propietats o camps i mostrar-ne els valors corresponents. No s'han de repartir camps diferents entre objectes com si les anotacions fossin només exemples parcials d'un esquema.
- En les comparacions de models, cada peu de figura ha de començar identificant el tipus de model representat i continuar amb els detalls que en permeten interpretar l'exemple.
- Quan el peu o el context ja anomenen la relació representada, la figura ha d'ometre títols i subtítols interns visibles que la repeteixin.
- Per defecte s'han d'evitar contenidors arrodonits, targetes i pastilles. Les cantonades arrodonides i les corbes només s'han d'utilitzar quan siguin intrínseques a la geometria o a la relació explicada.
- Una figura no ha de transcriure paràgrafs ni reproduir una taula. Les etiquetes han de ser breus i identificar objectes, relacions o resultats observables.
- No s'han d'inserir placeholders en contingut publicable. Una figura pendent s'ha de gestionar fora del capítol fins que n'existeixi una font aprovada.
- Les imatges han de tenir text alternatiu i peu explícit. Les taules han d'utilitzar el component numerat admès per `unaltremanual`.
- Els diagrames s'han de conservar com a fonts editables sota `assets/diagrams/` i renderitzar amb `diavisuals`.
- Els inventaris i les estructures de fitxers i carpetes del text publicable s'han de representar amb diavisuals i PlantUML, preferentment `@startfiles` per als arbres reals. Els blocs de codi es reserven per a expressions, peticions o codi que cal llegir o executar, no per substituir aquests diagrames.
- No s'ha d'editar manualment cap sortida gestionada per un renderitzador.

## Cas acumulatiu de filtres, seleccions i expressions

- L'ordre del capítol 5 és obligatòriament progressiu: localització i selecció manual de Vila-seca per clic o requadre; filtre de capa; modes del filtre de taula; eines de selecció i modificadors; selecció per expressió; selecció per ubicació; calculadora de camps. Els tipus, els predicats i les funcions s'expliquen en el punt on el cas els necessita, no com un catàleg previ desconnectat.
- Les dades del recorregut aplicat provenen d'Información Geográfica de Referencia del Centre de Descàrregues del CNIG: límits administratius, CartoCiudad i transport. El municipi CNIG seleccionat al començament serà la referència de les consultes espacials; tindrà una capa pròpia per no substituir el límit heretat de les fases anteriors.
- Cada captura de menú ha de mostrar l'accés: capa activa, clic dret o menú superior i acció concreta ressaltada. Les anotacions d'unaltracaptura utilitzen selectors de widgets reals i glifs d'entrada. Els peus expliquen què s'observa i com es comprova, sense confiar que el menú aparegui per si sol.
- Si una captura ja mostra la consulta completa i llegible, no cal repetir-la immediatament en un bloc de codi. Els blocs es reserven per als exemples que necessiten llegir o reutilitzar l'expressió fora de la captura.
- La calculadora diferencia crear i actualitzar un camp, camp emmagatzemat i virtual, i abast sobre totes les entitats o només les seleccionades. Recorda els tipus de dades del capítol de digitalització i mostra l'ajuda nativa d'una funció amb arguments, resultat i exemple, especialment per als agregats.
- El capítol 5 segueix el mateix territori i un GeoPackage que creix amb resultats comprovats: límits administratius, portals i illes de CartoCiudad i vies de transport. Els exemples conceptuals poden ser sintètics, però el recorregut aplicat utilitza les fonts reals i valors calculats amb QGIS.
- Es distingeixen filtre de capa/proveïdor, filtre de la taula d'atributs, selecció i exportació persistent. Cada exemple conserva els recomptes de font, capa, taula i selecció que corresponguin. El filtre provincial de referència és `"CODNUT3"='ES514'` sobre la distribució CNIG que realment conté aquest camp.
- Les eines de selecció i els modificadors Shift/Ctrl es comproven en el context concret: clic al mapa, selecció per àrea o selecció de files. No s'ha d'atribuir una regla única a gestos diferents. Les expressions i els predicats espacials es vinculen després al mateix cas.
- Les seleccions de portals, illes i vies es desen com a capes noves del GeoPackage. Es conserva la geometria sencera de l'entitat seleccionada; els retalls, buffers i superposicions que creen geometries noves corresponen al capítol 6.
- La selecció espacial ha de mostrar el resultat ressaltat al mapa i la seva exportació real: menú, només seleccionats, fitxer GeoPackage existent, nom de capa, CRS i reobertura. Les captures de selecció i resultat de portals i illes de CartoCiudad mostren el terme municipal complet, amb el mateix enquadrament de referència que el viari i el contorn visible per comprovar què queda dins i fora. Les illes es representen amb farciment. El cas principal conserva les illes contingudes; la intersecció és una comparació de frontera. El cas de vies primàries es concreta en autovies i autopistes, amb l'A-7 i l'AP-7 recognoscibles, distingint registres d'itinerari i identificadors de tram únics.
- Els camps i dominis de CartoCiudad i de `clased` s'inspeccionen abans d'escriure els filtres. La comparació de `$area` amb `area($geometry)`, i les mesures de perímetre i longitud, indiquen CRS, el·lipsoide i unitats. Els camps de mesures es mantenen numèrics; els àlies i les expressions d'etiquetatge incorporen unitats llegibles com `km²`.

## Cites i bibliografia

- Les afirmacions dependents de recerca, estàndards, especificacions o documentació tècnica s'han de basar en fonts verificades.
- Cal preferir estàndards, organismes responsables, documentació oficial i bibliografia acadèmica abans que tutorials secundaris.
- Els capítols amb cites han d'activar `manual_references: true` perquè `unaltremanual` hi generi la bibliografia corresponent.
- La bibliografia general es presentarà en un capítol final no numerat, amb una selecció comentada de lectures recomanades i el repertori complet del manual.
- No s'han d'importar entrades del repositori antic sense comprovar-ne autoria, títol, any, editorial o revista, DOI o URL i clau única.

## Aprovació i revisió

- Tot contingut nou s'ha de mantenir en `content_status: draft` o `review` fins a l'aprovació explícita de l'autor.
- No s'han d'incloure en el cos publicable instruccions de redacció, tasques pendents, placeholders, notes d'agents ni referències a converses.
- Abans de l'aprovació cal revisar ortografia, terminologia, exactitud tècnica, seqüència pedagògica, enllaços, cites, peus i referències creuades.
- Cal executar les comprovacions editorials, de fonts, figures, computacions i visualitzacions que siguin aplicables, construir el lloc i revisar-ne la versió renderitzada.
- La publicació i el canvi a `approved` requereixen sempre revisió humana.
