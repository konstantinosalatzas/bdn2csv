import unittest
import bdn2csv
import pandas as pd

class TestConvert(unittest.TestCase):
    def test_convert(self):
        xml_path = "/workspaces/bdn2csv/data/Export.xml"
        csv_path = "/workspaces/bdn2csv/data/Test.csv"
        bdn2csv.convert(xml_path, csv_path)
        df_out = pd.read_csv(csv_path) # Output DataFrame
        df_ans = pd.read_csv("/workspaces/bdn2csv/data/Import.csv") # Expected DataFrame
        df_cmp = df_out.compare(df_ans)
        self.assertEqual(len(df_cmp.index), 0)

class TestParseTypes(unittest.TestCase):
    def test_parse_types(self):
        xml_path = "/workspaces/bdn2csv/data/Export.xml"
        bdn = bdn2csv.BDN(xml_path)
        bdn.parse_types()
        list_out = bdn.std_attrs + bdn.non_std_attrs # Output list
        list_out = [attr.replace("Type_", "Type") for attr in list_out] # when "Type" is in standard AND non-standard attributes
        df = pd.read_csv("/workspaces/bdn2csv/data/Import.csv")
        list_ans = df.columns.tolist() # Expected list
        list_ans = [attr.replace("Type.1", "Type") for attr in list_ans] # when "Type" in in standard AND non-standard attributes
        self.assertListEqual(list_out, list_ans)

class TestParseValues(unittest.TestCase):
    def test_parse_values(self):
        xml_path = "/workspaces/bdn2csv/data/Export.xml"
        bdn = bdn2csv.BDN(xml_path)
        bdn.parse_types()
        bdn.parse_values()
        df_out = bdn.df # Output DataFrame
        df_out = df_out.rename(columns={"Type_": "Type"}) # when "Type" is in standard AND non-standard attributes
        if "Description" in df_out.columns.tolist():
            df_out['Description'] = df_out['Description'].apply(lambda x: str(x).strip('"'))
        df_ans = pd.read_csv("/workspaces/bdn2csv/data/Import.csv", dtype=object, keep_default_na=False) # Expected DataFrame
        df_cmp = df_out.compare(df_ans)
        self.assertEqual(len(df_cmp.index), 0)

if __name__ == "__main__":
    unittest.main()
