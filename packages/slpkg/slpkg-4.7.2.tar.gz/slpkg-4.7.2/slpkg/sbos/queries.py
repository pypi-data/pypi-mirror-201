#!/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import Union
from sqlalchemy import inspect

from slpkg.configs import Configs
from slpkg.blacklist import Blacklist
from slpkg.repositories import Repositories
from slpkg.models.models import session as Session
from slpkg.models.models import SBoTable, PonceTable


class SBoQueries(Configs):
    """ Queries class for the sbo repository. """

    def __init__(self, name: str):
        super(Configs, self).__init__()
        self.name: str = name
        self.session = Session
        self.repos = Repositories()

        self.black = Blacklist()
        if self.name in self.black.packages():
            self.name: str = ''

        # Switch between sbo and ponce repository.
        self.sbo_table = SBoTable
        if self.repos.ponce_repo:
            self.sbo_table = PonceTable

    def count_packages(self):
        """ Counts the number of the packages. """
        count = self.session.query(
            self.sbo_table.id).count()

        return count

    def repo_name(self):
        """ Returns the repo name by the table. """
        table = inspect(self.sbo_table)
        repo = self.repos.sbo_repo_name
        if table.tables[0].name == 'poncetable':
            repo = self.repos.ponce_repo_name

        return repo

    def sbos(self) -> list:
        """ Returns all the slackbuilds. """
        sbos: tuple = self.session.query(self.sbo_table.name).all()  # type: ignore
        return [sbo[0] for sbo in sbos]

    def slackbuild(self) -> str:
        """ Returns a slackbuild. """
        sbo: tuple = self.session.query(
            self.sbo_table.name).filter(self.sbo_table.name == self.name).first()  # type: ignore

        if sbo:
            return sbo[0]
        return ''

    def location(self) -> str:
        """ Returns the category of a slackbuild. """
        location: tuple = self.session.query(
            self.sbo_table.location).filter(self.sbo_table.name == self.name).first()  # type: ignore

        if location:
            return location[0]
        return ''

    def sources(self) -> list:
        """ Returns the source of a slackbuild. """
        source, source64 = self.session.query(
            self.sbo_table.download, self.sbo_table.download64).filter(  # type: ignore
                self.sbo_table.name == self.name).first()

        if self.os_arch == 'x86_64' and source64:
            return source64.split()

        return source.split()

    def requires(self) -> Union[str, list]:
        """ Returns the requirements of a slackbuild. """
        requires: tuple = self.session.query(
            self.sbo_table.requires).filter(
                self.sbo_table.name == self.name).first()

        if requires:
            requires: list = requires[0].split()
            for req in requires:
                if req in self.black.packages():
                    requires.remove(req)
            return requires
        return ''

    def version(self) -> str:
        """ Returns the version of a slackbuild. """
        version: tuple = self.session.query(
            self.sbo_table.version).filter(  # type: ignore
                self.sbo_table.name == self.name).first()

        if version:
            return version[0]
        return ''

    def checksum(self) -> list:
        """ Returns the source checksum. """
        mds5, md5s64 = self.session.query(
            self.sbo_table.md5sum, self.sbo_table.md5sum64).filter(  # type: ignore
                self.sbo_table.name == self.name).first()

        if self.os_arch == 'x86_64' and md5s64:
            return md5s64.split()

        return mds5.split()

    def description(self) -> str:
        """ Returns the slackbuild description. """
        desc: tuple = self.session.query(
            self.sbo_table.short_description).filter(  # type: ignore
                self.sbo_table.name == self.name).first()

        if desc:
            return desc[0]
        return ''

    def files(self) -> str:
        """ Returns the files of a slackbuild. """
        files: tuple = self.session.query(
            self.sbo_table.files).filter(  # type: ignore
                self.sbo_table.name == self.name).first()

        if files:
            return files[0]
        return ''

    def all_sbo_and_requires(self) -> list:
        """ Returns all package with the dependencies. """
        requires: list = self.session.query(
            self.sbo_table.name, self.sbo_table.requires).all()

        return requires
