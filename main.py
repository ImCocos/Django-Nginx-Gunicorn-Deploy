import os


SITES_ENABLED_PATH = '/etc/nginx/sites-enabled/'
SITES_AVAILABLE_PATH = '/etc/nginx/sites-available/'
GUNICORN_FILES_PATH = '/etc/systemd/system'

if not os.path.exists(SITES_ENABLED_PATH):
    raise ValueError(f'Path {SITES_ENABLED_PATH} does not exists!')

if not os.path.exists(GUNICORN_FILES_PATH):
    raise ValueError(f'Path {GUNICORN_FILES_PATH} does not exists!')


SITE_NAME_PLACEHOLDER = input('Your site name: ')
DAEMON_PLACEHOLDER = input('Your daemon: ')
USER_PLACEHOLDER = input('Your user: ')

STATIC_PATH_PLACEHOLDER = input('Your path to static(without /static/): ')
MEDIA_PATH_PLACEHOLDER = input('Your path to media(without /media/): ')

WORKDIR_PLACEHOLDER = input('Your workdir: ')
ENV_NAME = input('Your virtual enviroment name: ')
ENVPATH_PLACEHOLDER = os.path.join(WORKDIR_PLACEHOLDER, ENV_NAME)

DJANGO_PROJECT_NAME_PLACEHOLDER = input('Your django project name: ')
MODE_PLACEHOLDER = input('Your mode(wsgi/asgi): ')
if MODE_PLACEHOLDER not in ('wsgi', 'asgi'):
    raise ValueError(f'{MODE_PLACEHOLDER} is not a valid mode!')
APPLICATION_NAME_PLACEHOLDER = input('Your wsgi/asgi application name: ')

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
    print('{SITE_NAME_PLACEHOLDER}.tmp file created')

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
service_file_row = service_file_row.replace('DJANGO_PROJECT_NAME_PLACEHOLDER', DJANGO_PROJECT_NAME_PLACEHOLDER)
print(f'Django project name - {DJANGO_PROJECT_NAME_PLACEHOLDER}')
service_file_row = service_file_row.replace('MODE_PLACEHOLDER', MODE_PLACEHOLDER)
print(f'Mode(wsgi/asgi) - {MODE_PLACEHOLDER}')
service_file_row = service_file_row.replace('APPLICATION_NAME_PLACEHOLDER', APPLICATION_NAME_PLACEHOLDER)
print(f'Application name - {APPLICATION_NAME_PLACEHOLDER}')

with open(f'{SITE_NAME_PLACEHOLDER}.service.tmp', 'w') as file:
    file.write(service_file_row)
    print('{SITE_NAME_PLACEHOLDER}.service.tmp file created')

print()
print('---# Socket config #---')
with open('system/SITE_NAME_PLACEHOLDER.socket') as file:
    scoket_file_row = file.read()
    print('Config template read successfully.')

scoket_file_row = scoket_file_row.replace('SITE_NAME_PLACEHOLDER', SITE_NAME_PLACEHOLDER)
print(f'Site name - {SITE_NAME_PLACEHOLDER}')

with open(f'{SITE_NAME_PLACEHOLDER}.socket.tmp', 'w') as file:
    file.write(scoket_file_row)
    print('{SITE_NAME_PLACEHOLDER}.socket.tmp file created')

print()
print('Configs were created successfully')
print(f'Starting copipasting to nginx & system dirs...')
print()

confirmation = input('Are everything right?[Y/n, Yes/no]: ').lower()
if confirmation in ('n', 'no'):
    print('Configs will be deleted.')
    os.system(f'rm {SITE_NAME_PLACEHOLDER}.tmp')
    os.system(f'rm {SITE_NAME_PLACEHOLDER}.service.tmp')
    os.system(f'rm {SITE_NAME_PLACEHOLDER}.socket.tmp')

os.system(f'sudo cp {SITE_NAME_PLACEHOLDER}.tmp {SITES_ENABLED_PATH}/{SITE_NAME_PLACEHOLDER}')
os.system(f'sudo cp {SITE_NAME_PLACEHOLDER}.tmp {SITES_AVAILABLE_PATH}/{SITE_NAME_PLACEHOLDER}')
os.system(f'sudo cp {SITE_NAME_PLACEHOLDER}.service.tmp {GUNICORN_FILES_PATH}/{SITE_NAME_PLACEHOLDER}.service')
os.system(f'sudo cp {SITE_NAME_PLACEHOLDER}.socket.tmp {GUNICORN_FILES_PATH}/{SITE_NAME_PLACEHOLDER}.socket')

print('Configs pasted successfully.')
print(f'Enabling {SITE_NAME_PLACEHOLDER} and reloading nginx...')
print()

os.system(f'sudo systemctl enable {SITE_NAME_PLACEHOLDER}')
os.system(f'sudo systemctl start {SITE_NAME_PLACEHOLDER}')
os.system('sudo systemctl daemon-reload')
os.system(f'sudo systemctl restart {SITE_NAME_PLACEHOLDER}')
os.system('sudo systemctl restart nginx')

print(f'Configs were copiposting successfully!')
print(f'Try to visit {DAEMON_PLACEHOLDER}')