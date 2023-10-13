import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')
warnings.filterwarnings("ignore", category=UserWarning, module='ssl')

import csv 
import pandas as pd
from ip2geotools.databases.noncommercial import DbIpCity
from geopy.distance import distance

'''
IPtoLocation class is used to geolocate the ip address of each row of the csv file. this class uses the ip2geotools library.
this class takes the name of csv file which contains all of the ips (justIP.csv) and outputs a csv file (ipInformation.csv) which contains the geolocation of each ip address.
it works by calling returnDetails function for each ip address

this function would largely be the bottle neck to the performance of tool 2 as the database is relatively slow to respond to each request. 
unfortunately this is the best solution have access to which is free. 

if looking to further improve the performance of tool 2, this is definitely the best place to start.
'''
class IPtoLocation: 
    @staticmethod
    # this function performs a search through the external database for find matches and returns the details of the ip address
    def returnDetails(ip, counter ): 
            res = DbIpCity.get(ip, api_key="free")
            return [res.ip_address, res.country, res.city, res.latitude, res.longitude]

    # this function will take the name of the csv file with the ip addresses to be geolocated and output a csv file with the geolocation of each ip address termed ipInformation.csv
    def __init__(self, file):
        headers = ["id", "ip", "country", "city", "latitude", "longitude"]
        counter = 0
        with open(file, newline='') as openfile:
            csvFile = csv.reader(openfile, delimiter=',', quotechar='|')
            with open('backendData/ipInformation.csv', 'w', newline='') as outputfile:
                writer = csv.writer(outputfile, dialect= 'excel')
                writer.writerow(headers)
                for row in csvFile:
                    if row[1] == "ip":
                        continue
                    information = IPtoLocation.returnDetails(row[1], counter)
                    information = [row[0]] + information
                    counter += 1
                    writer.writerow(information)










