#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

from .bakery_api.v1 import (
    FileGenerator,
    OS,
    Plugin,
    register,
)


def get_secureboot_cert_files() -> FileGenerator:
    yield Plugin(
        base_os=OS.WINDOWS,
        source=Path("secureboot_cert.ps1"),
    )


register.bakery_plugin(
    name="secureboot_cert",
    files_function=get_secureboot_cert_files,
)
