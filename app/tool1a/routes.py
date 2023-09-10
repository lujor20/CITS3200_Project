import os
import random
from flask import render_template, jsonify
from werkzeug.utils import secure_filename
from . import tool1a
from .forms import FileForm

from .extractXML import *
from .docx_meta import *

#https://flask-wtf.readthedocs.io/en/1.0.x/form/
@tool1a.route('/visualise1', methods = ['GET', 'POST'])
def visualise():
    form = FileForm()

    if form.validate_on_submit():

        # Extract and process uploaded .docx file
        file = form.file.data
        filename = secure_filename(file.filename)

        docx = DOCX(filename)
        xml = Extract(file)

        xml.extract_to_docx(docx)

        """
        for x in range(len(docx.txt_array)):
        print('{0:3d}|{1}|{2}'.format(x, docx.rsid_array[x], docx.txt_array[x]))
        """
        
        # Prepare data for presentation.
        rsid_array = docx.rsid_array
        txt_array = docx.txt_array
        unique_rsids = docx.rsid_dict.keys()
        rsid_index = docx.rsid_index_array
        
        reds = []
        greens = []
        blues = []

        for rsid in unique_rsids:
            reds.append(random.randint(50, 250))
            greens.append(random.randint(50, 250))
            blues.append(random.randint(50, 250))
            colours = zip(unique_rsids, reds, greens, blues)

        print(docx.metadata)
        return render_template('visualise1.html', form=form, packed = zip(rsid_array, txt_array, rsid_index),
            unique_rsids = unique_rsids, colours = colours, metadata = docx.metadata)

    return render_template('visualise1.html', form=form)




  

