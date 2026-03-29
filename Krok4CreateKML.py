#from openpyxl import load_workbook
import os
import openpyxl as op
import simplekml
import csv
import logging
from _funcs import *
from _settings import *
chkdirs()
import _funcsKML as fKML

logging.basicConfig(filename = KROK4LOGFILE, level=logging.INFO, filemode='w')
logger=logging.getLogger()
# _KML = '' #global variable initialized in main

_KML = simplekml.Kml()
FOLGEO5 = _KML.newfolder(name='GEO5')
FOLVRTLOZ = _KML.newfolder(name='VRTLOZ',visibility=0, open=0)

FOLVRT = _KML.newfolder(name='VRT', visibility=0, open=0)
FOLVRT.visibility = 0

wb = op.load_workbook(EXCELWB)
vrtygeo5 = (fKML.process_GEO5(wb, FOLGEO5))
vrty = (fKML.process_vrt(wb, FOLVRT))
vrtyloz = (fKML.process_vrt_loz(wb, FOLVRTLOZ))
_KML.save(KMLNAME)
print(f'{EXCELWB} obsahuje = geo5:{len(vrtygeo5)} ks, vrt:{len(vrty)} ks, vrtloz:{len(vrtyloz)} ks ...  ALL DONE')

 