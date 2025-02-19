#!/usr/bin/env python3
"""
Usage: helloworld_test.py

unit testing example of hello world.
"""

import helloworld
import unittest

class TestStringMethods(unittest.TestCase):
    def test_1(self):
        self.assertEqual(
            helloworld.do_helloworld("Juan"), 
            "Hello Juan, how are you?")
            
    def test_2(self):
        self.assertEqual(
            helloworld.do_helloworld("Maria"), 
            "Hello Maria, how are you?")
            
    def test_3(self):
        self.assertEqual(
            helloworld.do_helloworld("Armando"), 
            "Hello Armando, how are you?")
            
    def test_4(self):
        self.assertEqual(
            helloworld.do_helloworld(10), 
            "Hello 10, how are you?")
            
    def test_5(self):
        self.assertEqual(
            helloworld.do_helloworld(""), 
            "Hello Stranger, how are you?")



if __name__ == "__main__":
    unittest.main()
