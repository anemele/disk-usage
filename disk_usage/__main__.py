""" Disk usage? I don't know."""
import argparse
import os
import time

from .core import run

parser = argparse.ArgumentParser(prog=__package__, description=__doc__)
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

print('\n', os.path.abspath(args_dir), '\n')
begin = time.perf_counter()
try:
    run(args_dir, args_r)
except KeyboardInterrupt:
    pass
finally:
    print(f' use time: {time.perf_counter()-begin:.3f}s')
