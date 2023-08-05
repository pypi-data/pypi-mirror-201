#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
from progress.spinner import (PixelSpinner, LineSpinner,
                              MoonSpinner, PieSpinner, Spinner)

from slpkg.configs import Configs


class ProgressBar(Configs):

    def __init__(self):
        super(Configs, self).__init__()
        self.color = self.colour()

        self.violet: str = self.color['violet']
        self.green: str = self.color['green']
        self.blue: str = self.color['blue']
        self.red: str = self.color['red']
        self.grey: str = self.color['grey']
        self.yellow: str = self.color['yellow']
        self.cyan: str = self.color['cyan']
        self.endc: str = self.color['endc']

    def bar(self, message: str, filename: str) -> None:
        """ Creating progress bar. """
        spinners: dict = {
            'pixel': PixelSpinner,
            'line': LineSpinner,
            'moon': MoonSpinner,
            'pie': PieSpinner,
            'spinner': Spinner
        }
        colors: dict = {
            'green': self.green,
            'violet': self.violet,
            'yellow': self.yellow,
            'blue': self.blue,
            'cyan': self.cyan,
            'grey': self.grey,
            'red': self.red,
            '': self.endc
        }

        try:
            spinner = spinners[self.progress_spinner]
            color: str = colors[self.spinner_color]
        except KeyError:
            spinner = PixelSpinner
            color: str = self.endc

        bar_spinner = spinner(f'{self.endc}{message} {filename} {color}')
        # print('\033[F', end='', flush=True)
        try:
            while True:
                time.sleep(0.1)
                bar_spinner.next()
        except KeyboardInterrupt:
            raise SystemExit(1)
