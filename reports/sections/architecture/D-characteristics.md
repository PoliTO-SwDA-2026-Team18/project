# Architecture — Section D: Architectural Characteristics

> **Owner:** Matteo Francesco Castigliego  
> **Status:** To be completed

<!-- 
Required content:
- System's architectural qualities (scalability, maintainability, security, performance, availability, etc.)
- How the architecture supports them
- Component coupling and cohesion metrics (recommended)
-->

## 1. Architectural Qualities

- **Extensibility**: is the best quality of Egeria. The presence of plug-in patterns like `frameworks` and `adapters` allows for major extensions in the project, adding new standards and connectors without overturning the system.
- **Scalability**: is a consequence of the division into multiple containers (e.g., *Metadata Access Server*, *Integration Daemon*). The system achieves horizontal scalability of OMAG servers depending on their load.
- **Maintainability**: several modules are separated by responsibility (`access-services`, `repository-services`, `common-services`), which allows for fast management of errors and changes in the code. However, some containers are related, making it difficult to find errors and make changes in those specific areas.
- **Security**: managed by the `user-security` module, which implements a token-based authentication and authorization system (`token-manager` module) ensuring isolation for concurrent requests. The module `common-services` contains the *Metadata Security* service that manages access to individual metadata instances.
- **Performance**: optimized by the presence of connectors which, when there is a change, publish an event on a notification channel that is immediately received by all other tools to be updated. This is an event-driven architecture and allows a real-time synchronization of data in the system.


## 2. Coupling and Cohesion

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
