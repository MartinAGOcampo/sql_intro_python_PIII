#!/usr/bin/env python
'''
SQL Introducción [Python]
Ejercicios de práctica
---------------------------
Autor: Ing.Jesús Matías González
Version: 1.1

Descripcion:
Programa creado para poner a prueba los conocimientos
adquiridos durante la clase
'''

__author__ = "Ing.Jesús Matías González"
__email__ = "ingjesusmrgonzalez@gmail.com"
__version__ = "1.1"

import sqlite3

# https://extendsclass.com/sqlite-browser.html


def create_schema():

    # Conectarnos a la base de datos
    # En caso de que no exista el archivo se genera
    # como una base de datos vacia
    conn = sqlite3.connect('secundaria.db')

    # Crear el cursor para poder ejecutar las querys
    c = conn.cursor()

    # Ejecutar una query
    c.execute("""
                DROP TABLE IF EXISTS estudiante; 
            """)

    # Ejecutar una query
    c.execute("""
            CREATE TABLE estudiante(
                [identificador] INTEGER PRIMARY KEY AUTOINCREMENT,
                [nombre] TEXT NOT NULL,
                [edad] INTEGER NOT NULL,
                [grado] INTEGER,
                [tutor] TEXT
            );
            """)

    # Para salvar los cambios realizados en la DB debemos
    # ejecutar el commit, NO olvidarse de este paso!
    conn.commit()

    # Cerrar la conexión con la base de datos
    conn.close()


def fill(estudiantes):
    # print('Completemos esta tablita!')
    # Llenar la tabla de la secundaria con al menos 5 estudiantes
    # Cada estudiante tiene los posibles campos:
    # id --> este campo es auto incremental por lo que no deberá completarlo
    # name --> El nombre del estudiante (puede ser solo nombre sin apellido)
    # age --> cuantos años tiene el estudiante
    # grade --> en que año de la secundaria se encuentra (1-6)
    # tutor --> nombre de su tutor

    # Se debe utilizar la sentencia INSERT.
    # Observar que hay campos como "grade" y "tutor" que no son obligatorios
    # en el schema creado, puede obivar en algunos casos completar esos campos

    print('Comenzemos a rellenar la tabla')
    print()
    conn = sqlite3.connect('secundaria.db')
    c = conn.cursor()

    c.executemany("""
              INSERT INTO estudiante(nombre, edad, grado, tutor)
              VALUES(?, ?, ?, ?);
              """, estudiantes)

    print('Los valores fueron agregados exitosamente')
    conn.commit()
    conn.close()


def fetch():
    # print('Comprobemos su contenido, ¿qué hay en la tabla?')
    # Utilizar la sentencia SELECT para imprimir en pantalla
    # todas las filas con todas sus columnas
    # Utilizar fetchone para imprimir de una fila a la vez

    print('La tabla se encuentra con los siguientes datos: ')
    print()
    conn = sqlite3.connect('secundaria.db')
    c = conn.cursor()
    c.execute("""
            SELECT * FROM estudiante;
            """)
    rows = c.fetchone()
    while rows is not None:
        print(rows)
        rows = c.fetchone()
    
    conn.close()
    print('Fin de la tabla')
    print('------------------------')

def search_by_grade(grade):
    print('Operación búsqueda!')
    # Utilizar la sentencia SELECT para imprimir en pantalla
    # aquellos estudiantes que se encuentra en en año "grade"

    # De la lista de esos estudiantes el SELECT solo debe traer
    # las siguientes columnas por fila encontrada:
    # id / name / age
    conn = sqlite3.connect('secundaria.db')
    c = conn.cursor()
    print(f'Estudiantes que estan en el año {grade}')
    print()
    c.execute("""
            SELECT identificador, nombre, edad FROM estudiante
            WHERE grado = ?;
            """, (grade,))
    rows = c.fetchone()
    while rows is not None:
        print(rows)
        rows = c.fetchone()
    
    conn.close()
    print('Fin de la búsqueda')
    print('------------------------')
    

def insert(nombre, edad, grado, tutor):
    print('Nuevos ingresos!')
    # Utilizar la sentencia INSERT para ingresar nuevos estudiantes
    # a la secundaria
    print('Vamos a ingresar nuevos estudiantes :D')
    print('')
    
    conn = sqlite3.connect('secundaria.db')
    c = conn.cursor()
    nuevo_estudiante = (nombre, edad, grado, tutor)
    print(f'Los valores que vamos a ingresar son: {nuevo_estudiante}')
    c.execute("""
              INSERT INTO estudiante (nombre, edad, grado, tutor) VALUES (?, ?, ?, ?);
               """, (nombre, edad, grado, tutor))
    
    conn.commit()
    conn.close()
    print()
    print('Ingresando valores')
    print()

def modify(id, name):
    print('Modificando la tabla')
    # Utilizar la sentencia UPDATE para modificar aquella fila (estudiante)
    # cuyo id sea el "id" pasado como parámetro,
    # modificar su nombre por "name" pasado como parámetro

    conn = sqlite3.connect('secundaria.db')
    c = conn.cursor()
    
    actualizacion = c.execute("""
            UPDATE estudiante SET nombre =? 
                              WHERE identificador = ? """, (name, id))
    conn.commit()
    conn.close()
    print('Los valores fueron modificados exitosamente')
    print('------------------------')

if __name__ == '__main__':
    print("Bienvenidos a otra clase con Python")
    print('Primero creamos la base de datos con la tabla llamada estudiantes')
    print('Va contener los siguientes datos: nombre, edad, curso y tutor')
    create_schema()   # create and reset database (DB)

    print('Creada la tabla vamos a comenzar a insertar datos')
    print()

    estudiantes = [
        ("Simon Alvarez", 48, 3, "Tio"),
        ("Carlos Mejia", 21, 3, "Madre"),
        ("Oscar Palavecino", 19, 3, "Padre"),
        ("Patricia Arevalo", 45, 1, "Madre"),
        ("María González", 22, 1, "Padre")
        ]
    fill(estudiantes)

    fetch()

    grade =3
    search_by_grade(grade)

    new_student = ('Martin', 30, 2, "Padre")
    insert(*new_student)
    print(f'El ingreso fue exitoso, ahora los valores {new_student} son parte de la base de datos ')
    print('------------------------')
    print()

    print('Vamos a realizar un UPDATE que vos elijas mediante un ID que puede ser 1, 2, 3, 4, 5, 6')
    while True:
        try:
            id = int(input('Cual es el ID al que quieres reemplazar el nombre: '))
            if 1 <= id <= 6:
                break
            else:
                print('Por favor ingresa un numero entre los valores dados')
        except ValueError:
            print('Eso no es un numero valido, intenta de nuevo')
    name = input('Cual es el nombre que le quieres otorgar?: ')
    modify(id, name)
    
    print('Veamos como queda la tabla finalmente')
    fetch()

