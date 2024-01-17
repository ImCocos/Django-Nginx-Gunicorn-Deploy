import os

import sys

import configparser

config_file: None | str
try:
    config_file = sys.argv[1]
except IndexError:
    config_file = None


def path_or_raise(path: str) -> None:
    if not os.path.exists(path):
        raise ValueError(f'Path "{path}" does not exists!')


print('Deploy process started...')
print('Required fields will be marked with [*]')
print('Other fileds aren\'t required to fill')
print()

if not config_file:
    SITES_ENABLED_PATH = input('Your path to "sites-enabled": ') or '/etc/nginx/sites-enabled/'
    SITES_AVAILABLE_PATH = input('Your path to "sites-available": ') or '/etc/nginx/sites-available/'
    GUNICORN_FILES_PATH = input('Your path to "systemd/system": ') or '/etc/systemd/system'

    path_or_raise(SITES_ENABLED_PATH)
    path_or_raise(SITES_AVAILABLE_PATH)
    path_or_raise(GUNICORN_FILES_PATH)


    SITE_NAME_PLACEHOLDER = input('[*] Your site name: ')
    DAEMON_PLACEHOLDER = input('Your daemon: ') or '127.0.0.1'
    USER_PLACEHOLDER = input('[*] Your user: ')

    WORKDIR_PLACEHOLDER = input('[*] Your workdir: ')
    STATIC_PATH_PLACEHOLDER = input('Your path to static(without /static/): ') or WORKDIR_PLACEHOLDER
    MEDIA_PATH_PLACEHOLDER = input('Your path to media(without /media/): ') or WORKDIR_PLACEHOLDER

    path_or_raise(WORKDIR_PLACEHOLDER)
    path_or_raise(STATIC_PATH_PLACEHOLDER)
    path_or_raise(MEDIA_PATH_PLACEHOLDER)


    ENVPATH_PLACEHOLDER = input('[*] Your virtual enviroment path: ')

    path_or_raise(ENVPATH_PLACEHOLDER)


    APPLICATION_FILE_PLACEHOLDER = input('[*] Your file with wsgi/asgi application: ')

    APPLICATION_NAME_PLACEHOLDER = input('Your wsgi/asgi application name(in code): ') or 'application'
else:
    config = configparser.ConfigParser()
    config.read(config_file)
    SITES_ENABLED_PATH = config['nginx']['SitesEnabledPath'] or '/etc/nginx/sites-enabled/'
    SITES_AVAILABLE_PATH = config['nginx']['SitesAvailablePath'] or '/etc/nginx/sites-available/'
    GUNICORN_FILES_PATH = config['gunicorn']['GunicornServicesPath'] or '/etc/systemd/system'
    path_or_raise(SITES_ENABLED_PATH)
    path_or_raise(SITES_AVAILABLE_PATH)
    path_or_raise(GUNICORN_FILES_PATH)
    SITE_NAME_PLACEHOLDER = config['DEFAULT']['SiteName']
    DAEMON_PLACEHOLDER = config['DEFAULT']['Daemon'] or '127.0.0.1'
    USER_PLACEHOLDER = config['DEFAULT']['User']
    WORKDIR_PLACEHOLDER = config['DEFAULT']['WorkingDirectory']
    path_or_raise(WORKDIR_PLACEHOLDER)
    STATIC_PATH_PLACEHOLDER = config['DEFAULT']['StaticPath'] or WORKDIR_PLACEHOLDER
    MEDIA_PATH_PLACEHOLDER = config['DEFAULT']['MediaPath'] or WORKDIR_PLACEHOLDER
    ENVPATH_PLACEHOLDER = config['DEFAULT']['VirtualEnviromentPath']
    path_or_raise(ENVPATH_PLACEHOLDER)
    APPLICATION_FILE_PLACEHOLDER = config['application']['ApplicationFile']
    APPLICATION_NAME_PLACEHOLDER = config['application']['ApplicationName'] or 'application'

print()
print('Data is stored.')
print('Starting deployement...')
print()


print('---# Nginx config #---')
with open('sites-available/SITE_NAME_PLACEHOLDER') as file:
    nginx_file_row = file.read()
    print('Config template read successfully.')


nginx_file_row = nginx_file_row.replace('SITE_NAME_PLACEHOLDER', SITE_NAME_PLACEHOLDER)
print(f'Site name - {SITE_NAME_PLACEHOLDER}')

nginx_file_row = nginx_file_row.replace('DAEMON_PLACEHOLDER', DAEMON_PLACEHOLDER)
print(f'Daemon - {DAEMON_PLACEHOLDER}')

nginx_file_row = nginx_file_row.replace('STATIC_PATH_PLACEHOLDER', STATIC_PATH_PLACEHOLDER)
print(f'Static path - {STATIC_PATH_PLACEHOLDER}')

nginx_file_row = nginx_file_row.replace('MEDIA_PATH_PLACEHOLDER', MEDIA_PATH_PLACEHOLDER)
print(f'Media path - {MEDIA_PATH_PLACEHOLDER}')

with open(f'{SITE_NAME_PLACEHOLDER}.tmp', 'w') as file:
    file.write(nginx_file_row)
    print(f'{SITE_NAME_PLACEHOLDER}.tmp file created')


print()
print('---# Service config #---')
with open('system/SITE_NAME_PLACEHOLDER.service') as file:
    service_file_row = file.read()
    print('Config template read successfully.')


service_file_row = service_file_row.replace('SITE_NAME_PLACEHOLDER', SITE_NAME_PLACEHOLDER)
print(f'Site name - {SITE_NAME_PLACEHOLDER}')

service_file_row = service_file_row.replace('USER_PLACEHOLDER', USER_PLACEHOLDER)
print(f'User - {USER_PLACEHOLDER}')

service_file_row = service_file_row.replace('WORKDIR_PLACEHOLDER', WORKDIR_PLACEHOLDER)
print(f'Workdir - {WORKDIR_PLACEHOLDER}')

service_file_row = service_file_row.replace('ENVPATH_PLACEHOLDER', ENVPATH_PLACEHOLDER)
print(f'Virtual enviroment - {ENVPATH_PLACEHOLDER}')

service_file_row = service_file_row.replace('APPLICATION_FILE_PLACEHOLDER', APPLICATION_FILE_PLACEHOLDER)
print(f'Application file - {APPLICATION_FILE_PLACEHOLDER}')

service_file_row = service_file_row.replace('APPLICATION_NAME_PLACEHOLDER', APPLICATION_NAME_PLACEHOLDER)
print(f'Application name - {APPLICATION_NAME_PLACEHOLDER}')


with open(f'{SITE_NAME_PLACEHOLDER}.service.tmp', 'w') as file:
    file.write(service_file_row)
    print(f'{SITE_NAME_PLACEHOLDER}.service.tmp file created')


print()
print('---# Socket config #---')
with open('system/SITE_NAME_PLACEHOLDER.socket') as file:
    socket_file_row = file.read()
    print('Config template read successfully.')


socket_file_row = socket_file_row.replace('SITE_NAME_PLACEHOLDER', SITE_NAME_PLACEHOLDER)
print(f'Site name - {SITE_NAME_PLACEHOLDER}')


with open(f'{SITE_NAME_PLACEHOLDER}.socket.tmp', 'w') as file:
    file.write(socket_file_row)
    print(f'{SITE_NAME_PLACEHOLDER}.socket.tmp file created')


print()
print('Configs were created successfully')
print(f'Starting moving configs to nginx & system dirs...')
print()

confirmation = input('Are everything right?[Y/n, Yes/no]: ').lower()
if confirmation in ('n', 'no'):
    print('Configs will be deleted.')
    os.system(f'rm {SITE_NAME_PLACEHOLDER}.tmp')
    os.system(f'rm {SITE_NAME_PLACEHOLDER}.service.tmp')
    os.system(f'rm {SITE_NAME_PLACEHOLDER}.socket.tmp')


os.system(f'sudo cp {SITE_NAME_PLACEHOLDER}.tmp {SITES_ENABLED_PATH}/{SITE_NAME_PLACEHOLDER}')
os.system(f'sudo mv {SITE_NAME_PLACEHOLDER}.tmp {SITES_AVAILABLE_PATH}/{SITE_NAME_PLACEHOLDER}')
os.system(f'sudo mv {SITE_NAME_PLACEHOLDER}.service.tmp {GUNICORN_FILES_PATH}/{SITE_NAME_PLACEHOLDER}.service')
os.system(f'sudo mv {SITE_NAME_PLACEHOLDER}.socket.tmp {GUNICORN_FILES_PATH}/{SITE_NAME_PLACEHOLDER}.socket')


print('Configs were moved successfully.')
print(f'Enabling {SITE_NAME_PLACEHOLDER}, starting gunicorn and reloading nginx...')
print()

os.system(f'sudo systemctl enable {SITE_NAME_PLACEHOLDER}')
os.system(f'sudo systemctl start {SITE_NAME_PLACEHOLDER}')
os.system('sudo systemctl daemon-reload')
os.system('sudo systemctl restart nginx')

print(f'All done!')
print(f'Try to visit {DAEMON_PLACEHOLDER}')
