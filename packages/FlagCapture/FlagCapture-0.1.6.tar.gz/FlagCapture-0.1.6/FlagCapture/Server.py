import socket
from threading import Thread as T
import random
from itertools import cycle

teams = cycle(['lynx', 'wolf'])

posiible_x_positions = [87, 69, 53, 37, 22, 5]

Ip = '127.0.0.1'
Port = 4544

ADDR = (Ip, Port)

Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
Server.bind(ADDR)

everything = {}

def handle_client(conn, addr):
    global redFlagPos, blueFlagPos
    password = conn.recv(52000).decode('utf-8')
    if password != 'Capture the red-and-blue special flags that are available for capture.':
        conn.close()
        print('Hacker alert')
        return
    team = next(teams)
    x = random.choice(posiible_x_positions)
    z = -3 if team == 'wolf' else 3
    dir = 4.754 if team == 'wolf' else 1.654
    conn.send(str({'Everything': everything,  'RedFlagPos': redFlagPos, 'BlueFlagPos': blueFlagPos, 'MyInfo': {'team': team, 'x': x, 'z': z, 'dir': dir, 'id': str(addr)}}).encode('utf-8'))
    everything[str(addr)] = {'pos': [x, 0, z], 'dir': dir, 'team': team, 'touching': False, 'carrying': None}
    notify()
    notifing_list.append(conn)

    while True:
        try:
            message = eval(conn.recv(58000).decode('utf-8'))
            if message[0] == 'Updating pos':
                everything[str(addr)]['pos'] = message[1]['pos']
            if message[0] == 'Updating dir':
                everything[str(addr)]['dir'] = message[1]['dir']
            if message[0] == 'Updating touching':
                everything[str(addr)]['touching'] = message[1]['touching']
            if message[0] == 'Updating carrying':
                everything[str(addr)]['carrying'] = message[1]['carrying']
            if message[0] == 'drop':
                everything[str(addr)]['carrying'] = None
                if message[1]['flag'] == 'red':
                    redFlagPos = everything[str(addr)]['pos']
                if message[1]['flag'] == 'blue':
                    blueFlagPos = everything[str(addr)]['pos']
            notify()
        except Exception:
            print('Some one disconnected')
            notifing_list.remove(conn)
            del everything[str(addr)]
            return

def notify():
    for connection in notifing_list:
        connection.send(str(everything).encode('utf-8'))

redFlagPos = random.choice([[4, 0, 58], [88, 0, 58]])
blueFlagPos = random.choice([[4, 0, -58], [88, 0, -58]])
notifing_list = []

def start():
    print('[[Server is listening]]')
    Server.listen()
    while True:
        conn, addr = Server.accept()
        print(f'[[New Connection]] {addr} has connected!!')
        T(target=handle_client, args=(conn, addr)).start()

print('[[Server is Starting]]')
start()