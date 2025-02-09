import pandas as pd
import json

def id2name(response):
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

    return df

def id2path(df):
    ids = df['id'].values.tolist()
    paths = [] # term paths

    for _, term in df.iterrows():
        path = term['name']
        parentId = term['parentId']
        parentName = term['parentName']
        while parentId != "": # O(max path length)
            path = parentName+"\\"+path # prepend parent name to term name to construct the term path
            parent = df[df['id'] == parentId].iloc[0] # the parent exists and is unique
            parentId = parent['parentId'] # update parent ID
            parentName = parent['parentName'] # update parent name
        paths.append(path)

    df = pd.DataFrame({"path": paths, "id": ids})
    print(df.head()) #dev

    return df

def path2id(json_path: str) -> pd.DataFrame:
    with open(json_path, 'r') as f:
        response = json.load(f) # GET /terms response JSON

    df = id2name(response)
    df = id2path(df)

    return df

path2id("/workspaces/bdn2csv/data/Response.json") #dev
