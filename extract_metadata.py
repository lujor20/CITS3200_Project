import os
import sys
from docx import Document

def extract_metadata(docx_path):
    doc = Document(docx_path)
    
    metadata = {
        "Created By": doc.core_properties.author,
        "Last Modified By": doc.core_properties.last_modified_by,
        "Date Created": doc.core_properties.created,
        "Date Last Modified": doc.core_properties.modified,
        "Revisions": doc.core_properties.revision,
        "Last Printed": doc.core_properties.last_printed,
        "Title": doc.core_properties.title,
        "Subject": doc.core_properties.subject,
        "Keywords": doc.core_properties.keywords,
        "Category": doc.core_properties.category,
        "Comments": doc.core_properties.comments,
        "Content Status": doc.core_properties.content_status,
        "Identifier": doc.core_properties.identifier,
        "Keywords": doc.core_properties.keywords,
        "Language": doc.core_properties.language,
        "Version": doc.core_properties.version,
    }
    
    return metadata


if __name__=="__main__":
    args = sys.argv
    if len(args) != 2:
        raise Exception("Usage: python extract_metadata.py <docx file path>")
    
    sourcefile = args[1]

    cwd = os.getcwd()
    docx_path = os.path.join(cwd, sourcefile)

    metadata = extract_metadata(docx_path)
    for key, value in metadata.items():
        print(f"{key}: {value}")


