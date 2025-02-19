#!/usr/bin/env python3
"""
Usage: helloworld.py

Hello world example.
"""


def do_helloworld():
    """Generate the hello world message"""
    # create a string with the message
    output = "Hola mundo!"
    return output


def run():
    """Script entrypoint"""
    # just print to console
    print(do_helloworld())


if __name__ == "__main__":
    run()
