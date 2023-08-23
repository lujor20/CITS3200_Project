import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')
warnings.filterwarnings("ignore", category=UserWarning, module='ssl')

import csv 
import pandas as pd
from ip2geotools.databases.noncommercial import DbIpCity
from geopy.distance import distance

#
# class for geting precise information on suspiscious ip addresses. reserve or suspiscious ip's
# returns ip address, country code, city, longitude and latitude coordinates 
# to use, pass csv of just ip's into file argument
# 

class IPtoLocation: 
    @staticmethod
    #
    # calls for relevant information from external db
    # 
    def returnDetails(ip, counter ): 
        res = DbIpCity.get(ip, api_key="free")
        print(res.ip_address, "  ", res.country)
        return [res.ip_address, res.country, res.city, res.latitude, res.longitude]
    #
    # creates easy to read formatting for output csv
    # keeps count of how many rows of ip processed
    #

    def __init__(self, file):
        headers = ["ip", "country", "city", "latitude", "longitude"]
        counter = 0
        #opening passed csv file that only contains a column of individual ip's
        with open(file, newline='') as openfile:
            csvFile = csv.reader(openfile, delimiter=',', quotechar='|')
            with open('IPlocating/ipInformation.csv', 'w', newline='') as outputfile:
                writer = csv.writer(outputfile, dialect= 'excel')
                writer.writerow(headers)
                for row in csvFile:
                    #assuming csv passed is just 1 column of ip's
                    information = IPtoLocation.returnDetails(row[0], counter)
                    counter += 1
                    print("country count: ", counter)
                    writer.writerow(information)


#
# keep at bottom for testing
#
test = IPtoLocation('IPlocating/justIP.csv')





