#!/usr/bin/python3
# -*- coding: utf-8 -*-

from slpkg.configs import Configs
from slpkg.views.ascii import Ascii
from slpkg.utilities import Utilities
from slpkg.sbos.queries import SBoQueries
from slpkg.sbos.dependencies import Requires
from slpkg.binaries.required import Required
from slpkg.binaries.queries import BinQueries


class Tracking(Configs):
    """ Tracking of the package dependencies. """

    def __init__(self, flags: list):
        super(Configs, self).__init__()
        self.flags: list = flags

        self.ascii = Ascii()
        self.color = self.colour()
        self.utils = Utilities()

        self.llc: str = self.ascii.lower_left_corner
        self.hl: str = self.ascii.horizontal_line
        self.vl: str = self.ascii.vertical_line
        self.cyan: str = self.color['cyan']
        self.grey: str = self.color['grey']
        self.yellow: str = self.color['yellow']
        self.endc: str = self.color['endc']
        self.flag_pkg_version: list = ['-p', '--pkg-version']
        self.flag_bin_repository: list = ['-B', '--bin-repo=']

    def packages(self, packages: list, repo: str) -> None:
        """ Prints the packages dependencies. """
        print(f"The list below shows the packages '{', '.join([p for p in packages])}' with dependencies:\n")

        packages: list = self.utils.apply_package_pattern(self.flags, packages, repo)

        char: str = f' {self.llc}{self.hl}'
        sp: str = ' ' * 4

        for package in packages:
            pkg = f'{self.yellow}{package}{self.endc}'

            if self.utils.is_option(self.flag_pkg_version, self.flags):

                version: str = SBoQueries(package).version()
                if self.utils.is_option(self.flag_bin_repository, self.flags):
                    version: str = BinQueries(package, repo).version()

                pkg = f'{self.yellow}{package} {version}{self.endc}'

            if self.utils.is_option(self.flag_bin_repository, self.flags):
                requires: list = Required(package, repo).resolve()
            else:
                requires: list = Requires(package).resolve()

            how_many: int = len(requires)

            print(pkg)
            print(char, end='')

            if not requires:
                print(f' {self.cyan}No dependencies{self.endc}')
            else:
                for i, req in enumerate(requires, start=1):
                    require: str = f'{self.cyan}{req}{self.endc}'

                    if self.utils.is_option(self.flag_pkg_version, self.flags):

                        version: str = f" {self.yellow}{SBoQueries(req).version()}{self.endc}"
                        if self.utils.is_option(self.flag_bin_repository, self.flags):
                            version: str = f" {self.yellow}{BinQueries(req, repo).version()}{self.endc}"

                        require: str = f'{self.cyan}{req}{self.endc}{version}'

                    if i == 1:
                        print(f' {require}')
                    else:
                        print(f'{sp}{require}')

            print(f'\n{self.grey}{how_many} dependencies for {package}{self.endc}\n')
