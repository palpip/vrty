''' Zakladne nastavenia pre pracu s vrtmi'''

TOPDIR = r'c:\Shares\vrty\vrty3\python\Vrty_202509'    #skúsiť r'./Data', teda TOPDIR by bola curdir/Data
# TOPDIR = r'c:\Shares\vrty\vrty3\python\Vrty_Geo5202506'    #skúsiť r'./Data', teda TOPDIR by bola curdir/Data
# TOPDIR = r'c:\Shares\vrty\vrty3\python\err'    #skúsiť r'./Data', teda TOPDIR by bola curdir/Data
EXPVRTLOZ = r'c:\Shares\vrty\vrty3\python\ExpVrtLozOld.exe' 
EXPVRT =  r'c:\Shares\vrty\vrty3\python\ExpVrt2025.exe'


# EXPVRTLOZ = r'f:\aaa\PROGRAM\python\vrty2\ExpVrtLozOld.exe' 
# EXPVRT = r'f:\aaa\PROGRAM\python\vrty2\ExpVrt2025.exe'

PATHBASEINDB = TOPDIR
WEBURL = r'http://172.16.0.2/dokumenty'                           #kde sa nachádza na webe    
WEBTOPDIR = WEBURL + r'/TEST'                                        #názov nového balíka
EXCELFILE = TOPDIR + r'\vrtydata.xls' #bude mat tabuľky VRT, VRTLOZ, GE05


VRTCSVQGIS = TOPDIR + r'\vrtyGIS.csv'    
VRTLOZCSVQGIS = TOPDIR + r'\vrtylozGIS.csv'
GEO5QGIS = TOPDIR + r'\GEO5QGIS.csv'

SHGEO5 = 'GEO5'
SHVRT = 'VRT'
SHVRTLOZ = 'VRTLOZ'

EXCELWB = TOPDIR + r'\vrty.xlsx'
KMLNAME = TOPDIR + r'\KML.kml'


#log files
ERRLOGFILE = TOPDIR + r'\errorLog.log'
KROK1LOGFILE = TOPDIR + r'\krok1.log'
KROK2LOGFILE = TOPDIR + r'\krok2.log'
KROK3LOGFILE = TOPDIR + r'\krok3.log'
KROK4LOGFILE = TOPDIR + r'\krok4.log'


#temporary files - výstup z ExpVrt a ExpVrtLoz, nachádzajú sa v jednotlivých úlohách
#tieto konštanty využíva Krok1Prepare.py a netreba sa o ne zaujímať.
VRTCSV = 'vrty.csv'    
VRTDATCSV = 'vrtdat.csv'
VRTLOZCSV = 'vrtloz.csv'
VRTLOZDATCSV = 'vrtlozdat.csv'

