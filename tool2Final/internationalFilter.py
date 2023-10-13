import csv
'''
This funciton "findinternational" takes in a csv file which consists of the flag category according to each row of students. It then goes through and checks each row 
and finds whether it contains the flag "international". As an empty list initialised earlier by the name of "international_rows", any rows with flag "international" is then 
appended into that newly created list. Once it has gone through the whole csv input file, this section of code then creates a new empty csv file by the name of 'international.csv'. 
This file includes the newly seperated "international" flagged rows only as output, along with its other forms of data included in the row. 
'''
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








        


