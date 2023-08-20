from tool1 import *
from docx_meta import *

from app import create_app

app = create_app(debug=True)

if __name__ == "__main__":
    args = sys.argv

    #document_name = "3970_Part_I_Aviation_Thesis.docx"
    document_name = "hi.docx"
    docx = docx(document_name)

    xml = Extract(document_name)
    parse_xml_to_docx(xml.document_content, docx)

    if args[1 % len(args)] == "list":
        for x in range(len(docx.txt_array)):
            print('{0:3d}|{1}|{2}'.format(x, docx.rsid_array[x], docx.txt_array[x]))
    else:
        for k, v in docx.rsid_dict.items():
            print(k, v.index_array)
    