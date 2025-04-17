import pickle
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout


def print_ast_nodes(glow_input):
    print("\n-- AST Nodes --")
    graph = glow_input.ast_graph.graph
    node_labels = glow_input.ast_graph.node_to_label

    for node in sorted(graph.nodes):
        label = node_labels.get(node)
        if label is None:
            print(f"Node {node}: <no label>")
            continue

        addr = getattr(label, "addr", None)
        ast_val = getattr(label, "ast_val", None)

        print(f"Node {node}:")
        print(f"  Addr: {hex(addr) if addr is not None else 'N/A'}")
        print(f"  Value: {ast_val}")


def draw_ast_graph(glow_input, out_path="ast_graph.png"):
    graph = glow_input.ast_graph.graph
    node_labels = glow_input.ast_graph.node_to_label
    edge_labels_dict = glow_input.ast_graph.edge_to_labels

    # ノードラベル作成
    labels = {}
    for node in graph.nodes:
        label = node_labels.get(node)
        if label is not None:
            addr = getattr(label, "addr", None)
            val = getattr(label, "ast_val", "")
            labels[node] = f"{hex(addr) if addr else 'N/A'}\n{val}"
        else:
            labels[node] = str(node)

    # エッジラベル作成
    edge_labels = {}
    for edge, label_set in edge_labels_dict.items():
        edge_labels[edge] = ",".join(sorted(label_set))

    # レイアウト
    try:
        pos = graphviz_layout(graph, prog="dot")
    except:
        pos = nx.spring_layout(graph)

    # 描画
    plt.figure(figsize=(16, 14))
    nx.draw(graph, pos, with_labels=True, labels=labels,
            node_size=800, font_size=8, node_color="lightblue", edge_color="gray")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=6)
    plt.title("AST Graph with Edge Labels")
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    print(f"[INFO] ASTグラフを保存しました → {out_path}")


# === Main ===
with open("/src/datasets/generation/O0/libcjson.so.1.7.15.pkl", "rb") as f:
    data = pickle.load(f)

if isinstance(data, list) and isinstance(data[0], tuple):
    glow_input, glow_output = data[0]

    print("Function:", glow_input.function_name)
    print("Binary:", glow_input.input_file_name)
    print("File:", glow_input.file_name)
    print("Range:", glow_input.low_high_pc)
    print("Arch:", glow_input.arch)

    print("\n-- Variables --")
    for var in glow_input.vars:
        print(f"  Name: {var.name}")
        print(f"  Locs:")
        for l in var.locs:
            try:
                low, high, loc_obj = l
                loc_type = type(loc_obj).__name__
                offset = getattr(loc_obj, 'offset', getattr(loc_obj, 'arg', 'n/a'))
                print(f"    - {loc_type}@{offset} ({hex(low)} - {hex(high)})")
            except Exception as e:
                print(f"    - <invalid location: {e}>")
        print(f"  Nodes: {var.nodes}")

    print("\n-- Types --")
    for ty in glow_output.types:
        print(f"  {ty}")

    print_ast_nodes(glow_input)
    draw_ast_graph(glow_input, "ast_output.png")
else:
    print("[ERROR] Unexpected pickle format.")
