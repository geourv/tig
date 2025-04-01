---
lang: ca
permalink: /:title/ca/
title: 1. Per què Jekyll amb GitBook
author: Tao He
date: 2019-04-27
category: Jekyll
weight: 1
layout: chapter
video: "https://www.youtube.com/watch?v=abc123"
zip-url: "https://www.youtube.com/watch?v=abc123"
---
GitBook és un estil frontal increïble per presentar i organitzar continguts (com capítols de llibres
i blogs) a la web. La manera típica de desplegar GitBook a [Github Pages][1]
és generar fitxers HTML localment i després pujar-los al repositori de Github, normalment a la branca `gh-pages`.
No obstant això, és bastant molest repetir aquesta càrrega de treball i dificulta que les persones
facin control de versions mitjançant git quan hi ha fitxers HTML generats per incloure i excloure.

Aquest tema extreu la definició d'estil del lloc generat per GitBook i proporciona la plantilla
perquè Jekyll renderitzi documents markdown a HTML, de manera que tot el lloc es pot desplegar
a [Github Pages][1] sense generar i pujar un paquet HTML cada vegada que hi ha
canvis al repositori original.

[1]: https://pages.github.com

Aquesta plantilla de Jekyll GitBook està dissenyada per ser una solució potent i flexible per crear documentació bella i fàcil de navegar, manuals o fins i tot llibres personals. Tant si ets un desenvolupador, un escriptor tècnic o qualsevol persona que necessiti compilar i presentar informació en un format estructurat, aquesta plantilla ofereix una manera fàcil d'utilitzar per fer-ho.

#### Per què utilitzar aquesta plantilla de Jekyll?

1.  **Facilitat d'ús:**
    
    *   Amb el generador de llocs estàtics de Jekyll al seu nucli, aquesta plantilla et permet centrar-te en escriure contingut en Markdown, mentre que la plantilla s'encarrega de l'organització i l'estil. No cal que et preocupis per una configuració complexa o detalls de disseny: només escriu i publica.
2.  **Disseny d'estil GitBook:**
    
    *   Inspirada en la popular plataforma GitBook, aquesta plantilla ofereix un disseny net i professional. Inclou una taula de continguts automàtica, navegació per la barra lateral i temes personalitzables, assegurant que el teu contingut sigui accessible i fàcil de navegar.
3.  **Personalitzable i extensible:**
    
    *   Dissenyada amb flexibilitat en ment, aquesta plantilla et permet personalitzar fàcilment dissenys, colors i components per adaptar-los a la teva marca o estil personal. A més, s'integra perfectament amb els complements de Jekyll, incloent Jekyll Scholar per a citacions i bibliografies, cosa que la fa ideal per a projectes acadèmics.
4.  **Perfecta per a documentació:**
    
    *   Tant si estàs documentant programari, escrivint un manual d'usuari o creant una base de coneixement, aquesta plantilla està equipada per gestionar-ho tot. El format estructurat t'ajuda a organitzar el contingut en seccions i capítols, facilitant que els usuaris trobin la informació que necessiten.
5.  **Beneficis dels llocs estàtics:**
    
    *   Com a plantilla basada en Jekyll, el teu lloc serà ràpid, segur i fàcil d'allotjar. Els llocs estàtics tenen menys vulnerabilitats en comparació amb els llocs dinàmics, i es poden allotjar en una àmplia gamma de plataformes, incloent GitHub Pages, de manera gratuïta.

#### Propòsit d'aquesta plantilla

L'objectiu principal d'aquesta plantilla és proporcionar una base sòlida per crear documentació o llibres estructurats, llegibles i d'aparença professional. Serveix com a punt de partida que pots adaptar ràpidament per adaptar-te a les teves necessitats específiques.

A més de proporcionar una estructura neta i organitzada per al teu contingut, aquesta plantilla de Jekyll està dissenyada amb funcions avançades per millorar el teu projecte de documentació o llibre. Un dels propòsits clau d'aquesta plantilla és integrar-se sense problemes amb la gestió de bibliografies, permetent-te citar fàcilment fonts i compilar llistes de referències completes utilitzant **Jekyll Scholar**. A més, suporta la compilació en PDF, permetent-te generar **versions preparades per a impressió** del teu contingut per a distribució fora de línia o fins arxivístics. Aquestes funcions, juntament amb d'altres com dissenys personalitzats i navegació flexible, fan que aquesta plantilla sigui una eina robusta per crear publicacions professionals i ben organitzades.

Aquest manual et guiarà pel procés de configurar el teu projecte amb aquesta plantilla, personalitzar-la al teu gust i entendre les funcions disponibles per a tu. Al final d'aquest manual, estaràs preparat per crear i mantenir el teu propi lloc de documentació o llibre elaborat amb facilitat.

* * *

Seguint els passos descrits en aquest manual, podràs aprofitar tot el potencial de la plantilla Jekyll GitBook, fent que sigui més fàcil que mai crear, gestionar i compartir el teu contingut amb el món.


# Lectures recomanades

{% bibliography %}
