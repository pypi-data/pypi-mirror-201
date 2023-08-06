"""
    | ┏┓       ┏┓
    ┏━┛┻━━━━━━━┛┻━┓
    ┃      ☃      ┃
    ┃  ┳┛     ┗┳  ┃
    ┃      ┻      ┃
    ┗━┓         ┏━┛
    | ┗┳        ┗━┓
    |  ┃          ┣┓
    |  ┃          ┏┛
    |  ┗┓┓┏━━━━┳┓┏┛
    |   ┃┫┫    ┃┫┫
    |   ┗┻┛    ┗┻┛
    God Bless,Never Bug.
"""
import click
from click_help_colors import HelpColorsCommand, HelpColorsGroup
from importlib_metadata import version

import mkie
from mkie.core.mkdk import Mkdk
from mkie.core.mkgit import MkGit


class Mkie(click.MultiCommand):

    @click.group(
        cls=HelpColorsGroup,
        help_headers_color='yellow',
        help_options_color='green',
        context_settings=dict(help_option_names=['-h', '--help']),
    )
    @click.version_option(version=version('mkie'), prog_name='mkie')
    def cli():
        """
        \b
                      __   _
           ____ ___  / /__(_)__
          / __ `__ \/ //_/ / _ \\
         / / / / / / ,< / /  __/
        /_/ /_/ /_/_/|_/_/\___/

        A useful tool for control clis in terminal.
        """
        pass

    @cli.command()
    @click.option('-i', '--ignore', help='ignore files', multiple=True)
    def gitadd(ignore):
        """ Auto add all files to git and ignore submodules. """
        MkGit.add(ignore=ignore)

    @cli.command()
    def gitfetch():
        """ sort out current branchs. """
        MkGit.fetch()

    @cli.command()
    @click.option('-i',
                  '--ignore',
                  help='ignore submodules',
                  is_flag=False,
                  flag_value='general',
                  multiple=True)
    @click.argument('branch_name', required=True)
    def s(ignore, branch_name):
        """ Swap current branch to target branch. """
        MkGit.swap(ignore=ignore, branch_name=branch_name)

    @cli.command()
    @click.option('--init')
    def gitpull(init):
        """ pull latest update from repo """
        MkGit.pull(init)

    @cli.command()
    @click.option('-f',
                  '--format',
                  help='pretty print container cols,'
                  'default:".ID.Names.Ports.Image"')
    @click.option('--pattern', help='rg pattern word container name')
    def dps(format, pattern):
        """ list docker containers """
        Mkdk.ps(format=format, pattern=pattern)

    @cli.command()
    def dbu():
        """ build docker container """
        Mkdk.build()

    @cli.command()
    @click.argument('project', required=False)
    @click.option('--subpath')
    @click.option('--filepath', help='e.q. docker-compose.yml')
    @click.option('--follow', help='aviod daemon mode', is_flag=True)
    def dup(project, subpath, filepath, follow):
        """ start docker container """
        Mkdk.up(
            project=project,
            subpath=subpath,
            filepath=filepath,
            is_follow=follow,
        )

    @cli.command()
    @click.argument('project', required=False)
    @click.option('--subpath')
    @click.option('--filepath', help='e.q. docker-compose.yml')
    def dd(project, subpath, filepath):
        """ start docker container """
        Mkdk.down(
            project=project,
            subpath=subpath,
            filepath=filepath,
        )

    @cli.command()
    @click.argument('project', required=False)
    @click.option('--command', help='default: bash')
    @click.option('--list', help='list all containers', is_flag=True)
    def drun(project, command, list):
        """
        \b
        run docker container

        e.q.
            tree:
            - demo
                |-- demo_api
                |-- demo_dms_api

            pwd -> ~/demo/demo_api

            - mkie drun -> exec demo_api contaniner
            - mkie drun demo_dms_api -> exec demo_dms_api container
            - mkie drun --list -> list the current running container to select
        """
        Mkdk.run(
            project=project,
            command=command,
            is_list=list,
        )


if __name__ == '__main__':
    Mkie.cli()
