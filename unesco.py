# -*- coding: utf-8 -*-
"""
Created on Thu Apr 24 15:15:37 2025

@author: jveraz
"""

import pickle
from rdflib import Graph, RDF, SKOS
import networkx as nx
import matplotlib.pyplot as plt

# === Configuración inicial ===
TTL_PATH = "unesco-thesaurus.ttl"  # Reemplazar con tu archivo real
g = Graph()
g.parse(TTL_PATH, format="turtle")

# === Crear grafo dirigido ===
G = nx.DiGraph()

# === Agregar nodos y relaciones ===
for concept in g.subjects(RDF.type, SKOS.Concept):
    label = g.value(concept, SKOS.prefLabel, any=True)
    alt_labels = [str(lit) for lit in g.objects(concept, SKOS.altLabel)]
    G.add_node(str(concept), label=str(label) if label else str(concept), altLabels=alt_labels)

    # skos:broader (jerarquía)
    for broader in g.objects(concept, SKOS.broader):
        G.add_edge(str(broader), str(concept), type="broader")

    # skos:related (asociación)
    for related in g.objects(concept, SKOS.related):
        G.add_edge(str(concept), str(related), type="related")
        
# === Guardar grafo como archivo Pickle ===
with open("unesco_graph.pkl", "wb") as f:
    pickle.dump(G, f)


