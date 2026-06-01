# Architecture — Section C: Component Level (C4 — Level 3)

> **Owner:** Matteo Francesco Castigliego  
> **Status:** Completed

## 1. C4 Component Diagrams for Relevant Containers

Egeria comprises approximately 14 OMAG Server types. The two analysed here — **Metadata Access Server** and **Integration Daemon** — are the most relevant for understanding the core metadata flow, as confirmed by the dependency analysis (Design report, Section A1), where `repository-services`, `access-services`, `adapters`, and `frameworks` account for the highest inter-module import counts in the entire codebase.

### 1.1 Metadata Access Server Component Diagram

`../../../diagrams/c4/component-metadata-access-server.puml`

![Metadata Access Server component diagram](../../images/component-metadata-access-server.svg)

The Metadata Access Server is the central container of the architecture. It is called by four distinct containers — **View Server**, **Integration Daemon**, **Engine Host**, and **Platform Administrator** — each with a dedicated interaction, and internally it is structured into four components:

- **`access-services (OMAS)`**: the REST API layer for all metadata operations. It is divided into domain-specific sub-modules: *ocf-metadata-management* for the Open Connector Framework (OCF), *omf-metadata-management* for the Open Metadata Framework (OMF), and *gaf-metadata-management* for the Open Governance Framework (OGF). Each sub-module exposes its own set of properties and APIs.

- **`repository-services (OMRS)`**: the federation engine. Its purpose is to allow independent metadata repositories to exchange metadata regardless of the underlying technology or vendor — effectively eliminating metadata silos by linking repositories into a cohort. It is composed of several sub-modules:
    - *apis*: connector interfaces and event structures for the repository services.
    - *archive-utilities*: common utilities for building Open Metadata Archives.
    - *client*: two client implementations — the *Local Repository Services Client* for calls to a local repository and the *Enterprise Repository Services Client* for calls to the enterprise-wide federated repository.
    - *implementation*: peer-to-peer metadata exchange and cohort federation logic.
    - *spring*: Spring annotations that expose OMRS capabilities as REST services.

- **`common-services`**: shared Java utilities consumed by both clients and the specialised services running in the OMAG Server. Key sub-modules include:
    - *First-Failure Data Capture (FFDC) Service*: common exception handling and error reporting.
    - *Metadata Security*: authorisation of access to OMAG services and individual metadata instances.
    - *Repository Handler*: mediates access to multiple related metadata instances from OMRS, translating repository-level exceptions into the exception types used by the access services.

- **`user-security`**: token-based authentication layer. Credentials extracted from incoming HTTP request headers are stored in thread-local storage and propagated to runtime modules and security connectors. The core sub-module is *token-manager*, which implements this extraction and distribution mechanism.

### 1.2 Integration Daemon Component Diagram

`../../../diagrams/c4/component-integration-daemon.puml`

![Integration Daemon component diagram](../../images/component-integration-daemon.svg)

The Integration Daemon is responsible for the continuous, bidirectional synchronisation of metadata between Egeria and third-party technologies. It is structured into two components:

- **`adapters`**: concrete integration connectors that implement communication with specific external tools (BI platforms, ETL tools, data catalogues, etc.). Each adapter translates between the tool's proprietary format and Egeria's Open Metadata Types. Adapters push and pull metadata to and from the Metadata Access Server via the paired OMAS, and subscribe to metadata change events from Apache Kafka to stay synchronised in real time.

- **`frameworks`**: pluggable interfaces that define the contracts for all integration components. They provide the customisation and technology-integration points of the open metadata and governance implementation. There are three main interface families:
    - *Metadata*: base definitions for Open Metadata Types.
    - *Connector*: interfaces for components that access real-world digital resources.
    - *Watchdog*: event-monitoring interfaces that trigger actions in response to metadata changes.


## 2. Justify Any Decisions to Exclude Specific Containers from Analysis

The **View Server**, **Engine Host**, and **Repository Proxy** were excluded from the component-level analysis for the following reasons:

- *View Server*: a thin adapter layer that translates HTTP UI requests into OMAS calls. It contains no domain logic of its own; its behaviour is fully determined by the access services it delegates to.
- *Engine Host*: hosts governance engines that execute automated actions. Its internal structure mirrors the Integration Daemon (engine services + frameworks) but with narrower scope; the patterns are already covered by the Integration Daemon analysis.
- *Repository Proxy*: a cohort member whose sole responsibility is mapping a third-party repository's API to OMRS events. It does not host business logic and its internal structure is connector-level detail, not architectural.

The two chosen containers — Metadata Access Server and Integration Daemon — hold the highest concentration of cross-module dependencies (Design report, Section A1) and together cover the full metadata lifecycle: ingestion, federation, persistence, and event propagation.


## 3. SOLID Principle Violations at Level 3

### 3.1 Single Responsibility Principle (SRP)

According to this principle, each class or module should have exactly one reason to change. This principle is violated by `JacquardIntegrationConnector`, which is responsible for assembling the entire **Open Metadata Digital Product Catalog** — a concern that spans product catalogs, glossaries, data dictionaries, reference data, and governance actions, each with its own property beans and element types, all within a single class.

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

### 3.2 Open/Closed Principle (OCP)

The system should be open for extension but closed for modification. Egeria supports adding new adapters without changing existing code. However, introducing an entirely new metadata standard requires modifying core enums in `access-services` and `repository-services` rather than extending an interface — a direct OCP violation.

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

### 3.3 Interface Segregation Principle (ISP)

Clients should not be forced to depend on interfaces they do not use. This principle is violated by `OMRSMetadataCollection`, located in *repository-services-apis*, which aggregates all methods for managing entities, relationships, types, and classifications into a single abstract class. Any component that needs only a subset of these operations must still depend on the entire interface.

```java
public abstract class OMRSMetadataCollection {
    public abstract TypeDefGallery getAllTypes(...);
    public abstract EntityDetail addEntity(...);
    public abstract EntityDetail updateEntityProperties(...);
    public abstract List<EntityDetail> findEntitiesByProperty(...);
}
```

### 3.4 Liskov Substitution Principle (LSP)

Objects of a superclass should be replaceable by objects of any subclass without altering the correctness of the program. In a codebase of this scale, it is not feasible for every repository connector to support the full operation set defined by the superclass. Concrete adapters routinely throw `FunctionNotSupportedException`, breaking the substitutability contract and potentially causing runtime failures in callers that assume full interface compliance.

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

### 3.5 Dependency Inversion Principle (DIP)

High-level modules should not depend on low-level modules; both should depend on abstractions. Despite the general use of connector interfaces throughout the codebase, violations still appear: `OMAGServerPlatformCatalogConnector` directly instantiates the concrete class `SoftwareServerProperties` via `new`, and pattern-matches against its concrete type instead of programming to an abstraction.

```java
SoftwareServerProperties softwareServerProperties = new SoftwareServerProperties();
softwareServerProperties.setQualifiedName(...);
```

```java
if (softwareServer.getProperties()
        instanceof SoftwareServerProperties softwareServerProperties) {
    softwareServerProperties.getDeployedImplementationType();
}
```
