#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import annotations

import math

from .enter_builtin_types import *
from .objects import EnterObject


none = ENoneType(None)
false = EBool(False)
true = EBool(True)

inf = EFloat(math.inf)
nan = EFloat(math.nan)
pi = EFloat(math.pi)
e = EFloat(math.e)


@EFunction
def abs_(x: EnterObject) -> EnterObject:
    return abs(x)


@EFunction
def floor(x: EnterObject) -> EnterObject:
    return x.floor()


@EFunction
def ceil(x: EnterObject) -> EnterObject:
    return x.ceil()


@EFunction
def typeof(obj: EnterObject) -> EnterObject:
    return EType(obj.obj_type)


@EFunction
def isinstance_(obj: EnterObject, cls: EnterObject) -> EnterObject:
    return EBool(typeof.call(obj) is cls)


@EFunction
def print_(obj: EnterObject) -> EnterObject:
    print(obj)
    return none


Object = EType(EObject)
NoneType = EType(ENoneType)
Bool = EType(EBool)
Int = EType(EInt)
Float = EType(EFloat)
String = EType(EString)
List = EType(EList)
Type = EType(EType)
Function = EType(EFunction)


all_dict: dict[str, EnterObject] = {
    "Bool": Bool,
    "Float": Float,
    "Function": Function,
    "Object": Object,
    "Int": Int,
    "List": List,
    "String": String,
    "Type": Type,
    "abs": abs_,
    "ceil": ceil,
    "e": e,
    "false": false,
    "floor": floor,
    "inf": inf,
    "isinstance": isinstance_,
    "nan": nan,
    "none": none,
    "pi": pi,
    "print": print_,
    "true": true,
    "typeof": typeof,
}
