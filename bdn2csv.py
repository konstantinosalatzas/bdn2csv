import argparse
import bdn2csv
import pandas as pd

parser = argparse.ArgumentParser(prog="bdn2csv",
                                 description="Convert SAS BDN XML Export file to CSV Import file")
parser.add_argument("xml_path", type=str,
                    help="XML Export file path")
parser.add_argument("csv_path", type=str,
                    help="CSV Import file path")
parser.add_argument("-v", "--verbose", action="store_true")
args = parser.parse_args()

xml_path = args.xml_path
csv_path = args.csv_path

bdn2csv.convert(xml_path, csv_path)

if args.verbose:
    df = pd.read_csv(csv_path)
    print(df.head())
