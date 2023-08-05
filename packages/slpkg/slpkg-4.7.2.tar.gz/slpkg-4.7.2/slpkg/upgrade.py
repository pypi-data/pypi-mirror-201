#!/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import Generator
from packaging.version import parse

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.sbos.queries import SBoQueries
from slpkg.binaries.queries import BinQueries


class Upgrade(Configs):
    """ Upgrade the installed packages. """

    def __init__(self, flags: list, repo=None):
        super(Configs, self).__init__()
        self.flags: list = flags
        self.repo: str = repo
        self.utils = Utilities()

        self.flag_bin_repository: list = ['-B=', '--bin-repo=']
        self.all_installed: list = self.utils.installed_packages

    def packages(self) -> Generator[str, None, None]:
        """ Compares version of packages and returns the maximum. """
        if self.utils.is_option(self.flag_bin_repository, self.flags):
            repo_packages: list = BinQueries('', self.repo).all_package_names_by_repo()
        else:
            repo_packages: list = SBoQueries('').sbos()

        for pkg in self.all_installed:
            inst_package: str = self.utils.split_binary_pkg(pkg)[0]

            if inst_package in repo_packages:

                if self.is_package_upgradeable(inst_package):
                    yield inst_package

    def is_package_upgradeable(self, name: str) -> bool:
        """ Checks for installed and upgradeable packages. """
        repo_version = repo_build = '0'
        inst_version = inst_build = '0'
        inst_package: str = self.utils.is_package_installed(name)

        if inst_package:
            inst_version: str = self.utils.split_binary_pkg(inst_package)[1]
            inst_build: str = self.utils.split_binary_pkg(inst_package)[3]

            if self.utils.is_option(self.flag_bin_repository, self.flags):
                repo_package: str = BinQueries(name, self.repo).package_bin()
                repo_version: str = BinQueries(name, self.repo).version()
                repo_build: str = self.utils.split_binary_pkg(repo_package)[3]
            else:
                repo_version: str = SBoQueries(name).version()
                repo_build: str = self.utils.read_sbo_build_tag(name)

        return parse(f'{repo_version}{repo_build}') > parse(f'{inst_version}{inst_build}')
