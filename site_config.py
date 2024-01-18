from typing import Any

import os

import configparser


CWD = os.path.dirname(__file__)


class Site:
    def __raise_if_none(self, name: str) -> Any:
            raise AttributeError(f'"{name}" can\'t be empty!')

    def validate_paths(self, *paths) -> None:
        for path in paths:
            if not os.path.exists(path):
                raise ValueError(f'Path "{path}" does not exists!')

    def __init__(self, name: str) -> None:
        config = configparser.ConfigParser(
            allow_no_value=True,
            comment_prefixes="#",
            inline_comment_prefixes='#',
            empty_lines_in_values=True
        )
        config.read(os.path.join(CWD, name))

        defaults = configparser.ConfigParser()
        defaults.read(os.path.join(CWD, 'defaults.ini'))

        self.name = config['DEFAULT']['SiteName'] or self.__raise_if_none('SiteName')
        self.user = config['DEFAULT']['User'] or self.__raise_if_none('User')
        self.workdir = config['DEFAULT']['WorkingDirectory'] or self.__raise_if_none('WorkingDirectory')
        self.virtual_enviromnt_path = config['DEFAULT']['VirtualEnviromentPath'] or self.__raise_if_none('VirtualEnviromentPath')
        self.application_file = config['application']['ApplicationFile'] or self.__raise_if_none('ApplicationFile')

        self.application_name = config['application']['ApplicationName'] or defaults['application']['ApplicationName']
        self.sites_enabled_path = config['nginx']['SitesEnabledPath'] or defaults['nginx']['SitesEnabledPath']
        self.sites_available_path = config['nginx']['SitesAvailablePath'] or defaults['nginx']['SitesAvailablePath']
        self.gunicorn_services_path = config['gunicorn']['GunicornServicesPath'] or defaults['gunicorn']['GunicornServicesPath']
        self.daemon = config['DEFAULT']['Daemon'] or defaults['DEFAULT']['Daemon']

        self.static_path = config['DEFAULT']['StaticPath'] or self.workdir
        self.media_path = config['DEFAULT']['MediaPath'] or self.workdir

        self.validate_paths(
            self.workdir,
            self.virtual_enviromnt_path,
            self.sites_enabled_path,
            self.sites_available_path,
            self.gunicorn_services_path
        )

    def __make_nginx_config(self) -> None:
        with open(os.path.join(CWD, '.sites-available/SITE_NAME_PLACEHOLDER')) as file:
            nginx_file_row = file.read()

        nginx_file_row = nginx_file_row.replace('SITE_NAME_PLACEHOLDER', self.name)
        nginx_file_row = nginx_file_row.replace('DAEMON_PLACEHOLDER', self.daemon)
        nginx_file_row = nginx_file_row.replace('STATIC_PATH_PLACEHOLDER', self.static_path)
        nginx_file_row = nginx_file_row.replace('MEDIA_PATH_PLACEHOLDER', self.media_path)

        with open(os.path.join(CWD, f'{self.name}.tmp'), 'w') as file:
            file.write(nginx_file_row)

    def __make_gunicorn_service(self) -> None:
        with open(os.path.join(CWD, '.system/SITE_NAME_PLACEHOLDER.service')) as file:
            service_file_row = file.read()

        service_file_row = service_file_row.replace('SITE_NAME_PLACEHOLDER', self.name)
        service_file_row = service_file_row.replace('USER_PLACEHOLDER', self.user)
        service_file_row = service_file_row.replace('WORKDIR_PLACEHOLDER', self.workdir)
        service_file_row = service_file_row.replace('ENVPATH_PLACEHOLDER', self.virtual_enviromnt_path)
        service_file_row = service_file_row.replace('APPLICATION_FILE_PLACEHOLDER', self.application_file)
        service_file_row = service_file_row.replace('APPLICATION_NAME_PLACEHOLDER', self.application_name)

        with open(os.path.join(CWD, f'{self.name}.service.tmp'), 'w') as file:
            file.write(service_file_row)

    def __make_gunicorn_socket(self) -> None:
        with open(os.path.join(CWD, '.system/SITE_NAME_PLACEHOLDER.socket')) as file:
            socket_file_row = file.read()

        socket_file_row = socket_file_row.replace('SITE_NAME_PLACEHOLDER', self.name)

        with open(os.path.join(CWD, f'{self.name}.socket.tmp'), 'w') as file:
            file.write(socket_file_row)

    def __make_configs(self) -> None:
        self.__make_nginx_config()
        self.__make_gunicorn_service()
        self.__make_gunicorn_socket()

    def __move_configs(self) -> None:
        os.system(f'sudo cp {os.path.join(CWD, self.name + ".tmp")} {os.path.join(CWD, self.sites_enabled_path, self.name)}')
        os.system(f'sudo mv {os.path.join(CWD, self.name + ".tmp")} {os.path.join(CWD, self.sites_available_path, self.name)}')
        os.system(f'sudo mv {os.path.join(CWD, self.name + ".service.tmp")} {os.path.join(CWD, self.gunicorn_services_path, self.name + ".service")}')
        os.system(f'sudo mv {os.path.join(CWD, self.name + ".socket.tmp")} {os.path.join(CWD, self.gunicorn_services_path, self.name + ".socket")}')

    def reload(self) -> None:
        os.system('sudo systemctl daemon-reload')
        os.system(f'sudo systemctl restart {self.name}.socket')
        os.system(f'sudo systemctl restart {self.name}.service')
        os.system('sudo systemctl restart nginx')

    def stop(self) -> None:
        os.system(f'sudo systemctl disable {self.name}')
        os.system(f'sudo systemctl stop {self.name}')
        os.system(f'sudo rm {self.sites_enabled_path}/{self.name}')
        os.system('sudo systemctl daemon-reload')
        os.system('sudo systemctl restart nginx')

    def start(self) -> None:
        os.system(f'sudo systemctl enable {self.name}')
        os.system(f'sudo systemctl start {self.name}')
        os.system(f'sudo systemctl restart {self.name}')
        os.system(f'sudo cp {self.sites_available_path}/{self.name} {self.sites_enabled_path}/{self.name}')
        os.system('sudo systemctl daemon-reload')
        os.system('sudo systemctl restart nginx')

    def make(self) -> None:
        self.__make_configs()
        self.__move_configs()
        os.system(f'{self.virtual_enviromnt_path}/bin/python -m pip install gunicorn --no-cache-dir')
        self.reload()

    def delete(self) -> None:
        os.system(f'sudo systemctl disable {self.name}')
        os.system(f'sudo systemctl stop {self.name}')
        os.system(f'sudo rm {self.sites_enabled_path}/{self.name}')
        os.system(f'sudo rm {self.sites_available_path}/{self.name}')
        os.system(f'sudo rm {self.gunicorn_services_path}/{self.name}.service')
        os.system(f'sudo rm {self.gunicorn_services_path}/{self.name}.socket')
        os.system('sudo systemctl daemon-reload')
        os.system('sudo systemctl restart nginx')
