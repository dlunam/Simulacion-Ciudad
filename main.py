from modelos import Ciudad, Edificio, Trabajador
from mapa import Mapa
from simulacion import Simulador
import ui


def main():
    ui.titulo("SIMULADOR URBANO (ABM + OPTIMIZACIÓN)")

    # 1) Ciudad + catálogo
    ciudad = Ciudad(presupuesto=800_000)

    catalogo = [
        Edificio("Casa", 100_000, 60, (5, 5), trabajo_necesario=15),
        Edificio("Hospital", 300_000, 200, (15, 10), trabajo_necesario=35),
        Edificio("Fábrica", 250_000, 180, (10, 15), trabajo_necesario=30),
        Edificio("Escuela", 150_000, 90, (20, 5), trabajo_necesario=20),
    ]

    ui.seccion("Datos iniciales")
    ui.paso(f"Presupuesto: {ciudad.presupuesto} €")
    ui.paso("Catálogo (incluye ROI):")
    for e in catalogo:
        ui.paso(f"{e.nombre} | coste={e.coste} | beneficio={e.beneficio} | roi={e.roi:.4f}")

    # 2) Mapa con obstáculos
    mapa = Mapa(25, 25)
    for i in range(7, 18):
        mapa.agregar_obstaculo(i, 12)
    ui.seccion("Mapa")
    ui.resultado("Mapa generado con obstáculos centrales")

    # 3) Trabajadores (agentes)
    ciudad.agregar_trabajador(Trabajador("Obrero-1", (0, 0), velocidad=2))
    ciudad.agregar_trabajador(Trabajador("Obrero-2", (0, 1), velocidad=2))

    # 4) Simulador (motor)
    sim = Simulador(
        ciudad=ciudad,
        mapa=mapa,
        ui=ui,
        coste_cable_por_metro=50.0,
        unidad_presupuesto=1000
    )

    # A) Selección inteligente (ROI o beneficio)
    ui.seccion("Selección de inversiones (Knapsack)")
    seleccion = sim.seleccionar_inversiones(catalogo, objetivo="roi")  # prueba "beneficio"
    for e in seleccion:
        ui.resultado(f"Seleccionado: {e.nombre} (roi={e.roi:.4f})")

    # B+C) Simulación (agentes + A*), y al final MST
    sim.ejecutar(max_ticks=200)

    ui.titulo("FIN")


if __name__ == "__main__":
    main()
