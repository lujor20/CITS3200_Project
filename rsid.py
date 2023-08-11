import os
import re
import json
import shutil
from subprocess import PIPE, run
import sys
from zipfile import ZipFile
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from xml.dom import minidom

def main(sourcefile):
    cwd = os.getcwd()
    sourcefile_path = os.path.join(cwd, sourcefile)

    xml_directory = "xml_files"
    xml_files_fullpath = os.path.join(cwd, xml_directory)
    print(xml_files_fullpath)
    try:
        os.mkdir(xml_files_fullpath)
        print(f"New directory '{xml_directory}' created successfully.")
    except OSError as e:
        print(f"Failed to create the directory: {e}")

    with ZipFile(sourcefile_path, 'r') as zObject:
        zObject.extractall(path=xml_files_fullpath)

    for root, dirs, files in os.walk(xml_files_fullpath):
        for filename in files:
            if(filename == "document.xml"):
                full_path_documentxml = os.path.join(root, filename)
                print(f'{full_path_documentxml}')

                # tree = ET.parse(full_path_documentxml)
                # root = tree.getroot()

                # print(root.findall(".//t"))
                # for i in range(3):
                #     print(root[0][0][i][1].text)

                # for child in myroot:
                #     print(child.tag, child.attrib)

                # for r in root.iter('r'):
                #     print(r.text)

                # for text in myroot.findall('w:r'):
                #     t = text.find('w:t').text
                #     print(t)

                # Textpattern = r'<w:t>.*</w:t>'
                # rsidPattern = r'w:rsidR="(.{8})"'

                # with open(full_path_documentxml, 'r') as file:
                #     content = file.read()
                #     matches = re.findall(Textpattern, content)
                #     for match in matches:
                #         print(f"{match}")
                    
                #     rsidMatches = re.findall(rsidPattern, content)
                #     for rsidMatch in rsidMatches:
                #         print(f"{rsidMatch}")


                with open(full_path_documentxml, 'r') as fp:
                    soup = BeautifulSoup(fp, 'xml')
                
                # print(soup.get_text())
                # print(soup.find_all('r'))
                p_tag = soup.r

                print(p_tag.contents[1])

                # # Reading the data inside the xml file to a variable under the name  data
                # with open(full_path_documentxml, 'r') as f:
                #     data = f.read() 

                # # Passing the stored data inside the beautifulsoup parser 
                # bs_data = BeautifulSoup(data, 'xml') 

                # # Finding all instances of tag   
                # b_unique = bs_data.find_all('w:r w:rsidR') 
                # print(b_unique) 

                # # Using find() to extract attributes of the first instance of the tag 
                # b_name = bs_data.find('w:rsid', {'w:val':'00082485'}) 
                # print(b_name) 

                # # Extracting the data stored in a specific attribute of the `child` tag 
                # value = b_name.get('qty') 
                # print(value)

if __name__=="__main__":
    args = sys.argv
    if len(args) != 2:
        raise Exception("You must pass one argument only!")
    
    sourcefile = args[1]
    main(sourcefile)