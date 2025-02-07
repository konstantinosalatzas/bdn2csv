import pandas as pd
import json

def path2id(json_path: str):
    with open(json_path, 'r') as f:
        response = json.load(f)
    print(response)
    return

path2id("/workspaces/bdn2csv/data/Response.json")
