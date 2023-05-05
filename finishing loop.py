import pandas as pd
from owlready2 import *
import csv
import win32com.client as win32
def goto(line):
    # path to the CSV file
    csv_file_path = r"C:\Users\ramid\OneDrive\Desktop\combined_data_v8f.csv"

    # create an Excel application object
    excel = win32.gencache.EnsureDispatch('Excel.Application')

    # make the Excel window visible (optional)
    excel.Visible = True

    # open the CSV file
    workbook = excel.Workbooks.Open(csv_file_path)

    # get the worksheet object
    worksheet = workbook.Worksheets(1)

    # navigate to a specific cell (e.g., cell A10)
    cell = worksheet.Cells(line, 1)
    cell.Select()
    cell.Select()

    # Activate the Excel window that contains the CSV file
    excel.Visible = True
    excel.WindowState = -4137 # minimize all windows
    # go down
    worksheet.Application.SendKeys("{DOWN}")
    worksheet.Application.SendKeys("{UP}")
    # make the Excel window visible (optional)
    excel.Visible = True


onto = get_ontology("test.owl").load()
onto1= get_ontology("testi.owl").load()
all_classes=list(onto1.classes())
reader1=[]
#saving lines into reader1
with open('combined_data_v8f.csv', 'r', encoding="utf-8") as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            reader1.append(row)
#going to rows
#print(reader1[1070])
for el in all_classes:
    length=max(el.iri.rfind("/"),el.iri.rfind("#"))+1
    if el.iri[0:length]=="http://w3id.org/gbo/mgg#":
        print("fixing "+ el.label[0])
        words=el.label[0].split(" ")
        maxx=len(words)
        for i in  range(len(reader1)-maxx+1):
            Flag=True
            for j in range(maxx):
                if j==0 and not ( reader1[i][3].startswith("B-") and reader1[i][1].lower()==words[j]):
                    Flag=False
                if j!=0 and not ( reader1[j+i][3].startswith("I-") and reader1[j+i][1].lower()==words[j]):
                    Flag=False
            if Flag:
                goto(i+1)
               # print(reader1[i])
                #print(i)
                input1 = input("press enter for next? ")
                inputs= input1.split()
                if inputs[0]=="all":
                    break
