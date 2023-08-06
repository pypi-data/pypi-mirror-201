import os
import textwrap

from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import TerminalFormatter

def format_output(input_string):
    terminal_width = os.get_terminal_size().columns
    lines = input_string.split('\n')
    formatted_output = []
    in_code_block = False
    code_block_lines = []

    for line in lines:
        if line.startswith("```"):
            if in_code_block:
                in_code_block = False
                block = '\n'.join(code_block_lines)
                try:
                    lexer = get_lexer_by_name(language, stripall=True)
                except:
                    try:
                        lexer = guess_lexer(block)
                    except:
                        lexer = PythonLexer()

                highlighted_code = highlight(block, lexer, TerminalFormatter())
                formatted_output.append(highlighted_code.rstrip('\n'))
                code_block_lines = []

            else:
                in_code_block = True
                language = line.strip("```")

        elif in_code_block:
            code_block_lines.append(line)
        else:
            wrapped_lines = textwrap.fill(line, width=terminal_width)
            formatted_output.extend(wrapped_lines.split("\n"))

    return "\n".join(formatted_output)
