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

        self.rsid_dict = {}

        # Following two arrays hold their respective contents in the sequential order as found by the
        # tool1 extract process

        """
        Following first two arrays display the corresponding "text" and "RSID" of each run
        in sequential order.
        Third array references the "index" of the unique RSID.
        """
        self.txt_array = []
        self.rsid_array = []
        self.rsid_index_array = []


        """Other Document Metadata"""
        self.metadata = {}

    def append_txt(self, txt, rsid_tag):
        """Add rsid to dict if not already in it"""
        if (rsid_tag not in self.rsid_dict):
            index = len(self.rsid_dict)
            rsid = RSID(rsid_tag, index)
            self.rsid_dict[rsid_tag] = rsid
        else:
            index = self.rsid_dict[rsid_tag].index
            rsid = self.rsid_dict[rsid_tag]
        
        """Process data"""
        index2 = len(self.txt_array) # Index in CLASS "RSID" to content

        self.rsid_array.append(rsid_tag)
        self.rsid_index_array.append(index)
        self.txt_array.append(txt)
        
        rsid.append_index(index2)

    def set_settings_rsid(self, settings_rsid):
        self.settings_rsid = settings_rsid

    def append_metadata(self, key, value):
        self.metadata[key] = value

    


class RSID:

    def __init__(self, tag, index):
        self.tag = tag
        self.index_array = []
        self.index = index

    def append_index(self, index):
        self.index_array.append(index)
