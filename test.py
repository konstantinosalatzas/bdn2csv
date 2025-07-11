import unittest
import bdn2csv
import pandas as pd
import networkx as nx

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
                    <attribute name="Type" value="Root"/>
                </Attributes>
                <Dependencies>
                    <dependency type="A">
                        <Resource identity="Logistics" type="BDNTAG"/>
                    </dependency>
                    <dependency type="I">
                        <Resource label="Type" identity="Warehouse\\Attribute0" type="BDNATTRIB">
                            <Attributes>
                                <attribute name="Instructions" value=""/>
                                <attribute name="Value" value="Test"/>
                                <attribute name="Required" value="Y"/>
                                <attribute name="Type" value="Common"/>
                            </Attributes>
                        </Resource>
                    </dependency>
                </Dependencies>
            </Resource>
            <Resource label="Loading Dock" identity="Warehouse\\Loading Dock" type="BDNTERM">
                <Attributes>
                    <attribute name="Description" value="Facility for incoming and outgoing goods"/>
                    <attribute name="Requirements" value=""/>
                    <attribute name="Status" value="Not Specified"/>
                    <attribute name="Importance" value="Medium"/>
                    <attribute name="Type" value="Leaf"/>
                </Attributes>
                <Dependencies>
                    <dependency type="D">
                        <Resource label="Warehouse" identity="Warehouse" type="BDNTERMREF"/>
                    </dependency>
                    <dependency type="I">
                        <Resource label="Type" identity="Warehouse\\Loading Dock\\Attribute0" type="BDNATTRIB">
                            <Attributes>
                                <attribute name="Instructions" value=""/>
                                <attribute name="Value" value="Test"/>
                                <attribute name="Required" value="Y"/>
                                <attribute name="Type" value="Common"/>
                            </Attributes>
                        </Resource>
                    </dependency>
                </Dependencies>
            </Resource>
            <Resource label="Section" identity="Warehouse\\Section" type="BDNTERM">
                <Attributes>
                    <attribute name="Description" value="Section of the warehouse designated for a specific product or type of product"/>
                    <attribute name="Requirements" value="Must be secure and accessible"/>
                    <attribute name="Status" value="Not Specified"/>
                    <attribute name="Importance" value="Medium"/>
                    <attribute name="Type" value="Leaf"/>
                </Attributes>
                <Dependencies>
                    <dependency type="D">
                        <Resource label="Warehouse" identity="Warehouse" type="BDNTERMREF"/>
                    </dependency>
                    <dependency type="A">
                        <Resource label="Picking" identity="Picking" type="BDNTERMREF"/>
                        <Resource identity="Warehouse\\Loading Dock" type="BDNTERMREF"/>
                        <Resource identity="Logistics" type="BDNTAG"/>
                    </dependency>
                    <dependency type="I">
                        <Resource label="Type" identity="Warehouse\\Section\\Attribute0" type="BDNATTRIB">
                            <Attributes>
                                <attribute name="Instructions" value=""/>
                                <attribute name="Value" value="Test"/>
                                <attribute name="Required" value="Y"/>
                                <attribute name="Type" value="Common"/>
                            </Attributes>
                        </Resource>
                    </dependency>
                </Dependencies>
            </Resource>
        </Resources>""" # input XML
        df_ans = pd.DataFrame(
            {"Name": ["Warehouse", "Loading Dock", "Section"],
             "Path": ["Warehouse", "Warehouse\\Loading Dock", "Warehouse\\Section"],
             "Description": ["Storage facility for goods and raw materials", "Facility for incoming and outgoing goods", "Section of the warehouse designated for a specific product or type of product"],
             "Requirements": ["Must meet size and security standards", "", "Must be secure and accessible"],
             "Status": ["Not Specified", "Not Specified", "Not Specified"],
             "Importance": ["Medium", "Medium", "Medium"],
             "Type": ["Root", "Leaf", "Leaf"],
             "Type.1": ["Test", "Test", "Test"],
             "Tags": ["Logistics", "", "Logistics"],
             "Related Terms": ["", "", "Picking|Picking,Warehouse\\Loading Dock"]}
        ) # expected DataFrame

        csv_path = "./data/Test.csv"
        bdn2csv.convert(xml_string, csv_path)
        df_out = pd.read_csv(csv_path, dtype=object, keep_default_na=False) # output DataFrame

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
                    <attribute name="Type" value="Root"/>
                </Attributes>
                <Dependencies>
                    <dependency type="A">
                        <Resource identity="Logistics" type="BDNTAG"/>
                    </dependency>
                    <dependency type="I">
                        <Resource label="Type" identity="Warehouse\\Attribute0" type="BDNATTRIB">
                            <Attributes>
                                <attribute name="Instructions" value=""/>
                                <attribute name="Value" value="Test"/>
                                <attribute name="Required" value="Y"/>
                                <attribute name="Type" value="Common"/>
                            </Attributes>
                        </Resource>
                    </dependency>
                </Dependencies>
            </Resource>
            <Resource label="Loading Dock" identity="Warehouse\\Loading Dock" type="BDNTERM">
                <Attributes>
                    <attribute name="Description" value="Facility for incoming and outgoing goods"/>
                    <attribute name="Requirements" value=""/>
                    <attribute name="Status" value="Not Specified"/>
                    <attribute name="Importance" value="Medium"/>
                    <attribute name="Type" value="Leaf"/>
                </Attributes>
                <Dependencies>
                    <dependency type="D">
                        <Resource label="Warehouse" identity="Warehouse" type="BDNTERMREF"/>
                    </dependency>
                    <dependency type="I">
                        <Resource label="Type" identity="Warehouse\\Loading Dock\\Attribute0" type="BDNATTRIB">
                            <Attributes>
                                <attribute name="Instructions" value=""/>
                                <attribute name="Value" value="Test"/>
                                <attribute name="Required" value="Y"/>
                                <attribute name="Type" value="Common"/>
                            </Attributes>
                        </Resource>
                    </dependency>
                </Dependencies>
            </Resource>
            <Resource label="Section" identity="Warehouse\\Section" type="BDNTERM">
                <Attributes>
                    <attribute name="Description" value="Section of the warehouse designated for a specific product or type of product"/>
                    <attribute name="Requirements" value="Must be secure and accessible"/>
                    <attribute name="Status" value="Not Specified"/>
                    <attribute name="Importance" value="Medium"/>
                    <attribute name="Type" value="Leaf"/>
                </Attributes>
                <Dependencies>
                    <dependency type="D">
                        <Resource label="Warehouse" identity="Warehouse" type="BDNTERMREF"/>
                    </dependency>
                    <dependency type="A">
                        <Resource label="Picking" identity="Picking" type="BDNTERMREF"/>
                        <Resource identity="Warehouse\\Loading Dock" type="BDNTERMREF"/>
                        <Resource identity="Logistics" type="BDNTAG"/>
                    </dependency>
                    <dependency type="I">
                        <Resource label="Type" identity="Warehouse\\Section\\Attribute0" type="BDNATTRIB">
                            <Attributes>
                                <attribute name="Instructions" value=""/>
                                <attribute name="Value" value="Test"/>
                                <attribute name="Required" value="Y"/>
                                <attribute name="Type" value="Common"/>
                            </Attributes>
                        </Resource>
                    </dependency>
                </Dependencies>
            </Resource>
        </Resources>""" # input XML
        self.bdn = bdn2csv.BDN(xml_string)
        self.df_ans = pd.DataFrame(
            {"Name": ["Warehouse", "Loading Dock", "Section"],
             "Path": ["Warehouse", "Warehouse\\Loading Dock", "Warehouse\\Section"],
             "Description": ["Storage facility for goods and raw materials", "Facility for incoming and outgoing goods", "Section of the warehouse designated for a specific product or type of product"],
             "Requirements": ["Must meet size and security standards", "", "Must be secure and accessible"],
             "Status": ["Not Specified", "Not Specified", "Not Specified"],
             "Importance": ["Medium", "Medium", "Medium"],
             "Type": ["Root", "Leaf", "Leaf"],
             "Type.1": ["Test", "Test", "Test"],
             "Tags": ["Logistics", "", "Logistics"],
             "Related Terms": ["", "", "Picking|Picking,Warehouse\\Loading Dock"]}
        ) # expected DataFrame

    def test_parse_types(self):
        list_ans = self.df_ans.columns.tolist() # expected list
        list_ans = [attr.replace("Type.1", "Type") for attr in list_ans] # when "Type" in in standard and non-standard attributes

        self.bdn.parse_types()
        list_out = self.bdn.std_attrs + self.bdn.non_std_attrs # output list
        list_out = [attr.replace("Type_", "Type") for attr in list_out] # when "Type" is in standard and non-standard attributes
        
        self.assertListEqual(list_out, list_ans)

    def test_parse_values(self):
        self.df_ans = self.df_ans.rename(columns={"Type": "Type_", "Type.1": "Type"}) # when "Type" is in standard and non-standard attributes

        self.bdn.parse_types()
        self.bdn.parse_values()
        df_out = self.bdn.df # output DataFrame
        if "Description" in df_out.columns.tolist():
            df_out['Description'] = df_out['Description'].apply(lambda x: str(x).strip('"'))
        
        df_cmp = df_out.compare(self.df_ans)
        self.assertEqual(len(df_cmp.index), 0)

class TestAddMultipleValue(unittest.TestCase):
    def test_add_multiple_value_to_empty(self):
        values = ""
        value = "Warehouse\\Loading Dock"
        values_ans = "Warehouse\\Loading Dock" # expected string
        
        values_out = bdn2csv.add_multiple_value(values, value) # output string
        
        self.assertEqual(values_out, values_ans)

    def test_add_multiple_value_to_not_empty(self):
        values = "Picking"
        value = "Warehouse\\Loading Dock"
        values_ans = "Picking,Warehouse\\Loading Dock" # expected string
        
        values_out = bdn2csv.add_multiple_value(values, value) # output string
        
        self.assertEqual(values_out, values_ans)

class TestPath2Id(unittest.TestCase):
    def test_id2name(self):
        response = {
            "items": [{"name": "Warehouse", "id": "1251572"},
                      {"name": "Loading Dock", "id": "1251573", "parentId": "1251572"},
                      {"name": "Section", "id": "1251574", "parentId": "1251572"}]
        } # input JSON dict
        df_ans = pd.DataFrame(
            {"name": ["Warehouse", "Loading Dock", "Section"],
             "id": ["1251572", "1251573", "1251574"],
             "parentId": ["", "1251572", "1251572"],
             "parentName": ["", "Warehouse", "Warehouse"]}
        ) # expected DataFrame

        df_out = bdn2csv.id2name(response) # output DataFrame

        df_cmp = df_out.compare(df_ans)
        self.assertEqual(len(df_cmp.index), 0)

    def test_id2path(self):
        df = pd.DataFrame(
            {"name": ["Warehouse", "Loading Dock", "Section"],
             "id": ["1251572", "1251573", "1251574"],
             "parentId": ["", "1251572", "1251572"],
             "parentName": ["", "Warehouse", "Warehouse"]}
        ) # input DataFrame
        df_ans = pd.DataFrame(
            {"path": ["Warehouse", "Warehouse\\Loading Dock", "Warehouse\\Section"],
             "id": ["1251572", "1251573", "1251574"]}
        ) # expected DataFrame

        df_out = bdn2csv.id2path(df) # output DataFrame

        df_cmp = df_out.compare(df_ans)
        self.assertEqual(len(df_cmp.index), 0)

    def test_path2id(self):
        json_string = """{
            "items": [{"name": "Warehouse", "id": "1251572"},
                      {"name": "Loading Dock", "id": "1251573", "parentId": "1251572"},
                      {"name": "Section", "id": "1251574", "parentId": "1251572"}]
        }""" # input JSON string
        df_ans = pd.DataFrame(
            {"path": ["Warehouse", "Warehouse\\Loading Dock", "Warehouse\\Section"],
             "id": ["1251572", "1251573", "1251574"]}
        ) # expected DataFrame

        df_out = bdn2csv.path2id(json_string) # output DataFrame

        df_cmp = df_out.compare(df_ans)
        self.assertEqual(len(df_cmp.index), 0)

class TestViz(unittest.TestCase):
    def test_construct(self):
        df = pd.DataFrame(
            {"Name": ["Warehouse", "Loading Dock", "Section"],
             "Path": ["Warehouse", "Warehouse\\Loading Dock", "Warehouse\\Section"],
             "Description": ["Storage facility for goods and raw materials", "Facility for incoming and outgoing goods", "Section of the warehouse designated for a specific product or type of product"],
             "Requirements": ["Must meet size and security standards", "", "Must be secure and accessible"],
             "Status": ["Not Specified", "Not Specified", "Not Specified"],
             "Importance": ["Medium", "Medium", "Medium"],
             "Type": ["Root", "Leaf", "Leaf"],
             "Type.1": ["Test", "Test", "Test"],
             "Tags": ["Logistics", "", "Logistics"],
             "Related Terms": ["", "", "Picking|Picking,Warehouse\\Loading Dock"]}
        ) # input DataFrame
        dict_ans = {"Warehouse": ["Warehouse\\Loading Dock", "Warehouse\\Section"],
                    "Warehouse\\Loading Dock": ["Warehouse\\Section"],
                    "Warehouse\\Section": ["Warehouse\\Loading Dock"]} # expected adjacency dictionary

        bdn = bdn2csv.BDNx(df)
        G = bdn.G
        adj = G.adj
        dict_out = {} # output adjacency dictionary
        for v in adj:
            dict_out[v] = []
            for u in adj[v]:
                dict_out[v].append(u)
        
        self.assertDictEqual(dict_out, dict_ans)

class TestUtils(unittest.TestCase):
    def setUp(self):
        df = pd.DataFrame(
            {"Name": ["Warehouse", "Loading Dock", "Section"],
             "Path": ["Warehouse", "Warehouse\\Loading Dock", "Warehouse\\Section"],
             "Description": ["Storage facility for goods and raw materials", "Facility for incoming and outgoing goods", "Section of the warehouse designated for a specific product or type of product"],
             "Requirements": ["Must meet size and security standards", "", "Must be secure and accessible"],
             "Status": ["Not Specified", "Not Specified", "Not Specified"],
             "Importance": ["Medium", "Medium", "Medium"],
             "Type": ["Root", "Leaf", "Leaf"],
             "Type.1": ["Test", "Test", "Test"],
             "Tags": ["Logistics", "", "Logistics"],
             "Related Terms": ["", "", "Picking|Picking,Warehouse\\Loading Dock"]}
        ) # input DataFrame
        self.df_dict = bdn2csv.BDN_dict(df, key='Path')

    def test_lookup_exists(self):
        row_ans = pd.Series(
            {"Name": "Loading Dock",
             "Path": "Warehouse\\Loading Dock",
             "Description": "Facility for incoming and outgoing goods",
             "Requirements": "",
             "Status": "Not Specified",
             "Importance": "Medium",
             "Type": "Leaf",
             "Type.1": "Test",
             "Tags": "",
             "Related Terms": ""}
        ) # expected Series

        df_dict = self.df_dict
        row_out = df_dict.lookup('Warehouse\\Loading Dock') # output Series

        row_cmp = row_out.compare(row_ans)
        self.assertEqual(len(row_cmp.index), 0)

    def test_lookup_not_exists(self):
        row_ans = pd.Series(dtype='float64') # expected Series

        df_dict = self.df_dict
        row_out = df_dict.lookup('Warehouse\\Test') # output Series

        row_cmp = row_out.compare(row_ans)
        self.assertEqual(len(row_cmp.index), 0)

    def test_get_parent_path_for_leaf(self):
        term_path = "Warehouse\\Section"
        parent_path_ans = "Warehouse"

        parent_path_out = bdn2csv.get_parent_path(term_path)

        self.assertEqual(parent_path_out, parent_path_ans)

    def test_get_parent_path_for_root(self):
        term_path = "Warehouse"
        parent_path_ans = ""

        parent_path_out = bdn2csv.get_parent_path(term_path)

        self.assertEqual(parent_path_out, parent_path_ans)

    def test_get_related_term_path_with_label(self):
        related_term = "Warehouse\\Loading Dock|Picking"
        related_term_path_ans = "Warehouse\\Loading Dock"
        
        related_term_path_out = bdn2csv.get_related_term_path(related_term)

        self.assertEqual(related_term_path_out, related_term_path_ans)

    def test_get_related_term_path_without_label(self):
        related_term = "Warehouse\\Loading Dock"
        related_term_path_ans = "Warehouse\\Loading Dock"
        
        related_term_path_out = bdn2csv.get_related_term_path(related_term)

        self.assertEqual(related_term_path_out, related_term_path_ans)

    def test_get_related_term_label_with_label(self):
        related_term = "Warehouse\\Loading Dock|Picking"
        related_term_label_ans = "Picking"
        
        related_term_label_out = bdn2csv.get_related_term_label(related_term)

        self.assertEqual(related_term_label_out, related_term_label_ans)

    def test_get_related_term_label_without_label(self):
        related_term = "Warehouse\\Loading Dock"
        related_term_label_ans = ""
        
        related_term_label_out = bdn2csv.get_related_term_label(related_term)

        self.assertEqual(related_term_label_out, related_term_label_ans)

    def test_check_dag_and_find_cycles_empty(self):
        g = nx.DiGraph() # empty directed graph
        cycles_ans = []

        cycles_out = bdn2csv.check_dag_and_find_cycles(g)

        self.assertEqual(cycles_out, cycles_ans)

    def test_check_dag_and_find_cycles(self):
        g = nx.DiGraph()
        g.add_nodes_from(["Warehouse", "Warehouse\\Loading Dock", "Warehouse\\Section"])

if __name__ == "__main__":
    unittest.main()
