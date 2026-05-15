# Design — Section B: Pattern 3 – Adapter

> **Owner:** Federico Angeloni  
> **Status:** Completed

### 1. Pattern name

**Adapter Pattern**

### 2. Involved classes and their roles

The Adapter pattern is widely used in the system to allow various connectors ("adapters") to integrate external tools into the Egeria stack by mapping their APIs and data structures onto the standard interface required by the framework.

- **Example:**
    - `org.odpi.openmetadata.adapters.connectors.*`: all the specific connector implementations act as Adapters.
    - **Target Interface:** The interface required by the framework, such as classes under `org.odpi.openmetadata.frameworks.connectors`.
    - **Adapter class:** For example, `MoveCopyFileGovernanceActionProvider` (path: `open-metadata-implementation/adapters/open-connectors/governance-action-connectors/src/main/java/org/odpi/openmetadata/adapters/connectors/governanceactions/provisioning/MoveCopyFileGovernanceActionProvider.java`), adapts the framework calls to external file management tools.
    - **Client/Framework:** The module using these connectors via the generic interface, e.g., the governance framework itself.

### 3. Motivation: which problem it solves

The Adapter pattern solves the problem of integrating heterogeneous tools (repositories, governance tools, storage providers, etc.) using a consistent and standardized interface. With Adapter, new tools can be added without needing modifications in the core framework—one needs only to implement a specific Adapter for the new tool.

- **Typical scenario:** Plugging in new types of connector/adapters to support additional external systems, with minimal changes to the core codebase.

### 4. Alternative to the pattern: pros and cons

**Alternative:** Direct API mapping inside the core framework, i.e., adding conditional branches or modifying the core code whenever a new tool is added.

- **Pro:** Simple when supporting only one or two tools.
- **Cons:** Not scalable, because each new integration means touching core framework code, increasing risk of bugs, redundancy, and lack of modularity. It breaks the Open/Closed Principle and requires risky deployments with each evolution.

**Using Adapter:**
- **Pros:** Modular and extensible; the framework remains stable while each adapter encapsulates the integration logic for a new tool.
- **Cons:** More boilerplate, as a new Adapter has to be written for every external tool; some code duplication if tools are very similar.

### 5. Direct links to code (GitHub permalinks)

- [MoveCopyFileGovernanceActionProvider.java](https://github.com/PoliTO-SwDA-2026-Team18/project/blob/main/open-metadata-implementation/adapters/open-connectors/governance-action-connectors/src/main/java/org/odpi/openmetadata/adapters/connectors/governanceactions/provisioning/MoveCopyFileGovernanceActionProvider.java)
- [Connectors package](https://github.com/PoliTO-SwDA-2026-Team18/project/tree/main/open-metadata-implementation/adapters/open-connectors)
- [Framework connectors interfaces](https://github.com/PoliTO-SwDA-2026-Team18/project/tree/main/open-metadata-implementation/frameworks)

### 6. UML diagram
`../../../diagrams/patterns/pattern-adapter.puml`

![UML diagram svg image](../../images/pattern-adapter.svg)
