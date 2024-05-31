import xml.etree.ElementTree as ET
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import re

def sanitize_header(header_value):
    """Sanitize the header to remove any linefeed or carriage return characters."""
    return re.sub(r'[\r\n]', '', header_value)

def xml_to_eml(xml_path, eml_path):
    # Parse the XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Create a new multipart email message
    multipart_msg = MIMEMultipart()

    # Extract headers from the XML
    headers = ['from', 'to', 'subject', 'date']
    for header in headers:
        element = root.find(header)
        if element is not None and element.text:
            sanitized_header = sanitize_header(element.text)
            multipart_msg[header.capitalize()] = sanitized_header

    # Extract the body
    body_element = root.find('body')
    if body_element is not None and body_element.text:
        body = body_element.text
        # Add the body as a MIMEText part
        text_part = MIMEText(body, 'plain', 'utf-8')
        multipart_msg.attach(text_part)

    # Handle any additional parts if present (e.g., attachments)
    parts = root.find('Parts')
    if parts is not None:
        for part in parts.findall('Part'):
            content_type = part.find('ContentType').text
            content = part.find('Content').text
            if content_type.startswith('text'):
                charset = part.find('charset')
                charset = charset.text if charset is not None else 'utf-8'
                text_part = MIMEText(content, _subtype=content_type.split('/')[1], _charset=charset)
                multipart_msg.attach(text_part)
            elif part.find('Attachment') is not None:
                filename = part.find('Attachment').get('filename')
                attachment_content = part.find('Attachment').text
                attachment = MIMEApplication(attachment_content, _subtype=content_type.split('/')[1])
                attachment.add_header('Content-Disposition', 'attachment', filename=filename)
                multipart_msg.attach(attachment)
            else:
                mime_part = MIMEApplication(content, _subtype=content_type.split('/')[1])
                multipart_msg.attach(mime_part)

    # Write the EML file
    with open(eml_path, 'wb') as f:
        f.write(multipart_msg.as_bytes())

# Usage
xml_path = 'data.xml'
eml_path = 'output_file.eml'
xml_to_eml(xml_path, eml_path)
