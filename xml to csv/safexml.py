import xml.etree.ElementTree as ET
import csv
from collections import OrderedDict, defaultdict

def parse_xml_to_dict(element):
    """Recursively parse XML elements into an ordered dictionary."""
    data_dict = OrderedDict()
    if element.text and element.text.strip():
        data_dict[element.tag] = element.text.strip()
    
    children = list(element)
    if children:
        child_dict = defaultdict(list)
        for child in children:
            child_dict[child.tag].append(parse_xml_to_dict(child))
        # print(child_dict)
        for k, v in child_dict.items():
            if len(v) == 1:
                data_dict[k] = v[0]
            else:
                data_dict[k] = v
    
    if element.attrib:
        for k, v in element.attrib.items():
            data_dict[f"{element.tag}@{k}"] = v

    return data_dict

def flatten_dict(d, parent_key='', sep='.'):
    """Flatten nested ordered dictionary."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, item in enumerate(v):
                print("items",items)
                if isinstance(item, dict):
                    items.extend(flatten_dict(item, f"{new_key}[{i}]", sep=sep).items())
                else:
                    items.append((f"{new_key}[{i}]", item))
        else:
            items.append((new_key, v))
    return OrderedDict(items)

def xml_to_csv(xml_file, csv_file):
    """Convert XML file to CSV file."""
    tree = ET.parse(xml_file)
    root = tree.getroot()
    all_rows = []
    headers = OrderedDict()

    # Parse XML data to a list of dictionaries
    for element in root:
        row_dict = parse_xml_to_dict(element)
        flat_row_dict = flatten_dict(row_dict)
        all_rows.append(flat_row_dict)
        for key in flat_row_dict.keys():
            headers[key] = None 
            # print(headers)  # Maintain order of headers

    # Write to CSV file
    print("headers",headers)
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers.keys())
        writer.writeheader()
        for row in all_rows:
            print("-->",all_rows)
            writer.writerow(row)

# Usage
xml_to_csv('data.xml', 'output.csv')
