from typing import Callable, Any, List

import sys


class Handler:
    def __init__(self, foo: Callable, cmd: str | None, *flags: str) -> None:
        self.cmd = cmd
        self.flags = flags
        self.foo = foo

    def can_handle(self, *args: str) -> bool:
        try:
            cmd: str = args[0]
        except IndexError:
            return False

        return (
            (cmd == self.cmd)
            and
            ((len(args[1:]) == len([
                flag
                for flag in self.flags
                if not isinstance(None, self.foo.__annotations__[flag])
            ])) or len(args[1:]) == len(self.flags))
        ) or not self.cmd

    def handle(self, *args: str) -> None:
        self.foo(
            **{
                name: value
                for name, value in zip(self.flags, args[1:])
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

    def handler(self, cmd: str | None = None) -> Callable:
        def decorator(foo: Callable) -> None:
            handler = Handler(
                foo,
                cmd,
                *[
                    key
                    for key in foo.__annotations__.keys()
                    if key != 'return'
                ]
            )
            self.handlers.append(handler)
        return decorator
