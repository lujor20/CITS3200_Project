import csv
# this module is for flagging for international only. if the ip matches with a high risk country code, then it will be flagged as high risk, otherwise just flagged as international

class flagging:
    def __init__(self, file, action):
        with open(file, newline='') as openfile: # opens the file 
            csvFile = csv.reader(openfile, delimiter=',', quotechar='|')# make the file accessible via csv library
            with open('ipwithflag.csv', 'w', newline='') as outputfile: # create a new file to write into
                writer = csv.writer(outputfile, dialect= 'excel')# make new file accessible to write into with csv library
                if (action == "initial"):
                    self.initial(csvFile, writer)
                elif (action == "international"):
                    self.international(csvFile, writer)
                elif (action == "distance"):
                    self.distance(csvFile, writer)
                else:
                    print("invalid action")

    def initial(self, readFile, writeFile):
        print("begin initial flagging option")
        headers = ["ip", "country", "city", "latitude", "longitude", "flag"]
        writeFile.writerow(headers)
        counter = 0 
        # for each row
        counter = 0
        for row in readFile:
            if (counter ==0):
                counter += 1
                continue
            row = list(row)
            flag = ''
            # if row is australia, then set domestic flag
            if (row[1] == "AU"):
                flag = "domestic"
                # if not australia, check if ip is within one of the righer risk country codes, and if match any of them, assign corresponding country code. otherwise set as international
            elif (row[1] != "AU"):
                flag = "international"
            # add the flag to the end of the row
            row.append(flag)
            # write to the new document
            writeFile.writerow(row)

    # this is one of the two optional modules which will take the extracted international IP's and determine if the international code is part of high risk country codes
    def international(self, readFile, writeFile):
        print("begin international flagging option")
        headers = ["ip", "country", "city", "latitude", "longitude", "flag"]
        writeFile.writerow(headers)
        sus = ["KE", "PK", "IN", "MA", "UA", "CN"]
        counter = 0 
        # for each row
        counter = 0
        for row in readFile:
            if (counter ==0):
                counter += 1
                continue
            row = list(row)
            flag = ''
            # if row is australia, then set domestic flag
            if (row[1] != "AU"):
                for i in sus:
                    if (row[1] == i):
                        flag = "high risk international"
                        break
                else:
                    flag = "international"
            # add the flag to the end of the row
            row.append(flag)
            # write to the new document
            writeFile.writerow(row)

    # this is one of the two optional modules which will take the extracted duplicate ips and determine if the last column distance is within the parameters of feasible travel distance
    def distance(self, readFile, writeFile):
        print("begin distance flagging option")
        headers = ["ip", "country", "city", "latitude", "longitude", "ip2", "country2", "city2", "latitude2", "longitude2","distance", "flag"]
        writeFile.writerow(headers)
        # for each row
        counter = 0
        for row in readFile:
            if (counter ==0):
                counter += 1
                continue
            row = list(row)
            flag = ''
            # if row is australia, then set domestic flag\
            if (row[-2] >50):
                flag = "high risk distance"
            if (row[-2] <=50):
                flag = "low risk distance"
            # add the flag to the end of the row
            row.append(flag)
            # write to the new document
            writeFile.writerow(row)
                    
#test = flagging('flagging/test.csv', 'initial')
#test = flagging('flagging/test.csv', 'international')
#test = flagging('flagging/test.csv', 'distance')
                        
