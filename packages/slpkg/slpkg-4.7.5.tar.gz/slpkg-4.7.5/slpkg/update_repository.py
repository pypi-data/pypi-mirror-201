#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path
from multiprocessing import Process, Queue

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.downloader import Downloader
from slpkg.views.views import ViewMessage
from slpkg.progress_bar import ProgressBar
from slpkg.install_data import InstallData
from slpkg.repositories import Repositories
from slpkg.check_updates import CheckUpdates
from slpkg.models.models import session as Session
from slpkg.models.models import (Base, engine, SBoTable,
                                 PonceTable, BinariesTable,
                                 LastRepoUpdated)


class UpdateRepository(Configs):
    """ Deletes and install the data. """

    def __init__(self, flags: list, repo: str):
        super(Configs, self).__init__()
        self.flags: list = flags
        self.repo: str = repo
        self.session = Session
        self.view = ViewMessage(self.flags)

        self.repos = Repositories()
        self.progress = ProgressBar()
        self.utils = Utilities()
        self.color = self.colour()
        self.data = InstallData()
        self.check_updates = CheckUpdates(
            self.flags, self.repo
        )

        if not self.repo:
            self.repo = self.repos.sbo_enabled_repository

        self.repos_for_update: dict = {}
        self.bold: str = self.color['bold']
        self.green: str = self.color['green']
        self.red: str = self.color['red']
        self.yellow: str = self.color['yellow']
        self.bgreen: str = f'{self.bold}{self.green}'
        self.bred: str = f'{self.bold}{self.red}'
        self.endc: str = self.color['endc']
        self.flag_generate: list = ['-G', '--generate-only']
        self.flag_bin_repository: list = ['-B', '--bin-repo=']

    def update_the_repositories(self) -> None:
        if not self.repos_for_update.values() or self.repo not in self.repos_for_update.keys():
            self.view.question()
        else:
            print()

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

                if repo == self.repo:
                    bin_repositories[repo]()
                    break

                if self.repo == '*':
                    bin_repositories[repo]()
        else:
            self.slackbuild_repositories()
        print()

    def slack_repository(self):
        if self.repos.slack_repo:
            urls: list = []
            print('Updating the packages list...\n')
            print(f"Downloading the '{self.green}{self.repos.slack_repo_name}{self.endc}"
                  f"' repository, please wait...\n")
            self.make_dirs(self.repos.slack_repo_name)

            urls.append(f'{self.repos.slack_repo_mirror}{self.repos.slack_repo_packages}')
            urls.append(f'{self.repos.slack_repo_mirror}{self.repos.slack_repo_changelog}')
            urls.append(f'{self.repos.slack_repo_mirror}{self.repos.slack_repo_checksums}')

            self.utils.remove_file_if_exists(self.repos.slack_repo_path, self.repos.slack_repo_packages)
            self.utils.remove_file_if_exists(self.repos.slack_repo_path, self.repos.slack_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.slack_repo_path, self.repos.slack_repo_checksums)

            down = Downloader(self.repos.slack_repo_path, urls, self.flags)
            down.download()
            print()

            self.delete_binaries_data(self.repos.slack_repo_name)
            self.delete_last_updated(self.repos.slack_repo_name)
            self.data.install_slack_data()
            print()
        else:
            self.not_enabled_message(self.repos.slack_repo_name)

    def slack_extra_repository(self):
        if self.repos.slack_extra_repo:
            urls: list = []
            print('Updating the packages list...\n')
            print(f"Downloading the '{self.green}{self.repos.slack_extra_repo_name}{self.endc}"
                  f"' repository, please wait...\n")
            self.make_dirs(self.repos.slack_extra_repo_name)

            urls.append(f'{self.repos.slack_extra_repo_packages_mirror}{self.repos.slack_extra_repo_packages}')
            urls.append(f'{self.repos.slack_extra_repo_mirror}{self.repos.slack_extra_repo_changelog}')
            urls.append(f'{self.repos.slack_extra_repo_mirror}{self.repos.slack_extra_repo_checksums}')

            self.utils.remove_file_if_exists(self.repos.slack_extra_repo_path,
                                             self.repos.slack_extra_repo_packages)
            self.utils.remove_file_if_exists(self.repos.slack_extra_repo_path,
                                             self.repos.slack_extra_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.slack_extra_repo_path,
                                             self.repos.slack_extra_repo_checksums)

            down = Downloader(self.repos.slack_extra_repo_path, urls, self.flags)
            down.download()
            print()

            self.delete_binaries_data(self.repos.slack_extra_repo_name)
            self.delete_last_updated(self.repos.slack_extra_repo_name)
            self.data.install_slack_extra_data()
            print()
        else:
            self.not_enabled_message(self.repos.slack_extra_repo_name)

    def slack_patches_repository(self):
        if self.repos.slack_patches_repo:
            urls: list = []
            print('Updating the packages list...\n')
            print(f"Downloading the '{self.green}{self.repos.slack_patches_repo_name}{self.endc}"
                  f"' repository, please wait...\n")
            self.make_dirs(self.repos.slack_patches_repo_name)

            urls.append(f'{self.repos.slack_patches_repo_packages_mirror}{self.repos.slack_patches_repo_packages}')
            urls.append(f'{self.repos.slack_patches_repo_mirror}{self.repos.slack_patches_repo_changelog}')
            urls.append(f'{self.repos.slack_patches_repo_mirror}{self.repos.slack_patches_repo_checksums}')

            self.utils.remove_file_if_exists(self.repos.slack_patches_repo_path,
                                             self.repos.slack_patches_repo_packages)
            self.utils.remove_file_if_exists(self.repos.slack_patches_repo_path,
                                             self.repos.slack_patches_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.slack_patches_repo_path,
                                             self.repos.slack_patches_repo_checksums)

            down = Downloader(self.repos.slack_patches_repo_path, urls, self.flags)
            down.download()
            print()

            self.delete_binaries_data(self.repos.slack_patches_repo_name)
            self.delete_last_updated(self.repos.slack_patches_repo_name)
            self.data.install_slack_patches_data()
            print()
        else:
            self.not_enabled_message(self.repos.slack_patches_repo_name)

    def alien_repository(self):
        if self.repos.alien_repo:
            urls: list = []
            print('Updating the packages list...\n')
            print(f"Downloading the '{self.green}{self.repos.alien_repo_name}{self.endc}' repository, please wait...\n")
            self.make_dirs(self.repos.alien_repo_name)

            urls.append(f'{self.repos.alien_repo_packages_mirror}{self.repos.alien_repo_packages}')
            urls.append(f'{self.repos.alien_repo_mirror}{self.repos.alien_repo_changelog}')
            urls.append(f'{self.repos.alien_repo_packages_mirror}{self.repos.alien_repo_checksums}')

            self.utils.remove_file_if_exists(self.repos.alien_repo_path, self.repos.alien_repo_packages)
            self.utils.remove_file_if_exists(self.repos.alien_repo_path, self.repos.alien_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.alien_repo_path, self.repos.alien_repo_checksums)

            down = Downloader(self.repos.alien_repo_path, urls, self.flags)
            down.download()
            print()

            self.delete_binaries_data(self.repos.alien_repo_name)
            self.delete_last_updated(self.repos.alien_repo_name)
            self.data.install_alien_data()
            print()
        else:
            self.not_enabled_message(self.repos.alien_repo_name)

    def multilib_repository(self) -> None:
        if self.repos.multilib_repo:
            urls: list = []
            print('Updating the packages list...\n')
            print(f"Downloading the '{self.green}{self.repos.multilib_repo_name}{self.endc}' "
                  f"repository, please wait...\n")
            self.make_dirs(self.repos.multilib_repo_name)

            urls.append(f'{self.repos.multilib_repo_packages_mirror}{self.repos.multilib_repo_packages}')
            urls.append(f'{self.repos.multilib_repo_mirror}{self.repos.multilib_repo_changelog}')
            urls.append(f'{self.repos.multilib_repo_mirror}{self.repos.multilib_repo_checksums}')

            self.utils.remove_file_if_exists(self.repos.multilib_repo_path, self.repos.multilib_repo_packages)
            self.utils.remove_file_if_exists(self.repos.multilib_repo_path, self.repos.multilib_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.multilib_repo_path, self.repos.multilib_repo_checksums)

            down = Downloader(self.repos.multilib_repo_path, urls, self.flags)
            down.download()
            print()

            self.delete_binaries_data(self.repos.multilib_repo_name)
            self.delete_last_updated(self.repos.multilib_repo_name)
            self.data.install_multilib_data()
            print()
        else:
            self.not_enabled_message(self.repos.multilib_repo_name)

    def restricted_repository(self) -> None:
        if self.repos.restricted_repo:
            urls: list = []
            print('Updating the packages list...\n')
            print(f"Downloading the '{self.green}{self.repos.restricted_repo_name}{self.endc}' "
                  f"repository, please wait...\n")
            self.make_dirs(self.repos.restricted_repo_name)

            urls.append(f'{self.repos.restricted_repo_packages_mirror}{self.repos.restricted_repo_packages}')
            urls.append(f'{self.repos.restricted_repo_mirror}{self.repos.restricted_repo_changelog}')
            urls.append(f'{self.repos.restricted_repo_packages_mirror}{self.repos.restricted_repo_checksums}')

            self.utils.remove_file_if_exists(self.repos.restricted_repo_path, self.repos.restricted_repo_packages)
            self.utils.remove_file_if_exists(self.repos.restricted_repo_path, self.repos.restricted_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.restricted_repo_path, self.repos.restricted_repo_checksums)

            down = Downloader(self.repos.restricted_repo_path, urls, self.flags)
            down.download()
            print()

            self.delete_binaries_data(self.repos.restricted_repo_name)
            self.delete_last_updated(self.repos.restricted_repo_name)
            self.data.install_restricted_data()
            print()
        else:
            self.not_enabled_message(self.repos.restricted_repo_name)

    def gnome_repository(self) -> None:
        if self.repos.gnome_repo:
            urls: list = []
            print('Updating the packages list...\n')
            print(f"Downloading the '{self.green}{self.repos.gnome_repo_name}{self.endc}' repository, please wait...\n")
            self.make_dirs(self.repos.gnome_repo_name)

            urls.append(f'{self.repos.gnome_repo_mirror}{self.repos.gnome_repo_packages}')
            urls.append(f'{self.repos.gnome_repo_mirror}{self.repos.gnome_repo_changelog}')
            urls.append(f'{self.repos.gnome_repo_mirror}{self.repos.gnome_repo_checksums}')

            self.utils.remove_file_if_exists(self.repos.gnome_repo_path, self.repos.gnome_repo_packages)
            self.utils.remove_file_if_exists(self.repos.gnome_repo_path, self.repos.gnome_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.gnome_repo_path, self.repos.gnome_repo_checksums)

            down = Downloader(self.repos.gnome_repo_path, urls, self.flags)
            down.download()
            print()

            self.delete_binaries_data(self.repos.gnome_repo_name)
            self.delete_last_updated(self.repos.gnome_repo_name)
            self.data.install_gnome_data()
            print()
        else:
            self.not_enabled_message(self.repos.gnome_repo_name)

    def msb_repository(self) -> None:
        if self.repos.msb_repo:
            urls: list = []
            print('Updating the packages list...\n')
            print(f"Downloading the '{self.green}{self.repos.msb_repo_name}{self.endc}' "
                  f"repository, please wait...\n")
            self.make_dirs(self.repos.msb_repo_name)

            urls.append(f'{self.repos.msb_repo_packages_mirror}{self.repos.msb_repo_packages}')
            urls.append(f'{self.repos.msb_repo_mirror}{self.repos.msb_repo_changelog}')
            urls.append(f'{self.repos.msb_repo_mirror}{self.repos.msb_repo_checksums}')

            self.utils.remove_file_if_exists(self.repos.msb_repo_path,
                                             self.repos.msb_repo_packages)
            self.utils.remove_file_if_exists(self.repos.msb_repo_path,
                                             self.repos.msb_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.msb_repo_path,
                                             self.repos.msb_repo_checksums)

            down = Downloader(self.repos.msb_repo_path, urls, self.flags)
            down.download()
            print()

            self.delete_binaries_data(self.repos.msb_repo_name)
            self.delete_last_updated(self.repos.msb_repo_name)
            self.data.install_msb_data()
            print()
        else:
            self.not_enabled_message(self.repos.msb_repo_name)

    def csb_repository(self) -> None:
        if self.repos.csb_repo:
            urls: list = []
            print('Updating the packages list...\n')
            print(f"Downloading the '{self.green}{self.repos.csb_repo_name}{self.endc}' "
                  f"repository, please wait...\n")
            self.make_dirs(self.repos.csb_repo_name)

            urls.append(f'{self.repos.csb_repo_packages_mirror}{self.repos.csb_repo_packages}')
            urls.append(f'{self.repos.csb_repo_mirror}{self.repos.csb_repo_changelog}')
            urls.append(f'{self.repos.csb_repo_mirror}{self.repos.csb_repo_checksums}')

            self.utils.remove_file_if_exists(self.repos.csb_repo_path,
                                             self.repos.csb_repo_packages)
            self.utils.remove_file_if_exists(self.repos.csb_repo_path,
                                             self.repos.csb_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.csb_repo_path,
                                             self.repos.csb_repo_checksums)

            down = Downloader(self.repos.csb_repo_path, urls, self.flags)
            down.download()
            print()

            self.delete_binaries_data(self.repos.csb_repo_name)
            self.delete_last_updated(self.repos.csb_repo_name)
            self.data.install_csb_data()
            print()
        else:
            self.not_enabled_message(self.repos.csb_repo_name)

    def conraid_repository(self) -> None:
        if self.repos.conraid_repo:
            urls: list = []
            print('Updating the packages list...\n')
            print(f"Downloading the '{self.green}{self.repos.conraid_repo_name}{self.endc}' "
                  f"repository, please wait...\n")
            self.make_dirs(self.repos.conraid_repo_name)

            urls.append(f'{self.repos.conraid_repo_mirror}{self.repos.conraid_repo_packages}')
            urls.append(f'{self.repos.conraid_repo_mirror}{self.repos.conraid_repo_changelog}')
            urls.append(f'{self.repos.conraid_repo_mirror}{self.repos.conraid_repo_checksums}')

            self.utils.remove_file_if_exists(self.repos.conraid_repo_path, self.repos.conraid_repo_packages)
            self.utils.remove_file_if_exists(self.repos.conraid_repo_path, self.repos.conraid_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.conraid_repo_path, self.repos.conraid_repo_checksums)

            down = Downloader(self.repos.conraid_repo_path, urls, self.flags)
            down.download()
            print()

            self.delete_binaries_data(self.repos.conraid_repo_name)
            self.delete_last_updated(self.repos.conraid_repo_name)
            self.data.install_conraid_data()
            print()
        else:
            self.not_enabled_message(self.repos.conraid_repo_name)

    def slackonly_repository(self) -> None:
        if self.repos.slackonly_repo:
            urls: list = []
            print('Updating the packages list...\n')
            print(f"Downloading the '{self.green}{self.repos.slackonly_repo_name}{self.endc}' "
                  f"repository, please wait...\n")
            self.make_dirs(self.repos.slackonly_repo_name)

            urls.append(f'{self.repos.slackonly_repo_mirror}{self.repos.slackonly_repo_packages}')
            urls.append(f'{self.repos.slackonly_repo_mirror}{self.repos.slackonly_repo_changelog}')
            urls.append(f'{self.repos.slackonly_repo_mirror}{self.repos.slackonly_repo_checksums}')

            self.utils.remove_file_if_exists(self.repos.slackonly_repo_path, self.repos.slackonly_repo_packages)
            self.utils.remove_file_if_exists(self.repos.slackonly_repo_path, self.repos.slackonly_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.slackonly_repo_path, self.repos.slackonly_repo_checksums)

            down = Downloader(self.repos.slackonly_repo_path, urls, self.flags)
            down.download()
            print()

            self.delete_binaries_data(self.repos.slackonly_repo_name)
            self.delete_last_updated(self.repos.slackonly_repo_name)
            self.data.install_slackonly_data()
            print()
        else:
            self.not_enabled_message(self.repos.slackonly_repo_name)

    def salixos_repository(self) -> None:
        if self.repos.salixos_repo:
            urls: list = []
            print('Updating the packages list...\n')
            print(f"Downloading the '{self.green}{self.repos.salixos_repo_name}{self.endc}' "
                  f"repository, please wait...\n")
            self.make_dirs(self.repos.salixos_repo_name)

            urls.append(f'{self.repos.salixos_repo_mirror}{self.repos.salixos_repo_packages}')
            urls.append(f'{self.repos.salixos_repo_mirror}{self.repos.salixos_repo_changelog}')
            urls.append(f'{self.repos.salixos_repo_mirror}{self.repos.salixos_repo_checksums}')

            self.utils.remove_file_if_exists(self.repos.salixos_repo_path, self.repos.salixos_repo_packages)
            self.utils.remove_file_if_exists(self.repos.salixos_repo_path, self.repos.salixos_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.salixos_repo_path, self.repos.salixos_repo_checksums)

            down = Downloader(self.repos.salixos_repo_path, urls, self.flags)
            down.download()
            print()

            self.delete_binaries_data(self.repos.salixos_repo_name)
            self.delete_last_updated(self.repos.salixos_repo_name)
            self.data.install_salixos_data()
            print()
        else:
            self.not_enabled_message(self.repos.salixos_repo_name)

    def salixos_extra_repository(self) -> None:
        if self.repos.salixos_extra_repo:
            urls: list = []
            print('Updating the packages list...\n')
            print(f"Downloading the '{self.green}{self.repos.salixos_extra_repo_name}{self.endc}' "
                  f"repository, please wait...\n")
            self.make_dirs(self.repos.salixos_extra_repo_name)

            urls.append(f'{self.repos.salixos_extra_repo_packages_mirror}{self.repos.salixos_extra_repo_packages}')
            urls.append(f'{self.repos.salixos_extra_repo_mirror}{self.repos.salixos_extra_repo_changelog}')
            urls.append(f'{self.repos.salixos_extra_repo_mirror}{self.repos.salixos_extra_repo_checksums}')

            self.utils.remove_file_if_exists(self.repos.salixos_extra_repo_path,
                                             self.repos.salixos_extra_repo_packages)
            self.utils.remove_file_if_exists(self.repos.salixos_extra_repo_path,
                                             self.repos.salixos_extra_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.salixos_extra_repo_path,
                                             self.repos.salixos_extra_repo_checksums)

            down = Downloader(self.repos.salixos_extra_repo_path, urls, self.flags)
            down.download()
            print()

            self.delete_binaries_data(self.repos.salixos_extra_repo_name)
            self.delete_last_updated(self.repos.salixos_extra_repo_name)
            self.data.install_salixos_extra_data()
            print()
        else:
            self.not_enabled_message(self.repos.salixos_extra_repo_name)

    def salixos_patches_repository(self) -> None:
        if self.repos.salixos_patches_repo:
            urls: list = []
            print('Updating the packages list...\n')
            print(f"Downloading the '{self.green}{self.repos.salixos_patches_repo_name}{self.endc}' "
                  f"repository, please wait...\n")
            self.make_dirs(self.repos.salixos_patches_repo_name)

            urls.append(f'{self.repos.salixos_patches_repo_packages_mirror}{self.repos.salixos_patches_repo_packages}')
            urls.append(f'{self.repos.salixos_patches_repo_mirror}{self.repos.salixos_patches_repo_changelog}')
            urls.append(f'{self.repos.salixos_patches_repo_mirror}{self.repos.salixos_patches_repo_checksums}')

            self.utils.remove_file_if_exists(self.repos.salixos_patches_repo_path,
                                             self.repos.salixos_patches_repo_packages)
            self.utils.remove_file_if_exists(self.repos.salixos_patches_repo_path,
                                             self.repos.salixos_patches_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.salixos_patches_repo_path,
                                             self.repos.salixos_patches_repo_checksums)

            down = Downloader(self.repos.salixos_patches_repo_path, urls, self.flags)
            down.download()
            print()

            self.delete_binaries_data(self.repos.salixos_patches_repo_name)
            self.delete_last_updated(self.repos.salixos_patches_repo_name)
            self.data.install_salixos_patches_data()
            print()
        else:
            self.not_enabled_message(self.repos.salixos_patches_repo_name)

    def slackel_repository(self) -> None:
        if self.repos.slackel_repo:
            urls: list = []
            print('Updating the packages list...\n')
            print(f"Downloading the '{self.green}{self.repos.slackel_repo_name}{self.endc}' "
                  f"repository, please wait...\n")
            self.make_dirs(self.repos.slackel_repo_name)

            urls.append(f'{self.repos.slackel_repo_mirror}{self.repos.slackel_repo_packages}')
            urls.append(f'{self.repos.slackel_repo_mirror}{self.repos.slackel_repo_changelog}')
            urls.append(f'{self.repos.slackel_repo_mirror}{self.repos.slackel_repo_checksums}')

            self.utils.remove_file_if_exists(self.repos.slackel_repo_path, self.repos.slackel_repo_packages)
            self.utils.remove_file_if_exists(self.repos.slackel_repo_path, self.repos.slackel_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.slackel_repo_path, self.repos.slackel_repo_checksums)

            down = Downloader(self.repos.slackel_repo_path, urls, self.flags)
            down.download()
            print()

            self.delete_binaries_data(self.repos.slackel_repo_name)
            self.delete_last_updated(self.repos.slackel_repo_name)
            self.data.install_slackel_data()
            print()
        else:
            self.not_enabled_message(self.repos.slackel_repo_name)

    def slint_repository(self) -> None:
        if self.repos.slint_repo:
            urls: list = []
            print('Updating the packages list...\n')
            print(f"Downloading the '{self.green}{self.repos.slint_repo_name}{self.endc}' "
                  f"repository, please wait...\n")
            self.make_dirs(self.repos.slint_repo_name)

            urls.append(f'{self.repos.slint_repo_mirror}{self.repos.slint_repo_packages}')
            urls.append(f'{self.repos.slint_repo_mirror}{self.repos.slint_repo_changelog}')
            urls.append(f'{self.repos.slint_repo_mirror}{self.repos.slint_repo_checksums}')

            self.utils.remove_file_if_exists(self.repos.slint_repo_path, self.repos.slint_repo_packages)
            self.utils.remove_file_if_exists(self.repos.slint_repo_path, self.repos.slint_repo_changelog)
            self.utils.remove_file_if_exists(self.repos.slint_repo_path, self.repos.slint_repo_checksums)

            down = Downloader(self.repos.slint_repo_path, urls, self.flags)
            down.download()
            print()

            self.delete_binaries_data(self.repos.slint_repo_name)
            self.delete_last_updated(self.repos.slint_repo_name)
            self.data.install_slint_data()
            print()
        else:
            self.not_enabled_message(self.repos.slint_repo_name)

    def slackbuild_repositories(self) -> None:
        """ Update the slackbuild repositories. """
        if self.repos.ponce_repo:
            self.make_dirs(self.repos.gnome_repo_name)
            if not self.utils.is_option(self.flag_generate, self.flags):
                print('Updating the packages list...\n')
                print(f"Downloading the '{self.green}{self.repos.ponce_repo_name}"
                      f"{self.endc}' repository, please wait...\n")
                self.utils.remove_file_if_exists(self.repos.ponce_repo_path, self.repos.ponce_repo_slackbuilds)
                lftp_command: str = (f'lftp {self.lftp_mirror_options} {self.repos.ponce_repo_mirror} '
                                     f'{self.repos.ponce_repo_path}')
                self.utils.process(lftp_command)

            # Remove the SLACKBUILDS.TXT file before generating the new one.
            sbo_file_txt = Path(self.repos.ponce_repo_path, self.repos.ponce_repo_slackbuilds)
            if sbo_file_txt.is_file():
                sbo_file_txt.unlink()

            # Generating the ponce SLACKBUILDS.TXT file.
            print(f'Generating the {self.repos.ponce_repo_slackbuilds} file... ', end='', flush=True)
            os.chdir(self.repos.ponce_repo_path)
            gen_command: str = f'./gen_sbo_txt.sh > {self.repos.ponce_repo_slackbuilds}'
            self.utils.process(gen_command)
            self.delete_last_updated(self.repos.ponce_repo_name)
            print('\n')

        else:
            self.make_dirs(self.repos.sbo_repo_name)
            print('Updating the packages list...\n')

            self.utils.remove_file_if_exists(self.repos.sbo_repo_path, self.repos.sbo_repo_slackbuilds)
            self.utils.remove_file_if_exists(self.repos.sbo_repo_path, self.repos.sbo_repo_changelog)

            print(f"Downloading the '{self.green}{self.repos.sbo_repo_name}{self.endc}' repository, please wait...\n")
            lftp_command: str = (f'lftp {self.lftp_mirror_options} {self.repos.sbo_repo_mirror} '
                                 f'{self.repos.sbo_repo_path}')
            self.utils.process(lftp_command)
            self.delete_last_updated(self.repos.sbo_repo_name)

        self.delete_sbo_data()
        self.data.install_sbos_data()

    def not_enabled_message(self, repo: str) -> None:
        print(f"{self.prog_name}: Repository '{self.green}{repo}{self.endc}' is not enabled.")

    def make_dirs(self, repo) -> None:
        path = Path(self.lib_path, 'repositories', repo)
        if not os.path.isdir(path):
            os.makedirs(path)

    def check(self, queue) -> None:
        compare = self.check_updates.check()
        is_update: dict = {}

        print()
        for repo, comp in compare.items():
            if comp:
                print(f"\n{self.endc}There are new updates available for the "
                      f"'{self.bgreen}{repo}{self.endc}' repository!")
                is_update[repo] = comp

        if True not in compare.values():
            print(f'\n{self.endc}{self.yellow}No changes in ChangeLog.txt between your '
                  f'last update and now.{self.endc}')

        return queue.put(is_update)

    def repositories(self) -> None:
        queue = Queue()
        message = f'Checking for news, please wait...'

        # Starting multiprocessing
        p1 = Process(target=self.check, args=(queue,))
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
        print('\x1b[?25h', self.endc, end='')

        self.repos_for_update = queue.get()
        self.update_the_repositories()

    def delete_sbo_data(self) -> None:
        """ Delete all the data from a table of the database. """
        if self.repos.ponce_repo:
            self.session.query(PonceTable).delete()
        else:
            self.session.query(SBoTable).delete()
        self.session.commit()

    def delete_binaries_data(self, repo) -> None:
        """ Delete the repository data from a table of the database. """
        self.session.query(BinariesTable).where(BinariesTable.repo == repo).delete()
        self.session.commit()

    def delete_last_updated(self, repo) -> None:
        """ Deletes the last updated date. """
        self.session.query(LastRepoUpdated).where(LastRepoUpdated.repo == repo).delete()
        self.session.commit()

    def drop_the_tables(self) -> None:
        """ Drop all the tables from the database. """
        print(f'\n{self.prog_name}: {self.bred}WARNING{self.endc}: All the data from the database will be deleted!')
        self.view.question()

        tables: list = [
            PonceTable.__table__,
            SBoTable.__table__,
            BinariesTable.__table__,
            LastRepoUpdated.__table__
        ]

        Base.metadata.drop_all(bind=engine, tables=tables)
        print("Successfully cleared!\n\nYou need to run 'slpkg update' now.")
