import pandas as pd
import json

def path2id(json_path: str) -> pd.DataFrame:
    with open(json_path, 'r') as f:
        response = json.load(f) # GET /terms response JSON

    names = [] # term names
    ids = [] # term IDS
    parentIds = [] # term parent IDs
    id2name = {} # maps term IDs to names
    parentNames = [] # term parent names

    for item in response['items']:
        name = item['name']
        id = item['id']
        parentId = (item['parentId'] if "parentId" in item else "")

        id2name[id] = name

        names.append(name)
        ids.append(id)
        parentIds.append(parentId)

    for item in response['items']:
        parentName = (id2name[item['parentId']] if "parentId" in item else "")
        parentNames.append(parentName)

    df = pd.DataFrame({"name": names, "id": ids, "parentId": parentIds, "parentName": parentNames})
    print(df.head())
    return df

path2id("/workspaces/bdn2csv/data/Response.json")
