from cmd import Cmd
from functools import wraps
import itertools
import os
import sys


def add_to_history(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
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
    def do_ls(self, arg):
        files_list = sorted(
            os.listdir(os.getcwd()), key=lambda x: x.upper().replace("_", "")
        )
        print_list_files(files_list)

    @add_to_history
    def do_env(self, arg):
        for var in os.environ:
            print("{}={}".format(var, os.environ[var]))

    @add_to_history
    def do_history(self, arg):
        for num, (cmd, arg) in enumerate(self.history):
            print('{:>4}  {} {}'.format(num + 1, cmd.replace('do_', ''), arg))

    @add_to_history
    def do_cd(self, arg):
        if len(arg) == 0:
            os.chdir(self.home_dir)
            self.prompt = self._set_prompt(self.home_dir)

        try:
            path = os.path.abspath(os.path.expanduser(arg))
            os.chdir(path)
            self.prompt = self._set_prompt(path)
        except OSError as err:
            print('Error: ', err.strerror)

    @add_to_history
    def do_cat(self, arg):
        # print(arg.split(' '))
        try:
            if arg == '':
                line = sys.stdin.readline()
                while line:
                    print(line.strip())
                    line = sys.stdin.readline()
        except KeyboardInterrupt:
            sys.stdout.write('\n')

    def _set_prompt(self, path):
        return '{}> '.format(path.replace(self.home_dir, '~'))

    def do_exit(self, arg):
        return True

    def postloop(self):
        print()

    do_EOF = do_exit


if __name__ == '__main__':
    promt = CommandShell()
    promt.cmdloop('Starting interactive shell...')
