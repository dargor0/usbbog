#!/usr/bin/env python3

"""
Exercise 01: Basic calculator

This is an example of how to use basic instructions in python

Author: Oscar Diaz <odiaz@ieee.org>
Date: 2025-02-20
"""

def run():
    """script entrypoint"""

    ### PLEASE put your code starting from here

    # get the operands from the user
    operand_a = int(input("Enter the first operand: "))
    operand_b = int(input("Enter the second operand: "))

    # execute operation
    result = operand_a + operand_b

    # print the result
    print(f"The sum of {operand_a} and {operand_b} is {result}")

    ### HERE YOUR CODE ENDS

if __name__ == "__main__":
    run()
