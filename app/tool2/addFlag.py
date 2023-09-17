import csv
class addFlag:
    def __init__(self, file):
        headers = ["ip", "country", "city", "latitude", "longitude", "flag"]
        sus = ["KE", "PK", "IN", "MA", "UA", "CN"]
        with open(file, newline='') as openfile:  # opens the file
            csvFile = csv.reader(openfile, delimiter=',', quotechar='|')  # make he file accessible via csv library
            with open('ipwithflag.csv', 'w', newline='') as outputfile:  # create a new file to write into
                writer = csv.writer(outputfile,
                                    dialect='excel')  # make new file accessible to write into with csv library
                writer.writerow(headers)
                counter = 0
                print('test')

                # for each row
                counter = 0
                for row in csvFile:
                    if (counter == 0):
                        counter += 1
                        continue
                    row = list(row)


                    # judge IP's country
                    if (row[1] == "AU"):
                        flag = "domestic"
                    elif row[1] == "AU":
                        flag = "domestic"
                    elif row[1] in sus:
                        flag = "suspicious"
                    else:
                        flag = "international"

                    # add the flag to the end of the row
                    row.append(flag)
                    # write to the new document
                    writer.writerow(row)


test = addFlag('test.csv')