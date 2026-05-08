import pandas as pd
import numpy as np
from collections import defaultdict
from pathlib import Path

# =========================================================
# PACKAGE NAME NORMALIZATION
# =========================================================


import os
import re

package_map = {}

JAVA_ROOT = "/Users/lucaferrone/Software design/Project/project/egeria/egeria"

package_pattern = re.compile(r"^\s*package\s+([a-zA-Z0-9_.]+)\s*;")

for root, _, files in os.walk(JAVA_ROOT):

    for file in files:

        if not file.endswith(".java"):
            continue

        full_path = os.path.join(root, file)

        relative_path = os.path.relpath(full_path, JAVA_ROOT)
        relative_path = relative_path.replace("\\", "/")

        try:
            with open(full_path, "r", encoding="utf-8") as f:

                for line in f:

                    match = package_pattern.match(line)

                    if match:

                        package_name = match.group(1)

                        package_map[relative_path] = package_name
                        break

        except:
            pass





# =========================================================
# CONFIG
# =========================================================

CODE_DEP_FILE = "/Users/lucaferrone/Software design/Project/project/analysis/data/inconsistency_analysis/code_dependency_scores.csv"
CO_DEP_FILE = "/Users/lucaferrone/Software design/Project/project/analysis/data/co-dependencies/filtered_results.csv"

OUTPUT_FILE = "/Users/lucaferrone/Software design/Project/project/analysis/data/inconsistency_analysis/inconsistency_analysis.csv"


# =========================================================
# HELPERS
# =========================================================


def normalize_package_pair(pkg1, pkg2):
    """
    Ensure package pairs are symmetric.
    """
    return tuple(sorted([pkg1, pkg2]))


# =========================================================
# LOAD FILES
# =========================================================

code_df = pd.read_csv(CODE_DEP_FILE)

co_df = pd.read_csv(CO_DEP_FILE)

# =========================================================
# PREPARE CODE DEPENDENCIES
# =========================================================

code_df["pair"] = code_df.apply(
    lambda row: normalize_package_pair(
        row["source_package"],
        row["target_package"]
    ),
    axis=1
)

code_dep_map = {}

for _, row in code_df.iterrows():
    code_dep_map[row["pair"]] = {
        "FINAL_SCORE": row["FINAL_SCORE"],
        "WDS": row.get("WDS", 0),
        "DD": row.get("DD", 0),
        "NWDS": row.get("NWDS", 0)
    }

# =========================================================
# PREPARE CO-DEPENDENCIES
# =========================================================

# Keep only Java files
co_df = co_df[
    co_df["entity"].str.endswith(".java") &
    co_df["coupled"].str.endswith(".java")
]

# Remove noisy files/directories
EXCLUDED_PATTERNS = [
    "/test/",
    "/tests/",
    "/mock/",
    "/generated/",
    "/samples/",
]

for pattern in EXCLUDED_PATTERNS:

    co_df = co_df[
        ~co_df["entity"].str.contains(pattern, regex=False)
    ]

    co_df = co_df[
        ~co_df["coupled"].str.contains(pattern, regex=False)
    ]

# Map files to real Java packages
co_df["source_package"] = co_df["entity"].map(package_map)
co_df["target_package"] = co_df["coupled"].map(package_map)
print("INITIAL:", len(co_df))
# Remove unresolved packages
co_df = co_df.dropna(
    subset=["source_package", "target_package"]
)
print("INITIAL:", len(co_df))
# Remove self-package dependencies
co_df = co_df[
    co_df["source_package"] != co_df["target_package"]
]
print("INITIAL:", len(co_df))
# Weighted co-dependency
co_df["weighted_degree"] = (
    co_df["degree"] * np.log1p(co_df["average-revs"])
)

# =========================================================
# COUNT FILES PER PACKAGE
# =========================================================

all_files = set(co_df["entity"]).union(set(co_df["coupled"]))

package_files = defaultdict(set)

for file in all_files:

    pkg = package_map.get(file)

    if pkg is not None:
        package_files[pkg].add(file)

package_sizes = {
    pkg: len(files)
    for pkg, files in package_files.items()
}

# =========================================================
# AGGREGATE CO-DEPENDENCIES AT PACKAGE LEVEL
# =========================================================

aggregated = defaultdict(float)

for _, row in co_df.iterrows():

    pkgA = row["source_package"]
    pkgB = row["target_package"]

    pair = normalize_package_pair(pkgA, pkgB)

    aggregated[pair] += row["weighted_degree"]

# =========================================================
# BUILD FINAL DATASET
# =========================================================

results = []

all_pairs = set(aggregated.keys()).union(set(code_dep_map.keys()))

for pair in all_pairs:

    pkgA, pkgB = pair

    # Co dependency
    raw_codep = aggregated.get(pair, 0)

    sizeA = package_sizes.get(pkgA, 1)
    sizeB = package_sizes.get(pkgB, 1)

    normalized_codep = raw_codep / (sizeA * sizeB)

    # Code dependency
    code_info = code_dep_map.get(pair, {})

    final_score = code_info.get("FINAL_SCORE", 0)

    # =====================================================
    # Hidden Dependency
    # High co-dep, low code-dep
    # =====================================================

    hidden_dependency = normalized_codep / (final_score + 1)

    # =====================================================
    # Overcoupling
    # High co-dep AND high code-dep
    # =====================================================

    overcoupling = normalized_codep * final_score

    results.append({
        "packageA": pkgA,
        "packageB": pkgB,

        "FINAL_SCORE": final_score,

        "RAW_CODEP": raw_codep,
        "NORMALIZED_CODEP": normalized_codep,

        "HIDDEN_DEPENDENCY": hidden_dependency,
        "OVERCOUPLING": overcoupling
    })

# =========================================================
# FINAL DATAFRAME
# =========================================================

result_df = pd.DataFrame(results)

# =========================================================
# CLASSIFICATION
# =========================================================

code_threshold = result_df["FINAL_SCORE"].quantile(0.75)

codep_threshold = result_df["NORMALIZED_CODEP"].quantile(0.75)


def classify(row):

    high_code = row["FINAL_SCORE"] >= code_threshold
    high_codep = row["NORMALIZED_CODEP"] >= codep_threshold

    if high_code and high_codep:
        return "OVERCOUPLED"

    elif (not high_code) and high_codep:
        return "HIDDEN_DEPENDENCY"

    elif high_code and (not high_codep):
        return "STRUCTURAL_DEPENDENCY"

    else:
        return "NORMAL"


result_df["CATEGORY"] = result_df.apply(classify, axis=1)

# =========================================================
# SORT
# =========================================================

result_df = result_df.sort_values(
    by="HIDDEN_DEPENDENCY",
    ascending=False
)

# =========================================================
# SAVE
# =========================================================

result_df.to_csv(OUTPUT_FILE, index=False)

print("Analysis completed.")
print(f"Output written to: {OUTPUT_FILE}")
