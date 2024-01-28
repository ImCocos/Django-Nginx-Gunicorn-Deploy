import os

import sys

from app import Router

from site_config import Site

from resolver import Cmd, Flag, Arg


router = Router()


def get_site_or_error(name: str | None) -> Site:
    if not name:
        site = Site.try_get_site_by_cwd()
        if not site:
            raise AttributeError(f'No site with such working directory - "{os.getcwd()}"')
        return site
    else:
        return Site(name)


@router.handler(Cmd('list'))
def sites_list(cmd: str, ):
    Site.list()

@router.handler(Cmd('help'))
def help(cmd: str, ):
    string = '''
help - all flags

list - list of all sites

make [<SiteName>] - creates configs and starts site # can be called from project workdir without <SiteName>

start [<SiteName>] - starts site # can be called from project workdir without <SiteName>
stop [<SiteName>] - stops site # can be called from project workdir without <SiteName>
reload [<SiteName>] - reloads site # can be called from project workdir without <SiteName>
delete [<SiteName>] - deletes ALL site configs beside <SiteName>.ini # can be called from project workdir without <SiteName>
status-json [<SiteName>] - status about configs in json # can be called from project workdir without <SiteName>
status [<SiteName>] - status about configs # can be called from project workdir without <SiteName>
 [+] - config exists
 [-] - config does not exists
'''.strip()
    print(string)

@router.handler(Cmd('make'), Arg('name'))
def make(cmd: str, name: str | None = None):
    site = get_site_or_error(name)
    site.make()
    site.print_status()

@router.handler(Cmd('start'), Arg('name'))
def start(cmd: str, name: str | None = None):
    site = get_site_or_error(name)
    site.start()
    site.print_status()

@router.handler(Cmd('stop'), Arg('name'))
def stop(cmd: str, name: str | None = None):
    site = get_site_or_error(name)
    site.stop()
    site.print_status()

@router.handler(Cmd('reload'), Arg('name'))
def reload(cmd: str, name: str | None = None):
    site = get_site_or_error(name)
    site.reload()
    site.print_status()

@router.handler(Cmd('delete'), Arg('name'))
def delete(cmd: str, name: str | None = None):
    site = get_site_or_error(name)
    confirmation = input(f'Are you sure? This will remove ALL {name} configs.[y/N]').lower()
    if confirmation in ('n', 'no'):
        print('Configs will not be deleted.')
        return
    print(f'Deleting configs...')
    site.delete()
    site.print_status()

@router.handler(Cmd('status'), Arg('name'), Flag('--json'))
def status(cmd: str, *flags: str, name: str | None = None):
    if '--json' in flags:
        site = get_site_or_error(name)
        print(site.status())
        return
    site = get_site_or_error(name)
    site.print_status()

@router.handler()
def unbound(cmd: str, ):
    print('Unbound command! Try "sitemanager help"')


if __name__ == '__main__':
    router(sys.argv[1:])
