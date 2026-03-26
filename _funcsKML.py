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

LOZVRTCOLOR = 'ffff0000' # aabbggrr def process_vrt(wb):
VRTCOLOR =    'ff00ff00'
GEO5COLOR =   'fffff00f'

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


def process_GEO5(wb, folgeo5):
    def kmlwrite_one_point_GEO5(vrt):
        btext = f"čís:{vrt['Vrt']}<br> \
                úloha:{vrt['Uloha']}<br> \
                výška:{vrt['Hteren']}<br> \
                hĺbka:{vrt['Hlbka']}<br> \
                'dokumentoval:{vrt['Geolog']}<br>" 
        if vrt['URL']: btext += f"<a href=\"{vrt['URL']}\">PDF</a>"
        pt = folgeo5.newpoint(name=vrt['Vrt'], coords=[(vrt['Lon'],vrt['Lat'])])
        pt.description = vrt['Vrt']
        pt.balloonstyle.text = btext
        pt.style.iconstyle.color = GEO5COLOR # aabbggrr
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


def process_vrt(wb, folvrt):
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

        pt = folvrt.newpoint(name=vrt['Vrt'], coords=[(vrt['Lon'],vrt['Lat'])])
        pt.description = vrt['Lokalita']
        pt.balloonstyle.text = btext
        pt.style.iconstyle.color = VRTCOLOR # aabbggrrdef process_vrt(wb):
        pt.visibility = 0
    sheet = wb[SHVRT]
    if sheet:
        vrty = get_cells_dict(sheet)
    else:
        logger.error("list Vrt nie je")
        return
    retval = []
    for vrt in vrty:
        try:
            kmlwrite_one_point_vrt(vrt)
            retval.append(vrt)
        except Exception as err:
            logger.error("KMLWRITER Exception: {err=}, {type(err)=}") 
    return list(retval)

    
def process_vrt_loz(wb, folvrtloz):
    def kmlwrite_one_point_vrt_loz(vrt):
        btext = f"čís:{vrt['Vrt']}<br> \
                úloha:{vrt['Uloha']}<br> \
                lokalita:{vrt['Lokalita']}<br> \
                výška:{vrt['Hteren']}<br> \
                hĺbka:{vrt['Hlbka']}<br>"
        if vrt['PDF']: btext += f"<a href=\"{vrt['PDF']}\">PDF</a>"
        pt = folvrtloz.newpoint(name=vrt['Vrt'], coords=[(vrt['Lon'],vrt['Lat'])])
        pt.description = vrt['Lokalita']
        pt.balloonstyle.text = btext
        pt.style.iconstyle.color = LOZVRTCOLOR # aabbggrrdef process_vrt(wb):

    sheet = wb[SHVRTLOZ]
    if sheet:
        vrty = get_cells_dict(sheet)
    else:
        logger.error("list Vrtloz nie je")
        return
    retval = []
    for vrt in vrty:
        try:
            kmlwrite_one_point_vrt_loz(vrt)
            retval.append(vrt)
        except Exception as err:
            logger.error("READER Exception:", dir, f"{err=}, {type(err)=}") 
    return list(retval)

