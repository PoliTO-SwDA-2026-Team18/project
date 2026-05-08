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
