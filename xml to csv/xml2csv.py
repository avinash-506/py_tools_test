import xml.etree.ElementTree as ET
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

def xml_to_eml(xml_path, eml_path):
    # Parse the XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Create a new email message
    msg = EmailMessage()

    # Extract headers from the XML
    for child in root:
        if child.tag not in ["Parts", "Part"]:
            msg[child.tag] = child.text

    # Initialize a multipart message
    multipart_msg = MIMEMultipart()
    for header, value in msg.items():
        multipart_msg[header] = value

    # Extract and add parts
    parts = root.find('Parts')
    if parts is not None:
        for part in parts.findall('Part'):
            content_type = part.find('ContentType').text
            content = part.find('Content').text
            if content_type.startswith('text'):
                charset = part.find('charset')
                if charset is not None:
                    charset = charset.text
                else:
                    charset = 'utf-8'
                text_part = MIMEText(content, _subtype=content_type.split('/')[1], _charset=charset)
                multipart_msg.attach(text_part)
            elif part.find('Attachment') is not None:
                filename = part.find('Attachment').get('filename')
                attachment_content = part.find('Attachment').text
                attachment = MIMEApplication(attachment_content, _subtype=content_type.split('/')[1])
                attachment.add_header('Content-Disposition', 'attachment', filename=filename)
                multipart_msg.attach(attachment)
            else:
                # If it's a non-text part but not an attachment, treat it as a raw MIME part
                mime_part = MIMEApplication(content, _subtype=content_type.split('/')[1])
                multipart_msg.attach(mime_part)
    
    # Write the EML file
    with open(eml_path, 'wb') as f:
        f.write(multipart_msg.as_bytes())

# Usage
xml_path = 'path_to_xml_file.xml'
eml_path = 'output_file.eml'
xml_to_eml(xml_path, eml_path)
