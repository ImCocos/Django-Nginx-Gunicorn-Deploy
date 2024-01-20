import sys

from site_config import Site


try:
    cmd = sys.argv[1]
except IndexError:
    print('Try "sitemanager help"')
    raise AttributeError('You can\'t call without flags!')


if cmd == 'help':
    string = '''
help - all flags

make <SiteName> - creates configs and starts site
start <SiteName> - starts site
stop <SiteName> - stops site
reload <SiteName> - reloads site
delete <SiteName> - deletes ALL site configs beside <SiteName>.ini
status <SiteName> - is active or not
'''.strip()
    print(string)
    sys.exit(1)


if cmd not in (
    'make',
    'start',
    'stop',
    'delete',
    'reload',
    'status',
):
    print('Unbound command! Try "sitemanager help"')
    sys.exit(1)

try:
    arg = 'sites/' + sys.argv[2] + '.ini'
except IndexError:
    raise AttributeError(f'Pass argument with {cmd}')

if cmd == 'make':
    site = Site(arg)
    site.make()
    sys.exit(1)

if cmd == 'start':
    site = Site(arg)
    site.start()
    sys.exit(1)

if cmd == 'stop':
    site = Site(arg)
    site.stop()
    sys.exit(1)

if cmd == 'reload':
    site = Site(arg)
    site.reload()
    sys.exit(1)

if cmd == 'delete':
    site = Site(arg)
    confirmation = input(f'Are you sure? This will remove ALL {arg} configs.[y/N]').lower()
    if confirmation in ('n', 'no'):
        print('Configs will not be deleted.')
        sys.exit(1)
    print(f'Deleting configs...')
    site.delete()
    sys.exit(1)

if cmd == 'status':
    site = Site(arg)
    status = 'active' if site.is_active() else 'inactive'
    print(f'{site.name} - {status}')
    sys.exit(1)
