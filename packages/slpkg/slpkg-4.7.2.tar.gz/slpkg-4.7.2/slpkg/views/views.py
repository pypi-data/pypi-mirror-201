#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from typing import Any
from pathlib import Path

from slpkg.configs import Configs
from slpkg.upgrade import Upgrade
from slpkg.views.ascii import Ascii
from slpkg.utilities import Utilities
from slpkg.dialog_box import DialogBox
from slpkg.sbos.queries import SBoQueries
from slpkg.repositories import Repositories
from slpkg.binaries.queries import BinQueries
from slpkg.models.models import LogsDependencies
from slpkg.models.models import session as Session


class ViewMessage(Configs):
    """ Print some messages before. """

    def __init__(self, flags: list, repo=None):
        super(Configs, self).__init__()
        self.flags: list = flags
        self.repo: str = repo

        self.session = Session
        self.utils = Utilities()
        self.dialogbox = DialogBox()
        self.ascii = Ascii()
        self.upgrade = Upgrade(self.flags, self.repo)
        self.color = self.colour()
        self.repos = Repositories()

        self.yellow: str = self.color['yellow']
        self.cyan: str = self.color['cyan']
        self.red: str = self.color['red']
        self.grey: str = self.color['grey']
        self.violet: str = self.color['violet']
        self.endc: str = self.color['endc']
        self.download_only = self.tmp_slpkg
        self.installed_packages: list = []
        self.flag_resolve_off: list = ['-o', '--resolve-off']
        self.flag_reinstall: list = ['-r', '--reinstall']
        self.flag_yes: list = ['-y', '--yes']
        self.flag_bin_repository: list = ['-B', '--bin-repo=']

    def view_packages(self, package: str, mode: str) -> None:
        """ Printing the main packages. """
        size: str = ''
        color: str = self.red

        if self.utils.is_option(self.flag_bin_repository, self.flags):
            version: str = BinQueries(package, self.repo).version()
            size: str = BinQueries(package, self.repo).size_comp()
            repo = BinQueries(package, self.repo).repository()
        else:
            version: str = SBoQueries(package).version()
            repo: str = SBoQueries('').repo_name()

        if mode in ['install', 'download']:
            color: str = self.cyan
        if mode == 'build':
            color: str = self.yellow
        if mode == 'upgrade':
            color: str = self.violet

        # If the package is installed and change the color to gray.
        if package in self.utils.installed_package_names and mode == 'install':
            color = self.grey

        self.ascii.draw_view_package(package, version, size, color, repo)

    def view_skipping_packages(self, package: str, version: str) -> None:
        """ Print the skipping packages. """
        print(f'[{self.yellow}Skipping{self.endc}] {package}-{version} {self.red}(already installed){self.endc}')

    def build_packages(self, slackbuilds: list, dependencies: list) -> None:
        """ View packages for build only. """
        self.ascii.draw_package_title_box('The following packages will be build:', 'Build Packages')

        for sbo in slackbuilds:
            self.view_packages(sbo, mode='build')

        if dependencies:
            self.ascii.draw_middle_line()
            self.ascii.draw_dependency_line()

            for sbo in dependencies:
                self.view_packages(sbo, mode='build')

        self.summary(slackbuilds, dependencies, option='build')

    def install_packages(self, packages: list, dependencies: list, mode: str) -> None:
        """ View packages for install. """
        if dependencies is None:
            dependencies: list = []

        title: str = 'Slpkg Install Packages'
        if mode == 'upgrade':
            title: str = 'Slpkg Upgrade Packages'

        self.ascii.draw_package_title_box('The following packages will be installed or upgraded:', title)

        for pkg in packages:
            self.view_packages(pkg, mode)

        if dependencies:
            self.ascii.draw_middle_line()
            self.ascii.draw_dependency_line()

            for pkg in dependencies:
                self.view_packages(pkg, mode)

        self.summary(packages, dependencies, option=mode)

    def download_packages(self, slackbuilds: list, directory: Path) -> None:
        """ View downloaded packages. """
        mode = 'download'

        self.ascii.draw_package_title_box('The following packages will be downloaded:', 'Slpkg Download Packages')

        if directory:
            self.download_only: Path = directory

        for sbo in slackbuilds:
            self.view_packages(sbo, mode)

        self.summary(slackbuilds, dependencies=[], option='download')

    def remove_packages(self, packages: list) -> Any:
        """ View remove packages. """
        pkgs, dependencies = [], []

        for pkg in packages:
            pkgs.append(pkg)

            requires = self.session.query(
                LogsDependencies.requires).filter(
                    LogsDependencies.name == pkg).first()

            if requires:
                dependencies += requires[0].split()

        if dependencies and not self.utils.is_option(self.flag_resolve_off, self.flags):
            dependencies: list = self.choose_dependencies_for_remove(list(set(dependencies)))

        self.ascii.draw_package_title_box('The following packages will be removed:', 'Slpkg Remove Packages')

        for pkg in pkgs:
            if pkg not in dependencies:
                self._view_removed(pkg)

        if dependencies and not self.utils.is_option(self.flag_resolve_off, self.flags):
            self.ascii.draw_middle_line()
            self.ascii.draw_dependency_line()

            for pkg in dependencies:
                self._view_removed(pkg)
        else:
            dependencies: list = []

        self.summary(pkgs, dependencies, option='remove')

        return self.installed_packages, dependencies

    def _view_removed(self, name: str) -> None:
        """ View and creates list with packages for remove. """
        installed = self.utils.is_package_installed(name)

        if installed:
            pkg: list = self.utils.split_binary_pkg(installed)
            self.installed_packages.append(installed)
            size: str = self.utils.get_file_size(f'{self.log_packages}/{installed}')
            self.ascii.draw_view_package(pkg[0], pkg[1], size, self.red, '')

    def choose_dependencies_for_remove(self, dependencies: list) -> list:
        """ Choose packages for remove using the dialog box. """
        height: int = 10
        width: int = 70
        list_height: int = 0
        choices: list = []
        title: str = " Choose dependencies you want to remove "

        for package in dependencies:
            repo_ver: str = SBoQueries(package).version()
            inst_pkg: str = self.utils.is_package_installed(package)
            choices += [(package, repo_ver, True, f'Package: {inst_pkg}')]

        text: str = f'There are {len(choices)} dependencies:'

        code, tags = self.dialogbox.checklist(text, dependencies, title, height,
                                              width, list_height, choices)

        if not code:
            return dependencies

        os.system('clear')
        return tags

    def summary(self, packages: list, dependencies: list, option: str) -> None:
        """ View the status of the packages action. """
        packages.extend(dependencies)
        install = upgrade = remove = 0
        reinstall: bool = self.utils.is_option(self.flag_reinstall, self.flags)

        for pkg in packages:

            upgradeable: bool = False
            if option != 'remove':
                upgradeable: bool = self.upgrade.is_package_upgradeable(pkg)

            installed: str = self.utils.is_package_installed(pkg)

            if not installed:
                install += 1
            elif installed and reinstall:
                upgrade += 1
            elif installed and upgradeable and reinstall:
                upgrade += 1
            elif installed and upgradeable:
                upgrade += 1
            elif installed and option == 'remove':
                remove += 1

        self.ascii.draw_bottom_line()

        if option in ['install', 'upgrade']:
            print(f'{self.grey}Total {install} packages will be '
                  f'installed and {upgrade} will be upgraded.{self.endc}')

        elif option == 'build':
            print(f'{self.grey}Total {len(packages)} packages '
                  f'will be build in {self.tmp_path} folder.{self.endc}')

        elif option == 'remove':
            print(f'{self.grey}Total {remove} packages '
                  f'will be removed.{self.endc}')

        elif option == 'download':
            print(f'{self.grey}{len(packages)} packages '
                  f'will be downloaded in {self.download_only} folder.{self.endc}')

    def logs_packages(self, dependencies: list) -> None:
        """ View the logging packages. """
        print('The following logs will be removed:\n')

        for dep in dependencies:
            print(f'{self.yellow}{dep[0]}{self.endc}')
            self.ascii.draw_log_package(dep[1])

        print('Note: After cleaning you should remove them one by one.')

    def question(self) -> None:
        """ Manage to proceed. """
        if not self.utils.is_option(self.flag_yes, self.flags) and self.ask_question:
            answer: str = input('\nDo you want to continue? [y/N] ')
            if answer not in ['Y', 'y']:
                raise SystemExit()
        print()
