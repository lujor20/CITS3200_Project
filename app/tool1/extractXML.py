import zipfile
from bs4 import BeautifulSoup
import sys

from .docx_meta import *

class Extract():
    def __init__(self, file):
        """Find and store xml content"""
        self.document_content = self.get_xml(file, "document")
        self.settings_content = self.get_xml(file, "settings")
        # xml_tree = self.get_xml_tree(xml_content)

    def get_xml(self, f, type):
        """Get the contents of relevant xml files"""
        zip = zipfile.ZipFile(f)
        if type == "document":
            xml_content = zip.read('word/document.xml')
        else:
            xml_content = zip.read('word/settings.xml')
        return xml_content

def parse_xml_to_docx(content, docx):
    """Create a function to parse the xml to docx class"""
    soup = BeautifulSoup(content, 'xml')
    # Gets the text of a particular run
    default_rsidR = soup.p['w:rsidR']
    for run in soup.find_all('r'):
        try:
            txt = str(run.t.string)
        except:
            continue
            
        try:
            rsid = run['w:rsidR']
            docx.append_txt(txt, rsid)
        except:
            docx.append_txt(txt, default_rsidR)