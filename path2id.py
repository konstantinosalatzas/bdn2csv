import argparse
import bdn2csv
import pandas as pd

parser = argparse.ArgumentParser(prog="path2id")
parser.add_argument("json_path", type=str,
                    help="GET /terms response JSON file path")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="activate output verbosity")
args = parser.parse_args()

json_path = args.json_path
