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
        print(item)

path2id("/workspaces/bdn2csv/data/Response.json")
