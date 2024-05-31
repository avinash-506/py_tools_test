import email
from email import policy
from email.parser import BytesParser
import xml.etree.ElementTree as ET

def eml_to_xml(eml_file_path, xml_file_path):
    # Read and parse the EML file
    with open(eml_file_path, 'rb') as eml_file:
        msg = BytesParser(policy=policy.default).parse(eml_file)
    
    # Create the root XML element
    root = ET.Element("email")
    
    # Helper function to create and append an XML element
    def add_element(parent, tag, text):
        element = ET.SubElement(parent, tag)
        element.text = text
        return element
    
    # Add basic headers to the XML
    add_element(root, "from", msg["from"])
    add_element(root, "to", msg["to"])
    add_element(root, "subject", msg["subject"])
    add_element(root, "date", msg["date"])
    
    # Add the email body
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if part.get_content_maintype() == 'text':
                body = part.get_payload(decode=True).decode(part.get_content_charset(), errors="replace")
                add_element(root, "body", body)
                break  # Assuming we only want the first text part
    else:
        body = msg.get_payload(decode=True).decode(msg.get_content_charset(), errors="replace")
        add_element(root, "body", body)
    
    # Convert the XML structure to a string
    xml_str = ET.tostring(root, encoding='unicode')
    
    # Write the XML to a file
    with open(xml_file_path, 'w', encoding='utf-8') as xml_file:
        xml_file.write(xml_str)

# Example usage
eml_to_xml('email.eml', 'output.xml')
