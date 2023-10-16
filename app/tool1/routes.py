import os
import random
from flask import render_template, jsonify, request
from werkzeug.utils import secure_filename
from . import tool1
from .forms import FileForm, MultipleFileForm

from .extractXML import *
from .docx_meta import *
from .analyse import *

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
        colours = []
        for rsid in unique_rsids:
            reds.append(random.randint(50, 250))
            greens.append(random.randint(50, 250))
            blues.append(random.randint(50, 250))
            colours = zip(unique_rsids, reds, greens, blues)

        # Get the content of the DOCX
        docx_content = docx.get_zips()

        # Get the properties
        docx_content_properties_array = []
        docx_content_properties_dict = docx.get_properties_dict()
        # turn into dictionary for jinja2 processing
        for hash, prop in docx_content_properties_dict.items():
            temp = dict()
            temp["xml"]               = str(prop.xml)
            temp["name"]              = prop.name
            temp["value_dict"]        = prop.value_dict
            temp["runs"]              = prop.runs
            temp["inheritance_array"] = prop.inheritance_array
            docx_content_properties_array.append(temp)

        # Quick analysis - see if average exceeds threshold
        docx_stat = DOCX_DATA(docx)
        if docx_stat.average_num_char_per_unique_rsid < 200:
            heading = "Average number of characters per RSID"
        else:
            heading = "Average number of characters per RSID (Suspicious)"
        docx.metadata[heading] = docx_stat.average_num_char_per_unique_rsid
        if docx_stat.average_num_char_per_run < 120:
            heading = "Average number of characters per Run"
        else:
            heading = "Average number of characters per Run (Suspicious)"
        docx.metadata[heading] = docx_stat.average_num_char_per_run
        
        return render_template('visualise.html', form=form, unique_rsids = unique_rsids,
            colours = colours, metadata = docx.metadata, docx_content = docx_content,
            docx_content_properties_array = docx_content_properties_array)

    return render_template('visualise.html', form=form)

@tool1.route('/analyse', methods = ['GET', 'POST'])
def analyse():
    multipleForm = MultipleFileForm()

    if multipleForm.validate_on_submit():
        # List of files
        files = request.files.getlist(multipleForm.multipleFile.name)
        analysis = ANALYSE(files)

        char_per_unique_rsid = analysis.get_dict_char_per_unique_rsid()
        char_per_run = analysis.get_dict_char_per_run()
        print(char_per_run)

        return render_template('analyse.html', multipleForm = multipleForm,
        char_per_unique_rsid=char_per_unique_rsid,
        char_per_run=char_per_run)
    #https://stackoverflow.com/questions/53021662/multiplefilefield-wtforms

    return render_template('analyse.html', multipleForm = multipleForm)



