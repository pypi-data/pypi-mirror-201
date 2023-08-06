import socket
import gymnasium as gym
import math
import pyglet
from pyglet.window import key
from FlagCapture.entity import MeshEnt
from FlagCapture.miniworld import MiniWorldEnv
from FlagCapture.utils import get_file_path
from  FlagCapture.build import BUILD
from threading import Thread as T

BUILD()

Ip = socket.gethostbyname('Anthony')
Port = 4544

ADDR = (Ip, Port)

cl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cl.connect(ADDR)

cl.send('Capture the red-and-blue special flags that are available for capture.'.encode('utf-8'))

start_info = eval(cl.recv(58000).decode('utf-8').split('A@^!')[0])

class Scene(MiniWorldEnv):
    def __init__(self, **kwargs):
        MiniWorldEnv.__init__(self, **kwargs)
    def _gen_world(self):
        self.mainroom = self.add_rect_room(min_x=0, max_x=92, min_z=-60, max_z=60)
        self.add_rect_room(min_x=2, max_x=2.01, min_z=-4, max_z=4, wall_tex='brick_wall')
        self.add_rect_room(min_x=10, max_x=10.01, min_z=-4, max_z=4, wall_tex='brick_wall')
        self.add_rect_room(min_x=18, max_x=18.01, min_z=-4, max_z=4, wall_tex='brick_wall')
        self.add_rect_room(min_x=26, max_x=26.01, min_z=-4, max_z=4, wall_tex='brick_wall')
        self.add_rect_room(min_x=34, max_x=34.01, min_z=-4, max_z=4, wall_tex='brick_wall')
        self.add_rect_room(min_x=42, max_x=42.01, min_z=-4, max_z=4, wall_tex='brick_wall')
        self.add_rect_room(min_x=50, max_x=50.01, min_z=-4, max_z=4, wall_tex='brick_wall')
        self.add_rect_room(min_x=58, max_x=58.01, min_z=-4, max_z=4, wall_tex='brick_wall')
        self.add_rect_room(min_x=66, max_x=66.01, min_z=-4, max_z=4, wall_tex='brick_wall')
        self.add_rect_room(min_x=74, max_x=74.01, min_z=-4, max_z=4, wall_tex='brick_wall')
        self.add_rect_room(min_x=82, max_x=82.01, min_z=-4, max_z=4, wall_tex='brick_wall')
        self.add_rect_room(min_x=90, max_x=90.01, min_z=-4, max_z=4, wall_tex='brick_wall')
        self.add_rect_room(min_x=2, max_x=10, min_z=-0.005, max_z=0.005, wall_tex='brick_wall')
        self.add_rect_room(min_x=18, max_x=26, min_z=-0.005, max_z=0.005, wall_tex='brick_wall')
        self.add_rect_room(min_x=34, max_x=42, min_z=-0.005, max_z=0.005, wall_tex='brick_wall')
        self.add_rect_room(min_x=50, max_x=58, min_z=-0.005, max_z=0.005, wall_tex='brick_wall')
        self.add_rect_room(min_x=66, max_x=74, min_z=-0.005, max_z=0.005, wall_tex='brick_wall')
        self.add_rect_room(min_x=82, max_x=90, min_z=-0.005, max_z=0.005, wall_tex='brick_wall')
        
        self.add_rect_room(min_x=2, max_x=22, min_z=28, max_z=28.01, wall_tex='redColor')
        self.add_rect_room(min_x=22, max_x=22.01, min_z=6, max_z=28, wall_tex='redColor')
        self.add_rect_room(min_x=78, max_x=90, min_z=28, max_z=28.01, wall_tex='redColor')
        self.add_rect_room(min_x=78, max_x=78.01, min_z=6, max_z=28, wall_tex='redColor')
        self.add_rect_room(min_x=26, max_x=26.01, min_z=20, max_z=36, wall_tex='redColor')
        self.add_rect_room(min_x=74, max_x=74.01, min_z=20, max_z=36, wall_tex='redColor')
        self.add_rect_room(min_x=34, max_x=66, min_z=10, max_z=10.01, wall_tex='redColor')
        self.add_rect_room(min_x=34, max_x=34.01, min_z=10, max_z=22, wall_tex='redColor')
        self.add_rect_room(min_x=66, max_x=66.01, min_z=10, max_z=22, wall_tex='redColor')
        self.add_rect_room(min_x=34, max_x=34.01, min_z=34, max_z=42, wall_tex='redColor')
        self.add_rect_room(min_x=66, max_x=66.01, min_z=34, max_z=42, wall_tex='redColor')
        self.add_rect_room(min_x=34, max_x=44, min_z=42, max_z=42.01, wall_tex='redColor')
        self.add_rect_room(min_x=54, max_x=66, min_z=42, max_z=42.01, wall_tex='redColor')
        self.add_rect_room(min_x=0, max_x=42, min_z=45, max_z=45.01, wall_tex='redColor')
        self.add_rect_room(min_x=56, max_x=92, min_z=45, max_z=45.01, wall_tex='redColor')
        self.add_rect_room(min_x=42.5, max_x=53.5, min_z=47, max_z=47.01, wall_tex='redColor')
        self.add_rect_room(min_x=40, max_x=46.5, min_z=49, max_z=49.01, wall_tex='redColor')
        self.add_rect_room(min_x=49.5, max_x=56, min_z=49, max_z=49.01, wall_tex='redColor')
        self.add_rect_room(min_x=40, max_x=40.01, min_z=49, max_z=60, wall_tex='redColor')
        self.add_rect_room(min_x=56, max_x=56.01, min_z=49, max_z=60, wall_tex='redColor')
        self.add_rect_room(min_x=18, max_x=35, min_z=49, max_z=49.01, wall_tex='redColor')
        self.add_rect_room(min_x=0, max_x=2, min_z=49, max_z=49.01, wall_tex='redColor')
        self.add_rect_room(min_x=4, max_x=10, min_z=49, max_z=49.01, wall_tex='redColor')
        self.add_rect_room(min_x=10, max_x=10.01, min_z=49, max_z=58, wall_tex='redColor')
        self.add_rect_room(min_x=61, max_x=74, min_z=49, max_z=49.01, wall_tex='redColor')
        self.add_rect_room(min_x=90, max_x=92, min_z=49, max_z=49.01, wall_tex='redColor')
        self.add_rect_room(min_x=82, max_x=88, min_z=49, max_z=49.01, wall_tex='redColor')
        self.add_rect_room(min_x=82, max_x=82.01, min_z=49, max_z=58, wall_tex='redColor')

        self.add_rect_room(min_x=2, max_x=22, max_z=-28, min_z=-28.01, wall_tex='blueColor')
        self.add_rect_room(min_x=22, max_x=22.01, max_z=-6, min_z=-28, wall_tex='blueColor')
        self.add_rect_room(min_x=78, max_x=90, max_z=-28, min_z=-28.01, wall_tex='blueColor')
        self.add_rect_room(min_x=78, max_x=78.01, max_z=-6, min_z=-28, wall_tex='blueColor')
        self.add_rect_room(min_x=26, max_x=26.01, max_z=-20, min_z=-36, wall_tex='blueColor')
        self.add_rect_room(min_x=74, max_x=74.01, max_z=-20, min_z=-36, wall_tex='blueColor')
        self.add_rect_room(min_x=34, max_x=66, max_z=-10, min_z=-10.01, wall_tex='blueColor')
        self.add_rect_room(min_x=34, max_x=34.01, max_z=-10, min_z=-22, wall_tex='blueColor')
        self.add_rect_room(min_x=66, max_x=66.01, max_z=-10, min_z=-22, wall_tex='blueColor')
        self.add_rect_room(min_x=34, max_x=34.01, max_z=-34, min_z=-42, wall_tex='blueColor')
        self.add_rect_room(min_x=66, max_x=66.01, max_z=-34, min_z=-42, wall_tex='blueColor')
        self.add_rect_room(min_x=34, max_x=44, max_z=-42, min_z=-42.01, wall_tex='blueColor')
        self.add_rect_room(min_x=54, max_x=66, max_z=-42, min_z=-42.01, wall_tex='blueColor')
        self.add_rect_room(min_x=0, max_x=42, max_z=-45, min_z=-45.01, wall_tex='blueColor')
        self.add_rect_room(min_x=56, max_x=92, max_z=-45, min_z=-45.01, wall_tex='blueColor')
        self.add_rect_room(min_x=42.5, max_x=53.5, max_z=-47, min_z=-47.01, wall_tex='blueColor')
        self.add_rect_room(min_x=40, max_x=46.5, max_z=-49, min_z=-49.01, wall_tex='blueColor')
        self.add_rect_room(min_x=49.5, max_x=56, max_z=-49, min_z=-49.01, wall_tex='blueColor' )
        self.add_rect_room(min_x=40, max_x=40.01, max_z=-49, min_z=-60, wall_tex='blueColor')
        self.add_rect_room(min_x=56, max_x=56.01, max_z=-49, min_z=-60, wall_tex='blueColor')
        self.add_rect_room(min_x=18, max_x=35, max_z=-49, min_z=-49.01, wall_tex='blueColor')
        self.add_rect_room(min_x=0, max_x=2, max_z=-49, min_z=-49.01, wall_tex='blueColor')
        self.add_rect_room(min_x=4, max_x=10, max_z=-49, min_z=-49.01, wall_tex='blueColor')
        self.add_rect_room(min_x=10, max_x=10.01, max_z=-49, min_z=-58, wall_tex='blueColor')
        self.add_rect_room(min_x=61, max_x=74, max_z=-49, min_z=-49.01, wall_tex='blueColor')
        self.add_rect_room(min_x=90, max_x=92, max_z=-49, min_z=-49.01, wall_tex='blueColor')
        self.add_rect_room(min_x=82, max_x=88, max_z=-49, min_z=-49.01, wall_tex='blueColor')
        self.add_rect_room(min_x=82, max_x=82.01, max_z=-49, min_z=-58, wall_tex='blueColor')
        self.redGate = self.place_entity(MeshEnt(mesh_name=f'gate', height=2.6), pos=[48, 0, 49], dir=-3.1)
        self.blueGate = self.place_entity(MeshEnt(mesh_name=f'gate', height=2.6), pos=[48, 0, -49], dir=6.3)
        self.redFlag = self.place_entity(MeshEnt(mesh_name=f'flagRed', height=2.5, static=False), pos=start_info['RedFlagPos'])
        self.blueFlag = self.place_entity(MeshEnt(mesh_name=f'flagBlue', height=2.5, static=False), pos=start_info['BlueFlagPos'])
        for person in start_info['Everything']:
            animal = self.place_entity(MeshEnt(mesh_name=f''+start_info['Everything'][person]['team'], height=1.4, static=False), pos=start_info['Everything'][person]['pos'], dir=start_info['Everything'][person]['dir'])
            people[person] = animal
            if start_info['Everything'][person]['team'] == myTeam:
                list_of_players_on_my_team.append(person)
            else:
                list_of_players_on_their_team.append(person)
        self.leftRedButton = self.place_entity(MeshEnt(mesh_name=f'RedButton', height=1), pos=[82.5, 1, -44.749], dir=-1.5)
        self.rightRedButton = self.place_entity(MeshEnt(mesh_name=f'RedButton', height=1), pos=[9.5, 1, -44.749], dir=-1.5)
        self.rightBlueButton = self.place_entity(MeshEnt(mesh_name=f'BlueButton', height=1), pos=[9.5, 1, 44.749], dir=1.6)
        self.leftBlueButton = self.place_entity(MeshEnt(mesh_name=f'BlueButton', height=1), pos=[82.5, 1, 44.749], dir=1.6)
        self.place_agent()

gym.envs.registration.register(id='Enviroment', entry_point=Scene)

myinfo = start_info['MyInfo']

myTeam = myinfo['team']
myId = myinfo['id']

list_of_players_on_my_team = []
list_of_players_on_their_team = []
people = {}

creating = False

board = key.KeyStateHandler()
scene = gym.make("Enviroment", view='agent', render_mode='human')
scene.unwrapped.fuel = 5
scene.reset()
scene.agent.pos = [myinfo['x'], 0, myinfo['z']]
scene.agent.dir = myinfo['dir']
scene.render()
scene.unwrapped.window.push_handlers(board)
scene.unwrapped.window.set_icon(pyglet.image.load(get_file_path("images", "icon", "png")))
caption = f'Capture the Flag: [{myTeam} Team]'
scene.unwrapped.window.set_caption(caption)
scene.unwrapped.window.maximize()
scene.unwrapped.window.set_mouse_visible(False)

def forward(obj, speed):
    global touching
    direction = -obj.dir
    x = obj.pos[0] + math.cos(direction)*speed
    z = obj.pos[2] + math.sin(direction)*speed
    intersection = scene.intersect(obj, [x, 0, z], obj.radius)
    if not touching:
        if myTeam == 'wolf':
            if intersection == scene.leftBlueButton or intersection == scene.rightBlueButton:
                cl.send(str(['Updating touching', {'touching': True}]).encode('utf-8'))
                touching = True
        if myTeam == 'lynx':
            if intersection == scene.leftRedButton or intersection == scene.rightRedButton:
                cl.send(str(['Updating touching', {'touching': True}]).encode('utf-8'))
                touching = True
    if intersection == scene.blueGate and IAmPrisoner:return
    if intersection == scene.redGate and IAmPrisoner:return
    if intersection == True:
        x_pos = [x, 0, obj.pos[2]]
        if scene.intersect(obj, x_pos, obj.radius) == True:
            z_pos = [obj.pos[0], 0, z]
            if scene.intersect(obj, z_pos, obj.radius) == True:
                return
            else:
                obj.pos = [obj.pos[0], 0, z]
        else:
            obj.pos = [x, 0, obj.pos[2]]
    else:
        obj.pos = [x, 0, z]
    if carrying == 'red' and z < 0:blue_wins()
    if carrying == 'blue' and z > 0:red_wins()

speed = 0.4

def tell_pos_to_server(dt):
    cl.send(str(['Updating pos', {'pos': scene.agent.pos}]).encode('utf-8'))

def tell_dir_to_server(dt):
    cl.send(str(['Updating dir', {'dir': scene.agent.dir}]).encode('utf-8'))

def update(dt):
    global speed, carrying
    scene.unwrapped.fuel += 1
    if board[key.UP]:
        forward(scene.agent, speed)
        pyglet.clock.schedule_once(tell_pos_to_server, 1.0/60)
    if board[key.LEFT]:
        scene.agent.dir += speed/2
        pyglet.clock.schedule_once(tell_dir_to_server, 1.0/60)
    if board[key.RIGHT]:
        scene.agent.dir -= speed/2
        pyglet.clock.schedule_once(tell_dir_to_server, 1.0/60)
    if board[key.DOWN]:
        forward(scene.agent, -speed)
        pyglet.clock.schedule_once(tell_pos_to_server, 1.0/60)
    if board[key.P]:
        if scene.intersect(scene.agent, scene.agent.pos, scene.agent.radius) == scene.redFlag:
            carrying = 'red'
            scene.unwrapped.window.set_caption(f'{caption} [CARRYING A FLAG]')
            cl.send(str(['Updating carrying', {'carrying': 'red'}]).encode('utf-8'))
            scene.redFlag.pos = [30, -90, 0]
        if scene.intersect(scene.agent, scene.agent.pos, scene.agent.radius) == scene.blueFlag:
            carrying = 'blue'
            scene.unwrapped.window.set_caption(f'{caption} [CARRYING A FLAG]')
            cl.send(str(['Updating carrying', {'carrying': 'blue'}]).encode('utf-8'))
            scene.blueFlag.pos = [30, -90, 0]

    if board[key.D]:
        drop_flag()

    if board[key.SPACE]:
        if scene.unwrapped.fuel < 3:
            speed = 0.4
        else:
            scene.unwrapped.fuel -= 3
            speed = 0.8
    else:
        speed = 0.4
    scene.render()

def blue_wins():
    def close(dt):
        scene.close()
    pyglet.clock.schedule_once(close, 4)
    alert(get_file_path("images", "wolfwin", "png"), 4)

def red_wins():
    def close(dt):
        scene.close()
    pyglet.clock.schedule_once(close, 4)
    alert(get_file_path("images", "lynxwin", "png"), 4)

def drop_flag():
    global carrying
    if carrying:
        if carrying == 'red':
            scene.redFlag.pos = scene.agent.pos
            if scene.redFlag.pos[2] < 0:blue_wins()   
        elif carrying == 'blue':
            scene.blueFlag.pos = scene.agent.pos
            if scene.blueFlag.pos[2] > 0:red_wins()
        cl.send(str(['drop', {'flag': carrying}]).encode('utf-8'))
        carrying = None
        scene.unwrapped.window.set_caption(caption)

carrying = None

IAmPrisoner = False

def alert(picture, time):
    scene.unwrapped.alert = pyglet.image.load(picture)
    scene.unwrapped.showAlert = True
    def put_back(dt):
        scene.unwrapped.showAlert = False
    pyglet.clock.schedule_once(put_back, time)

@scene.unwrapped.window.event
def on_draw():
    scene.unwrapped.window.clear()
    scene.render() 

def recv():
    global raw_message
    while True:
        raw_message = cl.recv(58000).decode('utf-8').split('A@^!')[0]
        if raw_message.strip() == '':continue
        pyglet.clock.schedule_once(process_message, 1.0/60)

raw_message = None

message = {}

def process_message(dt):
    global IAmPrisoner, message, creating
    try:
        message = eval(raw_message)
    except SyntaxError:
        return
    for person in message:
        if person not in people and person != myId and not creating:#Some one joined
            creating = True
            animal = scene.place_entity(MeshEnt(mesh_name=message[person]['team'], height=1.4, static=False), pos=message[person]['pos'], dir=message[person]['dir'])
            print(message[person]['pos'])
            people[person] = animal
            if message[person]['team'] == myTeam:
                list_of_players_on_my_team.append(person)
            else:
                list_of_players_on_their_team.append(person)
            creating = False

        elif person != myId: #Update the players
            people[person].pos = message[person]['pos']
            people[person].dir = message[person]['dir']
            if message[person]['carrying'] == 'red':
                scene.redFlag.pos = [message[person]['pos'][0], 0, message[person]['pos'][2]]
                if scene.redFlag.pos[2] < 0:blue_wins()
                scene.redFlag.dir = math.radians(math.degrees(message[person]['dir'])+180)
            if message[person]['carrying'] == 'blue':
                scene.blueFlag.pos = [message[person]['pos'][0], 0, message[person]['pos'][2]]
                if scene.blueFlag.pos[2] > 0:red_wins()
                scene.blueFlag.dir = math.radians(math.degrees(message[person]['dir'])+180)

            check_for_capture_and_touching_button()

            if person in list_of_players_on_my_team and IAmPrisoner and message[person]['touching']:#Check to see if someone is freeing you
                    IAmPrisoner=False
                    alert(get_file_path("images", "release", "png"), 2.5)
    for person in people:
        if person not in message:#Some one left
            scene.unwrapped.entities.remove(people[person])
            del people[person]
            try: list_of_players_on_my_team.remove(person)
            except ValueError: list_of_players_on_their_team.remove(person)
            break

@scene.unwrapped.window.event
def on_close():
    cl.close()

touching = False

def check_for_capture_and_touching_button():
    global IAmPrisoner, touching
    intersection = scene.intersect(scene.agent, scene.agent.pos, scene.agent.radius)

    #Check for touching button
    if touching:
        if myTeam == 'wolf':
            if intersection != scene.leftBlueButton or intersection == scene.rightBlueButton:
                cl.send(str(['Updating touching', {'touching': False}]).encode('utf-8'))
                touching = False
        if myTeam == 'lynx':
            if intersection != scene.leftRedButton or intersection == scene.rightRedButton:
                cl.send(str(['Updating touching', {'touching': False}]).encode('utf-8'))
                touching = False

    #Check for touching enemy and in enemy territory
    for person in list_of_players_on_their_team:
        if intersection == people[person] and scene.agent.pos[2] < 0:
            if myTeam == 'wolf':
                if carrying:
                    drop_flag()
                    scene.agent.pos = [48, 0, -55]
                    scene.agent.dir = 4.754
                    IAmPrisoner = True
                    cl.send(str(['Updating prisoner', {'prisoner': [48, 0, -55]}]).encode('utf-8'))
                    cl.send(str(['Updating pos', {'pos': [48, 0, -55]}]).encode('utf-8'))
            if myTeam == 'lynx':
                if message[person]['carrying']: return
                if message[person]['prisoner']: return
                drop_flag()
                scene.agent.pos = [48, 0, 55]
                scene.agent.dir = 1.654
                IAmPrisoner = True
                cl.send(str(['Updating prisoner', {'prisoner': [48, 0, -55]}]).encode('utf-8'))
                cl.send(str(['Updating pos', {'pos': [48, 0, 55]}]).encode('utf-8'))
        if intersection == people[person] and scene.agent.pos[2] > 0:
            if myTeam == 'lynx':
                if carrying:
                    drop_flag()
                    scene.agent.pos = [48, 0, 55]
                    scene.agent.dir = 1.654
                    IAmPrisoner = True
                    cl.send(str(['Updating prisoner', {'prisoner': [48, 0, -55]}]).encode('utf-8'))
                    cl.send(str(['Updating pos', {'pos': [48, 0, 55]}]).encode('utf-8'))
            if myTeam == 'wolf':
                if message[person]['carrying']:return
                if message[person]['prisoner']: return
                drop_flag()
                scene.agent.pos = [48, 0, -55]
                scene.agent.dir = 4.754
                IAmPrisoner = True
                cl.send(str(['Updating prisoner', {'prisoner': [48, 0, -55]}]).encode('utf-8'))
                cl.send(str(['Updating pos', {'pos': [48, 0, -55]}]).encode('utf-8'))


T(target=recv).start()

pyglet.clock.schedule_interval(update, 1.0/30)
pyglet.app.run()
