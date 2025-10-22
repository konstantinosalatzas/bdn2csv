from bdn2csv.convert import convert
import os

def batch(folder_path: str):
    for file in os.scandir(folder_path):
        if file.is_file():
            print(file.path)
            convert(file.path, str(file.path).replace(".xml", ".csv"))

path = "data"
batch(path)
