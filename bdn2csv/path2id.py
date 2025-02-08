import pandas as pd
import json

def path2id(json_path: str) -> pd.DataFrame:
    with open(json_path, 'r') as f:
        response = json.load(f) # GET /terms response JSON

    names = [] # term names
    ids = [] # term IDs
    parentIds = [] # term parent IDs
    id2name = {} # map term IDs to names
    for item in response['items']:
        name = item['name']
        id = item['id']
        parentId = (item['parentId'] if "parentId" in item else "")
        names.append(name)
        ids.append(id)
        parentIds.append(parentId)
        id2name[id] = name

    parentNames = [] # term parent names
    for item in response['items']:
        parentName = (id2name[item['parentId']] if "parentId" in item else "")
        parentNames.append(parentName)

    df = pd.DataFrame({"name": names, "id": ids, "parentId": parentIds, "parentName": parentNames})
    print(df.head()) #dev

    paths = [] # term paths
    for _, term in df.iterrows():
        pass

    return df

path2id("/workspaces/bdn2csv/data/Response.json") #dev
