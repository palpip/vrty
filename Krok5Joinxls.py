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
from _settings import *
from _funcs import *

logging.basicConfig(filename = KROK5LOGFILE, level=logging.INFO, filemode='w')
logger=logging.getLogger()
_KML = '' #global variable initialized in main


def get_cells_dict(sheet):
    '''fn dostane sheet z ktorého vráti zoznam dictionaries
    s dátami. Je to pokus, v tejto etape budeme načítavať
    len "FieldTests"'''
    rows =[]
    i = True
    for row in sheet.rows:
        row = [cell.value for cell in row]
        if i:
            header = row
            i = False
        else: 
            rows.append(dict(zip(header, row)))
            #rows.append(zip(header, row))
    # for row in rows:
    #     print(row)
    return rows


def get_cells_dict(sheet):
    '''fn dostane sheet z ktorého vráti zoznam dictionaries
    s dátami. Je to pokus, v tejto etape budeme načítavať
    len "FieldTests"'''
    rows =[]
    i = True
    for row in sheet.rows:
        row = [cell.value for cell in row]
        if i:
            header = row
            i = False
        else: 
            rows.append(dict(zip(header, row)))
            #rows.append(zip(header, row))
    # for row in rows:
    #     print(row)
    return rows


def kmlwrite_one_point_GEO5(vrt):
    '''Používa global _KML'''
    # btext = 'čís:{}<br>'.format(vrt['Vrt'])+\
    #         'úloha:{}<br>'.format(vrt['Uloha'])+\
    #         'výška:{}<br>'.format(vrt['Hteren'])+\
    #         'hĺbka:{}<br>'.format(vrt['Hlbka'])+\
    #         'dokumentoval:{}<br>'.format(vrt['Geolog'])+\
    #         '<a href="{}"> PDF </a>'.format(vrt['URL'])
    btext = f"čís:{vrt['Vrt']}<br> \
            úloha:{vrt['Uloha']}<br> \
            výška:{vrt['Hteren']}<br> \
            hĺbka:{vrt['Hlbka']}<br> \
            'dokumentoval:{vrt['Geolog']}<br>" 
    if vrt['URL']: btext += f"<a href=\"{vrt['URL']}\">PDF</a>"
    pt = FOLGEO5.newpoint(name=vrt['Vrt'], coords=[(vrt['Lon'],vrt['Lat'])])
    # print(vrt['Názov skúšky'], vrt['Súradnica X'], vrt['Súradnica Y'],str(vrt['Lat']),str(vrt['Lon']), vrt['URL'])
    pt.description = vrt['Vrt']
    pt.balloonstyle.text = btext
    pt.style.iconstyle.color ='ffffff00' # aabbggrr
    # print(vrt['Vrt'])

def process_GEO5(wb):
    retval = []
    if SHGEO5 in wb.sheetnames:
        sheet = wb[SHGEO5]
        vrty = get_cells_dict(sheet)
        logger.info(f'GEO5  {len(vrty)}')
        for vrt in vrty:
            try:
                kmlwrite_one_point_GEO5(vrt)
                retval.append(vrt)
            except Exception as err:
                # print("READER Exception:", dir, f"{err=}, {type(err)=}") 
                logger.error("READER Exception:", dir, f"{err}, {type(err)}") 
    else:
        logger.warn('tab. GEO5 neexistuje')
    return list(retval)

def kmlwrite_one_point_vrt(vrt):
    '''Používa global _KML'''
    if '[' in vrt['HPV']:
        HPVtext = 'HPV:' +  vrt['HPV'].strip().replace("'],['", '<br>').replace("']", '<br>').replace("['", '')
    else:
        HPVtext = ''
    btext = f"čís:{vrt['Vrt']}<br> \
            úloha:{vrt['Uloha']}<br> \
            lokalita:{vrt['Lokalita']}<br> \
            výška:{vrt['Hteren']}<br> \
            hĺbka:{vrt['Hlbka']}<br> \
            {HPVtext} \
            'dokumentoval:{vrt['Geolog']}<br>" 
    if vrt['PDF']: btext += f"<a href=\"{vrt['PDF']}\">PDF</a>"

    pt = FOLVRT.newpoint(name=vrt['Vrt'], coords=[(vrt['Lon'],vrt['Lat'])])
    pt.description = vrt['Lokalita']
    pt.balloonstyle.text = btext
    pt.style.iconstyle.color ='ff00ff00' # aabbggrrdef process_vrt(wb):
    pt.visibility = 0

def process_vrt(wb):
    sheet = wb[SHVRT]
    if sheet:
        vrty = get_cells_dict(sheet)
    else:
        logger.error("list Vrt nie je")
        return
    retval = []
    for vrt in vrty:
        #(vrt['URL'], vrt['Úloha']) = get_URL_uloha(vrt['Názov skúšky'], wbname)
        try:
            kmlwrite_one_point_vrt(vrt)
            retval.append(vrt)
        except Exception as err:
            logger.error("KMLWRITER Exception: {err=}, {type(err)=}") 
    return list(retval)

def kmlwrite_one_point_vrt_loz(vrt):
    '''Používa global _KML'''
    btext = f"čís:{vrt['Vrt']}<br> \
            úloha:{vrt['Uloha']}<br> \
            lokalita:{vrt['Lokalita']}<br> \
            výška:{vrt['Hteren']}<br> \
            hĺbka:{vrt['Hlbka']}<br>"
    if vrt['PDF']: btext += f"<a href=\"{vrt['PDF']}\">PDF</a>"

    # btext0 = 'čís:{}<br>'.format(vrt['Vrt'])+ \
    #         'úloha:{}<br>'.format(vrt['Uloha'])+ \
    #         'lokalita:{}<br>'.format(vrt['Lokalita'])+ \
    #         'výška:{}<br>'.format(vrt['Hteren'])+ \
    #         'hĺbka:{}<br>'.format(vrt['Hlbka'])+\
    #         '<a href="{}">PDF</a>'.format(vrt['PDF'])
    # if btext0 != btext:
    #     print(btext0,'\n', btext)        
            

    pt = FOLVRTLOZ.newpoint(name=vrt['Vrt'], coords=[(vrt['Lon'],vrt['Lat'])])
    pt.description = vrt['Lokalita']
    pt.balloonstyle.text = btext
    pt.style.iconstyle.color ='ff00ffff' # aabbggrrdef process_vrt(wb):
    
def process_vrt_loz(wb):
    sheet = wb[SHVRTLOZ]
    if sheet:
        vrty = get_cells_dict(sheet)
    else:
        logger.error(f"list {SHVRTLOZ} nie je")
        return
    
    retval = []
    for vrt in vrty:
        #(vrt['URL'], vrt['Úloha']) = get_URL_uloha(vrt['Názov skúšky'], wbname)
        try:
            kmlwrite_one_point_vrt_loz(vrt)
            retval.append(vrt)
        except Exception as err:
            logger.error("READER Exception:", dir, f"{err=}, {type(err)=}") 
    return list(retval)

# HEADER ='''Vrt;Uloha;JTSKX;JTSKY;Hteren;Vrtal;Geolog;Hlbka;Lat;Lon;URL\n'''
# SEP = ';'


import pandas as pd


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
    xlsfiles = dirEntries(TOPDIR, False, 'xlsx')
    xlsfiles.extend(dirEntries(JOINDIR, False, 'xlsx'))
    return (xlsfiles)




def create_joined():    
    '''Spoji excel vygenerovany v TOPDIR s excelmi z ineho spracovania, ktore sa ulozia v JOINDIR 
    Je to dolezite, lebo zakladny subor do septembra 2025 obsahuje v sebe viacero rucnych zasahov
    v Geosoftovych csv suborov a jeho automaticke pregenerovanie z cistych csv suborov by viedlo 
    ku strate niektorych udajov'''
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
        


# wb = op.load_workbook(EXCELWB)
# sheet = wb[SHGEO5]
# vrty = get_cells_dict(sheet)
# vrty_df = get_cells_dict(SHGEO5)
# print(vrty_df.shape)
# exit(0)




_KML = simplekml.Kml()
FOLGEO5 = _KML.newfolder(name='GEO5')
FOLVRTLOZ = _KML.newfolder(name='VRTLOZ',visibility=0, open=0)

FOLVRT = _KML.newfolder(name='VRT', visibility=0, open=0)
FOLVRT.visibility = 0

wb = op.load_workbook(EXCELJOINED)
# vrtyDict = list()
vrty = (process_GEO5(wb))
vrty = (process_vrt(wb))
vrty = (process_vrt_loz(wb))
# print(vrty)
# for dic in vrty:
#     vrtyDict.append(dic)
# print(vrtyDict) 

_KML.save(KMLJOINED)
print('ALL DONE')


 