from typing import Callable


class Cmd:
    def __repr__(self) -> str:
        return f'<Cmd({self.text})>'

    def __str__(self) -> str:
        return f'<Cmd({self.text})>'

    def __init__(self, arg: str) -> None:
        if arg.startswith('--'):
            raise AttributeError(f'Cmd must not starts with "--", "{arg}" is not acessed!')
        self.text = arg

    def __eq__(self, other: object) -> bool:
        return (self.text == other.text) if isinstance(other, self.__class__) else (self.text == other)


class Arg:
    def __repr__(self) -> str:
        return f'<Arg({self.name}: {self.value}, req: {self.required})>'

    def __str__(self) -> str:
        return f'<Arg({self.name}: {self.value}, req: {self.required})>'

    def __init__(self, name: str, required: bool = False, value: None | str = None) -> None:
        self.name = name
        self.required = required
        self.value = value


class Flag:
    def __repr__(self) -> str:
        return f'<Flag({self.text})>'

    def __str__(self) -> str:
        return f'<Flag({self.text})>'

    def __init__(self, arg: str) -> None:
        if not arg.startswith('--'):
            raise AttributeError(f'Flag must starts with "--", "{arg}" is not acessed!')
        self.text = arg

    def __eq__(self, other: object) -> bool:
        return (self.text == other.text) if isinstance(other, self.__class__) else (self.text == other)


class Resolver:
    def __call__(self, *args: str) -> tuple[tuple[Flag, ...], tuple[Arg, ...]]:
        flags: tuple[Flag, ...] = tuple((Flag(arg) for arg in args if arg.startswith('--')))
        arguments: tuple[Arg, ...] = tuple((Arg(name='', value=arg) for arg in args if not arg.startswith('--')))
        return flags, arguments
