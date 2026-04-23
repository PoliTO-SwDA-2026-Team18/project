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
- **`access-service`**: this module provides the API REST adapt for all metadata, for example we have *ocf-metadata-management* which provides metadata management for the Open Connector Framework (OCF), *omf-metadata-management* which provides metadata management for the Open Metadata Framework (OMF) and *gaf-metadata-management* which provides metadata management for the Open Governance Framework (OGF); all is referred to properties and APIs.
- **`repository-services (OMRS)`**: the Open Metadata Repository Services enable metadata repositories to exchange messages independently by technology or technology supplier. When a project borns is composed by a small number of interfaces, this number increases during the developement and several interfaces are present, as conseguence multiple silos of metadata are created. The goal of ORMS is to bring these repositories together so metadata are linked and can work together. There are more modules *repository-services..*:
    - <u>*apis*</u>: contains the connector interfaces and event structures for the repository services.
    - <u>*archive-utilities*</u>: provides the common utilities used to build Open Metadata Archives.
    - <u>*client*</u>: supports two clients:
        - *Local Repository Services Client*: calls to the local repository in a remote server
        - *Enterprise Repository Services Client*: calls to the enterprise repository services in a remote server.
    - <u>*implementation*</u>: implementation contains the support for the peer-to-peer metadata exchange and federation.
    - <u>*spring*</u>: uses spring annotations to create the OMRS REST services.
    

- **`common-services`**: provides common java functions to clients and the specialized services that run in the OMAG Server. It is divided in more parts, for example:
    - <u>*First-Failure Data Capture (FFDC) Service*</u>: supports common exceptions and error handling.
    - <u>*Metadata Security*</u>: supports authorization of access to OMAG Services and specific metadata instances. 
    - <u>*Repository Handle*</u>: supports access to multiple related metadata instances from the OMRS. It checks and translates exceptions of repository services into exceptions that are used in access services (OMASs).

- **`user-security`**: these modules use mechanisms based on tokens to be used as an authentication method; they are distributed to runtime modules and connectors such as security connectors via thread. The main module is the <u>*token-manager*</u> which provides the classes to extract the authorization headers from an incoming HTTP request and add them to thread local storage. 

### 1.2 Integration Daemon Component Diagram
Questo container ospita il motore di sincronizzazione continua. Al suo interno troviamo:
- **`adapters`**: Sono i *connector* pluggable che implementano la comunicazione con i tool proprietari.
- **`frameworks`**: Definisce le interfacce standardizzate necessarie per costruire i connettori.

