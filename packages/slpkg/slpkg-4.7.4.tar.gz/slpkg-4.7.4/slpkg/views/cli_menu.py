#!/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import NoReturn
from slpkg.configs import Configs


class Usage(Configs):

    def __init__(self):
        super(Configs, self).__init__()
        color = self.colour()

        self.bold: str = color['bold']
        self.red: str = color['red']
        self.cyan: str = color['cyan']
        self.yellow: str = color['yellow']
        self.endc: str = color['endc']

    def help_minimal(self, message: str) -> NoReturn:
        """ Prints the minimal help menu. """
        print(message)
        args: str = (
            f'\nUsage: {self.prog_name} [{self.cyan}COMMAND{self.endc}] [{self.yellow}OPTIONS{self.endc}]'
            f'[FILELIST|PACKAGES...]\n'
            f"\nTry '{self.prog_name} --help' for more options.\n")

        print(args)
        raise SystemExit(1)

    def help_short(self, status: int) -> NoReturn:
        """ Prints the short menu. """
        args = (
            f'Usage: {self.prog_name} [{self.cyan}COMMAND{self.endc}] [{self.yellow}OPTIONS{self.endc}] '
            f'[FILELIST|PACKAGES...]\n'
            f'\n  slpkg [{self.cyan}COMMAND{self.endc}] [-u, update, -U, upgrade, -c, check-updates, -I, repo-info]\n'
            f'  slpkg [{self.cyan}COMMAND{self.endc}] [-L, clean-logs, -T, clean-data, -D, clean-tmp, -g, configs]\n'
            f'  slpkg [{self.cyan}COMMAND{self.endc}] [-b, build, -i, install, -d, download [packages...]]\n'
            f'  slpkg [{self.cyan}COMMAND{self.endc}] [-R, remove, -f, find, -w, view [packages...]]\n'
            f'  slpkg [{self.cyan}COMMAND{self.endc}] [-s, search, -e, dependees, -t, tracking  [packages...]]\n'
            f'  slpkg [{self.yellow}OPTIONS{self.endc}] [-y, --yes, -j, --jobs, -o, --resolve-off, -r, --reinstall]\n'
            f'  slpkg [{self.yellow}OPTIONS{self.endc}] [-k, --skip-installed, -E, --full-reverse, -S, --search]\n'
            f'  slpkg [{self.yellow}OPTIONS{self.endc}] [-n, --no-silent, -p, --pkg-version, -G, --generate-only]\n'
            f'  slpkg [{self.yellow}OPTIONS{self.endc}] [-P, --parallel, -B, --bin-repo=[REPO]]\n'
            f'  slpkg [{self.yellow}OPTIONS{self.endc}] [-z, --directory=[PATH]]\n'
            "  \nIf you need more information please try 'slpkg --help'.")

        print(args)
        raise SystemExit(status)

    def help(self, status: int) -> NoReturn:
        """ Prints the main menu. """
        args: str = (
            f'{self.bold}USAGE:{self.endc} {self.prog_name} [{self.cyan}COMMAND{self.endc}] '
            f'[{self.yellow}OPTIONS{self.endc}] [FILELIST|PACKAGES...]\n'
            f'\n{self.bold}DESCRIPTION:{self.endc} Package manager utility for Slackware.\n'
            f'\n{self.bold}COMMANDS:{self.endc}\n'
            f'  {self.red}-u, update{self.endc}                    Update the package lists.\n'
            f'  {self.cyan}-U, upgrade{self.endc}                   Upgrade all the packages.\n'
            f'  {self.cyan}-c, check-updates{self.endc}             Check for news on ChangeLog.txt.\n'
            f'  {self.cyan}-I, repo-info{self.endc}                 Prints the repositories information.\n'
            f'  {self.cyan}-g, configs{self.endc}                   Edit the configuration file.\n'
            f'  {self.cyan}-L, clean-logs{self.endc}                Clean dependencies log tracking.\n'
            f'  {self.cyan}-T, clean-data{self.endc}                Clean all the repositories data.\n'
            f'  {self.cyan}-D, clean-tmp{self.endc}                 Delete all the downloaded sources.\n'
            f'  {self.cyan}-b, build{self.endc} [packages...]       Build only the packages.\n'
            f'  {self.cyan}-i, install{self.endc} [packages...]     Build and install the packages.\n'
            f'  {self.cyan}-d, download{self.endc} [packages...]    Download only the scripts and sources.\n'
            f'  {self.cyan}-R, remove{self.endc} [packages...]      Remove installed packages.\n'
            f'  {self.cyan}-f, find{self.endc} [packages...]        Find installed packages.\n'
            f'  {self.cyan}-w, view{self.endc} [packages...]        View packages from the repository.\n'
            f'  {self.cyan}-s, search{self.endc} [packages...]      Search packages from the repository.\n'
            f'  {self.cyan}-e, dependees{self.endc} [packages...]   Show which packages depend on.\n'
            f'  {self.cyan}-t, tracking{self.endc} [packages...]    Tracking the packages dependencies.\n'
            f'\n{self.bold}OPTIONS:{self.endc}\n'
            f'  {self.yellow}-y, --yes{self.endc}                     Answer Yes to all questions.\n'
            f'  {self.yellow}-j, --jobs{self.endc}                    Set it for multicore systems.\n'
            f'  {self.yellow}-o, --resolve-off{self.endc}             Turns off dependency resolving.\n'
            f'  {self.yellow}-r, --reinstall{self.endc}               Upgrade packages of the same version.\n'
            f'  {self.yellow}-k, --skip-installed{self.endc}          Skip installed packages.\n'
            f'  {self.yellow}-E, --full-reverse{self.endc}            Full reverse dependency.\n'
            f'  {self.yellow}-S, --search{self.endc}                  Search packages from the repository.\n'
            f'  {self.yellow}-n, --no-silent{self.endc}               Disable silent mode.\n'
            f'  {self.yellow}-p, --pkg-version{self.endc}             Print the repository package version.\n'
            f'  {self.yellow}-G, --generate-only{self.endc}           Generates only the SLACKBUILDS.TXT file.\n'
            f'  {self.yellow}-P, --parallel{self.endc}                Download files in parallel.\n'
            f'  {self.yellow}-B, --bin-repo={self.endc}[REPO]         Set a binary repository.\n'
            f'  {self.yellow}-z, --directory={self.endc}[PATH]        Download files to a specific path.\n'
            '\n  -h, --help                    Show this message and exit.\n'
            '  -v, --version                 Print version and exit.\n'
            "\nIf you need more information try to use slpkg manpage.\n"
            "Extra help for the commands, use: 'slpkg help [command]'.\n"
            "Edit the config file in the /etc/slpkg/slpkg.toml or 'slpkg configs'.")

        print(args)
        raise SystemExit(status)
