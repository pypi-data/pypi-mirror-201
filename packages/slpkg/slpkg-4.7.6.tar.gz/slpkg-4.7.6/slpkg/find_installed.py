#!/usr/bin/python3
# -*- coding: utf-8 -*-

from slpkg.configs import Configs
from slpkg.utilities import Utilities


class FindInstalled(Configs):
    """ Find installed packages. """

    def __init__(self):
        super(Configs, self).__init__()

        self.color = self.colour()
        self.utils = Utilities()

        self.yellow: str = self.color['yellow']
        self.cyan: str = self.color['cyan']
        self.green: str = self.color['green']
        self.blue: str = self.color['blue']
        self.endc: str = self.color['endc']
        self.grey: str = self.color['grey']

        self.installed: list = self.utils.installed_packages

    def find(self, packages: list) -> None:
        """ Find the packages. """
        matching: list = []

        print(f'The list below shows the installed packages '
              f'that contains \'{", ".join([p for p in packages])}\' files:\n')

        for pkg in packages:
            for package in self.installed:
                if pkg in package or pkg == '*':
                    matching.append(package)

        self.matched(matching)

    def matched(self, matching: list) -> None:
        """ Print the matched packages. """
        if matching:
            for package in matching:
                print(f'{self.cyan}{package}{self.endc}')
            print(f'\n{self.grey}Total found {len(matching)} packages.{self.endc}')
        else:
            print('\nDoes not match any package.\n')
