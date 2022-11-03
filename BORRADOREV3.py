# Evidencia
Evidencia 3 Lucero Perez
import pandas as pd
import openpyxl
import re
import sys
import sqlite3
from sqlite3 import Error
import datetime
import os

print(os.getcwd())

if not os.path.exists("BORRADOREV3.db"):
    print("No existen tablas")
    try:
        with sqlite3.connect("BORRADOREV3.db") as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("CREATE TABLE IF NOT EXISTS clientes(id INTEGER PRIMARY KEY, nombre_cliente TEXT NOT NULL);")
            mi_cursor.execute("CREATE TABLE IF NOT EXISTS salas(clave INTEGER PRIMARY KEY, nombre_sala TEXT NOT NULL, cupo INTEGER);")
            mi_cursor.execute("CREATE TABLE IF NOT EXISTS reservaciones(folio INTEGER PRIMARY KEY, numero_cliente INTEGER, sala INTEGER, fecha_reservacion timestamp, turno TEXT NOT NULL, nombre_del_evento TEXT NOT NULL, FOREIGN KEY (numero_cliente) REFERENCES clientes(id), FOREIGN KEY (sala) REFERENCES salas(clave));")
            print("Tablas creadas")
    except Error as e:
        print(e)
    except:
        print(f"Se produjo un error: {sys.exc_info()[0]}")
else:
    while True:
        print("""
        |--------------------------|
        |     Menú de opciones     |
        |--------------------------|
        |(1) Reservaciones         |
        |(2) Reportes              |
        |(3) Registrar una sala    |
        |(4) Registrar un cliente  |
        |(5) Salir                 |
        |--------------------------|\n""")
        opcion_menu_principal = input("Elige una opción del menú:  ")
        if opcion_menu_principal == "":
            print("Debe ingresar una opción del menú. \n")
            continue
        if opcion_menu_principal.isspace():
            print("Debe ingresar una opción del menú. \n")
            continue
        if not opcion_menu_principal in "12345":
            print("Debe ingresar una opción del menú. \n")
            continue
        if opcion_menu_principal == "1":
            while True:    
                print("""
                |----------------Menú de reservaciones---------------|
                |(1) Registrar nueva reservación                     |
                |(2) Modificar descripción de una reservación        |
                |(3) Consultar disponibilidad de salas para una fecha|
                |(4) Eliminar una reservación                        |
                |(5) Salir                                           |
                |----------------------------------------------------|""")
                opcion_menu_reservaciones = input("Elige una opción del menú:  ")
                if opcion_menu_reservaciones == "":
                    print("Debe ingresar una opción del menú. \n")
                    continue
                if opcion_menu_reservaciones.isspace():
                    print("Debe ingresar una opción del menú. \n")
                    continue
                if not opcion_menu_reservaciones in ("12345"):
                    print("Debe ingresar una opción del menú. \n")
                    continue
                if opcion_menu_reservaciones == "1":
                    while True:
                        try:
                            numero_cliente = int(input("Ingrese su ID Usuario:  "))
                        except:
                            print("Debe ingresar un número. \n")
                            continue
                        if numero_cliente == "":
                            print("Debe ingresar su ID Usuario. \n")
                            continue
                        try:
                            with sqlite3.connect("BORRADOREV3.db") as conn:
                                mi_cursor = conn.cursor()
                                mi_cursor.execute("SELECT * FROM clientes WHERE id=(?)", [numero_cliente])
                                folios = mi_cursor.fetchall()
                        except Error as e:
                            print(e)
                            break
                        if folios:
                            try:
                                with sqlite3.connect("BORRADOREV3.db") as conn:
                                    mi_cursor = conn.cursor()
                                    mi_cursor.execute("SELECT * FROM salas")
                                    salas = mi_cursor.fetchall()
                                    
                                    print("---------------------------------------")
                                    print("SALAS")
                                    print("---------------------------------------")
                                    print("ID SALA       NOMBRE DE SALA       CUPO")
                                    for numero_sala, nombre_sala, cupo in salas:
                                        print("---------------------------------------")
                                        print(numero_sala,"        ",nombre_sala,"        ",cupo,"      ")
                                        print("---------------------------------------")
                            except:
                                print("no")
                            while True:
                                try:
                                    sala = int(input("Seleccione un ID sala:  "))
                                except:
                                    print("Debe de ingresar un ID. \n")
                                    continue
                                if sala == "":
                                    print("Debe de seleccionar una sala. \n")
                                    continue
                                while True:
                                    try:
                                        fecha_reservacion = input("Ingrese la fecha deseada (dd/mm/aaa): \n")
                                        fecha_reservacion = datetime.datetime.strptime(fecha_reservacion,"%d/%m/%Y").date()
                                        break
                                    except:
                                        print("Debe ingresar una fecha. \n")
                                        continue 
                                if fecha_reservacion == "":
                                    print("Debe de ingresar una fecha. \n")
                                    continue
                                fecha_actual = (datetime.date.today())
                                limite_fecha = (fecha_reservacion - fecha_actual).days
                                if limite_fecha <=2:
                                    print("Debe de reservar con más de 2 días de anticipación. \n")
                                    continue
                                while True:
                                    print("""
                                    |-----Turnos-----|
                                    |(M) Matutino    |
                                    |(V) Vespertino  |
                                    |(N) Nocturno    |
                                    |----------------|""")
                                    turno = input("Ingrese un turno:  ").upper()
                                    if turno == "":
                                        print("Debe de ingresar un turno. \n")
                                        continue
                                    elif turno.isspace():
                                        print("Debe de ingresar un turno. \n")
                                        continue
                                    elif turno not in "MVN":
                                        print("Debe de ingresar una opción. \n")
                                        continue
                                    elif turno == "M":
                                        turno = "Matutino"
                                    elif turno == "V":
                                        turno = "Vespertino"
                                    elif turno == "N":
                                        turno = "Nocturno"
                                    try:
                                        with sqlite3.connect("BORRADOREV3.db") as conn:
                                            mi_cursor = conn.cursor()
                                            mi_cursor.execute("SELECT turno, fecha_reservacion FROM reservaciones WHERE fecha_reservacion=(?)", [fecha_reservacion])
                                            sala_reservada = mi_cursor.fetchall()
                                            fecha_resev = ""
                                            turno_resev = ""
                                            for turno,fecha in sala_reservada:
                                                if fecha_reservacion == sala_reservada[0][0] == str(sala_reservada[0][1]):
                                                    fecha_resev = str(sala_reservada[0][1])
                                                    turno_resev = sala_reservada[0][0]
                                            if fecha_reservacion == fecha_resev and turno == turno_resev:
                                                print("Ya existe una reservación en ese turno, favor de ingresar otro turno. \n")
                                                continue
                                    except Error as e:
                                            print(e)
                                            break
                                    while True:
                                        nombre_del_evento = input("Ingrese el nombre del evento:  ").title()
                                        if nombre_del_evento == "":
                                            print("Debe ingresar un nombre. \n")
                                            continue
                                        try:
                                            with sqlite3.connect("BORRADOREV3.db") as conn:
                                                mi_cursor = conn.cursor()
                                                valores = (numero_cliente, sala, fecha_reservacion, turno,  nombre_del_evento)
                                                mi_cursor.execute("INSERT INTO reservaciones(numero_cliente, sala, fecha_reservacion, turno,  nombre_del_evento) VALUES(?,?,?,?,?)", [numero_cliente, sala, fecha_reservacion, turno, nombre_del_evento])
                                                print("Registro agregado exitosamente")
                                                mi_cursor.execute("SELECT MAX(folio) FROM reservaciones;")
                                                id_reservacion = mi_cursor.fetchall()
                                                print("------------------------------------------------------------------------------------------------------")
                                                print("ID Reserva        Fecha reservación       Turno       ID Sala     ID Cliente      Nombre del evento")
                                                print("------------------------------------------------------------------------------------------------------")
                                                print(id_reservacion[0][0],"                  ",fecha_reservacion,"        ",turno,"       ",sala,"          ",numero_cliente,"         ",nombre_del_evento)
                                                print("------------------------------------------------------------------------------------------------------")
                                                break
                                        except Error as e:
                                            print(e)
                                            break
                                    break
                                break
                            break            
                        else:
                            print("No existe ningun ID con ese número")
                            continue
                if opcion_menu_reservaciones == "2":
                    while True:
                        try:
                            numero_reserva = int(input("Ingresa el ID Reserva:  "))
                        except:
                            print("Debe de ingresar un número. \n")
                            continue
                        if numero_reserva == "":
                            print("Debe de ingresar un número. \n")
                            continue
                        try:
                            with sqlite3.connect("BORRADOREV3.db") as conn:
                                mi_cursor = conn.cursor()
                                mi_cursor.execute("SELECT * FROM reservaciones WHERE folio=(?)", [numero_reserva])
                                identificador = mi_cursor.fetchall()
                                print("------------------------------------------------------------------------------------")
                                print("RESERVACION DEL ID: ", (numero_reserva))
                                print("------------------------------------------------------------------------------------")
                                print("ID RESERVA | ID CLIENTE | ID SALA | FECHA DE RESERVACION | TURNO | NOMBRE DEL EVENTO")
                                print("------------------------------------------------------------------------------------")
                                print(identificador[0][0],"              ",identificador[0][1],"        ",identificador[0][2],"        ",identificador[0][3],"       ",identificador[0][4],"   ",identificador[0][5],"     ")
                                print("------------------------------------------------------------------------------------")
                        except Error as e:
                            print(e)
                        while True:
                            if identificador:
                                nombre_nuevo = input("Ingrese el nuevo nombre del evento:  ").title()
                                if nombre_nuevo == "":
                                    print("Debe de ingresar un nombre. \n")
                                    continue
                                if (not re.match("^[a-zA-Z_ ]*$", nombre_nuevo)):
                                    print("Debe ingresar solamente letras. \n")
                                    continue
                                nombres =  nombre_nuevo, numero_reserva
                                try:
                                    with sqlite3.connect("BORRADOREV3.db") as conn:
                                        mi_cursor = conn.cursor()
                                        mi_cursor.execute("UPDATE reservaciones SET nombre_del_evento=(?) WHERE folio=(?);", (nombre_nuevo, numero_reserva))
                                        edicion = mi_cursor.fetchall()
                                        mi_cursor.execute("SELECT * FROM reservaciones WHERE folio=(?);", [numero_reserva])
                                        dat0s = mi_cursor.fetchall()
                                        print("Se ha editado el nombre del evento")
                                        print("------------------------------------------------------------------------------------")
                                        print("RESERVACION DEL ID: ", (numero_reserva))
                                        print("------------------------------------------------------------------------------------")
                                        print("ID RESERVA | ID CLIENTE | ID SALA | FECHA DE RESERVACION | TURNO | NOMBRE DEL EVENTO")
                                        print("------------------------------------------------------------------------------------")
                                        print(dat0s[0][0],"              ",dat0s[0][1],"        ",dat0s[0][2],"        ",dat0s[0][3],"       ",dat0s[0][4],"   ",dat0s[0][5],"     ")
                                        print("------------------------------------------------------------------------------------")
                                        break
                                except Exception as E:
                                    print(E)
                                    continue
                            else:
                                print("Debe de registrar una reservación. \n")
                        break
                if opcion_menu_reservaciones == "3":
                    while True:
                        try:
                            fecha_disponible = input("Ingrese la fecha que desea consultar (dd/mm/aaa): \n")
                            fecha_disponible = datetime.datetime.strptime(fecha_disponible,"%d/%m/%Y").date()
                            break
                        except:
                            print("Debe ingresar una fecha. \n")
                            continue 
                    if fecha_disponible == "":
                        print("Debe de ingresar una fecha. \n")
                        continue
                    try:
                        with sqlite3.connect("BORRADOREV3.db") as conn:
                            mi_cursor = conn.cursor()
                            mi_cursor.execute("SELECT clave FROM salas")
                            salas_existentes = mi_cursor.fetchall()
                            print(salas_existentes)
                            mi_cursor.execute("SELECT turno, sala FROM reservaciones WHERE fecha_reservacion=(?)", [fecha_disponible])
                            turnos_ocupados = mi_cursor.fetchall()
                            print(turnos_ocupados)
                            salass = []
                            if salas_existentes:
                                for clave in salas_existentes:
                                    salass.append(clave)
                                turnos_existentes = ["Matutino", "Vespertino", "Nocturno"]
                                turnos_posibles = []
                                for clave in salass:
                                    for turno in turnos_existentes:
                                        turnos_posibles.append(turno)
                                        print(turnos_posibles)
                                turnos_posibles = set(turnos_posibles)
                                turnos_ocupados = set(turnos_ocupados)
                                turnos_disponibles = turnos_posibles - turnos_ocupados
                                print(turnos_disponibles)
                            else:
                                print("No existe ninguna sala registrada con esa fecha. \n")
                    except Error as e:
                            print(e)
                            break
                if opcion_menu_reservaciones == "4":
                    while True:
                        try:
                            numero_reserva = int(input("Ingresa el ID Reserva:  "))
                        except:
                            print("Debe de ingresar un número. \n")
                            continue
                        if numero_reserva == "":
                            print("Debe de ingresar un número. \n")
                            continue
                        try:
                            with sqlite3.connect("BORRADOREV3.db") as conn:
                                mi_cursor = conn.cursor()
                                mi_cursor.execute("SELECT * FROM reservaciones WHERE folio=(?)", [numero_reserva])
                                numero = mi_cursor.fetchall()
                        except Error as e:
                            print(e)
                            break
                        if numero:
                            while True:
                                try:
                                    fecha_eliminada = input("Ingrese la fecha que desea eliminar (dd/mm/aaa): \n")
                                    fecha_eliminada = datetime.datetime.strptime(fecha_eliminada,"%d/%m/%Y").date()
                                    break
                                except:
                                    print("Debe ingresar una fecha. \n")
                                    continue 
                            if fecha_eliminada == "":
                                print("Debe de ingresar una fecha. \n")
                                continue
                            fecha_actual = (datetime.date.today())
                            limite_fecha = (fecha_eliminada - fecha_actual).days
                            if limite_fecha <=3:
                                print("Debe de eliminar la reservación, al menos con 3 días de anticipación. \n")
                                continue
                            else:
                                try:
                                    with sqlite3.connect("BORRADOREV3.db") as conn:
                                        mi_cursor = conn.cursor()
                                        mi_cursor.execute("SELECT * FROM reservaciones WHERE folio=(?);", [numero_reserva])
                                        reserva = mi_cursor.fetchall()
                                        print("------------------------------------------------------------------------------------")
                                        print("RESERVACION DEL ID: ", (numero_reserva))
                                        print("------------------------------------------------------------------------------------")
                                        print("ID RESERVA | ID CLIENTE | ID SALA | FECHA DE RESERVACION | TURNO | NOMBRE DEL EVENTO")
                                        print("------------------------------------------------------------------------------------")
                                        print(reserva[0][0],"              ",reserva[0][1],"        ",reserva[0][2],"        ",reserva[0][3],"       ",reserva[0][4],"   ",reserva[0][5],"     ")
                                        print("------------------------------------------------------------------------------------")
                                except Error as e:
                                    print(e)
                                    break
                                print("""\nEliminar reservacion:
                                        (1) SI
                                        (2) NO \n""")
                            
                                confirmacion = input("Esta seguro que desea eliminar un elemento?  ")
                                if confirmacion == "":
                                    print("Debe ingresar un número. \n")
                                    continue
                                if not confirmacion in ("12"):
                                    print("Debe de seleccionar una opción. \n")
                                    continue
                                if confirmacion == "1":
                                    try:
                                        with sqlite3.connect("BORRADOREV3.db") as conn:
                                            mi_cursor = conn.cursor()
                                            mi_cursor.execute("DELETE FROM reservaciones WHERE folio=(?)", [numero_reserva])
                                            print("Se ha eliminado la reservación. \n")
                                    except Error as e:
                                        print(e)
                                        break
                            if confirmacion == "2":
                                break
                            break
                        else:
                            print("No existe ninguna reserva para eliminar. \n")
                            break
                if opcion_menu_reservaciones == "5":
                                break
        if opcion_menu_principal == "2":
            while True:
                print("""
                |----------------Menú de reportes-----------------------|
                |(1) Reporte en pantalla de reservaciones para una fecha|
                |(2) Exportar reporte tabular en Excel                  |
                |(3) Salir                                              |
                |-------------------------------------------------------|""")
                opcion_menu_reportes = input("Elige una opción del menú:  ")
                if opcion_menu_reportes == "":
                    print("Debe ingresar una opción del menú. \n")
                    continue
                if opcion_menu_reportes.isspace():
                    print("Debe ingresar una opción del menú. \n")
                    continue
                if not opcion_menu_reportes in ("123"):
                    print("Debe ingresar una opción del menú. \n")
                    continue
                if opcion_menu_reportes == "1":
                    while True:
                        try:
                            fecha_consulta = input("Ingrese la fecha que desee consultar (dd/mm/aaa): \n")
                            fecha_consulta = datetime.datetime.strptime(fecha_consulta,"%d/%m/%Y").date()
                            break
                        except:
                            print("Debe ingresar una fecha. \n")
                            continue
                    if fecha_consulta == "":
                        print("Debe de ingresar una fecha. \n")
                        continue
                    try:
                        with sqlite3.connect("BORRADOREV3.db") as conn:
                            mi_cursor = conn.cursor()
                            mi_cursor.execute("SELECT * FROM reservaciones WHERE fecha_reservacion=(?)", [fecha_consulta])
                            fecha = mi_cursor.fetchall()
                    except Error as e:
                        print(e)
                        break
                    except:
                        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
                        break
                    finally:
                        conn.close()
                    if fecha:
                        try:
                            with sqlite3.connect("BORRADOREV3.db") as conn:
                                mi_cursor = conn.cursor()
                                mi_cursor.execute("SELECT sala, numero_cliente, nombre_del_evento, turno FROM reservaciones WHERE fecha_reservacion=(?)", [fecha_consulta])
                                memoria = mi_cursor.fetchall()
                                print("--------------------------------------------------------------------------------")
                                print("REPORTE DE RESERVACIONES PARA EL DIA: ", (str(fecha_consulta)))
                                print("--------------------------------------------------------------------------------")
                                print("ID SALA | ID CLIENTE | NOMBRE DEL EVENTO |  TURNO")
                                print("--------------------------------------------------------------------------------")
                                for sala, numero_cliente, nombre_del_evento, turno in memoria:
                                    print(sala,"\t\t",numero_cliente,"\t",nombre_del_evento,"\t",turno,"\t")
                                print("------------------------Fin del reporte-----------------------------------------")
                        except Error as e:
                            print(e)
                            break
                    else:
                        print("No existe ninguna fecha. \n")
                        break
                if opcion_menu_reportes == "2":
                    while True:
                        try:
                            fecha_consulta = input("Ingrese la fecha que desee exportar (dd/mm/aaa): \n")
                            fecha_consulta = datetime.datetime.strptime(fecha_consulta,"%d/%m/%Y").date()
                            break
                        except:
                            print("Debe ingresar una fecha. \n")
                            continue
                    if fecha_consulta == "":
                        print("Debe de ingresar una fecha. \n")
                        continue
                    try:
                        with sqlite3.connect("BORRADOREV3.db") as conn:
                            mi_cursor = conn.cursor()
                            mi_cursor.execute("SELECT * FROM reservaciones WHERE fecha_reservacion=(?)", [fecha_consulta])
                            fecha = mi_cursor.fetchall()
                    except Error as e:
                        print(e)
                        break
                    if fecha:
                        try:
                            with sqlite3.connect("BORRADOREV3.db") as conn:
                                mi_cursor = conn.cursor()
                                mi_cursor.execute("SELECT sala, numero_cliente, nombre_del_evento, turno FROM reservaciones WHERE fecha_reservacion=(?)", [fecha_consulta])
                                datos = mi_cursor.fetchall()
                                datos = pd.DataFrame(datos)
                                datos.to_excel('BORRADOREV3.xlsx', index= False)
                                print("Libro creado exitosamente")         
                        except Error as e:
                            print(e)
                            break
                if opcion_menu_reportes == "3":
                    break
        if opcion_menu_principal == "3":
            while True:
                nombre_sala = input("Ingrese el nombre de la sala:  ").title()
                if nombre_sala == "":
                    print("Debe ingresar solamente letras.")
                    continue
                if nombre_sala.isspace():
                    print("Debe ingresar solamente letras. \n")
                    continue
                while True:
                    try:
                        cupo = int(input("Ingrese el cupo de la sala:  "))
                    except:
                        print("Debe de ingresar un número. \n")
                        continue
                    if cupo == "":
                        print("Debe de ingresar un número. \n")
                        continue
                    try:
                        with sqlite3.connect("BORRADOREV3.db") as conn:
                            mi_cursor = conn.cursor()
                            valores = (nombre_sala, cupo)
                            mi_cursor.execute("INSERT INTO salas(nombre_sala, cupo) VALUES(?,?)", [nombre_sala, cupo])
                            print("Registro agregado exitosamente")
                            mi_cursor.execute("SELECT MAX(clave) FROM salas;")
                            id_sala = mi_cursor.fetchall()
                            print("-------------------------")
                            print(f"Tu ID Sala es: {id_sala[0][0]}")
                            print("-------------------------")
                    except Error as e:
                        print(e)
                        break
                break
        if opcion_menu_principal == "4":
            while True:
                nombre_cliente = input("Ingrese su nombre:  ").title()
                if nombre_cliente == "":
                    print("Debe ingresar solamente letras.")
                    continue
                elif nombre_cliente.isspace():
                    print("Debe ingresar solamente letras. \n")
                    continue
                elif (not re.match("^[a-zA-Z_ ]*$", nombre_cliente)):
                    print("Debe ingresar solamente letras. \n")
                    continue
                try:
                    with sqlite3.connect("BORRADOREV3.db") as conn:
                        mi_cursor = conn.cursor()
                        valores = (nombre_cliente)
                        mi_cursor.execute("INSERT INTO clientes(nombre_cliente) VALUES(?)", [nombre_cliente])
                        print("Registro agregado exitosamente")
                        mi_cursor.execute("SELECT MAX(id) FROM clientes;")
                        id_client3 = mi_cursor.fetchall()
                        print("-------------------------")
                        print(f"Tu ID Usuario es: {id_client3[0][0]}")
                        print("-------------------------")
                except Error as e:
                    print(e)
                    break

        if opcion_menu_principal == "5":
            break
