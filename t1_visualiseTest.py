from tool1 import *
from docx_meta import *

if __name__ == "__main__":
    document_name = "hi.docx"
    docx = docx(document_name)

    xml = Extract(document_name)
    parse_xml_to_docx(xml.document_content, docx)

    print(docx.rsid_dict.keys())
    print("".join(docx.get_text_array()))