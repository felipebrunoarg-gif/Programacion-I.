import json

codigos = [101, 102, 103, 104, 105, 106]
nombres = ["Café con leche", "Medialuna", "Sándwich de miga", "Agua mineral 500 ml", "Empanada", "Chipá (100 g)"]
precios = [1500, 700, 1800, 1000, 1200, 1300]

ventas = []
for i in range(6):
    ventas.append([0, 0, 0, 0, 0])

for i in range(6):
    print(str(codigos[i]) + " - " + nombres[i] + " - $" + str(precios[i]))

def leer_entero(mensaje, minimo, maximo):
    while True:
        try:
            numero = int(input(mensaje))
            if numero >= minimo and numero <= maximo:
                return numero
            print("Tiene que ser un número entre", minimo, "y", maximo)
        except ValueError:
            print("Eso no es un número válido.")

def buscar_producto(codigos, codigo):
    for i in range(len(codigos)):
        if codigos[i] == codigo:
            return i
    return -1

def total_producto(ventas, i):
    total = 0
    for d in range(5):
        total = total + ventas[i][d]
    return total

def recaudacion_dia(ventas, precios, d):
    total = 0
    for i in range(6):
        total += ventas[i][d] * precios[i]
    return total

def hay_ventas(ventas):
    for i in range(6):
        if total_producto(ventas, i) > 0:
            return True
    return False

def mostrar_menu():
    print("\n1. Cargar productos")
    print("2. Registrar venta")
    print("3. Ver informes")
    print("4. Salir")

def guardar_productos(codigos, nombres, precios):
    lista_productos = []
    for i in range(6):
        prod = {
            "codigo": codigos[i],
            "nombre": nombres[i],
            "precio": precios[i]
        }
        lista_productos.append(prod)
    
    archivo = open("productos.json", "w", encoding="utf-8")
    json.dump(lista_productos, archivo, indent=4, ensure_ascii=False)
    archivo.close()

def cargar_productos_archivo(codigos, nombres, precios):
    try:
        archivo = open("productos.json", "r", encoding="utf-8")
        lista_productos = json.load(archivo)
        archivo.close()
        
        for i in range(len(lista_productos)):
            if i < 6:
                codigos[i] = lista_productos[i]["codigo"]
                nombres[i] = lista_productos[i]["nombre"]
                precios[i] = lista_productos[i]["precio"]
    except FileNotFoundError:
        print("Primera vez que se usa el programa: se guarda el catálogo inicial.")
        guardar_productos(codigos, nombres, precios)

def cargar_ventas_archivo(ventas, codigos):
    try:
        archivo = open("ventas.json", "r", encoding="utf-8")
        datos_ventas = json.load(archivo)
        archivo.close()
        
        lista_ventas = datos_ventas.get("registro_ventas", [])
        for reg in lista_ventas:
            try:
                dia = int(reg["dia"])
                i = buscar_producto(codigos, int(reg["codigo"]))
                cantidad = int(reg["cantidad"])
                if i != -1 and dia >= 1 and dia <= 5 and cantidad > 0:
                    ventas[i][dia - 1] += cantidad
                else:
                    print("Se ignoró una venta con datos inválidos en ventas.json")
            except (ValueError, KeyError, IndexError):
                print("Se ignoró un registro mal escrito en ventas.json")
    except FileNotFoundError:
        print("Todavía no hay ventas guardadas.")

def guardar_venta(dia, codigo, cantidad, precio_unitario):
    monto_venta = cantidad * precio_unitario
    datos_ventas = {
        "recaudacion_por_dia": {
            "1": 0,
            "2": 0,
            "3": 0,
            "4": 0,
            "5": 0
        },
        "registro_ventas": []
    }
    
    try:
        archivo = open("ventas.json", "r", encoding="utf-8")
        datos_ventas = json.load(archivo)
        archivo.close()
    except FileNotFoundError:
        pass

    nueva_venta = {
        "dia": dia,
        "codigo": codigo,
        "cantidad": cantidad,
        "monto_total": monto_venta
    }
    datos_ventas["registro_ventas"].append(nueva_venta)

    clave_dia = str(dia)
    datos_ventas["recaudacion_por_dia"][clave_dia] += monto_venta

    archivo = open("ventas.json", "w", encoding="utf-8")
    json.dump(datos_ventas, archivo, indent=4, ensure_ascii=False)
    archivo.close()

def cargar_productos(codigos, nombres, precios, ventas):
    if hay_ventas(ventas):
        print("Ya hay ventas cargadas esta semana, no se puede cambiar el catálogo.")
    else:
        for i in range(6):
            print("\nProducto", i + 1)
            repetido = True
            while repetido:
                codigo = leer_entero("Código: ", 1, 999999)
                repetido = False
                for j in range(i):
                    if codigos[j] == codigo:
                        repetido = True
                        print("Ese código ya existe, ingresá otro.")
                        break
            codigos[i] = codigo
            nombres[i] = input("Nombre: ")
            precios[i] = leer_entero("Precio: ", 1, 1000000)
        guardar_productos(codigos, nombres, precios)
        print("Catálogo guardado.")

def registrar_venta(ventas, codigos, nombres, precios):
    dia = leer_entero("Día (1 = lunes ... 5 = viernes): ", 1, 5)
    codigo = leer_entero("Código del producto: ", 1, 999999)
    i = buscar_producto(codigos, codigo)
    if i == -1:
        print("No existe un producto con ese código.")
    else:
        cantidad = leer_entero("Cantidad: ", 1, 1000)
        ventas[i][dia - 1] += cantidad
        guardar_venta(dia, codigo, cantidad, precios[i])
        print("Venta registrada:", cantidad, "x", nombres[i])

def mostrar_informes(ventas, nombres, precios):
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    if not hay_ventas(ventas):
        print("Todavía no hay ventas cargadas, no hay informes para mostrar.")
    else:
        print("\nUnidades vendidas por producto")
        for i in range(6):
            print(nombres[i] + ": " + str(total_producto(ventas, i)))
        print("\nRecaudación por día")
        total_semana = 0
        for d in range(5):
            recaudado = recaudacion_dia(ventas, precios, d)
            total_semana += recaudado
            print(dias[d] + ": $" + str(recaudado))
        max_unidades = 0
        for i in range(6):
            if total_producto(ventas, i) > max_unidades:
                max_unidades = total_producto(ventas, i)
        print("\nProducto más vendido:")
        for i in range(6):
            if total_producto(ventas, i) == max_unidades:
                print(nombres[i], "(" + str(max_unidades) + " unidades)")
        max_recaudado = 0
        for d in range(5):
            if recaudacion_dia(ventas, precios, d) > max_recaudado:
                max_recaudado = recaudacion_dia(ventas, precios, d)
        print("\nDía de mayor recaudación:")
        for d in range(5):
            if recaudacion_dia(ventas, precios, d) == max_recaudado:
                print(dias[d], "($" + str(max_recaudado) + ")")
        print("\nProductos sin ventas:")
        ninguno = True
        for i in range(6):
            if total_producto(ventas, i) == 0:
                print(nombres[i])
                ninguno = False
        if ninguno:
            print("Todos los productos tuvieron ventas.")
        print("\nRecaudación total de la semana: $" + str(total_semana))

cargar_productos_archivo(codigos, nombres, precios)
cargar_ventas_archivo(ventas, codigos)

opcion = 0
while opcion != 4:
    mostrar_menu()
    opcion = leer_entero("Elegí una opción: ", 1, 4)
    if opcion == 1:
        cargar_productos(codigos, nombres, precios, ventas)
    elif opcion == 2:
        registrar_venta(ventas, codigos, nombres, precios)
    elif opcion == 3:
        mostrar_informes(ventas, nombres, precios)
    else:
        print("Datos guardados. ¡Hasta mañana!")