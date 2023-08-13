import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')
warnings.filterwarnings("ignore", category=UserWarning, module='ssl')

import csv
import pandas as pd
from ip2geotools.databases.noncommercial import DbIpCity
from geopy.distance import distance

class IPtoLocation:

    @staticmethod
    def returnDetails(ip):
        res = DbIpCity.get(ip, api_key="free")
        print("country:   {res.country}")
        return [res.ip_address, res.country, res.city, res.latitude, res.longitude]

    def __init__(self, file):
        headers = ["ip", "country", "city", "latitude", "longitude"]
        #opening passed csv file that only contains a column of individual ip's
        with open(file, newline='') as openfile:
            csvFile = csv.reader(openfile, delimiter=',', quotechar='|')
            with open('IPlocating/ipInformation.csv', 'w', newline='') as outputfile:
                writer = csv.writer(outputfile, dialect= 'excel')
                writer.writerow(headers)
                for row in csvFile:
                    #assuming csv passed is just 1 column of ip's
                    information = IPtoLocation.returnDetails(row[0])
                    writer.writerow(information)


test = IPtoLocation('IPlocating/justIP.csv')





