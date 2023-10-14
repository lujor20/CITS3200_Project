import csv

'''
flagging class is used for adding the flag column to the output.csv file depending on the action argument.
the program will iteratively go through all the rows of the input file (ipinformation.csv, international.csv, duplicate.csv) and add the flag to the last column of each row.
then this will use the output.csv file to save all the rows with the flag column added.
'''
class flagging:
    # this init funciton is used to determine which action to perform depending on the action argument
    def __init__(self, file, action):
        with open(file, newline='') as openfile: 
            csvFile = csv.reader(openfile, delimiter=',', quotechar='|')
            with open('output.csv', 'w', newline='') as outputfile: 
                writer = csv.writer(outputfile, dialect= 'excel')
                if (action == "initial"):
                    self.initial(csvFile, writer)
                elif (action == "international"):
                    self.international(csvFile, writer)
                elif (action == "distance"):
                    self.distance(csvFile, writer)
                else:
                    print("invalid action")

    # this function is used to determine if the ip is domestic or international by checking if the country code is AU. 
    def initial(self, readFile, writeFile):
        print("begin initial flagging option")
        headers = ["id", "ip", "country", "city", "longitude", "latitude", "flag"]
        writeFile.writerow(headers)
        counter = 0
        for row in readFile:
            # this is just to skip over the first row, which holds the headder in the staticInternalSave.csv file
            if (counter ==0):
                counter += 1
                continue
            row = list(row)
            flag = ''
            if (row[2] == "AU"):
                flag = "domestic"
            elif (row[2] != "AU"):
                flag = "international"
            row.append(flag)
            writeFile.writerow(row)

    # this function is used to determine if the ip is one of the high risk country codes, this will add a flag column which either says high risk code or low risk code
    def international(self, readFile, writeFile):
        print("begin international flagging option")
        headers = ["id", "ip", "country", "city", "latitude", "longitude", "origin", "flag"]
        writeFile.writerow(headers)
        sus = ["KE", "PK", "IN", "MA", "UA", "CN", "GB"]
        counter = 0
        for row in readFile:
            # this is just to skip over the first row, which holds the header in the staticInternalSave.csv file
            if (counter ==0):
                counter += 1
                continue
            row = list(row)
            flag = ''
            if (row[2] != "AU"):
                print(row[2])
                for i in sus:
                    print(i)
                    if (row[2] == i):
                        flag = "high risk code"
                        break
                else:
                    flag = "low risk code"
            row.append(flag)
            writeFile.writerow(row)

    # this function is used to determine if the distance between the two ip addesses on the same row are too far appart to be realistic over the duration of a test. anything that is over 10 is low risk, 10-20 is medium risk, and over 20 is high risk, and anything over is high risk
    def distance(self, readFile, writeFile):
        print("begin distance flagging option")
        headers = ["id","ip", "country", "city", "latitude", "longitude", "ip2", "country2", "city2", "latitude2", "longitude2","distance", "flag"]
        writeFile.writerow(headers)
        for row in readFile:
            row = list(row)
            flag = ''
            try:
                if (float(row[-1]) <float(10)):
                    flag = "low risk"
                elif (float(row[-1]) <=float(20)):
                    flag = "medium risk"
                elif (float(row[-1]) >float(20)):
                    flag = "high risk"            
            except ValueError as e:
                print("error in distance flagging")
                print(e)
            row.append(flag)
            writeFile.writerow(row)


