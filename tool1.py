import zipfile
from bs4 import BeautifulSoup
import sys

from docx_meta import *

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

def parse_xml(content):
    """Create a function to parse the xml"""
    soup = BeautifulSoup(content, 'xml')
    # Gets the text of a particular run
    default_rsidR = soup.p['w:rsidR']
    for run in soup.find_all('r'):
        try:
            txt = str(run.t.string)
            rsid = run['w:rsidR']
            print(rsid, "|" + txt + "|")
        except:
            print(default_rsidR, "|" + txt + "|")

def parse_xml_to_docx(content, docx):
    """Create a function to parse the xml to docx class"""
    soup = BeautifulSoup(content, 'xml')
    # Gets the text of a particular run
    default_rsidR = soup.p['w:rsidR']
    for run in soup.find_all('r'):
        try:
            txt = str(run.t.string)
            rsid = run['w:rsidR']
            docx.append_txt(txt, rsid)
        except:
            docx.append_txt(txt, default_rsidR)


def main(sourcefile):
    """Extracts the xml data"""
    xml = Extract(sourcefile)
    parse_xml(xml.document_content)

if __name__=="__main__":
    args = sys.argv
    if len(args) != 2:
        raise Exception("Usage: python rsid.py <docx file path>")
    
    sourcefile = args[1]
    main(sourcefile)