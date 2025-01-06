import pandas as pd
import xml.etree.ElementTree as et

def add_multiple_value(values: str, value: str) -> str:
    if len(values) > 0:
        values += ","
    values += value
    return values

class BDN:
    def __init__(self, xml_path: str):
        try:
            self.xml = et.parse(xml_path) # parse XML from file
        except:
            self.xml = et.fromstring(xml_path) # parse XML from string
        self.types = []
        self.std_attrs = ["Name", "Path"] # standard attributes
        self.non_std_attrs = [] # non-standard attributes
        self.df = pd.DataFrame() # DataFrame BDN representation
    
    def parse_types(self) -> list[str]:
        xml = self.xml
        types = self.types
        std_attrs = self.std_attrs
        non_std_attrs = self.non_std_attrs

        # Parse types of attributes
        for resource in xml.findall("Resource"):
            if resource.attrib['type'] == "BDNTERM":
                for attribute in resource.find("Attributes").findall("attribute"): # standard attributes
                    if attribute.attrib['name'] not in std_attrs:
                        # Handle the case when "Type" is in standard and non-standard attributes
                        if (attribute.attrib['name'] == "Type"):
                            if ("Type_" not in std_attrs):
                                std_attrs.append("Type_")
                        else:
                            std_attrs.append(attribute.attrib['name'])
                if resource.find("Dependencies") is not None:
                    has_tag_or_ref = False
                    dep = None
                    for dependency in resource.find("Dependencies").findall("dependency"):
                        if dependency.attrib['type'] == "I":
                            dep = dependency
                        elif dependency.attrib['type'] == "A": # Tag or Related Term
                            tag_or_ref = dependency
                            has_tag_or_ref = True
                else:
                    continue
                if dep != None:
                    for r in dep.findall("Resource"): # non-standard attributes
                        if r.attrib['type'] not in types:
                            types.append(r.attrib['type'])
                        if (r.attrib['type'] == "BDNATTRIB") and (r.attrib['label'] not in non_std_attrs) and (r.attrib['label'] not in std_attrs):
                            non_std_attrs.append(r.attrib['label'])
                        elif (r.attrib['type'] == "BDNNOTE") and ("Notes" not in non_std_attrs): # Notes
                            non_std_attrs.append("Notes")
                if has_tag_or_ref:
                    for r in tag_or_ref.findall("Resource"):
                        if (r.attrib['type'] == "BDNTAG") and ("Tags" not in non_std_attrs): # Tags
                            non_std_attrs.append("Tags")
                        if (r.attrib['type'] == "BDNTERMREF") and ("Related Terms" not in non_std_attrs): # Related Terms
                            non_std_attrs.append("Related Terms")
        
        return (std_attrs + non_std_attrs)
    
    def parse_values(self) -> pd.DataFrame:
        xml = self.xml
        std_attrs = self.std_attrs
        non_std_attrs = self.non_std_attrs
        bdn = {}
        for a in (std_attrs + non_std_attrs):
            bdn[a] = []
        
        # Parse attribute values
        for resource in xml.findall("Resource"):
            if resource.attrib['type'] == "BDNTERM":
                # Parse standard attribute values
                bdn['Name'].append(resource.attrib['label'])
                bdn['Path'].append(resource.attrib['identity'])
                for attribute in resource.find("Attributes").findall("attribute"):
                    if attribute.attrib['name'] == "Description":
                        bdn[attribute.attrib['name']].append("\""+attribute.attrib['value']+"\"")
                    else:
                        # Handle the case when "Type" is in standard and non-standard attributes
                        if attribute.attrib['name'] == "Type":
                            bdn["Type_"].append(attribute.attrib['value'])
                        else:
                            bdn[attribute.attrib['name']].append(attribute.attrib['value'])
                # Parse non-standard attribute values
                if resource.find("Dependencies") is not None:
                    has_tag_or_ref = False
                    dep = None
                    for dependency in resource.find("Dependencies").findall("dependency"):
                        if dependency.attrib['type'] == "I":
                            dep = dependency
                        elif dependency.attrib['type'] == "A": # Tag or Related Term
                            tag_or_ref = dependency
                            has_tag_or_ref = True
                else:
                    for a in non_std_attrs:
                        bdn[a].append("")
                    continue
                values = {}
                # Handle attributes with multiple values
                for a in non_std_attrs:
                    values[a] = ""
                if dep != None:
                    for r in dep.findall("Resource"):
                        if r.attrib['type'] == "BDNATTRIB":
                            for a in r.find("Attributes").findall("attribute"):
                                if a.attrib['name'] == "Value":
                                    values[r.attrib['label']] = add_multiple_value(values[r.attrib['label']], a.attrib['value'])
                        elif r.attrib['type'] == "BDNNOTE": # Notes
                            for a in r.find("Attributes").findall("attribute"):
                                if a.attrib['name'] == "Content":
                                    values['Notes'] = add_multiple_value(values['Notes'], a.attrib['value'])
                if has_tag_or_ref:
                    for r in tag_or_ref.findall("Resource"):
                        if r.attrib['type'] == "BDNTAG": # Tags
                            values['Tags'] = add_multiple_value(values['Tags'], r.attrib['identity'])
                    for r in tag_or_ref.findall("Resource"):
                        if r.attrib['type'] == "BDNTERMREF": # Related Terms
                            values['Related Terms'] = add_multiple_value(values['Related Terms'], r.attrib['identity'])
                for a in non_std_attrs:
                    bdn[a].append(values[a])
        
        self.df = pd.DataFrame(bdn)
        self.df = self.df.sort_values(by=['Path'])
        self.df = self.df.reset_index(drop=True)
        return self.df
