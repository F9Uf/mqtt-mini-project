from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import os, sys, threading


rooms = dict()

def on_new_client(clientsocket, addr, room):
    while True:
        try:
            msg = clientsocket.recv(1024).decode('utf-8')
            _, port = addr
            if len(msg) > 0:
                print('[%d] %s >> %s' %(port, room, msg))
                boardcast(msg, port, room)
            else:
                break
        except BlockingIOError:
            pass
        except:
            break
    rooms[room].remove(clientsocket)
    clientsocket.close()

def boardcast(msg, port, room):
    reMsg = str(port) + ':' + msg
    if room in rooms:
        for client in rooms[room]:
            client.send(reMsg.encode('utf-8'))
            # print(client)
    else:
        print('[ERROR] Not found room')

def closeClient():
    for room in rooms.keys():
        for client in rooms[room]:
            client.close()

def quit():
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

def main():
    HOST = '127.0.0.1'
    PORT = 5000
    
    if (len(sys.argv) == 2):
        if (':' in sys.argv[1]):
            HOST = str(sys.argv[1].split(':')[0])
            try:
                PORT = int(sys.argv[1].split(':')[1])
            except ValueError:
                print('[ERROR] Port is invalid!')
                quit()
        else:
            HOST = str(sys.argv[1])
    
    s = socket(AF_INET, SOCK_STREAM)
    serv_sock_addr = (HOST, PORT)

    try:
        s.bind(serv_sock_addr)
        s.listen(0)
        s.setblocking(0)
    except Exception as e:
        print('[ERROR]', e)
        quit()

    print('Broker is running on %s:%d...' % (str(HOST), PORT))

    while True:
        try:
            c, addr = s.accept()
            room = c.recv(1024).decode('utf-8')
            if room not in rooms:
                rooms[room] = [] # create new room
            rooms[room].append(c)

            try:
                Thread(target=on_new_client, args=(c, addr, room)).start()
            except:
                print('[ERROR] Cannot create the new Thread')
        except BlockingIOError:
            pass

if __name__ == '__main__' :
    try:
        main()
    except KeyboardInterrupt:
        print('Shut down broker...')
        closeClient()
        quit()
