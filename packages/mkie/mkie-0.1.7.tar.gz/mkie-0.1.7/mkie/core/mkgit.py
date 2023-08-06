import os
import re
import subprocess
from pathlib import Path

import click
from colorama import Back, Fore, Style

from .toolkit import Colored


class MkGit:
    _PATH_MAIN = subprocess.getoutput('git rev-parse --show-toplevel').strip()
    _PATH_MAIN_CONFIG = f'{_PATH_MAIN}/.git/config'
    _PATH_SUB_LS = subprocess.getoutput(
        "git config --file .gitmodules --get-regexp path | awk '{ print $2 }'"
    ).splitlines()
    _PATH_SUB = list()

    @classmethod
    def _get_submodules(cls):
        cls._PATH_SUB = [
            os.path.join(cls._PATH_MAIN, _) for _ in cls._PATH_SUB_LS
        ]

    @classmethod
    def _re_restores(cls, msg, restores):
        pattern = re.compile(r"(pathspec ')(.*)(')")
        for _ in pattern.findall(msg):
            restores.remove(_[1])

    @classmethod
    def add(cls, ignore):
        """ Auto add all files to git except submodules """
        cls._get_submodules()
        subprocess.run('git add .', shell=True)
        restores = ['git', 'restore', '--stage']

        if cls._PATH_SUB:
            restores.extend(cls._PATH_SUB_LS)

        if ignore:
            restores.extend(ignore)

        if len(restores) == 3:
            subprocess.run('git status', shell=True)
            return

        e = subprocess.run(restores, stderr=subprocess.PIPE, text=True).stderr
        if not e:
            subprocess.run('git status', shell=True)
            return

        cls._re_restores(msg=e, restores=restores)
        subprocess.run(restores)
        subprocess.run('git status', shell=True)
        print(e)

    @staticmethod
    def _re_words(info):
        """
        e.q.
            From https://xxx.net/xxx/xx
             - [
               group1: (deleted)
               group2: (]         (none)     -> origin/)
               group3: (feature/michael/xxxx)

             - [deleted] (none) -> origin/feature/xxxx/add-advanced-task
             - [deleted] (none) -> origin/patch/michael/rename-success
        """
        pattern = re.compile(r'\[(.+)(\].+-> origin/)(.+)')
        info = pattern.sub(
            rf'[{Fore.CYAN}\1{Fore.RESET}\2{Fore.CYAN}\3{Fore.RESET}', info)
        return info

    @staticmethod
    def _re_branchs(msg):
        """ """
        pattern_remote = re.compile(r'(remotes[/\w]*)')
        pattern_now = re.compile(r'(\*)( )(.*)')
        msg = pattern_remote.sub(rf'{Fore.RED}\1{Fore.RESET}', msg)
        msg = pattern_now.sub(
            rf'{Fore.YELLOW}\1{Fore.RESET}\2{Fore.GREEN}\3{Fore.RESET}', msg)
        return msg

    @classmethod
    def fetch(cls, show=True):
        """ sort out current branchs """
        prefix = Colored.get_color_prefix(color='YELLOW',
                                          color_prefix=Style.RESET_ALL +
                                          Fore.BLACK,
                                          prefix_msg='fetch')
        try:
            info = subprocess.getoutput('git fetch --prune')
        except Exception:
            print('No Git detect!')
            return

        msg = '--- Update ---' if info else 'Nothing To Update.'
        print(f'{prefix}{msg}')

        if not show and not info:
            return

        if 'deleted' in info:
            info = MkGit._re_words(info=info)
        print(info)

        # display branches
        click.echo('show branchs [y/N]: \n')
        show = click.getchar()
        if show == 'y':
            msg = cls._re_branchs(msg=subprocess.getoutput('git branch -a'))
            print(msg)

    @classmethod
    def _checkout(cls, branch):
        colored_repo = Colored.get_color_prefix(color='LIGHTBLACK_EX',
                                                color_prefix=Fore.WHITE)
        # """ check exist """
        branchs = set(subprocess.getoutput(
            "git for-each-ref "
            "--sort=-committerdate "
            "--format='%(refname:short)' | sed 's/^origin\///' ").splitlines())

        if branch in branchs:
            # """ checkout branch """
            info = subprocess.getoutput(f'git checkout {branch}')
            extra = ''
            try:
                if 'Already on' in info:
                    status = 'Already on '
                    color = Fore.CYAN

                elif 'Switched to' in info:
                    status = 'Switched to '
                    color = Fore.YELLOW

                else:
                    status = 'Error on '
                    color = Fore.RED
                    extra = f'\n{info}'

            except Exception:
                status = 'Except Error on '
                color = Fore.RED
                extra = f'\n{info}'

            print(
                f'{colored_repo}{status}{Colored.draw(color, branch)}{extra}')
            return

        # """ create new branch """
        draw_branch = Colored.draw(Fore.CYAN, branch)
        msg = Colored.draw(Fore.RED, 'Not Exist')
        print(f'\n< Branch: {draw_branch} > {msg}.')

        click.echo(f'Do you wanna create < Branch: {draw_branch} > [y/N]:')
        create = click.getchar()
        if create == 'y':
            info = subprocess.getoutput(f'git checkout -b {branch}')
            if 'Switched to' in info:
                info = f'Switched to {Colored.draw(Fore.YELLOW, branch)}'
            print(f'{colored_repo}{info}')

    @classmethod
    def _current_branch(cls):
        colored_repo = Colored.get_color_prefix(color='LIGHTBLACK_EX',
                                                color_prefix=Fore.WHITE)
        output = None
        try:
            output = str(
                subprocess.check_output(['git', 'branch'],
                                        cwd=os.getcwd(),
                                        universal_newlines=True))
            branch = [a for a in output.split('\n') if a.find('*') >= 0][0]
            current_branch = branch[branch.find('*') + 2:]
            status = f'Stay on {Colored.draw(Fore.GREEN, current_branch)}'

        except Exception:
            status = f'Error on {Colored.draw(Fore.RED, "info")}\n{output}'

        print(f'{colored_repo}{status}')

    @classmethod
    def swap(cls, branch_name, ignore=list(), level='all'):
        """s branch_name
        swap current branch to target branch

        ignore: Ignore specific submodule.
        """
        if level == 'all' or level == '1':
            cls._checkout(branch=branch_name)

        if level == 'all' or level == '2':
            cls._get_submodules()
            if not cls._PATH_SUB:
                return
            for path in cls._PATH_SUB:
                sub_name = path.split('/')[-1]
                if sub_name in ignore:
                    cls._current_branch()
                    continue
                try:
                    os.chdir(path)
                except Exception:
                    continue
                cls._checkout(branch=branch_name)

    @classmethod
    def _check_submodule_files(cls):
        has_files = None
        for path in cls._PATH_SUB:
            try:
                os.chdir(path)
                has_files = False if not subprocess.getoutput('ls') else True
            except Exception:
                return
        return has_files

    @classmethod
    def _init(cls, init=False):
        if not init:
            has_git = Path(f'{cls._PATH_MAIN}/.git').exists()
            has_config = Path(cls._PATH_MAIN_CONFIG).exists()

            if not has_config and not has_git:
                print('No Git Config Found!')
                return
            cls._get_submodules()
            if not cls._PATH_SUB:
                return

            # first init check submodule
            has_files = cls._check_submodule_files()
            if has_files:
                return

        color_prefix = Colored.get_color_prefix(color='MAGENTA',
                                                color_prefix=Fore.WHITE,
                                                prefix_msg='init')
        print(f'{color_prefix}Git Submodeles')
        subprocess.run('git submodule update --init --recursive', shell=True)
        _ = Colored.draw(color=Fore.MAGENTA, msg='---')
        print(f'{_} Finished. {_} ')

    @staticmethod
    def _re_pull_words(replacement, info, color):
        pattern = re.compile(rf'([{replacement}]+)([\n-)])')
        return pattern.sub(rf'{color}\1{Fore.RESET}\2', info)

    @classmethod
    def _git_pull(cls):
        info = subprocess.getoutput('git pull')
        info = cls._re_pull_words(replacement='-', info=info, color=Fore.RED)
        info = cls._re_pull_words(replacement='+', info=info, color=Fore.GREEN)
        print(f'{info}')

    @classmethod
    def pull(cls, init):
        """ pull all file from Git repo """
        cls._init(init=init)

        os.chdir(cls._PATH_MAIN)
        cls.fetch(show=False)

        color_prefix = Style.RESET_ALL + Fore.BLACK
        bottom_prefix = Fore.WHITE + Style.BRIGHT
        prefix = Colored.get_color_prefix(color='CYAN',
                                          color_prefix=color_prefix,
                                          prefix_msg='Main Module',
                                          bottom=True,
                                          bottom_color='LIGHTBLUE_EX',
                                          bottom_prefix=bottom_prefix,
                                          bottom_msg=Path.cwd().name)
        print(prefix)
        cls._git_pull()

        if not cls._PATH_SUB:
            return
        for path in cls._PATH_SUB:
            try:
                os.chdir(path)
            except Exception:
                continue
            prefix = Colored.get_color_prefix(color='CYAN',
                                              color_prefix=color_prefix,
                                              prefix_msg=' SubModule ',
                                              bottom=True,
                                              bottom_color='LIGHTBLUE_EX',
                                              bottom_prefix=bottom_prefix,
                                              bottom_msg=Path.cwd().name)
            print(prefix)
            cls._git_pull()
