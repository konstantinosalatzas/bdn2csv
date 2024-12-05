from bdn2csv.BDN import BDN
import pandas as pd
import xml.etree.ElementTree as et

def convert(xml_path: str, csv_path: str) -> pd.DataFrame:
    csv_name = csv_path.split("/")[-1].split(".")[0]
    csv_folder_path = "/".join(csv_path.split("/")[:-1])
    temp_csv_path = csv_folder_path+"/"+csv_name+" - temp.csv"

    bdn = BDN(xml_path)
    bdn.parse_types()
    bdn.parse_values()
    bdn.df = pd.DataFrame(bdn.dict)
    bdn.df = bdn.df.sort_values(by=['Path'])

    bdn.df.to_csv(temp_csv_path, index=False, encoding='utf-8')
    with open(temp_csv_path, 'r', encoding='utf-8') as rf, open(csv_path, 'w', encoding='utf-8') as wf:
        is_first_line = True
        for line in rf:
            if is_first_line:
                line = line.replace("Type_", "Type") # Handle the case when "Type" appears in standard AND non-standard attributes
                is_first_line = False
            line = line.replace('"""', '"') # Replace (""") with (") in quotation
            wf.write(line)

    return bdn.df