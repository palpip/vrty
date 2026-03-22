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
logging.basicConfig(filename = KROK3LOGFILE, level=logging.DEBUG, filemode='a')
logger=logging.getLogger('Krok3')
logger.addHandler(logging.StreamHandler())

# logger.addHandler(logging.FileHandler(KROK3LOGFILE, mode='w'))

# TOPDIR = TOPDIR + '\\'
# XLSNAME = r"PandasVrty.xlsx"
TOPDIR = TOPDIR + '\\'
XLSNAME = EXCELWB
# wb = opx.Workbook()
pd.DataFrame().to_excel(XLSNAME, sheet_name = 'info', index=0)

def save_frame(df, dirname, dfname):
    '''ulozi dataframes v adresari dirname vo formate
    dfname.csv, dfname.xlsx, dfname.sqlite3
    excelovské súbory sa ukladajú do XLSNAME '''
    
    # print(f'ukladám {dfname}')
    if len(df) < 1.048e6:
        try:    
            with pd.ExcelWriter(XLSNAME, mode = 'a', engine='openpyxl', if_sheet_exists='replace') as EXCELWRITER:
                df.to_excel(EXCELWRITER, sheet_name=dfname)
                #logger.info(f"{dirname} - {dfname} {len(df)} riadkov uložených do excelu {XLSNAME}:{dfname}")
                logger.info(f"{len(df)} riadkov uložených do excelu {XLSNAME}:{dfname}")
                
                # df.info()
        except Exception as err:
                # print("Exception:", __file__, __name__, f"{err=}, {type(err)=}")
                logger.error("Exception: %s %s", err, type(err))
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
def clean_duplicates(df, typ):
    if df.shape[0]:
        if typ == SHGEO5: sortby = 'Vrt'
        elif typ == SHVRT or typ == SHVRTLOZ: sortby = 'File'
        df_dup = df.sort_values(by=sortby,ascending=True).drop_duplicates(subset=["Vrt", "JTSKX", "JTSKY"], keep='last')
        return df_dup
    else:
        return pd.DataFrame()


def bad_coordinates_df(df):
    return df[(df.JTSKY >= 595000) | (df.JTSKY <= 160000) | (df.JTSKX >= 1340000) | (df.JTSKX <= 1128000) ] # bad values
 
def good_coordinates_df(df):
    return df[(df.JTSKY < 595000) & (df.JTSKY > 160000) & (df.JTSKX < 1340000) & (df.JTSKX > 1128000) ] # good values
 
def to_num(df, cols):
    '''prevedie stlpce cols na numeric'''
    for col in cols:
        df[col] = pd.to_numeric(df[col], errors='coerce', dtype_backend='numpy_nullable').astype('Float32')
        #memory usage 60347 vs 80255 bytes
        #df[col] = pd.to_numeric(df[col], errors='coerce', dtype_backend='pyarrow' ).astype(pd.ArrowDtype(pa.float64())) 
    return df



def create_xls_from_cvsPandas(fn, shname, shnum):
    # print(fn)
    df = pd.read_csv(fn, on_bad_lines='warn', delimiter=';', decimal='.')
    df = to_num(df, ['JTSKX', 'JTSKY'])
    df = clean_duplicates(df)
    bad_coor = bad_coordinates_df(df)
    df = good_coordinates_df(df)
    # print(df.shape)
    # print(df.Vrt.head())
    # print(df)
    save_frame(bad_coor, TOPDIR, 'ERR' + shnum)
    save_frame(df, TOPDIR, shnum)

def create_xls_from_cvsPandas2(fn, shname, shnum):
    # print(fn)
    if os.path.isfile(fn):
        df = pd.read_csv(fn, on_bad_lines='warn', delimiter=';', decimal='.')
        read_count = df.shape[0]
        df = to_num(df, ['JTSKX', 'JTSKY'])
        df = clean_duplicates(df, shname)
        dedupl_count = df.shape[0]
        bad_coor_df = bad_coordinates_df(df)
        df = good_coordinates_df(df)
        good_coor_count = df.shape[0]
        # print(df.shape)
        # print(df.Vrt.head())
        # print(df)
        logger.info(f'súbor {fn}: načítaných {read_count} deduplikovaných {dedupl_count}' \
                     f' so správnymi súr. {good_coor_count} riadkov')
        save_frame(df, TOPDIR, shnum)
        save_frame(bad_coor_df, TOPDIR, 'ERR' + shnum)
    else:
        logger.warn(f'Adresár {TOPDIR} neobsahuje súbory {shname}')



    



logger.info(40*'+'+' started krok3 Pandas')
create_xls_from_cvsPandas2(VRTCSVQGIS, SHVRT, SHVRT)
create_xls_from_cvsPandas2(GEO5QGIS, SHGEO5, SHGEO5)
create_xls_from_cvsPandas2(VRTLOZCSVQGIS, SHVRTLOZ,SHVRTLOZ)
logger.info(40*'+'+' done krok3 Pandas')


