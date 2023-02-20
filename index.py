#!/usr/bin/python3

"""
pygame program for practicing typing

text is read from a text file with a custom file browser
(planned: the program evaluates the user's speed and accuracy while typing)
"""

from typinginterface import TypingInterface


if __name__ == "__main__":
    typing_interface = TypingInterface()

    typing_interface.run()
