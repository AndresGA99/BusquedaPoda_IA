import networkx as nx
import matplotlib.pyplot as plt
import heapq

def branch_and_bound(graph, start, goal, heuristic):
    cola_prioridad = []
    heapq.heappush(cola_prioridad, (0, start, []))
    mejores_costes = {start: 0}
    aristas_podadas = []
    
    while cola_prioridad:
        coste_actual, nodo_actual, camino = heapq.heappop(cola_prioridad)
        
        if nodo_actual == goal:
            return camino + [nodo_actual], coste_actual, aristas_podadas
        
        for vecino in graph.neighbors(nodo_actual):
            nuevo_coste = coste_actual + graph[nodo_actual][vecino]['weight']
            coste_estimado = nuevo_coste + heuristic(vecino, goal)
            
            if vecino not in mejores_costes or nuevo_coste < mejores_costes[vecino]:
                mejores_costes[vecino] = nuevo_coste
                heapq.heappush(cola_prioridad, (coste_estimado, vecino, camino + [nodo_actual]))
            else:
                aristas_podadas.append((nodo_actual, vecino))
    
    return None, float('inf'), aristas_podadas

def heuristica(node, goal):
    return 17

# Crear el grafo
grafo = nx.Graph()
grafo.add_edge('A', 'B', weight=4)
grafo.add_edge('A', 'C', weight=2)
grafo.add_edge('B', 'D', weight=5)
grafo.add_edge('C', 'D', weight=8)
grafo.add_edge('C', 'E', weight=10)
grafo.add_edge('D', 'E', weight=2)

# Ejecutar el algoritmo
camino, coste, aristas_podadas = branch_and_bound(grafo, 'A', 'E', heuristica)

print(f"Camino óptimo: {camino} con coste: {coste}")
print(f"Podas (caminos descartados): {aristas_podadas}")

# Visualización del grafo
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(grafo)
nx.draw_networkx_nodes(grafo, pos, node_color='lightblue', node_size=500)
nx.draw_networkx_labels(grafo, pos)

# Dibujar todas las aristas
edge_labels = nx.get_edge_attributes(grafo, 'weight')
nx.draw_networkx_edge_labels(grafo, pos, edge_labels=edge_labels)
nx.draw_networkx_edges(grafo, pos, edge_color='gray', width=1)

# Resaltar el camino óptimo
camino_optimo = list(zip(camino, camino[1:]))
nx.draw_networkx_edges(grafo, pos, edgelist=camino_optimo, edge_color='r', width=2)

# Resaltar las aristas podadas
nx.draw_networkx_edges(grafo, pos, edgelist=aristas_podadas, edge_color='blue', style='dashed', width=1)

plt.title("Grafo con camino óptimo (rojo) y podas (azul punteado)")
plt.axis('off')
plt.tight_layout()
plt.show()

# Visualización del árbol de búsqueda
arbol = nx.DiGraph()
for i in range(len(camino) - 1):
    arbol.add_edge(camino[i], camino[i+1])

for arista in aristas_podadas:
    if arista[0] in camino:
        arbol.add_edge(arista[0], arista[1])

plt.figure(figsize=(12, 8))
pos = nx.spring_layout(arbol)
nx.draw_networkx_nodes(arbol, pos, node_color='lightgreen', node_size=500)
nx.draw_networkx_labels(arbol, pos)

# Dibujar aristas del camino óptimo
nx.draw_networkx_edges(arbol, pos, edgelist=camino_optimo, edge_color='r', width=2)

# Dibujar aristas podadas
podas_en_arbol = [arista for arista in aristas_podadas if arista[0] in camino]
nx.draw_networkx_edges(arbol, pos, edgelist=podas_en_arbol, edge_color='blue', style='dashed', width=1)

plt.title("Árbol de búsqueda con camino óptimo (rojo) y podas (azul punteado)")
plt.axis('off')
plt.tight_layout()
plt.show()