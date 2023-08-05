#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import subprocess
from multiprocessing import Process

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.views.views import ViewMessage
from slpkg.progress_bar import ProgressBar
from slpkg.models.models import LogsDependencies
from slpkg.models.models import session as Session


class RemovePackages(Configs):
    """ Removes installed packages. """

    def __init__(self, packages: list, flags: list):
        super(Configs, self).__init__()
        self.packages: list = packages
        self.flags: list = flags

        self.session = Session
        self.color = self.colour()
        self.utils = Utilities()
        self.progress = ProgressBar()

        self.output: int = 0
        self.installed_packages: list = []
        self.dependencies: list = []
        self.remove_pkg = None
        self.stderr = None
        self.stdout = None
        self.bold: str = self.color['bold']
        self.yellow: str = self.color['yellow']
        self.red: str = self.color['red']
        self.endc: str = self.color['endc']
        self.byellow: str = f'{self.bold}{self.yellow}'
        self.bred: str = f'{self.bold}{self.red}'
        self.flag_resolve_off: list = ['-o', '--resolve-off']
        self.flag_no_silent: list = ['-n', '--no-silent']

    def remove(self) -> None:
        """ Removes package with dependencies. """
        view = ViewMessage(self.flags)

        self.installed_packages, self.dependencies = view.remove_packages(self.packages)

        view.question()

        start: float = time.time()
        self.remove_packages()

        if self.dependencies and not self.utils.is_option(self.flag_resolve_off, self.flags):
            self.delete_deps_logs()

        self.delete_main_logs()

        elapsed_time: float = time.time() - start

        self.utils.finished_time(elapsed_time)

    def remove_packages(self) -> None:
        """ Run Slackware command to remove the packages. """
        for package in self.installed_packages:
            self.remove_pkg = package
            command: str = f'{self.removepkg} {package}'
            self.multi_process(command, package)

    def delete_main_logs(self) -> None:
        """ Deletes main packages from logs. """
        for pkg in self.packages:
            self.session.query(LogsDependencies).filter(
                LogsDependencies.name == pkg).delete()
        self.session.commit()

    def delete_deps_logs(self) -> None:
        """ Deletes depends packages from logs. """
        for pkg in self.dependencies:
            self.session.query(LogsDependencies).filter(
                LogsDependencies.name == pkg).delete()
        self.session.commit()

    def multi_process(self, command: str, package: str) -> None:
        """ Starting multiprocessing remove process. """
        if self.silent_mode and not self.utils.is_option(self.flag_no_silent, self.flags):

            done: str = f' {self.byellow} Done{self.endc}'
            message: str = f'{self.red}Remove{self.endc}'
            self.stderr = subprocess.DEVNULL
            self.stdout = subprocess.DEVNULL

            # Starting multiprocessing
            p1 = Process(target=self.utils.process, args=(command, self.stderr, self.stdout))
            p2 = Process(target=self.progress.bar, args=(f'[{message}]', package))

            p1.start()
            p2.start()

            # Wait until process 1 finish
            p1.join()

            # Terminate process 2 if process 1 finished
            if not p1.is_alive():

                if p1.exitcode != 0:
                    done: str = f' {self.bred} Failed{self.endc}'
                    self.output: int = p1.exitcode  # type: ignore

                print(f'{self.endc}{done}', end='')
                p2.terminate()

            # Wait until process 2 finish
            p2.join()

            # Restore the terminal cursor
            print('\x1b[?25h', self.endc)
        else:
            self.utils.process(command, self.stderr, self.stdout)
