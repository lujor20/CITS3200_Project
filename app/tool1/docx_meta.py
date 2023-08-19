class DOCX:
    def __init__(self, document_name):
        self.docx_name = document_name

        self.rsid_dict = {}

        # Following two arrays hold their respective contents in the sequential order as found by the
        # tool1 extract process

        self.rsid_array = []
        self.txt_array = []

    def append_txt(self, txt, rsid_tag):
        """Add rsid to dict if not already in it"""
        if (rsid_tag not in self.rsid_dict):
            rsid = RSID(rsid_tag)
            self.rsid_dict[rsid_tag] = rsid
        else:
            rsid = self.rsid_dict[rsid_tag]
        
        """Process data"""
        index = len(self.txt_array) # Index of appended content

        self.rsid_array.append(rsid_tag)
        self.txt_array.append(txt)

        rsid.append_index(index)



class RSID:

    def __init__(self, tag):
        self.tag = tag
        self.index_array = []

    def append_index(self, index):
        self.index_array.append(index)
