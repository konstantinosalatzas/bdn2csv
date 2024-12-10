import argparse
import bdn2csv
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("xml_path", type=str,
                    help="XML Export file path")
parser.add_argument("csv_path", type=str,
                    help="CSV Import file path")
args = parser.parse_args()
xml_path = args.xml_path
csv_path = args.csv_path
print(xml_path, csv_path)

'''
xml_path = "/workspaces/bdn2csv/data/Export.xml"
csv_path = "/workspaces/bdn2csv/data/Import.csv"

bdn2csv.convert(xml_path, csv_path)

df = pd.read_csv(csv_path)
print(df.head())
'''
