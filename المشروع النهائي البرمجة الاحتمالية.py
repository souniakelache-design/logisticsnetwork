company_name = "SOUNIA ISMAHANE KELACHE"
print(company_name)

# ---------------الجزء الثاني------------------
from pulp import *

Warehouses = ["W1", "W2", "W3"]
Markets = ["M4", "M5", "M6"]
scenarios = ["s1", "s2"]

capacity = {"W1": 250, "W2": 250, "W3": 300}
Cost = {"W1": 70000, "W2": 64000, "W3": 86000}
scenarios_prob = {"s1": 0.4, "s2": 0.6}

Demand = {
    "s1": {"M4": 250, "M5": 175, "M6": 210},
    "s2": {"M4": 310, "M5": 288, "M6": 202}
}

Shipping_Variables = {
    ("W1", "M4"): 180, ("W1", "M5"): 100, ("W1", "M6"): 200,
    ("W2", "M4"): 120, ("W2", "M5"): 230, ("W2", "M6"): 180,
    ("W3", "M4"): 250, ("W3", "M5"): 90,  ("W3", "M6"): 300
}

# -------------تعريف النموذج--------------
model = LpProblem("SOUNIA_ISMAHANE_KELACHE_EXPORT", LpMinimize)
ship = LpVariable.dicts("Ship", (scenarios, Warehouses, Markets), lowBound=0)
open_warehouse = LpVariable.dicts("Open", Warehouses, cat="Binary")
# دالة الهدف
model += lpSum(
    scenarios_prob[s] * Shipping_Variables[(w, m)] * ship[s][w][m]
    for s in scenarios for w in Warehouses for m in Markets
) + lpSum(Cost[w] * open_warehouse[w] for w in Warehouses)
# قيود الاستيعاب
for w in Warehouses:
    for s in scenarios:
        model += lpSum(ship[s][w][m] for m in Markets) <= capacity[w] * open_warehouse[w]
# قيود الطلب
for s in scenarios:
    for m in Markets:
        model += lpSum(ship[s][w][m] for w in Warehouses) >= Demand[s][m]
# حل النموذج
model.solve(PULP_CBC_CMD(msg=True))
# النتائج
print("\nنتائج الشحن:")
for s in scenarios:
    for w in Warehouses:
        for m in Markets:
            print(f"Ship[{s},{w},{m}] = {ship[s][w][m].value():.2f}")
print("\nالمستودعات المفتوحة:")
for w in Warehouses:
    print(f"{w}: {open_warehouse[w].value()}")
print(f"\nالقيمة المثلى للدالة الهدف المتوقعة = {value(model.objective):,.2f}")

import matplotlib.pyplot as plt
import networkx as nx

fig, axes = plt.subplots(1, len(scenarios), figsize=(16, 7))

# تحديد مواقع العقد الموحدة
pos = {}
for i, node in enumerate(Warehouses):
    pos[node] = (1, 3 - i * 1.5)
for i, node in enumerate(Markets):
    pos[node] = (2, 3 - i * 1.5)
# رسم شبكة لكل سيناريو
for idx, s in enumerate(scenarios):
    ax = axes[idx]
    G = nx.DiGraph()
    # إضافة العقد
    G.add_nodes_from(Warehouses, bipartite=0)
    G.add_nodes_from(Markets, bipartite=1)
    # تحديد حالة المستودعات (مفتوح / مغلق)
    open_status = {w: open_warehouse[w].value() for w in Warehouses}
    node_colors_w = ['#4C72B0' if open_status[w] > 0.5 else '#A8B6C1' for w in Warehouses]
    edge_labels = {}
    edge_widths = []

    for w in Warehouses:
        for m in Markets:
            qty = ship[s][w][m].value()
            if qty and qty > 0:
                cost = Shipping_Variables[(w, m)]
                G.add_edge(w, m, weight=qty)
                edge_labels[(w, m)] = f"Qty:{int(qty)}\nCost:{cost}"
                edge_widths.append(1.0 + (qty / 50))
    # رسم المستودعات والأسواق
    nx.draw_networkx_nodes(G, pos, nodelist=Warehouses, node_color=node_colors_w, node_size=2200, ax=ax)
    nx.draw_networkx_nodes(G, pos, nodelist=Markets, node_color='#55A868', node_size=2200, ax=ax)
    # أسماء العقد
    nx.draw_networkx_labels(G, pos, font_size=11, font_color='white', font_weight='bold', ax=ax)
    # الأسهم والوصلات النشطة
    if G.edges():
        nx.draw_networkx_edges(G, pos, edge_color='#C44E52', width=edge_widths,
                               arrowsize=20, alpha=0.8, ax=ax, connectionstyle="arc3,rad=0.05")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, label_pos=0.35, ax=ax)
    # عنوان الشكل الفرعي
    ax.set_title(f"Scenario: {s} (Prob: {scenarios_prob[s]})\nTotal Demand: {sum(Demand[s].values())}",
                 fontsize=12, fontweight='bold', pad=15)
    ax.axis('off')
plt.suptitle(f"{company_name} - Stochastic Shipping Optimization", fontsize=16, fontweight='bold', y=0.98)
plt.figlegend([
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#4C72B0', markersize=12, label='Open Warehouse'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#A8B6C1', markersize=12, label='Closed Warehouse'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#55A868', markersize=12, label='Market Demand'),
    plt.Line2D([0], [0], color='#C44E52', lw=2, label='Active Flow (Qty)')
], ['Open Warehouse', 'Closed Warehouse', 'Market Demand', 'Active Flow'],
    loc='lower center', ncol=4, bbox_to_anchor=(0.5, 0.02), frameon=True)
plt.tight_layout(rect=[0, 0.08, 1, 0.93])
plt.show()