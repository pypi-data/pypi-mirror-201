import index
import logconf
import logging
import os

from backend import create_index

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
        logging.warning("No argument provided for index_project command")

    return True

def list_projects():
    projects = index.list_projects()
    max_path_length = max(len(p['path']) for p in projects)
    tab_size = 8

    for p in projects:
        if p['is_current']:
            hyphens = "-" * (max_path_length - len(p['path']) + tab_size - 2)
            end = f" \033[1;35m<{hyphens} current\033[0m\n"
        else:
            end = "\n"

        line = p['path'] + end
        print(line, end="")

def set_project(query, messages):
    words = query.split()
    if len(words) > 1:
        path = _normalize(words[1])
        messages = []
        index.set_project(path)
    else:
        logging.warning("No argument provided for set_project command")

def print_help():
    commands = {
        "help": "Show this message.",
        "clear_context": "Clear the current message stack.",
        "index_project": "Index a new project for use with Codetalk.",
        "list_projects": "Show all indexed projects, and the currently selected one.",
        "set_project": "Set the current project.",
    }

    max_length = max(len(key) for key in commands.keys())

    for key, value in commands.items():
        key_length = len(key)
        value_length = len(str(value))

        num_spaces = max_length - key_length + 2
        print(key + ":" + " " * num_spaces + str(value))

def is_chat_command(query, messages):
    cmd = query.strip().lower().split(' ')[0]
    match cmd:
        case "":
            return True

        case "help":
            print_help()
            print()
            return True

        case "clear_context":
            messages.clear()
            logging.info("Message stack cleared")
            return True

        case "index_project":
            index_project(query, messages)
            print()
            return True

        case "list_projects":
            list_projects()
            print()
            return True

        case "set_project":
            set_project(query, messages)
            return True

        case _:
            return False
