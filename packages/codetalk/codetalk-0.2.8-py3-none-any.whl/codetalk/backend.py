import gzip
import json
import logging
import requests
import sseclient
import traceback

from . import logconf
from . import index
from .config import get_config
from .formatter import TokenFormatter
from .spinner import spinner

SERVER_ADDRESS = "https://server.codetalk.ai:8000"

def codetalk_api_call(route, payload={}, use_gzip=False):
    server = get_config('override_ip') or SERVER_ADDRESS
    addr = server + route
    auth_token = get_config('user_token')
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Content-Type": "application/json",
    }

    if use_gzip:
        payload = gzip.compress(json.dumps(payload).encode())
        headers["Content-Encoding"] = "gzip"
    else:
        payload = json.dumps(payload)

    try:
        response = requests.post(addr, data=payload, headers=headers)
    except KeyboardInterrupt:
        return None
    except:
        logging.error(f"Error when calling codetalk API: {traceback.format_exc()}")
        print("Failed to reach the Codetalk API, quitting...")
        exit(-1)

    return response

def validate_token(token):
    server = get_config('override_ip') or SERVER_ADDRESS
    addr = server + '/validate'
    headers = {'Authorization': f'Bearer {token}'}

    try:
        response = requests.get(addr, headers=headers)
    except Exception as e:
        print(f"Error validating token: {e}")
        return False

    if response.status_code == 200:
        return response.json()["valid"]
    else:
        return False

def _stream_message(client, tokens, use_formatter=True):
    token_fmt = TokenFormatter()
    last_event_role = None
    last_token = ''

    for event in client.events():
        if event.event != 'message':
            continue
        if event.data == '[DONE]':
            continue

        data = json.loads(event.data)
        current_event_role = data.get('choices', [{}])[0].get('delta', {}).get('role', None)
        token = data.get('choices', [{}])[0].get('delta', {}).get('content', None)
        if last_event_role == 'assistant' and token == '\n\n':
            last_event_role = None
            continue

        if token:
            if last_token:
                token = last_token + token
                last_token = ''
            if '`' in token and len(token) < 3:
                last_token = token
                continue

            tokens.append(token)
            if use_formatter:
                token_fmt.process_token(token)
            else:
                print(token, end='', flush=True)

        last_event_role = current_event_role

@spinner(text='Thinking...')
def get_stream_client(addr, headers, data):
    response = requests.post(addr, headers=headers, json=data, stream=True)
    return sseclient.SSEClient(response)

def get_response(query, messages):
    server = get_config('override_ip') or SERVER_ADDRESS
    addr = server + '/respond'

    auth_token = get_config('user_token')
    headers = {
        "Authorization": f"Bearer {auth_token}",
        'Accept': 'text/event-stream',
    }

    data = {
        'messages': messages,
        'query': query,
        'project_id': get_config('current_project'),
    }

    client = get_stream_client(addr, headers, data)
    if client == '__KEYBOARD_INTERRUPT':
        return client

    tokens = []
    try:
        _stream_message(client, tokens)
    except KeyboardInterrupt:
        pass

    return ''.join(tokens)

@spinner(text="Indexing...")
def create_index(project_path):
    files_to_index = index.get_files(project_path)
    logging.info(f'indexing on {len(files_to_index)} files')
    try:
        project_id = index.get_project(project_path)
    except:
        traceback.print_exc()
        return
    logging.debug(f'using project_id {project_id}')

    payload = {
        'files': files_to_index, # TODO encrypt files
        'project_path': project_path,
        'project_id': project_id,
    }

    logging.info(f"sending index request for {project_id}")
    response = codetalk_api_call('/index', payload=payload, use_gzip=True)
    data = response.json()
    logging.info(f"index route response: {response.text}")

    if response.status_code == 200:
        index.insert_project(project_path, data['project_id'])
    return response.json()['message']
