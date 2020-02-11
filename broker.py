from _thread import *
from socket import *
import os, sys

HOST = '192.168.1.36'
PORT = 5000

rooms = {}

def on_new_client(clientsocket, addr, room):
    while True:
        msg = clientsocket.recv(1024).decode('utf-8')
        _, port = addr
        if msg != 'quit':
            print(str(port) + ' -> ' + room + ' >> ' + str(msg))
            boardcast(msg, room)
        else:
            print(str(port) + ' disconnected!')
            break
    rooms[room].remove(clientsocket)
    clientsocket.close()

def boardcast(msg, room):
    if room in rooms:
        for client in rooms[room]:
            client.send(msg.encode('utf-8'))
    else:
        print('Error not found room')


def main():
    serv_sock_addr = (HOST, PORT)
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(serv_sock_addr)
    s.listen()
    print('Broker is running on ' + str(HOST) + ':' + str(PORT))

    while True:
        c, addr = s.accept()
        room = c.recv(1024).decode('utf-8')
        if room not in rooms:
            rooms[room] = []
        rooms[room].append(c)

        start_new_thread(on_new_client, (c, addr, room))

    s.close()

if __name__ == '__main__' :
    try:
        main()
    except KeyboardInterrupt:
        print('Shut down server...')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
