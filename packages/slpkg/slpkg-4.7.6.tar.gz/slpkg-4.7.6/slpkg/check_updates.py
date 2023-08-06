#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import urllib3
from pathlib import Path
from multiprocessing import Process

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.progress_bar import ProgressBar
from slpkg.repositories import Repositories


class CheckUpdates(Configs):
    """ Check for changes in the ChangeLog file. """

    def __init__(self, flags: list, repo: str):
        super(Configs, self).__init__()
        self.flags: list = flags
        self.repo = repo
        self.utils = Utilities()
        self.progress = ProgressBar()
        self.color = self.colour()
        self.repos = Repositories()

        self.bold: str = self.color['bold']
        self.green: str = self.color['green']
        self.yellow: str = self.color['yellow']
        self.bgreen: str = f'{self.bold}{self.green}'
        self.endc: str = self.color['endc']
        self.flag_bin_repository: list = ['-B', '--bin-repo=']
        self.compare: dict = {}

        self.local_chg_txt = None
        self.repo_chg_txt = None

    def check(self) -> dict:
        bin_repositories: dict = {
            self.repos.slack_repo_name: self.slack_repository,
            self.repos.slack_extra_repo_name: self.slack_extra_repository,
            self.repos.slack_patches_repo_name: self.slack_patches_repository,
            self.repos.alien_repo_name: self.alien_repository,
            self.repos.multilib_repo_name: self.multilib_repository,
            self.repos.restricted_repo_name: self.restricted_repository,
            self.repos.gnome_repo_name: self.gnome_repository,
            self.repos.msb_repo_name: self.msb_repository,
            self.repos.csb_repo_name: self.csb_repository,
            self.repos.conraid_repo_name: self.conraid_repository,
            self.repos.slackonly_repo_name: self.slackonly_repository,
            self.repos.salixos_repo_name: self.salixos_repository,
            self.repos.salixos_extra_repo_name: self.salixos_extra_repository,
            self.repos.salixos_patches_repo_name: self.salixos_patches_repository,
            self.repos.slackel_repo_name: self.slackel_repository,
            self.repos.slint_repo_name: self.slint_repository
        }

        if self.utils.is_option(self.flag_bin_repository, self.flags):

            for repo in bin_repositories.keys():
                if repo in self.repos.bin_enabled_repos and repo == self.repo:
                    bin_repositories[repo]()
                    break

                if repo in self.repos.bin_enabled_repos and self.repo == '*':
                    bin_repositories[repo]()
        else:

            if self.repos.ponce_repo:
                self.ponce_repository()
            else:
                self.sbo_repository()

        return self.compare

    def slack_repository(self) -> None:
        self.local_chg_txt: Path = Path(self.repos.slack_repo_path, self.repos.slack_repo_changelog)
        self.repo_chg_txt: str = f'{self.repos.slack_repo_mirror}{self.repos.slack_repo_changelog}'
        self.compare[self.repos.slack_repo_name] = self.compare_dates()

    def slack_extra_repository(self) -> None:
        self.local_chg_txt: Path = Path(self.repos.slack_extra_repo_path, self.repos.slack_extra_repo_changelog)
        self.repo_chg_txt: str = f'{self.repos.slack_extra_repo_mirror}{self.repos.slack_extra_repo_changelog}'
        self.compare[self.repos.slack_extra_repo_name] = self.compare_dates()

    def slack_patches_repository(self) -> None:
        self.local_chg_txt: Path = Path(self.repos.slack_patches_repo_path, self.repos.slack_patches_repo_changelog)
        self.repo_chg_txt: str = f'{self.repos.slack_patches_repo_mirror}{self.repos.slack_patches_repo_changelog}'
        self.compare[self.repos.slack_patches_repo_name] = self.compare_dates()

    def alien_repository(self) -> None:
        self.local_chg_txt: Path = Path(self.repos.alien_repo_path, self.repos.alien_repo_changelog)
        self.repo_chg_txt: str = f'{self.repos.alien_repo_mirror}{self.repos.alien_repo_changelog}'
        self.compare[self.repos.alien_repo_name] = self.compare_dates()

    def multilib_repository(self) -> None:
        self.local_chg_txt: Path = Path(self.repos.multilib_repo_path, self.repos.multilib_repo_changelog)
        self.repo_chg_txt: str = f'{self.repos.multilib_repo_mirror}{self.repos.multilib_repo_changelog}'
        self.compare[self.repos.multilib_repo_name] = self.compare_dates()

    def restricted_repository(self) -> None:
        self.local_chg_txt: Path = Path(self.repos.restricted_repo_path, self.repos.restricted_repo_changelog)
        self.repo_chg_txt: str = f'{self.repos.restricted_repo_mirror}{self.repos.restricted_repo_changelog}'
        self.compare[self.repos.restricted_repo_name] = self.compare_dates()

    def gnome_repository(self) -> None:
        self.local_chg_txt: Path = Path(self.repos.gnome_repo_path, self.repos.gnome_repo_changelog)
        self.repo_chg_txt: str = f'{self.repos.gnome_repo_mirror}{self.repos.gnome_repo_changelog}'
        self.compare[self.repos.gnome_repo_name] = self.compare_dates()

    def msb_repository(self) -> None:
        self.local_chg_txt: Path = Path(self.repos.msb_repo_path, self.repos.msb_repo_changelog)
        self.repo_chg_txt: str = f'{self.repos.msb_repo_mirror}{self.repos.msb_repo_changelog}'
        self.compare[self.repos.msb_repo_name] = self.compare_dates()

    def csb_repository(self) -> None:
        self.local_chg_txt: Path = Path(self.repos.csb_repo_path, self.repos.csb_repo_changelog)
        self.repo_chg_txt: str = f'{self.repos.csb_repo_mirror}{self.repos.csb_repo_changelog}'
        self.compare[self.repos.csb_repo_name] = self.compare_dates()

    def conraid_repository(self) -> None:
        self.local_chg_txt: Path = Path(self.repos.conraid_repo_path, self.repos.conraid_repo_changelog)
        self.repo_chg_txt: str = f'{self.repos.conraid_repo_mirror}{self.repos.conraid_repo_changelog}'
        self.compare[self.repos.conraid_repo_name] = self.compare_dates()

    def slackonly_repository(self) -> None:
        self.local_chg_txt: Path = Path(self.repos.slackonly_repo_path, self.repos.slackonly_repo_changelog)
        self.repo_chg_txt: str = f'{self.repos.slackonly_repo_mirror}{self.repos.slackonly_repo_changelog}'
        self.compare[self.repos.slackonly_repo_name] = self.compare_dates()

    def salixos_repository(self) -> None:
        self.local_chg_txt: Path = Path(self.repos.salixos_repo_path, self.repos.salixos_repo_changelog)
        self.repo_chg_txt: str = f'{self.repos.salixos_repo_mirror}{self.repos.salixos_repo_changelog}'
        self.compare[self.repos.salixos_repo_name] = self.compare_dates()

    def salixos_extra_repository(self) -> None:
        self.local_chg_txt: Path = Path(self.repos.salixos_extra_repo_path, self.repos.salixos_extra_repo_changelog)
        self.repo_chg_txt: str = f'{self.repos.salixos_extra_repo_mirror}{self.repos.salixos_extra_repo_changelog}'
        self.compare[self.repos.salixos_extra_repo_name] = self.compare_dates()

    def salixos_patches_repository(self) -> None:
        self.local_chg_txt: Path = Path(self.repos.salixos_patches_repo_path, self.repos.salixos_patches_repo_changelog)
        self.repo_chg_txt: str = f'{self.repos.salixos_patches_repo_mirror}{self.repos.salixos_patches_repo_changelog}'
        self.compare[self.repos.salixos_patches_repo_name] = self.compare_dates()

    def slackel_repository(self) -> None:
        self.local_chg_txt: Path = Path(self.repos.slackel_repo_path, self.repos.slackel_repo_changelog)
        self.repo_chg_txt: str = f'{self.repos.slackel_repo_mirror}{self.repos.slackel_repo_changelog}'
        self.compare[self.repos.slackel_repo_name] = self.compare_dates()

    def slint_repository(self) -> None:
        self.local_chg_txt: Path = Path(self.repos.slint_repo_path, self.repos.slint_repo_changelog)
        self.repo_chg_txt: str = f'{self.repos.slint_repo_mirror}{self.repos.slint_repo_changelog}'
        self.compare[self.repos.slint_repo_name] = self.compare_dates()

    def sbo_repository(self) -> None:
        self.local_chg_txt: Path = Path(self.repos.sbo_repo_path, self.repos.sbo_repo_changelog)
        self.repo_chg_txt: str = f'{self.repos.sbo_repo_mirror}{self.repos.sbo_repo_changelog}'
        self.compare[self.repos.sbo_repo_name] = self.compare_dates()

    def ponce_repository(self) -> None:
        self.local_chg_txt: Path = Path(self.repos.ponce_repo_path, self.repos.ponce_repo_changelog)
        self.repo_chg_txt: str = f'{self.repos.ponce_repo_mirror}{self.repos.ponce_repo_changelog}'
        self.compare[self.repos.ponce_repo_name] = self.compare_dates()

    def compare_dates(self) -> bool:
        local_date: int = 0
        try:
            http = urllib3.PoolManager()
            repo = http.request('GET', self.repo_chg_txt)
        except KeyboardInterrupt:
            raise SystemExit(1)

        if self.local_chg_txt.is_file():
            local_date = int(os.stat(self.local_chg_txt).st_size)

        repo_date: int = int(repo.headers['Content-Length'])

        return repo_date != local_date

    def view_message(self) -> None:
        self.check()

        print()
        for repo, comp in self.compare.items():
            if comp:
                print(f"\n{self.endc}There are new updates available for the "
                      f"'{self.bgreen}{repo}{self.endc}' repository!")

        if True not in self.compare.values():
            print(f'\n{self.endc}{self.yellow}No updated packages since the last check.{self.endc}')

    def updates(self) -> None:
        message: str = 'Checking for news, please wait...'

        # Starting multiprocessing
        p1 = Process(target=self.view_message)
        p2 = Process(target=self.progress.bar, args=(message, ''))

        p1.start()
        p2.start()

        # Wait until process 1 finish
        p1.join()

        # Terminate process 2 if process 1 finished
        if not p1.is_alive():
            p2.terminate()

        # Wait until process 2 finish
        p2.join()

        # Restore the terminal cursor
        print('\x1b[?25h', self.endc)
