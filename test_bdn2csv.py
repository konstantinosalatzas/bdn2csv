import unittest
import bdn2csv
import pandas as pd

class TestConvert(unittest.TestCase):
    def test_convert(self):
        xml_path = "/workspaces/bdn2csv/data/Export.xml"
        csv_path = "/workspaces/bdn2csv/data/Test.csv"
        bdn2csv.convert(xml_path, csv_path)
        out = pd.read_csv(csv_path) # Output DataFrame
        ans = pd.read_csv("/workspaces/bdn2csv/data/Import.csv") # Expected DataFrame
        cmp = out.compare(ans)
        self.assertEqual(len(cmp.index), 0)

class TestParse(unittest.TestCase):
    def test_parse_types(self):
        pass

    def test_parse_values(self):
        pass

if __name__ == "__main__":
    unittest.main()
