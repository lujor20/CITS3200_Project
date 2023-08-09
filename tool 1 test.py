import csv
import shutil

class main:


    def __init__(self, path):
        try:
            with open(path) as file:
                self.openFile = csv.reader(file)
            print("Success")
        except Exception as e:
            print("path didnt work: {e}")

    def duplicate(src, dst):
        

            

test = main('example LMS test log.csv')