import sys

from app import Router

from site_config import Site

from resolver import Cmd, Flag, Arg


router = Router()


@router.handler(Cmd('status'), Arg('name', required=True), Flag('--json'))
def status(cmd: str, *flags: str, name: str | None):
    if '--json' in flags:
        print(f'do json - {name}')
        return
    print(f'do normal - {name}')


if __name__ == '__main__':
    router(sys.argv[1:])
