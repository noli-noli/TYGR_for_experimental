import sys
import angr

# angr依存の外部クラス（事前に配置済みであること）
from src.analysis.angr.ast_graph import AstGraph

# === 対象バイナリのパス ===
BINARY_PATH = "/src/datasets/x86_64/c_cpp/app-accessibility/at-spi2-atk-2.38.0/libatk-bridge-2.0.so.0.0.0"

# === angrプロジェクト生成 ===
proj = angr.Project(BINARY_PATH, auto_load_libs=False)

# === main関数のアドレス取得 ===
sym = proj.loader.find_symbol("main")
if sym is None:
    print("mainシンボルが見つかりません")
    sys.exit(1)

main_addr = sym.rebased_addr

# === 実行状態（blank state）を作成 ===
state = proj.factory.blank_state(addr=main_addr)

# === 引数をシンボリックに指定（任意） ===
state.regs.rdi = state.solver.BVS("arg_rdi", 64)

# === 実行を数ステップ進める ===
simgr = proj.factory.simgr(state)
simgr.step(n=5)

# === アクティブな状態を取得（失敗していないかチェック） ===
if len(simgr.active) == 0:
    print("アクティブな状態がありません")
    sys.exit(1)

# === ASTグラフを生成 ===
g = AstGraph()
func_param_locs = []  # 関数引数オフセットが必要なら指定（空でも可）

# === ASTグラフ構築 ===
g.process_state(simgr.active[0], func_param_locs)

# === グラフを描画・保存 ===
g.plot("ast_graph.png", save=True, show=False)
print("グラフを ast_graph.png に保存しました")
