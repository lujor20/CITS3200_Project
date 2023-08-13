import pandas as pd
import csv

file = pd.read_csv('example LMS test log.csv')

with open('justIP.csv', 'w', newline='') as outputfile:
    writer = csv.writer(outputfile, dialect= 'excel')
    for index, row in file.iterrows():
        i,r = index,row['Last Edited by: IP Address']
        writer.writerow([r])
        print(r)
    