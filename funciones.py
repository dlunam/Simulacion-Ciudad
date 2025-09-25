import random
import time   #para el modo automático

def generar_edificios(tipos):
    resultados = []
    for edificio in tipos:
        cantidad = random.randint(*edificio["cantidad_rango"])
        coste_unitario = random.randint(*edificio["coste_rango"])
        tiempo = random.randint(*edificio["tiempo_construccion_rango"])

        # Cada edificio necesita "unidades de trabajo"
        trabajo_necesario = tiempo * 24

        resultados.append({
            "nombre": edificio["nombre"],
            "cantidad": cantidad,
            "coste_unitario": coste_unitario,
            "coste_total": cantidad * coste_unitario,
            "tiempo_construccion": tiempo,
            "trabajo_total": trabajo_necesario,
            "trabajo_realizado": 0,
            "terminado": False
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

def calcular_productividad_total(trabajadores):
    """Suma la productividad ponderada por la cantidad de trabajadores."""
    return sum(t["cantidad"] * t["productividad"] * t["horas_diarias"] for t in trabajadores)

def calcular_coste_trabajadores_dia(trabajadores):
    """Coste total en sueldos de un día de trabajo."""
    return sum(t["cantidad"] * t["coste"] * t["horas_diarias"] for t in trabajadores)

def simular_construccion(ciudad, trabajadores):
    productividad_diaria = calcular_productividad_total(trabajadores)
    coste_trabajadores_dia = calcular_coste_trabajadores_dia(trabajadores)

    # Preguntar al usuario el modo de simulación
    print("\nOpciones de simulación:")
    print("1. Manual (presionar ENTER para avanzar cada día)")
    print("2. Automática (el programa avanza solo)")
    modo = input("Elige el modo de simulación (1 o 2): ")

    espera = 0
    if modo == "2":
        try:
            espera = float(input("¿Cuántos segundos quieres esperar entre días? "))
        except ValueError:
            print("Valor no válido, se usará 1 segundo por defecto.")
            espera = 1.0

    dia = 1
    edificios_terminados = 0
    coste_total_trabajadores = 0

    print("\n🏗️ Iniciando la simulación de la construcción...\n")

    for edificio in ciudad:
        print(f"\n=== Construyendo {edificio['nombre']} ({edificio['cantidad']} unidades) ===\n")

        while not edificio["terminado"]:
            # Avance del día
            edificio["trabajo_realizado"] += productividad_diaria
            if edificio["trabajo_realizado"] >= edificio["trabajo_total"]:
                edificio["trabajo_realizado"] = edificio["trabajo_total"]
                edificio["terminado"] = True

            # Cálculos de progreso
            porcentaje = edificio["trabajo_realizado"] / edificio["trabajo_total"]
            gasto_edificio = int(edificio["coste_total"] * porcentaje)

            # Costes de trabajadores
            coste_total_trabajadores += coste_trabajadores_dia

            # Mostrar estado diario
            print(f"📅 Día {dia}")
            print(f"  {edificio['nombre']}:")
            print(f"  Progreso: {barra_progreso(porcentaje)}")
            print(f"  Gastado hasta ahora en este edificio: ${gasto_edificio} / {edificio['coste_total']}")
            print(f"  Trabajo realizado: {int(edificio['trabajo_realizado'])} / {edificio['trabajo_total']}")

            print("\n--- Estado General ---")
            print(f"  🏠 Edificios terminados: {edificios_terminados}")
            print(f"  💰 Coste acumulado trabajadores: ${coste_total_trabajadores}")
            print(f"  💵 Coste acumulado edificios: ${int(sum(e['coste_total'] * (e['trabajo_realizado']/e['trabajo_total']) for e in ciudad))}")
            print(f"  📊 Coste total acumulado: ${coste_total_trabajadores + int(sum(e['coste_total'] * (e['trabajo_realizado']/e['trabajo_total']) for e in ciudad))}\n")

            dia += 1

            #Dependiendo del modo elegido
            if modo == "1":
                input("Presiona ENTER para avanzar al siguiente día...")
            else:
                time.sleep(espera)

        edificios_terminados += 1
        print(f"✅ {edificio['nombre']} terminado en el día {dia-1}.\n")

    print("\n🎉 ¡Simulación terminada!")
    print(f"🏠 Total de edificios terminados: {edificios_terminados}")
    print(f"💵 Coste total en construcción: ${sum(e['coste_total'] for e in ciudad)}")
    print(f"💰 Coste total en trabajadores: ${coste_total_trabajadores}")
    print(f"📊 Coste final total: ${sum(e['coste_total'] for e in ciudad) + coste_total_trabajadores}")
