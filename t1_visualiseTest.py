from tool1 import *
from docx_meta import *

from app import create_app

app = create_app(debug=True)

if __name__ == "__main__":
    args = sys.argv

    document_name = "hi.docx"
    docx = docx(document_name)

    xml = Extract(document_name)
    parse_xml_to_docx(xml.document_content, docx)

    for x in range(len(docx.txt_array)):
        print('{0:3d}|{1}|{2}'.format(x, docx.rsid_array[x].tag, docx.txt_array[x]))

    for k, v in docx.rsid_dict.items():
        print(k, v.index_array)
    