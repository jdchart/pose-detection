import os
import json
from pathlib import Path

def makeDirsRecustive(pathList):
    for item in pathList:
        if os.path.isdir(item) == False:
            path = Path(item)
            path.mkdir(parents=True)

def getFileName(path):
    return os.path.splitext(os.path.basename(path))[0]

def writeJson(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def readJson(path):
    with open(path, 'r') as f:
        return json.load(f)
    
def sanitiseJson(path):
    output = {"items" : []}
    lines = []
    with open(path) as f:
        lines = f.readlines()
        for line in lines:
            output["items"].append(json.loads(line))
    writeJson(output, path)