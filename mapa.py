class Mapa:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.grid = [[0 for _ in range(ancho)] for _ in range(alto)]

    def agregar_obstaculo(self, x, y):
        if 0 <= x < self.ancho and 0 <= y < self.alto:
            self.grid[y][x] = 1

    def es_valido(self, x, y):
        return 0 <= x < self.ancho and 0 <= y < self.alto and self.grid[y][x] == 0

    def vecinos(self, x, y):
        movimientos = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        resultado = []
        for dx, dy in movimientos:
            nx, ny = x + dx, y + dy
            if self.es_valido(nx, ny):
                resultado.append((nx, ny))
        return resultado
