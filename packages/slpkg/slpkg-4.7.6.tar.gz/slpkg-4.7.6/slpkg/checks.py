#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pathlib import Path

from slpkg.configs import Configs
from slpkg.blacklist import Blacklist
from slpkg.utilities import Utilities
from slpkg.sbos.queries import SBoQueries
from slpkg.repositories import Repositories
from slpkg.binaries.queries import BinQueries
from slpkg.models.models import session as Session

from slpkg.models.models import SBoTable, PonceTable, BinariesTable


class Check(Configs):
    """ Some checks before proceed. """

    def __init__(self, flags: list):
        super(Configs, self).__init__()
        self.flags: list = flags
        self.black = Blacklist()
        self.utils = Utilities()
        self.repos = Repositories()

        self.session = Session
        self.flag_bin_repository: list = ['-B', '--bin-repo=']

        if self.utils.is_option(self.flag_bin_repository, self.flags):
            self.repo_table = BinariesTable
        else:
            self.repo_table = SBoTable
            if self.repos.ponce_repo:
                self.repo_table = PonceTable

    def exists_in_the_database(self, packages: list, repo=None) -> None:
        """ Checking if the slackbuild exists in the database. """
        not_packages: list = []

        for pkg in packages:

            if self.utils.is_option(self.flag_bin_repository, self.flags):
                if not BinQueries(pkg, repo).package_name() and pkg != '*':
                    not_packages.append(pkg)

            elif not SBoQueries(pkg).slackbuild() and pkg != '*':
                not_packages.append(pkg)

        if not_packages:
            self.utils.raise_error_message(f"Packages '{', '.join(not_packages)}' does not exists")

    def is_package_unsupported(self, slackbuilds: list) -> None:
        """ Checking for unsupported slackbuilds. """
        for sbo in slackbuilds:
            if sbo != '*':
                sources = SBoQueries(sbo).sources()

                if 'UNSUPPORTED' in sources:
                    self.utils.raise_error_message(f"Package '{sbo}' unsupported by arch")

    def is_installed(self, packages: list) -> None:
        """ Checking for installed packages. """
        not_found = []

        for pkg in packages:
            package: str = self.utils.is_package_installed(pkg)
            if not package:
                not_found.append(pkg)

        if not_found:
            self.utils.raise_error_message(f'Not found \'{", ".join(not_found)}\' installed packages')

    def is_blacklist(self, package: list) -> None:
        """ Checking if the packages are blacklisted. """
        blacklist: list = []

        for pkg in package:
            if pkg in self.black.packages():
                blacklist.append(pkg)

        if blacklist:
            self.utils.raise_error_message(f"The packages '{', '.join(blacklist)}' is blacklisted")

    def is_empty_database(self) -> None:
        """ Checking for empty table and database file. """
        db = Path(self.db_path, self.database_name)
        if not self.session.query(self.repo_table).first() or not db.is_file():
            self.utils.raise_error_message("You need to update the package lists first, run:\n\n"
                                           "              $ 'slpkg update'\n"
                                           "              $ 'slpkg update --bin-repo='*' for binaries")
