# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 15:58:33 2025

@author: jveraz
"""

import pickle
import networkx as nx
import matplotlib.pyplot as plt
from collections import Counter

# === Paso 1: Cargar el grafo guardado en Pickle ===
with open("unesco_graph.pkl", "rb") as f:
    G = pickle.load(f)

# === Paso 2: Características básicas del grafo ===
print("🔹 Número de nodos:", G.number_of_nodes())
print("🔹 Número de aristas:", G.number_of_edges())

# Tipos de aristas
edge_types = [d['type'] for _, _, d in G.edges(data=True) if 'type' in d]
print("🔹 Tipos de relaciones:")
print(Counter(edge_types))

# === Paso 3: Seleccionar un subgrafo ===
top_nodes = sorted(G.degree, key=lambda x: x[1], reverse=True)[:100]
selected_nodes = [n for n, _ in top_nodes]
subG = G.subgraph(selected_nodes)

# === Paso 4: Visualizar el subgrafo ===
plt.figure(figsize=(14, 10))
pos = nx.spring_layout(subG, k=0.6)

# Colores por tipo de relación
edges_broader = [(u, v) for u, v, d in subG.edges(data=True) if d.get("type") == "broader"]
edges_related = [(u, v) for u, v, d in subG.edges(data=True) if d.get("type") == "related"]

nx.draw_networkx_nodes(subG, pos, node_size=600, node_color='lightblue')
nx.draw_networkx_edges(subG, pos, edgelist=edges_broader, edge_color='gray', arrows=True)
nx.draw_networkx_edges(subG, pos, edgelist=edges_related, edge_color='green', style='dashed', arrows=False)

labels = nx.get_node_attributes(subG, 'label')
nx.draw_networkx_labels(subG, pos, labels=labels, font_size=8)

plt.title("Subgrafo UNESCO: top 20 nodos más conectados", fontsize=14)
plt.axis('off')
plt.tight_layout()
plt.show()
