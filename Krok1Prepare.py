''' 
Dávková konverzia súborov vrl a vrt na csv

Utilita spustí v každom podadresári TOPDIR program EXPVRT a EXPRVTLOZ a vygeneruje tam csv súbory 
Opatrne, lebo niektoré vrt.csv sú vadné, treba opraviť a pouťívajú sa ručne upravené csv v adresároch
ERRDIRS v _settings.py. Tento program súbory v ERRDIRS negeneruje, len kontroluje ich prítomnosť.

'''

import _utils
import subprocess
import os
import glob
import logging
from _funcs import chkdirs
from _settings import *
chkdirs()
logging.basicConfig(filename = KROK1LOGFILE, level=logging.DEBUG, filemode='w')
logger=logging.getLogger(name='ccc')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO)
print(logging.BASIC_FORMAT)

SEP = '\\' # window
def Prepare(subdirs):
    for  dir in subdirs:
        nodir = dir.replace(TOPDIR, '').split(SEP)
        if nodir[1] in ERRDIRS:
            print(f'zakazane spracovat {nodir[1]}')
        else:
            os.chdir(dir)
            #cleanup - vymaze csv subory na vrty
            if os.path.isfile(VRTCSV): os.remove(VRTCSV)
            if os.path.isfile(VRTDATCSV): os.remove(VRTDATCSV)
            # not blocking - nepouzite, lebo
            #  niektore csv neboli dokoncene
            subprocess.call(EXPVRT) # blocking
            #print(dir, os.path.isfile(VRTCSV) , os.path.isfile(VRTDATCSV), len(glob.glob('*.vrt')))
            #ak mal vytvorit csv, lebo je tam *.vrt a nevytvoril, print errmsg
            if (not os.path.isfile(VRTCSV)) or (not os.path.isfile(VRTDATCSV)):
                if len(glob.glob('*.vrt')) > 0:
                    logger.error('nevygeneroval csv v ' + dir + str(len(glob.glob('*.vrt')))) 
                else:
                    logger.debug('v adresari nie je *.vrt ' + dir)
            else:
                logger.info('csv vygenerované ' + dir) 
                # print('INFO csv vygenerované ' + dir) 

def PrepareLoz(subdirs):
    for  dir in subdirs:
        nodir = dir.replace(TOPDIR, '').split(SEP)
        if nodir[1] in ERRDIRS:
            print(f'zakazane spracovat {nodir[1]}')
        else:
            os.chdir(dir)
            
            #cleanup - vymaze csv subory na vrty
            if os.path.isfile(VRTLOZCSV): os.remove(VRTLOZCSV)
            if os.path.isfile(VRTLOZDATCSV): os.remove(VRTLOZDATCSV)
            # not blocking - nepouzite, lebo niektore csv neboli dokoncene
            # subprocess.Popen(EXPVRT)
            #print(dir, os.path.isfile('vrty.csv') , os.path.isfile('vrtdat.csv'))
            subprocess.call(EXPVRTLOZ ) # blocking
            #print(dir, os.path.isfile(VRTLOZCSV) , os.path.isfile(VRTLOZDATCSV), len(glob.glob('*.vrl')))
            #ak mal vytvorit csv, lebo je tam *.vrt a nevytvoril, print errmsg
            if (not os.path.isfile(VRTLOZCSV)) or (not os.path.isfile(VRTLOZDATCSV)):
                if len(glob.glob('*.vrl')) > 0:
                    logger.error('nevygeneroval csv v ' + dir + str(len(glob.glob('*.vrl')))) 
                else:
                    logger.debug('v adresari nie je *.vrl ' + dir)
            else:
                logger.info('csv vygenerované ' + dir) 
                # print('INFO csv vygenerované ' + dir) 

chkdirs()
subs = _utils.Subdirs(TOPDIR, True)
#eliminuj ERRDIRS
SEP = '\\' # window
PrepareLoz(subs)
Prepare(subs)
print ('hotovo')
