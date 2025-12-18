import heapq
import math


# ==========================
# KNAPSACK 0/1 (GENÉRICO)
# - capacidad y costes deben ser enteros (unidades)
# - valor_fn(item) devuelve el "beneficio" a maximizar (int)
# - coste_fn(item) devuelve el coste en "unidades" (int)
# ==========================
def knapsack(items, capacidad, valor_fn, coste_fn):
    n = len(items)
    dp = [[0] * (capacidad + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        item = items[i - 1]
        c = coste_fn(item)
        v = valor_fn(item)
        for cap in range(capacidad + 1):
            if c <= cap:
                dp[i][cap] = max(dp[i - 1][cap], dp[i - 1][cap - c] + v)
            else:
                dp[i][cap] = dp[i - 1][cap]

    # reconstrucción
    seleccion = []
    cap = capacidad
    for i in range(n, 0, -1):
        if dp[i][cap] != dp[i - 1][cap]:
            item = items[i - 1]
            seleccion.append(item)
            cap -= coste_fn(item)

    return list(reversed(seleccion))


# ==========================
# A* PATHFINDING (grid 4-dir)
# Devuelve lista de nodos (x,y), o None si no hay ruta
# ==========================
def heuristica_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star(mapa, inicio, objetivo):
    frontera = []
    heapq.heappush(frontera, (0, inicio))
    came_from = {inicio: None}
    coste = {inicio: 0}

    while frontera:
        _, actual = heapq.heappop(frontera)

        if actual == objetivo:
            break

        for vecino in mapa.vecinos(*actual):
            nuevo_coste = coste[actual] + 1
            if vecino not in coste or nuevo_coste < coste[vecino]:
                coste[vecino] = nuevo_coste
                prioridad = nuevo_coste + heuristica_manhattan(objetivo, vecino)
                heapq.heappush(frontera, (prioridad, vecino))
                came_from[vecino] = actual

    if objetivo not in came_from:
        return None  # no hay ruta

    # reconstrucción
    ruta = []
    nodo = objetivo
    while nodo is not None:
        ruta.append(nodo)
        nodo = came_from[nodo]
    ruta.reverse()
    return ruta


# ==========================
# MST – PRIM
# Devuelve lista de aristas (a, b, distancia)
# ==========================
def distancia(a, b):
    return math.dist(a, b)


def prim(nodos):
    if len(nodos) < 2:
        return []

    visitados = set()
    mst = []
    heap = []
    contador = 0

    inicio = nodos[0]
    visitados.add(inicio)

    for n in nodos[1:]:
        heapq.heappush(heap, (distancia(inicio.posicion, n.posicion), contador, inicio, n))
        contador += 1

    while heap:
        dist, _, a, b = heapq.heappop(heap)
        if b in visitados:
            continue

        visitados.add(b)
        mst.append((a, b, dist))

        for n in nodos:
            if n not in visitados:
                heapq.heappush(heap, (distancia(b.posicion, n.posicion), contador, b, n))
                contador += 1

    return mst
