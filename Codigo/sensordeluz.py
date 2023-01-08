#!/usr/bin/python3
# UNSA MCC

import serial   #importa libreria serial    
import time     #importa time para hacer delays
import datetime #importa libreria dia de hoy fechas
import pymysql  #importa libreria base de datos en mysql
from pymysql import cursors #importa cursors de la libreria pymysql para hacer crud en una base de datos
import os
import sys

#server = '127.0.0.1' #datos de conexion locales
#user = 'toor'
#password = 'toor'
#ddbb='daq'
#charset = 'utf8mb4'

server = '128.199.6.248' #iot database
user = 'newuser'
password = 'you_password_here'
ddbb='unsa'
charset = 'utf8mb4'

try:  #intenta conectarte y haz
    conexion = pymysql.connect(host=server, user=user, password=password, db=ddbb, charset=charset, cursorclass=pymysql.cursors.DictCursor)
    #conectarte a 127.0.0.1 usuario toor password toor base de datos daq chars utf8 con cursor
    print("Conexión correcta")
except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:  #si no logra el try haz esto
    print("Ocurrió un error al conectar: ", e) #e es el tipo de error de mysql


dispositivo = serial.Serial('COM4',9600)
dispositivo.flushInput()
#dispositivo.flushOutput()

time.sleep(1) # retardo estabiliza puerto osea delay

estado = 1

    
while estado==1:
    
    try:
        conexion = pymysql.connect(host=server, user=user, password=password, db=ddbb, charset=charset, cursorclass=pymysql.cursors.DictCursor)
        estado = True
        print("Conexión correcta 2")
        #time.sleep(2)
        luz = dispositivo.readline().decode('utf-8').rstrip() #lee la respuesta y guarda en 'luz'
        fecha = datetime.datetime.now()
        fecha = fecha.strftime("%Y/%m/%d %H:%M:%S")
        fecha = str(fecha) #'fecha' es fecha actual de datetime
        luz = int(luz)
        print (luz)

        #time.sleep(1)
        try:
            with conexion.cursor() as cursor: #metodo de escritura
                # Crear un record
                sql = "INSERT INTO `datos` (`fecha`,`luz`) VALUES (%s, %s)" #consulta SQL
                cursor.execute(sql, (fecha, luz)) #inserta variables en la consulta SQL
                conexion.commit() ##si no se hace commit no se guarda datos
                print ('Exito commit, esperando 10 segundos')
                dispositivo.flushInput()
                #☺dispositivo.flushOutput()
                time.sleep(0.1)
                

            #with conexion.cursor() as cursor: #metodo de lectura
                ## Lectura de un record
                #sql = "SELECT `luz` FROM `datos` WHERE `id`=%s"
                #cursor.execute(sql, ('30')) #id es 30 y lee luz
                #result = cursor.fetchone()
                #print(result)
        finally:
            conexion.close() #cerrar coneccion
            cursor.close()
            print('Conexion y cursor cerrados')
            time.sleep(10)
        
    except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
        print("Ocurrió un error al conectar: ", e)
        estado= False
        break
        

    
        






    
