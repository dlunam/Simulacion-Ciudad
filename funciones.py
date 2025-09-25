import random

def generar_edificios(tipos):
    resultados = []
    for edificio in tipos:
        cantidad = random.randint(*edificio["cantidad_rango"])
        coste_unitario = random.randint(*edificio["coste_rango"])
        tiempo = random.randint(*edificio["tiempo_construccion_rango"])

        resultados.append({
            "nombre": edificio["nombre"],
            "cantidad": cantidad,
            "coste_unitario": coste_unitario,
            "coste_total": cantidad * coste_unitario,
            "tiempo_construccion": tiempo,
            "progreso": 0  # días completados
        })
    return resultados

def mostrar_trabajadores(trabajadores):
    print("Resumen de trabajadores:\n")
    for t in trabajadores:
        print(f"{t['nombre']}: {t['cantidad']} disponibles | "
              f"{t['horas_diarias']} horas/día | "
              f"Coste: ${t['coste']}/hora | "
              f"Productividad: {t['productividad']}")

def barra_progreso(porcentaje, longitud=30):
    """Genera una barra de progreso visual."""
    completado = int(longitud * porcentaje)
    restante = longitud - completado
    return "[" + "#" * completado + "-" * restante + f"] {porcentaje*100:.1f}%"

def simular_construccion(ciudad):
    """
    Simula la construcción día a día.
    Cada edificio avanza 1 día de progreso hasta llegar a su tiempo de construcción.
    """
    dia = 1
    terminado = False

    while not terminado:
        print(f"\n📅 Día {dia}")
        terminado = True  # asumimos que todo está terminado, salvo que veamos lo contrario

        for edificio in ciudad:
            if edificio["progreso"] < edificio["tiempo_construccion"]:
                edificio["progreso"] += 1
                terminado = False  # aún queda trabajo por hacer

            porcentaje = edificio["progreso"] / edificio["tiempo_construccion"]
            gasto_estimado = edificio["coste_total"] * porcentaje

            print(f"{edificio['nombre']} ({edificio['cantidad']} unidades):")
            print(f"  Progreso: {barra_progreso(porcentaje)}")
            print(f"  Gastado hasta ahora: ${int(gasto_estimado)} / {edificio['coste_total']}")
            print(f"  Tiempo transcurrido: {edificio['progreso']} / {edificio['tiempo_construccion']} días\n")

        dia += 1
        input("Presiona ENTER para avanzar al siguiente día...")
