import pandas as pd
import json

def path2id(json_path: str):
    with open(json_path, 'r') as f:
        response = json.load(f)

    names = []
    ids = []
    parentIds = []
    parentNames = []

    for item in response['items']:
        print(item['name'])
        names.append(item['name'])
        print(item['id'])
        ids.append(item['id'])
        if "parentId" in item:
            print(item['parentId'])
            parentIds.append(item['parentId'])
        else:
            parentIds.append("")

path2id("/workspaces/bdn2csv/data/Response.json")
