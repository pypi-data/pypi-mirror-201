import os
if os.name == 'nt':
    print()
    print('Windows understøttes ikke p.t.!')
    print()
    quit()

import sys
import pty
from time import sleep
from threading import Thread

EMULATOR_PROMPT = 'Skriv kommando der skal sendes til controlleren og tryk <Enter>: '

is_ctrl_initialized = False
track_id = 1

def listen_to_controller(master):
    global is_ctrl_initialized, track_id

    print(f'Starter lytte-tråd...')

    if not is_ctrl_initialized:
        print('Venter på controller i baggrunden...')

    while True:
        s_input = os.read(master, 100)
        recieved = str(s_input, 'utf-8').strip()

        if len(s_input) > 0:
            print()
            print('<-- ' + recieved)

            if (recieved == 'init'):
                print('Controlleren er vågnet...! Init-signal modtaget.')
                print(f'Sender bane-ID "{track_id}" til controller')
                text = f'init:{track_id}\n'
                print(f'--> {text}')
                os.write(master, text.encode('utf-8'))
                sleep(0.5)
                s_input = os.read(master, 100)
                if len(s_input) == 0:
                    print("Fejl! Ingen svar modtaget!")
                else:
                    recieved = str(s_input, 'utf-8').strip()
                    print('<-- ' + recieved)
                    print('Controller INITIALISERET.')
                    is_ctrl_initialized = True

            elif recieved.startswith('EVENT-TRACKS:'):
                temp = recieved[13:]
                slice = temp.index(':')
                track_id = temp[:slice]
                count = temp[slice + 1:]
                print(f'    Kuglebane: {track_id} - antal beskeder: {count}')
             
            elif recieved.startswith('OK:POP:'):
                temp = recieved[7:]
                slice = temp.index(':')
                from_dep_id = temp[:slice]
                temp = temp[len(from_dep_id)+1:]
                slice = temp.index(':')
                from_track_id = temp[:slice]
                command = temp[slice + 1:]
                print(f'    {command} kommando modtaget fra {from_dep_id} - kuglebane {from_track_id}')
             
            elif (recieved == 'OK:QUIT' or recieved == 'quit'):
                print('QUIT kommando modtaget - stopper lytte-tråden!')
                break

            print()
            print(EMULATOR_PROMPT)

def start(id=1):

    global is_ctrl_initialized, track_id

    track_id = id
    if len(sys.argv) > 1:
        track_id = sys.argv[1]

    master, ubitSlave = pty.openpty()
    s_name = os.ttyname(ubitSlave)

    display_emulator_info(s_name)

    event_listener = Thread(group=None, target=listen_to_controller, args=(master,))
    event_listener.start()
    print()

    print()
    print(EMULATOR_PROMPT)
    while True:
        text = input()

        if text == 'clear':
            os.system('cls' if os.name == 'nt' else 'clear')
            display_emulator_info(s_name)
        else:
            if not is_ctrl_initialized:
                print()
                print('Vi venter stadig på controlleren...')
                print()
            else:
                text2send = text + '\n'
                print('--> ' + text)
                os.write(master, text2send.encode('utf-8'))
                sleep(1)

            if  text == 'quit':
                print('Emulatoren lukker og slukker... FARVEL!')
                os.write(master, text.encode('utf-8'))
                break
            

def display_emulator_info(s_name):
    print()
    print()
    print('=============================')
    print('     micro:bit emulator')
    print('=============================')
    print()
    print('Skriv kommandoen "quit" for at afslutte')
    print()
    print('Brug denne port på controlleren:')
    print('--------------------------------')
    print()
    print(s_name)
    print()
    print('--------------------------------')
    print()
    print(f'micro:bit track-ID: {track_id}')
    print()

if __name__ == '__main__':
    start()
