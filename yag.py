import argparse
import os
from pydoc import text
import shutil
import hashlib
import json
from datetime import datetime
from statistics import harmonic_mean

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


# ========== #
# save utils #
# ========== #
def getIgnoreList():
    if os.path.exists(".yagignore"):
        with open(".yagignore", "r", encoding="utf-8") as file:
            lines = file.read().splitlines()
        return lines
    else:
        return []
        
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

        if os.path.isdir(".yag/objects/" + shaHashDir):
            pass
        else:
            os.makedirs(".yag/objects/" + shaHashDir)
            
        if os.path.exists(".yag/objects/" + shaHashDir + "/" + shaHashFileName):
            pass
        else:
            with open(".yag/objects/" + shaHashDir + "/" + shaHashFileName, 'wb') as file:
                file.write(blobStr)
    
    return shaHash    


def createTree(dirPath, ignoreList):
    entries = {}
    exludeDirs = {".yag", ".yagignore"}
    for name in os.listdir(dirPath):
        if name not in ignoreList and name not in exludeDirs:
            fullPath = os.path.join(dirPath, name)
            if os.path.isfile(fullPath):
                blobHash = createBlob(fullPath)
                entries[name] = {"type": "blob", "hash": blobHash}
            if os.path.isdir(fullPath):
                treeHash = createTree(fullPath, ignoreList)
                entries[name] = {"type": "tree", "hash": treeHash}
    
    jsonStr = json.dumps(entries)
    jsonBytes = jsonStr.encode("utf-8")
    jsonBytesSize = len(jsonBytes)
    treeData = f"tree {jsonBytesSize}\0".encode("utf-8") + jsonBytes
    treeDataHash = hashlib.sha1(treeData).hexdigest()
    
    shaHashDir = treeDataHash[:2]
    shaHashFileName = treeDataHash[2:]

    if os.path.isdir(".yag/objects/" + shaHashDir):
        pass
    else:
        os.makedirs(".yag/objects/" + shaHashDir)
        
    if os.path.exists(".yag/objects/" + shaHashDir + "/" + shaHashFileName):
        pass
    else:
        with open(".yag/objects/" + shaHashDir + "/" + shaHashFileName, 'wb') as file:
            file.write(treeData)
        
    return treeDataHash
    
    
    
def createCommit(message, treeHash):
    if os.path.isfile(".yag/refs/heads/main"):
        with open(".yag/refs/heads/main", "r") as file:
            parentHash = file.read()
    else:
        parentHash = None
    
    commit = {
        "message":      message,
        "timestamp":    datetime.now().isoformat(),
        "tree":         treeHash,
        "parent":       parentHash
    }
    
    jsonStr = json.dumps(commit)
    jsonBytes = jsonStr.encode("utf-8")
    jsonBytesSize = len(jsonBytes)
    commitData = f"commit {jsonBytesSize}\0".encode("utf-8") + jsonBytes
    commitDataHash = hashlib.sha1(commitData).hexdigest()
    
    shaHashDir = commitDataHash[:2]
    shaHashFileName = commitDataHash[2:]
    
    if os.path.isdir(".yag/objects/" + shaHashDir):
        pass
    else:
        os.makedirs(".yag/objects/" + shaHashDir)
        
    if os.path.exists(".yag/objects/" + shaHashDir + "/" + shaHashFileName):
        pass
    else:
        with open(".yag/objects/" + shaHashDir + "/" + shaHashFileName, 'wb') as file:
            file.write(commitData)
    
    with open(".yag/refs/heads/main", "w") as file:
        file.write(commitDataHash)
    return commitDataHash    

# ============== #
# checkout utils #
# ============== # 

def findCommit(shortID):
    match = []
    for folder in os.listdir(".yag/objects/"):
        for file in os.listdir(".yag/objects/" + folder):
            name = folder + file
    
            if name.startswith(shortID):
                match.append(name)
    
    if len(match) == 0:
        print("Commit not found")
    elif len(match) > 1:
        print("Ambiguous ID, please clarify")
    elif len(match) == 1:
        return match[0]
    

def readObject(hash):
    hashDir = hash[:2]
    hashFileName = hash[2:]
    fullHashPath = ".yag/objects/" + hashDir + "/" + hashFileName
    
    with open(fullHashPath, "rb") as file:
        data = file.read()
        zeroPos = data.find(b"\0")
        header = data[:zeroPos]
        inner = data[zeroPos + 1:]
        
        headerDecode = header.decode("utf-8").split()
        if headerDecode[0] == "blob":
            return headerDecode[0], inner
        if headerDecode[0] == "tree" or headerDecode[0] == "commit":
            innerDecode = inner.decode("utf-8")
            jsonStr = json.loads(innerDecode)
            return headerDecode[0], jsonStr
            
                
            
    

    
def save(args):
    if os.path.isdir(".yag"):
        ignoreList = getIgnoreList()
        treeHash = createTree(".", ignoreList)
        createCommit(args.message, treeHash)


# TODO: create checkout (last ride)
def checkout(args):
    pass

def createParser():
    parser = argparse.ArgumentParser(prog="yag")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    parserInit = subparsers.add_parser("init", help="Create an empty Yag repository or reinitialize an existing one")

    parserSave = subparsers.add_parser("save", help="Save current state")
    parserSave.add_argument("message", help="Commit message")
    
    return parser



def main():
    parser = createParser()
    args = parser.parse_args()
    
    if args.command == "init":
        init(args)
    if args.command == "save":
        save(args)



if __name__ == "__main__":
    main()
