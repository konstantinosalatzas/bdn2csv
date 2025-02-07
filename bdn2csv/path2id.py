import pandas as pd
import json

def path2id(json_path: str):
    with open(json_path, 'r') as f:
        response = json.load(f)

    names = []
    ids = []
    parentIds = []
    parentNames = []

    id2name = {}

    for item in response['items']:
        names.append(item['name'])
        ids.append(item['id'])
        parentIds.append(item['parentId'] if "parentId" in item else "")
        id2name[item['id']] = item['name']

    for item in response['items']:
        if "parentId" in item:
            parentNames.append(id2name[item['parentId']])
        else:
            parentNames.append("")
        pass

    return

path2id("/workspaces/bdn2csv/data/Response.json")
