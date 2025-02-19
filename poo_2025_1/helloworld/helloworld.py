#!/usr/bin/env python3
"""
Usage: helloworld.py

Hello world example.
"""


def do_helloworld(name):
    """Generate the hello world message"""
    # create a string with the message
    if name == "":
        output = "Hello Stranger, how are you?"
    else:
        output = f"Hello {name}, how are you?"
    return output


def run():
    """Script entrypoint"""
    # just print to console
    print(do_helloworld("Oscar"))


if __name__ == "__main__":
    run()
