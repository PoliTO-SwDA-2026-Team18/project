# Architecture — Section B: Container Level (C4 — Level 2)

> **Owner:** Viorel Strogoteanu  
> **Status:** Completed

## Diagram

`../../../diagrams/c4/container.puml`

## Scope

Each OMAG Server type runs as an independent Spring Boot process on an OMAG Server Platform. They can share one platform instance (dev/test) or be distributed across multiple instances (production). The diagram models the production-style distributed case, where each server type is a separate deployable unit.

## Relationship with Clean Architecture

Clean Architecture (Robert C. Martin) organises source-code dependencies into four concentric rings — Entities, Use Cases, Interface Adapters, Frameworks & Drivers — with one strict rule: **dependencies can only point inward**. Outer rings know about inner rings; inner rings know nothing about outer ones. The goal is to keep domain logic independent from infrastructure so that databases, frameworks, and external tools are swappable without touching business rules.

Egeria's container layout maps onto those rings as follows:

| Clean Architecture ring | Egeria container | Why |
| --- | --- | --- |
| **Entities** | Core of the **Metadata Access Server** (OMRS) | The Open Metadata Type System — canonical types, relationships, classifications — is pure domain. No dependency on Spring, Kafka, or any database. |
| **Use Cases** | Also the **Metadata Access Server** (OMAS) | The Access Services (Asset Manager, Data Manager, Governance Program…) implement application-level metadata workflows. They orchestrate types without knowing how they are stored or transported. |
| **Interface Adapters** | **View Server, Integration Daemon, Engine Host, Repository Proxy** | Each translates between an external concern and the metadata core: the View Server adapts HTTP UI requests into OMAS calls; the Integration Daemon translates third-party data formats into Open Metadata Types; the Repository Proxy maps a foreign repository's model onto OMRS. They all depend on MAS; they do not depend on each other. |
| **Frameworks & Drivers** | **Metadata Repository, Apache Kafka, Data Sources, Third-party Repositories, Egeria React UI** | Concrete infrastructure. Replaceable without touching the business rules, because each is reached through an abstraction defined by the inner layers (Repository Connector, Open Metadata Topic Connector, Integration Connector). |

**Dependency rule check.** The arrows in the diagram respect the inward rule:
- View Server → MAS, Integration Daemon → MAS, Engine Host → MAS: adapters calling the core. ✓
- MAS → Metadata Repository: the dependency is on the *Repository Connector interface* (defined inside OCF, the core framework), not on PostgreSQL or in-memory directly. The concrete driver lives in the outermost ring and is injected at startup. ✓
- MAS → Apache Kafka: similarly mediated by the *Open Metadata Topic Connector* abstraction. ✓

**Main deviations from strict Clean Architecture:**

1. **Collapsed inner rings.** MAS bundles both the Entity layer (OMRS, type system) and the Use Case layer (OMAS business rules) into one deployable unit. The boundary between them exists in the source code but is invisible at L2; it only becomes visible at L3. This is a deliberate design choice: separating OMRS and OMAS into two independent processes would create distributed coupling with no architectural gain, since every OMAS call needs synchronous access to the type system.
2. **Framework ubiquity.** All five OMAG Server types are built on Spring Boot, meaning the Frameworks & Drivers ring is present inside every container. This is an unavoidable characteristic of microservice architectures. The risk — that framework concerns bleed into business logic — is mitigated by the OCF connector boundary, which forces all infrastructure access through interfaces owned by the inner layers.
