# Håndterer alle requests og forespørgsler til kuglebane centralen

import jwt
from requests.auth import HTTPBasicAuth
import requests
from datetime import datetime
from . import kb_config, helper

jwt_token = None

def get_tracks():
    response = get_request_to_host('api/tracks/all')
    return response.json()['departments']


def send_start_event(from_track_id, to_track_id):
    #'/event/<int:from_track_id>/<int:to_track_id>/<command_id>'
    response = post_request_to_host(f'api/event/{from_track_id}/{to_track_id}/START')
    print(response.text)


def get_events_for_department():
    response = get_request_to_host('api/events/department')
    events = response.json()
    print('Response:')
    print(events)
    return events


def get_number_of_events_for_track(track_id):
    response = get_events_for_track(track_id)
    count = 0 if len(response)==0 else len(response["events"])
    return count

def get_events_for_track(track_id):
    response = get_request_to_host(f'api/events/{track_id}')
    events = response.json()
    print()
    if len(events) > 0:
        for event_id in events["events"]:
            print_kb_event(event_id, events["events"][event_id])
            print()
    return events

def print_kb_event(event_id, event):
    command_id = event['command_id']
    created = event['created']
    from_department_id = event['from_department_id']
    from_track_id = event['from_track_id']
    from_track_name = event['from_track_name']

    print(f' Event id: {event_id} - kommando: {command_id}')
    print(f'   - afsendt: {created}')
    print(f'   - fra {from_department_id}, bane {from_track_id} ({from_track_name})')


def delete_event(event_id):
    response = delete_request_to_host(f'api/event/{event_id}')
    print(response.text)


def get_jwt_bearer_auth_header():
    headers = {"Authorization": f"Bearer {get_auth_jwt_token()}"}
    return headers

def get_department_id_from_token():
    return get_decoded_jwt(get_auth_jwt_token())['department_id']

def get_decoded_jwt(token):
    key = "jwt_lkasjdf/(asdkjfh#AQWD!)" if kb_config.is_production else "jwt_dev"
    decoded_jwt = jwt.decode(token, key, algorithms=["HS256"])
    return decoded_jwt

def get_auth_jwt_token():
    global jwt_token

    if jwt_token is None:
        print('Getting token...')
        jwt_token = request_token_from_kb_cetral()

    try:
        get_decoded_jwt(jwt_token)
    except jwt.ExpiredSignatureError:
        print('Token expired! Renewing...')
        jwt_token = request_token_from_kb_cetral()

    return jwt_token

def request_token_from_kb_cetral():
    basic = HTTPBasicAuth(kb_config.api_user, kb_config.pwd)
    url = f'{kb_config.kbc_host}auth/token'
    helper.printLog(f'KB-CENTRAL >>> {url}')
    try:
        response = requests.get(url, auth=basic)
    except requests.exceptions.ConnectionError as e:
        print_http_connection_error(e)
        exit()
    try:
        validate_response(response)
    except Exception as e:
        print()
        print(e)
        print()
        exit()

    return response.json()['token']


def validate_response(response):
    if not response.status_code == 200:
        raise Exception(f'Response not OK! URL: {response.url} (status = {response.status_code})')
    
    helper.printLog(f'KB-CENTRAL <<< Response status OK!')
    print()

    
def get_request_to_host(endpoint):
    url = f'{kb_config.kbc_host}{endpoint}'
    helper.printLog(f'KB-CENTRAL >>> {url}  [GET]')
    try:
        response = requests.get(url, headers=get_jwt_bearer_auth_header())
    except requests.exceptions.ConnectionError as e:
        print_http_connection_error(e)
        exit()
    validate_response(response)
    return response
    
def post_request_to_host(endpoint):
    url = f'{kb_config.kbc_host}{endpoint}'
    helper.printLog(f'KB-CENTRAL >>> {url}  [POST]')
    try:
        response = requests.post(url, headers=get_jwt_bearer_auth_header())
    except requests.exceptions.ConnectionError as e:
        print_http_connection_error(e)
        exit()
    validate_response(response)
    return response

def delete_request_to_host(endpoint):
    url = f'{kb_config.kbc_host}{endpoint}'
    helper.printLog(f'KB-CENTRAL >>> {url}  [DELETE]')
    try:
        response = requests.delete(url, headers=get_jwt_bearer_auth_header())
    except requests.exceptions.ConnectionError as e:
        print_http_connection_error(e)
        exit()
    validate_response(response)
    return response

def print_http_connection_error(e):    
    print()
    print("FEJL! Ingen forbindelse til kugelbane centralen!")
    print(f"Host: {kb_config.kbc_host}")
    print()
    print(type(e))
    print(e)
    print(e.args)
