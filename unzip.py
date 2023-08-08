import zipfile
# from lxml import etree
# import pandas as pd

FILE_PATH = 'C:/Users/david/OneDrive/Desktop/Uni/,Third Year Sem 2/Professional Computing/Project/CITS3200_Project'

class Application():
    def __init__(self):
        self.document_content = self.get_xml(f'{FILE_PATH}/hi.docx', 0)
        self.settings_content = self.get_xml(f'{FILE_PATH}/hi.docx', 1)
        # xml_tree = self.get_xml_tree(xml_content)

    def get_xml(self, docx_filename, content):
        with open(docx_filename, "rb") as f:
            zip = zipfile.ZipFile(f)
            if content == 0:
                xml_content = zip.read('word/document.xml')
            else:
                xml_content = zip.read('word/settings.xml')
        return xml_content

    def document_content(self):
        return self.document_content
    
    def settings_content(self):
        return self.settings_content

    # def get_xml_tree(self, xml_string):
    #     return (etree.fromstring(xml_string))

a = Application()
print(a.settings_content)
