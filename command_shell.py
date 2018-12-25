from cmd import Cmd
from functools import wraps
import itertools
import os
import sys
import subprocess


def add_to_history(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if method.__name__ == 'default':
            method.__name__ = ''
        self.history.append((method.__name__, args[0]))
        return method(self, *args, **kwargs)
    return wrapper


def print_list_files(files_list, col_count=5):
    col, dangling = divmod(len(files_list), col_count)
    iterator = iter(files_list)
    columns = [take(col + (dangling > i), iterator) for i in range(col_count)]
    paddings = [max(map(len, col)) for col in columns if len(col) > 0]
    for row in itertools.zip_longest(*columns, fillvalue=''):
        print('  '.join(file.ljust(pad) for file, pad in zip(row, paddings)))


def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(itertools.islice(iterable, n))


class CommandShell(Cmd):

    def __init__(self):
        super().__init__()
        self.history = []
        self.home_dir = '/home/{}'.format(os.getlogin())
        self.prompt = '{}> '.format(os.getcwd().replace(self.home_dir, '~'))

    @add_to_history
    def do_ls(self, args):
        files_list = sorted(
            os.listdir(os.getcwd()), key=lambda x: x.upper().replace("_", "")
        )
        print_list_files(files_list)

    @add_to_history
    def do_env(self, args):
        for var in os.environ:
            print("{}={}".format(var, os.environ[var]))

    @add_to_history
    def do_history(self, args):
        for num, (cmd, arg) in enumerate(self.history):
            print('{:>4}  {}{}{}'.format(
                num + 1,
                cmd.replace('do_', ''),
                ' ' if cmd else '',
                arg
            ))

    @add_to_history
    def do_cd(self, args):
        if len(args) == 0:
            os.chdir(self.home_dir)
            self.prompt = self._set_prompt(self.home_dir)

        try:
            path = os.path.abspath(os.path.expanduser(args))
            os.chdir(path)
            self.prompt = self._set_prompt(path)
        except OSError as err:
            print('Error: ', err.strerror)

    @add_to_history
    def do_cat(self, args):
        if args == '':
            try:
                line = sys.stdin.readline()
                while line:
                    print(line.strip())
                    line = sys.stdin.readline()
            except KeyboardInterrupt:
                sys.stdout.write('\n')
        else:
            for arg in args.split(' '):
                try:
                    with open(arg, 'r') as fp:
                        for line in fp:
                            print(line.strip())
                except OSError as err:
                    print('Error: {}: {}'.format(err.filename, err.strerror))

    @add_to_history
    def do_grep(self, args):
        pattern, *files = args.split(' ')

        for file in files:
            try:
                with open(file, 'r') as fp:
                    for line in fp:
                        if line.find(pattern) is not -1:
                            print(
                                '{}'.format(
                                    ':'.join((file, line.rstrip()))
                                    if len(files) > 1 else line.rstrip()
                                )
                            )
            except OSError as err:
                print('Error: {}: {}'.format(err.filename, err.strerror))

    @add_to_history
    def do_echo(self, args):
        if args.startswith('$'):
            print(os.environ.get(args[1:], ''))
        else:
            print(args)

    @add_to_history
    def default(self, args):
        command = subprocess.run(args, shell=True)
        output = command.stdout

        if output is None:
            return

        print(output.decode('utf-8').rstrip())

    def _set_prompt(self, path):
        return '{}> '.format(path.replace(self.home_dir, '~'))

    def do_exit(self, args):
        return True

    def postloop(self):
        print()

    do_EOF = do_exit


if __name__ == '__main__':
    promt = CommandShell()
    promt.cmdloop('Starting interactive shell...')
