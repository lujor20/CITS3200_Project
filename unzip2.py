import zipfile
# from lxml import etree
# import pandas as pd

FILE_PATH = 'C:/Users/david/OneDrive/Desktop/Uni/,Third Year Sem 2/Professional Computing/Project/CITS3200_Project'

class Application():
    def __init__(self):
        self.xml_content = self.get_word_xml(f'{FILE_PATH}/hi.docx') 
        # xml_tree = self.get_xml_tree(xml_content)

    def get_word_xml(self, docx_filename):
        with open(docx_filename, "rb") as f:
            zip = zipfile.ZipFile(f)
            xml_content = zip.read('word/document.xml')
        return xml_content

    def xml_content(self):
        return(self.xml_content)

a = Application()
print(a.xml_content)
