import zipfile
# from lxml import etree
# import pandas as pd

class Extract():
    def __init__(self, filename):
        """Find and store xml content"""
        self.document_content = self.get_xml(filename, "document")
        self.settings_content = self.get_xml(filename, "settings")
        # xml_tree = self.get_xml_tree(xml_content)

    def get_xml(self, docx_filename, type):
        """Get the contents of relevant xml files"""
        with open(docx_filename, "rb") as f:
            zip = zipfile.ZipFile(f)
            if type == "document":
                xml_content = zip.read('word/document.xml')
            else:
                xml_content = zip.read('word/settings.xml')
        return xml_content

    # def get_xml_tree(self, xml_string):
    #     return (etree.fromstring(xml_string))

xml = Extract("hi.docx")
print(xml.document_content)
