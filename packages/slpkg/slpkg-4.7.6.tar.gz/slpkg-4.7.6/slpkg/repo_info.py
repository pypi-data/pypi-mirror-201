#!/usr/bin/python3
# -*- coding: utf-8 -*-

import shutil

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.sbos.queries import SBoQueries
from slpkg.repositories import Repositories
from slpkg.binaries.queries import BinQueries
from slpkg.models.models import LastRepoUpdated
from slpkg.models.models import session as Session


class RepoInfo(Configs):

    def __init__(self):
        super(Configs, self).__init__()

        self.utils = Utilities()
        self.repos = Repositories()
        self.color = self.colour()
        self.columns, self.rows = shutil.get_terminal_size()
        self.session = Session

        self.bold: str = self.color['bold']
        self.green: str = self.color['green']
        self.red: str = self.color['red']
        self.cyan: str = self.color['cyan']
        self.grey: str = self.color['grey']
        self.yellow: str = self.color['yellow']
        self.byellow: str = f'{self.bold}{self.yellow}'
        self.endc: str = self.color['endc']

    def info(self):
        """ Prints information about repositories. """
        total_packages: int = 0
        enabled: int = 0

        print('Repositories Information:')
        print('=' * self.columns)
        print(f"{'Name:':<18}{'Status:':<15}{'Last Updated:':<35}{'Packages:':>12}")
        print('=' * self.columns)

        for repo, value in self.repos.repositories.items():
            count: int = 0
            status: str = 'Disabled'
            color: str = self.red

            if value[0]:
                enabled += 1
                status: str = 'Enabled'
                color: str = self.green

            last: str = self.session.query(
                LastRepoUpdated.date).where(
                LastRepoUpdated.repo == repo).first()

            if last is None:
                last: tuple = ('',)

            if value[0]:
                if repo in [self.repos.sbo_repo_name, self.repos.ponce_repo_name]:
                    count = int(SBoQueries('').count_packages())
                else:
                    count = int(BinQueries('', repo).count_packages())

            total_packages += count

            print(f"{self.cyan}{repo:<18}{self.endc}{color}{status:<15}{self.endc}{last[0]:<35}"
                  f"{self.yellow}{count:>12}{self.endc}")

        print('=' * self.columns)
        print(f"{self.grey}Total of {enabled}/{len(self.repos.repositories)} "
              f"repositories are enabled with {total_packages} packages available.\n")
