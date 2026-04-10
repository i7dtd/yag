import argparse
import os
import shutil



def init(args):
    if os.path.exists('.yag/refs/heads'):
        shutil.rmtree('.yag/refs/heads')
    if os.path.exists('.yag/objects'):
        shutil.rmtree('.yag/objects')
    os.makedirs('.yag/refs/heads')
    os.mkdir('.yag/objects')
    with open(".yag/HEAD", 'w') as file:
        file.write("ref: refs/heads/main")


def add(args):
    pass

def createParser():
    parser = argparse.ArgumentParser(prog='yag')
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    
    parserInit = subparsers.add_parser('init', help='Create an empty Yag repository or reinitialize an existing one')

    # add ? pass for 10 april
    parserAdd = subparsers.add_parser('add', help='Add file contents to the index')
    parserAdd.add_argument('file', help='Add file')

    return parser


def main():
    parser = createParser()
    args = parser.parse_args()
    
    if args.command == 'init':
        init(args)

if __name__ == "__main__":
    main()
