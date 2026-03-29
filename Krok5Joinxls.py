'''Krok5Joinxls.py
spojí viacero xlsx do jedného, vytvorí KML a do infa vloží metadáta
'''
#from openpyxl import load_workbook
import os
import openpyxl as op
import simplekml
import csv
import logging
# from proj4 import JTSK_to_WGS
from _utils import dirEntries
from _funcs import *
from _settings import *
import _funcsKML as fKML
import pandas as pd
chkdirs()

logging.basicConfig(filename = 'CCC'+KROK5LOGFILE, level=logging.INFO, filemode='w')
logger=logging.getLogger()

fKML.logger = logger # pokus o presmerovanie
logger.info('start')
# _KML = '' #global variable initialized in main


def save_frame(df, dirname, dfname):
    '''ulozi dataframes v adresari dirname vo formate
    dfname.csv, dfname.xlsx, dfname.sqlite3
    excelovské súbory sa ukladajú do XLSNAME '''
    
    # print(f'ukladám {dfname}')
    if len(df) < 1.048e6:
        try:    
            with pd.ExcelWriter(EXCELJOINED, mode = 'a', engine='openpyxl', if_sheet_exists='replace') as excelwriter:
                df.to_excel(excelwriter, sheet_name=dfname)
                #logger.info(f"{dirname} - {dfname} {len(df)} riadkov uložených do excelu {XLSNAME}:{dfname}")
                logger.info(f"{len(df)} riadkov uložených do excelu {EXCELJOINED}:{dfname}")
                
                # df.info()
        except Exception as err:
                # print("Exception:", __file__, __name__, f"{err=}, {type(err)=}")
                logger.error("Exception: %s %s", err, type(err))
    else:
        logger.error(f'{dfname} obsahuje {len(df)} riadkov, viac ako je povolený limit excelu, nie je uložené')

def add_to_xls(df, shnum):
    bad_coor_df = pd.DataFrame()
    if (read_count := df.shape[0]) != 0: 
        df = to_num(df, ['JTSKX', 'JTSKY'])
        df = clean_duplicates(df, shnum)
        dedupl_count = df.shape[0]
        bad_coor_df = bad_coordinates_df(df)
        df = good_coordinates_df(df)
        good_coor_count = df.shape[0]
        # print(df.shape)
        # print(df.Vrt.head())
        # print(df)
        logger.info(f'súbor {shnum}: načítaných {read_count} deduplikovaných {dedupl_count}' \
                    f' so správnymi súr. {good_coor_count} riadkov')
    else:
        logger.info(f'súbor {shnum}: neobsahuje dáta')
    save_frame(df, TOPDIR, shnum)
    save_frame(bad_coor_df, TOPDIR, 'ERR' + shnum)

    

def get_xlsx_to_join():
    ''' Funkcia pozrie do TOPDIR a JOINDIR a vráti zoznam xls na spájanie
    táto funkcia netestuje, či sú to súbory z vrtov alebo nie'''
    xlsfiles = (dirEntries(JOINDIR, False, 'xlsx'))
    # xlsfiles = xlsfiles.extend(TOPDIR, False, 'xlsx')
    return (xlsfiles)

def create_joined():    
    '''Spoji excel vygenerovany v TOPDIR s excelmi z ineho spracovania, ktore sa ulozia v JOINDIR 
    Je to dolezite, lebo zakladny subor do septembra 2025 obsahuje v sebe viacero rucnych zasahov
    v Geosoftovych csv suborov a jeho automaticke pregenerovanie z cistych csv suborov by viedlo 
    ku strate niektorych udajov'''
    if  os.path.isfile(EXCELJOINED):
        os.remove(EXCELJOINED)
    sheets = [SHGEO5, SHVRT, SHVRTLOZ]
    xlsfiles = get_xlsx_to_join()

    pd.DataFrame().to_excel(EXCELJOINED, sheet_name = 'info', index=0)

    for sheet in sheets:
        df_concat = pd.DataFrame()
        for xlsfile in xlsfiles:
            print(sheet, xlsfile)
            df = pd.read_excel(xlsfile, sheet_name = sheet)
            print(xlsfile, sheet, df.shape)
            df_concat = pd.concat([df_concat, df])
            print(xlsfile, sheet, df.shape, df_concat.shape)
            add_to_xls(df_concat, sheet)
import requests
def test_url(df, list):
    # for row in  df[list].iterrows():
    #     print(row)
    # return

    tested = 0
    failed = 0

    for row in  df[list].iterrows():
        myrow = row[1]
        url=myrow[list[0]]
        rest = f"{myrow[list[1]]} : {myrow[list[2]]} "
        tested += 1
        try:
            page = requests.get(url)
            # print(url, page.status_code)
            if page.status_code != 200:
                print("Err ", url, page.status_code, rest)
                failed += 1
        except Exception as err:        
            failed += 1         #(requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
            print("Err ", url, rest)
    print(f'pokusov: {tested} zlyhani {failed}')
def test_pdf_access():
    TOTEST = EXCELJOINED
    TOTEST = EXCELWB
    
    test_url(pd.read_excel(TOTEST, sheet_name='GEO5'), ['URL','Vrt', 'Uloha'])
    test_url(pd.read_excel(TOTEST, sheet_name='VRT'), ['PDF','Vrt', 'File'])
    test_url(pd.read_excel(TOTEST, sheet_name='VRTLOZ'), ['PDF','Vrt', 'File'])
    
test_pdf_access()    
exit(0)

_KML = simplekml.Kml()
FOLGEO5 = _KML.newfolder(name='GEO5')
FOLVRTLOZ = _KML.newfolder(name='VRTLOZ',visibility=0, open=0)
FOLVRT = _KML.newfolder(name='VRT', visibility=0, open=0)
FOLVRT.visibility = 0

create_joined()
wb = op.load_workbook(EXCELJOINED)
vrtygeo5 = (fKML.process_GEO5(wb, FOLGEO5))
vrty = (fKML.process_vrt(wb, FOLVRT))
vrtyloz = (fKML.process_vrt_loz(wb, FOLVRTLOZ))
_KML.save(KMLNAME)

print(f'{EXCELJOINED} obsahuje = geo5:{len(vrtygeo5)} ks, vrt:{len(vrty)} ks, vrtloz:{len(vrtyloz)} ks ...  ALL DONE')



exit(0)
#########################################




test_pdf_access()
exit(0)    


 