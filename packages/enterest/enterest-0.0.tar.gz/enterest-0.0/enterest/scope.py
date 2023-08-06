#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any

from .objects import EnterObject


__all__ = [
    "Scope",
]


class Scope:
    _values: dict[str, EnterObject]

    interpreter: Any
    master: Scope | None

    def __init__(
        self,
        master: Scope | None,
        values: dict[str, EnterObject | None] | None = None,
        interpreter: Any = None,
    ):
        if interpreter is None:
            self.interpreter = self.master.interpreter
        else:
            self.interpreter = interpreter

        self.master = master
        self._values = {}
        if values:
            self._values = {**values}

    def __contains__(self, item: str) -> bool:
        return item in self._values

    def __getitem__(self, item: str) -> EnterObject:
        if item in self:
            return self._values[item]
        elif not self.is_root:
            return self.master[item]
        else:
            self.interpreter.raise_(f"NameError: name '{item}' is not defined")

    def __setitem__(self, key: str, value: EnterObject):
        self._values[key] = value

    def __delitem__(self, key: str):
        if key in self:
            del self._values[key]
        else:
            self.interpreter.raise_(f"NameError: name '{key}' is not defined")

    @property
    def is_root(self) -> bool:
        return self.master is None
