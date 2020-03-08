from socket import *
import os, sys



def main():
    SERV_PORT = 5000
    HOST = '127.0.0.1'
    while True:
        cs = socket(AF_INET, SOCK_STREAM)
        print('[NOTE] Please connect socket with `pub` or `sub`')
        while True:
            try:
                cli_type, addr, room = input('>> ').split()
                if (':' in addr):
                    HOST = str(addr.split(':')[0])
                    try:
                        SERV_PORT = int(addr.split(':')[1])
                    except ValueError:
                        print('[ERROR] Port is invalid!')
                        continue
                else:
                    HOST = str(addr)
                break
            except ValueError:
                print('[ERROR] Invalid argument. Please Type `{pub/sub} {ip-broker} {topic-name}`')
                pass
        serv_sock_addr = (HOST, SERV_PORT)

        try:
            cs.connect(serv_sock_addr)
            cs.send(room.encode('utf-8'))
        except ConnectionRefusedError:
            print('[ERROR] Can\'t connect broker')
            # pass
            break
        except OSError:
            print('[ERROR] Can\'t connect broker2')
            break

        cs.setblocking(0)
        if cli_type == 'publish' or cli_type == 'pub':
            publish(cs,room)
        elif cli_type == 'subscribe' or cli_type == 'sub':
            subscribe(cs, room)
        print('')
    cs.close()

def publish(cs, room):
    msg = input('publisher>> ')
    cs.send(msg.encode('utf-8'))
    # if msg == 'quit':
    #     cs.close()

def subscribe(cs, room):
    print('Subscribe room %s...' %(room))
    while True:
        try:
            res = cs.recv(1024).decode('utf-8')
            port, msg = res.split(':')
            print('[%s] %s >> %s' %(port, room, msg))
        except BlockingIOError:
            pass
        except:
            print('[ERROR] Broker is shuting down!')
            break

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
