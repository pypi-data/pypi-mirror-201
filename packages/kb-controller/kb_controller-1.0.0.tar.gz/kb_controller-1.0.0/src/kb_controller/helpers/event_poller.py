from threading import Thread
from time import sleep
from datetime import datetime
from . import microbit
from . import kb_config
from . import kb_central
from . import helper

thread = None

def kb_central_poller(current_track_id):
    sleep(1) # Give controller time to initialize
    while True:
        print()
        print('- - - - - - - - - - - - - - - - - - - - -')
        print('Henter events fra kukglebane centralen...')
        print()

        count = kb_central.get_number_of_events_for_track(current_track_id)
        print()
        print(f'Antal events modtaget i alt: {count}')
        print()

        # Do not send events automatically for now
        # We go for a "pure" polling solution

        # microbit.send_message(f'EVENT-TRACKS:{current_track_id}:{count}')

        interval = kb_config.poll_interval_in_seconds
        text_interval = f'{interval} sekunder' if interval <=60 else f'ca. {"%.0f" % (interval / 60)} minutter'

        print(f'Kontakter kuglebane-centralen igen om {text_interval}...')
        print('- - - - - - - - - - - - - - - - - - - - -')
        print()
        sleep(kb_config.poll_interval_in_seconds)

def start_thread(current_track_id):
    print()
    print(f'Starter baggrunds-tråd der poller kb-centralen: {kb_config.kbc_host}')
    global thread
    if thread is None:
        thread = Thread(group=None, daemon=True, target=kb_central_poller, args=(current_track_id,))
        thread.start()
