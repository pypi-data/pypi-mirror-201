#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import tomli
import platform
from pathlib import Path
from dataclasses import dataclass


class Load:

    def __init__(self):
        bold = '\033[1m'
        red = '\x1b[91m'

        self.endc: str = '\x1b[0m'
        self.bred: str = f'{bold}{red}'

    def config_file(self, path: Path, file: str) -> dict:  # type: ignore
        try:
            """ Load the configs from the file. """
            config_path_file = Path(path, f'{file}.toml')
            if config_path_file.exists():
                with open(config_path_file, 'rb') as conf:
                    return tomli.load(conf)
        except tomli.TOMLDecodeError as error:
            raise SystemExit(f"\nslpkg: {self.bred}Error{self.endc}: {error}: in the configuration file "
                             "'/etc/slpkg/slpkg.toml'\n")


@dataclass
class Configs:
    """ Default configurations. """

    color = {
        'bold': '\033[1m',
        'red': '\x1b[91m',
        'green': '\x1b[32m',
        'yellow': '\x1b[93m',
        'cyan': '\x1b[96m',
        'blue': '\x1b[94m',
        'grey': '\x1b[38;5;247m',
        'violet': '\x1b[35m',
        'endc': '\x1b[0m'
    }

    prog_name: str = 'slpkg'
    os_arch: str = platform.machine()
    tmp_path: str = '/tmp/'
    tmp_slpkg: Path = Path(tmp_path, prog_name)
    build_path: Path = Path(tmp_path, prog_name, 'build')
    download_only_path: Path = Path(tmp_slpkg, '')
    lib_path: Path = Path('/var/lib', prog_name)
    etc_path: Path = Path('/etc', prog_name)
    db_path: Path = Path(lib_path, 'database')
    log_packages: Path = Path('/var', 'log', 'packages')

    database_name: str = f'database.{prog_name}'
    file_list_suffix: str = '.pkgs'
    installpkg: str = 'upgradepkg --install-new'
    reinstall: str = 'upgradepkg --reinstall'
    removepkg: str = 'removepkg'
    colors: bool = True
    dialog: bool = True
    downloader: str = 'wget'
    wget_options: str = '--c -q --progress=bar:force:noscroll --show-progress'
    curl_options: str = ''
    lftp_get_options: str = '-c get -e'
    lftp_mirror_options: str = '-c mirror --parallel=100 --only-newer'
    silent_mode: bool = True
    ascii_characters: bool = True
    ask_question: bool = True
    parallel_downloads: bool = False
    file_pattern: str = '*'
    progress_spinner: str = 'pixel'
    spinner_color: str = 'green'

    load = Load()
    configs = load.config_file(etc_path, prog_name)

    if configs:
        try:
            config = configs['CONFIGS']

            os_arch: str = config['OS_ARCH']
            download_only_path: Path = config['DOWNLOAD_ONLY_PATH']
            ask_question: bool = config['ASK_QUESTION']
            installpkg: str = config['INSTALLPKG']
            reinstall: str = config['REINSTALL']
            removepkg: str = config['REMOVEPKG']
            colors: bool = config['COLORS']
            dialog: str = config['DIALOG']
            downloader: str = config['DOWNLOADER']
            wget_options: str = config['WGET_OPTIONS']
            curl_options: str = config['CURL_OPTIONS']
            lftp_get_options: str = config['LFTP_GET_OPTIONS']
            lftp_mirror_options: str = config['LFTP_MIRROR_OPTIONS']
            silent_mode: bool = config['SILENT_MODE']
            ascii_characters: bool = config['ASCII_CHARACTERS']
            file_list_suffix: str = config['FILE_LIST_SUFFIX']
            parallel_downloads: bool = config['PARALLEL_DOWNLOADS']
            file_pattern_conf: str = config['FILE_PATTERN']
            progress_spinner: str = config['PROGRESS_SPINNER']
            spinner_color: str = config['SPINNER_COLOR']

        except KeyError as error:
            raise SystemExit(f"\n{prog_name}: {color['bold']}{color['red']}Error{color['endc']}: "
                             f"{error}: in the configuration file '/etc/slpkg/slpkg.toml'.\n"
                             f"\nIf you have upgraded the '{prog_name}' probably you need to run:\n"
                             f"'mv {etc_path}/{prog_name}.toml.new {etc_path}/{prog_name}.toml'.\n"
                             f"or '{color['cyan']}slpkg_new-configs{color['endc']}' command.\n")

    # Creating the paths if not exists
    paths = [
        tmp_slpkg,
        build_path,
        download_only_path,
        lib_path,
        etc_path,
        db_path,
    ]

    for path in paths:
        if not os.path.isdir(path):
            os.makedirs(path)

    @classmethod
    def colour(cls) -> dict:

        if not cls.colors:

            cls.color = {
                'bold': '',
                'red': '',
                'green': '',
                'yellow': '',
                'cyan': '',
                'blue': '',
                'grey': '',
                'violet': '',
                'endc': ''
            }

        return cls.color
