from typing import Callable, Any, List, Tuple

import sys

from resolver import Cmd, Flag, Arg, Resolver


class Handler:
    def __init__(self, foo: Callable, cmd: Cmd | None, *flags_and_args: tuple[Arg | Flag]) -> None:
        self.cmd: Cmd | None = cmd
        self.flags: tuple[Flag, ...] = tuple((x for x in flags_and_args if isinstance(x, Flag)))
        self.args: tuple[Arg, ...] = tuple((x for x in flags_and_args if isinstance(x, Arg)))
        self.foo: Callable = foo

    def can_handle(self, *args: str) -> bool:
        if not self.cmd:
            return True

        if len(args) < 1:
            return False

        cmd = Cmd(args[0])
        args = args[1:]

        if not self.cmd == cmd:
            return False

        resolve = Resolver()

        flags: tuple[Flag, ...]
        arguments: tuple[Arg, ...]
        flags, arguments = resolve(*args)

        for flag in flags:
            if not flag in self.flags:
                raise AttributeError(f'Flag "{flag.text}" is not acessed with command "{cmd.text}"!')

        if len(tuple((arg for arg in self.args if arg.required))) > len(arguments):
            raise AttributeError(f'Not all reuired arguments were provided!')

        if len(self.args) < len(arguments):
            raise AttributeError(f'Too many arguments({self.args} < {arguments})!')

        return True

    def handle(self, *args: str) -> None:
        resolve = Resolver()
        flags, arguments = resolve(*args[1:])
        self.foo(
            *(
                Cmd(arg)
                if Cmd is self.foo.__annotations__.get('cmd')
                else arg
                for arg in args[0:1]
            ),
            *(
                arg
                if Flag is self.foo.__annotations__.get('flags')
                else arg.text
                for arg in flags
            ),
            **{
                reqarg.name:
                    Arg(reqarg.name, value=arg.value)
                    if Arg is self.foo.__annotations__.get(reqarg.name)
                    else arg.value
                for reqarg, arg in zip(self.args, arguments)
            }
        )

class Router:
    def __init__(self) -> None:
        self.handlers: List[Handler] = []

    def __call__(self, args: List[str]) -> None:
        for handler in self.handlers:
            if handler.can_handle(*args):
                handler.handle(*args)
                break

    def handler(self, cmd: Cmd | None = None, *flags_and_args) -> Callable:
        def decorator(foo: Callable) -> None:
            handler = Handler(
                foo,
                cmd,
                *flags_and_args,
            )
            self.handlers.append(handler)
        return decorator
