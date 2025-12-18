class Edificio:
    def __init__(self, nombre, coste, beneficio, posicion, trabajo_necesario=20):
        self.nombre = nombre
        self.coste = coste
        self.beneficio = beneficio
        self.posicion = posicion  # (x, y)

        # simulación simple de construcción
        self.trabajo_necesario = trabajo_necesario
        self.trabajo_actual = 0
        self.construido = False

    @property
    def roi(self):
        # retorno por euro invertido (simple)
        return self.beneficio / self.coste if self.coste else 0

    def avanzar_construccion(self, unidades):
        if self.construido:
            return
        self.trabajo_actual += unidades
        if self.trabajo_actual >= self.trabajo_necesario:
            self.trabajo_actual = self.trabajo_necesario
            self.construido = True

    def __repr__(self):
        return f"{self.nombre}(coste={self.coste}, beneficio={self.beneficio}, roi={self.roi:.4f})"


class Trabajador:
    def __init__(self, nombre, posicion, velocidad=1):
        self.nombre = nombre
        self.posicion = posicion
        self.velocidad = velocidad

        self.objetivo = None      # Edificio
        self.ruta = None          # lista de (x,y)
        self.indice_ruta = 0

    def esta_ocioso(self):
        return self.objetivo is None

    def asignar_objetivo(self, edificio, ruta):
        self.objetivo = edificio
        self.ruta = ruta
        self.indice_ruta = 0

    def limpiar_tarea(self):
        self.objetivo = None
        self.ruta = None
        self.indice_ruta = 0

    def tick_movimiento(self):
        """Avanza velocidad celdas por tick. Devuelve True si llega al objetivo."""
        if self.ruta is None:
            return False

        pasos = self.velocidad
        while pasos > 0 and self.indice_ruta < len(self.ruta) - 1:
            self.indice_ruta += 1
            self.posicion = self.ruta[self.indice_ruta]
            pasos -= 1

        # llegó si está en el último nodo
        return self.indice_ruta == len(self.ruta) - 1


class Ciudad:
    def __init__(self, presupuesto):
        self.presupuesto = presupuesto
        self.proyectos = []     # edificios seleccionados (planificados)
        self.trabajadores = []

        # red eléctrica (resultado MST)
        self.red_aristas = []
        self.coste_red = 0.0

    def agregar_trabajador(self, trabajador):
        self.trabajadores.append(trabajador)

    def planificar(self, edificios):
        self.proyectos = list(edificios)

    def edificios_construidos(self):
        return [e for e in self.proyectos if e.construido]
