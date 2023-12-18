""" Disk usage? I don't know."""
import argparse
import os
from typing import Iterable

from rich import print


def count_root(root: tuple[str, list[str], list[str]]) -> tuple[int, int, int]:
    """return a tuple of
    (number of dirs, number of files, size of files)"""
    r, d, f = root
    pth = (os.path.join(r, i) for i in f)
    return len(d), len(f), sum(map(os.path.getsize, pth))


def count(directory: str, recursive: bool) -> Iterable[tuple[int, int, int]]:
    walker = os.walk(directory)
    yield count_root(next(walker))

    if recursive:
        try:
            for item in map(count_root, walker):
                yield item
        except KeyboardInterrupt:
            pass


def pprint(root: str, count: Iterable[tuple[int, int, int]]):
    print(' ', os.path.abspath(root), '\n')
    nd, nf, ns = 0, 0, 0
    for d, f, s in count:
        nd += d
        nf += f
        ns += s
        print(f'  {nd} dir(s)  {nf} file(s)  {ns:,} bytes', end='\r')
    print()


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    'dir',
    type=str,
    nargs='?',
    default='.',
    help='default: current directory',
)
parser.add_argument(
    '-r',
    '--recursive',
    action='store_true',
    help='recursive',
)


args = parser.parse_args()
# print(args)
# return
args_dir: str = args.dir
args_r: bool = args.recursive

if not os.path.isdir(args_dir):
    print(f'not a dir: {args_dir}')
    exit(1)

pprint(args_dir, count(args_dir, args_r))
