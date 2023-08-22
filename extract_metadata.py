import os
import sys
from docx import Document

def extract_metadata(docx_path):
    doc = Document(docx_path)
    
    metadata = {
        "Title": doc.core_properties.title,
        "Author": doc.core_properties.author,
        "Subject": doc.core_properties.subject,
        "Keywords": doc.core_properties.keywords,
        "Last Modified By": doc.core_properties.last_modified_by,
        "Created": doc.core_properties.created,
        "Modified": doc.core_properties.modified,
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


