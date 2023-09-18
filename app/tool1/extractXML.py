import zipfile
from bs4 import BeautifulSoup
import sys
from docx import Document
from docx_meta import *

class Extract():

    """ Upon initialisation, prepares file for extraction """
    def __init__(self, file):

        """Get the contents of relevant xml files"""
        def get_xml(f, type):
            zip = zipfile.ZipFile(f)
            if type == "document":
                xml_content = zip.read('word/document.xml')
            elif type == "settings":
                xml_content = zip.read('word/settings.xml')
            elif type == "app":
                xml_content = zip.read('docProps/app.xml')
            return xml_content

        """Find and store xml content"""
        self.document_content = get_xml(file, "document")
        self.settings_content = get_xml(file, "settings")
        self.app_content = get_xml(file, "app")
        # xml_tree = self.get_xml_tree(xml_content)

        self.sourcefile = file

    def extract_to_docx(self, docx):
        self.parse_xml(docx, self.document_content)
        self.extractSettingsXML(docx, self.settings_content)
        self.extractAppXML(docx, self.app_content)
        self.extract_metadata(docx,self.sourcefile)

    def parse_xml(self, docx, document_content):
        """Create a function to parse the xml"""
        soup = BeautifulSoup(document_content, 'xml')
        # Gets the text of a particular run
        runCount = 0
        for run in soup.find_all('r'):
            runCount += 1
            try:
                txt = str(run.t.string)
                rsid = run['w:rsidR']
                docx.append_txt(txt, rsid)
            except:
                default_rsidR = run.parent['w:rsidR']
                docx.append_txt(txt, default_rsidR)
        
        docx.append_metadata("Run Count: ", runCount)


    def extractSettingsXML(self, docx, settings_content):
        soup = BeautifulSoup(settings_content, 'xml')
        docx.set_settings_rsid(soup.find_all('rsid'))

        uniqueRun = 0
        for run in soup.find_all('rsid'):
            uniqueRun += 1
        
        docx.append_metadata("Unique Run: ", uniqueRun)


    def extractAppXML(self, docx, app_content):

        soup = BeautifulSoup(app_content, 'xml')
        wordVersion = soup.AppVersion.string
        totalTime = soup.TotalTime.string
        numWords = soup.Words.string
        isDocumentShared = soup.SharedDoc.string
        
        docx.append_metadata(docx.WORD_VERSION, wordVersion)
        docx.append_metadata(docx.TOTAL_TIME, totalTime)
        docx.append_metadata(docx.NUMBER_WORDS, numWords)
        docx.append_metadata(docx.IS_SHARED, isDocumentShared)


    def extract_metadata(self, docx, sourcefile):
        doc = Document(sourcefile)
        
        docx.append_metadata(docx.CREATED_BY, doc.core_properties.author)
        docx.append_metadata(docx.LAST_MODIFIED_BY, doc.core_properties.last_modified_by)
        docx.append_metadata(docx.DATE_CREATED, doc.core_properties.created)
        docx.append_metadata(docx.DATE_LAST_MODIFIED, doc.core_properties.modified)
        docx.append_metadata(docx.REVISIONS, doc.core_properties.revision)
        docx.append_metadata(docx.LAST_PRINTED, doc.core_properties.last_printed)
        docx.append_metadata(docx.TITLE, doc.core_properties.title)
        docx.append_metadata(docx.SUBJECT, doc.core_properties.subject)
        docx.append_metadata(docx.KEYWORDS, doc.core_properties.keywords)
        docx.append_metadata(docx.CATEGORY, doc.core_properties.category)
        docx.append_metadata(docx.COMMENTS, doc.core_properties.comments)
        docx.append_metadata(docx.CONTENT_STATUS, doc.core_properties.content_status)
        docx.append_metadata(docx.IDENTIFIER, doc.core_properties.identifier)
        docx.append_metadata(docx.KEYWORDS, doc.core_properties.keywords)
        docx.append_metadata(docx.LANGUAGE, doc.core_properties.language)
        docx.append_metadata(docx.VERSION, doc.core_properties.version)