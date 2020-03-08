from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import os, sys, threading


rooms = dict()

def on_new_client(clientsocket, addr):
    room = ''
    while True:
        try:
            cliMsg = clientsocket.recv(1024).decode('utf-8').split() # recv command from client
            cliType = cliMsg[0]
            cliRoom = cliMsg[1]
            room = cliRoom
            _, port = addr
            
            # join room only subscribe
            if cliType == 'sub':
                if cliRoom not in rooms:
                    rooms[cliRoom] = []
                rooms[cliRoom].append(clientsocket)

            elif cliType == 'pub':
                msg = cliMsg[2]
                if len(msg) > 0:
                    print('[%d] %s >> %s' %(port, cliRoom, msg))
                    broadcast(msg, port, cliRoom) # broadcast message
                else:
                    break
        except BlockingIOError:
            pass
        except:
            break
    # remove subscriber out of room
    if room in rooms:
        if clientsocket in rooms[room]:
            rooms[room].remove(clientsocket)    
    clientsocket.close()

# broadcast to all client in the room
def broadcast(msg, port, room):
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
    
    # initial HOST and PORT
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
    
    s = socket(AF_INET, SOCK_STREAM) # create socket
    serv_sock_addr = (HOST, PORT) # create tuple 

    try:
        s.bind(serv_sock_addr) # bind HOST and PORT
        s.listen(0) # listen for connect socket with 0 queue
        s.setblocking(0) # set nonblocking
    except Exception as e:
        print('[ERROR]', e)
        quit()

    print('Broker is running on %s:%d...' % (str(HOST), PORT))

    while True:
        try:
            c, addr = s.accept() # accept new client connect

            try:
                Thread(target=on_new_client, args=(c, addr)).start() # create new thread
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
