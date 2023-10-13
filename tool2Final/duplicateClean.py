import pandas as pd
import csv


def cleanfile(inputfile):
    with open(inputfile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        columns_needed = ['id', 'ip', 'country', 'city', 'latitude', 'longitude', 'ip2', 'country2', 'city2', 'latitude2', 'longitude2', 'distance']
        user_records = {}  # To store user records with their associated IP addresses
        duplicate_users = []  # To store users with different IP addresses
        with open('duplicate.csv', 'w', newline='') as csvfile:
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
            


            





