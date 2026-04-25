import sys
import csv
import networkx as nx

def analyze_coupling(file):
    G = nx.Graph()

    with open(file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=",")

        for row in reader:
            f1 = row["entity"]
            f2 = row["coupled"]

            if not f1.endswith(".java") or not f2.endswith(".java"):
                continue

            degree = float(row["degree"])

            G.add_edge(f1, f2, weight=degree)

    print("=== TOP HUB (file più connessi) ===")
    degrees = sorted(G.degree, key=lambda x: x[1], reverse=True)
    for node, deg in degrees[:10]:
        print(f"{node} -> {deg}")

    print("\n=== TOP COUPLING ===")
    edges = sorted(G.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)
    for e in edges[:10]:
        print(f"{e[0]} <-> {e[1]} ({e[2]['weight']})")

    print("\n=== CLUSTERS ===")
    components = list(nx.connected_components(G))
    components = sorted(components, key=len, reverse=True)

    for i, comp in enumerate(components[:5]):
        print(f"Cluster {i+1}: size {len(comp)}")
        for node in comp:
            print(f"  - {node}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py input_file")
        sys.exit(1)

    input_file = sys.argv[1]
    analyze_coupling(input_file)