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
    pt.style.iconstyle.color ='ff00ff00' # aabbggrr

def process_GEO5(wb):
    retval = []
    if SHGEO5 in wb.sheetnames:
        sheet = wb[SHGEO5]
        vrty = get_cells_dict(sheet)
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
    pt.style.iconstyle.color ='ffffffff' # aabbggrrdef process_vrt(wb):
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
    pt.style.iconstyle.color ='dd00ff00' # aabbggrrdef process_vrt(wb):
    
def process_vrt_loz(wb):
    sheet = wb[SHVRTLOZ]
    if sheet:
        vrty = get_cells_dict(sheet)
    else:
        logger.error("list Vrtloz nie je")
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
# print(vrty)
# for dic in vrty:
#     vrtyDict.append(dic)
# print(vrtyDict) 

_KML.save(KMLNAME)
print('ALL DONE')


 