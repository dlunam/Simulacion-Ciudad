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


def obtener_constructores():
    return [
        {
            "nombre": "Currito",
            "horas_dia": 14,
            "costo_hora": 100,
            "reduccion_por_hora": 1,
            "rango_cantidad": range(0, 6)
        },
        {
            "nombre": "Manitas",
            "horas_dia": 8,
            "costo_hora": 275,
            "reduccion_por_hora": 2.5,
            "rango_cantidad": range(0, 4)
        },
        {
            "nombre": "Maquinista",
            "horas_dia": 5.5,
            "costo_hora": 400,
            "reduccion_por_hora": 5,
            "rango_cantidad": range(0, 4)
        }
    ]

