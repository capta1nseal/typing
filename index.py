#!/usr/bin/python3

"""
pygame program for practicing typing

text is read from a text file with a custom file browser
the program evaluates the user's speed and accuracy while typing
"""

from typinginterface import TypingInterface
from typingprogram import TypingProgram

typing_program = TypingProgram()
typing_interface = TypingInterface(typing_program, False)

typing_interface.run()
