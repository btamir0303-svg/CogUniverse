from core.framework import UDSFSystem
from ai.emergent import KnowledgeEmergence
from experiments.metrics import KnowledgeGraphMetrics

if __name__ == "__main__":
    print("=" * 50)
    print(" CogUniverse - Knowledge Emergence System")
    print("=" * 50)

    udsf = UDSFSystem()

    engine = KnowledgeEmergence()
    files = ["knowledge/tao.txt", "knowledge/psych.txt", "knowledge/complex.txt"]
    engine.load_knowledge(files)
    engine.build_vector_db()
    print(f"Loaded knowledge units: {len(engine.knowledge_units)}")

    relations = engine.build_relations(threshold=0.65)

    metrics = KnowledgeGraphMetrics()
    G = metrics.build_graph(engine.knowledge_units, relations)
    report = metrics.full_analysis(G)

    metrics.print_report(report)

    # ======================== 可视化输出 ========================
    metrics.plot_network(G)
    metrics.plot_metrics(report["entropy"], report["density"])
    # metrics.plot_interactive_network(G)

    print("\n✅ 全部可视化图片已生成！")