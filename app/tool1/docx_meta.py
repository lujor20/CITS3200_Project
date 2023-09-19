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
        self.num_runs = 0
        self.metadata = {}

        self.properties_dict = {}

    def append_txt(self, paragraph_id, rsid_tag, properties_array, txt):
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
        run_index = self.num_runs
        paragraph.append_txt2(txt, rsid_tag, index, run_index)
        self.append_properties(properties_array, run_index)
        self.num_runs += 1
    
    def append_properties(self, properties_array, run_index):
        for prop in properties_array:
            hashed = hash(prop.xml)
            if hashed not in self.properties_dict:
                self.properties_dict[hashed] = prop
                prop.append_run(run_index, prop.inherit_from)
            else:
                docxProp = self.properties_dict[hashed]
                docxProp.append_run(run_index, prop.inherit_from)

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

    def get_properties_dict(self):
        return self.properties_dict

    

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
        self.run_index_array = []

    def append_txt2(self, txt, rsid, rsid_index, run_index):
        self.txt_array.append(txt)
        self.rsid_array.append(rsid)
        self.rsid_index_array.append(rsid_index)
        self.run_index_array.append(run_index)

    def get_zip(self):
        return zip(self.txt_array, self.rsid_array, self.rsid_index_array)
        
class PROPERTY:
    """ inherit_from values """
    SELF        = 0
    PARENT      = 1
    GRANDPARENT = 2

    def __init__(self, xml, name, value_dict, inherit_from):
        self.xml = xml
        self.name = name
        self.value_dict = value_dict
        self.inherit_from = inherit_from

        self.runs = []
        self.inheritance_array = []

    def append_run(self, run_index, inherit_value):
        self.runs.append(run_index)

        