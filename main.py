# import os

import sys

from app import Router

from site_config import Site

from completer import Completer


# CWD = os.path.dirname(__file__)
router = Router()
# Completer(
#     [
#         'help',
#         'make',
#         'start',
#         'stop',
#         'reload',
#         'delete',
#         'status-json',
#         'status',
#     ],
#     [
#         name.replace('.ini')
#         for name in os.listdr(os.path.join(CWD, 'sites/'))
#         if '.ini' in name
#     ]
# )

@router.handler('list')
def sites_list():
    Site.list()

@router.handler('help')
def help():
    string = '''
help - all flags

list - list of all sites

make <SiteName> - creates configs and starts site

start <SiteName> - starts site
stop <SiteName> - stops site
reload <SiteName> - reloads site
delete <SiteName> - deletes ALL site configs beside <SiteName>.ini

status-json <SiteName> - status about configs in json
status <SiteName> - status about configs
 [+] - config exists
 [-] - config does not exists
'''.strip()
    print(string)

@router.handler('make')
def make(name: str):
    site = Site(name)
    site.make()
    site.print_status()

@router.handler('start')
def start(name: str):
    site = Site(name)
    site.start()
    site.print_status()

@router.handler('stop')
def stop(name: str):
    site = Site(name)
    site.stop()
    site.print_status()

@router.handler('reload')
def reload(name: str):
    site = Site(name)
    site.reload()
    site.print_status()

@router.handler('delete')
def delete(name: str):
    site = Site(name)
    confirmation = input(f'Are you sure? This will remove ALL {name} configs.[y/N]').lower()
    if confirmation in ('n', 'no'):
        print('Configs will not be deleted.')
        return
    print(f'Deleting configs...')
    site.delete()
    site.print_status()

@router.handler('status')
def status(name: str):
    site = Site(name)
    site.print_status()

@router.handler('status-json')
def status_json(name: str):
    site = Site(name)
    print(site.status())

@router.handler()
def unbound():
    print('Unbound command! Try "sitemanager help"')


if __name__ == '__main__':
    router(sys.argv[1:])
