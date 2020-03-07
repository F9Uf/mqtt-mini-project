from socket import *
import os, sys


SERV_PORT = 5000

def main():
    while True:
        cs = socket(AF_INET, SOCK_STREAM)
        while True:
            try:
                cli_type, addr, room = input('>> ').split()
                break
            except ValueError:
                print('[ERROR] Invalid argument. Please Type `{pub/sub} {ip-broker} {topic-name}`')
                pass
        serv_sock_addr = (addr, SERV_PORT)

        cs.connect(serv_sock_addr)
        cs.send(room.encode('utf-8'))
        print('Connected!')

        cs.setblocking(0)
        if cli_type == 'publish' or cli_type == 'pub':
            publish(cs,room)
        elif cli_type == 'subscribe' or cli_type == 'sub':
            subscribe(cs, room)
    cs.close()

def publish(cs, room):
    msg = input('>> ')
    cs.send(msg.encode('utf-8'))
    if msg == 'quit':
        cs.close()

def subscribe(cs, room):
    while True:
        try:
            res = cs.recv(1024).decode('utf-8')
            port, msg = res.split(':')
            print('[%s] %s >> %s' %(port, room, msg))
        except BlockingIOError:
            pass
    cs.close()

def quit():
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupt connection')
        quit()
