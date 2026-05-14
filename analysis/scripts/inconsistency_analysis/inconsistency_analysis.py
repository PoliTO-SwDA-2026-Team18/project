import pandas as pd
import numpy as np
from collections import defaultdict
import os
import re

# =========================================================
# PACKAGE NAME NORMALIZATION
# =========================================================

package_map = {}

JAVA_ROOT = (
    "/Users/lucaferrone/Software design/"
    "Project/project/egeria/egeria"
)

package_pattern = re.compile(
    r"^\s*package\s+([a-zA-Z0-9_.]+)\s*;"
)

for root, _, files in os.walk(JAVA_ROOT):

    for file in files:

        if not file.endswith(".java"):
            continue

        full_path = os.path.join(root, file)

        relative_path = os.path.relpath(
            full_path,
            JAVA_ROOT
        ).replace("\\", "/")

        try:

            with open(
                full_path,
                "r",
                encoding="utf-8"
            ) as f:

                for line in f:

                    match = package_pattern.match(line)

                    if match:

                        package_map[relative_path] = (
                            match.group(1)
                        )

                        break

        except:
            pass

# =========================================================
# CONFIG
# =========================================================

CODE_DEP_FILE = (
    "/Users/lucaferrone/Software design/"
    "Project/project/analysis/data/"
    "inconsistency_analysis/"
    "code_dependency_scores.csv"
)

CO_DEP_FILE = (
    "/Users/lucaferrone/Software design/"
    "Project/project/analysis/data/"
    "co-dependencies/"
    "filtered_results.csv"
)

OUTPUT_FILE = (
    "/Users/lucaferrone/Software design/"
    "Project/project/analysis/data/"
    "inconsistency_analysis/"
    "inconsistency_analysis.csv"
)

# =========================================================
# HELPERS
# =========================================================

def normalize_pair(a, b):

    return tuple(sorted([a, b]))


def robust_zscore(series):

    median = series.median()

    mad = np.median(np.abs(series - median))

    if mad == 0:
        mad = 1e-9

    return 0.6745 * (series - median) / mad


def high_low(value, threshold=1.0):

    return "HIGH" if value >= threshold else "LOW"


def classify(row):

    code = row["CODE-DEPENDENCY"]
    codep = row["CO-DEPENDENCY"]

    if code == "LOW" and codep == "HIGH":
        return "HIDDEN_DEPENDENCY"

    elif code == "HIGH" and codep == "HIGH":
        return "NORMAL or OVERCOUPLED"

    elif code == "HIGH" and codep == "LOW":
        return "CAN BE INCONSISTENT"

    return "UNRELATED or NORMAL"


# =========================================================
# LOAD DATA
# =========================================================

code_df = pd.read_csv(CODE_DEP_FILE)

co_df = pd.read_csv(CO_DEP_FILE)

# =========================================================
# CODE DEPENDENCIES
# =========================================================

code_df["pair"] = code_df.apply(
    lambda row: normalize_pair(
        row["source_package"],
        row["target_package"]
    ),
    axis=1
)

code_dep_map = dict(zip(
    code_df["pair"],
    code_df["FINAL_SCORE"]
))

# =========================================================
# CO-DEPENDENCIES
# =========================================================

co_df = co_df[
    co_df["entity"].str.endswith(".java") &
    co_df["coupled"].str.endswith(".java")
]

EXCLUDED_PATTERNS = [
    "/test/",
    "/tests/",
    "/mock/",
    "/generated/",
    "/samples/",
]

for pattern in EXCLUDED_PATTERNS:

    co_df = co_df[
        ~co_df["entity"].str.contains(
            pattern,
            regex=False
        )
    ]

    co_df = co_df[
        ~co_df["coupled"].str.contains(
            pattern,
            regex=False
        )
    ]

co_df["source_package"] = (
    co_df["entity"].map(package_map)
)

co_df["target_package"] = (
    co_df["coupled"].map(package_map)
)

co_df = co_df.dropna(
    subset=[
        "source_package",
        "target_package"
    ]
)

co_df = co_df[
    co_df["source_package"] !=
    co_df["target_package"]
]

# =========================================================
# WEIGHTED CO-DEPENDENCY
# =========================================================

co_df["weighted_degree"] = (
    co_df["degree"] *
    np.log1p(co_df["average-revs"])
)

# =========================================================
# PACKAGE SIZES
# =========================================================

all_files = set(co_df["entity"]).union(
    set(co_df["coupled"])
)

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
# AGGREGATE CO-DEPENDENCIES
# =========================================================

aggregated = defaultdict(float)

for _, row in co_df.iterrows():

    pair = normalize_pair(
        row["source_package"],
        row["target_package"]
    )

    aggregated[pair] += row["weighted_degree"]

# =========================================================
# BUILD DATASET
# =========================================================

results = []

all_pairs = (
    set(aggregated.keys())
    .union(set(code_dep_map.keys()))
)

for pair in all_pairs:

    pkgA, pkgB = pair

    raw_codep = aggregated.get(pair, 0)

    sizeA = package_sizes.get(pkgA, 1)
    sizeB = package_sizes.get(pkgB, 1)

    normalized_codep = (
        raw_codep / (sizeA * sizeB)
    )

    final_score = code_dep_map.get(pair, 0)

    if normalized_codep == 0 and final_score == 0:
        continue

    results.append({

        "packageA": pkgA,
        "packageB": pkgB,

        "FINAL_SCORE": final_score,
        "NORMALIZED_CODEP": normalized_codep
    })

result_df = pd.DataFrame(results)

# =========================================================
# NORMALIZATION
# =========================================================

result_df["Z_CODE"] = robust_zscore(
    np.log1p(result_df["FINAL_SCORE"])
)

result_df["Z_CODEP"] = robust_zscore(
    np.log1p(result_df["NORMALIZED_CODEP"])
)

# =========================================================
# HIGH / LOW LABELS
# =========================================================

result_df["CODE-DEPENDENCY"] = (
    result_df["Z_CODE"]
    .apply(high_low)
)

result_df["CO-DEPENDENCY"] = (
    result_df["Z_CODEP"]
    .apply(high_low)
)

# =========================================================
# SCORES
# =========================================================

result_df["INCONSISTENCY_SCORE"] = np.abs(
    result_df["Z_CODEP"] -
    result_df["Z_CODE"]
)

result_df["HIDDEN_DEPENDENCY_SCORE"] = (
    result_df["Z_CODEP"] -
    result_df["Z_CODE"]
)

result_df["OVERCOUPLING_SCORE"] = (
    result_df["Z_CODEP"] +
    result_df["Z_CODE"]
)

# =========================================================
# CLASSIFICATION
# =========================================================

result_df["CATEGORY"] = result_df.apply(
    classify,
    axis=1
)

# =========================================================
# SORT
# =========================================================

category_order = {
    "HIDDEN_DEPENDENCY": 0,
    "NORMAL or OVERCOUPLED": 1,
    "CAN BE INCONSISTENT": 2,
    "UNRELATED or NORMAL": 3
}


result_df["ORDER"] = (
    result_df["CATEGORY"]
    .map(category_order)
)

result_df = result_df.sort_values(
    by=[
        "ORDER",
        "INCONSISTENCY_SCORE"
    ],
    ascending=[True, False]
)

result_df = result_df.drop(
    columns=["ORDER"]
)

# =========================================================
# KEEP ONLY FINAL COLUMNS
# =========================================================

result_df = result_df[
    [
        "packageA",
        "packageB",
        "CODE-DEPENDENCY",
        "CO-DEPENDENCY",
        "CATEGORY"
    ]
]

# =========================================================
# SAVE
# =========================================================

result_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("Analysis completed.")
print(f"Output written to: {OUTPUT_FILE}")