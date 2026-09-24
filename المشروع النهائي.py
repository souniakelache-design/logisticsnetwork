company_name= "SOUNIA ISMAHANE KELACHE"
print(company_name)
#---------------الجزء الأول------------------
import pulp
Warehouses= ["W1", "W2", "W3"]
Markets= ["M1", "M2", "M3"]
capacity={"W1": 250, "W2": 250, "W3": 300}
Cost= {"W1": 70000, "W2": 64000, "W3": 86000}
Demand= {"M1": 60, "M2": 25, "M3": 100}
Shipping_Variables={
    ("W1", "M1"): 150, ("W1", "M2"): 150, ("W1", "M3"): 320,
    ("W2", "M1"): 120, ("W2", "M2"): 160, ("W2", "M3"): 350,
    ("W3", "M1"): 250, ("W3", "M2"): 175, ("W3", "M3"): 300
}
#-------------تعريف النموذج--------------
model = pulp.LpProblem("SOUNIA_ISMAHANE_KELACHE_EXPORT", pulp.LpMinimize)

# ---------------------المتغيرات--------------------
x = pulp.LpVariable.dicts("x", (Warehouses, Markets), lowBound=0)
y = pulp.LpVariable.dicts("y", Warehouses, cat='Binary')

# ------------دالة الهدف------------------
model += pulp.lpSum(Cost[i] * y[i] for i in Warehouses) + \
         pulp.lpSum(Shipping_Variables[(i,j)] * x[i][j] for i in Warehouses for j in Markets)

# -------------------قيود الطلب-------------
for j in Markets:
    model += pulp.lpSum(x[i][j] for i in Warehouses) == Demand[j]

# -------------قيود الاستيعاب--------------
for i in Warehouses:
    model += pulp.lpSum(x[i][j] for j in Markets) <= capacity[i] * y[i]

# حل النموذج
model.solve()

# النتائج
print("statut:", pulp.LpStatus[model.status])
for i in Warehouses:
    print(f"{i} open؟", y[i].value())
for i in Warehouses:
    for j in Markets:
        if x[i][j].value() > 0:
            print(f"Shipping_Variables {x[i][j].value()} tons from {i} to {j}")
print("Total cost =", pulp.value(model.objective))
import networkx as nx
import matplotlib.pyplot as plt

# إنشاء شبكة موجهة
G = nx.DiGraph()

# إضافة العقد (المراكز والأسواق)
for c in Warehouses:
    G.add_node(c, pos=(0, Warehouses.index(c)*2))  # المراكز على اليسار
for m in Markets:
    G.add_node(m, pos=(6, Markets.index(m)*2))  # الأسواق على اليمين

# إضافة الحواف التي تم شحنها فقط (x[i][j] > 0)
for i in Warehouses:
    for j in Markets:
        if x[i][j].value() > 0:
            G.add_edge(i, j, weight=Shipping_Variables[(i, j)], flow=x[i][j].value())
# استخراج المواقع
pos = nx.get_node_attributes(G, 'pos')

# رسم العقد
nx.draw_networkx_nodes(G, pos, nodelist=Warehouses, node_color='Pink', node_size=1500, label='Warehouses')
nx.draw_networkx_nodes(G, pos, nodelist=Markets, node_color='Skyblue', node_size=1500, label='Markets')

# رسم الحواف (مع عرض سماكة حسب كمية الشحن)
edges = G.edges()
widths = [G[u][v]['flow']/100 for u, v in edges]  # لتوضيح الكميات
nx.draw_networkx_edges(G, pos, edgelist=edges, width=widths, arrows=True, arrowstyle='-|>', arrowsize=15)

# كتابة أسماء العقد
nx.draw_networkx_labels(G, pos, font_size=10, font_color='black')

# كتابة القيم على الحواف (كمية وتكلفة)
edge_labels = {(u, v): f"{G[u][v]['flow']} @ {G[u][v]['weight']}" for u, v in G.edges()}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

# إعداد الشكل العام
plt.title("SOUNIA_ISMAHANE_KELACHE_EXPORT", fontsize=12)
plt.axis('off')
plt.legend()
plt.show()