# Design — Section B: Pattern 3

> **Owner:** Federico Angeloni  
> **Status:** completed

#### 1. Pattern Name
**Adapter Pattern**.

#### 2. Involved Classes and Roles
* **`MoveCopyFileGovernanceActionProvider` (Adapter):** This concrete provider adapts the governance framework to the specific move/copy/delete file behavior. It translates framework-level configuration into the connector-specific setup.
* **`GovernanceActionServiceProviderBase` (Base Adapter):** This abstract base class supplies the common behavior for governance action service providers and standardizes the information exposed to the framework.
* **`GovernanceServiceProviderBase` (Common Service Base):** This base class defines the shared capabilities for governance services, such as supported request types, request parameters, action targets and produced guards.
* **`OpenConnectorProviderBase` and `ConnectorProviderBase` (Infrastructure):** These classes provide the reusable connector-provider machinery that creates connector instances from a class name and exposes the connector type metadata.
* **`MoveCopyFileGovernanceActionConnector` (Adaptee):** This is the concrete connector that contains the real file operation logic.

#### 3. Motivation: Which Problem It Solves
Egeria must support many different connectors while keeping the framework stable and uniform. The Adapter pattern solves the **integration and variability problem**:
* it allows each service to expose a consistent interface to the framework;
* it hides the details of the specific external tool or connector implementation;
* it lets the framework work with many different services without hard-wiring their logic into the core code.

In this project, `MoveCopyFileGovernanceActionProvider` is a good example because it adapts file-oriented governance actions to the generic provider model used by Egeria.

#### 4. Alternative to the Pattern: Pros and Cons
**Alternative: hard-coded branching inside the framework**
* **Pros:** easier to write in the short term if only one integration exists.
* **Cons:** every new connector would require changing the core framework, which increases coupling, reduces reuse and breaks the Open/Closed Principle.

**Using Adapter**
* **Pros:** each integration remains isolated in its own provider/connector pair; the framework stays stable; new services can be added with minimal impact on existing code.
* **Cons:** more classes and more indirection, so the design is slightly more verbose.

#### 5. Direct Links to Code (GitHub Permalink)
* [MoveCopyFileGovernanceActionProvider.java](https://github.com/PoliTO-SwDA-2026-Team18/project/blob/main/open-metadata-implementation/adapters/open-connectors/governance-action-connectors/src/main/java/org/odpi/openmetadata/adapters/connectors/governanceactions/provisioning/MoveCopyFileGovernanceActionProvider.java)
* [GovernanceActionServiceProviderBase.java](https://github.com/odpi/egeria/blob/main/open-metadata-implementation/frameworks/open-governance-framework/src/main/java/org/odpi/openmetadata/frameworks/opengovernance/GovernanceActionServiceProviderBase.java)
* [GovernanceServiceProviderBase.java](https://github.com/odpi/egeria/blob/main/open-metadata-implementation/frameworks/open-governance-framework/src/main/java/org/odpi/openmetadata/frameworks/opengovernance/GovernanceServiceProviderBase.java)
* [ConnectorProviderBase.java](https://github.com/odpi/egeria/blob/main/open-metadata-implementation/frameworks/open-connector-framework/src/main/java/org/odpi/openmetadata/frameworks/connectors/ConnectorProviderBase.java)

#### 6. UML Diagram
`../../../diagrams/patterns/pattern-adapter.puml`

![UML diagram svg image](../../images/pattern-adapter.svg)
