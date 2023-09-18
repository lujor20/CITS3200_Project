import Cits3200etl as etl
import csv
import flagging as flag


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
        with open("test.csv", newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            print("initial flagging")
            
            object = flag.flagging("test.csv", "initial")
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

test = integrated()