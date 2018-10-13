import sys

from ucomponents import invoke
import machine
import uos
from uio import FileIO


class FileSystem:
    def __init__(self, address):
        self.address = address

    def mount(self, readonly, mkfs):
        pass

    def umount(self):
        pass

    def getcwd(self):
        return '/'

    def ilistdir(self, dir):
        for name in invoke(self.address, 'list', dir):
            if invoke(self.address, 'isDirectory', dir + "/" + name):
                yield (name, 0x4000, 0, -1)
            else:
                yield (name, 0x8000, 0, 0)

    def stat(self, path):
        if not invoke(self.address, 'exists', path):
            raise OSError(1)

        return 0x4000 if invoke(self.address, 'isDirectory', path) else 0x8000, 0, 0, 0, 0, 0, 0, 0, 0, 0

    def open(self, file, mode):
        return FileIO(self.address, file, mode)


@machine.hook_stdin
def input_handler():
    return 0


@machine.hook_stdout
def print_handler(string):
    machine.debug(string)


def init():
    uos.mount(FileSystem(__path__), '/')
    sys.path.append('/lib')
    sys.path.append('/lib/micropython')

    contexts = []  # prevent from gc
    for filename in sorted(uos.listdir("/boot")):
        context = {'__name__': '__main__', '__path__': __path__}
        contexts.append(context)
        # noinspection PyUnresolvedReferences
        execfile("/boot/" + filename, context)

    from shell import spawn
    spawn("/bin/shell.py")


if __name__ == "__main__":
    init()
