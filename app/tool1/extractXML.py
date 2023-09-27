import zipfile
from bs4 import BeautifulSoup
import sys
from docx import Document
from .docx_meta import *

from html import escape

class Extract():

    # .docx XML tags for respective ele,emts
    BODY_TAG                   = "w:body"
    PARAGRAPH_TAG              = "p"
    PARAGRAPH_PROPERTY_TAG     = "pPr"
    RUN_TAG                    = "r"
    RUN_PROPERTY_TAG           = "rPr"
    HYPERLINK_TAG              = "hyperlink"
    TEXT_TAG                   = "t"
    RSIDR_PROPERTY             = "w:rsidR"
    PARAGRAPH_ID_PROPERTY      = "w14:paraId"
    

    MISSING_RSID_REPLACEMENT            = "None"
    MISSING_PARAGRAPH_ID_REPLACEMENT    = "None"

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

        # Have beuatifulSoup process .docx xml.
        soup = BeautifulSoup(document_content, 'xml')

        # Ge the body of the xml
        body = soup.find(Extract.BODY_TAG)

        """ Iterate through the body's children """
        for child in body.children:
            # Skip branches that don't represent paragraphs.
            if child.name != Extract.PARAGRAPH_TAG:
                print("skipping" + child.name)
                continue 

            # Set Default values
            if Extract.RSIDR_PROPERTY not in child.attrs:
                default_rsid = Extract.MISSING_RSID_REPLACEMENT
            else:
                default_rsid = child[Extract.RSIDR_PROPERTY]

            if Extract.PARAGRAPH_ID_PROPERTY not in child.attrs:
                paragraph_id = Extract.MISSING_PARAGRAPH_ID_REPLACEMENT
            else:
                paragraph_id = child[Extract.PARAGRAPH_ID_PROPERTY]
            
            
            paragraph_property = child.find(Extract.PARAGRAPH_PROPERTY_TAG)
            if (paragraph_property is None):
                default_properties = []
            else:
                default_properties = self.parse_tagPr(paragraph_property, PROPERTY.PARENT)

            # Iterate through the child of <p>
            for gchild in child.children:

                if gchild.name == Extract.RUN_TAG:
                    self.parse_tagr(docx, gchild, paragraph_id, default_rsid, default_properties)
                elif gchild.name == Extract.HYPERLINK_TAG:
                    run_tag = gchild.find(Extract.RUN_TAG)
                    if run_tag is not None:
                        self.parse_tagr(docx, run_tag, paragraph_id, default_rsid, default_properties)
                else:
                    print(paragraph_id, "skipping", gchild.name)
                    continue

    """
    Given a beautifulsoup4 object corresponding to a .docx <w:pPr> or <w:rPr> tag,
    returns an array of the tag's children as class PROPERTY objects.
    """
    def parse_tagPr(self, tagPr, inherit_from = PROPERTY.GRANDPARENT):
        properties = []
        for child in tagPr.children:
            name = child.name
            value_dict = child.attrs
            new_property = PROPERTY(child, name, value_dict, inherit_from)
            properties.append(new_property)
        return properties

    """
    Given a beautifulsoup4 object corresponding to .docx <w:r> tag,
    processes the tag to appropriately call the docx class method
    "append_text".
    """
    def parse_tagr(self, docx, tagr, paragraph_id, default_rsid, default_properties):
        # get text
        tagr_t = tagr.find(Extract.TEXT_TAG)
        if tagr_t is None:
            return
        else:
            txt = tagr_t.string

        # get rsidR
        if Extract.RSIDR_PROPERTY not in tagr.attrs:
            rsid = default_rsid
        else:
            rsid = tagr[Extract.RSIDR_PROPERTY]

        # get run property
        property_tag = tagr.find(Extract.RUN_PROPERTY_TAG)
        if property_tag is not None:
            tagr_properties = self.parse_tagPr(property_tag, PROPERTY.SELF)
        else:
            tagr_properties = default_properties

        # finally add to docx
        docx.append_txt(paragraph_id, rsid, tagr_properties, txt)
        

    def extractSettingsXML(self, docx, settings_content):
        soup = BeautifulSoup(settings_content, 'xml')
        docx.set_settings_rsid(soup.find_all('rsid'))

        uniqueRun = 0
        for run in soup.find_all('rsid'):
            uniqueRun += 1
        
        docx.append_metadata("Unique Run: ", uniqueRun)


    def extractAppXML(self, docx, app_content):

        soup = BeautifulSoup(app_content, 'xml')

        # Incredibly lazy
        def lazy_try (tag, property_string):
            try:
                string = tag.string
                docx.append_metadata(property_string, string)
            except:
                print("Could not find", property_string)
                
        
        lazy_try(soup.AppVersion, docx.WORD_VERSION)
        lazy_try(soup.TotalTime, docx.TOTAL_TIME)
        lazy_try(soup.Words, docx.NUMBER_WORDS)
        lazy_try(soup.SharedDoc, docx.IS_SHARED)
        
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