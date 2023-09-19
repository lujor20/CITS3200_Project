import zipfile
from bs4 import BeautifulSoup
import sys
from docx import Document
from docx_meta import *

class Extract():
    def __init__(self, filename):
        """Find and store xml content"""
        self.document_content = self.get_xml(filename, "document")
        self.settings_content = self.get_xml(filename, "settings")
        self.app_content = self.get_xml(filename, "app")
        # xml_tree = self.get_xml_tree(xml_content)

    def get_xml(self, docx_filename, type):
        """Get the contents of relevant xml files"""
        with open(docx_filename, "rb") as f:
            zip = zipfile.ZipFile(f)
            if type == "document":
                xml_content = zip.read('word/document.xml')
            elif type == "settings":
                xml_content = zip.read('word/settings.xml')
            elif type == "app":
                xml_content = zip.read('docProps/app.xml')
        return xml_content



def parse_xml(content):
    print("|    RSID value and its corresponding text   |")
    runCount = 0
    """Create a function to parse the xml"""
    soup = BeautifulSoup(content, 'xml')
    # Gets the text of a particular run
    for run in soup.find_all('r'):
        runCount += 1
        try:
            txt = str(run.t.string)
            rsid = run['w:rsidR']
            print(rsid, "|" + txt + "|")
        except:
            default_rsidR = run.parent['w:rsidR']
            print(default_rsidR, "|" + txt + "|")
    
    print("Run count: ", runCount)
    print(" ")


def extractSettingsXML(content):
    print("|    Unique RSIDs in Settings.xml   |")
    soup = BeautifulSoup(content, 'xml')
    for run in soup.find_all('rsid'):
        print(run['w:val'])
    print(" ")



def extractAppXML(content):
    print("|    Metadata from App.xml   |")
    soup = BeautifulSoup(content, 'xml')
    wordVersion = soup.AppVersion.string
    totalTime = soup.TotalTime.string
    numWords = soup.Words.string
    isDocumentShared = soup.SharedDoc.string
    print("Word Version: ", wordVersion)
    print("Total Time: ", totalTime)
    print("Number of words: ", numWords)
    print("The document is shared: ", isDocumentShared)
    print(" ")


def extract_metadata(sourcefile):
    print("|    Metadata from core.xml  |")

    doc = Document(sourcefile)
    
    metadata = {
        "Created By": doc.core_properties.author,
        "Last Modified By": doc.core_properties.last_modified_by,
        "Date Created": doc.core_properties.created,
        "Date Last Modified": doc.core_properties.modified,
        "Revisions": doc.core_properties.revision,
        "Last Printed": doc.core_properties.last_printed,
        "Title": doc.core_properties.title,
        "Subject": doc.core_properties.subject,
        "Keywords": doc.core_properties.keywords,
        "Category": doc.core_properties.category,
        "Comments": doc.core_properties.comments,
        "Content Status": doc.core_properties.content_status,
        "Identifier": doc.core_properties.identifier,
        "Keywords": doc.core_properties.keywords,
        "Language": doc.core_properties.language,
        "Version": doc.core_properties.version,
    }
    
    for key, value in metadata.items():
        print(f"{key}: {value}")
    print(" ")



def main(sourcefile):
    """Extracts the xml data"""
    xml = Extract(sourcefile)

    parse_xml(xml.document_content)
    extractAppXML(xml.app_content)
    extract_metadata(sourcefile)
    extractSettingsXML(xml.settings_content)


if __name__=="__main__":
    args = sys.argv
    if len(args) != 2:
        raise Exception("Usage: python rsid.py <docx file path>")
    
    sourcefile = args[1]
    main(sourcefile)