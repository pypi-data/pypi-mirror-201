#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pathlib import Path


class LoggingConfig:
    root_slpkg: Path = Path(Path.home(), '.slpkg')
    log_path: Path = Path(root_slpkg, 'logs')
    log_file: Path = Path(log_path, 'errors_slpkg.log')
