"""
graphical user interface for a typing practice program
"""

import math
import json
import contextlib

with contextlib.redirect_stdout(None):
    import pygame
from typingprogram import TypingProgram


class TypingInterface:
    """graphical interface wrapper class for a typing practice program"""

    def __init__(
        self, program: TypingProgram | None = None, fullscreen: bool = True
    ) -> None:
        pygame.init()
        self.__fullscreen = fullscreen
        self.__constants = {
            "windowed_size": (800, 640),
            "screen_size": None,
            "line_size": None,
            "previous_line_position": None,
            "text_font_size": None,
        }
        self.__load_window_state()
        self.__set_screen()

        self.__clock = pygame.time.Clock()

        self.__load_colours()

        self.__load_fonts()

        if program is None:
            program = TypingProgram()
        self.__program = program

    def __load_window_state(self) -> None:
        """load previous or default window state from file"""
        with open("config/window_state.json", "r", encoding="utf-8") as file:
            window_state = json.loads(file.read())
        self.__constants["windowed_size"] = tuple(window_state["windowed_size"])
        self.__fullscreen = window_state["fullscreen"]

    def __set_screen(self) -> None:
        """set the __screen member to the appropriate pygame display mode"""
        if self.__fullscreen:
            self.__screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
            self.__constants["screen_size"] = self.__screen.get_size()
            self.__calculate_constants()
        else:
            self.__screen = pygame.display.set_mode(
                self.__constants["windowed_size"], pygame.RESIZABLE
            )
            self.__constants["screen_size"] = self.__constants["windowed_size"]
            self.__calculate_constants()
        self.__save_window_state()

    def __toggle_fullscreen(self) -> None:
        """toggle between windowed and fullscreen"""
        if self.__fullscreen:
            self.__fullscreen = False
            self.__set_screen()
        else:
            self.__fullscreen = True
            self.__set_screen()

    def __calculate_constants(self) -> None:
        """calculate the graphical scaling constants"""
        self.__constants["line_size"] = (
            math.floor(self.__constants["screen_size"][0] * 0.75),
            math.floor(self.__constants["screen_size"][0] * 0.075),
        )
        self.__constants["previous_line_position"] = (
            (self.__constants["screen_size"][0] - self.__constants["line_size"][0])
            // 2,
            (self.__constants["screen_size"][1] - 3 * self.__constants["line_size"][1])
            // 2,
        )
        self.__constants["text_font_size"] = self.__constants["screen_size"][1] // 10

    def __load_colours(self) -> None:
        """load colours from colours/config.json"""
        with open("config/colours.json", "r", encoding="utf-8") as file:
            self.__colours = json.loads(file.read())

    def __load_fonts(self) -> None:
        """load fonts"""
        self.__text_font = pygame.font.Font(
            "fonts/Fira_Sans/FiraSans-Regular.ttf", self.__constants["text_font_size"]
        )

    def __save_window_state(self) -> None:
        """save the current window state to a config file"""
        print(self.__fullscreen)
        window_state = {
            "windowed_size": list(self.__constants["windowed_size"]),
            "fullscreen": self.__fullscreen,
        }
        with open("config/window_state.json", "w", encoding="utf-8") as file:
            file.writelines(json.dumps(window_state, indent=4))

    def __stop(self) -> None:
        """stop typing program"""
        self.__program.stop()

    def __handle_events(self) -> None:
        """handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__stop()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.__stop()
                elif event.key == pygame.K_F11:
                    self.__toggle_fullscreen()
            elif event.type == pygame.VIDEORESIZE:
                if not self.__fullscreen:
                    self.__constants["windowed_size"] = pygame.display.get_surface().get_size()
                self.__set_screen()

    def __draw_backgrounds(self) -> None:
        """draw the backrounds for the text lines"""
        self.__screen.fill(self.__colours["background"])

        top_left = self.__constants["previous_line_position"]
        line_size = self.__constants["line_size"]
        line_rect = pygame.Rect(top_left[0], top_left[1], line_size[0], line_size[1])
        corner_radius = line_size[1] // 5

        pygame.draw.rect(
            self.__screen,
            self.__colours["inactive_background"],
            line_rect,
            border_top_left_radius=corner_radius,
            border_top_right_radius=corner_radius,
        )
        line_rect.top += line_size[1]
        pygame.draw.rect(self.__screen, self.__colours["active_background"], line_rect)
        line_rect.top += line_size[1]
        pygame.draw.rect(
            self.__screen,
            self.__colours["inactive_background"],
            line_rect,
            border_bottom_left_radius=corner_radius,
            border_bottom_right_radius=corner_radius,
        )

    def __draw_previous_line(self) -> None:
        """draw the previous line to the screen"""
        line = self.__program.previous_line
        line_surface = self.__text_font.render(
            line, True, self.__colours["inactive_foreground"]
        )
        self.__screen.blit(line_surface, self.__constants[""])

    def __draw_next_line(self) -> None:
        """draw the next line to the screen"""
        line = self.__program.next_line
        line_surface = self.__text_font.render(
            line, True, self.__colours["inactive_foreground"]
        )
        self.__screen.blit(line_surface, self.__constants[""])

    def __draw_current_line(self) -> None:
        """draw the current line to the screen"""
        line = self.__program.current_line

    def __draw(self) -> None:
        """draw the program's state to the screen"""
        self.__draw_backgrounds()
        # if self.__program.cursor[0] > 0:
        #     self.__draw_previous_line()
        # if self.__program.cursor[0] < self.__program.line_count - 1:
        #     self.__draw_next_line()
        # self.__draw_current_line()
        pygame.display.update()

    def run(self) -> None:
        """main loop for running the program"""
        fps = 60
        self.__program.start()
        while self.__program.running:
            self.__handle_events()
            self.__draw()
            self.__clock.tick(fps)
        pygame.quit()
