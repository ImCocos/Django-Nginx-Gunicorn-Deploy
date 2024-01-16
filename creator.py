import os


def get_or_raise(string: str) -> str:
    res = input(string)
    if not res:
        raise ValueError(f'"{string}" is reuqiered!')
    return res


def cmd(command: str) -> int:
    return os.system(command)


def root_cmd(command: str) -> int:
    return os.system('sudo ' + command)


print(f'Requiered fields are marked with "*"')
PYTHON_PATH = input('Path to python(if none provided "python3.11" will be used): ') or 'python3.11'

WORKDIR_PLACEHOLDER = get_or_raise('* Your workdir: ')

SITE_NAME = get_or_raise('* Your site name for nginx and gunicorn: ')
SITE_NAME_FOR_DJANGIO = input(f'Your site name for django(if none provided "{SITE_NAME.lower()}" will be used): ') or SITE_NAME.lower()

DAEMON = input('Your daemon(if none provided "127.0.0.1" will be used): ') or '127.0.0.1'
USER = get_or_raise('Your user: ')

SITE_PATH = os.path.join(WORKDIR_PLACEHOLDER, SITE_NAME)

ENV_PATH = os.path.join(SITE_PATH, 'env')


cmd(f'mkdir {os.path.join(WORKDIR_PLACEHOLDER, SITE_NAME)}')
cmd(f'{PYTHON_PATH} -m venv {ENV_PATH}')
cmd(f'''
cd {SITE_PATH};
{os.path.join(ENV_PATH, "bin/python3.11")} -m pip install django gunicorn --no-cache-dir;
{os.path.join(ENV_PATH, "bin/python3.11")} -m django startproject {SITE_NAME_FOR_DJANGIO} .;
''')


with open(os.path.join(SITE_PATH, SITE_NAME_FOR_DJANGIO, 'settings.py'), 'r') as file:
    row = file.read()
    row = row.replace('ALLOWED_HOSTS = []', f'ALLOWED_HOSTS = ["{DAEMON}"]')

with open(os.path.join(SITE_PATH, SITE_NAME_FOR_DJANGIO, 'settings.py'), 'w') as file:
    file.write(row)


dot_tmp = f"""
{SITE_NAME}
{DAEMON}
{USER}
{SITE_PATH}
{SITE_PATH}
{SITE_PATH}
env
{SITE_NAME_FOR_DJANGIO}
wsgi
application
y
""".strip()


with open('.tmp', 'w') as file:
    file.write(dot_tmp)

cmd(f'{os.path.realpath(__file__).strip("creator.py")};{PYTHON_PATH} deploy.py < .tmp')
