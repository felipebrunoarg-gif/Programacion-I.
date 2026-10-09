import json

def cargar_jugadores():
    jugadores = []
    cantidad = int(input("¿Cuántos jugadores van a participar en el torneo? "))
    for i in range(cantidad):
        nombre = input(f"Ingrese el nombre del jugador {i + 1}: ")
        categoria = input(f"Ingrese la categoría del jugador {i + 1} (por ejemplo, 4ª, 5ª o 6ª): ")
        jugadores.append({"nombre": nombre, "categoria": categoria})
    return jugadores

def armar_parejas(jugadores):
    parejas = []
    cantidad_parejas = len(jugadores) // 2
    for i in range(cantidad_parejas):
        nombre_pareja = input(f"Ingrese el nombre de la pareja {i + 1}: ")
        print("Seleccione los jugadores para esta pareja:")
        for j, jugador in enumerate(jugadores):
            print(f"{j + 1}. {jugador['nombre']} ({jugador['categoria']})")
        indices = input("Ingrese los números de los dos jugadores separados por un espacio: ").split()
        jugador1 = jugadores[int(indices[0]) - 1]
        jugador2 = jugadores[int(indices[1]) - 1]
        parejas.append({"nombre": nombre_pareja, "jugadores": [jugador1, jugador2]})
    return parejas

def guardar_jugadores(jugadores):
    archivo = open("jugadores.json", "w", encoding="utf-8")
    json.dump(jugadores, archivo, indent=4, ensure_ascii=False)
    archivo.close()

def guardar_parejas(parejas):
    archivo = open("parejas.json", "w", encoding="utf-8")
    json.dump(parejas, archivo, indent=4, ensure_ascii=False)
    archivo.close()

def main():
    jugadores = cargar_jugadores()
    parejas = armar_parejas(jugadores)

    print("\nParejas formadas:")
    for pareja in parejas:
        print(f"Pareja: {pareja['nombre']}")
        for jugador in pareja["jugadores"]:
            print(f"  Jugador: {jugador['nombre']} ({jugador['categoria']})")

    guardar_jugadores(jugadores)
    guardar_parejas(parejas)
    print("\nLos jugadores se guardaron en jugadores.json")
    print("Las parejas se guardaron en parejas.json")

if __name__ == "__main__":
    main()