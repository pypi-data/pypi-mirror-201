#!/usr/bin/python3
# -*- coding: utf-8 -*-

import shutil

from slpkg.configs import Configs


class Ascii(Configs):
    """ ascii characters. """
    def __init__(self):
        super(Configs, self).__init__()
        self.color = self.colour()
        self.columns, self.rows = shutil.get_terminal_size()

        self.vertical_line: str = '|'
        self.horizontal_line: str = '='
        self.horizontal_vertical: str = '+'
        self.upper_right_corner: str = '+'
        self.lower_left_corner: str = '+'
        self.lower_right_corner: str = '+'
        self.upper_left_corner: str = '+'
        self.horizontal_and_up: str = '+'
        self.horizontal_and_down: str = '+'
        self.vertical_and_right: str = '+'
        self.vertical_and_left: str = '+'

        if self.ascii_characters:
            self.vertical_line: str = '│'
            self.horizontal_line: str = '─'
            self.horizontal_vertical: str = '┼'
            self.upper_right_corner: str = '┐'
            self.lower_left_corner: str = '└'
            self.lower_right_corner: str = '┘'
            self.upper_left_corner: str = '┌'
            self.horizontal_and_up: str = '┴'
            self.horizontal_and_down: str = '┬'
            self.vertical_and_right: str = '├'
            self.vertical_and_left: str = '┤'

        self.bold: str = self.color['bold']
        self.blue: str = self.color['blue']
        self.green: str = self.color['green']
        self.cyan: str = self.color['cyan']
        self.red: str = self.color['red']
        self.yellow: str = self.color['yellow']
        self.violet: str = self.color['violet']
        self.endc: str = self.color['endc']
        self.bgreen: str = f'{self.bold}{self.green}'
        self.bred: str = f'{self.bold}{self.red}'

    def draw_package_title_box(self, message: str, title: str) -> None:
        """ Drawing package title box. """
        middle_title: int = int((self.columns / 2) - len(title) + 10)

        print(f'{self.bgreen}{self.upper_left_corner}' + f'{self.horizontal_line}' * (self.columns - 2) +
              f'{self.upper_right_corner}')

        print(f'{self.vertical_line}' + ' ' * middle_title + f'{title}' + ' ' *
              (self.columns - middle_title - len(title) - 2) + f'{self.vertical_line}')

        self.draw_middle_line()

        print(f'{self.vertical_line}{self.endc} {message}' + ' ' * (self.columns - len(message) - 3) +
              f'{self.bgreen}{self.vertical_line}')

        self.draw_middle_line()

        print(f'{self.bgreen}{self.vertical_line}{self.endc} Package:' + ' ' * 22 + 'Version:' +
              ' ' * (self.columns - 65) + 'Size:' + ' ' * 13 + f'Repo:{self.bgreen} {self.vertical_line}{self.endc}')

    def draw_view_package(self, package: str, version: str, size: str, color: str, repo: str) -> None:
        """ Draw nad print the packages. """
        if self.columns <= 80 and len(version) >= 11:
            version: str = f'{version[:10]}...'
        if self.columns <= 80 and len(package) >= 25:
            package: str = f'{package[:24]}...'
        print(f'{self.bgreen}{self.vertical_line} {self.bold}{color}{package}{self.endc}' + ' ' * (30 - len(package)) +
              f'{self.bgreen}{version}' + ' ' * ((self.columns - 53) - len(version) - len(size)) +
              f'{self.endc}{size}' + ' ' * (19 - len(repo)) +
              f'{self.blue}{repo} {self.bgreen}{self.vertical_line}{self.endc}')

    def draw_log_package(self, package: str) -> None:
        """ Drawing and print logs packages. """
        print(f'  {self.lower_left_corner}{self.horizontal_line}{self.cyan} {package}{self.endc}\n')

    def draw_middle_line(self) -> None:
        """ Drawing a middle line. """
        print(f'{self.bgreen}{self.vertical_and_right}' + f'{self.horizontal_line}' *
              (self.columns - 2) + f'{self.vertical_and_left}')

    def draw_dependency_line(self) -> None:
        """ Drawing  the dependencies line. """
        print(f'{self.bgreen}{self.vertical_line}{self.endc} Dependencies:' + ' ' * (self.columns - 16) +
              f'{self.bgreen}{self.vertical_line}{self.endc}')

    def draw_bottom_line(self) -> None:
        """ Drawing the bottom line. """
        print(f'{self.bold}{self.green}{self.lower_left_corner}' + f'{self.horizontal_line}' *
              (self.columns - 2) + f'{self.lower_right_corner}{self.endc}')

    def draw_checksum_error_box(self, name: str, checksum: str, file_check: str) -> None:
        """ Drawing checksum error box. """
        print('\n' + self.bred + self.upper_left_corner + self.horizontal_line * (self.columns - 2) +
              self.upper_right_corner)

        print(f"{self.bred}{self.vertical_line}{self.bred} Error:{self.endc} MD5SUM check for "
              f"'{self.cyan}{name}'{self.red} FAILED!" + ' ' * (self.columns - (len(name)) - 37) + self.vertical_line)

        print(self.bred + self.vertical_and_right + self.horizontal_line * (self.columns - 2) + self.vertical_and_left)

        print(f'{self.bred}{self.vertical_line}{self.yellow} Expected:{self.endc} {checksum}{self.bred}'
              + ' ' * (self.columns - (len(checksum)) - 13) + self.vertical_line)

        print(f'{self.bred}{self.vertical_line}{self.violet} Found:{self.endc} {file_check}{self.bred}'
              + ' ' * (self.columns - (len(file_check)) - 10) + self.vertical_line)

        print(self.bred + self.lower_left_corner + self.horizontal_line * (self.columns - 2) +
              self.lower_right_corner + self.endc)
