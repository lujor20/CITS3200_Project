import csv
from .IPtoLocation import get_country, get_location_type

def cleanfile(inputfile):
    with open(inputfile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        # Add 'Country' and 'Flag' to the output columns
        output_rows = [['Username', 'IPAddress1', 'IPAddress2', 'Country', 'Flag']]
        user_records = {}  # To store user records with their associated IP addresses

        for row in reader:
            username = row['Username']
            ip_address = row['Last Edited by: IP Address']

            if username in user_records:
                if ip_address not in user_records[username]:
                    user_records[username].append(ip_address)
            else:
                user_records[username] = [ip_address]

        for username, ips in user_records.items():
            country = get_country(ips[-1] if len(ips) > 1 else ips[0])
            flag = get_location_type(country)
            if len(ips) > 1:
                output_rows.append([username, ips[-2], ips[-1], country, flag])
            else:
                output_rows.append([username, ips[0], 'None', country, flag])

    with open('Cleaned.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(output_rows)



