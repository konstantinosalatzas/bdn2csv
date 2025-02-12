import argparse
import bdn2csv
import pandas as pd

parser = argparse.ArgumentParser(prog="bdn2csv",
                                 description="Convert SAS BDN XML Export file to CSV Import file")
parser.add_argument("in_path", type=str,
                    help="input file path")
parser.add_argument("out_path", type=str,
                    help="output file path")
parser.add_argument("--path2id", action="store_true")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="activate output verbosity")
args = parser.parse_args()

xml_path = args.xml_path
csv_path = args.csv_path

bdn2csv.convert(xml_path, csv_path)

if args.verbose:
    df = pd.read_csv(csv_path)
    print(df.head())
