# Design — Section B: Pattern 1

> **Owner:** Michele Castrucci  
> **Status:** completed


### Observer Pattern

#### 1. Pattern Name
**Observer Pattern** (often referred to as Publish-Subscribe in distributed systems).

#### 2. Involved Classes and Roles
* **`OMRSTopicConnector` (Subject):** This class acts as the Subject. it maintains the registry of listeners and is responsible for receiving events from the underlying event bus (e.g., Kafka) and notifying all registered observers.
* **`OMRSTopicListener` (Observer Interface):** The interface that defines the contract for any component wishing to receive metadata events. It contains callback methods like `processRegistryEvent` and `processTypeDefEvent`.
* **`OpenMetadataOMRSTopicListener` (Concrete Observer):** A specific implementation that reacts to the events. It contains the actual business logic to be executed (e.g., updating a local cache or triggering a governance action) when a notification is received.

#### 3. Motivation: which problem it solves
Egeria operates in a **Federated Metadata Architecture**. Metadata is distributed across multiple independent repositories (the "Cohort"). 
The Observer pattern solves the **decoupling and synchronization problem**: 
* It allows repositories to stay synchronized without having direct dependencies on each other. 
* The Subject does not need to know the identity or the number of Observers. 
* It enables a highly scalable environment where new services can join the metadata exchange simply by registering a new listener.

#### 4. Alternative to the pattern: pros and cons
**Alternative: Synchronous Calls**
* **Pros:** Strong consistency (the caller knows immediately if the update was successful).
* **Cons:** High coupling; if one server in the cohort is down, the entire update process might fail or hang (low resilience).

#### 5. Direct links to code (GitHub permalink)
* [OMRSTopicListener.java (Interface)](https://github.com/odpi/egeria/blob/master/open-metadata-implementation/repository-services/repository-services-apis/src/main/java/org/odpi/openmetadata/repositoryservices/connectors/omrstopic/OMRSTopicListener.java)
* [OMRSTopicConnector.java (Subject)](https://github.com/odpi/egeria/blob/master/open-metadata-implementation/repository-services/repository-services-apis/src/main/java/org/odpi/openmetadata/repositoryservices/connectors/omrstopic/OMRSTopicConnector.java)
* [OpenMetadataOMRSTopicListener.java (Concrete Observer)](https://github.com/odpi/egeria/blob/master/open-metadata-implementation/access-services/omf-metadata-management/omf-metadata-server/src/main/java/org/odpi/openmetadata/frameworkservices/omf/listener/OpenMetadataOMRSTopicListener.java)

#### 6. UML diagram
`../../../diagrams/patterns/pattern-observer.puml`

![UML diagram svg image](../../images/pattern-observer.svg)
