import unittest
import bdn2csv
import pandas as pd

class TestConvert(unittest.TestCase):
    def test_convert(self):
        xml_path = "/workspaces/bdn2csv/data/Warehouse.xml"
        csv_path = "/workspaces/bdn2csv/data/Test.csv"
        bdn2csv.convert(xml_path, csv_path)
        df_out = pd.read_csv(csv_path) # Output DataFrame
        df_ans = pd.read_csv("/workspaces/bdn2csv/data/Warehouse.csv") # Expected DataFrame
        df_cmp = df_out.compare(df_ans)
        self.assertEqual(len(df_cmp.index), 0)

class TestParse(unittest.TestCase):
    def setUp(self):
        self.bdn = bdn2csv.BDN("/workspaces/bdn2csv/data/Warehouse.xml")
        self.df_ans = pd.read_csv("/workspaces/bdn2csv/data/Warehouse.csv", dtype=object, keep_default_na=False) # Expected DataFrame

    def test_parse_types(self):
        self.bdn.parse_types()
        list_out = self.bdn.std_attrs + self.bdn.non_std_attrs # Output list
        list_out = [attr.replace("Type_", "Type") for attr in list_out] # when "Type" is in standard AND non-standard attributes
        list_ans = self.df_ans.columns.tolist() # Expected list
        list_ans = [attr.replace("Type.1", "Type") for attr in list_ans] # when "Type" in in standard AND non-standard attributes
        self.assertListEqual(list_out, list_ans)

    def test_parse_values(self):
        self.bdn.parse_types()
        self.bdn.parse_values()
        df_out = self.bdn.df # Output DataFrame
        df_out = df_out.rename(columns={"Type_": "Type"}) # when "Type" is in standard AND non-standard attributes
        if "Description" in df_out.columns.tolist():
            df_out['Description'] = df_out['Description'].apply(lambda x: str(x).strip('"'))
        df_cmp = df_out.compare(self.df_ans)
        self.assertEqual(len(df_cmp.index), 0)

if __name__ == "__main__":
    unittest.main()
