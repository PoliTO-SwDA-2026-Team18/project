# Architecture — Section C: Component Level (C4 — Level 3)

> **Owner:** Matteo Francesco Castigliego  
> **Status:** To be completed

<!-- 
Required content:
- C4 Component Diagram(s) for relevant containers
- Justify any decisions to exclude specific containers from analysis
- Mandatory question: SOLID principle violations at level 3
- Diagrams: ../../../diagrams/c4/component-<name>.puml
-->

## 1. C4 Component Diagrams for Relevant Containers

The most important modules of Egeria are about 14 and i've decided to analyze two of them that are the most importanto for the flow of metadata.  

Basandoci sulla suddivisione in 14 sottomoduli del codice sorgente di Egeria (che rappresentano i componenti architetturali), abbiamo deciso di esplodere i due container fondamentali per il flusso di scambio dei metadati. I diagrammi PlantUML illustrano i seguenti componenti interni:

### 1.1 Metadata Access Server (OMAS) Component Diagram
This is the main container of the architecture, his main components are linked with some module like:
- **access-service**: this module provides the API REST adapt for all metadata, for example we have *ocf-metadata-management* which provides metadata management for the Open Connector Framework (OCF), *omf-metadata-management* which provides metadata management for the Open Metadata Framework (OMF) and *gaf-metadata-management* which provides metadata management for the Open Governance Framework (OGF); all is referred to properties and APIs.
- **repository-services (OMRS)**: the Open Metadata Repository Services enable metadata repositories to exchange messages independently by technology or technology supplier. When a project borns is composed by a small number of interfaces, this number increases during the developement and several interfaces are present, as conseguence multiple silos of metadata are created. The goal of ORMS is to bring these repositories together so metadata are linked and can work together. There are more modules *repository-services..*:
    --*apis*:
    --*archive-utilities*:
    --*client*:
    --*implementation*:
    --*spring*:
    

.
- **`common-services` & `user-security`**: Forniscono utilità trasversali come la cattura degli errori (FFDC) e l'autorizzazione.

### 1.2 Integration Daemon Component Diagram
Questo container ospita il motore di sincronizzazione continua. Al suo interno troviamo:
- **`adapters`**: Sono i *connector* pluggable che implementano la comunicazione con i tool proprietari.
- **`frameworks`**: Definisce le interfacce standardizzate necessarie per costruire i connettori.

