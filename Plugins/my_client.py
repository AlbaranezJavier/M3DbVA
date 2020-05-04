'''
Complemento o plugin para establecer conexión e intercambiar mensajes de texto entre dos plataformas. Produciéndose
esta comunicación en la misma máquina.
'''
import socket

def bind2server(PORT=12345):
    '''
    Establece una conexión con el servidor, el cual, está escuchando en el puerto 12345 de esta máquina.
    '''
    HOST = socket.gethostname()
    HOST = socket.gethostbyname(HOST)
    print(f'IP: {HOST}, Port: {PORT}')

    # Create a socket (SOCK_STREAM means a TCP socket)
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.connect((HOST, PORT))
    return mySocket

def send_msg(mySocket, data):
    mySocket.sendall((data + "\n").encode())

def receive_msg(mySocket):
    return mySocket.recv(1024)

def print_msg(data, received):
    print("Sent:     {}".format(data))
    print("Received: {}".format(received))

'''
from my_client import bind2server, send_msg, receive_msg, print_msg

# Script, prueba de comunicación.
if __name__ == '__main__':
    print("Ejecutando prueba de client")
    mySocket = bind2server()
    try:
        data = "hola"
        send_msg(mySocket, data)
        serverMsg = receive_msg(mySocket)
        print_msg(data, serverMsg)

        data = "adios"
        send_msg(mySocket, data)
        serverMsg = receive_msg(mySocket)
        print_msg(data, serverMsg)
    finally:
        mySocket.close()
'''