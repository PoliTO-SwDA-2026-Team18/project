# Software Architecture

## Context Level (C4 — Level 1)

### Diagram

`../../../diagrams/c4/context.puml`

### Description

The context diagram places **Egeria Platform** at the center as a single black box, showing every external actor and system that interacts with it without exposing any internal structure.

### External Actors

| Actor | Description |
|---|---|
| **Data Platform Users** | Collective actor covering Data Engineers, Data Officers, Data Stewards, and Analysts. They interact with Egeria to search and manage metadata, create business glossaries, and consume governance outputs. |
| **Platform Administrators** | DevOps, SRE, and Platform team members responsible for deploying, configuring, and monitoring Egeria servers via the Admin REST APIs. |
| **Data Governance Teams** | Compliance, Privacy, and Security Officers who define governance policies, audit requirements, and consume compliance reports. |

All three actors are grouped by _role_ rather than job title. Individual roles (e.g. Data Designer, Security Officer) are served by dedicated view services and appear at component level.

### External Systems

| System | Description |
|---|---|
| **Data Sources** | SQL databases, file systems, Kafka topics, data lakes, and data platforms (e.g. Databricks Unity Catalog). Egeria crawls and catalogs their metadata via integration connectors. |
| **External Tools** | BI tools, ETL platforms, data catalogs, and analytics platforms that exchange metadata with Egeria through REST APIs. |
| **Message Bus** | Apache Kafka, used as the event-streaming backbone for asynchronous metadata change events and federation notifications. |

Configuration management and secrets storage are intentionally excluded at this level: they are internal infrastructure details that appear in the Container diagram.

### Key Interactions

| Flow | Protocol | Intent |
|---|---|---|
| Data Platform Users → Egeria | HTTP REST (token auth) | Request metadata, submit governance actions |
| Egeria → Data Platform Users | HTTP REST | Expose search results, metadata APIs |
| Platform Administrators → Egeria | HTTP REST (Admin APIs) | Configure platform, manage server lifecycle |
| Egeria → Platform Administrators | HTTP REST | Server status, operational metrics |
| Data Governance Teams → Egeria | HTTP REST | Create policies and audit rules |
| Egeria → Data Governance Teams | HTTP REST | Compliance reports, governance status |
| Egeria ↔ Data Sources | Integration Connectors (JDBC, native APIs) | Discover schema, lineage, and statistics |
| Egeria ↔ Message Bus | Kafka Pub/Sub | Publish and subscribe to metadata change events |
| Data Sources → Message Bus | Kafka | Publish lineage and audit events |
| Egeria ↔ External Tools | REST APIs | Export metadata, policies; receive discovery requests |

All labels use intent rather than technical detail, following C4 context-level conventions.

## Container Level (C4 — Level 2)

### Diagram

`../../../diagrams/c4/container.puml`

### Description

The container diagram opens the Egeria Platform black box and shows the six major deployable units and how they communicate.

### Containers

| Container | Technology | Responsibility |
|---|---|---|
| **OMAG Server Platform** | Java 17, Spring Boot | Main entry point for all HTTP traffic. Hosts View Services (26 domain APIs), Access Services (metadata management), Admin Services (server lifecycle), and Platform Services. |
| **Repository Services (OMRS)** | Java, event-driven | Core metadata engine. Handles metadata federation across cohorts, event publishing/subscription, and audit logging. |
| **Data Repository** | PostgreSQL | Persistent storage for metadata, type definitions, and audit logs. XTDB and in-memory connectors are available as alternatives for temporal queries and testing respectively. |
| **Message Bus** | Apache Kafka | Asynchronous event streaming for metadata changes, cohort federation events, and notifications. Decouples the repository from downstream consumers. |
| **Configuration Store** | File-based (YAML/JSON) | Stores server configurations, connector definitions, and deployment settings. Extensible to etcd or Vault for production-grade configuration management. |
| **Secrets Management** | File-based (YAML) | Stores credentials, API keys, and encryption tokens. Designed to be replaced by Vault or AWS Secrets Manager in production deployments. |

### Internal Interactions

| From | To | Protocol | Intent |
|---|---|---|---|
| OMAG Server Platform | Repository Services | Java API | Metadata queries and governance operations |
| OMAG Server Platform | Configuration Store | File / REST API | Read server configuration on startup and at runtime |
| OMAG Server Platform | Secrets Management | Secure API call | Retrieve credentials and API keys |
| OMAG Server Platform | Message Bus | Kafka API | Publish and subscribe to REST-triggered events |
| Repository Services | Data Repository | JDBC SQL | Persist and retrieve metadata and audit logs |
| Repository Services | Message Bus | Kafka API | Publish metadata change events; subscribe to federation events |

### External Interactions

| From | To | Protocol | Intent |
|---|---|---|---|
| User | OMAG Server Platform | HTTP/HTTPS | All user-facing API calls |
| OMAG Server Platform | Authentication Service | LDAP / OAuth2 / OIDC | Validate user identity and retrieve authorization info |
| OMAG Server Platform | Data Sources | Integration Connectors (JDBC, native APIs) | Discover schema, lineage, and statistics |
| External Tools | OMAG Server Platform | REST APIs | Retrieve metadata; submit lineage and governance policies |
| Data Sources | Message Bus | Kafka API | Publish lineage and data quality events |

### Relationship with Clean Architecture

Clean Architecture organizes software into concentric layers where source-code dependencies can only point inward: Frameworks & Drivers → Interface Adapters → Use Cases → Entities. The inner layers know nothing about the outer ones.

Egeria's container layout maps closely onto this blueprint:

- **Entities** → the Open Metadata Type System and governance rules defined inside **Repository Services (OMRS)**. These core business objects have no dependency on web frameworks, databases, or external tooling.

- **Use Cases** → also **Repository Services**. Cohort federation, metadata event pub/sub, and audit management are application-level business rules that orchestrate entities without knowing how they are exposed or stored.

- **Interface Adapters** → **OMAG Server Platform**. Spring Boot controllers translate incoming HTTP requests into domain calls and format domain objects into REST responses. View Services and Access Services act as role-specific adapters between the domain and the outside world.

- **Frameworks & Drivers** → **Data Repository (PostgreSQL), Message Bus (Kafka), Configuration Store, Secrets Management, Authentication Service, Data Sources**. All of these are replaceable infrastructure. PostgreSQL, Kafka, YAML files, and LDAP are concrete implementations of abstract interfaces defined by the inner layers — the connector abstraction in `frameworks/` enforces this boundary, so the domain never depends on a specific technology.

The main deviation from strict Clean Architecture is that the **OMAG Server Platform publishes directly to the Message Bus** without going through Repository Services. This means that a container in the Interface Adapters layer (OMAG) communicates directly with a container in the Frameworks & Drivers layer (Kafka), skipping the Use Case layer entirely — which breaks the strict inward-only dependency rule. It is a pragmatic trade-off to avoid routing every real-time notification through the metadata engine.


## Component Level (C4 — Level 3)

### 1. C4 Component Diagrams for Relevant Containers

The modules of Egeria are about 14 and i've decided to analyze two of them that are the most important for the flow of metadata.  

#### 1.1 Metadata Access Server (OMAS) Component Diagram

`../../../diagrams/c4/component-metadata-access-server.puml`

![Metadata Access Server component diagram](../../images/component-metadata-access-server.svg)

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

#### 1.2 Integration Daemon Component Diagram

`../../../diagrams/c4/component-integration-daemon.puml`

![Integration Daemon component diagram](../../images/component-integration-daemon.svg)

In this container there are tools for a continued syncronization:

- **`adapters`**: connectors that implement the comunication with owners tools.

- **`frameworks`**: define the interfaces for pluggable components, these components provide much of the customization and technology integration points offered by the open metadata and governance implementation. Depending by the context there are several types like:
    - *Metadata*: basic definitions for metadata types.
    - *Connector*: interfaces for components that access real-world digital resources.
    - *Watchdog*: monitoring for events and issues actions to report.


### 2. Justify any decisions to exclude specific containers from analysis

I decided to exclude peripheral containers (such as the *View Server*, UI applications, or pure administrative/platform chassis services) because they do not handle the core business logic of metadata federation and synchronization. I've done a "zoom in" on the most important and complex containers. Modules like `repository-services`, `access-services`, `adapters`, and `frameworks` act as the central hubs of the system, possessing the highest number of inter-module dependencies. Focusing on the *Metadata Access Server* and *Integration Daemon* provides the best way for understanding Egeria's architecture.


### 3. SOLID Principle Violations at Level 3

#### 3.1 Single Responsability Principle (SRP)
According to this principle there should be only one actor responsable of changes in each class or module. 
We can see that this principle is violated for exsample by `JacquardIntegrationConnector`, which is responsable to assemble all the **Open Metadata Digital Product Catalog** that is composed by several components like catalogs, glossaries or dictionaries. Each of them has its own set of elements and properties.

```java
public class JacquardIntegrationConnector extends CatalogIntegratorConnector {
    // The same class assembles unrelated concerns:
    private void refreshDigitalProductCatalog()  { ... }
    private void refreshGlossaries()             { ... }
    private void refreshDataDictionaries()       { ... }
    private void refreshReferenceData()          { ... }
    private void refreshGovernanceActions()      { ... }
}
```

#### 3.2 Open/Closed Principle (OCP)
The system should be open for extension but closed for modification. 
Egeria allows the addition of new adapters without overturn the code. However, if a completely new standard of metadata is introduced, all the core as *access-services* or *repository-services* might require great modifications on the logic, not only extensions of interfaces, and as conseguence there's the OCP violation.

```java
// Adding a brand-new standard means extending core enums/switches
// scattered across access-services and repository-services:
public enum AccessServiceDescription {
    OCF_METADATA_MANAGEMENT(...),
    OMF_METADATA_MANAGEMENT(...),
    GAF_METADATA_MANAGEMENT(...);
    // NEW_STANDARD_MANAGEMENT(...)  <-- requires modifying this enum
}
```

#### 3.3 Interface Segregation Principle (ISP)
Each actor should have its own interface composed by the elements that are effectively used by him, not a general interface where everything is putted inside it and several components aren't used depending by the actor. This violation is marked in the `OMRSMetadataCollection`, a module situated in the *repository-services-apis*, which contains all methods that manages entities, relationships etc., so if an actor needs only some part of that must depend by all the entire interface.

```java
public abstract class OMRSMetadataCollection {
    public abstract TypeDefGallery getAllTypes(...);
    public abstract EntityDetail addEntity(...);
    public abstract EntityDetail updateEntityProperties(...);
    public abstract List<EntityDetail> findEntitiesByProperty(...);
}
```

#### 3.4 Liskov Substitution Principle (LSP)
Objects of a superclass shall be replaceable with objects of its subclasses without breaking the application.
In a project too big like this, it's impossible to have metadata tools that support every operation of the interface, infact even if there are a lot of *adapters* they can throw exceptions; this represents a violation of the principle causing a crash of the application.

```java
// A concrete repository connector cannot honour the full contract:
@Override
public EntityDetail isEntityKnown(String userId, String guid)
        throws FunctionNotSupportedException {
    throw new FunctionNotSupportedException(
            OMRSErrorCode.METHOD_NOT_IMPLEMENTED.getMessageDefinition(),
            this.getClass().getName(), "isEntityKnown");
}
```

#### 3.5 Dependency Inversion Principle (DIP)
High-level modules should not depend on low-level modules; both should depend on abstractions. 
Especially within the `frameworks` module, there are still instances of tight coupling where high-level modules depend on concrete implementations. An example is found in the `OMAGServerPlatformCatalogConnector`, which directly instantiates the concrete class `SoftwareServerProperties` via the `new` keyword: 

```java
SoftwareServerProperties softwareServerProperties = new SoftwareServerProperties();
softwareServerProperties.setQualifiedName(...);
```

The same connector also pattern-matches against the concrete type instead of an abstraction:

```java
if (softwareServer.getProperties()
        instanceof SoftwareServerProperties softwareServerProperties) {
    softwareServerProperties.getDeployedImplementationType();
}
```

## Architectural Characteristics

### 1. Architectural Qualities

- **Extensibility**: is the best quality of Egeria. The presence of plug-in patterns like `frameworks` and `adapters` allows for major extensions in the project, adding new standards and connectors without overturning the system.
- **Scalability**: is a consequence of the division into multiple containers (e.g., *Metadata Access Server*, *Integration Daemon*). The system achieves horizontal scalability of OMAG servers depending on their load.
- **Maintainability**: several modules are separated by responsibility (`access-services`, `repository-services`, `common-services`), which allows for fast management of errors and changes in the code. However, some containers are related, making it difficult to find errors and make changes in those specific areas.
- **Security**: managed by the `user-security` module, which implements a token-based authentication and authorization system (`token-manager` module) ensuring isolation for concurrent requests. The module `common-services` contains the *Metadata Security* service that manages access to individual metadata instances.
- **Performance**: optimized by the presence of connectors which, when there is a change, publish an event on a notification channel that is immediately received by all other tools to be updated. This is an event-driven architecture and allows a real-time synchronization of data in the system.


### 2. Coupling and Cohesion

A structural and co-change analysis (Design report, Sections A1 and A2) reveals a system with a strongly coupled core and uneven cohesion across modules.

*   **Cohesion**:
    *   **Low**: `JacquardIntegrationConnector` is a clear example of low cohesion because has a big number of outgoing imports, it handles too many responsibilities (catalogs, glossaries, dictionaries etc.), violating the Single Responsibility Principle.
    *   **High**: `CommunityMattersResource`, by contrast, shows high cohesion. It delegates all logic to `CommunityMattersRESTServices`, resulting in a single Egeria import and a very focused responsibility.

*   **Structural coupling (code)**:
    *   **Central hubs**: `frameworks`, `repository-services`, and `access-services` act as architectural hubs, with `frameworks` being the most critical — imported by almost every other module.
    *   **SOLID-driven coupling**: the coupling is amplified by SOLID violations such as the "fat" interface `OMRSMetadataCollection` (ISP) and the direct instantiation of concrete classes like `SoftwareServerProperties` (DIP).

*   **Logical coupling (co-change)**:
    *   **Over-coupling**: the *Search Executor* classes (e.g., `FindEntitiesBy…Executor`) are frequently modified together, suggesting duplicated logic — a form of unnecessary coupling.
    *   **Hidden dependencies**: content-pack files (`.omarchive`) are almost always modified together (≈100% coupling), forming a single logical unit. This "knowledge dependency" is invisible to static code analysis but is critical for maintainability.

