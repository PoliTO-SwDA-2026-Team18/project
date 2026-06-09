# Architecture — Section D: Architectural Characteristics

> **Owner:** Matteo Francesco Castigliego  
> **Status:** Completed

## Architectural Style

Egeria follows a **modular, plugin-based, event-driven service architecture**. The system is decomposed into a set of independent OMAG Servers (Metadata Access Server, Integration Daemon, Engine Host, View Server, Repository Proxy), each deployable and scalable independently (modular). All cross-server and cross-repository communication is mediated by two mechanisms: synchronous REST calls for request/response interactions, and asynchronous Apache Kafka topics for metadata change propagation and cohort federation (event-drien). Extensibility is built into the core through the `frameworks` abstraction layer, which defines pluggable interfaces that connectors and adapters implement without touching the platform internals (plugin-based).

This is not a microservices architecture in the strict DDD sense: the OMAG Servers share a common Metadata Repository and do not own independent data stores per domain. It is better described as a **federated metadata platform** where modularity is achieved at the connector and service level rather than at the data ownership level.

---

## 1. Architectural Qualities

- **Extensibility**: the defining quality of Egeria. The `frameworks` + `adapters` plugin model allows new connectors, metadata standards, and governance services to be added without modifying the platform core. New integrations require only a new provider/connector pair implementing the relevant framework interface.

- **Scalability**: each OMAG Server type is an independently deployable Spring Boot process. This means the Integration Daemon (responsible for metadata ingestion from external tools) and the Engine Host (responsible for governance automation) can be scaled horizontally and independently of the Metadata Access Server, based on their respective workloads. Multiple Integration Daemons can run in parallel against different data sources without any coordination overhead on the MAS side.

- **Maintainability**: the separation of concerns across modules (`access-services`, `repository-services`, `common-services`) allows localised changes to most of the codebase. However, `frameworks` acts as a central hub imported by almost every other module (Design report, Section A1), which means changes to core framework interfaces have a wide blast radius and must be managed carefully.

- **Security**: the `user-security` component extracts authentication tokens from incoming HTTP headers and propagates credentials via thread-local storage to all runtime modules and connectors, ensuring per-request isolation. Authorisation at the metadata instance level is handled separately by the *Metadata Security* sub-module within `common-services`.

- **Performance**: the event-driven backbone — Apache Kafka topics for OMRS cohort events and OMAS in/out topics — decouples producers from consumers and allows metadata changes to propagate asynchronously across the entire cohort in near real time, without polling. This avoids synchronous fan-out to all subscribers on every write operation.

- **Resilience**: the use of Kafka as an intermediary means that downstream consumers (Integration Daemon adapters, external tools) can be temporarily unavailable without causing the Metadata Access Server to fail or block. An in-memory fallback is available for development and testing scenarios where a Kafka broker is not present.

---

## 2. Coupling and Cohesion

A structural and co-change analysis (Design report, Sections A1 and A2) reveals a system with a strongly coupled core and uneven cohesion across modules.

- **Cohesion**:
    - **Low**: `JacquardIntegrationConnector` is a clear example of low cohesion. It handles too many unrelated responsibilities (catalogs, glossaries, dictionaries, governance actions), violating the Single Responsibility Principle and accumulating the highest outgoing import count in the codebase (56 imports).
    - **High**: `CommunityMattersResource`, by contrast, shows high cohesion. It exposes HTTP endpoints and immediately delegates all logic to `CommunityMattersRESTServices`, resulting in a single Egeria import and a tightly focused responsibility.

- **Structural coupling (code)**:
    - **Central hubs**: `frameworks`, `repository-services`, and `access-services` act as architectural hubs. `frameworks` is the most critical, imported by almost every other module in the system. This is a deliberate design decision — it is the abstraction layer that all connectors depend on — but it means changes to framework interfaces carry the highest propagation risk.
    - **SOLID-driven coupling**: coupling is amplified by SOLID violations such as the fat interface `OMRSMetadataCollection` (ISP) and the direct instantiation of concrete classes like `SoftwareServerProperties` (DIP), which prevent the compiler from enforcing the boundary between abstraction and implementation.

- **Logical coupling (co-change)**:
    - **Over-coupling**: Search Executor classes (e.g., `FindEntitiesByClassificationExecutor` vs `FindEntitiesByPropertyValueExecutor`) are frequently modified together despite being separate classes, suggesting duplicated logic. A common abstract base would reduce this unnecessary co-evolution.
    - **Hidden dependencies**: content-pack files (`.omarchive`) exhibit approximately 100% co-change coupling, meaning they effectively form a single logical unit despite being physically separate files. This knowledge dependency is invisible to static analysis tools but represents a significant maintainability risk, as it is undocumented and can only be detected through historical change data.
