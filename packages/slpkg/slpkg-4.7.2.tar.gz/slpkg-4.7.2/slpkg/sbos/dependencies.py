#!/usr/bin/python3
# -*- coding: utf-8 -*-

from slpkg.sbos.queries import SBoQueries


class Requires:
    """ Creates a list of dependencies with
    the right order to install. """

    def __init__(self, name: str):
        self.name: str = name
        self.repo_slackbuilds_names: list = SBoQueries(self.name).sbos()

    def resolve(self) -> list:
        """ Resolve the dependencies. """
        requires: list[str] = SBoQueries(self.name).requires()

        for req in requires:

            # Remove requirements that are included as dependencies,
            # but are not included in the repository.
            if req not in self.repo_slackbuilds_names:
                requires.remove(req)

            if req:
                sub_requires: list[str] = SBoQueries(req).requires()
                for sub in sub_requires:
                    requires.append(sub)

        requires.reverse()

        return list(dict.fromkeys(requires))
