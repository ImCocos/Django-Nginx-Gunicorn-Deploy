import sys

import os

from site_config import Site


try:
    cmd = sys.argv[1]
except IndexError:
    print('Try "sitemanager help"')
    raise AttributeError('You can\'t call without flags!')


if cmd == 'list':
    Site.list()
    sys.exit(1)

if cmd == 'help':
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
    sys.exit(1)


try:
    arg = 'sites/' + sys.argv[2] + '.ini'
except IndexError:
    raise AttributeError(f'Pass argument with {cmd}')

if cmd == 'make':
    site = Site(arg)
    site.make()
    site.print_status()
    sys.exit(1)

if cmd == 'start':
    site = Site(arg)
    site.start()
    site.print_status()
    sys.exit(1)

if cmd == 'stop':
    site = Site(arg)
    site.stop()
    site.print_status()
    sys.exit(1)

if cmd == 'reload':
    site = Site(arg)
    site.reload()
    site.print_status()
    sys.exit(1)

if cmd == 'delete':
    site = Site(arg)
    confirmation = input(f'Are you sure? This will remove ALL {arg} configs.[y/N]').lower()
    if confirmation in ('n', 'no'):
        print('Configs will not be deleted.')
        sys.exit(1)
    print(f'Deleting configs...')
    site.delete()
    site.print_status()
    sys.exit(1)

if cmd == 'status':
    site = Site(arg)
    site.print_status()
    sys.exit(1)

if cmd == 'status-json':
    site = Site(arg)
    print(site.status())
    sys.exit(1)


print('Unbound command! Try "sitemanager help"')
