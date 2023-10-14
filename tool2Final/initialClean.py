import pandas as pd
import csv

'''
this class is used for removing all unnecessary columns fromt he rows of the drag/dropped csv file.
it will remove all columns except for the ones that contain the ip address and the id of the user.
this class takes one argument, which is the name of the csv file to be cleaned, and outputs a "justIP.csv" file which will contain only the id and ip address of the user respectively.
'''

class initialClean:

    def __init__(self, inputFile):
        file = pd.read_csv(inputFile)
        with open('backendData/justIP.csv', 'w', newline='') as outputfile:
            writer = csv.writer(outputfile, dialect= 'excel')
            count = 0
            # for each index and row in the file, check if if the column in the current iterating row contains the ip address or id. when found, add such columns from row into the justIP.csv file
            for index, row in file.iterrows():
                i,ip = index,row['Last Edited by: IP Address']
                i,id = index,row['Last Edited by: Username']
                writer.writerow([id,ip])
                count += 1
                if count == 1000:
                    print("count reached", count)
                    break





