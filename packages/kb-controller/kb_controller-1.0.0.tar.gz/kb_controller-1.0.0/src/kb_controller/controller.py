import serial
import os
import getpass
from kb_controller.helpers import kb_config, kb_central, microbit, event_poller, helper

current_track_id = 0
department_id = 0
tracks_per_department = {}

def start():
    clear_console()
    print()
    print(f'  CONTROLLER STARTER OP {helper.getDateString()}')
    print('================================================')
    microbit.initialize_connection()
    print()
    print('Tjek evt. https://kuglebane.pythonanywhere.com/users/')
    print()
    u = input('Api bruger: ')
    p = getpass.getpass(prompt='Kodeord:')
    kb_config.set_api_user(u,p)

    global current_track_id
    global department_id
    global tracks_per_department

    department_id = kb_central.get_department_id_from_token()
    tracks_per_department = kb_central.get_tracks()

    show_console_info()

    while True:

        if current_track_id > 0 and event_poller.thread is None:
            event_poller.start_thread(current_track_id)

        try:
            byte_text = microbit.read_line()
            response = ''
            text = str(byte_text, 'utf-8').strip()

            if text != '':
                helper.printLog('m:b <<< ' + text)

                if text == 'quit':
                    microbit.send_message('OK:QUIT')
                    break

                if text.startswith('init:'):
                    track = text[5:]
                    if track == '0':
                        print()
                        print("FEJL! Micro:bit'en er sat rigtig op - den står til bane ID = 0")
                        print()
                        response = 'ERROR:INIT:INVALID-TRACK:' + track
                    elif not track in tracks_per_department[department_id]['tracks']:
                        print()
                        print(f'FEJL! Bane ID {track} findes ikke for afdeling {department_id}')
                        print()
                        response = 'ERROR:INIT:INVALID-TRACK:' + track
                        
                    else:
                        current_track_id = int(track)
                        response = 'OK:INIT:' + track
                        print_tracks()

                elif current_track_id == 0:
                    print()
                    print('Der er ikke tilknyttet en kuglebane til controlleren')
                    print('Brug kommandoen: "init:<<kuglebane-ID>>" for at tilknytte kuglebanen')
                    print("Dette kan du f.eks. programmere micro:bit'en til at gøre :-)")
                    print()
                    response = 'ERROR:NOT-INITIALIZED'

                elif (text == 'events'):
                    print()
                    print('Henter events for kuglebanen')
                    print('-----------------------------')
                    count = kb_central.get_number_of_events_for_track(current_track_id)
                    response = f'OK:EVENTS-TRACK:{current_track_id}:{count}'

                elif text.startswith('send:'):
                    to_track = text[5:]
                    to_track_exists = False
                    for dep_id in tracks_per_department:
                        to_track_exists = to_track in tracks_per_department[dep_id]['tracks']
                        if to_track_exists:
                            break

                    if not to_track_exists:
                        print(f'ERROR! Bane ID {to_track} findes ikke!')
                        response = 'ERROR:START:INVALID-TRACK:' + to_track
                    else:
                        print()
                        print(
                            f'Sender START besked til "bane {to_track}"')
                        print('-------------------------------------')
                        kb_central.send_start_event(current_track_id, to_track)
                        response = 'OK:SEND:' + to_track

                elif text.startswith('pop'):
                        print()
                        print(
                            '"Popper" den ældste vent fra event-køen')
                        print('-------------------------------------')
                        events = kb_central.get_events_for_track(current_track_id)
                        if events is None or not 'events' in events:
                            response = 'ERROR:POP:INGEN-EVENTS'
                        else:
                            response = pop_event(events)

                elif text.startswith('FEJL!'):
                    print()
                    print("Microbit'en har opgivet dét den var igang med.")
                    print('Prøv igen (eller undersøg hvilke fejl der er skrevt i konsollen herover)')

                else:
                    print('Ukendt kommando modtaget: ' + text)
                    response = 'ERROR:unknown-command'

            if not response=='':
                microbit.send_message(response)

        except serial.serialutil.SerialException as err:
            print()
            print("Der skete en fejl med den serielle forbindelse!")
            print(type(err))
            print(err)
            print(err.args)
            break

        except Exception as err:
            print()
            print("Der skete en fejl!")
            print(type(err))
            print(err)
            print(err.args)
            microbit.send_message('ERROR:Exception')

    microbit.close_connection()

    print()
    print(f'FARVEL! Controlleren lukker ned nu! {helper.getDateString()}')
    print()


def pop_event(events):
    # first event is always the oldest
    event_id_to_pop = list(events['events'])[0]
    event = events['events'][event_id_to_pop]

    kb_central.print_kb_event(event_id_to_pop, event)

    command_id = event['command_id']
    from_department_id = event['from_department_id']
    from_track_id = event['from_track_id']

    kb_central.delete_event(event_id_to_pop)
    return f'OK:POP:{from_department_id}:{from_track_id}:{command_id}'

def clear_console():
    global department_id
    global tracks_per_department
    os.system('cls' if os.name == 'nt' else 'clear')

def show_console_info():
    print()
    print('============================================================')
    print('   M I C R O : B I T   S E R I A L   C O N T R O L L E R')
    print('============================================================')
    print(f'Kuglebane central........: {kb_config.kbc_host}')
    print(f'API bruger...............: {kb_config.api_user}')
    print(f'Controller for afdeling..: {department_id}')
    print('-----------------------------------------------------------')
    print()
    print('Kommandoer:')
    print()
    print('  init:<<kuglebane_id>>')
    print('     - fortæller hvilken kuglebane controlleren håndterer')
    print()
    print('  events')
    print('     - henter alle events for den kuglebane controlleren håndterer')
    print('       BEMÆRK: controlleren spørger automatisk efter disse events i')
    print('               det interval der er angivet i "polling_interval" i ')
    print('               kbc-config.ini filen')
    print()
    print('  pop')
    print('     - henter den ældste besked til den kuglebane controlleren håndterer')
    print("     - sender kommandoen fra beskeden til micro:bit'en")
    print("     - sletter beskeden fra kuglebane centralen")
    print()
    print('  send:<<to_track_id>>')
    print('     - sender en besked til en anden kuglebane om at starte kuglen')
    print()
    print('  quit')
    print('     - Afbryder controlleren')
    print()
    print('-----------------------------------------------------------')
    print()
    print("Venter på at modtage en 'init' kommando fra micro:bit'en...")
    print()

def print_tracks():
    global current_track_id
    global department_id
    global tracks_per_department

    print()
    print('-----------------------------------------------------------')
    print('Tilgængelige kuglebaner:')
    print()
    print(f'  {department_id} (egen afdeling):')
    print('  -------------------------------------')
    own_tracks = tracks_per_department[department_id]['tracks']
    for track_id in own_tracks:
        is_controlled_track = (int(track_id) == current_track_id)
        print(f"    {track_id} - {own_tracks[track_id]}    {'[CONTROLLER]' if is_controlled_track else ''}")
    print('  -------------------------------------')

    for dep_id in tracks_per_department:
        if not dep_id == department_id:
            print()
            print(f'  {dep_id}:')
            tracks = tracks_per_department[dep_id]['tracks']
            for track_id in tracks:
                print(f"    {track_id} - {tracks[track_id]}")
    print('-----------------------------------------------------------')
    print()


if __name__ == '__main__':
    start()