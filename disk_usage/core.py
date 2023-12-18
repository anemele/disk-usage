import os
from typing import Iterable

from rich import print as rich_print


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
    print('\n', os.path.abspath(root), '\n')
    nd, nf, ns = 0, 0, 0
    for d, f, s in count:
        nd += d
        nf += f
        ns += s
        rich_print(f'  {nd} dir(s)  {nf} file(s)  {ns:,} bytes', end='\r')
    print()
