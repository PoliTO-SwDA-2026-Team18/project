import json
from collections import defaultdict

# <--------------------- Load JSON --------------------->
INPUT_FILE = "imports-matrix.json"

with open(INPUT_FILE, encoding="utf-8") as f:
    data = json.load(f)

# 'variables' is a plain list: position = numeric ID used in cells
# e.g. variables[0] = "path/to/FileA.java"  →  ID 0 refers to FileA
variables = data["variables"]
cells     = data["cells"]       # list of {src: int, dest: int, values: dict}

idx_to_name = {i: variables[i] for i in range(len(variables))}

# <--------------------- Helpers --------------------->
SEP = "─" * 80

def norm(path: str) -> str:
    """Normalize path separators to forward slashes."""
    return path.replace("\\", "/")

def get_submodule(path: str) -> str:
    """Return the direct child of open-metadata-implementation, or the
    first path segment when the file is outside that directory."""
    parts = norm(path).split("/")
    if "open-metadata-implementation" in parts:
        idx = parts.index("open-metadata-implementation")
        if idx + 1 < len(parts):
            return parts[idx + 1]
    return parts[0] if parts else path

def section(title: str) -> None:
    print(f"\n{SEP}")
    print(f"  {title}")
    print(SEP)

# <--------------------- Build per-file import counters --------------------->
# import_out[file] = total Import edges leaving that file   (outgoing)
# import_in[file]  = total Import edges arriving at that file (incoming)
import_out: dict = defaultdict(int)
import_in:  dict = defaultdict(int)

for cell in cells:
    src  = idx_to_name[cell["src"]]
    dest = idx_to_name[cell["dest"]]
    imp  = int(cell["values"].get("Import", 0))
    if imp:
        import_out[src]  += imp
        import_in[dest]  += imp

# <--------------------- Section 1 – Top 5 files with the most outgoing imports --------------------->
files_with_import = {k: v for k, v in import_out.items() if v >= 1}
top5_out    = sorted(files_with_import.items(), key=lambda x: -x[1])[:5]
bottom5_out = sorted(files_with_import.items(), key=lambda x:  x[1])[:5]
top5_in     = sorted(import_in.items(),         key=lambda x: -x[1])[:5]

section("1. TOP 5 FILES WITH THE MOST OUTGOING IMPORTS")
for rank, (name, val) in enumerate(top5_out, 1):
    print(f"  {rank}. imports={val:>3}  {norm(name)}")

# <--------------------- Section 2 – Bottom 5 files with the fewest outgoing imports (>=1) --------------------->
section("2. BOTTOM 5 FILES WITH THE FEWEST OUTGOING IMPORTS  (minimum 1)")
for rank, (name, val) in enumerate(bottom5_out, 1):
    print(f"  {rank}. imports={val:>3}  {norm(name)}")

# <--------------------- Section 3 – Top 5 most imported files (incoming) --------------------->
section("3. TOP 5 MOST IMPORTED FILES  (incoming import count)")
for rank, (name, val) in enumerate(top5_in, 1):
    print(f"  {rank}. imported_by={val:>3}  {norm(name)}")

# <--------------------- Section 4 – One example per dependency type --------------------->
# Only look inside open-metadata-implementation for cleaner examples.
omi_cells = [
    (c, idx_to_name[c["src"]], idx_to_name[c["dest"]])
    for c in cells
    if "open-metadata-implementation" in norm(idx_to_name.get(c["src"], ""))
]

ex_impl    = None   # Implementation Dependency
ex_constr  = None   # Construction Dependency
ex_compile = None   # Compile-Time Dependency

for cell, src, dest in omi_cells:
    v = cell["values"]

    # Construction: file directly instantiates a collaborator via 'new'
    if ex_constr is None and v.get("Create", 0) > 0:
        ex_constr = (src, dest, v)

    # Implementation: depends on a concrete class (Import + Call/Use),
    # no inheritance relationship (no Extend / Implement), not an Exception
    if (ex_impl is None
            and v.get("Import", 0) > 0
            and (v.get("Call", 0) > 0 or v.get("Use", 0) > 0)
            and v.get("Extend", 0) == 0
            and v.get("Implement", 0) == 0
            and "Exception" not in dest):
        ex_impl = (src, dest, v)

    # Compile-Time: the only relationship is Import - pure compile-time coupling
    if ex_compile is None and set(v.keys()) == {"Import"}:
        ex_compile = (src, dest, v)

    if ex_impl and ex_constr and ex_compile:
        break

section("4a. IMPLEMENTATION DEPENDENCY EXAMPLE")
print("    Signal: Import + (Call | Use), no Extend/Implement -> depends on a concrete class")
if ex_impl:
    s, d, v = ex_impl
    print(f"  Source     : {norm(s)}")
    print(f"  Depends on : {norm(d)}")
    print(f"  Values     : {v}")
else:
    print("  (no example found)")

section("4b. CONSTRUCTION DEPENDENCY EXAMPLE")
print("    Signal: Create present -> source directly instantiates the collaborator")
if ex_constr:
    s, d, v = ex_constr
    print(f"  Source     : {norm(s)}")
    print(f"  Depends on : {norm(d)}")
    print(f"  Values     : {v}")
else:
    print("  (no example found)")

section("4c. COMPILE-TIME DEPENDENCY EXAMPLE")
print("    Signal: Import only, nothing else -> module must know the other at compile time")
if ex_compile:
    s, d, v = ex_compile
    print(f"  Source     : {norm(s)}")
    print(f"  Depends on : {norm(d)}")
    print(f"  Values     : {v}")
else:
    print("  (no example found)")

# <--------------------- Section 5 – Inter-module import matrix (all 14 OMI submodules) --------------------->
# Submodules are discovered dynamically from the file paths in 'variables'
all_submodules = set()
for var in variables:
    parts = norm(var).split("/")
    if "open-metadata-implementation" in parts:
        idx = parts.index("open-metadata-implementation")
        if idx + 1 < len(parts):
            all_submodules.add(parts[idx + 1])

OMI_MODULES = sorted(all_submodules)

# Build the matrix: pkg_matrix[src_module][dest_module] = total imports
pkg_matrix = defaultdict(lambda: defaultdict(int))
for cell in cells:
    src  = idx_to_name[cell["src"]]
    dest = idx_to_name[cell["dest"]]
    sp   = get_submodule(src)
    dp   = get_submodule(dest)
    imp  = int(cell["values"].get("Import", 0))
    if sp != dp and sp in OMI_MODULES and dp in OMI_MODULES and imp:
        pkg_matrix[sp][dp] += imp

section("5. INTER-MODULE CODE DEPENDENCIES  (metric: import count, full module names)")
print(f"  {'Source module':<40}  {'Target module':<40}  {'Imports':>7}")
print(f"  {'-'*40}  {'-'*40}  {'-'*7}")

THRESHOLD = 10

printed = False
for src_mod in OMI_MODULES:
    for dest_mod in OMI_MODULES:
        w = pkg_matrix[src_mod][dest_mod]
        if w >= THRESHOLD:
            print(f"  {src_mod:<40}  {dest_mod:<40}  {w:>7}")
            printed = True

if not printed:
    print("  (no cross-module import relationships found)")

print(f"\n{SEP}")
print(f"  Analysis complete  |  total files: {len(variables)}  |  total dependency edges: {len(cells)}")
print(SEP)
