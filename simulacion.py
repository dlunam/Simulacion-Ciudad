from algoritmos import knapsack, a_star, prim


class Simulador:
    """
    Motor ABM muy simple:
    - Selecciona inversiones con knapsack (valor = ROI o beneficio).
    - Asigna edificios a trabajadores.
    - Cada tick: trabajadores se mueven paso a paso con A* y construyen al llegar.
    - Al final (o cuando quieras), calcula la red eléctrica mínima (MST).
    """

    def __init__(self, ciudad, mapa, ui, coste_cable_por_metro=50.0, unidad_presupuesto=1000):
        self.ciudad = ciudad
        self.mapa = mapa
        self.ui = ui

        self.coste_cable_por_metro = coste_cable_por_metro
        self.unidad_presupuesto = unidad_presupuesto  # discretización para DP

        self.ticks = 0

    # ----------------------
    # A) Optimización financiera
    # ----------------------
    def seleccionar_inversiones(self, catalogo, objetivo="roi"):
        """
        objetivo:
          - "roi": maximiza ROI total (aprox) con knapsack
          - "beneficio": maximiza beneficio total con knapsack
        """
        cap = self.ciudad.presupuesto // self.unidad_presupuesto

        def coste_u(e):
            return e.coste // self.unidad_presupuesto

        if objetivo == "roi":
            # ROI es float → lo escalamos a int para DP
            def valor(e):
                return int(e.roi * 1_000_000)  # escala simple
        else:
            def valor(e):
                return int(e.beneficio)

        seleccion = knapsack(catalogo, cap, valor_fn=valor, coste_fn=coste_u)
        self.ciudad.planificar(seleccion)
        return seleccion

    # ----------------------
    # C) Logística (asignación + movimiento)
    # ----------------------
    def _edificios_pendientes(self):
        return [e for e in self.ciudad.proyectos if not e.construido]

    def asignar_tareas(self):
        pendientes = self._edificios_pendientes()
        if not pendientes:
            return

        for t in self.ciudad.trabajadores:
            if not t.esta_ocioso():
                continue

            # asignación simple: el primer edificio no construido
            objetivo = pendientes[0]

            ruta = a_star(self.mapa, t.posicion, objetivo.posicion)
            if ruta is None:
                # si no hay ruta, probamos con otro edificio
                for alt in pendientes[1:]:
                    ruta = a_star(self.mapa, t.posicion, alt.posicion)
                    if ruta is not None:
                        objetivo = alt
                        break

            if ruta is None:
                self.ui.paso(f"{t.nombre}: no encuentra ruta a ningún edificio pendiente.")
                continue

            t.asignar_objetivo(objetivo, ruta)
            self.ui.paso(f"{t.nombre}: objetivo asignado → {objetivo.nombre} (ruta {len(ruta)} pasos)")

    def tick(self):
        self.ticks += 1

        # si hay trabajadores libres, asignamos tareas
        self.asignar_tareas()

        # mover y construir
        for t in self.ciudad.trabajadores:
            if t.esta_ocioso():
                continue

            llego = t.tick_movimiento()
            if llego:
                # “trabaja” en el edificio
                t.objetivo.avanzar_construccion(unidades=5)
                self.ui.paso(
                    f"{t.nombre} trabaja en {t.objetivo.nombre} "
                    f"({t.objetivo.trabajo_actual}/{t.objetivo.trabajo_necesario})"
                )

                if t.objetivo.construido:
                    self.ui.resultado(f"✅ Construido: {t.objetivo.nombre}")
                    t.limpiar_tarea()

    def terminado(self):
        return len(self._edificios_pendientes()) == 0

    # ----------------------
    # B) Red eléctrica (MST)
    # ----------------------
    def calcular_red_electrica(self):
        construidos = self.ciudad.edificios_construidos()
        aristas = prim(construidos)

        coste_total_dist = sum(dist for _, _, dist in aristas)
        coste_total = coste_total_dist * self.coste_cable_por_metro

        self.ciudad.red_aristas = aristas
        self.ciudad.coste_red = coste_total
        return aristas, coste_total

    # ----------------------
    # Ejecución
    # ----------------------
    def ejecutar(self, max_ticks=200):
        self.ui.seccion("Simulación por ticks (agentes + logística + construcción)")

        while not self.terminado() and self.ticks < max_ticks:
            self.ui.paso(f"--- Tick {self.ticks + 1} ---")
            self.tick()

        if self.terminado():
            self.ui.resultado(f"Simulación terminada en {self.ticks} ticks.")
        else:
            self.ui.paso(f"Se alcanzó el límite de ticks ({max_ticks}).")

        self.ui.seccion("Cálculo de red eléctrica mínima (MST)")
        aristas, coste = self.calcular_red_electrica()
        for a, b, dist in aristas:
            self.ui.resultado(f"{a.nombre} ↔ {b.nombre} | Dist: {dist:.2f} | Coste: {dist * self.coste_cable_por_metro:.2f} €")
        self.ui.resultado(f"Coste total red: {coste:.2f} €")
