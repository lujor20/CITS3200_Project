import csv
import shutil
import os

class main:

    ## initialising file as object
    def __init__(self, path):
        try:
            with open(path) as file:
                self.openFile = csv.reader(file)
            self.filePath = path
            print("Success")
            self.duplicate('copyCSV.txt')
        except Exception as e:
            print("path didnt work: {e}")

    def duplicate(self, dst):
        try:
            shutil.copy(self.filePath, dst)
            print("copy success")
        except:
            print("could not copy file")


        

test = main('example LMS test log.csv')


print(os.getcwd())



