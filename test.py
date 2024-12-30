import unittest
import bdn2csv
import pandas as pd

class TestConvert(unittest.TestCase):
    def test_convert(self):
        xml_string = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <Resources>
            <Resource label="Warehouse" identity="Warehouse" type="BDNTERM">
                <Attributes>
                    <attribute name="Description" value="Storage facility for goods and raw materials"/>
                    <attribute name="Requirements" value="Must meet size and security standards"/>
                    <attribute name="Status" value="Not Specified"/>
                    <attribute name="Importance" value="Medium"/>
                </Attributes>
                <Dependencies>
                    <dependency type="A">
                        <Resource identity="Logistics" type="BDNTAG"/>
                    </dependency>
                </Dependencies>
            </Resource>
            <Resource label="Loading Dock" identity="Warehouse\Loading Dock" type="BDNTERM">
                <Attributes>
                    <attribute name="Description" value="Facility for incoming and outgoing goods"/>
                    <attribute name="Requirements" value=""/>
                    <attribute name="Status" value="Not Specified"/>
                    <attribute name="Importance" value="Medium"/>
                </Attributes>
                <Dependencies>
                    <dependency type="D">
                        <Resource label="Warehouse" identity="Warehouse" type="BDNTERMREF"/>
                    </dependency>
                </Dependencies>
            </Resource>
            <Resource label="Section" identity="Warehouse\Section" type="BDNTERM">
                <Attributes>
                    <attribute name="Description" value="Section of the warehouse designated for a specific product or type of product"/>
                    <attribute name="Requirements" value="Must be secure and accessible"/>
                    <attribute name="Status" value="Not Specified"/>
                    <attribute name="Importance" value="Medium"/>
                </Attributes>
                <Dependencies>
                    <dependency type="D">
                        <Resource label="Warehouse" identity="Warehouse" type="BDNTERMREF"/>
                    </dependency>
                    <dependency type="A">
                        <Resource label="Picking" identity="Picking" type="BDNTERMREF"/>
                        <Resource identity="Logistics" type="BDNTAG"/>
                    </dependency>
                </Dependencies>
            </Resource>
        </Resources>"""
        csv_path = "./data/Test.csv"
        bdn2csv.convert(xml_string, csv_path)
        df_out = pd.read_csv(csv_path, dtype=object, keep_default_na=False) # Output DataFrame
        # Expected DataFrame
        df_ans = pd.DataFrame(
            {"Name": ["Warehouse", "Loading Dock", "Section"],
             "Path": ["Warehouse", "Warehouse\Loading Dock", "Warehouse\Section"],
             "Description": ["Storage facility for goods and raw materials", "Facility for incoming and outgoing goods", "Section of the warehouse designated for a specific product or type of product"],
             "Requirements": ["Must meet size and security standards", "", "Must be secure and accessible"],
             "Status": ["Not Specified", "Not Specified", "Not Specified"],
             "Importance": ["Medium", "Medium", "Medium"],
             "Tags": ["Logistics", "", "Logistics"],
             "Related Terms": ["", "", "Picking"]}
        )
        df_cmp = df_out.compare(df_ans)
        self.assertEqual(len(df_cmp.index), 0)

class TestParse(unittest.TestCase):
    def setUp(self):
        xml_string = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <Resources>
            <Resource label="Warehouse" identity="Warehouse" type="BDNTERM">
                <Attributes>
                    <attribute name="Description" value="Storage facility for goods and raw materials"/>
                    <attribute name="Requirements" value="Must meet size and security standards"/>
                    <attribute name="Status" value="Not Specified"/>
                    <attribute name="Importance" value="Medium"/>
                </Attributes>
                <Dependencies>
                    <dependency type="A">
                        <Resource identity="Logistics" type="BDNTAG"/>
                    </dependency>
                </Dependencies>
            </Resource>
            <Resource label="Loading Dock" identity="Warehouse\Loading Dock" type="BDNTERM">
                <Attributes>
                    <attribute name="Description" value="Facility for incoming and outgoing goods"/>
                    <attribute name="Requirements" value=""/>
                    <attribute name="Status" value="Not Specified"/>
                    <attribute name="Importance" value="Medium"/>
                </Attributes>
                <Dependencies>
                    <dependency type="D">
                        <Resource label="Warehouse" identity="Warehouse" type="BDNTERMREF"/>
                    </dependency>
                </Dependencies>
            </Resource>
            <Resource label="Section" identity="Warehouse\Section" type="BDNTERM">
                <Attributes>
                    <attribute name="Description" value="Section of the warehouse designated for a specific product or type of product"/>
                    <attribute name="Requirements" value="Must be secure and accessible"/>
                    <attribute name="Status" value="Not Specified"/>
                    <attribute name="Importance" value="Medium"/>
                </Attributes>
                <Dependencies>
                    <dependency type="D">
                        <Resource label="Warehouse" identity="Warehouse" type="BDNTERMREF"/>
                    </dependency>
                    <dependency type="A">
                        <Resource label="Picking" identity="Picking" type="BDNTERMREF"/>
                        <Resource identity="Logistics" type="BDNTAG"/>
                    </dependency>
                </Dependencies>
            </Resource>
        </Resources>"""
        self.bdn = bdn2csv.BDN(xml_string)
        # Expected DataFrame
        self.df_ans = pd.DataFrame(
            {"Name": ["Warehouse", "Loading Dock", "Section"],
             "Path": ["Warehouse", "Warehouse\Loading Dock", "Warehouse\Section"],
             "Description": ["Storage facility for goods and raw materials", "Facility for incoming and outgoing goods", "Section of the warehouse designated for a specific product or type of product"],
             "Requirements": ["Must meet size and security standards", "", "Must be secure and accessible"],
             "Status": ["Not Specified", "Not Specified", "Not Specified"],
             "Importance": ["Medium", "Medium", "Medium"],
             "Tags": ["Logistics", "", "Logistics"],
             "Related Terms": ["", "", "Picking"]}
        )

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
