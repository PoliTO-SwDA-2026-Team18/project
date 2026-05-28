# Architecture — Section A: Context Level (C4 — Level 1)

> **Owner:** Viorel Strogoteanu
> **Status:** Completed

## Diagram

`../../../diagrams/c4/context.puml`

## Scope

Single OMAG Server Platform deployment. Cohort federation across multiple Egeria platforms is a runtime capability of OMRS, not a separate system at L1; it
surfaces in the Container diagram.

## External Actors

Actors are grouped by **functional role** (what they do with metadata), not by job title or organisational team: this is stable across reorganisations and aligns with the View Services that Egeria exposes per role.

| Actor                      | Identity                                                                                     |
| -------------------------- | -------------------------------------------------------------------------------------------- |
| **Information Architect**  | Domain expert designing the canonical metadata model — types, glossaries, governance models. |
| **Data Steward**           | Owner of asset quality and metadata correctness; curates assets and handles exceptions.      |
| **Asset Consumer**         | Analyst, data engineer or product user searching the catalogue for usable data.              |
| **Platform Administrator** | DevOps / SRE responsible for deploying, configuring and operating Egeria.                    |

Compliance / Privacy / Security Officers are not a separate actor: their work splits between Information Architect (writing policies) and Data Steward (enforcing them) at L1 granularity.

## External Systems

| System                    | Why it is external                                                                                                                     |
| ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| **Data Sources**          | Heterogeneous origins of metadata (databases, lakes, file systems, warehouses). Egeria does not own them; integration connectors crawl |
| them.                     |
| **Data Tools**            | BI, ETL and data science platforms that produce or consume metadata via Egeria's REST APIs.                                            |
| **Apache Kafka**          | Event backbone for asynchronous metadata change events and cohort federation. Real out-of-process service; the in-memory fallback      |
| exists only for dev/test. |

Three systems are deliberately **not** at L1:

- The **Egeria React UI** lives in a separate repository: it is the access channel for human users and appears at L2.
- **Identity Provider, configuration store and secrets store** are infrastructure details reached through pluggable connectors; they appear at L2/L3.

## Key Interactions

| Flow                                            | Intent                                                                                                                               |
| ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Architect / Steward / Consumer / Admin → Egeria | Each actor invokes the metadata, governance or admin operations relevant to their role.                                              |
| Egeria → Data Sources                           | Egeria **pulls** schema, lineage and statistics through integration connectors that run inside the platform.                         |
| Egeria ↔ Apache Kafka                           | Egeria publishes and consumes Open Metadata change events; the platform connects to the broker as both publisher and subscriber.     |
| Data Tools → Egeria                             | BI / ETL tools **call Egeria's REST APIs** to read catalogue metadata and to push lineage / audit events. The tools initiate; Egeria |
| does not push to them.                          |

Arrows are unidirectional and labelled with intent. Protocol detail belongs in the Container diagram.

## Design notes

- **Pull-first for Data Sources.** Integration connectors live inside Egeria and poll or observe the sources. The push model (sources emitting events to
  Kafka or to a REST endpoint) exists but is the minority case and is captured at L2.
- **Tools initiate, not Egeria.** Outbound notifications to data tools, when they happen, travel via Kafka rather than via direct calls from Egeria —
  therefore the only L1 arrow between Egeria and Data Tools is _inbound_.
- **Single platform at L1.** Modelling a cohort as N separate systems at L1 would suggest each platform is independently usable, which is misleading: the
  cohort is a federation property of a single Egeria deployment, not a separate product.
