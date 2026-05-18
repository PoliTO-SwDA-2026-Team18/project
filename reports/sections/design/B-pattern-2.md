# Design — Section B: Pattern 2

> **Owner:** Michele Castrucci  
> **Status:** Completed

### Facade Pattern (Open Metadata Store Client)

#### 1. Pattern Name
**Facade Pattern**

#### 2. Involved Classes and Each One's Role
* **`EgeriaOpenMetadataStoreClient` (Facade):** This is the concrete Facade class. It provides a simplified, unified interface to the Open Metadata Framework (OMF). It is the primary entry point for developers who need to perform metadata operations without dealing with the internal technicalities of the framework.
* **`OpenMetadataClientBase` (Base Facade / Orchestrator):** An abstract base class that manages the shared infrastructure for various clients. It coordinates the interactions between different subsystems such as REST communication, security, and logging.
* **`OMFRESTClient` (Subsystem):** A complex subsystem responsible for low-level HTTP communication. It handles JSON serialization/deserialization and the execution of REST calls to the OMAG Server Platform.
* **`AuditLog` (Subsystem):** A subsystem that provides diagnostic logging capabilities. It ensures that all client activities are correctly recorded for audit purposes.
* **`SecretsStoreConnector` (Subsystem):** A specialized subsystem that manages security tokens and authentication. It shields the client from the complexities of bearer token management and secret storage.

#### 3. Motivation: Which Problem It Solves
The Open Metadata Framework (OMF) within Egeria is an extremely large and modular system. Interacting directly with the underlying subsystems would require a developer to manually manage REST connections, handle complex security handshakes via secret stores, and configure audit logging for every single operation. 

The Facade pattern solves the **complexity and interface pollution** problems by:
* Providing a high-level Java API that hides the network plumbing (REST).
* Encapsulating the initialization and coordination of multiple subsystems (Security, Logging, REST).
* Reducing the learning curve for third-party developers who only need to "search" or "maintain" metadata without understanding the entire OMRS/OMF internal stack.

#### 4. Alternative to the Pattern: Pros and Cons
**Alternative: Direct Subsystem Access**
* **Pros:** * Provides maximum flexibility, allowing access to low-level features not exposed by the Facade.
    * Avoids the overhead of an additional abstraction layer.
* **Cons:** * **High Coupling:** Any change in the internal REST protocol or security management would break all client applications.
    * **Complexity:** Developers must write significant boilerplate code to manage connections and authentication.
    * **Error Prone:** Improper handling of low-level components can lead to inconsistent metadata states or security vulnerabilities.

#### 5. Direct Links to Code (GitHub Permalink)
* [`EgeriaOpenMetadataStoreClient.java` (Facade)](https://github.com/odpi/egeria/blob/88c26bef1db455222c61a99d62ef0c47f1fb67c3/open-metadata-implementation/access-services/omf-metadata-management/omf-metadata-client/src/main/java/org/odpi/openmetadata/frameworkservices/omf/client/EgeriaOpenMetadataStoreClient.java)
* [`OpenMetadataClientBase.java` (Base Infrastructure)](https://github.com/odpi/egeria/blob/88c26bef1db455222c61a99d62ef0c47f1fb67c3/open-metadata-implementation/access-services/omf-metadata-management/omf-metadata-client/src/main/java/org/odpi/openmetadata/frameworkservices/omf/client/OpenMetadataClientBase.java)
* [`OMFRESTClient.java` (REST Subsystem)](https://github.com/odpi/egeria/blob/88c26bef1db455222c61a99d62ef0c47f1fb67c3/open-metadata-implementation/access-services/omf-metadata-management/omf-metadata-client/src/main/java/org/odpi/openmetadata/frameworkservices/omf/client/rest/OMFRESTClient.java)

#### 6. UML Diagram

`../../../diagrams/patterns/pattern-facade.puml`

![UML diagram svg image](../../images/pattern-facade.svg)