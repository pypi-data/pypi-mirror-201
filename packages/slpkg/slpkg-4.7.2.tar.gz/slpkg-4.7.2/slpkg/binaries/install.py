#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
import subprocess
from multiprocessing import Process

from slpkg.configs import Configs
from slpkg.checksum import Md5sum
from slpkg.upgrade import Upgrade
from slpkg.utilities import Utilities
from slpkg.dialog_box import DialogBox
from slpkg.downloader import Downloader
from slpkg.views.views import ViewMessage
from slpkg.progress_bar import ProgressBar
from slpkg.repositories import Repositories
from slpkg.binaries.required import Required
from slpkg.binaries.queries import BinQueries
from slpkg.models.models import LogsDependencies
from slpkg.models.models import session as Session


class Packages(Configs):

    def __init__(self, packages: list, flags: list, repo: str, mode: str):
        super(Configs, self).__init__()
        self.packages: list = packages
        self.flags: list = flags
        self.repo: str = repo
        self.mode: str = mode

        self.progress = ProgressBar()
        self.color = self.colour()
        self.utils = Utilities()
        self.repos = Repositories()
        self.dialogbox = DialogBox()
        self.upgrade = Upgrade(self.flags, self.repo)
        self.view_message = ViewMessage(self.flags, self.repo)
        self.session = Session

        self.output: int = 0
        self.stderr = None
        self.stdout = None
        self.process_message: str = ''
        self.bold: str = self.color['bold']
        self.cyan: str = self.color['cyan']
        self.red: str = self.color['red']
        self.yellow: str = self.color['yellow']
        self.endc: str = self.color['endc']
        self.byellow: str = f'{self.bold}{self.yellow}'
        self.bred: str = f'{self.bold}{self.red}'

        self.packages_requires: list = []
        self.install_order: list = []
        self.binary_packages: list = []
        self.flag_reinstall: list = ['-r', '--reinstall']
        self.flag_skip_installed: list = ['-k', '--skip-installed']
        self.flag_no_silent: list = ['-n', '--no-silent']
        self.flag_resolve_off: list = ['-o', '--resolve-off']

        self.packages: list = self.utils.apply_package_pattern(self.flags, self.packages, self.repo)

    def execute(self) -> None:
        self.dependencies()

        self.view_message.install_packages(self.packages, self.packages_requires, self.mode)
        self.view_message.question()

        start: float = time.time()
        self.download()
        self.checksum()
        self.install_packages()
        elapsed_time: float = time.time() - start

        self.utils.finished_time(elapsed_time)

    def dependencies(self):
        """ Creating the dependencies list and the order for install. """
        requires: list = []

        if not self.utils.is_option(self.flag_resolve_off, self.flags):

            for pkg in self.packages:

                # Skip installed package when the option --skip-installed is applied.
                if (self.utils.is_option(self.flag_skip_installed, self.flags) and
                        self.utils.is_package_installed(pkg)):
                    continue

                self.packages_requires += Required(pkg, self.repo).resolve()

            # Clean dependencies from the dependencies list if already added with main packages.
            for req in self.packages_requires:
                if req not in self.packages:
                    requires.append(req)

            requires = list(set(requires))

            if requires:
                self.packages_requires = self.choose_dependencies(requires)

        self.install_order = [*self.packages_requires, *self.packages]

    def download(self) -> None:
        """ Download packages from the repositories. """
        pkg_urls: list = []

        for pkg in self.install_order:

            if self.continue_install(pkg):
                mirror: str = BinQueries(pkg, self.repo).mirror()
                location: str = BinQueries(pkg, self.repo).location()
                package: str = BinQueries(pkg, self.repo).package_bin()

                pkg_urls.append(f'{mirror}{location}/{package}')
                self.binary_packages.append(package)
                self.utils.remove_file_if_exists(self.tmp_slpkg, package)
            else:
                version: str = BinQueries(pkg, self.repo).version()
                self.view_message.view_skipping_packages(pkg, version)

        if pkg_urls:
            down = Downloader(self.tmp_slpkg, pkg_urls, self.flags)
            down.download()
            print()

    def continue_install(self, name) -> bool:
        """ Skip installed package when the option --skip-installed is applied
            and continue to install if the package is upgradable or the --reinstall option
            applied.
         """
        if (self.utils.is_option(self.flag_skip_installed, self.flags)
                and not self.utils.is_option(self.flag_reinstall, self.flags)):
            return False

        if self.utils.is_option(self.flag_reinstall, self.flags):
            return True

        if not self.utils.is_package_installed(name):
            return True

        if not self.upgrade.is_package_upgradeable(name):
            return False

        return True

    def checksum(self) -> None:
        """ Packages checksums. """
        md5 = Md5sum(self.flags)
        for package in self.binary_packages:
            pkg_checksum: str = BinQueries(package, self.repo).package_checksum()
            md5.check(self.tmp_slpkg, package, pkg_checksum)

    def install_packages(self) -> None:
        """ Install the packages. """
        slack_command: str = self.installpkg
        if self.utils.is_option(self.flag_reinstall, self.flags) or self.mode == 'upgrade':
            slack_command: str = self.reinstall

        message: str = f'{self.cyan}Installing{self.endc}'

        for package in self.binary_packages:
            self.process_message: str = f"package '{package}' to install"
            command: str = f'{slack_command} {self.tmp_slpkg}/{package}'

            self.multi_process(command, package, message)

            if not self.utils.is_option(self.flag_resolve_off, self.flags):
                name: str = self.utils.split_binary_pkg(package[:-4])[0]

                if not self.utils.is_option(self.flag_resolve_off, self.flags):
                    self.logging_installed_dependencies(name)

    def logging_installed_dependencies(self, name: str) -> None:
        """ Logging installed dependencies and used for remove. """
        exist = self.session.query(LogsDependencies.name).filter(
            LogsDependencies.name == name).first()

        requires: list = Required(name, self.repo).resolve()

        # Update the dependencies if exist else create it.
        if exist:
            self.session.query(
                LogsDependencies).filter(
                    LogsDependencies.name == name).update(
                        {LogsDependencies.requires: ' '.join(requires)})

        elif requires:
            deps: list = LogsDependencies(name=name, requires=' '.join(requires))
            self.session.add(deps)
        self.session.commit()

    def multi_process(self, command: str, filename: str, message: str) -> None:
        """ Starting multiprocessing install/upgrade process. """
        if self.silent_mode and not self.utils.is_option(self.flag_no_silent, self.flags):

            done: str = f' {self.byellow} Done{self.endc}'
            self.stderr = subprocess.DEVNULL
            self.stdout = subprocess.DEVNULL

            # Starting multiprocessing
            p1 = Process(target=self.utils.process, args=(command, self.stderr, self.stdout))
            p2 = Process(target=self.progress.bar, args=(f'[{message}]', filename))

            p1.start()
            p2.start()

            # Wait until process 1 finish
            p1.join()

            # Terminate process 2 if process 1 finished
            if not p1.is_alive():

                if p1.exitcode != 0:
                    done: str = f'{self.bred}Failed: {self.endc}{self.process_message}.'
                    self.output: int = p1.exitcode  # type: ignore

                print(f'{self.endc}{done}', end='')
                p2.terminate()

            # Wait until process 2 finish
            p2.join()

            # Restore the terminal cursor
            print('\x1b[?25h', self.endc)
        else:
            self.utils.process(command, self.stderr, self.stdout)

        self.print_error()

    def print_error(self) -> None:
        """ Stop the process and print the error message. """
        if self.output != 0:
            self.utils.raise_error_message(f"{self.output}: {self.process_message}")

    def choose_dependencies(self, dependencies: list) -> list:
        """ Choose packages for install. """
        height: int = 10
        width: int = 70
        list_height: int = 0
        choices: list = []
        title: str = ' Choose dependencies you want to install '

        for package in dependencies:
            status: bool = False

            repo_ver: str = BinQueries(package, self.repo).version()
            help_text: str = f'Package: {package} {repo_ver}'
            upgradable: bool = self.upgrade.is_package_upgradeable(package)
            installed: str = self.utils.is_package_installed(package)

            if self.mode == 'upgrade' and upgradable:
                status: bool = True

            if self.mode == 'install' and upgradable:
                status: bool = True

            if self.mode == 'install' and not installed:
                status: bool = True

            choices += [(package, repo_ver, status, help_text)]

        text: str = f'There are {len(choices)} dependencies:'

        code, tags = self.dialogbox.checklist(text, dependencies, title, height,
                                              width, list_height, choices)

        if not code:
            return dependencies

        os.system('clear')

        return tags
