import os
import random

from fontmanager import FontManager
class TypingProgram:
    """
    program for practicing typing

    this class just contains the back-end and requires a user interface
    """

    def __init__(self, font_manager: FontManager) -> None:
        self.__font_manager = font_manager

        self.__cursor = (0, 0)  # (row_index, column_index)
        self.__running = False

    def start(self) -> None:
        """start program"""
        self.__running = True

    def stop(self) -> None:
        """stop program"""
        self.__running = False

    def load_file(
        self, path: str | None = None, default_folder_path: str = "samples"
    ) -> None:
        """load in a text file"""
        if path is None:
            sample_names = [
                os.path.join(default_folder_path, path)
                for path in os.listdir(default_folder_path)
                if os.path.isfile(os.path.join(default_folder_path, path))
            ]
            if sample_names == []:
                self.__text = [""]
                return
            path = str(random.sample(sample_names, 1)[0])

        if not os.path.isfile(path):
            raise ValueError(f"no file at path {path}")

        with open(path, "r", encoding="utf-8") as file:
            self.__text = [row.strip() for row in file]

    def __move_cursor_forwards(self) -> bool:
        """
        moves the cursor forwards by one character
        increment the line if EOL reached
        return True if EOF reached
        all other cases return False
        """
        if self.__cursor[1] == len(self.__text[self.__cursor[0]]):
            if self.__cursor[0] == len(self.__text):
                return True
            self.__cursor = (self.__cursor[0] + 1, 0)
            return False
        self.__cursor = (self.__cursor[0], self.__cursor[1] + 1)
        return False

    def __read_cursor(self) -> str:
        """returns the character after cursor"""
        if self.__cursor[1] == len(self.__text[self.__cursor[0]]):
            return "\n"
        return self.__text[self.__cursor[0]][self.__cursor[1]]

    def next_character(self, character: str) -> bool:
        """move the cursor forwards and return whether the character is correct"""
        if character == self.__read_cursor():
            self.__move_cursor_forwards()
            return True
        self.__move_cursor_forwards()
        return False

    @property
    def previous_line(self) -> str:
        """previous line"""
        return self.__text[self.__cursor[0] - 1]

    @property
    def next_line(self) -> str:
        """next line"""
        return self.__text[self.__cursor[0] + 1]

    @property
    def current_line(self) -> str:
        """current line"""
        return self.__text[self.__cursor[0]]

    @property
    def cursor(self) -> tuple[int, int]:
        """current cursor property"""
        return self.__cursor

    @property
    def line_count(self) -> int:
        """total line count property"""
        return len(self.__text)

    @property
    def running(self) -> bool:
        """running property"""
        return self.__running
