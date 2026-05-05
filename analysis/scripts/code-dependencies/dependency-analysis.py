import json
from collections import defaultdict
import re

# <--------------------- Load JSON --------------------->
INPUT_FILE = "imports-matrix.json"

with open(INPUT_FILE, encoding="utf-8") as f:
    data = json.load(f)

# 'variables' is a plain list: position = numeric ID used in cells
# e.g. variables[0] = "path/to/FileA.java"  →  ID 0 refers to FileA
variables = data["variables"]
cells     = data["cells"]       # list of {src: int, dest: int, values: dict}

# <--------------------- Helpers --------------------->
SEP = "─" * 80

def norm(path: str) -> str:
    """Normalize path separators to forward slashes."""
    return path.replace("\\", "/")

def section(title: str) -> None:
    print(f"\n{SEP}")
    print(f"{title}")
    print(SEP)

# <--------------------- Build per-file import counters --------------------->
# import_out[file] = total Import edges leaving that file   (outgoing)
# import_in[file]  = total Import edges arriving at that file (incoming)
import_out: dict = defaultdict(int)
import_in:  dict = defaultdict(int)

for cell in cells:
    src  = variables[cell["src"]]
    dest = variables[cell["dest"]]
    imp  = int(cell["values"].get("Import", 0))
    import_out[src]  += imp
    import_in[dest]  += imp

# <--------------------- Section 1 - Ranking files --------------------->
NUMBER_OF_ELEMENTS_RANKING = 5
files_with_import = {k: v for k, v in import_out.items() if v >= 1}
top_out    = sorted(files_with_import.items(), key=lambda x: -x[1])[:NUMBER_OF_ELEMENTS_RANKING]
bottom_out = sorted(files_with_import.items(), key=lambda x:  x[1])[:NUMBER_OF_ELEMENTS_RANKING]
top_in     = sorted(import_in.items(),         key=lambda x: -x[1])[:NUMBER_OF_ELEMENTS_RANKING]

# <--------------------- Top files with the most outgoing imports --------------------->
section(f"1a. TOP {NUMBER_OF_ELEMENTS_RANKING} FILES WITH THE MOST OUTGOING IMPORTS")
for rank, (name, val) in enumerate(top_out, 1):
    print(f"{rank}. imports={val:>3}  {norm(name)}")

# <--------------------- Bottom files with the fewest outgoing imports (>=1) --------------------->
section(f"1b. BOTTOM {NUMBER_OF_ELEMENTS_RANKING} FILES WITH THE FEWEST OUTGOING IMPORTS  (minimum 1)")
for rank, (name, val) in enumerate(bottom_out, 1):
    print(f"{rank}. imports={val:>3}  {norm(name)}")

# <--------------------- Top most imported files (incoming) --------------------->
section(f"1c. TOP {NUMBER_OF_ELEMENTS_RANKING} MOST IMPORTED FILES  (incoming import count)")
for rank, (name, val) in enumerate(top_in, 1):
    print(f"{rank}. imported_by={val:>3}  {norm(name)}")

# <--------------------- Section 2 - One example per dependency type --------------------->
omi_cells = [ # Open Metadata Implementation cells
    (c, variables[c["src"]], variables[c["dest"]])
    for c in cells
    if "open-metadata-implementation" in norm(variables[c["src"]])
]

ex_impl    = None   # Implementation Dependency
ex_constr  = None   # Construction Dependency
ex_compile = None   # Compile-Time Dependency

for cell, src, dest in omi_cells:
    v = cell["values"]

    # Implementation: depends on a concrete class (Import + Call/Use),
    # no inheritance relationship (no Extend / Implement), not an Exception
    if (ex_impl is None
            and v.get("Import", 0) > 0
            and (v.get("Call", 0) > 0 or v.get("Use", 0) > 0)
            and v.get("Extend", 0) == 0
            and v.get("Implement", 0) == 0
            and "Exception" not in dest):
        ex_impl = (src, dest, v)

    # Construction: file directly instantiates a collaborator via 'new'
    if ex_constr is None and v.get("Create", 0) > 0:
        ex_constr = (src, dest, v)

    # Compile-Time: the only relationship is Import - pure compile-time coupling
    if ex_compile is None and set(v.keys()) == {"Import"}:
        ex_compile = (src, dest, v)

    if ex_impl and ex_constr and ex_compile:
        break

section("2a. IMPLEMENTATION DEPENDENCY EXAMPLE")
if ex_impl:
    s, d, v = ex_impl
    print(f"Source     : {norm(s)}")
    print(f"Depends on : {norm(d)}")
    print(f"Values     : {v}")
else:
    print("(no example found)")

section("2b. CONSTRUCTION DEPENDENCY EXAMPLE")
if ex_constr:
    s, d, v = ex_constr
    print(f"Source     : {norm(s)}")
    print(f"Depends on : {norm(d)}")
    print(f"Values     : {v}")
else:
    print("(no example found)")

section("2c. COMPILE-TIME DEPENDENCY EXAMPLE")
if ex_compile:
    s, d, v = ex_compile
    print(f"Source     : {norm(s)}")
    print(f"Depends on : {norm(d)}")
    print(f"Values     : {v}")
else:
    print("(no example found)")

# <--------------------- Section 3 - Inter-module import matrix (all 14 OMI submodules) --------------------->

def get_omi_submodule(path: str) -> str:
    """Return the direct child of open-metadata-implementation, or the
    first path segment when the file is outside that directory."""
    parts = norm(path).split("/")
    if "open-metadata-implementation" in parts:
        idx = parts.index("open-metadata-implementation")
        if idx + 1 < len(parts):
            return parts[idx + 1]
    return parts[0] if parts else path

# Submodules are discovered dynamically from the file paths in 'variables'
OMI_MODULES = sorted({
    get_omi_submodule(var)
    for var in variables
    if "open-metadata-implementation" in norm(var)
})

# Build the matrix: module_matrix[src_module][dest_module] = total imports
module_matrix = defaultdict(lambda: defaultdict(int))
for cell in cells:
    src  = variables[cell["src"]]
    dest = variables[cell["dest"]]
    sp   = get_omi_submodule(src)
    dp   = get_omi_submodule(dest)
    imp  = int(cell["values"].get("Import", 0))
    if sp != dp and sp in OMI_MODULES and dp in OMI_MODULES:
        module_matrix[sp][dp] += imp

section("3. INTER-MODULE CODE DEPENDENCIES")
print(f"{'Source module':<40}  {'Target module':<40}  {'Imports':>7}")
print(f"{'-'*40}  {'-'*40}  {'-'*7}")

THRESHOLD = 10

printed = False
for src_mod in OMI_MODULES:
    for dest_mod in OMI_MODULES:
        w = module_matrix[src_mod][dest_mod]
        if w >= THRESHOLD:
            print(f"  {src_mod:<40}  {dest_mod:<40}  {w:>7}")
            printed = True

if not printed:
    print("(no cross-module import relationships found)")

# <--------------------- Section 4 - Saving import number --------------------->
OUTPUT_FILE_FILES = "import-edges-files.csv"
OUTPUT_FILE_PACKAGES = "import-edges-packages.csv"

section("4. SAVING IMPORT NUMBER")

def get_java_package(path: str) -> str:
    path = norm(path)
    match = re.search(r'src/main/java/(.+)/[^/]+\.java$', path)
    if match:
        return match.group(1).replace("/", ".")
    return None


pkg_matrix = defaultdict(lambda: defaultdict(int))

with open(OUTPUT_FILE_FILES, "w", encoding="utf-8") as f:
    f.write("source_file,target_file,imports\n")
    for cell in cells:
        src  = variables[cell["src"]]
        dest = variables[cell["dest"]]
        imp  = int(cell["values"].get("Import", 0))

        if imp > 0:
            f.write(f"{norm(src)},{norm(dest)},{imp}\n")
                
            src_pkg  = get_java_package(src)
            dest_pkg = get_java_package(dest)
            if src_pkg and dest_pkg and src_pkg != dest_pkg:
                pkg_matrix[src_pkg][dest_pkg] += imp


with open(OUTPUT_FILE_PACKAGES, "w", encoding="utf-8") as f:
    f.write("source_package,target_package,imports\n")
    for s_pkg, targets in pkg_matrix.items():
        for d_pkg, count in targets.items():
            f.write(f"{s_pkg},{d_pkg},{count}\n")


print(f"File-level data saved to: {OUTPUT_FILE_FILES}")
print(f"Full Java Package data saved to: {OUTPUT_FILE_PACKAGES}")

# <--------------------- Final informations --------------------->
section("ANALYSIS COMPLETED")
print(f"Total files: {len(variables)}")
print(f"Total dependency edges: {len(cells)}")
