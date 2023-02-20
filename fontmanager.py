import os

import contextlib
with contextlib.redirect_stdout(None):
    import pygame

class FontManager:
    """class for rendering with fonts and calculating how many words fit on a line"""

    def __init__(self, font_path: str, font_size: int) -> None:
        pygame.font.init()

        self.__font_path = ""
        self.__font_size = 1

        self.font_path = font_path
        self.font_size = font_size

        self.__load_font()

    def __load_font(self) -> None:
        """load the font"""
        self.__font = pygame.font.Font(self.font_path, self.font_size)

    @property
    def font_path(self) -> str:
        """font path property"""
        return self.__font_path

    @staticmethod
    def __validate_font_path(font_path: str) -> None:
        """validates a font path. no return, raises exception if necessary"""
        if (not isinstance(font_path, str)) or (not font_path[-4:] in (".ttf", ".otf")):
            raise ValueError("invalid path")

        if not os.path.isfile(font_path):
            raise FileNotFoundError("no file found at given path")

    @font_path.setter
    def font_path(self, new_path: str) -> None:
        """
        font path setter
        validates the path then loads new font if valid
        """
        self.__validate_font_path(new_path)

        self.__font_path = new_path

        self.__load_font()

    @property
    def font_size(self) -> int:
        """font size property"""
        return self.__font_size

    @staticmethod
    def __validate_font_size(font_size: int) -> None:
        """validates a font size. no return, raises exception if necessary"""
        if not 0 < font_size:
            raise ValueError("font size must be greater than 0")

    @font_size.setter
    def font_size(self, new_size: int) -> None:
        """
        set new font size
        then recreates the font
        """
        self.__validate_font_size(new_size)

        self.__font_size = new_size

        self.__load_font()

    @property
    def font(self) -> pygame.font.Font:
        """font object property"""
        return self.__font

    @font.setter
    def font(self, new_font: tuple[str, int]) -> None:
        """set new font path and size"""
        new_path, new_size = new_font
        self.__validate_font_path(new_path)
        self.__validate_font_size(new_size)
