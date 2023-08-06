import logging
import os

from . import logconf
from .backend import create_index
from . import index

def _normalize(path):
    path = os.path.expanduser(path)
    return os.path.normpath(path)

def index_project(query, messages):
    logging.debug("in index_project subcommand")
    words = query.split()
    if len(words) > 1:
        path = _normalize(words[1])
        response = create_index(path)
        messages.clear()
        print(response)
    else:
        logging.warning("No argument provided for `index` command")

def delete_project(query, messages):
    words = query.split()
    if len(words) > 1:
        path = _normalize(words[1])
        index.delete_project(path)
    else:
        logging.warning("No argument provided for `delete` command")

def reindex():
    current_project_id = index.get_config('current_project')
    if not current_project_id:
        print("No current project found. Please index a project first.")
        return

    all_projects = index.get_config('all_projects')
    project_path = None

    for path, project_id in all_projects.items():
        if project_id == current_project_id:
            project_path = path
            break

    if project_path:
        create_index(project_path)
        print("Successfully re-indexed.")
    else:
        print("Current project not found in the list of indexed projects.")

def list_projects(truncate=False):
    projects = index.list_projects()
    if truncate and len(projects) == 1:
        return

    try:
        max_path_length = max(len(p['path']) for p in projects)
        tab_size = 8
    except ValueError: # no projects exist
        return

    for p in projects:
        if p['is_current']:
            hyphens = "-" * (max_path_length - len(p['path']) + tab_size - 2)
            end = f" \033[1;35m<{hyphens} current\033[0m\n"
        else:
            end = "\n"

        line = p['path'] + end
        print(line, end="")

    if truncate:
        print()

def use_project(query, messages):
    words = query.split()
    if len(words) > 1:
        path = _normalize(words[1])
        messages = []
        index.set_project(path)
    else:
        logging.warning("No argument provided for `use` command")

def print_help():
    commands = {
        "help": "Show this message.",
        "clear": "Clear the current message stack.",
        "index": "Index a new project for use with Codetalk.",
        "reindex": "Update the index for the current project.",
        "list": "Show all indexed projects, and the currently selected one.",
        "use": "Set the current project.",
        "delete": "Delete a project locally.",
    }

    max_length = max(len(key) for key in commands.keys())

    for key, value in commands.items():
        key_length = len(key)
        value_length = len(str(value))

        num_spaces = max_length - key_length + 2
        print(key + ":" + " " * num_spaces + str(value))

def is_chat_command(query, messages):
    cmd = query.strip().lower().split(' ')[0]
    if cmd == "":
        return True

    elif cmd == "help":
        print_help()
        print()
        return True

    elif cmd == "clear":
        messages.clear()
        logging.info("Message stack cleared")
        return True

    elif cmd == "index":
        index_project(query, messages)
        print()
        return True

    elif cmd == "delete":
        delete_project(query, messages)
        print()
        return True

    elif cmd == "reindex":
        reindex()
        print()
        return True

    elif cmd == "list":
        list_projects()
        print()
        return True

    elif cmd == "use":
        use_project(query, messages)
        return True

    elif cmd == "quit":
        exit()

    else:
        return False
