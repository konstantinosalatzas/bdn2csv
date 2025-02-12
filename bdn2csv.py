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

in_path = args.in_path
out_path = args.out_path

bdn2csv.convert(in_path, out_path)

if args.verbose:
    df = pd.read_csv(out_path)
    print(df.head())
