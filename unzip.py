from zipfile import ZipFile

def unzipfile(filename):
    """Unzips docx files and store in current directory"""
    with ZipFile(filename, 'r') as doc_file:
        doc_file.extractall(path="C:\Users\david\OneDrive\Desktop\Uni\,Third Year Sem 2\Professional Computing\Project\CITS3200_Project")
    doc_file.close()

unzipfile("hi.docx")