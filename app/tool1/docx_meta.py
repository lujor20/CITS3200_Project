class DOCX:
    """
    Variables for keyname in meta_dict
    """
    WORD_VERSION        = "Word Version"
    TOTAL_TIME          = "Total Time Spent"
    NUMBER_WORDS        = "Number of Words"
    CREATED_BY          = "Created By"
    LAST_MODIFIED_BY    = "Last Modified By"
    DATE_CREATED        = "Date Created"
    DATE_LAST_MODIFIED  = "Date Lasted Modified"
    REVISIONS           = "Number of Revisions"
    LAST_PRINTED        = "Last Printed"
    TITLE               = "Title"
    SUBJECT             = "Subject"
    KEYWORDS            = "Keywords"
    CATEGORY            = "Category"
    COMMENTS            = "Comments"
    CONTENT_STATUS      = "Content Status"
    IDENTIFIER          = "Identifier"
    KEYWORDS            = "Keywords"
    LANGUAGE            = "Language"
    VERSION             = "Version"
 

    def __init__(self, document_name):
        self.docx_name = document_name

        self.unique_rsid = {}
        self.paragraphs = {}


        self.metadata = {}

    def append_txt(self, paragraph_id, txt, rsid_tag):
        """Get corresponding paragraph"""
        if (paragraph_id not in self.paragraphs):
            paragraph = PARAGRAPH(paragraph_id)
            self.paragraphs[paragraph_id] = paragraph
        else:
            paragraph = self.paragraphs[paragraph_id]

        """Get rsid index"""
        if (rsid_tag not in self.unique_rsid):
            index = len(self.unique_rsid)
            rsid = RSID(rsid_tag, index)
            self.unique_rsid[rsid_tag] = rsid
        else:
            index = self.unique_rsid[rsid_tag].index
        
        """Process data"""
        paragraph.append_txt2(txt, rsid_tag, index)

    def set_settings_rsid(self, settings_rsid):
        self.settings_rsid = settings_rsid

    def append_metadata(self, key, value):
        self.metadata[key] = value

    def get_zips(self):
        zips = []
        for key, paragraph in self.paragraphs.items():
            zip1 = paragraph.get_zip()
            zips.append(zip1)
        return zips

    


class RSID:
    def __init__(self, tag, index):
        self.tag = tag
        self.index = index


class PARAGRAPH:
    def __init__(self, id):
        self.id = id
        self.txt_array = []
        self.rsid_array = []
        self.rsid_index_array = []

    def append_txt2(self, txt, rsid, rsid_index):
        self.txt_array.append(txt)
        self.rsid_array.append(rsid)
        self.rsid_index_array.append(rsid_index)

    def get_zip(self):
        return zip(self.txt_array, self.rsid_array, self.rsid_index_array)
