import gzip
import index
import json
import logconf
import logging
import requests
import traceback

from config import get_config
from spinner import spinner

def codetalk_api_call(route, payload={}, use_gzip=False):
    server = 'http://127.0.0.1:8000' if get_config('use_local') else get_config('api_address')
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

@spinner(text="Thinking...")
def get_response(query, messages):
    try:
        project_id = get_config('current_project')
        assert project_id
    except:
        return "You need to index a project before you can use Codetalk.\nTry `index_project $PROJECT_PATH`"

    payload = {
        'query': query,
        'messages': messages,
        'project_id': get_config('current_project'),
    }

    try:
        response = codetalk_api_call("/respond", payload=payload)
        if not response:
            return None
    except:
        traceback.print_exc()
        return

    logging.debug(f"Server response {response.status_code} {response.text}")
    return response.json()['response']

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
