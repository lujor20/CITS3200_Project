import csv
from . import flagging as flag
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

class integrated:

    def __init__(self):
        #rawcsv
        # initiates all the initial data cleaning, using aby modules
        #etl.cleanfile(rawCsv)

        self.initial()
        # set output file as .self
        # report class initialisation success

    def initial(self):
        # call flagging module using the cleaned output file and passing through flagging.py with action as "initial"
        csv_path = os.path.join(dir_path, "test.csv")
        with open( csv_path, newline='') as csvfile:
            
            reader = csv.DictReader(csvfile)
            print("initial flagging")
            
            flag.flagging( csv_path, "initial")
        # report successful initial flagging

    def international():
        # with the cleaned output file, pass it through aby international filtering module, and save as .self
        # pass the international filtered csv and pass it through the flagging module with action as "international"
        # report successful international flagging
        pass

    def distance():
        # with the cleaned output file, pass it through aby duplicate filtering module, and save as .self
        # pass the duplicate filtered csv and pass it through the flagging module with action as "distance"
        # report successful distance flagging
        pass

#test = integrated()