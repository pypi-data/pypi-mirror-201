#!/usr/bin/python3
# -*- coding: utf-8 -*-

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.sbos.queries import SBoQueries
from slpkg.repositories import Repositories
from slpkg.binaries.queries import BinQueries


class SearchPackage(Configs):
    """ Search packages from the repositories. """

    def __init__(self, flags=None):
        super(Configs, self).__init__()
        self.flags: list = flags

        self.color = self.colour()
        self.utils = Utilities()
        self.repos = Repositories()

        self.yellow: str = self.color['yellow']
        self.cyan: str = self.color['cyan']
        self.green: str = self.color['green']
        self.grey: str = self.color['grey']
        self.endc: str = self.color['endc']

        self.flag_bin_repository: list = ['-B', '--bin-repo=']

    def package(self, packages: list, repo=None) -> None:
        """ Searching and print the matched packages. """
        matching: int = 0
        repository: str = ''

        print(f'The list below shows the repo '
              f'packages that contains \'{", ".join([p for p in packages])}\':\n')

        # Searching for binaries.
        if self.utils.is_option(self.flag_bin_repository, self.flags):
            if repo == '*':
                pkg_repo: tuple = BinQueries('', repo).all_package_names_from_repositories()

                for pkg in packages:
                    for pr in pkg_repo:

                        if pkg in pr[0] or pkg == '*':
                            matching += 1

                            desc: str = BinQueries(pr[0], pr[1]).description()
                            version: str = BinQueries(pr[0], pr[1]).version()

                            if repo == '*':
                                repository: str = f'{pr[1]}: '

                            print(f'{repository}{self.cyan}{pr[0]}{self.endc} {self.yellow}{version}{self.endc}'
                                  f'{self.green}{desc}{self.endc}')
            else:
                pkg_repo: list = BinQueries('', repo).all_package_names_by_repo()

                for pkg in packages:
                    for pr in pkg_repo:

                        if pkg in pr or pkg == '*':
                            matching += 1

                            desc: str = BinQueries(pr, repo).description()
                            version: str = BinQueries(pr, repo).version()

                            print(f'{repository}{self.cyan}{pr}{self.endc} {self.yellow}{version}{self.endc}'
                                  f'{self.green}{desc}{self.endc}')

        else:
            # Searching for slackbuilds.
            names: list = SBoQueries('').sbos()
            for name in names:
                for package in packages:

                    if package in name or package == '*':
                        matching += 1

                        desc: str = SBoQueries(name).description().replace(name, '')
                        version: str = SBoQueries(name).version()

                        print(f'{self.cyan}{name}{self.endc}-{self.yellow}'
                              f'{version}{self.endc}{self.green}{desc}{self.endc}')

        if not matching:
            print('\nDoes not match any package.\n')
        else:
            print(f'\n{self.grey}Total found {matching} packages.{self.endc}')
