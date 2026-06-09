# Project — Egeria Analysis

Analysis of the open-source system **[Egeria](https://github.com/odpi/egeria)** — an open metadata and governance platform. The project produces three Markdown reports (Overview, Design, Architecture) along with supporting diagrams and individual journals.

### Analyzed System

|                      |                                                                                            |
| -------------------- | ------------------------------------------------------------------------------------------ |
| **Repository**       | [odpi/egeria](https://github.com/odpi/egeria)                                              |
| **Analyzed Release** | [V6.0](https://github.com/odpi/egeria/releases/tag/V6.0)                                   |
| **Reference Commit** | [`d893f299`](https://github.com/odpi/egeria/tree/d893f299defd372c7c571e6d8f934a127a2fbd75) |

---

## Repository Structure

```
project/
│
├── README.md                           # Repository overview
│
├── reports/
│   ├── overview.md                     # Report 1: System Overview
│   ├── design.md                       # Report 2: Software Design
│   ├── architecture.md                 # Report 3: Software Architecture
│   ├── images/                         # Images used in reports
│   └── sections/                       # Individual sections (assembled into final reports)
│       ├── design/
│       │   ├── A1-code-dependencies.md
│       │   ├── A2-knowledge-dependencies.md
│       │   ├── B-pattern-1.md
│       │   ├── B-pattern-2.md
│       │   ├── B-pattern-3.md
│       │   ├── B-pattern-4.md
│       │   └── C-summary.md
│       └── architecture/
│           ├── A-context.md
│           ├── B-container.md
│           ├── C-component.md
│           └── D-characteristics.md
│
├── diagrams/
│   ├── c4/
│   │   ├── context.puml                # C4 Diagram — Context (Level 1)
│   │   ├── container.puml              # C4 Diagram — Container (Level 2)
│   │   └── component-<name>.puml       # C4 Diagrams — Component (Level 3)
│   └── patterns/
│       └── pattern-<name>.puml         # Design pattern UML diagrams (4 patterns)
│
├── journals/
│   ├── gabriele-ferrero.md             # Individual journal — Gabriele Ferrero
│   ├── luca-ferrone.md                 # Individual journal — Luca Ferrone
│   ├── michele-castrucci.md            # Individual journal — Michele Castrucci
│   ├── federico-angeloni.md            # Individual journal — Federico Angeloni
│   ├── viorel-strogoteanu.md           # Individual journal — Viorel Strogoteanu
│   └── matteo-francesco-castigliego.md # Individual journal — Matteo Francesco Castigliego
│
├── analysis/
│   ├── data/                           # Raw data from analysis tools
│   ├── scripts/                        # Python scripts used for analysis
│   └── tools/                          # External tools
│
└── egeria/                             # Local clone / reference of the analyzed system
```

---

## Report Table of Contents

### [Overview](reports/overview.md)

- [Overview](reports/overview.md#overview)
  - [System Purpose](reports/overview.md#system-purpose)
  - [Principal Stakeholders](reports/overview.md#principal-stakeholders)
  - [System Description](reports/overview.md#system-description)
    - [Functional Overview](reports/overview.md#functional-overview)
    - [Technical Description](reports/overview.md#technical-description)
  - [Code Statistics](reports/overview.md#code-statistics)
    - [Language Breakdown](reports/overview.md#language-breakdown)
    - [Summary Metrics](reports/overview.md#summary-metrics)

### [Design](reports/design.md)

- [Software Design](reports/design.md#software-design)
  - [Code Dependencies](reports/design.md#code-dependencies)
    - [Methodology](reports/design.md#methodology)
    - [File Dependency Rankings](reports/design.md#file-dependency-rankings)
      - [Highest Outgoing Imports](reports/design.md#highest-outgoing-imports)
      - [Lowest Outgoing Imports](reports/design.md#lowest-outgoing-imports)
      - [Most Imported Files](reports/design.md#most-imported-files)
    - [Observed Structural (Code-Level) Dependencies](reports/design.md#observed-structural-code-level-dependencies)
      - [Implementation Dependency](reports/design.md#implementation-dependency)
      - [Construction Dependency](reports/design.md#construction-dependency)
      - [Compile-Time Dependency](reports/design.md#compile-time-dependency)
    - [Module Dependency Graph](reports/design.md#module-dependency-graph)
  - [Knowledge Dependencies](reports/design.md#knowledge-dependencies)
    - [Hub analysis](reports/design.md#hub-analysis)
    - [Coupling analysis](reports/design.md#coupling-analysis)
    - [Inconsistencies with code dependencies](reports/design.md#inconsistencies-with-code-dependencies)
      - [1. Connectors and Repository Architecture (Most Critical Area)](reports/design.md#1-connectors-and-repository-architecture-most-critical-area)
      - [2. Misalignment Between Client and Server/Spring Layers](reports/design.md#2-misalignment-between-client-and-serverspring-layers)
      - [3. Security and Governance Components](reports/design.md#3-security-and-governance-components)
      - [4. Other packages](reports/design.md#4-other-packages)
  - [Observer Pattern](reports/design.md#observer-pattern)
    - [1. Involved Classes and Roles](reports/design.md#1-involved-classes-and-roles)
    - [2. Motivation: which problem it solves](reports/design.md#2-motivation-which-problem-it-solves)
    - [3. Alternative to the pattern: pros and cons](reports/design.md#3-alternative-to-the-pattern-pros-and-cons)
    - [4. Direct links to code (GitHub permalink)](reports/design.md#4-direct-links-to-code-github-permalink)
    - [5. UML diagram](reports/design.md#5-uml-diagram)
  - [Facade Pattern (Open Metadata Store Client)](reports/design.md#facade-pattern-open-metadata-store-client)
    - [1. Involved Classes and Each One's Role](reports/design.md#1-involved-classes-and-each-ones-role)
    - [2. Motivation: Which Problem It Solves](reports/design.md#2-motivation-which-problem-it-solves-1)
    - [3. Alternative to the Pattern: Pros and Cons](reports/design.md#3-alternative-to-the-pattern-pros-and-cons-1)
    - [4. Direct Links to Code (GitHub Permalink)](reports/design.md#4-direct-links-to-code-github-permalink-1)
    - [5. UML Diagram](reports/design.md#5-uml-diagram-1)
  - [Adapter Pattern](reports/design.md#adapter-pattern)
    - [1. Involved Classes and Roles](reports/design.md#1-involved-classes-and-roles-1)
    - [2. Motivation: Which Problem It Solves](reports/design.md#2-motivation-which-problem-it-solves-2)
    - [3. Alternative to the Pattern: Pros and Cons](reports/design.md#3-alternative-to-the-pattern-pros-and-cons-2)
    - [4. Direct Links to Code (GitHub Permalink)](reports/design.md#4-direct-links-to-code-github-permalink-2)
    - [5. UML Diagram](reports/design.md#5-uml-diagram-2)
  - [Factory Method](reports/design.md#factory-method)
    - [1. Involved Classes and Roles](reports/design.md#1-involved-classes-and-roles-2)
    - [2. Motivation: Which Problem It Solves](reports/design.md#2-motivation-which-problem-it-solves-3)
    - [3. Alternative to the Pattern: Pros and Cons](reports/design.md#3-alternative-to-the-pattern-pros-and-cons-3)
    - [4. Direct Links to Code (GitHub Permalink)](reports/design.md#4-direct-links-to-code-github-permalink-3)
    - [5. UML diagram](reports/design.md#5-uml-diagram-3)
  - [Summary](reports/design.md#summary)

### [Architecture](reports/architecture.md)

- [Software Architecture](reports/architecture.md#software-architecture)
  - [Context Level (C4 — Level 1)](reports/architecture.md#context-level-c4--level-1)
    - [Diagram](reports/architecture.md#diagram)
    - [Description](reports/architecture.md#description)
    - [External Actors](reports/architecture.md#external-actors)
    - [External Systems](reports/architecture.md#external-systems)
    - [Key Interactions](reports/architecture.md#key-interactions)
  - [Container Level (C4 — Level 2)](reports/architecture.md#container-level-c4--level-2)
    - [Diagram](reports/architecture.md#diagram-1)
    - [Description](reports/architecture.md#description-1)
    - [Containers](reports/architecture.md#containers)
    - [Internal Interactions](reports/architecture.md#internal-interactions)
    - [External Interactions](reports/architecture.md#external-interactions)
    - [Relationship with Clean Architecture](reports/architecture.md#relationship-with-clean-architecture)
  - [Component Level (C4 — Level 3)](reports/architecture.md#component-level-c4--level-3)
    - [1. C4 Component Diagrams for Relevant Containers](reports/architecture.md#1-c4-component-diagrams-for-relevant-containers)
      - [1.1 Metadata Access Server (OMAS) Component Diagram](reports/architecture.md#11-metadata-access-server-omas-component-diagram)
      - [1.2 Integration Daemon Component Diagram](reports/architecture.md#12-integration-daemon-component-diagram)
    - [2. Justify any decisions to exclude specific containers from analysis](reports/architecture.md#2-justify-any-decisions-to-exclude-specific-containers-from-analysis)
    - [3. SOLID Principle Violations at Level 3](reports/architecture.md#3-solid-principle-violations-at-level-3)
      - [3.1 Single Responsability Principle (SRP)](reports/architecture.md#31-single-responsability-principle-srp)
      - [3.2 Open/Closed Principle (OCP)](reports/architecture.md#32-openclosed-principle-ocp)
      - [3.3 Interface Segregation Principle (ISP)](reports/architecture.md#33-interface-segregation-principle-isp)
      - [3.4 Liskov Substitution Principle (LSP)](reports/architecture.md#34-liskov-substitution-principle-lsp)
      - [3.5 Dependency Inversion Principle (DIP)](reports/architecture.md#35-dependency-inversion-principle-dip)
  - [Architectural Characteristics](reports/architecture.md#architectural-characteristics)
    - [1. Architectural Qualities](reports/architecture.md#1-architectural-qualities)
    - [2. Coupling and Cohesion](reports/architecture.md#2-coupling-and-cohesion)

---

## Contributions

| Member                           | Contributions                                                                         |
| -------------------------------- | ------------------------------------------------------------------------------------- |
| **Gabriele Ferrero**             | `overview.md` · `sections/design/A1-code-dependencies.md`                             |
| **Luca Ferrone**                 | `sections/design/A2-knowledge-dependencies.md` · `sections/design/C-summary.md`       |
| **Michele Castrucci**            | `sections/design/B-pattern-1.md` · `sections/design/B-pattern-2.md`                   |
| **Federico Angeloni**            | `sections/design/B-pattern-3.md` · `sections/design/B-pattern-4.md`                   |
| **Viorel Strogoteanu**           | `sections/architecture/A-context.md` · `sections/architecture/B-container.md`         |
| **Matteo Francesco Castigliego** | `sections/architecture/C-component.md` · `sections/architecture/D-characteristics.md` |

---
