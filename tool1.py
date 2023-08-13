import zipfile
from bs4 import BeautifulSoup
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

def parse_xml(content):
    """Create a function to parse the xml"""
    soup = BeautifulSoup(content, 'xml')
    # Gets the text of a particular run
    default_rsidR = soup.p['w:rsidR']
    for run in soup.find_all('r'):
        try:
            print(run.t.string)
            print(run['w:rsidR'])
        except:
            print(default_rsidR)

xml = Extract("hi.docx")
parse_xml(xml.document_content)
