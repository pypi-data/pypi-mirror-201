#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import annotations

import math

from . import objects


__all__ = [
    "EObject",
    "ENoneType",
    "EBool",
    "EInt",
    "EFloat",
    "EString",
    "EList",
    "ERange",
    "EType",
    "EFunction",
]


EObject = objects.EnterClass("Object")
ENoneType = objects.EnterClass("NoneType")
EBool = objects.EnterClass("Bool")
EInt = objects.EnterClass("Int")
EFloat = objects.EnterClass("Float")
EString = objects.EnterClass("String")
EList = objects.EnterClass("List")
ERange = objects.EnterClass("Range")
EType = objects.EnterClass("Type")
EFunction = objects.EnterClass("Function")


EObject.new = lambda value: None
ENoneType.new = lambda value: False
EBool.new = lambda value: bool(value)
EInt.new = lambda value: int(value)
EFloat.new = lambda value: float(value)
EString.new = lambda value: str(value)
EList.new = lambda value: tuple(value)
ERange.new = lambda value: range(value)
EType.new = lambda value: value
EFunction.new = lambda value: value


EObject.repr = lambda value: "object"


ENoneType.repr = lambda value: "none"


EBool.repr = lambda value: "true" if value.obj else "false"

EBool["__ne__"] = objects.EMethodWrapper(lambda value, other: EBool(value.obj != other.obj))
EBool["__eq__"] = objects.EMethodWrapper(lambda value, other: EBool(value.obj == other.obj))

EBool["__or__"] = objects.EMethodWrapper(lambda value, other: EBool(value.obj or other.obj))
EBool["__xor__"] = objects.EMethodWrapper(lambda value, other: EBool(value.obj != other.obj))
EBool["__and__"] = objects.EMethodWrapper(lambda value, other: EBool(value.obj and other.obj))
EBool["__not__"] = objects.EMethodWrapper(lambda value: EBool(not value.obj))


EInt["__lt__"] = objects.EMethodWrapper(lambda value, other: EBool(value.obj < other.obj))
EInt["__le__"] = objects.EMethodWrapper(lambda value, other: EBool(value.obj <= other.obj))
EInt["__gt__"] = objects.EMethodWrapper(lambda value, other: EBool(value.obj > other.obj))
EInt["__ge__"] = objects.EMethodWrapper(lambda value, other: EBool(value.obj >= other.obj))
EInt["__ne__"] = objects.EMethodWrapper(lambda value, other: EBool(value.obj != other.obj))
EInt["__eq__"] = objects.EMethodWrapper(lambda value, other: EBool(value.obj == other.obj))

EInt["__or__"] = objects.EMethodWrapper(lambda value, other: EInt(value.obj | other.obj))
EInt["__xor__"] = objects.EMethodWrapper(lambda value, other: EInt(value.obj ^ other.obj))
EInt["__and__"] = objects.EMethodWrapper(lambda value, other: EInt(value.obj & other.obj))
EInt["__lshift__"] = objects.EMethodWrapper(lambda value, other: EInt(value.obj << other.obj))
EInt["__rshift__"] = objects.EMethodWrapper(lambda value, other: EInt(value.obj >> other.obj))
EInt["__not__"] = objects.EMethodWrapper(lambda value: EInt(~value.obj))

EInt["__add__"] = objects.EMethodWrapper(lambda value, other: EInt(value.obj + other.obj))
EInt["__sub__"] = objects.EMethodWrapper(lambda value, other: EInt(value.obj - other.obj))
EInt["__mul__"] = objects.EMethodWrapper(lambda value, other: EInt(value.obj * other.obj))
EInt["__div__"] = objects.EMethodWrapper(lambda value, other: EInt(value.obj / other.obj))
EInt["__pow__"] = objects.EMethodWrapper(lambda value, other: EInt(value.obj ** other.obj))
EInt["__mod__"] = objects.EMethodWrapper(lambda value, other: EInt(value.obj % other.obj))
EInt["__pos__"] = objects.EMethodWrapper(lambda value: EInt(+value.obj))
EInt["__neg__"] = objects.EMethodWrapper(lambda value: EInt(-value.obj))

EInt["__abs__"] = objects.EMethodWrapper(lambda value: EInt(abs(value.obj)))
EInt["__floor__"] = objects.EMethodWrapper(lambda value: EInt(math.floor(value.obj)))
EInt["__ceil__"] = objects.EMethodWrapper(lambda value: EInt(math.ceil(value.obj)))


EFloat["__lt__"] = objects.EMethodWrapper(lambda value, other: EBool(value.obj < other.obj))
EFloat["__le__"] = objects.EMethodWrapper(lambda value, other: EBool(value.obj <= other.obj))
EFloat["__gt__"] = objects.EMethodWrapper(lambda value, other: EBool(value.obj > other.obj))
EFloat["__ge__"] = objects.EMethodWrapper(lambda value, other: EBool(value.obj >= other.obj))
EFloat["__ne__"] = objects.EMethodWrapper(lambda value, other: EBool(value.obj != other.obj))
EFloat["__eq__"] = objects.EMethodWrapper(lambda value, other: EBool(value.obj == other.obj))

EFloat["__add__"] = objects.EMethodWrapper(lambda value, other: EFloat(value.obj + other.obj))
EFloat["__sub__"] = objects.EMethodWrapper(lambda value, other: EFloat(value.obj - other.obj))
EFloat["__mul__"] = objects.EMethodWrapper(lambda value, other: EFloat(value.obj * other.obj))
EFloat["__div__"] = objects.EMethodWrapper(lambda value, other: EFloat(value.obj / other.obj))
EFloat["__pow__"] = objects.EMethodWrapper(lambda value, other: EFloat(value.obj ** other.obj))
EFloat["__mod__"] = objects.EMethodWrapper(lambda value, other: EFloat(value.obj % other.obj))
EFloat["__pos__"] = objects.EMethodWrapper(lambda value: EFloat(+value.obj))
EFloat["__neg__"] = objects.EMethodWrapper(lambda value: EFloat(-value.obj))

EFloat["__abs__"] = objects.EMethodWrapper(lambda value: EFloat(abs(value.obj)))
EFloat["__floor__"] = objects.EMethodWrapper(lambda value: EInt(math.floor(value.obj)))
EFloat["__ceil__"] = objects.EMethodWrapper(lambda value: EInt(math.ceil(value.obj)))


EString["__contains__"] = objects.EMethodWrapper(
    lambda value, item: EBool(any(EString(obj).eq(item) for obj in value.obj))
)

EString["__ne__"] = objects.EMethodWrapper(lambda value, other: EBool(value.obj != other.obj))
EString["__eq__"] = objects.EMethodWrapper(lambda value, other: EBool(value.obj == other.obj))

EString["__add__"] = objects.EMethodWrapper(lambda value, other: EString(value.obj + other.obj))
EString["__mul__"] = objects.EMethodWrapper(lambda value, other: EString(value.obj * other.obj))


EList["__contains__"] = objects.EMethodWrapper(
    lambda value, item: EBool(any(obj.eq(item) for obj in value.obj))
)

EList["__ne__"] = objects.EMethodWrapper(
    lambda value, other: EBool(
        any(value_item.ne(other_item) for value_item, other_item in zip(value.obj, other.obj))
    )
)
EList["__eq__"] = objects.EMethodWrapper(
    lambda value, other: EBool(
        all(value_item.eq(other_item) for value_item, other_item in zip(value.obj, other.obj))
    )
)

EList["__add__"] = objects.EMethodWrapper(lambda value, other: EList(value.obj + other.obj))
EList["__mul__"] = objects.EMethodWrapper(lambda value, other: EList(value.obj * other.obj))

EList["__iter__"] = objects.EMethodWrapper(lambda value: iter(value.obj))

EList["__getitem__"] = objects.EMethodWrapper(lambda value, key: value.obj.__getitem__(key.obj))
EList["__setitem__"] = objects.EMethodWrapper(lambda value, key, obj: value.obj.__setitem__(key.obj, obj))
EList["__delitem__"] = objects.EMethodWrapper(lambda value, key: value.obj.__delitem__(key.obj))


ERange["__contains__"] = objects.EMethodWrapper(lambda value, item: EBool(item in value.obj))

ERange["__ne__"] = objects.EMethodWrapper(lambda value, other: EBool(value.obj != other.obj))
ERange["__eq__"] = objects.EMethodWrapper(lambda value, other: EBool(value.obj == other.obj))

ERange["__iter__"] = objects.EMethodWrapper(lambda value: iter(value.obj))

ERange["__getitem__"] = objects.EMethodWrapper(lambda value, key: value.obj.__getitem__(key.obj))
ERange["__setitem__"] = objects.EMethodWrapper(lambda value, key, obj: value.obj.__setitem__(key.obj, obj))
ERange["__delitem__"] = objects.EMethodWrapper(lambda value, key: value.obj.__delitem__(key.obj))


EType.is_ = lambda value, other: EBool(value.obj is other.obj)

EType["__call__"] = objects.EMethodWrapper(lambda value, *args: value.obj(*args))


EFunction.repr = lambda value: "function"

EFunction["__call__"] = objects.EMethodWrapper(lambda value, *args: value.obj(*args))
