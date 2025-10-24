"""Convert every BDN export XML file in a folder."""

from bdn2csv.convert import convert
import os

def batch(in_folder_path: str, out_folder_path: str):
    for file in os.scandir(in_folder_path):
        if file.is_file():
            if file.path.split(".")[1] == "xml":
                try: # only BDN export XML files are valid to be converted
                    convert(file.path, file.path.replace(".xml", ".csv"))
                    print(file.name)
                except Exception as error:
                    print(error)

batch("data", "data")
