import csv

def findinternational(inputfile):
    # Create a list to store the rows with flag = international
    international_rows = []

    with open(inputfile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldnames = reader.fieldnames
        for row in reader:
            if row['flag'] == "international":
                international_rows.append(row)

    # Create a new file "international.csv" and write the international rows to it
    with open('international.csv', 'w', newline='') as international_file:
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(international_file, fieldnames=fieldnames)
        
        # Write the header row
        # Write the international rows
        writer.writeheader()
        writer.writerows(international_rows)








        


