from socket import *
from threading import Thread
import os, sys, threading


rooms = dict()

def on_new_client(clientsocket, addr, room):
    while True:
        try:
            msg = clientsocket.recv(1024).decode('utf-8')
            _, port = addr
            if msg != 'quit':
                print(str(port) + ' -> ' + room + ' >> ' + str(msg))
                boardcast(msg, room)
            else:
                print(str(port) + ' disconnected!')
                break
        except BlockingIOError:
            pass
        except:
            print('disconnect')
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
    HOST = '127.0.0.1'
    PORT = 5000
    s = socket(AF_INET, SOCK_STREAM)
    serv_sock_addr = (HOST, PORT)
    s.bind(serv_sock_addr)
    s.listen(0)
    s.setblocking(0)
    print('Broker is running on ' + str(HOST) + ':' + str(PORT))


    while True:
        try:
            c, addr = s.accept()
            room = c.recv(1024).decode('utf-8')
            print(room)
            if room not in rooms:
                rooms[room] = []
            rooms[room].append(c)

            try:
                Thread(target=on_new_client, args=(c, addr, room)).start()
            except:
                print('errrrrrrr')
        except BlockingIOError:
            pass

if __name__ == '__main__' :
    try:
        main()

    except KeyboardInterrupt:
        print('Shut down server...')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
