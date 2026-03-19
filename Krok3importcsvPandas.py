import csv
import os
import logging
import pandas as pd
import openpyxl as opx
# from openpyxl import Workbook
# from openpyxl.utils import get_column_letter
from  _settings import *

# VRTCSVQGIS = 'vrtyGIS.csv'    
# VRTLOZCSVQGIS = 'vrtlozGIS.csv'
# GEO5QGIS = 'GEO5QGIS.csv'

# logging.basicConfig(filename = KROK3LOGFILE, level=logging.INFO, filemode='w')
# logger=logging.getLogger()

logger=logging.getLogger('vrt')
logger.addHandler(logging.FileHandler(KROK3LOGFILE, mode='a'))

# TOPDIR = TOPDIR + '\\'
# XLSNAME = r"PandasVrty.xlsx"
TOPDIR = TOPDIR + '\\'
XLSNAME = EXCELWB
# wb = opx.Workbook()
pd.DataFrame().to_excel(XLSNAME, sheet_name = 'info', index=3)

def save_frame(df, dirname, dfname):
    '''ulozi dataframes v adresari dirname vo formate
    dfname.csv, dfname.xlsx, dfname.sqlite3'''
    
    print(f'ukladám {dfname}')
    if len(df) < 1.048e6:
        with pd.ExcelWriter(XLSNAME, mode = 'a', engine='openpyxl', if_sheet_exists='replace') as EXCELWRITER:
            df.to_excel(EXCELWRITER, sheet_name=dfname, index=False)
            logger.info(f"{dirname} - {dfname} {len(df)} riadkov uložených do excelu")
    else:
        logger.error(f'{dfname} obsahuje {len(df)} riadkov, viac ako je povolený limit excelu, nie je uložené')


# def create_xls_from_cvs(fn, shname, shnum):
#     print(fn)
#     f = open(fn)
#     csv.register_dialect('semicolons', delimiter=';')
#     reader = csv.reader(f, dialect='semicolons')
#     wb.create_sheet(shname)
#     ws = wb.worksheets[shnum]
#     #ws.title = "vrtyGIS"
#     for row_index, row in enumerate(reader):
#         for column_index, cell in enumerate(row):
#             # column_letter = get_column_letter((column_index + 1))
#             try:
#                 ws.cell(column=column_index+1, row=row_index+1).value = cell
#             except Exception as err:
#                 print("Exception:", __file__, __name__, f"{err=}, {type(err)=}", row)
#                 logger.error("Exception: %s %s %s", err, type(err), row)


#     f.close
def clean_duplicates(df):
    df_dup = df.sort_values(by='File',ascending=True).drop_duplicates(subset=["Vrt", "JTSKX", "JTSKY"], keep='last')
    print(f"original:{df.shape}  reduced{df_dup.shape}")
    return df_dup


def clean_coordinates(df):
    # return df[(df.JTSKY > 595000) | (df.JTSKY < 160000) | (df.JTSKX> 1340000) | (df.JTSKX < 1128000) ] # bad values
    return df[(df.JTSKY < 595000) & (df.JTSKY > 160000) & (df.JTSKX < 1340000) & (df.JTSKX > 1128000) ] # good values
    # pass

def to_num(df, cols):
    '''prevedie stlpce cols na numeric'''
    for col in cols:
        df[col] = pd.to_numeric(df[col], errors='coerce', dtype_backend='numpy_nullable').astype('Float32')
        #memory usage 60347 vs 80255 bytes
        #df[col] = pd.to_numeric(df[col], errors='coerce', dtype_backend='pyarrow' ).astype(pd.ArrowDtype(pa.float64())) 
    return df



def create_xls_from_cvsPandas(fn, shname, shnum):
    print(fn)
    df = pd.read_csv(fn, on_bad_lines='warn', delimiter=';', decimal='.')
    df = to_num(df, ['JTSKX', 'JTSKY'])
    df = clean_duplicates(df)
    df = clean_coordinates(df)
    print(df.shape)
    print(df.Vrt.head())
    print(df)
    save_frame(df, TOPDIR, shnum)

def create_xls_from_cvsPandas2(fn, shname, shnum):
    print(fn)
    df = pd.read_csv(fn, on_bad_lines='warn', delimiter=';', decimal='.')
    df = to_num(df, ['JTSKX', 'JTSKY'])
    # df = clean_duplicates(df)
    df = clean_coordinates(df)
    print(df.shape)
    print(df.Vrt.head())
    print(df)
    save_frame(df, TOPDIR, shnum)



    




create_xls_from_cvsPandas(VRTLOZCSVQGIS, SHVRTLOZ,SHVRTLOZ)
create_xls_from_cvsPandas(VRTCSVQGIS, SHVRT, SHVRT)
create_xls_from_cvsPandas2(GEO5QGIS, SHGEO5, SHGEO5)

print('Done')


# wb.save(filename = dest_filename)