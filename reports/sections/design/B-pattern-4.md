# Design — Section B: Pattern 4

> **Owner:** Federico Angeloni  
> **Status:** completed

#### 1. Pattern Name
**Factory Method**.

#### 2. Involved Classes and Roles
* **`OpenConnectorProviderBase` / `ConnectorProviderBase` (Creator / Factory):** base classes that store the connector class name and create `Connector` instances at runtime.
* **`CSVFileStoreProvider` (Concrete Creator / Concrete Factory):** the concrete provider that selects the `CSVFileStoreConnector` implementation.
* **`CSVFileStoreConnector` (Product):** the concrete connector created by the provider.

#### 3. Motivation: Which Problem It Solves
Egeria needs to instantiate many variants of connectors (storage, messaging, governance, etc.) without hard-coding dependencies into the framework. The Factory Method addresses the **problem of parameterized object creation**:
* it separates construction responsibility from product usage;
* it enables adding new connectors by extending a provider subclass without changing framework code;
* it reduces coupling and improves extensibility.

In Egeria this pattern is fundamental: the framework uses provider/connector pairs to load implementations at runtime based on metadata or configuration.

In this project, `CSVFileStoreProvider` is only an example; Factory Method is widely used across Egeria.

#### 4. Alternative to the Pattern: Pros and Cons
**Alternative: reflection / centralized generic factory**
* **Pros:** a single creation point might appear simpler.
* **Cons:** centralizing creation logic makes it harder to extend per-connector behavior; it raises complexity in the central configuration.

**Using Factory Method (concrete providers)**
* **Pros:** each provider encapsulates registration logic and connector metadata; extending is straightforward (add a new provider subclass).
* **Cons:** requires a provider class per connector family (still the most maintainable trade-off).

#### 5. Direct Links to Code (GitHub Permalink)
* [CSVFileStoreProvider.java](https://github.com/odpi/egeria/blob/main/open-metadata-implementation/adapters/open-connectors/data-store-connectors/file-connectors/csv-file-connector/src/main/java/org/odpi/openmetadata/adapters/connectors/datastore/csvfile/CSVFileStoreProvider.java)
* [ValidMetadataValueSetListProvider.java](https://github.com/odpi/egeria/blob/main/open-metadata-implementation/adapters/open-connectors/nanny-connectors/src/main/java/org/odpi/openmetadata/adapters/connectors/jacquard/tabulardatasets/validmetadatavalues/ValidMetadataValueSetListProvider.java)
* [PostgresTabularDataSetProvider.java](https://github.com/odpi/egeria/blob/main/open-metadata-implementation/adapters/open-connectors/data-manager-connectors/postgres-server-connectors/src/main/java/org/odpi/openmetadata/adapters/connectors/postgres/tabulardatasource/PostgresTabularDataSetProvider.java)
* [MoveCopyFileGovernanceActionProvider.java](https://github.com/PoliTO-SwDA-2026-Team18/project/blob/main/open-metadata-implementation/adapters/open-connectors/governance-action-connectors/src/main/java/org/odpi/openmetadata/adapters/connectors/governanceactions/provisioning/MoveCopyFileGovernanceActionProvider.java)

* [OpenConnectorProviderBase.java](https://github.com/odpi/egeria/blob/main/open-metadata-frameworks/open-connector-framework/src/main/java/org/odpi/openmetadata/frameworks/connectors/OpenConnectorProviderBase.java)
* [ConnectorProviderBase.java](https://github.com/odpi/egeria/blob/main/open-metadata-frameworks/open-connector-framework/src/main/java/org/odpi/openmetadata/frameworks/connectors/ConnectorProviderBase.java)

#### 6. UML diagram
`../../../diagrams/patterns/pattern-factory.puml`

![UML diagram svg image](../../images/pattern-factory.svg)

