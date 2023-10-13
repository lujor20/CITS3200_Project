
import haversineDistance as haversine
import flagging as flag
import duplicateClean as dClean
import internationalFilter as international
import IPtoLocation as iptolocation
import initialClean
import copyOutput as cpy

''' 
integrated class is where all backend modules are tyed together and scheduled in correct order. 
this class is also the only point of interraction between front and back end to control the flow of the program.
front end can interract with this module through 3 actions: initial, international, distance.
* initial is the default action, which should be run automatically when a user drag and drops a csv file into the program.
* international is the action to be run when the user wants to analyse international ip's only.
* distance is the action to be run when the user wants to analyse the distance between duplicate id's with different ip's to determine if its feasible to travel between the two locations.

the only file front end should read from is the output.csv file, which is the final output of the program.

for front end to run the program, call the integrated class, and input the csv file name and one of the action as arguments e.g integrated("sample.csv", "initial") '''
class integrated:

    # this is used to determine which action to run depending on action argument
    def __init__(self, rawCsv, action):
        self.rawCsv = rawCsv
        if (action == "initial"):
            self.initial()
        elif (action == "international"):
            self.international()
        elif (action == "distance"):
            self.distance()
        else:
            print("invalid action")

    # this is the default action, which will run the initial analysis on the raw csv file, setting up the staticInternalSave.csv file for the international and distance analysis
    def initial(self):
        initialClean.initialClean(self.rawCsv)
        iptolocation.IPtoLocation('backendData/justIP.csv')
        print("SUCCSSS")
        object = flag.flagging("backendData/ipinformation.csv", "initial")
        cpy.copyOutput("output.csv")

    # this is one of the two optional modules which will take the extracted international IP's and determine if the international code is part of high risk country codes
    def international(self):
        international.findinternational('backendData/staticInternalSave.csv')
        internationalObject = flag.flagging("backendData/international.csv", "international")

    # this is one of the two optional modules which will take the extracted duplicate ips and determine if the last column distance is within the parameters of feasible travel distance
    def distance(self):
        dClean.cleanfile("backendData/staticInternalSave.csv")
        haversine.haversineDistance("backendData/duplicate.csv")
        distanceObject = flag.flagging("backendData/duplicate.csv", "distance")

''' 
use this for internal testing
fyi, for this program to work, it requires preexisting filenames, please ensure such exists before running:
    justIP.csv
    ipinformation.csv
    staticInternalSave.csv
    international.csv
    duplicate.csv
    output.csv

sample.csv is a small csv file which holds enough data and rows to sufficiently test all features of backend
'''
integrated("sample.csv", "distance")
#integrated("sample.csv", "distance")
#integrated("sample.csv", "international")
