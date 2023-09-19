
import csv

def cleanfile(inputfile):
    with open(inputfile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        columns_needed = [['Date', 'IPAddress', 'Username', 'Type', 'Value', 'AttemptActivity']]
        user_records = {}  # To store user records with their associated IP addresses
        duplicate_users = []  # To store users with different IP addresses

        for row in reader:
            username = row['Username']
            ip_address = row['Last Edited by: IP Address']

            # Check if this username is already in user_records
            if username in user_records:
                # If the IP address is different, add to duplicate_users
                if ip_address != user_records[username]:
                    duplicate_users.append({'Username': username, 'IPAddress1': user_records[username], 'IPAddress2': ip_address})
            else:
                # Add this username and IP address to user_records
                user_records[username] = ip_address

            cleaned_row = [
                row['Date'],
                row['Last Edited by: IP Address'],
                username,
                row['Type'],
                row['Value'],
                row['Attempt Activity']
            ]
            columns_needed.append(cleaned_row)

    # Write the cleaned data to 'Cleaned.csv'ls
    
    with open('Cleaned.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(columns_needed)

    # Write the duplicate users with different IP addresses to 'DuplicateUsers.csv'
    with open('duplicate.csv', 'w', newline='') as csvfile:
        fieldnames = ['Username', 'IPAddress1', 'IPAddress2']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(duplicate_users)

