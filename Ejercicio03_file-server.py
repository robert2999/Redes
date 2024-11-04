import sys
import time
from collections import defaultdict
import heapq

# Definición de las topologías de redgit add README.md
topologias = {
    '1': {  # Topología básica con 6 nodos
        'A': {'B': 4, 'C': 2},
        'B': {'A': 4, 'C': 1, 'D': 5},
        'C': {'A': 2, 'B': 1, 'D': 8, 'E': 10},
        'D': {'B': 5, 'C': 8, 'E': 2, 'F': 6},
        'E': {'C': 10, 'D': 2, 'F': 3},
        'F': {'D': 6, 'E': 3}
    },
    '2': {  # Topología compleja con 12 nodos
        'A': {'B': 3, 'C': 1},
        'B': {'A': 3, 'D': 4, 'E': 2},
        'C': {'A': 1, 'F': 5, 'G': 2},
        'D': {'B': 4, 'H': 7},
        'E': {'B': 2, 'H': 5, 'I': 6},
        'F': {'C': 5, 'G': 3, 'J': 8},
        'G': {'C': 2, 'F': 3, 'J': 4, 'K': 7},
        'H': {'D': 7, 'E': 5, 'I': 1, 'K': 3},
        'I': {'E': 6, 'H': 1, 'K': 2, 'L': 4},
        'J': {'F': 8, 'G': 4, 'K': 1, 'L': 5},
        'K': {'G': 7, 'H': 3, 'I': 2, 'J': 1, 'L': 2},
        'L': {'I': 4, 'J': 5, 'K': 2}
    }
}

def dijkstra(grafo, inicio):
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    visi
    heap = [(0, inicio)]
    prev = {nodo: None for nodo in grafo}

    while heap:
        (dist, actual) = heapq.heappop(heap)
        if actual in visitados:
            continue
        visitados.add(actual)

        for vecino, peso in grafo[actual].items():
            if vecino in visitados:
                continue
            nueva_dist = dist + peso
            if nueva_dist < distancias[vecino]:
                distancias[vecino] = nueva_dist
                prev[vecino] = actual
                heapq.heappush(heap, (nueva_dist, vecino))

    return distancias, prev

def bellman_ford(grafo, inicio):
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0
    prev = {nodo: None for nodo in grafo}

    for _ in range(len(grafo) - 1):
        for nodo in grafo:
            for vecino, peso in grafo[nodo].items():
                if distancias[nodo] + peso < distancias[vecino]:
                    distancias[vecino] = distancias[nodo] + peso
                    prev[vecino] = nodo

    # Verificar ciclos negativos
    for nodo in grafo:
        for vecino, peso in grafo[nodo].items():
            if distancias[nodo] + peso < distancias[vecino]:
                raise ValueError("El grafo contiene un ciclo de peso negativo")

    return distancias, prev

def reconstruir_camino(prev, destino):
    camino = []
    while destino is not None:
        camino.insert(0, destino)
        destino = prev[destino]
    return camino

def seleccionar_topologia():
    print("Selecciona la topología de red:")
    print("1. Topología básica (6 nodos)")
    print("2. Topología compleja (12 nodos)")
    seleccion = input("Ingresa el número de la topología (1 o 2): ")
    if seleccion in topologias:
        return topologias[seleccion]
    else:
        print("Selección inválida. Se seleccionará la topología básica por defecto.")
        return topologias['1']

def seleccionar_algoritmo():
    print("\nSelecciona el algoritmo de enrutamiento:")
    print("1. Dijkstra")
    print("2. Bellman-Ford")
    seleccion = input("Ingresa el número del algoritmo (1 o 2): ")
    if seleccion == '1':
        return 'dijkstra'
    elif seleccion == '2':
        return 'bellman_ford'
    else:
        print("Selección inválida. Se seleccionará Dijkstra por defecto.")
        return 'dijkstra'

def obtener_nodos(grafo):
    print("\nNodos disponibles:")
    print(", ".join(grafo.keys()))
    origen = input("Ingresa el nodo de origen: ").strip().upper()
    while origen not in grafo:
        print("Nodo inválido. Inténtalo de nuevo.")
        origen = input("Ingresa el nodo de origen: ").strip().upper()
    destino = input("Ingresa el nodo de destino: ").strip().upper()
    while destino not in grafo:
        print("Nodo inválido. Inténtalo de nuevo.")
        destino = input("Ingresa el nodo de destino: ").strip().upper()
    return origen, destino

def main():
    grafo = seleccionar_topologia()
    algoritmo = seleccionar_algoritmo()
    origen, destino = obtener_nodos(grafo)

    print(f"\nCalculando la ruta más corta desde {origen} hasta {destino} usando {algoritmo.replace('_', ' ').title()}...")

    inicio_tiempo = time.time()
    try:
        if algoritmo == 'dijkstra':
            distancias, prev = dijkstra(grafo, origen)
        else:
            distancias, prev = bellman_ford(grafo, origen)
    except ValueError as e:
        print(e)
        sys.exit(1)
    fin_tiempo = time.time()

    if distancias[destino] == float('inf'):
        print("No hay ruta disponible entre los nodos seleccionados.")
    else:
        camino = reconstruir_camino(prev, destino)
        print(f"Ruta más corta: {' -> '.join(camino)}")
        print(f"Costo total: {distancias[destino]}")
        print(f"Tiempo de ejecución: {fin_tiempo - inicio_tiempo:.6f} segundos")

if __name__ == "__main__":
    main()
