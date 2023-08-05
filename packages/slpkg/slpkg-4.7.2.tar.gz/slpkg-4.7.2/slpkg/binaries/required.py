#!/usr/bin/python3
# -*- coding: utf-8 -*-

from slpkg.repositories import Repositories
from slpkg.binaries.queries import BinQueries


class Required:
    """ Creates a list of dependencies with
    the right order to install. """

    def __init__(self, name: str, repo: str):
        self.name: str = name
        self.repo: str = repo
        self.repos = Repositories()
        self.repo_package_names: list = BinQueries(
            self.name, self.repo).all_package_names_by_repo()

        self.special_repos: list = [
            self.repos.salixos_repo_name,
            self.repos.salixos_extra_repo_name,
            self.repos.slackel_repo_name,
            self.repos.slint_repo_name
        ]

    def resolve(self) -> list:
        """ Resolve the dependencies. """
        required: list[str] = BinQueries(self.name, self.repo).required()

        # Resolve dependencies for some special repos.
        if self.repo in self.special_repos:
            requires: list = []
            for req in required:
                if req in self.repo_package_names:
                    requires.append(req)
            return requires

        for req in required:

            # Remove requirements that are included as dependencies,
            # but are not included in the repository.
            if req not in self.repo_package_names:
                required.remove(req)

            if req:
                sub_required: list[str] = BinQueries(req, self.repo).required()

                for sub in sub_required:
                    required.append(sub)

        # Clean for dependencies not in the repository.
        for dep in required:
            if dep not in self.repo_package_names:
                required.remove(dep)

        required.reverse()

        return list(dict.fromkeys(required))
