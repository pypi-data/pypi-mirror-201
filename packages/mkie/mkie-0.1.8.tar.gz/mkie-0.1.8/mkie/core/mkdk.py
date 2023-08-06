import os
import subprocess
from pathlib import Path

import click
from colorama import Fore, Style

from .toolkit import Colored


class Mkdk:

    _DEFAULT_PS_FORMAT = 'table {{.ID}}\t{{.Names}}\t{{.Ports}}\t{{.Image}}'
    _PS_FORMAT = os.environ.get('MKIE_PS_FORMAT', _DEFAULT_PS_FORMAT)

    # fetch fila path with sub path or not / e.q. str()-> /Users/me/project : e.q. {PRIFIX} -> /Users/me/{PREIFX}/project
    _SUB_PATH = os.environ.get('MKIE_SUB_PATH', str())

    _DEFAULT_FILE_PATH = 'docker-compose.yml'
    _DEFAULT_EXEC_COMMAND = 'bash'

    @classmethod
    def ps(cls, format, pattern):
        format = format or cls._PS_FORMAT
        _cmd = ['docker', 'ps', '--format', format]

        if pattern:
            _cmd.extend(['--filter', f'name={pattern}'])

        subprocess.run(_cmd)

    @classmethod
    def build(cls):
        subprocess.run(['docker-compose', 'build'])

    @classmethod
    def _parse_project_name(cls, project_name):
        conj = '_'
        if not isinstance(project_name, str):
            raise ValueError(
                f'invalid <project:{project_name}> in fetching project')
        tmp = project_name.split(conj)
        data = tmp[:-1] if len(tmp) > 1 else tmp
        return conj.join(data)

    @classmethod
    def _parse_subpath(cls, root_path, subpath, project_name):
        results = list()
        sub_path = subpath or cls._SUB_PATH

        # validate subpath
        if '~' in sub_path or root_path.name in sub_path:
            click.echo(
                f'Detect invalid <Path:{root_path}> from `MKIE_SUB_PATH` or `--subpath`'
            )
            exit('Program has been exit')

        # parse subpath
        if not sub_path:
            return results
        project_prefix = cls._parse_project_name(project_name=project_name)
        for name in sub_path.split('/'):
            tmp = name.replace(cls._SUB_PATH, project_prefix)
            results.append(tmp)
        return results

    @classmethod
    def _locate_docker_filepath(cls, project_name, subpath, filepath):
        root_path = Path.home()
        sub_path = cls._parse_subpath(
            root_path=root_path,
            subpath=subpath,
            project_name=project_name,
        )
        compose_path = filepath or cls._DEFAULT_FILE_PATH
        return root_path.joinpath(*sub_path, project_name, compose_path)

    @classmethod
    def up(cls, project, subpath, filepath, is_follow):
        """
        subpath
            - demo
            - demo_try

        project
            - demo
            - demo_api
            - demo_try_api
        """
        _cmd = ['docker-compose']
        project_name = project or Path.cwd().name

        if project:
            _path = cls._locate_docker_filepath(
                project_name=project_name,
                subpath=subpath,
                filepath=filepath,
            )
            _cmd.extend(['-f', str(_path)])

        _cmd.append('up')
        if is_follow:
            _cmd.append('-d')

        # color log
        color_prefix = Style.RESET_ALL + Fore.BLACK
        prefix = Colored.get_color_prefix(color='LIGHTYELLOW_EX',
                                          color_prefix=color_prefix,
                                          prefix_msg='🐳 Docker ⬆ ',
                                          bottom=True,
                                          bottom_color='LIGHTBLUE_EX',
                                          bottom_prefix=Fore.BLACK,
                                          bottom_msg=project_name)
        print(prefix)
        subprocess.run(_cmd)

    @classmethod
    def down(cls, project, subpath, filepath):
        _cmd = ['docker-compose']
        project_name = project or Path.cwd().name

        if project:
            _path = cls._locate_docker_filepath(
                project_name=project_name,
                subpath=subpath,
                filepath=filepath,
            )
            _cmd.extend(['-f', str(_path)])

        color_prefix = Style.RESET_ALL + Fore.BLACK
        prefix = Colored.get_color_prefix(color='LIGHTGREEN_EX',
                                          color_prefix=color_prefix,
                                          prefix_msg='🐳 Docker ⬇ ',
                                          bottom=True,
                                          bottom_color='LIGHTBLUE_EX',
                                          bottom_prefix=Fore.BLACK,
                                          bottom_msg=project_name)
        print(prefix)
        _cmd.extend(['down'])
        subprocess.run(_cmd)

    @classmethod
    def _parse_containers(cls, info):
        tmp = info.split('\n')
        result = dict()
        for index, data in enumerate(tmp):
            _, container = data.split(':')
            result.update({index: container})
        return result

    @classmethod
    def _select_container_list(cls, cons):
        for index, name in cons.items():
            print(f'[{index:2}] | * {name}')

        msg = Colored.draw(
            color=Fore.YELLOW,
            msg='Please Choice Above Num for Exec Container',
        )
        value = click.prompt(msg, type=int)
        return cons[value]

    @classmethod
    def run(cls, project, command, is_list):
        if not is_list:
            project_name = project or Path.cwd().name
        else:
            info = subprocess.getoutput(
                'docker ps --format {{.ID}}:{{.Names}}')
            cons = cls._parse_containers(info=info)
            project_name = cls._select_container_list(cons=cons)
        command = command or cls._DEFAULT_EXEC_COMMAND
        _cmd = ['docker', 'exec', '-it', project_name, command]
        os.system('clear')
        color_prefix = Style.RESET_ALL + Fore.BLACK
        prefix = Colored.get_color_prefix(color='LIGHTCYAN_EX',
                                          color_prefix=color_prefix,
                                          prefix_msg='🐳 Docker exec',
                                          bottom=True,
                                          bottom_color='LIGHTBLUE_EX',
                                          bottom_prefix=Fore.BLACK,
                                          bottom_msg=project_name)
        print(prefix)
        subprocess.run(_cmd)
