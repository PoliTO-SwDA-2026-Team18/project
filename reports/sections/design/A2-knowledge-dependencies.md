# Design — Section A2: Knowledge Dependencies

> **Owner:** Luca Ferrone  
> **Status:** Completed

<!-- 
Required content:
- Co-change analysis: files modified together in the same commits
- Knowledge dependencies NOT consistent with code dependencies (A1)
- Explanation of anomalies found
-->

<!-- 
Contenuto personale per ricordami cosa ho fatto:

come ho fatto l'analisi:

ho generato i file di log della storia di egeria e li ho salvati in analysis/data/co-dependencies/co_dependencies_log.txt

con code-maat ho generato un file per l'analisi delle co_dipendenze -> analysis/data/co-dependencies/co_dependencies_result.txt

successivamento ho filtrato i dati con un degree > 40 usando analysis/scripts/co-dependencies/co_dependencies_filter.py e salvando i dati in analysis/data/co-dependencies/filtered_results.txt

poi ho usato uno script di analisi che trasformava le tuple di filtered_result.txt in un grafo e mi mostrava hub, file più accoppiati e clusters più importanti, salvando il risultato in analysis/data/co-dependencies/co_dependencies_analysis_results.txt
-->

<!-- Official report -->


The co-dependency analysis was performed using CodeMaat, following this workflow:

![co-dependency anaysis workflow](../../images/co-dependencies-workflow.jpg)

Using file `analysis.txt`, I derived the following conclusions.


### Hub analysis

- **`Content packs (.omarchive)`**  
  These files contain definitions of data models. If you change the data model, you need to update almost everything else.

- **`open-metadata-conformance-suite`**  
  The testing system is deeply integrated. It's a sign of software maturity, but it also indicates that every change to the core APIs requires a massive update of compliance testing.

- **`Infrastructure & DevOps`**  
  Files like Dockerfile, build.gradle, and GitHub workflows show a co-dependency related to the build and deployment process.

### Coupling analysis

- **`Content packs (.omarchive)`**  
  Content pack files have 100% of coupling, this means that there is a very high cohesion between the content packages. 
  This suggests that, although they are physically separate, they logically form a single information block. 
  Splitting these dependencies in the future may be difficult.

- **`Enterprise Executors`**   
  Search executors (e.g., FindEntitiesByClassificationExecutor vs FindEntitiesByPropertyValueExecutor) show very high coupling (100%–92%).
  This suggests code duplication or highly similar logic (if a bug appears in one, it is likely present in the other as well).
  It can be usefull estract common logic in a unique class.


- **`.gradle and .config files`**  
  Co-changes among configuration files are expected, but frequent or widespread coupling may indicate tight module dependencies (.gradle) or duplicated configuration logic (.config), reducing maintainability.


### Inconsistencies with code dependencies

After a comprehensive data analysis conducted using Pandas (a detailed explanation of the methodology can be found in file [analysis_explanation.md](../../../analysis/scripts/inconsistency_analysis/analysis_explanation.md)), package pairs were classified according to their levels of code-dependency and co-dependency.

The most critical and interesting inconsistencies are those classified as HIDDEN_DEPENDENCY. <br> 
They occur when the direct code dependency is low, while the logical/historical coupling is high. <br>
This indicates a potential <u>*maintenance risk*</u> : modifying one package may unintentionally break another without the compiler providing clear warnings.

Below are the most relevant cases grouped by thematic area:


#### <u>1. Connectors and Repository Architecture (Most Critical Area)</u>
These packages are responsible for data integration and persistence-layer management.
The presence of high logical coupling despite low structural dependency suggests the existence of implicit assumptions and hidden coordination mechanisms within the codebase.

| Package A | Package B |
|:----------|:----------|
| `adapters.repositoryservices.inmemory.repositoryconnector`                         | `adapters.repositoryservices.rest.repositoryconnector`        | 
| `adapters.repositoryservices.rest.repositoryconnector`                             | `repositoryservices.rest.server`                              |
| `repositoryservices.connectors.stores.metadatacollectionstore.repositoryconnector` | `repositoryservices.localrepository.repositorycontentmanager` |

From a software architecture perspective, decoupling in-memory and REST connectors from backend server implementations is considered a good design practice. However, the high co-dependency observed between these components indicates that modifications in one package are consistently reflected in the others.
This behavior suggests the existence of undocumented behavioral contracts, shared assumptions, or implicit synchronization between modules, which increases maintenance complexity and the risk of unintended side effects during evolution activities.

<br>

#### <u>2. Misalignment Between Client and Server/Spring Layers</u>

In a clean distributed architecture, client components and Spring-based server controllers should ideally interact only through well-defined APIs, DTOs (Data Transfer Objects), or shared interfaces.
The analysis, however, reveals the presence of strong hidden logical dependencies between these layers.

| Package A | Package B |
|:----------|:----------|
| `repositoryservices.clients` | `repositoryservices.rest.server.spring` | 
| `adminservices.client`       | `adminservices.spring`                  |
| `platformservices.client`    | `platformservices.server`               |

The fact that client-side modules and their corresponding server/Spring services evolve together, despite exhibiting weak direct code dependencies, suggests that communication protocols and API contracts are not sufficiently isolated.
This pattern often indicates architectural erosion, where changes propagate across distributed layers due to implicit behavioral coupling rather than explicit interface definitions.

<br>

#### <u>3. Security and Governance Components</u>

The analysis also highlights hidden logical coupling within security-related and governance-oriented modules.

| Package A | Package B |
|:----------|:----------|
| `metadatasecurity.connectors`                | `metadatasecurity.server`                            | 
| `adapters.connectors.governanceactions.ffdc` | `adapters.connectors.governanceactions.provisioning` |

The relationship between metadatasecurity.connectors and metadatasecurity.server suggests that security connectors are tightly coupled to the server-side implementation logic, despite the absence of strong explicit structural dependencies.
The co-evolution observed between governanceactions.ffdc (First Failure Data Capture) and governanceactions.provisioning indicates that failure-management mechanisms and governance provisioning workflows are strongly interconnected at the logical level.
These findings may reveal critical maintenance hotspots, where architectural modularity is only partially achieved in practice.

<br>

#### <u>4. Other packages</u>

The vast majority of the remaining package pairs in the dataset exhibit LOW - LOW values and are therefore correctly classified as UNRELATED or NORMAL.
These cases do not represent architectural anomalies.