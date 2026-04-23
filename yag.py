import argparse
import os
from pydoc import text
import shutil
import hashlib


# yag init function. create requared files and path
def init(args):
    if os.path.exists(".yag/refs/heads"):
        shutil.rmtree(".yag/refs/heads")
    if os.path.exists(".yag/objects"):
        shutil.rmtree(".yag/objects")
    os.makedirs(".yag/refs/heads")
    os.mkdir(".yag/objects")
    with open(".yag/HEAD", "w") as file:
        file.write("ref: refs/heads/main")


# save utils
def getIgnoreList():
    if os.path.exists(".yagignore"):
        with open(".yagignore", "r", encoding="utf-8") as file:
            lines = file.read().splitlines()
        return lines
        
def getWalkList():
    rezult = []
    exludeDirs = {".yag", ".yagignore"}
    for root, dirs, files in os.walk(".", topdown=True):
        dirs[:] = [dir for dir in dirs if dir not in exludeDirs]
        for file in files:
            rezult.append(os.path.join(root, file)[2:])
    return rezult
    
def createBlob(path):
    # create sha-1
    with open(path, "rb") as file:
        data = file.read()
        dataSize = len(data)
        blobStr = f"blob {dataSize}\0".encode("utf-8") + data
        shaHash = hashlib.sha1(blobStr).hexdigest()
        # check if exist
        shaHashDir = shaHash[:2]
        shaHashFileName = shaHash[2:]
        # TODO: get walklist .yag/objects/
        for fileName in getWalkList(".yag/objects/"):
        
        
        
        
        
    
    
# yag add&commit in 1 function
def save(args):
    pass

def createParser():
    parser = argparse.ArgumentParser(prog="yag")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    
    parserInit = subparsers.add_parser("init", help="Create an empty Yag repository or reinitialize an existing one")

    # save ? pass for 17 april
    parserSave = subparsers.add_parser("save", help="Add file contents to the index and record changes")
    
    return parser


def main():
    parser = createParser()
    args = parser.parse_args()
    
    if args.command == "init":
        init(args)

if __name__ == "__main__":
    main()
