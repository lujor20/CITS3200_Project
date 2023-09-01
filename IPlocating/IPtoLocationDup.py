import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')
warnings.filterwarnings("ignore", category=UserWarning, module='ssl')

import csv 
import pandas as pd
from ip2geotools.databases.noncommercial import DbIpCity
#from geopy.distance import distance

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
    def returnDetails(username,ip_address1, ip_address2, counter): 
        res = DbIpCity.get(ip_address1, api_key="free")
        res2 = DbIpCity.get(ip_address2, api_key="free")
        print(res.ip_address, "  ", res.country)
        print(res2.ip_address, "  ", res2.country)
        return [res.ip_address, res.country, res.city, res.latitude, res.longitude, res2.ip_address, res2.country, res2.city, res2.latitude, res2.longitude]
    #
    # creates easy to read formatting for output csv
    # keeps count of how many rows of ip processed
    #

    def __init__(self, file):
        headers = ["ip", "country", "city", "latitude", "longitude", "ip2", "country2", "city2", "latitude2", "longitude2"]
        counter = 0
        #opening passed csv file that only contains a column of individual ip's
        with open(file, newline='') as openfile:
            csvFile = csv.reader(openfile, delimiter=',', quotechar='|')
            with open('ipInformation.csv', 'w', newline='') as outputfile:
                writer = csv.writer(outputfile, dialect= 'excel')
                writer.writerow(headers)
                for row in csvFile:
                    #assuming csv passed is just 1 column of ip's
                    #information = IPtoLocation.returnDetails(row[0], counter)
                    #counter += 1
                    #print("country count: ", counter)
                    #writer.writerow(information)
                     if len(row) >= 2:
                        username = row[0]
                        ip_address1 = row[1]
                        ip_address2 = row[2]
                        information = IPtoLocation.returnDetails(username,ip_address1, ip_address2, counter)
                        counter += 1
                        print("country count:", counter)
                        writer.writerow(information)


IPtoLocation('duplicate.csv')




