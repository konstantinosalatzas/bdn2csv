import pandas as pd
import json

def path2id(json_path: str):
    with open(json_path, 'r') as f:
        response = json.load(f)

    for item in response['items']:
        print(item)

path2id("/workspaces/bdn2csv/data/Response.json")
