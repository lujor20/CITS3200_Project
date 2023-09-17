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

        """ Extract and process uploaded .docx file """
        file = form.file.data
        filename = secure_filename(file.filename)

        docx = DOCX(filename)
        xml = Extract(file)
        xml.extract_to_docx(docx)

   
        
        """ Prepare data for presentation. """
        unique_rsids = list(docx.unique_rsid.keys())

        # Generate colours for each RSID
        reds = []
        greens = []
        blues = []
        for rsid in unique_rsids:
            reds.append(random.randint(50, 250))
            greens.append(random.randint(50, 250))
            blues.append(random.randint(50, 250))
            colours = zip(unique_rsids, reds, greens, blues)

        docx_content = docx.get_zips()
        return render_template('visualise.html', form=form, unique_rsids = unique_rsids,
            colours = colours, metadata = docx.metadata, docx_content = docx_content)

    return render_template('visualise.html', form=form)







