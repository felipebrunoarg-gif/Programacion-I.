
import json

alumnos = [
    { "nombre": "Juan", "notas": [7, 8, 9, 6], "asistencia": 90 },
    { "nombre": "Maria", "notas": [5, 6, 4, 7], "asistencia": 60 },
    { "nombre": "Pedro", "notas": [1, 9, 4, 7], "asistencia": 95 },
    { "nombre": "Ana", "notas": [6, 5, 7, 8], "asistencia": 85 }
]

def guardar_alumnos(alumnos):
    archivo = open("alumnos.json", "w", encoding="utf-8")
    json.dump(alumnos, archivo, indent=4, ensure_ascii=False)
    archivo.close()

def cargar_alumnos():
    try:
        archivo = open("alumnos.json", "r", encoding="utf-8")
        alumnos_cargados = json.load(archivo)
        archivo.close()
        return alumnos_cargados
    except FileNotFoundError:
        guardar_alumnos(alumnos)
        return alumnos

def calcular_promedio(notas):
    suma = sum(notas)
    cantidad = len(notas)
    promedio = suma / cantidad
    return promedio

def evaluar_regularidad(alumno):
    promedio_notas = calcular_promedio(alumno["notas"])
    asistencia = alumno["asistencia"]

    if asistencia >= 70 and promedio_notas >= 6:
        return True
    else:
        return False

alumnos = cargar_alumnos()

print("ESTADO DE REGULARIDAD DE LOS ALUMNOS")
for alumno in alumnos:
    es_regular = evaluar_regularidad(alumno)
    promedio = calcular_promedio(alumno["notas"])

    print(f"Alumno: {alumno['nombre']}")
    print(f"Promedio de notas: {promedio}")
    print(f"Asistencia: {alumno['asistencia']}%")

    if es_regular:
        print("Estado: ESTÁ REGULAR")
    else:
        print("Estado: NO ESTÁ REGULAR")

guardar_alumnos(alumnos)
