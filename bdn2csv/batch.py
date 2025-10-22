"""Convert every XML file in a folder path."""

from bdn2csv.convert import convert
import os

def batch(folder_path: str):
    for file in os.scandir(folder_path):
        if file.is_file():
            if file.path.split(".")[1] == "xml":
                try: # not all XML files are valid to convert
                    convert(file.path, file.path.replace(".xml", ".csv"))
                except Exception as error:
                    print(error)

path = "data"
batch(path)
