class DOCX:
    def __init__(self, document_name):
        self.docx_name = document_name

        self.rsid_dict = {}

        # Following two arrays hold their respective contents in the sequential order as found by the
        # tool1 extract process

        # Array of txt in "runs" in document, in sequential order"
        self.txt_array = []
        # Respective RSID of txt
        self.rsid_array = []
        # Index of rsid in "list of unique rsids".
        self.rsid_index_array = []
        
        

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



class RSID:

    def __init__(self, tag, index):
        self.tag = tag
        self.index_array = []
        self.index = index

    def append_index(self, index):
        self.index_array.append(index)
