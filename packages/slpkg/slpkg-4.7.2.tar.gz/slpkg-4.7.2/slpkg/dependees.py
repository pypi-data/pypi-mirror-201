#!/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import Generator
from slpkg.configs import Configs
from slpkg.views.ascii import Ascii
from slpkg.utilities import Utilities
from slpkg.sbos.queries import SBoQueries
from slpkg.repositories import Repositories
from slpkg.binaries.queries import BinQueries


class Dependees(Configs):
    """ Show which packages depend. """

    def __init__(self, packages: list, flags: list):
        super(Configs, self).__init__()
        self.packages: list = packages
        self.flags: list = flags

        self.ascii = Ascii()
        self.repos = Repositories()
        self.color = self.colour()
        self.utils = Utilities()

        self.llc: str = self.ascii.lower_left_corner
        self.hl: str = self.ascii.horizontal_line
        self.var: str = self.ascii.vertical_and_right
        self.bold: str = self.color['bold']
        self.violet: str = self.color['violet']
        self.cyan: str = self.color['cyan']
        self.grey: str = self.color['grey']
        self.yellow: str = self.color['yellow']
        self.byellow: str = f'{self.bold}{self.yellow}'
        self.endc: str = self.color['endc']
        self.flag_full_reverse: list = ['-E', '--full-reverse']
        self.flag_pkg_version: list = ['-p', '--pkg-version']
        self.flag_bin_repository: list = ['-B', '--bin-repo=']

    def find(self, repo: str) -> None:
        """ Collecting the dependees. """
        print(f"The list below shows the "
              f"packages that dependees on '{', '.join([p for p in self.packages])}':\n")

        self.packages: list = self.utils.apply_package_pattern(self.flags, self.packages, repo)

        for pkg in self.packages:
            dependees: list = list(self.find_requires(pkg, repo))

            package: str = f'{self.byellow}{pkg}{self.endc}'

            if self.utils.is_option(self.flag_pkg_version, self.flags):
                if self.utils.is_option(self.flag_bin_repository, self.flags):
                    version: str = BinQueries(pkg, repo).version()
                else:
                    version: str = SBoQueries(pkg).version()

                package: str = f'{self.byellow}{pkg} {version}{self.endc}'

            print(package)

            print(f' {self.llc}{self.hl}', end='')

            if not dependees:
                print(f'{self.cyan} No dependees{self.endc}')

            sp: str = ' ' * 4
            for i, dep in enumerate(dependees, start=1):
                dependency: str = f'{self.cyan}{dep[0]}{self.endc}'

                if self.utils.is_option(self.flag_pkg_version, self.flags):

                    if self.utils.is_option(self.flag_bin_repository, self.flags):
                        version: str = BinQueries(dep[0], repo).version()
                    else:
                        version: str = SBoQueries(dep[0]).version()

                    dependency: str = (f'{self.cyan}{dep[0]}{self.endc} {self.yellow}'
                                       f'{version}{self.endc}')

                if i == 1:
                    print(f' {dependency}')
                else:
                    print(f'{sp}{dependency}')

                if self.utils.is_option(self.flag_full_reverse, self.flags):
                    if i == len(dependees):
                        print(' ' * 4 + f' {self.llc}{self.hl} {self.violet}{dep[1]}{self.endc}')
                    else:
                        print(' ' * 4 + f' {self.var}{self.hl} {self.violet}{dep[1]}{self.endc}')

            print(f'\n{self.grey}{len(dependees)} dependees for {pkg}{self.endc}\n')

    def find_requires(self, pkg: str, repo) -> Generator[str, None, None]:
        """ Find requires that slackbuild dependees. """
        if self.utils.is_option(self.flag_bin_repository, self.flags):
            requires: list = BinQueries(pkg, repo).all_package_names_with_required()
        else:
            requires: list = SBoQueries('').all_sbo_and_requires()

        for req in requires:
            if [r for r in req[1].split() if r == pkg]:
                yield req
