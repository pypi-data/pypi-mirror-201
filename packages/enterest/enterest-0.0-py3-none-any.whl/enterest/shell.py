#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import annotations

from .interpreter import *


IS_DEBUG_MODE = False


class Shell:
    def __init__(self):
        self.enter = Enter()

    def exec(self, code: str) -> None:
        result = self.enter.exec(code)
        if IS_DEBUG_MODE:
            print(result, self.enter.global_values)

    def run(self) -> None:
        try:
            while True:
                self.exec(input(">>>"))
        except KeyboardInterrupt:
            pass
