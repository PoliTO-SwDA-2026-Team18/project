# Architecture — Section A: Context Level (C4 — Level 1)

> **Owner:** Viorel Strogoteanu  
> **Status:** Completed

<!-- 
Required content:
- C4 Context Diagram
- Explanation: external actors, external systems, analyzed system at the center
- Diagram: ../../../diagrams/c4/context.puml
-->

## Diagram

`../../../diagrams/c4/context.puml`

## Description

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
