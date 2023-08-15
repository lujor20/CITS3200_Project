class docx:
  docx_name = None
  rsid_array = []

  def __init__(self, document_name):
    self.docx_name = document_name
    self.rsid_array = []

  def append_rsid(rsid):
    self.rsid_array.append(rsid)

  def get_text_array:
    txt = []
    for (rsid in rsid_array):
      text_array = rsid.text_array
      for (text in text_array):
        txt.append(text)
    return txt

class rsid:
  tag = None
  text_array = []

  def __init__(self, tag):
    self.tag = tag

  def append_text(text):
    self.text_array.append(text)
