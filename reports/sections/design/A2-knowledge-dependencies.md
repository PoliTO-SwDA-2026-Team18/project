# Design — Section A2: Knowledge Dependencies

> **Owner:** Luca Ferrone  
> **Status:** To be completed

<!-- 
Required content:
- Co-change analysis: files modified together in the same commits
- Knowledge dependencies NOT consistent with code dependencies (A1)
- Explanation of anomalies found
- Diagram: ../../../diagrams/dependencies/knowledge-dependencies.puml
-->

Contenuto personale per ricordami cosa ho fatto:

come ho fatto l'analisi:

ho generato i file di log della storia di egeria e li ho salvati in analysis/data/co-dependencies/co_dependencies_log.txt

con code-maat ho generato un file per l'analisi delle co_dipendenze -> analysis/data/co-dependencies/co_dependencies_result.txt

successivamento ho filtrato i dati con un degree > 40 usando analysis/scripts/co-dependencies/co_dependencies_filter.py e salvando i dati in analysis/data/co-dependencies/filtered_results.txt

poi ho usato uno script di analisi che trasformava le tuple di filtered_result.txt in un grafo e mi mostrava hub, file più accoppiati e clusters più importanti, salvando il risultato in analysis/data/co-dependencies/co_dependencies_analysis_results.txt
