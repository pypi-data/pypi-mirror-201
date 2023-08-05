#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import time
import shutil
import subprocess
from pathlib import Path
from typing import Generator, Union

from slpkg.configs import Configs
from slpkg.blacklist import Blacklist
from slpkg.sbos.queries import SBoQueries
from slpkg.repositories import Repositories
from slpkg.binaries.queries import BinQueries


class Utilities:

    def __init__(self):
        self.configs = Configs
        self.colors = self.configs.colour
        self.color = self.colors()
        self.black = Blacklist()
        self.repos = Repositories()

        self.bold: str = self.color['bold']
        self.yellow: str = self.color['yellow']
        self.cyan: str = self.color['cyan']
        self.red: str = self.color['red']
        self.endc: str = self.color['endc']
        self.bred: str = f'{self.bold}{self.red}'
        self.flag_bin_repository: list = ['-B=', '--bin-repo=']

        self.installed_packages: list = list(self.all_installed())
        self.installed_package_names: list = list(self.all_installed_names())

    def is_package_installed(self, name: str) -> str:
        """ Returns the installed package name. """
        for package in self.installed_packages:
            pkg_name: str = self.split_binary_pkg(package)[0]

            if pkg_name == name:
                return package

        return ''

    def all_installed(self) -> Generator:
        """ Return all installed packages from /val/log/packages folder. """
        var_log_packages = Path(self.configs.log_packages)

        try:
            for file in var_log_packages.glob(self.configs.file_pattern):
                package_name = self.split_binary_pkg(file.name)[0]

                if package_name not in self.black.packages():
                    yield file.name
        except ValueError:
            pass

    def all_installed_names(self) -> Generator:
        """ Return all installed packages names from /val/log/packages folder. """
        var_log_packages = Path(self.configs.log_packages)

        try:
            for file in var_log_packages.glob(self.configs.file_pattern):
                package_name = self.split_binary_pkg(file.name)[0]

                if package_name not in self.black.packages():
                    yield package_name
        except ValueError:
            pass

    @staticmethod
    def remove_file_if_exists(path: Path, file: str) -> None:
        """ Clean the old files. """
        archive = Path(path, file)
        if archive.is_file():
            archive.unlink()

    @staticmethod
    def remove_folder_if_exists(folder: Path) -> None:
        """ Clean the old folders. """
        directory = Path(folder)
        if directory.exists():
            shutil.rmtree(directory)

    @staticmethod
    def create_folder(path: Path, folder: str) -> None:
        """ Creates folder. """
        directory = Path(path, folder)
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def split_binary_pkg(package: str) -> list:
        """ Split the package by the name, version, arch, build and tag. """
        name: str = '-'.join(package.split('-')[:-3])
        version: str = ''.join(package[len(name):].split('-')[:-2])
        arch: str = ''.join(package[len(name + version) + 2:].split('-')[:-1])
        build_tag: str = package.split('-')[-1]
        build: str = ''.join(re.findall(r'\d+', build_tag[:2]))
        tag: str = build_tag[len(build):].replace('_', '')

        return [name, version, arch, build, tag]

    def finished_time(self, elapsed_time: float) -> None:
        """ Printing the elapsed time. """
        print(f'\n{self.yellow}Finished Successfully:{self.endc}',
              time.strftime(f'[{self.cyan}%H:%M:%S{self.endc}]',
                            time.gmtime(elapsed_time)))

    def read_sbo_build_tag(self, sbo: str) -> str:
        """ Returns build tag from .SlackBuild file. """
        build: str = ''
        location: str = SBoQueries(sbo).location()
        sbo_script = Path(self.repos.sbo_repo_path, location, sbo, f'{sbo}.SlackBuild')

        if sbo_script.is_file():
            with open(sbo_script, 'r', encoding='utf-8') as f:
                lines = f.readlines()

                for line in lines:
                    if line.startswith('BUILD=$'):
                        build = ''.join(re.findall(r'\d+', line))

        return build

    @staticmethod
    def is_option(flag: list, flags: list) -> bool:
        """ Checking for flags. """
        for f in flag:
            if f in flags:
                return True

    def read_packages_from_file(self, file: Path) -> Generator:
        """ Reads packages from file and split these to list. """
        try:

            with open(file, 'r', encoding='utf-8') as pkgs:
                packages: list = pkgs.read().splitlines()

            for package in packages:
                if package and not package.startswith('#'):
                    if '#' in package:
                        package = package.split('#')[0].strip()

                    yield package

        except FileNotFoundError:
            self.raise_error_message(f"No such file or directory: '{file}'")

    @staticmethod
    def read_file(file: Union[str, Path]) -> list:
        """ Reads the text file. """
        with open(file, 'r', encoding='utf-8', errors='replace') as f:
            return f.readlines()

    @staticmethod
    def process(command: str, stderr=None, stdout=None) -> None:
        """ Handle the processes. """
        try:
            output = subprocess.call(command, shell=True, stderr=stderr, stdout=stdout)
        except (KeyboardInterrupt, subprocess.CalledProcessError) as err:
            raise SystemExit(err)

        if output != 0:
            raise SystemExit(output)

    def raise_error_message(self, message: str) -> None:
        """ A general method to raise an error message and exit. """
        raise SystemExit(f"\n{self.configs.prog_name}: {self.bred}Error{self.endc}: {message}.\n")

    @staticmethod
    def get_file_size(file):
        """ Get the file size and converted to units. """
        unit: str = 'KB'
        file_size = Path(file).stat().st_size
        mb = file_size / 1024 ** 2
        gb = file_size / 1024 ** 3

        if mb >= 0.1:
            file_size = mb
            unit: str = 'MB'

        if gb >= 0.1:
            file_size = mb
            unit: str = 'GB'

        return f'{str(round(file_size, 2))} {unit}'

    def apply_package_pattern(self, flags: list, packages: list, repo=None) -> list:
        """ Apply the pattern. """
        for pkg in packages:
            if pkg == '*':
                packages.remove(pkg)

                if self.is_option(self.flag_bin_repository, flags):
                    packages += BinQueries('', repo).all_package_names_by_repo()
                else:
                    packages += SBoQueries('').sbos()

        return packages
