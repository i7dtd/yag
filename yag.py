import argparse
import os






def init(args):
    os.makedirs('.yag/refs/heads')
    os.mkdir('.yag/objects')
    with open(".yag/HEAD") as file:
        file.write("ref: refs/heads/main")


def createParser():
    parser = argparse.ArgumentParser(prog='yag')
    subparsers = argparse.ArgumentParser(dest='command', requared=True)
    
    # init ?
    parserInit = subparsers.add_subparser('init', help='Create an empty Yag repository or reinitialize an existing one')

    # add ? pass for 10 april
    parserAdd = subparsers.add_subparsers('add', help='Add file contents to the index')

    return parser


def main():
    parser = createParser()
    args = parser.parse_args()

if __name__ == "__main__":
    main()
