from typing import Any, Self, List

import os

from pathlib import Path

import configparser

from text import Painter


CWD = os.path.dirname(__file__)
paint = Painter()


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
        if 'sites/' not in name:
            name = 'sites/' + name
        if '.ini' not in name:
            name += '.ini'
        config_path = os.path.join(CWD, name)

        if not os.path.exists(config_path):
            raise AttributeError(f'No such site with config "{name}"!')

        config.read(config_path)

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

        self.nginx_enabled_config_path = Path(self.sites_enabled_path) / Path(self.name)
        self.nginx_available_config_path = Path(self.sites_available_path) / Path(self.name)
        self.systemd_service_config_path = Path(self.gunicorn_services_path) / Path(self.name + '.service')
        self.systemd_socket_config_path = Path(self.gunicorn_services_path) / Path(self.name + '.socket')

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
        os.system(f'sudo cp {Path(CWD) / Path(self.name + ".tmp")} {self.nginx_enabled_config_path}')
        os.system(f'sudo mv {Path(CWD) / Path(self.name + ".tmp")} {self.nginx_available_config_path}')
        os.system(f'sudo mv {Path(CWD) / Path(self.name + ".service.tmp")} {self.systemd_service_config_path}')
        os.system(f'sudo mv {Path(CWD) / Path(self.name + ".socket.tmp")} {self.systemd_socket_config_path}')

    def reload(self) -> None:
        os.system(f'sudo systemctl restart {self.name}.socket')
        os.system(f'sudo systemctl restart {self.name}.service')
        os.system('sudo systemctl daemon-reload')
        os.system('sudo systemctl restart nginx')

    def stop(self) -> None:
        os.system(f'sudo systemctl disable {self.name}.socket')
        os.system(f'sudo systemctl disable {self.name}.service')
        os.system(f'sudo systemctl stop {self.name}.socket')
        os.system(f'sudo systemctl stop {self.name}.service')
        os.system(f'sudo rm {self.nginx_enabled_config_path}')
        os.system('sudo systemctl daemon-reload')
        os.system('sudo systemctl restart nginx')

    def start(self) -> None:
        os.system(f'sudo systemctl enable {self.name}.socket')
        os.system(f'sudo systemctl enable {self.name}.service')
        os.system(f'sudo systemctl start {self.name}.socket')
        os.system(f'sudo systemctl start {self.name}.service')
        os.system(f'sudo cp {self.nginx_available_config_path} {self.nginx_enabled_config_path}')
        os.system('sudo systemctl daemon-reload')
        os.system('sudo systemctl restart nginx')

    def make(self) -> None:
        self.__make_configs()
        self.__move_configs()
        os.system(f'{Path(self.virtual_enviromnt_path)}/bin/python -m pip install gunicorn --no-cache-dir')
        self.reload()

    def delete(self) -> None:
        os.system(f'sudo systemctl disable {self.name}.socket')
        os.system(f'sudo systemctl disable {self.name}.service')
        os.system(f'sudo systemctl stop {self.name}.socket')
        os.system(f'sudo systemctl stop {self.name}.service')
        os.system(f'sudo rm {self.nginx_enabled_config_path}')
        os.system(f'sudo rm {self.nginx_available_config_path}')
        os.system(f'sudo rm {self.systemd_service_config_path}')
        os.system(f'sudo rm {self.systemd_socket_config_path}')
        os.system('sudo systemctl daemon-reload')
        os.system('sudo systemctl restart nginx')

    def service_is_active(self) -> bool:
        return int(os.system(f'systemctl is-active --quiet {self.name}.service')) == 0

    def socket_is_active(self) -> bool:
        return int(os.system(f'systemctl is-active --quiet {self.name}.socket')) == 0

    def __have_nginx_config_available(self) -> bool:
        return self.nginx_available_config_path.exists()

    def __have_nginx_config_enabled(self) -> bool:
        return self.nginx_enabled_config_path.exists()

    def __have_gunicorn_service(self) -> bool:
        return self.systemd_service_config_path.exists()

    def __have_gunicorn_socket(self) -> bool:
        return self.systemd_socket_config_path.exists()

    def status(self) -> dict:
        nginx_config_enabled_exists = self.__have_nginx_config_enabled()
        nginx_config_available_exists = self.__have_nginx_config_available()

        systemd_service_config_exists = self.__have_gunicorn_service()
        systemd_socket_config_exists = self.__have_gunicorn_socket()

        service_status = self.service_is_active()
        socket_status = self.socket_is_active()

        return {
            'nginx': {
                'enabled': {
                    'exists': nginx_config_enabled_exists,
                    'active': 'none'
                },
                'available': {
                    'exists': nginx_config_available_exists,
                    'active': 'none'
                }
            },
            'systemd': {
                'service': {
                    'exists': systemd_service_config_exists,
                    'active': service_status
                },
                'socket': {
                    'exists': systemd_socket_config_exists,
                    'active': socket_status
                }
            }
        }

    def print_status(self) -> None:
        data = self.status()

        service_status = paint('active', paint.GREEN) if data['systemd']['service']['active'] else paint('inactive', paint.RED)
        socket_status = paint('active', paint.GREEN) if data['systemd']['socket']['active'] else paint('inactive', paint.RED)

        nginx_enabled_config_status = paint(data['nginx']['enabled']['active'], paint.YELLOW)
        nginx_available_config_status = paint(data['nginx']['available']['active'], paint.YELLOW)

        service_config_exists = paint('[+]', paint.GREEN) if data['systemd']['service']['exists'] else paint('[-]', paint.RED)
        socket_config_exists = paint('[+]', paint.GREEN) if data['systemd']['socket']['exists'] else paint('[-]', paint.RED)

        service_config_path = self.systemd_service_config_path if data['systemd']['service']['exists'] else paint(self.systemd_service_config_path.__str__(), paint.GREY)
        socket_config_path = self.systemd_socket_config_path if data['systemd']['socket']['exists'] else paint(self.systemd_socket_config_path.__str__(), paint.GREY)

        nginx_enabled_config_exists_status = paint("[+]", paint.GREEN) if data['nginx']['enabled']['exists'] else paint("[-]", paint.RED)
        nginx_available_config_exists_status = paint("[+]", paint.GREEN) if data['nginx']['available']['exists'] else paint("[-]", paint.RED)

        nginx_enabled_config_path = self.nginx_enabled_config_path if data['nginx']['enabled']['exists'] else paint(self.nginx_enabled_config_path.__str__(), paint.GREY)
        nginx_available_config_path = self.nginx_available_config_path if data['nginx']['available']['exists'] else paint(self.nginx_available_config_path.__str__(), paint.GREY)

        daemon = paint(self.daemon, paint.GREEN)\
        if all((data['systemd']['service']['active'], data['systemd']['socket']['active']))\
        else paint(self.daemon, paint.GREY)

        print(f'{self.name}[{paint("daemon", paint.GREEN)}: {daemon}]:')

        print(f' {nginx_enabled_config_exists_status} ({nginx_enabled_config_status}) Nginx config in sites-enabled - {nginx_enabled_config_path}')
        print(f' {nginx_available_config_exists_status} ({nginx_available_config_status}) Nginx config in sites-available - {nginx_available_config_path}')
        print(f' {service_config_exists} ({service_status}) Systemd service config in system - {service_config_path}')
        print(f' {socket_config_exists} ({socket_status}) Systemd socket config in system - {socket_config_path}')

    @classmethod
    def list(cls) -> None:
        for name in os.listdir(os.path.join(CWD, 'sites')):
            if '.ini' in name:
                site = cls(name)
                site.print_status()
                print()

    @classmethod
    def get_all_sites(cls) -> List[Self]:
        return [
            cls(name)
            for name in os.listdir(os.path.join(CWD, 'sites'))
            if '.ini' in name
        ]

    @classmethod
    def try_get_site_by_cwd(cls) -> Self | None:
        workdir = os.getcwd()
        for site in cls.get_all_sites():
            if site.workdir == workdir:
                return site
        return None

