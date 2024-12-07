import pandas as pd
import xml.etree.ElementTree as et

class BDN:
    def __init__(self, xml_path: str):
        self.xml = et.parse(xml_path)
        self.types = [] # list of unique types of attributes
        self.std_attrs = ["Name", "Path"] # list of unique standard attrbiutes
        self.non_std_attrs = [] # list of unique non-standard attributes
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
                        # Handle the case when "Type" appears in standard AND non-standard attributes
                        if attribute.attrib['name'] == "Type":
                            if "Type_" not in std_attrs:
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
                if not has_tag_or_ref:
                    continue
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
                        # Handle the case when "Type" appears in standard AND non-standard attributes
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
                # Handle multiple values per attribute
                for a in non_std_attrs:
                    values[a] = ""
                if dep != None:
                    for r in dep.findall("Resource"):
                        if r.attrib['type'] == "BDNATTRIB":
                            for a in r.find("Attributes").findall("attribute"):
                                if a.attrib['name'] == "Value":
                                    if len(values[r.attrib['label']]) > 0:
                                        values[r.attrib['label']] += ","
                                    values[r.attrib['label']] += a.attrib['value']
                        elif r.attrib['type'] == "BDNNOTE": # Notes
                            for a in r.find("Attributes").findall("attribute"):
                                if a.attrib['name'] == "Content":
                                    if len(values['Notes']) > 0:
                                        values['Notes'] += ","
                                    values['Notes'] += a.attrib['value']
                if has_tag_or_ref:
                    for r in tag_or_ref.findall("Resource"):
                        if r.attrib['type'] == "BDNTAG": # Tags
                            if len(values['Tags']) > 0:
                                values['Tags'] += ","
                            values['Tags'] += r.attrib['identity']
                    for r in tag_or_ref.findall("Resource"):
                        if r.attrib['type'] == "BDNTERMREF": # Related Terms
                            if len(values['Related Terms']) > 0:
                                values['Related Terms'] += ","
                            values['Related Terms'] += r.attrib['identity']
                for a in non_std_attrs:
                    bdn[a].append(values[a])
        
        self.df = pd.DataFrame(bdn)
        self.df = self.df.sort_values(by=['Path'])
        self.df = self.df.reset_index(drop=True)
        return self.df
