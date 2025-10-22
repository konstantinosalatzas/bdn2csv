"""Convert every XML file in a folder path."""

from bdn2csv.convert import convert
import os

def batch(folder_path: str):
    for file in os.scandir(folder_path):
        if file.is_file():
            if file.path.split(".")[1] == "xml":
                convert(file.path, file.path.replace(".xml", ".csv"))

path = "data"
batch(path)
