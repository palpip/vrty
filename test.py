import os
import openpyxl as op

excelfn = r'C:\Shares\vrty\vrty3\python\err\12016\vrty SLJ.xlsx'


def test(wbname = excelfn):
    wb = op.load_workbook(wbname)
    sheet = wb['Dáta - Skúška|Vŕtanie']
    print(sheet.columns)
    for column in sheet.columns:
        print (column[0].value)
    
    print(sheet[3][1].value)
    print(sheet[3][1].value)
    print(enumerate(sheet.columns))
    for col in sheet.columns:
        print (col[0].value)
    col = sheet.columns
    print(col)
    
    for row in sheet.rows:
        print (row[0].value,row[2].value)
    
    # column = sheet.columns[]
    # for cell in column:
    #     print (cell.value)
    
    res = {}

    for row in sheet.rows:
        hlbka = row[2].value
        vrt = row[0].value
        print(vrt,hlbka)
        if vrt not in res:
            res[vrt] = hlbka
        elif res[vrt] < hlbka:    
            res[vrt] = hlbka
    print(res)

# test()
from _settings import *
print(TOPDIR)    
print('finish')