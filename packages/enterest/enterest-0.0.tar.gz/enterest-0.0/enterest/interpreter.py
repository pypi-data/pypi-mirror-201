#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Callable

from lark import Lark
from lark.tree import Tree
from lark.visitors import Interpreter

from . import enter_builtins
from .objects import EnterObject
from .scope import *


class EInterpreter(Interpreter):
    root_scope: Scope
    now_scope: Scope
    arguments: list[str]

    def __init__(self):
        super().__init__()
        self.root_scope = Scope(
            interpreter=self,
            master=None,
        )
        self.now_scope = self.root_scope

    def statements(self, tree: Tree) -> list[dict[str, EnterObject]]:
        return [self.visit(child) for child in tree.children]

    def statement(self, tree: Tree) -> dict[str, EnterObject]:
        return self.visit(tree.children[0])

    def expression_statement(self, tree: Tree) -> dict[str, EnterObject]:
        return {"result": self.visit(tree.children[0])}

    def set_(self, tree: Tree) -> dict[str, EnterObject]:
        expression = self.visit(tree.children[1])

        for child in tree.children[0].children:
            for target_child in child.children:
                target = self.visit(target_child)
                if isinstance(target, str):
                    self.now_scope[target] = expression
                elif isinstance(target, tuple):
                    if isinstance(target[1], str):
                        target[0][target[1]] = expression
                    elif isinstance(target[1], EnterObject):
                        target[0].setitem(target[1], expression)

        return {}

    def orset(self, tree: Tree) -> dict[str, EnterObject]:
        self.now_scope[self.visit(tree.children[0])] |= self.visit(tree.children[1])
        return {}

    def xorset(self, tree: Tree) -> dict[str, EnterObject]:
        self.now_scope[self.visit(tree.children[0])] ^= self.visit(tree.children[1])
        return {}

    def andset(self, tree: Tree) -> dict[str, EnterObject]:
        self.now_scope[self.visit(tree.children[0])] &= self.visit(tree.children[1])
        return {}

    def lshiftset(self, tree: Tree) -> dict[str, EnterObject]:
        self.now_scope[self.visit(tree.children[0])] <<= self.visit(tree.children[1])
        return {}

    def rshiftset(self, tree: Tree) -> dict[str, EnterObject]:
        self.now_scope[self.visit(tree.children[0])] >>= self.visit(tree.children[1])
        return {}

    def addset(self, tree: Tree) -> dict[str, EnterObject]:
        self.now_scope[self.visit(tree.children[0])] += self.visit(tree.children[1])
        return {}

    def subset(self, tree: Tree) -> dict[str, EnterObject]:
        self.now_scope[self.visit(tree.children[0])] -= self.visit(tree.children[1])
        return {}

    def mulset(self, tree: Tree) -> dict[str, EnterObject]:
        self.now_scope[self.visit(tree.children[0])] *= self.visit(tree.children[1])
        return {}

    def divset(self, tree: Tree) -> dict[str, EnterObject]:
        self.now_scope[self.visit(tree.children[0])] /= self.visit(tree.children[1])
        return {}

    def modset(self, tree: Tree) -> dict[str, EnterObject]:
        self.now_scope[self.visit(tree.children[0])] %= self.visit(tree.children[1])
        return {}

    def powset(self, tree: Tree) -> dict[str, EnterObject]:
        self.now_scope[self.visit(tree.children[0])] **= self.visit(tree.children[1])
        return {}

    def del_(self, tree: Tree) -> dict[str, EnterObject]:
        for child in tree.children[0].children:
            del self.now_scope[self.visit(child)]
        return {}

    def return_(self, tree: Tree) -> dict[str, EnterObject]:
        return {"return": self.visit(tree.children[0]) if 0 < len(tree.children) else enter_builtins.none}

    def expression(self, tree: Tree) -> EnterObject:
        return self.visit(tree.children[0])

    def equal_targets(self, tree: Tree) -> list[str | tuple[EnterObject, EnterObject]]:
        return [self.visit(child) for child in tree.children]

    def targets(self, tree: Tree) -> list[str | tuple[EnterObject, EnterObject]]:
        return [self.visit(child) for child in tree.children]

    def target(self, tree: Tree) -> str | tuple[EnterObject, EnterObject]:
        return self.visit(tree.children[0])

    def subscription(self, tree: Tree) -> tuple[EnterObject, EnterObject]:
        return self.visit(tree.children[0]), self.visit(tree.children[1])

    def attribution(self, tree: Tree) -> tuple[EnterObject, str]:
        return self.visit(tree.children[0]), self.visit(tree.children[1])

    def get(self, tree: Tree) -> EnterObject:
        return self.now_scope[self.visit(tree.children[0])]

    @staticmethod
    def identifier(tree: Tree) -> str:
        return tree.children[0].value

    def while_(self, tree: Tree) -> EnterObject:
        result = []
        while bool(self.visit(tree.children[1])):
            result += [self.visit(tree.children[0])]
        return enter_builtins.List.call(result)

    def for_(self, tree: Tree) -> EnterObject:
        result = []
        function = self.visit(tree.children[1])
        for obj in self.visit(tree.children[0]):
            result += [function.call(obj)]
        return enter_builtins.List.call(result)

    def func(self, tree: Tree) -> EnterObject:
        arguments: list[str] = []
        for child in tree.children[:-1]:
            arguments.append(self.visit(child))

        def _func(interpreter: EInterpreter, arg_ids: tuple[str], func_tree: Tree) -> Callable:
            def _wrapper(*args: EnterObject) -> EnterObject:
                nonlocal interpreter, arg_ids, func_tree

                scope = Scope(
                    master=interpreter.now_scope,
                    values={key: value for key, value in zip(arg_ids, args)},
                    interpreter=interpreter,
                )
                interpreter.now_scope = scope
                result = interpreter.visit(func_tree)
                interpreter.now_scope = scope.master
                return result
            return _wrapper

        return enter_builtins.EFunction(_func(self, tuple(arguments), tree.children[-1]))

    def then_else(self, tree: Tree) -> EnterObject:
        return self.visit(tree.children[1]) if self.visit(tree.children[0]) else self.visit(tree.children[2])

    def then(self, tree: Tree) -> EnterObject:
        return self.visit(tree.children[1]) if self.visit(tree.children[0]) else enter_builtins.none

    def in_(self, tree: Tree) -> EnterObject:
        return self.visit(tree.children[1]).contains(self.visit(tree.children[0]))

    def is_(self, tree: Tree) -> EnterObject:
        return enter_builtins.EBool(self.visit(tree.children[0]) is self.visit(tree.children[1]))

    def lt(self, tree: Tree) -> EnterObject:
        return self.visit(tree.children[0]).lt(self.visit(tree.children[1]))

    def le(self, tree: Tree) -> EnterObject:
        return self.visit(tree.children[0]).le(self.visit(tree.children[1]))

    def gt(self, tree: Tree) -> EnterObject:
        return self.visit(tree.children[0]).gt(self.visit(tree.children[1]))

    def ge(self, tree: Tree) -> EnterObject:
        return self.visit(tree.children[0]).ge(self.visit(tree.children[1]))

    def ne(self, tree: Tree) -> EnterObject:
        return self.visit(tree.children[0]).ne(self.visit(tree.children[1]))

    def eq(self, tree: Tree) -> EnterObject:
        return self.visit(tree.children[0]).eq(self.visit(tree.children[1]))

    def or_(self, tree: Tree) -> EnterObject:
        return self.visit(tree.children[0]) | self.visit(tree.children[1])

    def xor(self, tree: Tree) -> EnterObject:
        return self.visit(tree.children[0]) ^ self.visit(tree.children[1])

    def and_(self, tree: Tree) -> EnterObject:
        return self.visit(tree.children[0]) & self.visit(tree.children[1])

    def lshift(self, tree: Tree) -> EnterObject:
        return self.visit(tree.children[0]) << self.visit(tree.children[1])

    def rshift(self, tree: Tree) -> EnterObject:
        return self.visit(tree.children[0]) >> self.visit(tree.children[1])

    def add(self, tree: Tree) -> EnterObject:
        return self.visit(tree.children[0]) + self.visit(tree.children[1])

    def sub(self, tree: Tree) -> EnterObject:
        return self.visit(tree.children[0]) - self.visit(tree.children[1])

    def mul(self, tree: Tree) -> EnterObject:
        return self.visit(tree.children[0]) * self.visit(tree.children[1])

    def div(self, tree: Tree) -> EnterObject:
        return self.visit(tree.children[0]) / self.visit(tree.children[1])

    def pow(self, tree: Tree) -> EnterObject:
        return self.visit(tree.children[0]) ** self.visit(tree.children[1])

    def mod(self, tree: Tree) -> EnterObject:
        return self.visit(tree.children[0]) % self.visit(tree.children[1])

    def pos(self, tree: Tree) -> EnterObject:
        return +self.visit(tree.children[0])

    def neg(self, tree: Tree) -> EnterObject:
        return -self.visit(tree.children[0])

    def not_(self, tree: Tree) -> EnterObject:
        return ~self.visit(tree.children[0])

    def literal(self, tree: Tree) -> EnterObject:
        return self.visit(tree.children[0])

    @staticmethod
    def string(tree: Tree) -> EnterObject:
        return enter_builtins.EString(str(tree.children[0])[1:-1])

    @staticmethod
    def integer(tree: Tree) -> EnterObject:
        return enter_builtins.EInt(int(tree.children[0]))

    @staticmethod
    def floating(tree: Tree) -> EnterObject:
        return enter_builtins.EFloat(float(tree.children[0]))

    def list_(self, tree: Tree) -> EnterObject:
        return enter_builtins.EList(tuple(self.visit(child) for child in tree.children))

    def call(self, tree: Tree) -> EnterObject:
        arguments = []
        for child in tree.children[1:]:
            arguments.append(self.visit(child))
        return self.visit(tree.children[0]).call(*arguments)

    def attr(self, tree: Tree) -> EnterObject:
        return self.visit(tree.children[0])[self.visit(tree.children[1])]

    def item(self, tree: Tree) -> EnterObject:
        return self.visit(tree.children[0]).getitem(self.visit(tree.children[1]))

    def parenthesis(self, tree: Tree) -> EnterObject:
        return self.visit(tree.children[0])

    def block(self, tree: Tree) -> EnterObject:
        value = enter_builtins.none
        for child in tree.children[0].children:
            return_ = self.visit(child)
            if "return" in return_:
                value = return_["return"]
                break
        return value


class Enter:
    def __init__(self):
        with open("./enter.lark", encoding="utf-8") as grammar:
            self.parser = Lark(grammar.read())

        self.interpreter = EInterpreter()

        self.global_values = self.interpreter.root_scope._values = {**enter_builtins.all_dict}

        with open("./enter_builtins.enter", encoding="utf-8") as file:
            self.exec(file.read())

    @staticmethod
    def raise_(err: str) -> None:
        print(err)

    def exec(self, code: str) -> dict[str, EnterObject]:
        return self.interpreter.visit(self.parser.parse(code))
