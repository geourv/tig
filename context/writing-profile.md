# Perfil de redacció del manual TIG

Aquest document defineix els criteris editorials duradors del manual de Tecnologies de la Informació Geogràfica. La versió catalana és l'única font de treball mentre el contingut estigui en revisió.

## Públic i coneixements previs

- El manual s'adreça principalment a estudiants de segon curs del Grau en Geografia, Anàlisi Territorial i Sostenibilitat.
- Es pressuposa una primera experiència amb dades territorials, taules, mapes, sistemes de coordenades i operacions bàsiques de QGIS adquirida a l'assignatura TIGIT.
- Els conceptes previs necessaris s'han de recordar breument quan condicionin una decisió, però no cal repetir el curs anterior.
- El text també ha de poder servir com a manual introductori de consulta fora de l'assignatura. Cap explicació essencial no pot dependre d'haver seguit una demostració presencial.

## Finalitat del manual

- El manual és principalment un text de teoria aplicada. Ha d'explicar models, conceptes, criteris i conseqüències abans de presentar una seqüència de programari.
- La teoria i la pràctica formen un únic recorregut: cada operació ha de respondre una pregunta geogràfica, utilitzar dades adequades i produir un resultat que es pugui comprovar i interpretar.
- El manual pot incloure més exemples i activitats que els exigits per l'avaluació. Les sis micropràctiques lliurables s'han de distingir inequívocament de la resta d'exercicis.
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

## Dades i casos docents

- Les dades principals procediran del CNIG. L'ICGC, el Cadastre i altres fonts oficials o obertes s'utilitzaran quan el cas ho requereixi.
- Cada font s'ha de valorar per autoria, data, escala o resolució, CRS, llicència, unitat d'observació, esquema i limitacions.
- Les taules d'atributs reals s'han de llegir amb les metadades disponibles i amb raonament explícit sobre el significat, el tipus i el domini de cada camp.
- Vila-seca i l'entorn de la Facultat poden actuar com a demostració comuna. Els fanals del carrer de Joanot Martorell, els carrils bici, les plaques solars i altres elements recognoscibles són casos adequats quan permeten comprovar el resultat sobre el terreny.
- Les activitats han d'ajudar a transferir el procediment al municipi assignat. No s'ha de confondre el cas resolt a classe amb la resposta que correspon lliurar.
- Les distàncies, llindars i criteris d'una anàlisi multicriteri s'han de justificar com a decisions del cas, no presentar-se com a valors universals.

## Projecte acumulatiu i evidències

- El curs construeix un projecte acumulatiu format per un GeoPackage, un projecte QGIS reproduïble i un diari d'activitats.
- Cal distingir dades originals, dades preparades, resultats intermedis i resultats finals. Les fonts originals no s'han de sobreescriure.
- El projecte s'ha de conservar dins del GeoPackage quan la funcionalitat utilitzada ho permeti i també en un fitxer `.qgz` independent que permeti revisar-ne l'estructura.
- Les rutes, els noms de capes, els camps, els CRS i les dependències han de permetre obrir i diagnosticar el projecte en un altre equip.
- El diari ha d'explicar l'objectiu, les fonts, les operacions, els paràmetres, les incidències, les correccions, els resultats i les limitacions.
- Les captures han de provar una decisió, una configuració, una incidència o un resultat. No s'ha de convertir el diari en una seqüència de captures de cada clic.
- Una activitat només es pot considerar reproduïble si els fitxers es tornen a obrir, les fonts es resolen i el resultat es pot relacionar amb les entrades i els paràmetres documentats.

## Estructura dels capítols i activitats

- Cada capítol ha de començar amb una introducció breu que situï la pregunta i la seva utilitat territorial.
- Els objectius d'aprenentatge s'han de limitar normalment a tres o cinc resultats observables dins d'un únic callout `>>>>>`.
- Els conceptes s'han d'introduir quan siguin necessaris per entendre una decisió; no s'ha d'obrir sistemàticament amb un glossari.
- Els exemples han d'arribar precedits pel problema o la distinció que ajuden a comprendre.
- Cada capítol de contingut ha d'acabar amb una secció `## Activitats`.
- Les activitats poden incloure comprovacions conceptuals, exercicis breus, pràctiques guiades, aplicacions al municipi propi, micropràctiques lliurables i ampliacions.
- Cada micropràctica lliurable ha d'indicar entrades, operacions mínimes, resultats esperats, evidències del diari, comprovacions i fitxers que cal conservar. Les dates i la configuració concreta del lliurament pertanyen a Moodle.
- Els capítols poden tenir una extensió desigual quan el desenvolupament conceptual ho exigeixi, però una acumulació de preguntes independents indica que cal separar-los.

## Terminologia i format tècnic

- Cal introduir sistema de referència de coordenades (`CRS`) en la primera aparició i utilitzar `CRS` de manera consistent després, d'acord amb la terminologia visible a QGIS.
- Cal distingir una unió d'atributs basada en una clau d'una unió espacial basada en una relació geomètrica.
- Cal distingir topologia d'edició, predicats topològics i geoprocessament; no són sinònims.
- Els noms de programari, organismes i formats consolidats, com QGIS, CNIG, ICGC i GeoPackage, s'escriuen sense format especial.
- El codi en línia es reserva per a noms literals de camps, expressions, funcions, extensions com `.gpkg` o `.qgz`, paràmetres i rutes de menú.
- Els anglicismes només s'han d'utilitzar quan no hi hagi una forma catalana prou precisa. La primera aparició pot indicar el terme original entre parèntesis.

## Figures, taules i diagrames

- Les figures, taules i diagrames només s'han d'incorporar quan fan visible una relació que la prosa no explica amb la mateixa claredat.
- No s'han d'inserir placeholders en contingut publicable. Una figura pendent s'ha de gestionar fora del capítol fins que n'existeixi una font aprovada.
- Les imatges han de tenir text alternatiu i peu explícit. Les taules han d'utilitzar el component numerat admès per `unaltremanual`.
- Els diagrames s'han de conservar com a fonts editables sota `assets/diagrams/` i renderitzar amb `diavisuals`.
- No s'ha d'editar manualment cap sortida gestionada per un renderitzador.

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
