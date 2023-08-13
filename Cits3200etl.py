def cleanfile(inputfile):
    import csv
    with open(inputfile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        columns_needed = [['Date','IPAddress', 'Username','Type','Value','AttemptActivity']] 
        for i, row in enumerate(reader):
            cleaned_row = [
                row['Date'],
                row['Last Edited by: IP Address'],
                row['Username'],
                row['Type'],
                row['Value'],
                row['Attempt Activity']
            ]
            columns_needed.append(cleaned_row)

    with open('Cleaned.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(columns_needed)

