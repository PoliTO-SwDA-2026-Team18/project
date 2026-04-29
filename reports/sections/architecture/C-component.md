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

The modules of Egeria are about 14 and i've decided to analyze two of them that are the most important for the flow of metadata.  

Diagrammi PlantUML

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
In this container there are tools for a continued syncronization:

- **`adapters`**: connectors that implement the comunication with owners tools.

- **`frameworks`**: define the interfaces for pluggable components, these components provide much of the customization and technology integration points offered by the open metadata and governance implementation. Depending by the context there are several types like:
    - *Metadata*: basic definitions for metadata types.
    - *Connector*: interfaces for components that access real-world digital resources.
    - *Watchdog*: monitoring for events and issues actions to report.


## 2. Justify any decisions to exclude specific containers from analysis

I decided to exclude peripheral containers (such as the *View Server*, UI applications, or pure administrative/platform chassis services) because they do not handle the core business logic of metadata federation and synchronization. I've done a "zoom in" on the most important and complex containers. Modules like `repository-services`, `access-services`, `adapters`, and `frameworks` act as the central hubs of the system, possessing the highest number of inter-module dependencies. Focusing on the *Metadata Access Server* and *Integration Daemon* provides the best way for understanding Egeria's architecture.


## 3. SOLID Principle Violations at Level 3

### 3.1 Single Responsability Principle (SRP)
According to this principle there should be only one actor responsable of changes in each class or module. 
We can see that this principle is violated for exsample by `JacquardIntegrationConnector`, which is responsable to assemble all the **Open Metadata Digital Product Catalog** that is composed by several components like catalogs, glossaries or dictionaries. Each of them has its own set of elements and properties.

### 3.2 Open/Closed Principle (OCP)
The system should be open for extension but closed for modification. 
Egeria allows the addition of new adapters without overturn the code. However, if a completely new standard of metadata is introduced, all the core as *access-services* or *repository-services* might require great modifications on the logic, not only extensions of interfaces, and as conseguence there's the OCP violation.

### 3.3 Interface Segregation Principle (ISP)
Each actor should have its own interface composed by the elements that are effectively used by him, not a general interface where everything is putted inside it and several components aren't used depending by the actor. This violation is marked in the `OMRSMetadataCollection`, a module situated in the *repository-services-apis*, which contains all methods that manages entities, relationships etc., so if an actor needs only some part of that must depend by all the entire interface.

### 3.4 Liskov Substitution Principle (LSP)
Objects of a superclass shall be replaceable with objects of its subclasses without breaking the application.
In a project too big like this, it's impossible to have metadata tools that support every operation of the interface, infact even if there are a lot of *adapters* they can throw exceptions; this represents a violation of the principle causing a crash of the application.

### 3.5 Dependency Inversion Principle (DIP)
High-level modules should not depend on low-level modules; both should depend on abstractions. 
Especially within the `frameworks` module, there are still instances of tight coupling where high-level modules depend on concrete implementations. An example is found in the `OMAGServerPlatformCatalogConnector`, which directly instantiates the concrete class `SoftwareServerProperties` via the `new` keyword: 
SoftwareServerProperties softwareServerProperties = new SoftwareServerProperties();
