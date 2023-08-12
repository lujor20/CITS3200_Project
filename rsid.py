import os
import sys
from zipfile import ZipFile
from bs4 import BeautifulSoup

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

                with open(full_path_documentxml, 'r') as fp:
                    soup = BeautifulSoup(fp, 'xml')
                
                '''Gets the text of a particular run'''
                default_rsidR = soup.p['w:rsidR']
                for run in soup.find_all('r'):
                    try:
                        print(run.t.string)
                        print(run['w:rsidR'])
                        
                    except:
                        print(default_rsidR)

if __name__=="__main__":
    args = sys.argv
    if len(args) != 2:
        raise Exception("Usage: python rsid.py <docx file path>")
    
    sourcefile = args[1]
    main(sourcefile)