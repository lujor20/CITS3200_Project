import xlsxwriter 
import csv

class importData:
    def __init__(self, file):

        workbook = xlsxwriter.Workbook('formatting/export.xlsx')# creates the spreadsheet
        UI = workbook.add_worksheet()
        UI.set_margins(left=0.7, right=0.7, top=0.75, bottom=0.75)
        worksheet = workbook.add_worksheet()# adds worksheet
        self.rows = 0
        self.columns = 0

        with open(file, newline='') as openfile: # opens the file 
            csvFile = csv.reader(openfile, delimiter=',', quotechar='|')# make he file accessible via csv library

            # creates a temporary 2d array to store the data which makes it easier to input later
            temp = []
            counter = 0
            for row in csvFile:
                temprow = []
                for i in row:
                    temprow.append(i)
                temp.append(temprow)
        
            # now write into the excel spreadsheet
            row = 0
            col = 0

            for ip, country, city, latitude, longitude, flag in (temp):
                worksheet.write(row, col,     ip)
                worksheet.write(row, col + 1, country)
                worksheet.write(row, col + 2, city)
                worksheet.write(row, col + 3, latitude)
                worksheet.write(row, col + 4, longitude)
                worksheet.write(row, col + 5, flag)

                row += 1
            
            range = str('A'+2+':'+'F'+col)
            domesticColour = # add ability to fill colour
            
            
            worksheet.conditional_format(range, {'type':     'text',
                                        'criteria': 'begins with',
                                        'value':    'DOMESTIC',
                                        'format':   domesticColour})
            
            self.rows = row
            self.columns = col

        
        UI.write(1,1, "TOOL 2")
        UI.write(2,1, "NO. DOMESTIC")
        UI.write(3,1,'=SUM()')
        UI.write(2,2, "NO. INTERNATIONAL")
        UI.write(2,3, "NO. AT RISK")
        
        workbook.close()


    
    

test = importData('formatting/ipwithflag.csv')