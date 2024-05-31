import xml.etree.ElementTree as ET
import csv

def flatten_xml(element, parent_key='', sep='_'):
    items = {}
    for child in list(element):
        key = f"{parent_key}{sep}{child.tag}" if parent_key else child.tag
        if list(child):
            items.update(flatten_xml(child, key, sep))
        else:
            items[key] = child.text
    return items

def xml_to_csv(xml_file, csv_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Collect data
    rows = []
    headers = set()
    for elem in root.findall('.//'):
        row_data = flatten_xml(elem)
        headers.update(row_data.keys())
        rows.append(row_data)

    headers = sorted(headers)

    # Write the CSV file
    with open(csv_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

# Example usage
xml_file = 'x.xml'
csv_file = 'output.csv'
xml_to_csv(xml_file, csv_file)
