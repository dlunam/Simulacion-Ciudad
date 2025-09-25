import funciones as func

tipos_de_edificios = [
    {
        "nombre": "Casa",
        "cantidad_rango": (5, 15),
        "coste_rango": (10000, 50000),
        "tiempo_construccion_rango": (5, 15)
    },
    {
        "nombre": "Edificio de oficinas",
        "cantidad_rango": (2, 10),
        "coste_rango": (100000, 500000),
        "tiempo_construccion_rango": (30, 90)
    },
    {
        "nombre": "Fábrica",
        "cantidad_rango": (1, 5),
        "coste_rango": (200000, 1000000),
        "tiempo_construccion_rango": (45, 120)
    },
    {
        "nombre": "Hospital",
        "cantidad_rango": (1, 3),
        "coste_rango": (500000, 2000000),
        "tiempo_construccion_rango": (60, 150)
    },
    {
        "nombre": "Escuela",
        "cantidad_rango": (2, 7),
        "coste_rango": (150000, 700000),
        "tiempo_construccion_rango": (40, 100)
    },
    {
        "nombre": "Centro comercial",
        "cantidad_rango": (1, 3),
        "coste_rango": (300000, 1500000),
        "tiempo_construccion_rango": (50, 130)
    },
    {
        "nombre": "Parque",
        "cantidad_rango": (2, 8),
        "coste_rango": (5000, 30000),
        "tiempo_construccion_rango": (3, 10)
    }
]

tipos_de_trabajadores = [
    {
        "nombre": "Currito",
        "cantidad": 10,
        "horas_diarias": 8,
        "coste": 50,  
        "productividad": 0.5  
    },
    {
        "nombre": "Manita",
        "cantidad": 5,
        "horas_diarias": 6,
        "coste": 80,
        "productividad": 1.0
    },
    {
        "nombre": "Maquinista",
        "cantidad": 3,
        "horas_diarias": 4,
        "coste": 120,
        "productividad": 2.0
    }
]



ciudad = func.generar_edificios(tipos_de_edificios)

print("Resultados de la simulación de la ciudad:\n")
for edificio in ciudad:
    print(f"{edificio['nombre']}: {edificio['cantidad']} unidades | "
          f"Coste: {edificio['coste']} | "
          f"Tiempo de construcción: {edificio['tiempo_construccion']} días")
