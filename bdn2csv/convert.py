from bdn2csv.BDN import BDN
import pandas as pd
import xml.etree.ElementTree as et

def convert(xml_path: str, csv_path: str) -> BDN:
    csv_name = csv_path.split("/")[-1].split(".")[0]
    csv_folder_path = "/".join(csv_path.split("/")[:-1])
    temp_csv_path = csv_folder_path+"/"+csv_name+" - temp.csv"

    bdn = BDN(xml_path)
    bdn.parse_types()
    bdn.parse_values()

    bdn.df.to_csv(temp_csv_path, index=False, encoding='utf-8')
    with open(temp_csv_path, 'r', encoding='utf-8') as rf, open(csv_path, 'w', encoding='utf-8') as wf:
        is_first_line = True
        for line in rf:
            if is_first_line:
                line = line.replace("Type_", "Type") # when "Type" is in standard AND non-standard attributes
                is_first_line = False
            line = line.replace('"""', '"') # Replace (""") with (") quotation
            wf.write(line)

    return bdn
