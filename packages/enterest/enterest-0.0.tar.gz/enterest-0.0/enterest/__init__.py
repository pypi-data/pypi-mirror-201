#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import annotations

from . import shell


if __name__ == "__main__":
    shell.IS_DEBUG_MODE = True

    enter_shell = shell.Shell()

    with open("./main.enter", encoding="utf-8") as file:
        code = file.read()

    enter_shell.exec(code)
    enter_shell.run()
