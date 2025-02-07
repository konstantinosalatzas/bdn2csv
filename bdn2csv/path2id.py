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
        names.append(name)
        ids.append(id)
        parentIds.append(parentId)
        id2name[item['id']] = item['name']

    for item in response['items']:
        parentName = (id2name[item['parentId']] if "parentId" in item else "")
        parentNames.append(parentName)

    df = pd.DataFrame({"name": names, "id": ids, "parentId": parentIds, "parentNames": parentName})
    print(df.head())
    return df

path2id("/workspaces/bdn2csv/data/Response.json")
