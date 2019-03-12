''' Mehdi Hajikhani
    Panther Id NO. 5594946'''

import sys
import socket
import threading
import time

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = '127.0.0.1'
port = 10000

s.connect((host,port))
def receiveThread():
    while True:
        try:
            data = s.recv(1024)
            if data:
                print(data.decode(),end='')
        except socket.error as msg:
            print('Communication error, plz restart client %s' %msg)
            break
        except Exception as e:
            print(e)
            break
    print('')
threading._start_new_thread(receiveThread,())
def sendMessage(msg):
    try:
        print(msg)
        s.send(msg.encode())
    except Exception as e:
        print(e)
        #print('exception')
        return

while True:
    option = input("\nPlease enter your query :  ")
    if option == 'quit':
        sys.exit()
    else:
        sendMessage(option)
        time.sleep(3)