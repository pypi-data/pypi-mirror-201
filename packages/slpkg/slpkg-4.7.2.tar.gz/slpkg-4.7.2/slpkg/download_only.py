#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import shutil
from pathlib import Path

from slpkg.configs import Configs
from slpkg.utilities import Utilities
from slpkg.downloader import Downloader
from slpkg.views.views import ViewMessage
from slpkg.sbos.queries import SBoQueries
from slpkg.repositories import Repositories
from slpkg.binaries.queries import BinQueries
from slpkg.models.models import session as Session


class Download(Configs):
    """ Download the slackbuilds with the sources only. """

    def __init__(self, directory: Path, flags: list):
        super(Configs, self).__init__()
        self.flags: list = flags
        self.directory: Path = directory

        self.repos = Repositories()
        self.utils = Utilities()
        self.session = Session

        self.flag_directory: list = ['-z', '--directory=']
        self.flag_bin_repository: list = ['-B', '--bin-repo=']

    def packages(self, packages: list, repo=None) -> None:
        """ Download the package only. """
        packages: list = self.utils.apply_package_pattern(self.flags, packages, repo)
        view = ViewMessage(self.flags, repo)
        view.download_packages(packages, self.directory)
        view.question()

        download_path: Path = self.download_only_path
        if self.utils.is_option(self.flag_directory, self.flags):
            download_path: Path = self.directory

        start: float = time.time()
        urls: list = []
        for pkg in packages:

            if self.utils.is_option(self.flag_bin_repository, self.flags):
                mirror: str = BinQueries(pkg, repo).mirror()
                location: str = BinQueries(pkg, repo).location()
                package: str = BinQueries(pkg, repo).package_bin()
                urls.append(f'{mirror}{location}/{package}')
            else:
                location: str = SBoQueries(pkg).location()
                sources = SBoQueries(pkg).sources()
                urls += sources

                if self.repos.ponce_repo:
                    ponce_repo_path_package = Path(self.repos.ponce_repo_path, location, pkg)
                    shutil.copytree(ponce_repo_path_package, Path(download_path, pkg))
                else:
                    file: str = f'{pkg}{self.repos.sbo_repo_tar_suffix}'
                    urls += [f'{self.repos.sbo_repo_mirror}{location}/{file}']

        down = Downloader(download_path, urls, self.flags)
        down.download()

        elapsed_time: float = time.time() - start
        self.utils.finished_time(elapsed_time)
