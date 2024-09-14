import networkx as nx
import heapq


def branch_and_bound(graph, start, goal, heuristic):
    # Cola de prioridad para manejar los nodos (prioridad por coste estimado)
    cola_prioridad = []
    
    # Almacenar los nodos iniciales con su coste 0 y la estimación
    heapq.heappush(cola_prioridad, (0, start, []))
    
    # Almacenar los mejores costes hacia cada nodo
    mejores_costes = {start: 0}
    
    # Almacenar las aristas que fueron exploradas pero no seleccionadas (poda)
    aristas_podadas = []

    while cola_prioridad:
        # Sacar el nodo actual con el coste más bajo de la cola
        coste_actual, nodo_actual, camino = heapq.heappop(cola_prioridad)
        
        # Si llegamos al nodo objetivo, retornar el camino, el coste y las podas
        if nodo_actual == goal:
            return camino + [nodo_actual], coste_actual, aristas_podadas
        
        # Extender la rama actual (explorar vecinos)
        for vecino in graph.neighbors(nodo_actual):
            nuevo_coste = coste_actual + graph[nodo_actual][vecino]['weight']
            coste_estimado = nuevo_coste + heuristic(vecino, goal)
            
            # Solo explorar si el nuevo coste es mejor que el conocido
            if vecino not in mejores_costes or nuevo_coste < mejores_costes[vecino]:
                mejores_costes[vecino] = nuevo_coste
                heapq.heappush(cola_prioridad, (coste_estimado, vecino, camino + [nodo_actual]))
            else:
                # Si el nuevo camino no es mejor, lo consideramos como una poda
                aristas_podadas.append((nodo_actual, vecino))
    
    return None, float('inf'), aristas_podadas


def heuristica(node, goal):
    return 10

grafo = nx.Graph()

grafo.add_edge('A', 'B', weight=7)
grafo.add_edge('A', 'C', weight=9)
grafo.add_edge('A', 'F', weight=14)
grafo.add_edge('B', 'C', weight=10)
grafo.add_edge('B', 'D', weight=15)
grafo.add_edge('C', 'D', weight=11)
grafo.add_edge('C', 'F', weight=2)
grafo.add_edge('D', 'E', weight=6)
grafo.add_edge('E', 'F', weight=9)

'''
graph.add_edge('A', 'B', weight=4)
graph.add_edge('A', 'C', weight=2)
graph.add_edge('B', 'D', weight=5)
graph.add_edge('C', 'D', weight=8)
graph.add_edge('C', 'E', weight=10)
graph.add_edge('D', 'E', weight=2)'''

'''
graph.add_edge('Madrid', 'Barcelona', weight=620)
graph.add_edge('Madrid', 'Valencia', weight=355)
graph.add_edge('Barcelona', 'Zaragoza', weight=300)
graph.add_edge('Valencia', 'Zaragoza', weight=310)
graph.add_edge('Madrid', 'Sevilla', weight=530)
graph.add_edge('Sevilla', 'Malaga', weight=205)
graph.add_edge('Zaragoza', 'Bilbao', weight=330)
graph.add_edge('Bilbao', 'Valencia', weight=620)
graph.add_edge('Bilbao', 'Santander', weight=100)
graph.add_edge('Malaga', 'Granada', weight=125)
graph.add_edge('Granada', 'Valencia', weight=490)
graph.add_edge('Santander', 'Zaragoza', weight=400)'''

camino, coste, aristas_podadas = branch_and_bound(grafo, 'A', 'F', heuristica)

print(f"Camino óptimo: {camino} con coste: {coste}")
print(f"Podas (caminos descartados): {aristas_podadas}")