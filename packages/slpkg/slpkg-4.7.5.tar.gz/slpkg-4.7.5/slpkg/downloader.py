#!/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import Union
from pathlib import Path
from urllib.parse import unquote
from multiprocessing import Process

from slpkg.configs import Configs
from slpkg.utilities import Utilities


class Downloader(Configs):

    def __init__(self, path: Union[str, Path], urls: list, flags: list):
        super(Configs, self).__init__()
        self.path = path
        self.urls: list = urls
        self.flags: list = flags

        self.utils = Utilities()

        self.flag_parallel: list = ['-P', '--parallel']

    def download(self) -> None:
        """ Starting the processing for downloading. """
        process: list = []

        if self.parallel_downloads or self.utils.is_option(self.flag_parallel, self.flags):
            for url in self.urls:
                p1 = Process(target=self.tools, args=(url,))
                process.append(p1)
                p1.start()

            for proc in process:
                proc.join()
        else:
            for url in self.urls:
                self.tools(url)

    def tools(self, url: str) -> None:
        """ Downloader tools wget, curl and lftp. """
        command: str = ''
        filename: str = url.split('/')[-1]

        if self.downloader == 'wget':
            command: str = f'{self.downloader} {self.wget_options} --directory-prefix={self.path} "{url}"'

        elif self.downloader == 'curl':
            command: str = f'{self.downloader} {self.curl_options} "{url}" --output {self.path}/{filename}'

        elif self.downloader == 'lftp':
            command: str = f'{self.downloader} {self.lftp_get_options} {url} -o {self.path}'

        else:
            self.utils.raise_error_message(f"Downloader '{self.downloader}' not supported")

        self.utils.process(command)
        self.check_if_downloaded(url)

    def check_if_downloaded(self, url: str) -> None:
        """ Checks if the file downloaded. """
        url: str = unquote(url)
        file: str = url.split('/')[-1]
        path_file = Path(self.path, file)

        if not path_file.exists():
            self.utils.raise_error_message(f"Download the '{file}' file")
