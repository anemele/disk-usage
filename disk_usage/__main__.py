""" Disk usage? I don't know."""
import argparse
import os

from .core import count, pprint

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
pprint(count(args_dir, args_r))
