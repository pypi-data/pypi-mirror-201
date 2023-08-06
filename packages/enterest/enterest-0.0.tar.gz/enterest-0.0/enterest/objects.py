#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any, Callable


class EnterClass:
    instances: list[EnterObject]
    values: dict[str, EnterObject]

    def __repr__(self): return self.name

    def __init__(self, name: str, values: dict[str, EnterObject] | None = None):
        if values is None:
            values = {}

        self.instances = []
        self.name = name
        self.values = {**values}

    def __getitem__(self, item: str) -> EnterObject:
        return self.values[item]

    def __setitem__(self, key: str, value: EnterObject):
        self.values[key] = value

    def __delitem__(self, key: str):
        del self.values[key]

    def new(self, _) -> Any:
        return None

    def repr(self, value: EnterObject) -> str:
        return value.obj.__repr__()

    def bool_(self, value: EnterObject) -> bool:
        return bool(value.obj)

    def int_(self, value: EnterObject) -> int:
        return int(value.obj)

    def float_(self, value: EnterObject) -> float:
        return float(value.obj)

    def complex_(self, value: EnterObject) -> complex:
        return complex(value.obj)

    def str_(self, value: EnterObject) -> str:
        return str(value.obj)

    def __call__(self, value=None) -> EnterObject:
        return EnterObject(self, self.new(value))


class EnterObject:
    obj_type: EnterClass
    _values: dict[str, EnterObject]
    obj: None | bool | int | float | complex | str | tuple | EnterClass | Callable[..., EnterObject]

    def __new__(cls, obj_type: EnterClass, obj: Any = None):
        if obj is not None:
            for instance in obj_type.instances:
                if instance.obj == obj or instance.obj is obj:
                    return instance
        instance = super().__new__(cls)
        obj_type.instances.append(instance)
        return instance

    def __init__(self, obj_type: EnterClass, obj: Any = None):
        self.obj_type = obj_type
        self.obj = obj
        self._values = {**obj_type.values}

    def __repr__(self):
        return self.obj_type.repr(self)

    def __bool__(self):
        return self.obj_type.bool_(self)

    def __int__(self):
        return self.obj_type.int_(self)

    def __float__(self):
        return self.obj_type.float_(self)

    def __str__(self):
        return self.obj_type.str_(self)

    def __contains__(self, item: EnterObject) -> bool:
        return self.contains(item).obj

    def contains(self, item: EnterObject) -> EnterObject:
        return self.call_method("__contains__", item)

    def lt(self, other: EnterObject) -> EnterObject:
        return self.call_method("__lt__", other)

    def le(self, other: EnterObject) -> EnterObject:
        return self.call_method("__le__", other)

    def gt(self, other: EnterObject) -> EnterObject:
        return self.call_method("__gt__", other)

    def ge(self, other: EnterObject) -> EnterObject:
        return self.call_method("__ge__", other)

    def ne(self, other: EnterObject) -> EnterObject:
        return self.call_method("__ne__", other)

    def eq(self, other: EnterObject) -> EnterObject:
        return self.call_method("__eq__", other)

    def __or__(self, other: EnterObject) -> EnterObject:
        return self.call_method("__or__", other)

    def __xor__(self, other: EnterObject) -> EnterObject:
        return self.call_method("__xor__", other)

    def __and__(self, other: EnterObject) -> EnterObject:
        return self.call_method("__and__", other)

    def __lshift__(self, other: EnterObject) -> EnterObject:
        return self.call_method("__lshift__", other)

    def __rshift__(self, other: EnterObject) -> EnterObject:
        return self.call_method("__rshift__", other)

    def __invert__(self) -> EnterObject:
        return self.call_method("__not__")

    def __add__(self, other: EnterObject) -> EnterObject:
        return self.call_method("__add__", other)

    def __sub__(self, other: EnterObject) -> EnterObject:
        return self.call_method("__sub__", other)

    def __mul__(self, other: EnterObject) -> EnterObject:
        return self.call_method("__mul__", other)

    def __truediv__(self, other: EnterObject) -> EnterObject:
        return self.call_method("__div__", other)

    def __pow__(self, other: EnterObject) -> EnterObject:
        return self.call_method("__pow__", other)

    def __mod__(self, other: EnterObject) -> EnterObject:
        return self.call_method("__mod__", other)

    def __pos__(self) -> EnterObject:
        return self.call_method("__pos__")

    def __neg__(self) -> EnterObject:
        return self.call_method("__neg__")

    def __abs__(self) -> EnterObject:
        return self.call_method("__abs__")

    def floor(self) -> EnterObject:
        return self.call_method("__floor__")

    def ceil(self) -> EnterObject:
        return self.call_method("__ceil__")

    def call(self, *args: EnterObject) -> EnterObject:
        if self.obj_type == EMethodWrapper:
            return self.obj(*args)
        return self._values["__call__"].call(self, *args)

    def call_method(self, key: str, *args: EnterObject) -> EnterObject:
        return self._values[key].call(self, *args)

    def __iter__(self):
        return self.call_method("__iter__")

    def getitem(self, item: EnterObject) -> EnterObject:
        return self._values["__getitem__"].call(self, item)

    def setitem(self, key: EnterObject, value: EnterObject) -> EnterObject:
        return self._values["__setitem__"].call(self, key, value)

    def delitem(self, key: EnterObject) -> EnterObject:
        return self._values["__delitem__"].call(self, key)

    def __getitem__(self, item: str) -> EnterObject:
        return self._values[item]

    def __setitem__(self, key: str, value: EnterObject):
        self._values[key] = value

    def __delitem__(self, key: str):
        del self._values[key]

    def copy(self) -> EnterObject:
        result = EnterObject(self.obj_type, self.obj)
        result._values = {**self._values}
        return result


EMethodWrapper = EnterClass("MethodWrapper")
EMethodWrapper.new = lambda value: value
