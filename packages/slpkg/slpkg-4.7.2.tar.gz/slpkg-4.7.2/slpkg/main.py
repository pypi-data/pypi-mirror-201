#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path

from slpkg.checks import Check
from slpkg.upgrade import Upgrade
from slpkg.configs import Configs
from slpkg.tracking import Tracking
from slpkg.repo_info import RepoInfo
from slpkg.dependees import Dependees
from slpkg.utilities import Utilities
from slpkg.search import SearchPackage
from slpkg.views.cli_menu import Usage
from slpkg.dialog_box import DialogBox
from slpkg.views.version import Version
from slpkg.download_only import Download
from slpkg.views.views import ViewMessage
from slpkg.sbos.queries import SBoQueries
from slpkg.form_configs import FormConfigs
from slpkg.views.help_commands import Help
from slpkg.repositories import Repositories
from slpkg.binaries.install import Packages
from slpkg.check_updates import CheckUpdates
from slpkg.sbos.slackbuild import Slackbuilds
from slpkg.binaries.queries import BinQueries
from slpkg.find_installed import FindInstalled
from slpkg.views.view_package import ViewPackage
from slpkg.remove_packages import RemovePackages
from slpkg.clean_logs import CleanLogsDependencies
from slpkg.update_repository import UpdateRepository


class Argparse(Configs):

    def __init__(self, args: list):
        super(Configs).__init__()
        self.args: list = args
        self.flags: list = []
        self.directory = self.tmp_slpkg
        self.dialogbox = DialogBox()
        self.utils = Utilities()
        self.usage = Usage()
        self.form_configs = FormConfigs()
        self.color = self.colour()
        self.repos = Repositories()

        self.bold: str = self.color['bold']
        self.red: str = self.color['red']
        self.endc: str = self.color['endc']
        self.bred: str = f'{self.bold}{self.red}'
        self.binary_repo = None

        if len(self.args) == 0 or '' in self.args:
            self.usage.help_short(1)

        self.flag_yes: str = '--yes'
        self.flag_short_yes: str = '-y'
        self.flag_jobs: str = '--jobs'
        self.flag_short_jobs: str = '-j'
        self.flag_resolve_off: str = '--resolve-off'
        self.flag_short_resolve_off: str = '-o'
        self.flag_reinstall: str = '--reinstall'
        self.flag_short_reinstall: str = '-r'
        self.flag_skip_installed: str = '--skip-installed'
        self.flag_short_skip_installed: str = '-k'
        self.flag_full_reverse: str = '--full-reverse'
        self.flag_short_full_reverse: str = '-E'
        self.flag_search: str = '--search'
        self.flag_short_search: str = '-S'
        self.flag_no_silent: str = '--no-silent'
        self.flag_short_no_silent: str = '-n'
        self.flag_pkg_version: str = '--pkg-version'
        self.flag_short_pkg_version: str = '-p'
        self.flag_generate: str = '--generate-only'
        self.flag_short_generate: str = '-G'
        self.flag_parallel: str = '--parallel'
        self.flag_short_parallel: str = '-P'
        self.flag_bin_repository: str = '--bin-repo='
        self.flag_short_bin_repository: str = '-B'
        self.flag_directory: str = '--directory='
        self.flag_short_directory: str = '-z'

        self.flag_searches: list = [self.flag_short_search, self.flag_search]
        self.flag_binaries: list = [self.flag_short_bin_repository, self.flag_bin_repository]

        self.options: list = [
            self.flag_yes,
            self.flag_short_yes,
            self.flag_jobs,
            self.flag_short_jobs,
            self.flag_resolve_off,
            self.flag_short_resolve_off,
            self.flag_reinstall,
            self.flag_short_reinstall,
            self.flag_skip_installed,
            self.flag_short_skip_installed,
            self.flag_full_reverse,
            self.flag_short_full_reverse,
            self.flag_search,
            self.flag_short_search,
            self.flag_no_silent,
            self.flag_short_no_silent,
            self.flag_pkg_version,
            self.flag_short_pkg_version,
            self.flag_generate,
            self.flag_short_generate,
            self.flag_parallel,
            self.flag_short_parallel,
            self.flag_bin_repository,
            self.flag_short_bin_repository,
            self.flag_directory,
            self.flag_short_directory,
        ]

        self.commands: dict = {
            '--help': [],
            '--version': [],
            'help': [],
            'update': [
                self.flag_yes,
                self.flag_short_yes,
                self.flag_generate,
                self.flag_short_generate,
                self.flag_bin_repository,
                self.flag_short_bin_repository,
                self.flag_parallel,
                self.flag_short_parallel
            ],
            'upgrade': [
                self.flag_yes,
                self.flag_short_yes,
                self.flag_jobs,
                self.flag_short_jobs,
                self.flag_resolve_off,
                self.flag_short_resolve_off,
                self.flag_reinstall,
                self.flag_short_reinstall,
                self.flag_no_silent,
                self.flag_short_no_silent,
                self.flag_bin_repository,
                self.flag_short_bin_repository,
                self.flag_parallel,
                self.flag_short_parallel
            ],
            'check-updates': [
                self.flag_bin_repository,
                self.flag_short_bin_repository
            ],
            'repo-info': [],
            'configs': [],
            'clean-logs': [
                self.flag_yes,
                self.flag_short_yes
            ],
            'clean-data': [
                self.flag_yes,
                self.flag_short_yes
            ],
            'clean-tmp': [],
            'build': [
                self.flag_yes,
                self.flag_short_yes,
                self.flag_jobs,
                self.flag_short_jobs,
                self.flag_resolve_off,
                self.flag_short_resolve_off,
                self.flag_search,
                self.flag_short_search,
                self.flag_no_silent,
                self.flag_short_no_silent,
                self.flag_parallel,
                self.flag_short_parallel
            ],
            'install': [
                self.flag_yes,
                self.flag_short_yes,
                self.flag_jobs,
                self.flag_short_jobs,
                self.flag_resolve_off,
                self.flag_short_resolve_off,
                self.flag_reinstall,
                self.flag_short_reinstall,
                self.flag_skip_installed,
                self.flag_short_skip_installed,
                self.flag_search,
                self.flag_short_search,
                self.flag_no_silent,
                self.flag_short_no_silent,
                self.flag_bin_repository,
                self.flag_short_bin_repository,
                self.flag_parallel,
                self.flag_short_parallel
            ],
            'download': [
                self.flag_yes,
                self.flag_short_yes,
                self.flag_search,
                self.flag_short_search,
                self.flag_directory,
                self.flag_short_directory,
                self.flag_bin_repository,
                self.flag_short_bin_repository,
                self.flag_parallel,
                self.flag_short_parallel
            ],
            'remove': [
                self.flag_resolve_off,
                self.flag_short_resolve_off,
                self.flag_search,
                self.flag_short_search,
                self.flag_no_silent,
                self.flag_short_no_silent,
            ],
            'find': [
                self.flag_search,
                self.flag_short_search,
            ],
            'view': [
                self.flag_search,
                self.flag_short_search,
                self.flag_bin_repository,
                self.flag_short_bin_repository,
                self.flag_pkg_version,
                self.flag_short_pkg_version
            ],
            'search': [
                self.flag_search,
                self.flag_short_search,
                self.flag_bin_repository,
                self.flag_short_bin_repository
            ],
            'dependees': [
                self.flag_full_reverse,
                self.flag_short_full_reverse,
                self.flag_search,
                self.flag_short_search,
                self.flag_bin_repository,
                self.flag_short_bin_repository,
                self.flag_pkg_version,
                self.flag_short_pkg_version
            ],
            'tracking': [
                self.flag_search,
                self.flag_short_search,
                self.flag_pkg_version,
                self.flag_short_pkg_version,
                self.flag_bin_repository,
                self.flag_short_bin_repository
            ]
        }

        self.commands['-h'] = self.commands['--help']
        self.commands['-v'] = self.commands['--version']
        self.commands['-u'] = self.commands['update']
        self.commands['-U'] = self.commands['upgrade']
        self.commands['-c'] = self.commands['check-updates']
        self.commands['-I'] = self.commands['repo-info']
        self.commands['-g'] = self.commands['configs']
        self.commands['-L'] = self.commands['clean-logs']
        self.commands['-D'] = self.commands['clean-tmp']
        self.commands['-T'] = self.commands['clean-data']
        self.commands['-b'] = self.commands['build']
        self.commands['-i'] = self.commands['install']
        self.commands['-d'] = self.commands['download']
        self.commands['-R'] = self.commands['remove']
        self.commands['-f'] = self.commands['find']
        self.commands['-w'] = self.commands['view']
        self.commands['-s'] = self.commands['search']
        self.commands['-e'] = self.commands['dependees']
        self.commands['-t'] = self.commands['tracking']

        self.split_options()
        self.split_options_from_args()
        self.move_options()
        self.invalid_options()

        self.check = Check(self.flags)
        self.check.is_blacklist(self.args[1:])
        self.check_for_bin_repositories()

    def check_for_bin_repositories(self) -> None:
        """ Checks combination for binaries use repositories only and if repository exists. """
        if self.utils.is_option(self.flag_binaries, self.flags):

            except_options: list = ['-s', 'search', '-u', 'update', '-c', 'check-updates']

            if self.binary_repo == '*' and not self.utils.is_option(except_options, self.args):
                self.usage.help_minimal(f"{self.prog_name}: invalid binary repository '{self.binary_repo}'")

            elif self.binary_repo not in self.repos.bin_repos_names and self.binary_repo != '*':
                self.usage.help_minimal(f"{self.prog_name}: invalid binary repository '{self.binary_repo}'")

    def invalid_options(self) -> None:
        """ Checks for invalid options. """
        invalid, commands, repeat = [], [], []

        for arg in self.args:
            if arg[0] == '-' and arg in self.commands.keys():
                commands.append(arg)
            elif arg[0] == '-' and arg not in self.options:
                invalid.append(arg)

        # Counts the recurring options.
        for opt in self.flags:
            if self.flags.count(opt) > 1:
                repeat.append(opt)

        # Fixed for recurring options.
        if repeat:
            self.usage.help_minimal(f"{self.prog_name}: invalid recurring options '{', '.join(repeat)}'")

        # Fixed for invalid commands combination.
        if len(commands) > 1:
            self.usage.help_minimal(f"{self.prog_name}: invalid commands combination '{', '.join(commands)}'")

        # Fixed for correct options by command.
        try:
            options: list = self.commands[self.args[0]]
            for opt in self.flags:
                if opt not in options:
                    invalid.append(opt)
        except (KeyError, IndexError):
            self.usage.help_short(1)

        # Prints error for invalid options.
        if invalid:
            self.usage.help_minimal(f"{self.prog_name}: invalid options '{','.join(invalid)}'")

    def split_options(self) -> None:
        """ Split options and commands, like: -iyjR

            slpkg -jyiR package

            Puts the command first and options after.
            Result: ['-i', '-y', '-j', '-R']
        """
        for args in self.args:
            if args[0] == '-' and args[:2] != '--' and len(args) >= 3 and '=' not in args:
                self.args.remove(args)

                for opt in list(map(lambda x: f'-{x}', [arg for arg in list(args[1:])])):
                    if opt in self.commands.keys():
                        self.args.insert(0, opt)
                        continue

                    self.args.append(opt)

    def split_options_from_args(self) -> None:
        """ Split options from arguments.

            slpkg -f package --file-pattern='*'

            Splits the option ['--file-pattern'] and ['*']
        """
        for arg in self.args:
            if arg.startswith(self.flag_directory):
                self.directory: str = arg.split('=')[1]
                self.args[self.args.index(arg)] = self.flag_directory

            if arg.startswith(self.flag_short_directory) and len(self.args) > 3:
                self.directory: str = self.args[self.args.index(arg) + 1]
                self.args.remove(self.directory)

            if arg.startswith(self.flag_bin_repository):
                self.binary_repo: str = arg.split('=')[1]
                self.args[self.args.index(arg)] = self.flag_bin_repository

            if arg.startswith(self.flag_short_bin_repository) and len(self.args) > 3:
                self.binary_repo: str = self.args[self.args.index(arg) + 1]
                self.args.remove(self.binary_repo)

    def move_options(self) -> None:
        """ Move options to the flags and removes from the arguments. """
        new_args: list = []

        for arg in self.args:
            if arg in self.options:
                self.flags.append(arg)
            else:
                new_args.append(arg)

        self.args: list = new_args

    def is_file_list_packages(self) -> list:
        """ Checks if the arg is filelist.pkgs. """
        if self.args[1].endswith(self.file_list_suffix):
            file = Path(self.args[1])
            packages: list = list(self.utils.read_packages_from_file(file))
        else:
            packages: list = list(set(self.args[1:]))

        return packages

    def choose_packages(self, packages: list, method: str) -> list:
        """ Choose packages with dialog utility and -S, --search flag. """
        height: int = 10
        width: int = 70
        list_height: int = 0
        choices: list = []
        title: str = f' Choose packages you want to {method} '

        repo_packages: list = SBoQueries('').sbos()
        if self.utils.is_option(self.flag_binaries, self.flags):
            repo_packages: list = BinQueries('', self.binary_repo).all_package_names_by_repo()

        installed: list = self.utils.installed_packages

        if method in ['remove', 'find']:

            for package in installed:
                split_package: list = self.utils.split_binary_pkg(package)

                for pkg in packages:
                    if pkg in split_package[0]:
                        choices += [(split_package[0], split_package[1], False, f'Package: {package}')]

        elif method == 'upgrade':
            for pkg in packages:
                for package in repo_packages:

                    if pkg == package:

                        inst_pkg: str = self.utils.is_package_installed(package)
                        split_inst_pkg: list = self.utils.split_binary_pkg(inst_pkg)

                        if self.utils.is_option(self.flag_binaries, self.flags):
                            repo_ver: str = BinQueries(package, self.binary_repo).version()
                            bin_pkg: str = BinQueries(package, self.binary_repo).package_bin()
                            repo_build_tag: str = self.utils.split_binary_pkg(bin_pkg[:-4])[3]
                        else:
                            repo_ver: str = SBoQueries(package).version()
                            repo_build_tag: str = self.utils.read_sbo_build_tag(package)

                        choices += [(package, f'{split_inst_pkg[1]} -> {repo_ver}', True,
                                     f'Installed: {package}-{split_inst_pkg[1]} Build: {split_inst_pkg[3]} -> '
                                     f'Available: {repo_ver} Build: {repo_build_tag}')]
        else:
            for pkg in packages:
                for package in repo_packages:
                    if pkg in package:
                        if self.utils.is_option(self.flag_binaries, self.flags):
                            repo_ver: str = BinQueries(package, self.binary_repo).version()
                            repo: str = BinQueries(package, self.binary_repo).repository()
                        else:
                            repo_ver: str = SBoQueries(package).version()
                            repo: str = self.repos.sbo_enabled_repository
                        choices += [(package, repo_ver, False, f'Package: {package}-{repo_ver} '
                                                               f'> {repo}')]

        if not choices:
            return packages

        text: str = f'There are {len(choices)} packages:'
        code, tags = self.dialogbox.checklist(text, packages, title, height,
                                              width, list_height, choices)
        os.system('clear')

        if code == 'cancel':
            raise SystemExit()

        if not tags:
            return packages

        return list(set(tags))

    def help(self) -> None:
        if len(self.args) == 1:
            self.usage.help(0)
        self.usage.help_short(1)

    def version(self) -> None:
        if len(self.args) == 1:
            version = Version()
            version.view()
            raise SystemExit()
        self.usage.help_short(1)

    def update(self) -> None:
        if len(self.args) == 1:
            update = UpdateRepository(self.flags, self.binary_repo)
            update.repositories()
            raise SystemExit()
        self.usage.help_short(1)

    def upgrade(self) -> None:
        command = Argparse.upgrade.__name__

        if len(self.args) == 1:
            self.check.is_empty_database()

            upgrade = Upgrade(self.flags, self.binary_repo)
            packages: list = list(upgrade.packages())

            packages: list = self.choose_packages(packages, command)

            if not packages:
                print('\nEverything is up-to-date!\n')
                raise SystemExit()

            if self.utils.is_option(self.flag_binaries, self.flags):
                install = Packages(packages, self.flags, self.binary_repo, mode=command)
                install.execute()
            else:
                install = Slackbuilds(packages, self.flags, mode=command)
                install.execute()
            raise SystemExit()
        self.usage.help_short(1)

    def check_updates(self) -> None:
        if len(self.args) == 1:
            check = CheckUpdates(self.flags, self.binary_repo)
            check.updates()
            raise SystemExit()
        self.usage.help_short(1)

    def repo_info(self) -> None:
        if len(self.args) == 1:
            repo = RepoInfo()
            repo.info()
            raise SystemExit()
        self.usage.help_short(1)

    def edit_configs(self) -> None:
        if len(self.args) == 1:
            self.form_configs.edit()
            raise SystemExit()
        self.usage.help_short(1)

    def clean_logs(self) -> None:
        if len(self.args) == 1:
            self.check.is_empty_database()

            logs = CleanLogsDependencies(self.flags)
            logs.clean()
            raise SystemExit()
        self.usage.help_short(1)

    def clean_tmp(self) -> None:
        if len(self.args) == 1:

            print(f"\n{self.prog_name}: {self.bred}WARNING{self.endc}: All the files in the "
                  f"'{self.tmp_path}{self.prog_name}' "
                  f"folder will delete!")

            views = ViewMessage(self.flags)
            views.question()

            self.utils.remove_folder_if_exists(Path(self.tmp_path, self.prog_name))
            self.utils.create_folder(path=self.tmp_slpkg, folder='build')
            print(f"The folder '{self.tmp_path}{self.prog_name}' was cleaned!")

            raise SystemExit()
        self.usage.help_short(1)

    def clean_data(self) -> None:
        if len(self.args) == 1:
            update = UpdateRepository(self.flags, self.binary_repo)
            update.drop_the_tables()
            raise SystemExit()
        self.usage.help_short(1)

    def build(self) -> None:
        command = Argparse.build.__name__

        if len(self.args) >= 2:

            self.check.is_empty_database()
            packages: list = self.is_file_list_packages()

            if self.utils.is_option(self.flag_searches, self.flags):
                packages: list = self.choose_packages(packages, command)

            self.check.exists_in_the_database(packages)
            self.check.is_package_unsupported(packages)

            build = Slackbuilds(packages, self.flags, mode=command)
            build.execute()
            raise SystemExit()
        self.usage.help_short(1)

    def install(self) -> None:
        command = Argparse.install.__name__

        if len(self.args) >= 2:

            self.check.is_empty_database()
            packages: list = self.is_file_list_packages()

            if self.utils.is_option(self.flag_searches, self.flags):
                packages: list = self.choose_packages(packages, command)

            if self.utils.is_option(self.flag_binaries, self.flags):
                self.check.exists_in_the_database(packages, self.binary_repo)

                install = Packages(packages, self.flags, self.binary_repo, mode=command)
                install.execute()
            else:
                self.check.exists_in_the_database(packages)
                self.check.is_package_unsupported(packages)

                install = Slackbuilds(packages, self.flags, mode=command)
                install.execute()
            raise SystemExit()
        self.usage.help_short(1)

    def download(self) -> None:
        command = Argparse.download.__name__

        if len(self.args) >= 2:

            self.check.is_empty_database()
            packages: list = self.is_file_list_packages()

            if self.utils.is_option(self.flag_searches, self.flags):
                packages: list = self.choose_packages(packages, command)

            self.check.exists_in_the_database(packages, self.binary_repo)
            download = Download(self.directory, self.flags)
            download.packages(packages, self.binary_repo)
            raise SystemExit()
        self.usage.help_short(1)

    def remove(self) -> None:
        command = Argparse.remove.__name__

        if len(self.args) >= 2:

            packages: list = self.is_file_list_packages()

            if self.utils.is_option(self.flag_searches, self.flags):
                packages: list = self.choose_packages(packages, command)

            self.check.is_installed(packages)

            remove = RemovePackages(packages, self.flags)
            remove.remove()
            raise SystemExit()
        self.usage.help_short(1)

    def find(self) -> None:
        command = Argparse.find.__name__

        if len(self.args) >= 2:

            self.check.is_empty_database()
            packages: list = self.is_file_list_packages()

            if self.utils.is_option(self.flag_searches, self.flags):
                packages: list = self.choose_packages(packages, command)

            find = FindInstalled()
            find.find(packages)
            raise SystemExit()
        self.usage.help_short(1)

    def view(self) -> None:
        command = Argparse.view.__name__

        if len(self.args) >= 2:

            self.check.is_empty_database()
            packages: list = self.is_file_list_packages()

            if self.utils.is_option(self.flag_searches, self.flags):
                packages: list = self.choose_packages(packages, command)

            self.check.exists_in_the_database(packages, self.binary_repo)

            view = ViewPackage(self.flags)

            if self.utils.is_option(self.flag_binaries, self.flags):
                view.package(packages, self.binary_repo)
            else:
                view.slackbuild(packages)
            raise SystemExit()
        self.usage.help_short(1)

    def search(self) -> None:
        command = Argparse.search.__name__

        if len(self.args) >= 2:

            self.check.is_empty_database()
            packages: list = self.is_file_list_packages()

            if self.utils.is_option(self.flag_searches, self.flags):
                packages: list = self.choose_packages(packages, command)

            search = SearchPackage(self.flags)
            search.package(packages, self.binary_repo)
            raise SystemExit()
        self.usage.help_short(1)

    def dependees(self) -> None:
        command = Argparse.dependees.__name__

        if len(self.args) >= 2:

            self.check.is_empty_database()
            packages: list = self.is_file_list_packages()

            if self.utils.is_option(self.flag_searches, self.flags):
                packages: list = self.choose_packages(packages, command)

            self.check.exists_in_the_database(packages, self.binary_repo)

            dependees = Dependees(packages, self.flags)
            dependees.find(self.binary_repo)
            raise SystemExit()
        self.usage.help_short(1)

    def tracking(self) -> None:
        command = Argparse.tracking.__name__

        if len(self.args) >= 2:

            self.check.is_empty_database()
            packages: list = self.is_file_list_packages()

            if self.utils.is_option(self.flag_searches, self.flags):
                packages: list = self.choose_packages(packages, command)

            self.check.exists_in_the_database(packages, self.binary_repo)

            tracking = Tracking(self.flags)
            tracking.packages(packages, self.binary_repo)
            raise SystemExit()
        self.usage.help_short(1)

    def help_for_commands(self) -> None:
        """ Extra help information for commands. """
        if len(self.args) == 2:
            try:
                flags = self.commands[self.args[1]]
                Help(self.args[1], flags).view()
            except KeyError:
                self.usage.help_minimal(f"{self.prog_name}: invalid argument '{''.join(self.args[1])}'")
        else:
            self.usage.help_short(1)


def main():
    args = sys.argv
    args.pop(0)
    usage = Usage()

    argparse = Argparse(args)

    arguments: dict = {
        '-h': argparse.help,
        '--help': argparse.help,
        '-v': argparse.version,
        '--version': argparse.version,
        'help': argparse.help_for_commands,
        'update': argparse.update,
        '-u': argparse.update,
        'upgrade': argparse.upgrade,
        '-U': argparse.upgrade,
        'check-updates': argparse.check_updates,
        '-c': argparse.check_updates,
        'repo-info': argparse.repo_info,
        '-I': argparse.repo_info,
        'configs': argparse.edit_configs,
        '-g': argparse.edit_configs,
        'clean-logs': argparse.clean_logs,
        '-L': argparse.clean_logs,
        'clean-data': argparse.clean_data,
        '-T': argparse.clean_data,
        'clean-tmp': argparse.clean_tmp,
        '-D': argparse.clean_tmp,
        'build': argparse.build,
        '-b': argparse.build,
        'install': argparse.install,
        '-i': argparse.install,
        'download': argparse.download,
        '-d': argparse.download,
        'remove': argparse.remove,
        '-R': argparse.remove,
        'view': argparse.view,
        '-w': argparse.view,
        'find': argparse.find,
        '-f': argparse.find,
        'search': argparse.search,
        '-s': argparse.search,
        'dependees': argparse.dependees,
        '-e': argparse.dependees,
        'tracking': argparse.tracking,
        '-t': argparse.tracking
    }

    try:
        arguments[args[0]]()
    except (KeyError, IndexError):
        usage.help_short(1)


if __name__ == '__main__':
    main()
