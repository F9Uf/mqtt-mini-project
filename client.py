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
                userMsg = input('>> ').split()
                cli_type = userMsg[0]
                addr = userMsg[1]
                room = userMsg[2]
                
                if ('pub' in cli_type) and (len(userMsg) == 4):
                    msg = userMsg[3]

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
            except IndexError:
                print('[ERROR] Invalid argument. Please Type `{pub/sub} {ip-broker}:{port-broker}? {topic-name} {message}?`')
                pass
        serv_sock_addr = (HOST, SERV_PORT)

        try:
            cs.connect(serv_sock_addr)
        except ConnectionRefusedError:
            print('[ERROR] Can\'t connect broker')
            continue
        except OSError:
            print('[ERROR] Can\'t connect broker2')
            continue

        cs.setblocking(0)
        if cli_type == 'publish' or cli_type == 'pub':
            publish(cs, room, msg)
        elif cli_type == 'subscribe' or cli_type == 'sub':
            subscribe(cs, room)
        print('')
    cs.close()

def publish(cs, room, msg):
    reMsg = 'pub ' + str(room) + ' ' + str(msg)
    cs.send(reMsg.encode('utf-8'))
    print('publish>> %s' %(msg))

def subscribe(cs, room):
    reMsg = 'sub ' + str(room)
    cs.send(reMsg.encode('utf-8'))
    print('Subscribe room %s...' %(room))
    while True:
        try:
            res = cs.recv(1024).decode('utf-8')
            if len(res) > 0:
                port, msg = res.split(':')
                print('[%s] %s >> %s' %(port, room, msg))
                # print(res)
            else:
                print('[ERROR] Broker is shutting down!')
                break
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
