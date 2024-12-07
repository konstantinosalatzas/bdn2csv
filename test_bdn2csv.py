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

class TestParseTypes(unittest.TestCase):
    def test_parse_types(self):
        xml_path = "/workspaces/bdn2csv/data/Export.xml"
        bdn = bdn2csv.BDN(xml_path)
        bdn.parse_types()
        list_out = bdn.std_attrs + bdn.non_std_attrs # Output list
        list_out = [attr.replace("Type_", "Type") for attr in list_out] # the case when "Type" is in standard AND non-standard attributes
        df = pd.read_csv("/workspaces/bdn2csv/data/Import.csv")
        list_ans = df.columns.tolist() # Expected list
        list_ans = [attr.replace("Type.1", "Type") for attr in list_ans] # the case when "Type" in in standard AND non-standard attributes
        self.assertListEqual(list_out, list_ans)

class TestParseValues(unittest.TestCase):
    def test_parse_values(self):
        pass

if __name__ == "__main__":
    unittest.main()
