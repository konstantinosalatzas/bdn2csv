import argparse
import bdn2csv
import pandas as pd

parser = argparse.ArgumentParser(prog="path2id")
parser.add_argument("json_path", type=str,
                    help="GET /terms response JSON file path")
parser.add_argument("csv_path", type=str,
                    help="output CSV file path")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="activate output verbosity")
args = parser.parse_args()

json_path = args.json_path
csv_path = args.csv_path

df = bdn2csv.path2id(json_path)

df.to_csv(csv_path, index=False)

if args.verbose:
    print(df.head())
