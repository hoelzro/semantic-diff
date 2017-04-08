import argparse
import ast

import semantic_diff
from semantic_diff.debug import dump_ast

def read_file(filename):
    with open(filename, 'r') as fp:
        return fp.read()

options = argparse.ArgumentParser()
options.add_argument('targets', type=str, metavar='files', nargs='+', help='Files to be diffed')
options.add_argument('--dump', dest='dump', action='store_const',
                     const=True, default=False, help='dump the AST for the given file')

args = options.parse_args()
if args.dump:
    dump_ast(ast.parse(read_file(args.targets[0]), filename=args.targets[0]))
else:
    print semantic_diff.diff(read_file(args.targets[0]), read_file(args.targets[1]))
