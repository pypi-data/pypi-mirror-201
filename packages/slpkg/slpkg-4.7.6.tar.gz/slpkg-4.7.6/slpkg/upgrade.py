#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
from typing import Generator
from packaging.version import parse, InvalidVersion

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.sbos.queries import SBoQueries
from slpkg.binaries.queries import BinQueries
from slpkg.logging_config import LoggingConfig
from slpkg.repositories import Repositories


class Upgrade(Configs):
    """ Upgrade the installed packages. """

    def __init__(self, flags: list, repo=None):
        super(Configs, self).__init__()
        self.flags: list = flags
        self.repo: str = repo
        self.utils = Utilities()
        self.repos = Repositories()

        self.flag_bin_repository: list = ['-B', '--bin-repo=']
        self.repo_for_binaries: bool = self.utils.is_option(self.flag_bin_repository, self.flags)

        self.all_installed: list = self.utils.installed_package_names

        logging.basicConfig(filename=str(LoggingConfig.log_file),
                            filemode='w',
                            encoding='utf-8',
                            level=logging.INFO)

    def packages(self) -> Generator[str, None, None]:
        """ Returns the upgradable packages. """
        if self.utils.is_option(self.flag_bin_repository, self.flags):
            repo_packages: list = list(BinQueries('', self.repo).all_package_names_by_repo())
        else:
            repo_packages: list = list(SBoQueries('').sbos())

        # Compares two lists and get only the installed packages from the repository.
        packages: list = list(set(self.all_installed) & set(repo_packages))

        for pkg in packages:

            if self.is_package_upgradeable(pkg):
                yield pkg

    def is_package_upgradeable(self, name: str) -> bool:
        """ Compares version of packages and returns the maximum. """
        repo_version = repo_build = '0'
        inst_version = inst_build = '0'
        inst_package: str = self.utils.is_package_installed(name)

        repo_tag: str = self.repos.repo_tag
        if self.repo_for_binaries:
            repo_tag: str = self.repos.repositories[self.repo][3]

        if inst_package and inst_package.endswith(repo_tag):
            inst_version: str = self.utils.split_binary_pkg(inst_package)[1]
            inst_build: str = self.utils.split_binary_pkg(inst_package)[3]

            if self.repo_for_binaries and BinQueries(name, self.repo).package_bin():
                repo_package: str = BinQueries(name, self.repo).package_bin()
                repo_version: str = BinQueries(name, self.repo).version()
                repo_build: str = self.utils.split_binary_pkg(repo_package)[3]

            elif not self.repo_for_binaries and SBoQueries(name).slackbuild():
                repo_version: str = SBoQueries(name).version()
                repo_build: str = self.utils.read_sbo_build_tag(name)

        try:
            if parse(repo_version) > parse(inst_version):
                return True

            if parse(repo_version) == parse(inst_version) and parse(repo_build) > parse(inst_build):
                return True
        except InvalidVersion as err:
            logger = logging.getLogger(__name__)
            logger.info('%s: %s: %s: %s', self.__class__.__name__,
                        Upgrade.is_package_upgradeable.__name__,
                        name,
                        err)
            return repo_version > inst_version and repo_build > inst_build

        return False
