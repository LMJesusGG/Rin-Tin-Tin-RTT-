import socket
import network
import utime
from machine import Pin, PWM


serverAddressPort = socket.getaddrinfo('0.0.0.0', 3000)[0][-1]
bufferSize = 128

Barril=Pin(13, Pin.OUT)

Motor1=Pin(21, Pin.OUT)
SentidoA1=Pin(22, Pin.OUT)
SentidoB1=Pin(23, Pin.OUT)

Motor2=Pin(4, Pin.OUT)
SentidoA2=Pin(2, Pin.OUT)
SentidoB2=Pin(15, Pin.OUT)

def connect_wifi(ssid, password):
    wf = network.WLAN(network.STA_IF)
    wf.active(True)
    wf.connect(ssid, password)
    while not wf.isconnected():
        print(".")
        utime.sleep(1)
    print("Connected to Wi-Fi:", wf.ifconfig())

connect_wifi("Malcom's A25", "TARDIS10")

def exec(data):
    print(data)
    commands = {
        b'U1': "Arriba",
        b'U0': "Arriba no",
        b'D1': "Abajo",
        b'D0': "Abajo no",
        b'L1': "Izquierda",
        b'L0': "Izquierda no",
        b'R1': "Derecha",
        b'R0': "Derecha no",
        b'K1': "Barril ac",
        b'K0': "Barril desac",
    }
    print(commands.get(data, "Otra opcion"))
    if commands.get(data)=="Barril ac":
       print("Atacando")
       Barril.value(1)
    elif commands.get(data)=="Barril desac":
       Barril.value(0)
       print("Ataque parado")
    elif commands.get(data)=="Arriba":
       Motor1.value(1)
       SentidoA1.value(1)
       SentidoB1.value(0)
       Motor2.value(1)
       SentidoA2.value(1)
       SentidoB2.value(0)
       print("Avanzando")
    elif commands.get(data)=="Arriba no":
       Motor1.value(0)
       SentidoA1.value(0)
       SentidoB1.value(0)
       Motor2.value(0)
       SentidoA2.value(0)
       SentidoB2.value(0)
       print("Parando")
    elif commands.get(data)=="Abajo":
       Motor1.value(1)
       SentidoA1.value(0)
       SentidoB1.value(1)
       Motor2.value(1)
       SentidoA2.value(0)
       SentidoB2.value(1)
       print("Retrocediendo")
    elif commands.get(data)=="Abajo no":
       Motor1.value(0)
       SentidoA1.value(0)
       SentidoB1.value(0)
       Motor2.value(0)
       SentidoA2.value(0)
       SentidoB2.value(0)
       print("Parando")
    elif commands.get(data)=="Izquierda":
       Motor1.value(1)
       SentidoA1.value(0)
       SentidoB1.value(1)
       Motor2.value(1)
       SentidoA2.value(1)
       SentidoB2.value(0)
       print("Izquierda")
    elif commands.get(data)=="Izquierda no":
       Motor1.value(0)
       SentidoA1.value(0)
       SentidoB1.value(0)
       Motor2.value(0)
       SentidoA2.value(0)
       SentidoB2.value(0)
       print("Parando")
    elif commands.get(data)=="Derecha":
       Motor1.value(1)
       SentidoA1.value(1)
       SentidoB1.value(0)
       Motor2.value(1)
       SentidoA2.value(0)
       SentidoB2.value(1)
       print("Derecha")
    elif commands.get(data)=="Derecha no":
       Motor1.value(0)
       SentidoA1.value(0)
       SentidoB1.value(0)
       Motor2.value(0)
       SentidoA2.value(0)
       SentidoB2.value(0)
       print("Parando")

def start_server():
    sk = socket.socket()
    sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow address reuse
    sk.bind(serverAddressPort)
    sk.listen(1)
    return sk

while True:
    try:
        sk = start_server()
        print("Recibiendo de:", serverAddressPort)

        while True:
            try:
                conn, addr = sk.accept()
                print("Conexión desde:", addr)
                while True:
                    data = conn.recv(bufferSize)
                    if data:
                        exec(data)
                        conn.sendall(b"ok")
                    else:
                        print("Data no recibida, terminando conexión")
                        break
            except OSError as e:
                print("Error de conexión", e)
            finally:
                conn.close()
                print("Conexión terminada.")

    except OSError as e:
        print("Error de servidor:", e)
        utime.sleep(1)  

