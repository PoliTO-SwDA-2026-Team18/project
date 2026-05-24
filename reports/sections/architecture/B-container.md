# Architecture — Section B: Container Level (C4 — Level 2)

> **Owner:** Viorel Strogoteanu  
> **Status:** Completed

<!-- 
Required content:
- C4 Container Diagram
- Explanation: applications, databases, services of the system
- Mandatory question: relationship with Clean Architecture (justify)
- Diagram: ../../../diagrams/c4/container.puml
-->

## Diagram

`../../../diagrams/c4/container.puml`

## Description

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

## Relationship with Clean Architecture

Clean Architecture organizes software into concentric layers where source-code dependencies can only point inward: Frameworks & Drivers → Interface Adapters → Use Cases → Entities. The inner layers know nothing about the outer ones.

Egeria's container layout maps closely onto this blueprint:

- **Entities** → the Open Metadata Type System and governance rules defined inside **Repository Services (OMRS)**. These core business objects have no dependency on web frameworks, databases, or external tooling.

- **Use Cases** → also **Repository Services**. Cohort federation, metadata event pub/sub, and audit management are application-level business rules that orchestrate entities without knowing how they are exposed or stored.

- **Interface Adapters** → **OMAG Server Platform**. Spring Boot controllers translate incoming HTTP requests into domain calls and format domain objects into REST responses. View Services and Access Services act as role-specific adapters between the domain and the outside world.

- **Frameworks & Drivers** → **Data Repository (PostgreSQL), Message Bus (Kafka), Configuration Store, Secrets Management, Authentication Service, Data Sources**. All of these are replaceable infrastructure. PostgreSQL, Kafka, YAML files, and LDAP are concrete implementations of abstract interfaces defined by the inner layers — the connector abstraction in `frameworks/` enforces this boundary, so the domain never depends on a specific technology.

The main deviation from strict Clean Architecture is that the **OMAG Server Platform publishes directly to the Message Bus** without going through Repository Services. This means that a container in the Interface Adapters layer (OMAG) communicates directly with a container in the Frameworks & Drivers layer (Kafka), skipping the Use Case layer entirely — which breaks the strict inward-only dependency rule. It is a pragmatic trade-off to avoid routing every real-time notification through the metadata engine.
