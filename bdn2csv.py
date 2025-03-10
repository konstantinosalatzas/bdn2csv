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
parser.add_argument("--viz", action="store_true")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="activate output verbosity")

args = parser.parse_args()

in_path = args.in_path
out_path = args.out_path

# convert
if not args.path2id:
    bdn2csv.convert(in_path, out_path)
    df = pd.read_csv(out_path)

# path2id
if args.path2id:
    df = bdn2csv.path2id(in_path)
    df.to_csv(out_path, index=False)

# viz
if args.viz:
    bdn2csv.visualize(in_path, out_path)

if args.verbose:
    print(df.head())
