import csv
import shutil
import os

class Main:

    ## initialising file as object
    def __init__(self, path):
        try:
            with open(path) as file:
                self.openFile = csv.reader(file)
            self.filePath = path
            print("Success")
            self.duplicate('copyCSV.txt')
        except Exception as e:
            print(f"path didnt work: {e}")

    ## create duplicate file
    def duplicate(self, dst):
        try:
            shutil.copy(self.filePath, dst)
            print("copy success")
        except Exception as e:
            print(f"could not copy file: {e}")


        

test = Main('example LMS test log.csv')


print(os.getcwd())



