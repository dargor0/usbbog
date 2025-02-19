#!/usr/bin/env python3
"""
Usage: helloworld_test.py

unit testing example of hello world.
"""

import helloworld


def test():
    """Unit test for do_helloworld function"""
    # run the function to test and recover its output
    check_output = helloworld.do_helloworld()
    # verify the output
    if check_output == "Hello world!":
        print("Test is OK")
    else:
        print('Test is not OK! expected a "Hello world!"')
        print(f'  but received {check_output}')


if __name__ == "__main__":
    test()
