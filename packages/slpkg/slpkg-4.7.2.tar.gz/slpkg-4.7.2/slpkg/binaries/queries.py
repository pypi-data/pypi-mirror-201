#!/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import Union

from slpkg.configs import Configs
from slpkg.blacklist import Blacklist
from slpkg.repositories import Repositories
from slpkg.models.models import BinariesTable
from slpkg.models.models import session as Session


class BinQueries(Configs):
    """ Queries class for the sbo repository. """

    def __init__(self, name: str, repo: str):
        super(Configs, self).__init__()
        self.name: str = name
        self.repo: str = repo
        self.session = Session
        self.repos = Repositories()

        self.black = Blacklist()
        if self.name in self.black.packages():
            self.name: str = ''

    def count_packages(self):
        """ Counts the number of the packages. """
        count = self.session.query(
            BinariesTable.id).where(
            BinariesTable.repo == self.repo).count()

        return count

    def all_package_names_by_repo(self) -> list:
        """ Returns all the names of the binaries packages. """
        pkgs: tuple = self.session.query(
            BinariesTable.name).where(
            BinariesTable.repo == self.repo).all()

        return [pkg[0] for pkg in pkgs]

    def all_binaries_packages_by_repo(self) -> list:
        """ Returns all the binaries packages. """
        pkgs: tuple = self.session.query(
            BinariesTable.package).where(
            BinariesTable.repo == self.repo).all()

        return [pkg[0] for pkg in pkgs]

    def all_package_names_from_repositories(self) -> tuple:
        """ Returns the package name with the repo. """
        pkgs: tuple = self.session.query(
            BinariesTable.name, BinariesTable.repo).where(
            BinariesTable.repo.in_(self.repos.bin_enabled_repos)).all()

        if pkgs:
            return pkgs

        return ()

    def all_package_names_with_required(self) -> list:
        """ Returns all package with the dependencies. """
        required: list = self.session.query(
            BinariesTable.name, BinariesTable.required).where(
            BinariesTable.repo == self.repo).all()

        return required

    def repository(self) -> str:
        """ Return the repository name fo the package. """
        repository: tuple = self.session.query(
            BinariesTable.repo).filter(
            BinariesTable.name == self.name).where(
            BinariesTable.repo == self.repo).first()

        if repository:
            return repository[0]
        return ''

    def package_name(self) -> str:
        """ Returns the package name. """
        pkg: tuple = self.session.query(
            BinariesTable.name).filter(
            BinariesTable.name == self.name).where(
            BinariesTable.repo == self.repo).first()

        if pkg:
            return pkg[0]
        return ''

    def package_bin(self) -> str:
        """ Returns the binary package. """
        pkg: tuple = self.session.query(
            BinariesTable.package).filter(
            BinariesTable.name == self.name).where(
            BinariesTable.repo == self.repo).first()

        if pkg:
            return pkg[0]
        return ''

    def package_checksum(self) -> str:
        """ Returns the binary package checksum. """
        md5: tuple = self.session.query(
            BinariesTable.checksum).filter(
            BinariesTable.package == self.name).where(
            BinariesTable.repo == self.repo).first()

        if md5:
            return md5[0]
        return ''

    def version(self) -> str:
        """ Returns the package version. """
        pkg: tuple = self.session.query(
            BinariesTable.version).filter(
            BinariesTable.name == self.name).where(
            BinariesTable.repo == self.repo).first()

        if pkg:
            return pkg[0]
        return ''

    def mirror(self) -> str:
        """ Returns the package mirror. """
        mir: tuple = self.session.query(
            BinariesTable.mirror).filter(
            BinariesTable.name == self.name).where(
            BinariesTable.repo == self.repo).first()

        if mir:
            return mir[0]
        return ''

    def location(self) -> str:
        """ Returns the package location. """
        loc: tuple = self.session.query(
            BinariesTable.location).filter(
            BinariesTable.name == self.name).where(
            BinariesTable.repo == self.repo).first()

        if loc:
            return loc[0]
        return ''

    def size_comp(self) -> str:
        """ Returns the package comp size. """
        size: tuple = self.session.query(
            BinariesTable.size_comp).filter(
            BinariesTable.name == self.name).where(
            BinariesTable.repo == self.repo).first()

        if size:
            return size[0]
        return ''

    def unsize_comp(self) -> str:
        """ Returns the package uncomp size. """
        size: tuple = self.session.query(
            BinariesTable.unsize_comp).filter(
            BinariesTable.name == self.name).where(
            BinariesTable.repo == self.repo).first()

        if size:
            return size[0]
        return ''

    def required(self) -> Union[list, list]:
        """ Returns the package required. """
        requires: tuple = self.session.query(
            BinariesTable.required).filter(
            BinariesTable.name == self.name).where(
            BinariesTable.repo == self.repo).first()

        if requires and not requires[0] is None:
            requires: list = requires[0].split()
            for req in requires:
                if req in self.black.packages():
                    requires.remove(req)
            return requires
        return []

    def conflicts(self) -> str:
        """ Returns the package conflicts. """
        con: tuple = self.session.query(
            BinariesTable.conflicts).filter(
            BinariesTable.name == self.name).where(
            BinariesTable.repo == self.repo).first()

        if con:
            return con[0]
        return ''

    def suggests(self) -> str:
        """ Returns the package suggests. """
        sug: tuple = self.session.query(
            BinariesTable.suggests).filter(
            BinariesTable.name == self.name).where(
            BinariesTable.repo == self.repo).first()

        if sug:
            return sug[0]
        return ''

    def description(self) -> str:
        """ Returns the package description. """
        desc: tuple = self.session.query(
            BinariesTable.description).filter(
            BinariesTable.name == self.name).where(
            BinariesTable.repo == self.repo).first()

        if desc:
            return desc[0]
        return ''
