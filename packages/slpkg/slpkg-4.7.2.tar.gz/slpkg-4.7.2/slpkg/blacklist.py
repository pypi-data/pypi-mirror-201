#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tomli
from pathlib import Path

from slpkg.configs import Configs
from slpkg.models.models import session as Session


class Blacklist(Configs):
    """ Reads and returns the blacklist. """

    def __init__(self):
        super(Configs, self).__init__()
        self.session = Session

        self.color = self.colour()
        self.bold: str = self.color['bold']
        self.red: str = self.color['red']
        self.cyan: str = self.color['cyan']
        self.endc: str = self.color['endc']
        self.bred: str = f'{self.bold}{self.red}'
        self.blacklist_file_toml = Path(self.etc_path, 'blacklist.toml')

    def packages(self) -> list:
        """ Reads the blacklist file. """

        if self.blacklist_file_toml.is_file():
            try:
                with open(self.blacklist_file_toml, 'rb') as black:
                    return tomli.load(black)['BLACKLIST']['PACKAGES']
            except (tomli.TOMLDecodeError, KeyError) as error:
                raise SystemExit(f"\n{self.prog_name} {self.bred}Error{self.endc}: {error}: in the configuration file "
                                 f"'{self.blacklist_file_toml}'.\n"
                                 f"\nIf you have upgraded the '{self.prog_name}' probably you need to run:\n"
                                 f"'mv {self.blacklist_file_toml}.new {self.blacklist_file_toml}'.\n"
                                 f"or '{self.cyan}slpkg_new-configs{self.endc}' command.\n")
        return []
