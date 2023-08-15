class docx:
    docx_name = None
    rsid_dict = {}

    def __init__(self, document_name):
        self.docx_name = document_name

    def append_rsid(self, rsid_tag, txt):
        """Add rsid to dict if not already in it"""
        if (rsid_tag not in self.rsid_dict):
            rsid = rsid_class(rsid_tag)
            self.rsid_dict[rsid_tag] = rsid
        else:
            rsid = self.rsid_dict[rsid_tag]
        
        """Associate txt with the rsid"""
        if (txt is not None):
            rsid.append_txt(txt)

    def get_text_array(self):
        all_txt = []
        for tag, rsid in self.rsid_dict.items():
            for txt in rsid.txt_array:
                all_txt.append(txt)
        return all_txt

class rsid_class:
    tag = None
    txt_array = []

    def __init__(self, tag):
        self.tag = tag

    def append_txt(self, txt):
        self.txt_array.append(txt)
