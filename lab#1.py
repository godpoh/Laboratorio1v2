import random
from colorama import Fore, Style
import datetime

class Compra:
    def __init__(self, espectador, asientos_comprados, monto_total):
        self.cedula = espectador.cedula
        self.nombre = espectador.nombre
        self.genero = espectador.genero
        self.asientos_comprados = asientos_comprados
        self.monto_total = monto_total
        self.fecha_hora = datetime.datetime.now()

class Espectador:
    def __init__(self, cedula, nombre, genero):
        self.cedula = cedula
        self.nombre = nombre
        self.genero = genero

class Asiento:
    def __init__(self, nombre, precio):
        self.nombre = nombre
        self.precio = precio
        self.reservado = False  # Por defecto, el asiento no está reservado

class Menu:
    def __init__(self):
        self.opciones_principales = {
            '1': self.visualizar_estadio_y_precios,
            '2': self.registro_espectadores,
            '3': self.compra_entradas,
            '4': self.reporte_ventas,
            '5': self.salir
        }

        self.espectadores = []  # Lista para almacenar los espectadores registrados

        self.filas = 10
        self.columnas = 10
        self.matriz_asientos = self.generar_matriz_asientos()

        self.asientos_comprados = []

        self.compras_realizadas = []

    def generar_matriz_asientos(self):
        matriz = []
        reservados = 0  # Contador para llevar la cuenta de los asientos reservados
        for fila in range(self.filas, 0, -1):  # Comenzar desde filas (10) y decrementar hasta 1
            fila_asientos = []
            precio_fila = self.calcular_precio_fila(fila)
            for columna in range(self.columnas):
                nombre_asiento = f"{fila}{chr(65 + columna)}"
                asiento = Asiento(nombre_asiento, precio_fila)
                if not asiento.reservado and reservados < 15 and random.choice([True, False]):
                    asiento.reservado = True
                    reservados += 1
                fila_asientos.append(asiento)
            matriz.append(fila_asientos)
        return matriz

    def calcular_precio_fila(self, fila):
        if fila >= 8:
            return 15000
        elif 5 <= fila <= 7:
            return 10000
        else:
            return 5000
    
    def mostrar_precio_asiento(self, nombre_asiento):
        for fila in self.matriz_asientos:
            for asiento in fila:
                if asiento.nombre == nombre_asiento:
                    print("\n*******************************************************")
                    print(f"El precio del asiento {asiento.nombre} es ₡{asiento.precio}")
                    if (asiento.reservado):
                        print("⚠ ATENCIÓN: El asiento se encuentra RESERVADO y ya no puede ser comprado")
                    print("*******************************************************")
                    input("\nPresione Enter para visualizar el estadio nuevamente...")
                    self.visualizar_estadio_y_precios()
                    return
        print("\nNo se encontró un asiento con ese nombre.")
        print("Intente de nuevo.\n")
        self.visualizar_estadio_y_precios()

    def mostrar_menu_principal(self):
        print("\n---------------------------------------------------------------------")
        print("Bienvenido al Sistema de Gestión de Asientos para Partidos de Fútbol:")
        print("---------------------------------------------------------------------")
        print("1. Visualizar estadio y precio de los asientos")
        print("2. Registro de espectadores")
        print("3. Compra de entradas")
        print("4. Reporte de Ventas")
        print("5. Salir")

    def visualizar_estadio_y_precios(self):
        print("")
        print(" " * 33 + "Cancha")
        print("\n" * 2)
        for fila in self.matriz_asientos:
            for asiento in fila:
                if asiento.reservado:
                    print(Fore.RED + f"{asiento.nombre}" + Style.RESET_ALL, end="\t")
                else:
                    print(f"{asiento.nombre}", end="\t")
            print()  # Saltar a la siguiente fila al imprimir todos los asientos de una fila
        print("\n****************************************")
        print("Simbología: Coloreados en rojo = Reservado")
        print("******************************************\n")
        nombre_asiento = input("Ingrese el nombre del asiento seguido de un Enter para conocer su precio (o presione Enter para volver al menú principal): ")
        if nombre_asiento.lower() == "":
            return
        else:
            self.mostrar_precio_asiento(nombre_asiento)

    def registro_espectadores(self):
        print("\n")
        print("------------------------")
        print("Registro de espectadores")
        print("------------------------\n")
        while True:
            cedula_input = input("Ingrese la cédula del espectador (sin guiones, solo números), o presione Enter para volver al menú principal: ")
            if cedula_input == "":
                print("\nVolviendo al menú principal...\n")
                return
            try:
                cedula = int(cedula_input)
            except ValueError:
                print("Esta no es una cédula válida")
                continue
            nombre = input("Ingrese el nombre del espectador, o solo Enter para salir al menú principal: ")
            if nombre == "":
                print("\nVolviendo al menú principal...\n")
                return
            genero = input("Ingrese el género del espectador (M para Masculino, F para Femenino): ").upper()
            if genero not in ('M', 'F'):
                print("Género no válido. Solo puede ingresar M para Masculino o F para Femenino.")
                continue
            espectador = Espectador(cedula_input, nombre, genero)
            self.espectadores.append(espectador)
            print("\n¡Espectador registrado exitosamente!")
            input("\nPresione Enter para volver al menú principal...")
            break

    def compra_entradas(self):
        print("\n----------------")
        print("Comprar Entradas")
        print("----------------\n")
        cedula = input("Ingrese su cédula para verificar su registro: ")
        espectador = self.buscar_espectador(cedula)
        if espectador:
            if self.cantidad_asientos_de_compras_anteriores(cedula) < 3:
                while len(self.asientos_comprados) + self.cantidad_asientos_de_compras_anteriores(cedula) < 3:
                    self.visualizar_asientos()
                    nombre_asiento = input("\nIngrese el nombre del asiento que desea comprar (o escriba 'listo' para finalizar): ")
                    if nombre_asiento.lower() == 'listo':
                        break
                    elif self.validar_asiento(nombre_asiento):
                        self.comprar_asiento(nombre_asiento)
                    else:
                        print("\n⚠ ATENCIÓN: El asiento no está disponible o no existe. Por favor, intente de nuevo.")

                if len(self.asientos_comprados) > 0:
                    monto_total_asientos_comprados = 0
                    for asiento in self.asientos_comprados:
                        monto_total_asientos_comprados += asiento.precio
                    compra = Compra(espectador, self.asientos_comprados, monto_total_asientos_comprados)
                    self.compras_realizadas.append(compra)

                self.imprimir_asientos_comprados(cedula)
            else:
                print("Ya ha alcanzado el límite máximo de asientos permitidos por persona (3 asientos).")
        else:
            if cedula == '':
                print("\nCédula no válida.")
            else:
                print("\nEl espectador no está registrado.")
            input("\nPresione Enter para volver al menú principal...")

    def buscar_espectador(self, cedula):
        for espectador in self.espectadores:
            if espectador.cedula == cedula:
                return espectador
        return None
    
    def validar_asiento(self, nombre_asiento):
        for fila in self.matriz_asientos:
            for asiento in fila:
                if asiento.nombre == nombre_asiento and not asiento.reservado:
                    return True
        return False
    
    def comprar_asiento(self, nombre_asiento):
        for fila in self.matriz_asientos:
            for asiento in fila:
                if asiento.nombre == nombre_asiento:
                    self.asientos_comprados.append(asiento)
                    asiento.reservado = True
                    print(f"Asiento {asiento.nombre} comprado correctamente.")
    
    def cantidad_asientos_de_compras_anteriores(self, cedula):
        cantidad_entradas = 0
        for compra in self.compras_realizadas:
            if compra.cedula == cedula:
                cantidad_entradas += len(compra.asientos_comprados)
        return cantidad_entradas

    def visualizar_asientos(self):
        print("")
        print(" " * 33 + "Cancha")
        print("\n" * 2)
        for fila in self.matriz_asientos:
            for asiento in fila:
                if asiento in self.asientos_comprados:
                    print(Fore.BLUE + f"{asiento.nombre}" + Style.RESET_ALL, end="\t")
                elif asiento.reservado:
                    print(Fore.RED + f"{asiento.nombre}" + Style.RESET_ALL, end="\t")
                else:
                    print(f"{asiento.nombre}", end="\t")
            print()  # Saltar a la siguiente fila al imprimir todos los asientos de una fila

    def imprimir_asientos_comprados(self, cedula):
        self.visualizar_asientos()
        
        total = sum(asiento.precio for asiento in self.asientos_comprados)
        print("\n*************************************************")
        print("Asientos recién comprados se muestran en azul")
        print("Total de la compra: ₡", total)
        print("Cantidad asientos recién comprados: ", len(self.asientos_comprados))
        total_asientos_comprados = self.cantidad_asientos_de_compras_anteriores(cedula)
        print("Cantidad total de asientos comprados, incluyendo compras anteriores: ", total_asientos_comprados)
        print("¿Límite de asientos por persona alcanzado? (3 asientos): ", "Sí" if total_asientos_comprados == 3 else "No")
        print("\n*************************************************")
        self.asientos_comprados = [] # Reseteo asientos comprados para la próxima compra
        input("\nPresione Enter para volver al menú principal...")
    
    def reporte_ventas(self):
        print("\n------------------")
        print("Reporte de Ventas")
        print("------------------\n")
        print("******************************************")
        print("Cantidad de entradas compradas por género:")
        print("******************************************\n")
        cantidad_masculino = sum(len(compra.asientos_comprados) for compra in self.compras_realizadas if compra.genero == 'M')
        cantidad_femenino = sum(len(compra.asientos_comprados) for compra in self.compras_realizadas if compra.genero == 'F')
        print(f"Masculino: {cantidad_masculino}")
        print(f"Femenino: {cantidad_femenino}")

        print("\n************************")
        print("Detalles de cada compra:")
        print("************************")
        for compra in self.compras_realizadas:
            print("\n---------------------------------------")
            print(f"Fecha y Hora de la Compra: {compra.fecha_hora.strftime('%d/%m/%Y %H:%M:%S')}")
            print(f"Cédula: {compra.cedula}")
            print(f"Nombre: {compra.nombre}")
            print(f"Género: {compra.genero}")
            print("Asientos Comprados:", ", ".join(asiento.nombre for asiento in compra.asientos_comprados))
            print(f"Monto Total: ₡{compra.monto_total}")
        input("\nPresione Enter para volver al menú principal...")

    def volver_atras(self):
        print("\nVolviendo al menú principal.\n")
        self.mostrar_menu_principal()

    def salir(self):
        print("¡Hasta luego!")
        exit()

    def main(self):
        while True:
            self.mostrar_menu_principal()
            opcion = input("\nSeleccione una opción: ")
            accion = menu.opciones_principales.get(opcion)
            if accion:
                accion()
            else:
                print("\nError: Opción no válida. Por favor, seleccione una opción válida.\n")

# Inicio de ejecución del programa
menu = Menu()
menu.main()