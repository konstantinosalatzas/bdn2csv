"""Convert every BDN export XML file in a folder."""

from bdn2csv.convert import convert
import os

def batch(folder_path: str):
    for file in os.scandir(folder_path):
        if file.is_file():
            if file.path.split(".")[1] == "xml":
                try: # only BDN export XML files are valid to be converted
                    convert(file.path, file.path.replace(".xml", ".csv"))
                except Exception as error:
                    print(error)
