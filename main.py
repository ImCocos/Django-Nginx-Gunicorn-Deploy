import sys

from site_config import Site


try:
    cmd = sys.argv[1]
except IndexError:
    raise AttributeError('You can\'t call without flags!')


if cmd == 'help':
    string = '''
help - all flags

make sites/<SiteName>.ini - creates configs and starts site
start sites/<SiteName>.ini - starts site
stop sites/<SiteName>.ini - stops site
reload sites/<SiteName>.ini - reloads site
delete sites/<SiteName>.ini - deletes ALL site configs beside <SiteName>.ini
'''.strip()
    print(string)
    sys.exit(1)


if cmd not in ('make', 'start', 'stop', 'delete', 'reload'):
    print('Unbound command! Try "sitemanager help"')
    sys.exit(1)

try:
    arg = sys.argv[2]
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
