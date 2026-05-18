# Weighted Dependency Strength (WDS)

```math
WDS(A,B)=\sum_i w_i \cdot d_i(A,B)
```

Where:
- A is the first package
- B is the second package
- $d_i(A,B)$ is the number of dependencies of type $i$
- $w_i$ is the weight assigned to dependency type $i$

<br><br>

# Dependency Diversity (DD)

```math
DD(A,B)=|\{dependency\ types\ present\}|
```
<br><br>

# Normalized Weighted Dependency Strength (NWDS)

```math
NWDS(A,B)=\frac{WDS(A,B)}{\sqrt{|A|\cdot|B|}}
```

Where:

- $|A|$ is the number of files in package A
- $|B|$ is the number of files in package B

<br><br>

# Final Dependency Score

```math
FinalScore(A,B)=NWDS(A,B)\cdot\log(1+DD(A,B))
```

<br><br><br><br>

# Statistical Methods Used for Dependency Inconsistency Analysis

This part describes the statistical techniques and normalization methods used to analyze the relationship between **code dependencies** and **co-dependencies** between software packages.

The analysis aims to identify hidden architectural relationships, potential inconsistencies, and over-coupled components inside the system.

---

# 1. Package Normalization

The analysis starts by extracting Java package declarations from all `.java` files in the project.

Each source file is mapped to its corresponding package using the Java `package` declaration.

This normalization step allows all dependency metrics to be aggregated at the **package level** instead of the file level.

---

# 2. Code Dependency Analysis

Static code dependencies are loaded from an external dataset:

- `source_package`
- `target_package`
- `FINAL_SCORE`

Each dependency pair is normalized using unordered pairs:

```python 
tuple(sorted([a, b]))
```

This makes the dependency relationship symmetric.

The FINAL_SCORE represents the structural dependency strength between two packages.

---

# 3. Co-Dependency Analysis

Co-dependencies represent how often two files change together during software evolution.

The analysis uses historical co-change information extracted from version control data.

Only valid Java source files are considered:
- .java files only
- test files removed
- mocks removed
- generated code removed
- sample code removed

This filtering reduces noise and improves statistical reliability.

--- 

# 4. Weighted Co-Dependency Metric

The co-dependency strength is computed using a weighted metric:
```math
weighted\_degree=degree×log(1+average\_revs)
```
Where:
- degree = number of co-change occurrences
- average-revs = average number of revisions involved

The logarithmic scaling reduces the dominance of extremely large revision counts while preserving proportional growth.

This is a common statistical stabilization technique for heavy-tailed distributions.

---

# 5. Package Size Normalization

Raw co-dependency values are normalized by package size:
```math
normalized\_codep=\frac{raw\_codep}{size(packageA)×size(packageB)}
```
 
This prevents large packages from artificially producing higher co-dependency values simply because they contain more files.

The normalization converts the metric into a density-like measure.

---

# 6. Logarithmic Transformation

Before statistical comparison, both metrics are transformed using:
```math
log(1+x)
```
The transformation is applied to:
- code dependency scores
- normalized co-dependency scores

Purpose:
- reduce skewness <!-- traduzione: sbilanciato -->
- stabilize variance
- compress extreme outliers
- improve comparability between distributions

This is particularly useful because dependency metrics usually follow highly skewed distributions.

--- 

# 7. Robust Z-Score Normalization

Instead of classical z-score normalization, the analysis uses a robust z-score based on:
- median
- Median Absolute Deviation (MAD)

The formula used is:

```math
z = 0.6745 \times \frac{x - median(x)}{MAD}
```

Where:

```math
MAD = median(|x - median(x)|)
```

This approach is significantly more robust against outliers than standard mean/std-dev normalization.

The constant 0.6745 makes MAD comparable to standard deviation under normal distributions.

--- 

# 8. High / Low Classification

After normalization:
- values with z-score ≥ 1.0 are classified as ```HIGH```
- values with z-score < 1.0 are classified as ```LOW```

This threshold identifies statistically relevant deviations from the median behavior.

---

# 9. Inconsistency Metrics
Three derived metrics are computed.

## 9.1 Inconsistency Score
```math
Z_{codep} −Z_{code}
```

Measures the statistical divergence between:
- structural dependencies
- evolutionary dependencies

Large values indicate architectural inconsistency.

## 9.2 Hidden Dependency Score
```math
Z_{codep} - Z_{code}
```
 
High positive values indicate packages that frequently evolve together despite weak structural coupling.

This may reveal:
- hidden runtime coupling
- implicit architectural dependencies
- missing abstractions


## 9.3 Overcoupling Score
```math
Z_{codep} + Z_{code}
```
​	
Measures the combined intensity of both dependency dimensions.

High values may indicate excessive coupling.


--- 

# 10. Rule-Based Dependency Classification

The final classification is based on the combination of:
- HIGH/LOW code dependency
- HIGH/LOW co-dependency

| Name   | Code dependency level | Co-dependency level  | Description |
|:---------------------:|:----:|:----:|:-------|
| UNRELATED or NORMAL   | LOW  | LOW  | No significant relationship detected. |
| HIDDEN_DEPENDENCY     | LOW  | HIGH | Indicates implicit or undocumented coupling. |
| CAN BE INCONSISTENT   | HIGH | LOW  | Indicates structural coupling that is not reflected in maintenance activity. Possible architectural inconsistency. |
| NORMAL or OVERCOUPLED | HIGH | HIGH | Indicates strong structural and evolutionary alignment. |
