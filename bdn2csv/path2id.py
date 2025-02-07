import pandas as pd
import json

def path2id(json_path: str):
    with open(json_path, 'r') as f:
        response = json.load(f)
    names = []
    ids = []
    parentIds = []
    id2name = {}
    parentNames = []
    for item in response['items']:
        name = item['name']
        id = item['id']
        parentId = (item['parentId'] if "parentId" in item else "")
        print(name, id, parentId)
        names.append(name)
        ids.append(id)
        parentIds.append(parentId)
        id2name[item['id']] = item['name']
    for item in response['items']:
        if "parentId" in item:
            parentNames.append(id2name[item['parentId']])
        else:
            parentNames.append("")
    return

path2id("/workspaces/bdn2csv/data/Response.json")
