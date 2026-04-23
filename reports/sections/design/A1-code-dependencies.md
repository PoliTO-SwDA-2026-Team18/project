# A1 — Code Dependencies

## Methodology

**[Depends](https://github.com/multilang-depends/depends)** (v0.9.7) was used for the initial static analysis of the source code, producing a JSON dependency matrix; a custom Python script (`analyze_dependencies.py`) then processed this output to compute the final statistics.

---

## File Dependency Rankings

### Highest Outgoing Imports

| Imports | File |
|---------|------|
| 56 | `nanny-connectors/.../JacquardIntegrationConnector.java` |
| 51 | `repository-services-apis/.../OMRSMetadataCollection.java` |
| 51 | `open-metadata-framework/.../OpenMetadataPropertyConverterBase.java` |

`JacquardIntegrationConnector` ranks highest because it assembles the **Open Metadata Digital Product Catalog**, managing digital products across a single class: product catalogs, solution blueprints, reference data sets, governance actions, communities, glossaries, and data dictionaries. Each concern introduces its own set of property beans, elements, and context types.

### Lowest Outgoing Imports

| Imports | File |
|---------|------|
| 1 | `community-matters-spring/.../CommunityMattersResource.java` |
| 1 | `open-metadata-framework/.../DataMappingProperties.java` |
| 1 | `open-metadata-framework/.../ConceptBeadAttributeProperties.java` |

`CommunityMattersResource` ranks lowest because it is the server-side REST controller for **Community Matters OMVS**: it only exposes HTTP endpoints and immediately delegates each call to `CommunityMattersRESTServices`. Since all logic is delegated to `CommunityMattersRESTServices`, this class never touches Egeria types directly — `CommunityMattersRESTServices` is the only explicit Egeria import it declares.

### Most Imported Files

| Imported by | File |
|-------------|------|
| 863 | `open-metadata-framework/.../OpenMetadataType.java` |
| 631 | `audit-log-framework/.../AuditLog.java` |
| 574 | `open-metadata-framework/.../InvalidParameterException.java` |

---

## Observed Structural (Code-Level) Dependencies

### Implementation Dependency

- **Source:** `egeria-system-connectors/.../OMAGServerPlatformCatalogConnector.java`
- **Depends on:** `open-metadata-framework/.../SoftwareServerProperties.java`

The connector pattern-matches against the concrete type and calls methods on it directly:

```java
if (softwareServer.getProperties()
        instanceof SoftwareServerProperties softwareServerProperties)
    softwareServerProperties.getDeployedImplementationType();
```

### Construction Dependency

- **Source:** `egeria-system-connectors/.../OMAGServerPlatformCatalogConnector.java`
- **Depends on:** `open-metadata-framework/.../SoftwareServerProperties.java`

The connector directly instantiates `SoftwareServerProperties` via `new` and populates it before use:

```java
SoftwareServerProperties softwareServerProperties = new SoftwareServerProperties();
softwareServerProperties.setQualifiedName(…);
```

### Compile-Time Dependency

- **Source:** `common-services/multi-tenant/.../OMAGServerInstanceAuditCode.java`
- **Depends on:** `audit-log-framework/.../AuditLogMessageSet.java`

The enum declares `AuditLogMessageSet` only in its type signature — no calls or instantiations, purely a compiler-level contract:

```java
public enum OMAGServerInstanceAuditCode implements AuditLogMessageSet { … }
```

---

## Module Dependency Graph

> Edge weights = total `Import` count between submodules of `open-metadata-implementation`. Only edges with ≥ 10 imports are shown.

```mermaid
flowchart LR
    adapters["adapters"]
    frameworks["frameworks"]
    repo_svc["repository-services"]
    access_svc["access-services"]
    view_svc["view-services"]
    common_svc["common-services"]
    admin_svc["admin-services"]
    engine_svc["engine-services"]
    gov_svc["governance-server-services"]
    view_gen_svc["view-server-generic-services"]
    plt_chassis["platform-chassis"]
    plt_svc["platform-services"]
    srv_ops["server-operations"]
    usr_sec["user-security"]

    adapters -->|"2558"| frameworks
    adapters -->|"224"| repo_svc
    adapters -->|"18"| common_svc
    adapters -->|"17"| admin_svc
    adapters -->|"11"| gov_svc
    adapters -->|"10"| srv_ops
    repo_svc -->|"434"| frameworks
    repo_svc -->|"21"| common_svc
    repo_svc -->|"12"| admin_svc
    access_svc -->|"354"| frameworks
    access_svc -->|"118"| repo_svc
    access_svc -->|"94"| common_svc
    access_svc -->|"32"| admin_svc
    view_svc -->|"439"| frameworks
    view_svc -->|"28"| access_svc
    view_svc -->|"152"| common_svc
    view_svc -->|"240"| admin_svc
    view_svc -->|"24"| usr_sec
    common_svc -->|"386"| frameworks
    common_svc -->|"146"| repo_svc
    common_svc -->|"11"| admin_svc
    admin_svc -->|"126"| frameworks
    admin_svc -->|"13"| repo_svc
    admin_svc -->|"77"| common_svc
    engine_svc -->|"212"| frameworks
    engine_svc -->|"59"| repo_svc
    engine_svc -->|"30"| access_svc
    engine_svc -->|"50"| common_svc
    engine_svc -->|"41"| admin_svc
    engine_svc -->|"39"| gov_svc
    gov_svc -->|"152"| frameworks
    gov_svc -->|"15"| access_svc
    gov_svc -->|"31"| common_svc
    gov_svc -->|"22"| admin_svc
    view_gen_svc -->|"357"| frameworks
    view_gen_svc -->|"20"| access_svc
    view_gen_svc -->|"106"| common_svc
    view_gen_svc -->|"164"| admin_svc
    view_gen_svc -->|"15"| usr_sec
    plt_svc -->|"18"| frameworks
    plt_svc -->|"22"| common_svc
    plt_svc -->|"12"| admin_svc
    plt_svc -->|"20"| srv_ops
    srv_ops -->|"25"| frameworks
    srv_ops -->|"15"| common_svc
    srv_ops -->|"18"| admin_svc
```
