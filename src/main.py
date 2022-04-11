#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import global_vars
from interpreter import Interpreter, remove_extension
from colorama import init
from colormanager import ColorManager as CM
from help_message import generate_help_message


def main():
    if set(["-h", "--help"]).intersection(sys.argv):
        _deal_with_help_page()
        return

    init(strip=False)

    interpreter = Interpreter()

    if not global_vars.args.infile:
        sys.exit(interpreter.cmdloop())

    if global_vars.args.color:
        CM().color_on()
    else:
        CM().color_off()

    global_vars.outbase = remove_extension(global_vars.args.infile)

    try:
        interpreter.read_and_write_file()
    except FileNotFoundError:
        print("File does not exist\n")
    # TODO: Uncomment before release
    except Exception as e:
        print(
            f"{CM().BRIGHT}{CM().WHITE}Compilation unsuccessfull{CM().RESET}{CM().RESET_ALL}\n"
        )
        if global_vars.args.show_error_messages:
            raise e
    else:
        print(
            f"{CM().BRIGHT}{CM().WHITE}Compilation successfull{CM().RESET}{CM().RESET_ALL}\n"
        )


def _deal_with_help_page():
    if set(["-C", "--color"]).intersection(sys.argv):
        global_vars.args.color = True
        CM().color_on()
    else:
        global_vars.args.color = False
        CM().color_off()
    print(generate_help_message())


if __name__ == "__main__":
    main()
