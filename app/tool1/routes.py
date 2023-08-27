import os
import random
from flask import render_template, jsonify
from werkzeug.utils import secure_filename
from . import tool1
from .forms import FileForm

from .extractXML import *
from .docx_meta import *

#https://flask-wtf.readthedocs.io/en/1.0.x/form/
@tool1.route('/visualise', methods = ['GET', 'POST'])
def visualise():
  form = FileForm()

  if form.validate_on_submit():
    file = form.file.data
    filename = secure_filename(file.filename)

    docx = DOCX(filename)
    xml = Extract(file)

    parse_xml_to_docx(xml.document_content, docx)

    """
    for x in range(len(docx.txt_array)):
      print('{0:3d}|{1}|{2}'.format(x, docx.rsid_array[x], docx.txt_array[x]))
    """
    
    rsid_array = docx.rsid_array
    txt_array = docx.txt_array

    rsids = []
    reds = []
    greens = []
    blues = []

    for rsid in docx.rsid_dict:
      rsids.append(rsid)
      reds.append(random.randint(50, 250))
      greens.append(random.randint(50, 250))
      blues.append(random.randint(50, 250))
    colours = zip(rsids, reds, greens, blues)
    return render_template('visualise.html', form=form, packed = zip(rsid_array, txt_array), rsids = rsids, colours = colours)

  return render_template('visualise.html', form=form)

"""Function to serve request for RSID and Text."""
@tool1.route("/get_rsid", methods = ['POST'])
def get_rsid():
  data = t1_visualiseTest.givedata()
  return jsonify(data)






  

