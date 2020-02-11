from socket import *


SERV_PORT = 5000

def main():
    cli_type, addr, room = input('>> ').split()
    serv_sock_addr = (addr, SERV_PORT)
    cs = socket(AF_INET, SOCK_STREAM)
    cs.connect(serv_sock_addr)

    cs.send(room.encode('utf-8'))
    print('Connected!')

    if cli_type == 'publish' or cli_type == 'pub':
        publish(cs,room)
    elif cli_type == 'subscribe' or cli_type == 'sub':
        subscribe(cs, room)

    cs.close()

def publish(cs, room):
    while True:
        msg = input('>> ')
        cs.send(msg.encode('utf-8'))
        if msg == 'quit':
            break
    cs.close()

def subscribe(cs, room):
    while True:
        msg = cs.recv(1024)
        print(room + '>> ' + msg.decode('utf-8'))
    cs.close()

if __name__ == "__main__":
    main()
