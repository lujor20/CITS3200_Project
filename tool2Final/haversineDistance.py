import math
import csv
import geopy.distance as geodist

'''
haversineDistance class is used for computing the distance between two points on a sphere using their longitudes and latitudes.
this program will iteratively go through the inputfiile which is going to be the duplicate.csv file,
and calculate the distance between the two ip's on the same row, add the distance to the distance column, and save the row into the "data" array.
finally, this wiill reopen the same input file but as a writer file to deposit all rows in "data" into the duplicate.csv file.
'''
class haversineDistance:
    def calculate2(self, long1, lat1, long2, lat2):
        one = (long1, lat1)
        two = (long2, lat2)
        return geodist.geodesic(one,two).km
    
    def __init__(self, inputfile):
        data = []
        with open(inputfile, newline = '') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                distance = self.calculate2(row['longitude'], row['latitude'], row['longitude2'], row['latitude2'])
                distance = round(distance, 2)
                row['distance'] = distance
                data.append(row)
        csvfile.close()
        with open(inputfile, 'w', newline = '') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = ['id', 'ip', 'country', 'city', 'latitude', 'longitude', 'ip2', 'country2', 'city2', 'latitude2', 'longitude2', 'distance'])
            writer.writerows(data)
            
        
    
    # this function takes 4 parameters, 2 coordinates per ip, and calculates the distance between the two points using the haversine formula
    def calculate(self, longitude1, latitude1, longitude2, latitude2):
        longitude1 = math.radians(float(longitude1))
        latitude1 = math.radians(float(latitude1))
        longitude2 = math.radians(float(longitude2))
        latitude2 = math.radians(float(latitude2))

        longDifference = longitude2 - longitude1
        latDifference = latitude2 - latitude1
        a = math.sin(latDifference / 2)**2 + math.cos(latitude1) * math.cos(latitude2) * math.sin(longDifference / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        difference = 6371.0 * c
        return difference
    
