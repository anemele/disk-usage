import asyncio
import os
from typing import AsyncGenerator

from rich import print as rich_print

T_ITEM = tuple[int, int, int]
T_OS_WALKER = tuple[str, list[str], list[str]]
T_AG = AsyncGenerator[T_ITEM, None]


async def count_root(root: T_OS_WALKER) -> T_ITEM:
    """return a tuple of
    (number of dirs, number of files, size of files)"""
    r, d, f = root
    pth = (os.path.join(r, i) for i in f)
    return len(d), len(f), sum(map(os.path.getsize, pth))


async def count(directory: str, recursive: bool) -> T_AG:
    walker = os.walk(directory)
    yield await count_root(next(walker))

    if recursive:
        try:
            for item in walker:
                yield await count_root(item)
        except KeyboardInterrupt:
            pass


async def pprint(count: T_AG):
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
