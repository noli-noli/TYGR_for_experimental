import pickle
import pprint

def inspect_pickle(path):
    with open(path, "rb") as f:
        data = pickle.load(f)

    if isinstance(data, list) and isinstance(data[0], tuple):
        glow_input, glow_output = data[0]
    elif isinstance(data, tuple):
        glow_input, glow_output = data
    else:
        print("[!] 不明なフォーマットです")
        return

    print("=== GlowInput ===")
    print(f"Function: {glow_input.function_name}")
    print(f"Binary: {glow_input.input_file_name}")
    print(f"File: {glow_input.file_name}")
    print(f"Range: {glow_input.low_high_pc}")
    print(f"Arch: {glow_input.arch}")
    print()

    print("=== Variables ===")
    for var in glow_input.vars:
        print(f"Name: {var.name}")
        print("Locs:")
        for loc in var.locs:
            try:
                low, high, loc_obj = loc
                loc_type = type(loc_obj).__name__
                offset = getattr(loc_obj, 'offset', getattr(loc_obj, 'arg', 'n/a'))
                print(f"  - {loc_type}@{offset} ({hex(low)} - {hex(high)})")
            except Exception as e:
                print(f"  - <invalid location: {e}>")
        print(f"Nodes: {var.nodes}")
    print()

    print("=== Types ===")
    for ty in glow_output.types:
        print(ty)
    print()

    print("=== AST Nodes ===")
    graph = glow_input.ast_graph.graph
    node_labels = glow_input.ast_graph.node_to_label
    for node in sorted(graph.nodes):
        label = node_labels.get(node)
        print(f"Node {node}:")
        if label:
            print(f"  Addr: {hex(label.addr) if getattr(label, 'addr', None) else 'N/A'}")
            print(f"  AST: {getattr(label, 'ast', None)}")
            print(f"  Value: {getattr(label, 'ast_val', None)}")
        else:
            print("  <No label>")

    print("\n=== Edges ===")
    for u, v, attr in graph.edges(data=True):
        print(f"{u} → {v}")
        pprint.pprint(attr)

if __name__ == "__main__":
    inspect_pickle("sample.pkl")
