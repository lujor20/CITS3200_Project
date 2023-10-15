import pandas as pd
import csv
'''
To summarise this code file, it takes a csv file as input (inputfile) and processes this file to identify and extract any duplicate records of student ID's with 
different Ip addresses. Any duplicates found in the file will be placed into a newly created CSV file called "duplicate.csv". This newly created file, acts as the 
output. 


- This is done through csv.DictReader reading the input file 
- specifies the important columns needed for the new output csv
- creates structures: user_records and duplicate_users which stores the data from our duplicate analysis. This is later added into the new csv file
- The use of the for loop in this code acts as the data read in each row of the file. 
- The use of the if and else statements, is where the real work happens which checks if there more than one id/ ip in the file. 
- all this data is then added into the new file, shown down below through the functions of write.header() and writerow(row)
'''

def cleanfile(inputfile):
    with open(inputfile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        columns_needed = ['id', 'ip', 'country', 'city', 'latitude', 'longitude', 'ip2', 'country2', 'city2', 'latitude2', 'longitude2', 'distance']
        user_records = {}  # To store user records with their associated IP addresses
        duplicate_users = []  # To store users with different IP addresses
        with open('app/tool2/tool2Final/backendData/duplicate.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=columns_needed)
            for row in reader:
                # Check if this username is already in user_records
                if row['id'] in user_records:
                    # If the IP address is different, add to duplicate_users
                    if row['ip'] != user_records[row['id']][0]:
                        duplicate_users.append({'id': row['id'], 'ip': user_records[row['id']][0], 'country': user_records[row['id']][1], 'city': user_records[row['id']][2], 'latitude': user_records[row['id']][3], 'longitude': user_records[row['id']][4], 'ip2': row['ip'], 'country2': row['country'], 'city2': row['city'], 'latitude2': row['latitude'], 'longitude2': row['longitude']})
                else:
                    # Add this username and IP address to user_records
                    user_records[row['id']] = [row['ip'], row['country'], row['city'], row['latitude'], row['longitude']]
            
            # Write the rows from duplicate_users to the duplicate.csv file
            writer.writeheader()
            for row in duplicate_users:
                writer.writerow(row)
            


            





