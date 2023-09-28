import re
from .docx_meta import *
from .extractXML import *
from werkzeug.utils import secure_filename

class ANALYSE:
  DOCX_REGEX = ".*.docx$"

  def __init__(self, array_files):
    self.failed_files = []
    array_files = self.filter_for_docx(array_files)
    print(len(array_files), "this is the length of the array_files")
    array_docx = self.turn_into_DOCX(array_files)
    print(len(array_docx), "this is the length of the array_docx")
    self.array_docx_data = self.get_docx_data(array_docx)
    print(len(self.array_docx_data), "this is the length of the docx_data array")

    



  def filter_for_docx(self, array_files):
    docx = []
    for file in array_files:
      if re.search(ANALYSE.DOCX_REGEX, file.filename):
        print(file)
        docx.append(file)
      else:
        filename = secure_filename(file.filename)
        self.failed_files.append(filename)
    return docx

  def turn_into_DOCX(self, array_files):
    array_docx = []
    for file in array_files:
      filename = secure_filename(file.filename)
      try:
        docx = DOCX(filename)
        extract = Extract(file)
        extract.extract_to_docx(docx)
        array_docx.append(docx)
      except:
        self.failed_files.append(filename)

    return array_docx
  
  def get_docx_data(self, array_docx):
    array_docx_data = []
    for docx in array_docx:
      docx_data = DOCX_DATA(docx)
      array_docx_data.append(docx_data)
    return array_docx_data

  def get_dict_average_char_per_unique_rsid(self):
    averages = {}
    #potentail source of bugs filename as unique
    for docx_data in self.array_docx_data:
      docx_name = docx_data.docx_name
      averages[docx_name] = docx_data.average_num_char_per_unique_rsid
    return averages

  def get_dict_average_char_per_run(self):
    averages = {}
    #potentail source of bugs filename as unique
    for docx_data in self.array_docx_data:
      docx_name = docx_data.docx_name
      averages[docx_name] = docx_data.average_num_char_per_run
    return averages






class DOCX_DATA:
  # Potential statistics
  # Average characters per unique RSID
  # Average characters per Run

  def __init__(self, docx):
    self.docx_name = docx.docx_name
    self.average_num_char_per_unique_rsid = self.get_average_num_char_per_unique_rsid(docx)
    self.average_num_char_per_run = self.get_average_num_char_per_run(docx)


  def get_average_num_char_per_unique_rsid(self, docx):
    num_rsids = len(list(docx.unique_rsid))
    total_char = 0
    for key, paragraph in docx.paragraphs.items():
      txt_array = paragraph.txt_array
      for txt in txt_array:
        total_char += len(txt)
    
    if (num_rsids > 0):
      average = total_char / num_rsids
      return average
    else:
      return 0


  def get_average_num_char_per_run(self, docx):
    total_char = 0
    for key, paragraph in docx.paragraphs.items():
      txt_array = paragraph.txt_array
      for txt in txt_array:
        total_char += len(txt)
    num_run = docx.num_runs

    if (num_run > 0):
      average = total_char / num_run
      return average
    else:
      return 0


  
