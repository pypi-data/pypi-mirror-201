import argparse
import logging
import os

from . import logconf
from .asset import get_version, print_logo
from .backend import check_for_updates, create_index, get_response, validate_token
from .config import get_config, set_config
from .subcommand import is_chat_command, list_projects

from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, PathCompleter
from prompt_toolkit.document import Document
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import InMemoryHistory

class CustomPathCompleter(Completer):
    def get_completions(self, document, complete_event):
        text_before_cursor = document.text_before_cursor.lstrip()
        words = text_before_cursor.split()

        if len(words) > 1 and words[0] in ['delete', 'use', 'index']:
            path = words[-1]
            path_completer = PathCompleter(expanduser=True)
            path_doc = Document(text=path, cursor_position=len(path))
            for completion in path_completer.get_completions(path_doc, complete_event):
                yield completion

def _validate():
    fields = ['current_project', 'user_token']
    return all(get_config(f) for f in fields)

def _setup():
    if not get_config('user_token'):
        while True:
            token = input("Please input your user token: ").strip()
            if validate_token(token):
                set_config("user_token", token)
                break
            else:
                print("Invalid token! Please try again or go to codetalk.ai to obtain a token.\n")

    if not get_config('current_project'):
        while True:
            try:
                path = prompt("Which directory would you like to use with Codetalk?\n> ",
                  completer=PathCompleter(expanduser=True, only_directories=True)).strip()
            except EOFError:
                exit()

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
    print_logo()
    messages = []

    if not _validate():
        _setup()
    list_projects(truncate=True)
    print("Type `help` to see a list of commands.\n")

    history = InMemoryHistory()
    path_completer = CustomPathCompleter()
    while True:
        try:
            query = prompt(
                HTML("<ansimagenta>codetalk> </ansimagenta>"),
                history=history,
                prompt_continuation=prompt_continuation,
                completer=path_completer,
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
        print('\n')

        msg_size = len(''.join(m['content'] for m in messages))
        logging.info(f"Query completed. message stack is {len(messages)} messages and {msg_size} bytes")

def main():
    parser = argparse.ArgumentParser(description='codetalk')
    parser.add_argument('-v', '--version', action='store_true', help='Display the version information and exit')

    args = parser.parse_args()

    if args.version:
        get_version()
    else:
        check_for_updates()
        converse()

if __name__ == '__main__':
    main()
