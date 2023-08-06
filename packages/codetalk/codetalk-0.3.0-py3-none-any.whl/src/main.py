import logconf
import logging
import os

from backend import create_index, get_response
from config import get_config, set_config
from formatter import format_output
from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import InMemoryHistory
from subcommand import is_chat_command

def _print_logo():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    logo_path = os.path.join(dir_path, 'assets', 'logo.txt')
    with open(logo_path) as fp:
        logo = fp.read()
    print(logo)

def _validate():
    fields = ['api_address', 'current_project', 'user_token']
    return all(get_config(f) for f in fields)

def _setup():
    if not get_config("api_address"):
        api_addr = "http://54.219.16.72:8000"
        set_config("api_address", api_addr)

    if not get_config('user_token'):
        token = input("Please input your user token: ").strip()
        set_config("user_token", token)

    if not get_config('current_project'):
        while True:
            path = input("Which directory would you like to use with Codetalk?\n> ").strip()
            path = os.path.expanduser(path)
            path = os.path.normpath(path)

            if not os.path.isdir(path):
                print("Invalid directory!\n")
                continue

            logging.debug(f'setup first time index at {path}')
            create_index(path)
            break

def prompt_continuation(width, line_number, wrap_count):
    if wrap_count > 0:
        return " " * (width - 3) + "-> "
    else:
        text = "...: ".rjust(width)
        return HTML("<ansigray>%s</ansigray>") % text

def converse():
    _print_logo()
    messages = []

    if not _validate():
        _setup()

    history = InMemoryHistory()
    while True:
        try:
            query = prompt(
                HTML("<ansimagenta>codetalk> </ansimagenta>"),
                history=history,
                prompt_continuation=prompt_continuation
            )

        except EOFError:
            return
        except KeyboardInterrupt:
            print()
            continue
        if is_chat_command(query, messages):
            continue

        logging.info(f"Handling user query: \"{query}\"")
        response = get_response(query, messages)
        if not response or response == "__KEYBOARD_INTERRUPT":
            continue

        messages.append({'role': 'user', 'content': query})
        messages.append({'role': 'assistant', 'content': response})
        print("\n", format_output(response), "\n", sep='')

        msg_size = len(''.join(m['content'] for m in messages))
        logging.info(f"Query completed. message stack is {len(messages)} messages and {msg_size} bytes")

if __name__ == '__main__':
    converse()
