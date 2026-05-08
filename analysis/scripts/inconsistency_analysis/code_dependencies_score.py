import pandas as pd
import numpy as np
from pathlib import Path

# ============================================================
# CONFIGURAZIONE PESI
# ============================================================

WEIGHTS = {
    "import": 1,
    "contain": 4,
    "parameter": 3,
    "call": 4,
    "return": 3,
    "throw": 2,
    "implement": 5,
    "extend": 5,
    "create": 3,
    "use": 2,
    "cast": 1,
    "impllink": 4,
    "annotation": 1,
    "mixin": 4
}

# ============================================================
# FILE
# ============================================================

PACKAGE_FILE = "/Users/lucaferrone/Software design/Project/project/analysis/data/code-dependencies/import-edges-packages.csv"

FILE_FILE = "/Users/lucaferrone/Software design/Project/project/analysis/data/code-dependencies/import-edges-files.csv"

OUTPUT_FILE = "/Users/lucaferrone/Software design/Project/project/analysis/data/inconsistency_analysis/code_dependency_scores.csv"

# ============================================================
# LOAD CSV
# ============================================================

pkg_df = pd.read_csv(PACKAGE_FILE)
file_df = pd.read_csv(FILE_FILE)

# ============================================================
# ESTRAZIONE PACKAGE DAL PATH
# ============================================================

def extract_package(filepath):

    filepath = str(filepath)

    # prende la cartella parent
    return str(Path(filepath).parent)

file_df["source_package"] = file_df["source_file"].apply(extract_package)
file_df["target_package"] = file_df["target_file"].apply(extract_package)

# ============================================================
# DIMENSIONE PACKAGE
# ============================================================

source_sizes = (
    file_df.groupby("source_package")["source_file"]
    .nunique()
)

target_sizes = (
    file_df.groupby("target_package")["target_file"]
    .nunique()
)

package_sizes = pd.concat(
    [source_sizes, target_sizes],
    axis=1
).fillna(0)

package_sizes["size"] = package_sizes.max(axis=1)

package_sizes = package_sizes["size"].to_dict()

# ============================================================
# WDS
# ============================================================

def compute_wds(row):

    score = 0

    for dep_type, weight in WEIGHTS.items():

        value = row.get(dep_type, 0)

        if pd.notna(value):
            score += value * weight

    return score

pkg_df["WDS"] = pkg_df.apply(compute_wds, axis=1)

# ============================================================
# DEPENDENCY DIVERSITY
# ============================================================

def compute_dd(row):

    diversity = 0

    for dep_type in WEIGHTS.keys():

        value = row.get(dep_type, 0)

        if pd.notna(value) and value > 0:
            diversity += 1

    return diversity

pkg_df["DD"] = pkg_df.apply(compute_dd, axis=1)

# ============================================================
# NORMALIZED WDS
# ============================================================

def compute_nwds(row):

    src = row["source_package"]
    tgt = row["target_package"]

    size_a = package_sizes.get(src, 1)
    size_b = package_sizes.get(tgt, 1)

    normalization = np.sqrt(size_a * size_b)

    if normalization == 0:
        return 0

    return row["WDS"] / normalization

pkg_df["NWDS"] = pkg_df.apply(compute_nwds, axis=1)

# ============================================================
# FINAL SCORE
# ============================================================

pkg_df["FINAL_SCORE"] = (
    pkg_df["NWDS"] * np.log1p(pkg_df["DD"])
)

# ============================================================
# SORT
# ============================================================

result_df = pkg_df.sort_values(
    by="FINAL_SCORE",
    ascending=False
)

# ============================================================
# KEEP ONLY FINAL COLUMNS
# ============================================================

output_df = result_df[
    [
        "source_package",
        "target_package",
        "WDS",
        "DD",
        "NWDS",
        "FINAL_SCORE"
    ]
]

# ============================================================
# SAVE
# ============================================================

output_df.to_csv(OUTPUT_FILE, index=False)

# ============================================================
# OUTPUT
# ============================================================

print("\n===================================")
print("DONE")
print("===================================\n")
