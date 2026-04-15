# Project — Egeria Analysis

Analysis of the open-source system **[Egeria](https://github.com/odpi/egeria)** — an open metadata and governance platform. The project produces three Markdown reports (Overview, Design, Architecture) along with supporting diagrams and individual journals.

### Analyzed System

| | |
|---|---|
| **Repository** | [odpi/egeria](https://github.com/odpi/egeria) |
| **Analyzed Release** | [V6.0](https://github.com/odpi/egeria/releases/tag/V6.0) |
| **Reference Commit** | [`d893f299`](https://github.com/odpi/egeria/tree/d893f299defd372c7c571e6d8f934a127a2fbd75) |

---

## Repository Structure

### Reports

Final reports are in `reports/`. Individual sections that each member works on independently are in `reports/sections/`, and will be assembled into the final reports at the end.

| File | Description | Owner |
|---|---|---|
| [reports/overview.md](reports/overview.md) | System Overview | Gabriele Ferrero |
| [reports/design.md](reports/design.md) | Software Design | — |
| [reports/architecture.md](reports/architecture.md) | Software Architecture | — |

#### Design Sections

| File | Section | Owner |
|---|---|---|
| [A1-code-dependencies.md](reports/sections/design/A1-code-dependencies.md) | A1: Code Dependencies | Gabriele Ferrero |
| [A2-knowledge-dependencies.md](reports/sections/design/A2-knowledge-dependencies.md) | A2: Knowledge Dependencies | Luca Ferrone |
| [B-pattern-1.md](reports/sections/design/B-pattern-1.md) | B: Pattern 1 | Michele Castrucci |
| [B-pattern-2.md](reports/sections/design/B-pattern-2.md) | B: Pattern 2 | Michele Castrucci |
| [B-pattern-3.md](reports/sections/design/B-pattern-3.md) | B: Pattern 3 | Federico Angeloni |
| [B-pattern-4.md](reports/sections/design/B-pattern-4.md) | B: Pattern 4 | Federico Angeloni |
| [C-summary.md](reports/sections/design/C-summary.md) | C: Summary | Luca Ferrone |

#### Architecture Sections

| File | Section | Owner |
|---|---|---|
| [A-context.md](reports/sections/architecture/A-context.md) | A: Context Level (C4 L1) | Viorel Strogoteanu |
| [B-container.md](reports/sections/architecture/B-container.md) | B: Container Level (C4 L2) | Viorel Strogoteanu |
| [C-component.md](reports/sections/architecture/C-component.md) | C: Component Level (C4 L3) | Matteo Francesco Castigliego |
| [D-characteristics.md](reports/sections/architecture/D-characteristics.md) | D: Architectural Characteristics | Matteo Francesco Castigliego |

### Diagrams

| File | Description |
|---|---|
| [diagrams/c4/context.puml](diagrams/c4/context.puml) | C4 Diagram — Context (Level 1) |
| [diagrams/c4/container.puml](diagrams/c4/container.puml) | C4 Diagram — Container (Level 2) |
| `diagrams/c4/component-<name>.puml` | C4 Diagrams — Component (Level 3) — *to be created* |
| [diagrams/dependencies/code-dependencies.puml](diagrams/dependencies/code-dependencies.puml) | Code dependencies graph (imports) |
| [diagrams/dependencies/knowledge-dependencies.puml](diagrams/dependencies/knowledge-dependencies.puml) | Knowledge dependencies graph (co-change) |
| `diagrams/patterns/pattern-<name>.puml` | Design pattern UML diagrams — *to be created (4 patterns)* |

### Individual Journals

One file per team member, logging activities, hours spent, and report contributions.

| File | Member |
|---|---|
| [journals/gabriele-ferrero.md](journals/gabriele-ferrero.md) | Gabriele Ferrero |
| [journals/luca-ferrone.md](journals/luca-ferrone.md) | Luca Ferrone |
| [journals/michele-castrucci.md](journals/michele-castrucci.md) | Michele Castrucci |
| [journals/federico-angeloni.md](journals/federico-angeloni.md) | Federico Angeloni |
| [journals/viorel-strogoteanu.md](journals/viorel-strogoteanu.md) | Viorel Strogoteanu |
| [journals/matteo-francesco-castigliego.md](journals/matteo-francesco-castigliego.md) | Matteo Francesco Castigliego |
