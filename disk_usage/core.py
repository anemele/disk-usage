import asyncio
import os
from typing import AsyncGenerator

from rich import print as rich_print

T_ITEM = tuple[int, int, int]


def count_root(root: tuple[str, list[str], list[str]]) -> T_ITEM:
    """return a tuple of
    (number of dirs, number of files, size of files)"""
    r, d, f = root
    pth = (os.path.join(r, i) for i in f)
    return len(d), len(f), sum(map(os.path.getsize, pth))


async def count(directory: str, recursive: bool) -> AsyncGenerator[T_ITEM, None]:
    walker = os.walk(directory)
    yield count_root(next(walker))

    if recursive:
        try:
            for item in map(count_root, walker):
                yield item
        except KeyboardInterrupt:
            pass


async def pprint(count):
    nd, nf, ns = 0, 0, 0
    async for d, f, s in count:
        nd += d
        nf += f
        ns += s
        rich_print(f'  {nd} dir(s)  {nf} file(s)  {ns:,} bytes', end='\r')
    print()


async def manager(directory, recursive):
    await pprint(count(directory, recursive))


def run(directory, recursive):
    asyncio.run(manager(directory, recursive))
