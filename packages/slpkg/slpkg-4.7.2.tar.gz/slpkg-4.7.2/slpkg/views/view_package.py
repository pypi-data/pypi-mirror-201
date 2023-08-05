#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pathlib import Path

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.sbos.queries import SBoQueries
from slpkg.repositories import Repositories
from slpkg.binaries.queries import BinQueries
from slpkg.models.models import session as Session
from slpkg.models.models import (SBoTable, PonceTable,
                                 BinariesTable, LastRepoUpdated)


class ViewPackage(Configs):
    """ View the repository packages. """

    def __init__(self, flags: list):
        super(Configs, self).__init__()
        self.flags: list = flags

        self.utils = Utilities()
        self.repos = Repositories()
        self.session = Session
        
        self.color = self.colour()
        self.green: str = self.color['green']
        self.blue: str = self.color['blue']
        self.yellow: str = self.color['yellow']
        self.cyan: str = self.color['cyan']
        self.red: str = self.color['red']
        self.violet: str = self.color['violet']
        self.endc: str = self.color['endc']
        self.flag_pkg_version: list = ['-p', '--pkg-version']

        # Switch between sbo and ponce repository.
        self.sbo_table = SBoTable
        self.repo_url: str = self.repos.sbo_repo_mirror
        self.repo_path: Path = self.repos.sbo_repo_path
        self.repo_tar_suffix: str = self.repos.sbo_repo_tar_suffix
        if self.repos.ponce_repo:
            self.sbo_table = PonceTable
            self.repo_url: str = self.repos.ponce_repo_mirror
            self.repo_path: Path = self.repos.ponce_repo_path
            self.repo_tar_suffix: str = ''

    def slackbuild(self, slackbuilds: list) -> None:
        """ View the packages from the repository. """
        slackbuilds: list = self.utils.apply_package_pattern(self.flags, slackbuilds)

        for sbo in slackbuilds:

            info: list = self.session.query(
                self.sbo_table.name,
                self.sbo_table.version,
                self.sbo_table.requires,
                self.sbo_table.download,
                self.sbo_table.download64,
                self.sbo_table.md5sum,
                self.sbo_table.md5sum64,
                self.sbo_table.files,
                self.sbo_table.short_description,
                self.sbo_table.location
            ).filter(self.sbo_table.name == sbo).first()

            path = Path(self.repo_path, info[9], info[0], 'README')
            readme = self.utils.read_file(path)

            path = Path(self.repo_path, info[9], info[0], f'{info[0]}.info')
            info_file = self.utils.read_file(path)

            repo_build_tag = self.utils.read_sbo_build_tag(info[0])

            maintainer, email, homepage = '', '', ''
            for line in info_file:
                if line.startswith('HOMEPAGE'):
                    homepage: str = line[10:-2].strip()
                if line.startswith('MAINTAINER'):
                    maintainer: str = line[12:-2].strip()
                if line.startswith('EMAIL'):
                    email: str = line[7:-2].strip()

            deps: str = (', '.join([f'{self.cyan}{pkg}' for pkg in info[2].split()]))

            if self.utils.is_option(self.flag_pkg_version, self.flags):
                deps: str = (', '.join([f'{self.cyan}{pkg}{self.endc}-{self.yellow}{SBoQueries(pkg).version()}'
                             f'{self.green}' for pkg in info[2].split()]))

            print(f'Name: {self.green}{info[0]}{self.endc}\n'
                  f'Version: {self.green}{info[1]}{self.endc}\n'
                  f'Build: {self.green}{repo_build_tag}{self.endc}\n'
                  f'Requires: {self.green}{deps}{self.endc}\n'
                  f'Homepage: {self.blue}{homepage}{self.endc}\n'
                  f'Download SlackBuild: {self.blue}{self.repo_url}{info[9]}/{info[0]}'
                  f'{self.repo_tar_suffix}{self.endc}\n'
                  f'Download sources: {self.blue}{info[3]}{self.endc}\n'
                  f'Download_x86_64 sources: {self.blue}{info[4]}{self.endc}\n'
                  f'Md5sum: {self.yellow}{info[5]}{self.endc}\n'
                  f'Md5sum_x86_64: {self.yellow}{info[6]}{self.endc}\n'
                  f'Files: {self.green}{info[7]}{self.endc}\n'
                  f'Description: {self.green}{info[8]}{self.endc}\n'
                  f'Slackware: {self.cyan}{self.repo_url.split("/")[-1]}{self.endc}\n'
                  f'Category: {self.red}{info[9]}{self.endc}\n'
                  f'SBo url: {self.blue}{self.repo_url}{info[9]}/{info[0]}{self.endc}\n'
                  f'Maintainer: {self.yellow}{maintainer}{self.endc}\n'
                  f'Email: {self.yellow}{email}{self.endc}\n'
                  f'\nREADME: {self.cyan}{"".join(readme)}{self.endc}')

    def package(self, packages: list, repo: str) -> None:

        for package in packages:

            info: list = self.session.query(
                BinariesTable.repo,
                BinariesTable.name,
                BinariesTable.version,
                BinariesTable.package,
                BinariesTable.checksum,
                BinariesTable.mirror,
                BinariesTable.location,
                BinariesTable.size_comp,
                BinariesTable.size_uncomp,
                BinariesTable.required,
                BinariesTable.conflicts,
                BinariesTable.suggests,
                BinariesTable.description,
            ).filter(BinariesTable.name == package).where(
                BinariesTable.repo == repo).first()

            build: str = self.utils.split_binary_pkg(info[3])[3]

            last: str = self.session.query(
                LastRepoUpdated.date).where(
                LastRepoUpdated.repo == repo).first()

            deps: str = (', '.join([f'{self.cyan}{pkg}' for pkg in info[9].split()]))
            if self.utils.is_option(self.flag_pkg_version, self.flags):
                deps: str = (', '.join([f'{self.cyan}{pkg}{self.endc}-{self.yellow}{BinQueries(pkg, repo).version()}'
                             f'{self.green}' for pkg in info[9].split()]))

            print(f'Repository: {self.yellow}{info[0]}{self.endc}\n'
                  f'Last Updated: {self.violet}{last[0]}{self.endc}\n'
                  f'Name: {self.green}{info[1]}{self.endc}\n'
                  f'Version: {self.green}{info[2]}{self.endc}\n'
                  f'Build: {self.green}{build}{self.endc}\n'
                  f'Package: {self.cyan}{info[3]}{self.endc}\n'
                  f'Download: {self.blue}{info[5]}{info[6]}/{info[3]}{self.endc}\n'
                  f'Md5sum: {info[4]}\n'
                  f'Mirror: {self.blue}{info[5]}{self.endc}\n'
                  f'Location: {self.red}{info[6]}{self.endc}\n'
                  f'Size Comp: {info[7]}\n'
                  f'Size Uncomp: {info[8]}\n'
                  f'Requires: {self.green}{deps}{self.endc}\n'
                  f'Conflicts: {info[10]}\n'
                  f'Suggests: {info[11]}\n'
                  f'Description: {info[12]}\n')
