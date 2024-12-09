import argparse
import bdn2csv
import pandas as pd

xml_path = "/workspaces/bdn2csv/data/Export.xml"
csv_path = "/workspaces/bdn2csv/data/Import.csv"

bdn2csv.convert(xml_path, csv_path)

df = pd.read_csv(csv_path)
print(df.head())
