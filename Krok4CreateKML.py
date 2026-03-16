#from openpyxl import load_workbook
import os
import openpyxl as op
import simplekml
import csv
import logging
# from proj4 import JTSK_to_WGS
# from _utils import dirEntries
from _settings import *

logging.basicConfig(filename = KROK4LOGFILE, level=logging.INFO, filemode='w')
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

def kmlwrite_one_point_GEO5(vrt):
    '''Používa global _KML'''
    btext = 'čís:{}<br>'.format(vrt['Vrt'])+\
            'úloha:{}<br>'.format(vrt['Uloha'])+\
            'výška:{}<br>'.format(vrt['Hteren'])+\
            'hĺbka:{}<br>'.format(vrt['Hlbka'])+\
            'dokumentoval:{}<br>'.format(vrt['Geolog'])+\
            '<a href="{}"> PDF </a>'.format(vrt['URL'])

    pt = FOLGEO5.newpoint(name=vrt['Vrt'], coords=[(vrt['Lon'],vrt['Lat'])])
    # print(vrt['Názov skúšky'], vrt['Súradnica X'], vrt['Súradnica Y'],str(vrt['Lat']),str(vrt['Lon']), vrt['URL'])
    pt.description = vrt['Vrt']
    pt.balloonstyle.text = btext
    pt.style.iconstyle.color ='ff00ff00' # aabbggrr

def process_GEO5(wb):
    sheet = wb[SHGEO5]
    if sheet:
        vrty = get_cells_dict(sheet)
    else:
        print("list GEO5 nie je")
        return
    retval = []
    for vrt in vrty:
        try:
            kmlwrite_one_point_GEO5(vrt)
            retval.append(vrt)
        except Exception as err:
            print("READER Exception:", dir, f"{err=}, {type(err)=}") 
            logger.error("READER Exception:", dir, f"{err=}, {type(err)=}") 
    return list(retval)

def kmlwrite_one_point_vrt(vrt):
    '''Používa global _KML'''
    HPVtext = vrt['HPV']
    if (HPVtext != ' NA2'):
        HPVtext = 'HPV:<br>' +  HPVtext.replace("'],['", '<br>').replace("']", '<br>').replace("['", '')
    btext = 'čís:{}<br>'.format(vrt['Vrt'])+\
            'úloha:{}<br>'.format(vrt['Uloha'])+\
            'lokalita:{}<br>'.format(vrt['Lokalita'])+\
            'výška:{}<br>'.format(vrt['Hteren'])+\
            'hĺbka:{}<br>'.format(vrt['Hlbka'])+\
            'dokumentoval:{}<br>'.format(vrt['Geolog'])+\
            HPVtext+\
            '<a href="{}"> PDF </a>'.format(vrt['PDF'])

    pt = FOLVRT.newpoint(name=vrt['Vrt'], coords=[(vrt['Lon'],vrt['Lat'])])
    pt.description = vrt['Lokalita']
    pt.balloonstyle.text = btext
    pt.style.iconstyle.color ='ffffffff' # aabbggrrdef process_vrt(wb):
    pt.visibility = 0

def process_vrt(wb):
    sheet = wb[SHVRT]
    if sheet:
        vrty = get_cells_dict(sheet)
    else:
        print("list Vrt nie je")
        return
    retval = []
    for vrt in vrty:
        #(vrt['URL'], vrt['Úloha']) = get_URL_uloha(vrt['Názov skúšky'], wbname)
        try:
            kmlwrite_one_point_vrt(vrt)
            retval.append(vrt)
        except Exception as err:
            print("READER Exception:", dir, f"{err=}, {type(err)=}") 
            logger.error("READER Exception:", dir, f"{err=}, {type(err)=}") 
    return list(retval)

def kmlwrite_one_point_vrt_loz(vrt):
    '''Používa global _KML'''
    btext = 'čís:{}<br>'.format(vrt['Vrt'])+\
            'úloha:{}<br>'.format(vrt['Uloha'])+\
            'lokalita:{}<br>'.format(vrt['Lokalita'])+\
            'výška:{}<br>'.format(vrt['Hteren'])+\
            'hĺbka:{}<br>'.format(vrt['Hlbka'])+\
            '<a href="{}"> PDF </a>'.format(vrt['PDF'])

    pt = FOLVRTLOZ.newpoint(name=vrt['Vrt'], coords=[(vrt['Lon'],vrt['Lat'])])
    pt.description = vrt['Lokalita']
    pt.balloonstyle.text = btext
    pt.style.iconstyle.color ='dd00ff00' # aabbggrrdef process_vrt(wb):
    
def process_vrt_loz(wb):
    sheet = wb[SHVRTLOZ]
    if sheet:
        vrty = get_cells_dict(sheet)
    else:
        print("list Vrt loz nie je")
        return
    retval = []
    for vrt in vrty:
        #(vrt['URL'], vrt['Úloha']) = get_URL_uloha(vrt['Názov skúšky'], wbname)
        try:
            kmlwrite_one_point_vrt_loz(vrt)
            retval.append(vrt)
        except Exception as err:
            print("READER Exception:", dir, f"{err=}, {type(err)=}") 
            logger.error("READER Exception:", dir, f"{err=}, {type(err)=}") 
    return list(retval)

# def process_workbook(wbname = EXCELWB):
#     wb = op.load_workbook(wbname)
#     sheet = wb['FieldTests']
#     if sheet:
#         vrty = get_cells_dict(sheet)
#     else:
#         print(wbname, "neni")
#         return
#     retval = []
#     for vrt in vrty:
#         # [vrt['Lat'], vrt['Lon']] =JTSK_to_WGS(str(vrt['Súradnica X']),str(vrt['Súradnica Y'])) #pridáme WGS
#         # (vrt['URL'], vrt['Úloha']) = get_URL_uloha(vrt['Názov skúšky'], wbname)
#         try:
#             #kmlwrite_one_point_extended(vrt)
#             kmlwrite_one_point_balloon(vrt)
#             retval.append(vrt)
#         except Exception as err:
#             print("READER Exception:", dir, f"{err=}, {type(err)=}") 
#             logger.error("READER Exception:", dir, f"{err=}, {type(err)=}") 
#     return list(retval)
    
# HEADER1 = ['Názov skúšky',	'Template',	'Súradnica X', 'Súradnica Y', 'Súradnica Z','Posun počiatku',\
#         'Súradnica Z pažnice', 'Príloha č.', 'Vrtmajster', 'Dokumentoval', 'Dátum zač.', 'Dátum kon.']
# HEADER2 = ['Názov skúšky',	'Template',	'Súradnica X', 'Súradnica Y', 'Súradnica Z','Posun počiatku',\
#         'Príloha č.', 'Vrtmajster',	'Dokumentoval',	'Dátum zač.', 'Dátum kon.',\
#         'Poznámky k vrtu	Dáta - Skúška|Vrtná súprava']
# HEADERCSV ='''Vrt;File;Uloha;Priloha;Ucel;Firma;Lokalita;Okres;Kraj;JTSKX;\
#         JTSKY;Hteren;Hpaznica;Dielo;Etapa;Obstaravatel;Vrtal;Suprava;Vrtmajster;Doba;\
#          Geolog;Mierka;Hlbka;void;Lat;Lon;HPV;Na;URL\n'''

# HEADER =['Vrt','File','Uloha','Priloha','Ucel','Firma','Lokalita','Okres','Kraj','JTSKX','\
#         JTSKY','Hteren','Hpaznica','Dielo','Etapa','Obstaravatel','Vrtal','Suprava','Vrtmajster','Doba','\
#         Geolog','Mierka','Hlbka','void','Lat','Lon','HPV','Na','URL']

HEADER ='''Vrt;Uloha;JTSKX;JTSKY;Hteren;Vrtal;Geolog;Hlbka;Lat;Lon;URL\n'''
# SEP = ';'



_KML = simplekml.Kml()
FOLGEO5 = _KML.newfolder(name='GEO5')
FOLVRTLOZ = _KML.newfolder(name='VRTLOZ',visibility=0, open=0)

FOLVRT = _KML.newfolder(name='VRT', visibility=0, open=0)
FOLVRT.visibility = 0

wb = op.load_workbook(EXCELWB)
# vrtyDict = list()
vrty = (process_GEO5(wb))
vrty = (process_vrt(wb))

vrty = (process_vrt_loz(wb))
print(vrty)
# for dic in vrty:
#     vrtyDict.append(dic)
# print(vrtyDict) 

_KML.save(KMLNAME)


print('DONE')


 