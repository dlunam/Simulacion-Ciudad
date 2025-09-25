import random

def generar_edificios(tipos):
    resultados = []
    for edificio in tipos:
        cantidad = random.randint(*edificio["cantidad_rango"])
        coste = random.randint(*edificio["coste_rango"])
        tiempo = random.randint(*edificio["tiempo_construccion_rango"])
    
        resultados.append({
            "nombre": edificio["nombre"],
            "cantidad": cantidad,
            "coste": coste,
            "tiempo_construccion": tiempo
        })
    return resultados

def mostrar_trabajadores(trabajadores):
    print("Resumen de trabajadores:\n")
    for t in trabajadores:
        print(f"{t['nombre']}: {t['cantidad']} disponibles | "
              f"{t['horas_diarias']} horas/día | "
              f"Coste: ${t['coste']}/hora | "
              f"Productividad: {t['productividad']}")