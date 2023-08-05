#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
import shutil
import subprocess

from pathlib import Path
from collections import OrderedDict
from multiprocessing import Process, cpu_count

from slpkg.checksum import Md5sum
from slpkg.configs import Configs
from slpkg.upgrade import Upgrade
from slpkg.utilities import Utilities
from slpkg.dialog_box import DialogBox
from slpkg.downloader import Downloader
from slpkg.views.views import ViewMessage
from slpkg.sbos.queries import SBoQueries
from slpkg.progress_bar import ProgressBar
from slpkg.repositories import Repositories
from slpkg.sbos.dependencies import Requires
from slpkg.models.models import LogsDependencies
from slpkg.models.models import session as Session


class Slackbuilds(Configs):
    """ Download build and install the SlackBuilds. """

    def __init__(self, slackbuilds: list, flags: list, mode: str):
        super(Configs, self).__init__()
        self.slackbuilds: list = slackbuilds
        self.flags: list = flags
        self.mode: str = mode

        self.session = Session
        self.repos = Repositories()
        self.utils = Utilities()
        self.progress = ProgressBar()
        self.dialogbox = DialogBox()
        self.upgrade = Upgrade(self.flags)
        self.view_message = ViewMessage(self.flags)
        self.color = self.colour()

        self.install_order: list = []
        self.dependencies: list = []
        self.sbos: dict = {}
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
        self.flag_reinstall: list = ['-r', '--reinstall']
        self.flag_skip_installed: list = ['-k', '--skip-installed']
        self.flag_resolve_off: list = ['-o', '--resolve-off']
        self.flag_jobs: list = ['-j', '--jobs']
        self.flag_no_silent: list = ['-n', '--no-silent']

        self.slackbuilds: list = self.utils.apply_package_pattern(self.flags, self.slackbuilds)

        # Patch the TAG from configs.
        if self.repos.patch_repo_tag:
            self.repos.repo_tag = self.repos.patch_repo_tag

    def execute(self) -> None:
        """ Starting build or install the slackbuilds. """
        self.creating_dictionary()
        self.creating_dependencies_for_build()
        self.creating_main_for_build()
        self.view_before_build()

        start: float = time.time()
        self.prepare_slackbuilds_for_build()
        self.build_and_install()
        elapsed_time: float = time.time() - start

        self.utils.finished_time(elapsed_time)

    def creating_dictionary(self) -> None:
        """ Dictionary with the main slackbuilds and dependencies. """
        for sbo in self.slackbuilds:
            if self.utils.is_option(self.flag_resolve_off, self.flags):
                self.sbos[sbo] = []
            else:
                self.sbos[sbo] = Requires(sbo).resolve()

    def creating_dependencies_for_build(self) -> None:
        """ List with the dependencies. """
        for deps in self.sbos.values():
            for dep in deps:

                # Skip installed package when the option --skip-installed is applied.
                if (self.utils.is_option(self.flag_skip_installed, self.flags) and
                        self.utils.is_package_installed(dep)):
                    continue

                self.dependencies.append(dep)

        # Remove duplicate packages and keeps the order.
        dependencies = list(OrderedDict.fromkeys(self.dependencies))

        if dependencies:
            self.dependencies = self.choose_dependencies(dependencies)

            # Clean up the main packages if they were selected for dependencies.
            for dep in self.dependencies:
                if dep in self.slackbuilds:
                    self.slackbuilds.remove(dep)

        self.install_order.extend(self.dependencies)

    def creating_main_for_build(self) -> None:
        """ List with the main slackbuilds. """
        [self.install_order.append(main) for main in self.sbos.keys() if main not in self.install_order]

    def view_before_build(self) -> None:
        """ View slackbuilds before proceed. """
        if not self.mode == 'build':
            self.view_message.install_packages(self.slackbuilds, self.dependencies, self.mode)
        else:
            self.view_message.build_packages(self.slackbuilds, self.dependencies)

        del self.dependencies  # no more needed

        self.view_message.question()

    def continue_build_or_install(self, name) -> bool:
        """ Skip installed package when the option --skip-installed is applied
            and continue to install if the package is upgradable or the --reinstall option
            applied.
        """
        if (self.utils.is_option(self.flag_skip_installed, self.flags)
                and not self.utils.is_option(self.flag_reinstall, self.flags)
                and self.mode != 'build'):
            return False

        if self.utils.is_option(self.flag_reinstall, self.flags) and self.mode != 'build':
            return True

        if not self.utils.is_package_installed(name) and self.mode != 'build':
            return True

        if not self.upgrade.is_package_upgradeable(name) and self.mode not in ['build', 'upgrade']:
            return False

        return True

    def prepare_slackbuilds_for_build(self) -> None:
        """ Downloads files and sources. """
        sources_urls: list = []
        sources: dict = {}

        for sbo in self.install_order:

            if self.continue_build_or_install(sbo):

                build_path: Path = Path(self.build_path, sbo)

                self.utils.remove_folder_if_exists(build_path)
                location: str = SBoQueries(sbo).location()
                slackbuild = Path(self.build_path, sbo, f'{sbo}.SlackBuild')

                # Copy slackbuilds to the build folder.
                if self.repos.ponce_repo:
                    path_ponce_repo_package = Path(self.repos.ponce_repo_path, location, sbo)
                    shutil.copytree(path_ponce_repo_package, build_path)
                else:
                    path_sbo_repo_package = Path(self.repos.sbo_repo_path, location, sbo)
                    shutil.copytree(path_sbo_repo_package, build_path)

                os.chmod(slackbuild, 0o775)
                sources[sbo] = SBoQueries(sbo).sources()
                sources_urls += SBoQueries(sbo).sources()

        # Download the sources.
        if sources:
            down_urls = Downloader(self.build_path, sources_urls, self.flags)
            down_urls.download()

            print()  # New line here.

            self.move_sources(sources)
            self.checksum_downloads()

    def move_sources(self, sources: dict) -> None:
        """ Move the sources into the folders for build. """
        for sbo, source in sources.items():
            for src in source:
                source = Path(self.build_path, src.split('/')[-1])
                path = Path(self.build_path, sbo)
                shutil.move(source, path)

    def checksum_downloads(self) -> None:
        """ Checking the correct checksums. """
        for sbo in self.install_order:
            path = Path(self.build_path, sbo)
            checksums = SBoQueries(sbo).checksum()
            sources = SBoQueries(sbo).sources()

            for source, checksum in zip(sources, checksums):
                md5sum = Md5sum(self.flags)
                md5sum.check(path, source, checksum)

    def build_and_install(self) -> None:
        """ Build the slackbuilds and install. """
        for sbo in self.install_order:

            if self.continue_build_or_install(sbo):

                self.patch_sbo_tag(sbo)

                self.build_the_script(self.build_path, sbo)

                if self.mode in ['install', 'upgrade']:

                    pkg: str = self.package_for_install(sbo)
                    self.install_package(pkg)

                    if not self.utils.is_option(self.flag_resolve_off, self.flags):
                        self.logging_installed_dependencies(sbo)
            else:
                package: str = self.utils.is_package_installed(sbo)
                version: str = self.utils.split_binary_pkg(package)[1]
                self.view_message.view_skipping_packages(sbo, version)

    def patch_sbo_tag(self, sbo: str) -> None:
        """ Patching SBo TAG from the configuration file. """
        sbo_script = Path(self.build_path, sbo, f'{sbo}.SlackBuild')

        if sbo_script.is_file() and self.repos.patch_repo_tag:

            with open(sbo_script, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            with open(sbo_script, 'w') as script:
                for line in lines:
                    if line.startswith('TAG=$'):
                        line: str = f'TAG=${{TAG:-{self.repos.patch_repo_tag}}}\n'
                    script.write(line)

    def logging_installed_dependencies(self, name: str) -> None:
        """ Logging installed dependencies and used for remove. """
        exist = self.session.query(LogsDependencies.name).filter(
            LogsDependencies.name == name).first()

        requires: list = Requires(name).resolve()

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

    def install_package(self, package: str) -> None:
        """ Install the packages that before created in the tmp directory. """
        pkg: str = self.utils.split_binary_pkg(package)[0]

        execute: str = self.installpkg
        if (self.utils.is_option(self.flag_reinstall, self.flags) and
                self.utils.is_package_installed(pkg)):
            execute: str = self.reinstall

        message: str = f'{self.cyan}Installing{self.endc}'
        self.process_message: str = f"package '{pkg}' to install"

        if self.mode == 'upgrade':
            self.process_message: str = f"package '{pkg}' to upgrade"
            message: str = f'{self.cyan}Upgrade{self.endc}'

        command: str = f'{execute} {self.tmp_path}{package}'

        self.multi_process(command, package, message)

    def package_for_install(self, name: str) -> str:
        """ Returns the package for install. """
        package_to_install: str = ''
        version: str = SBoQueries(name).version()
        pattern: str = f'{name}-{version}*{self.repos.repo_tag}*'

        tmp = Path(self.tmp_path)
        packages: list = [file.name for file in tmp.glob(pattern)]

        try:
            package_to_install: str = max(packages)
        except ValueError:
            self.utils.raise_error_message(f"Package '{name}' not found for install")

        return package_to_install

    def build_the_script(self, path: Path, name: str) -> None:
        """ Run the .SlackBuild script. """
        folder: str = f'{Path(path, name)}/'
        execute: str = f'{folder}./{name}.SlackBuild'

        # Change to root privileges
        os.chown(folder, 0, 0)
        for file in os.listdir(folder):
            os.chown(f'{folder}{file}', 0, 0)

        if self.utils.is_option(self.flag_jobs, self.flags):
            self.set_makeflags()

        name = f'{name}.SlackBuild'
        message: str = f'{self.red}Build{self.endc}'
        self.process_message: str = f"package '{name}' to build"

        self.multi_process(execute, name, message)

    @staticmethod
    def set_makeflags() -> None:
        """ Set number of processors. """
        os.environ['MAKEFLAGS'] = f'-j {cpu_count()}'

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

                p2.terminate()
                print(f'{self.endc}{done}', end='')

            # Wait until process 2 finish
            p2.join()

            # Restore the terminal cursor
            print('\x1b[?25h', self.endc)
        else:
            self.utils.process(command, self.stderr, self.stdout)

    def choose_dependencies(self, dependencies: list) -> list:
        """ Choose packages for install. """
        height: int = 10
        width: int = 70
        list_height: int = 0
        choices: list = []
        title: str = ' Choose dependencies you want to install '

        for package in dependencies:
            status: bool = False

            repo_ver: str = SBoQueries(package).version()
            description: str = SBoQueries(package).description()
            help_text: str = f'Description: {description}'
            upgradable: bool = self.upgrade.is_package_upgradeable(package)
            installed: str = self.utils.is_package_installed(package)

            if self.mode == 'build':
                status: bool = True

            if self.mode == 'upgrade':
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
