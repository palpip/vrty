''' Utilita načíta v každom podadresári TOPDIR
csv súbory vty.csv '''
#import chardet
import csv
import re #parsovanie vrtdat
import proj4
import os.path
import logging
import _utils
from _settings import *


VRTCSV = '\\' + VRTCSV
VRTDATCSV = '\\' + VRTDATCSV


# logging.basicConfig(filename = KROK2LOGFILE, level=logging.INFO, filemode='w')
logger=logging.getLogger('vrt')
logger.addHandler(logging.FileHandler(KROK2LOGFILE, mode='w'))
logger.addHandler(logging.StreamHandler())
logger.setLevel = logging.INFO
logger_pdf = logging.getLogger('pdf')
# logger_pdf.addHandler(logging.StreamHandler())
logger_pdf.addHandler(logging.FileHandler(KROK2PDF, mode='w'))
resultfile = open(VRTCSVQGIS, 'w') # do resultfile zapisuje len CVSReader a main a uzatvara ho main 

logger.info('Starting')
def adjust_pdf(dir, filename):
	'''dostane kompletny riadok vrtu, v poli 0 je cislo vrtu
	v poli 1 je cesta ku suboru vrt a vráti názov pdf'''
	pdfpath0 = dir + '\\'
	
	retval = 'NA'
	pdffullname = pdfpath0 + filename + '.pdf'
	if os.path.isfile(pdffullname): 
		# logger.warning("0 " + pdffullname)
	    # print(pdfullname)
		retval = pdffullname
	else:
		filename = 	filename.replace(' ','').replace('/','_').replace('.','_')
		pdffullname = pdfpath0 +  filename + '.pdf'
		if os.path.isfile(pdffullname):
			# logger.warning("1 " + pdffullname)
	        # print(pdfullname)
			retval = pdffullname
		else:
			filename = 	_utils.remove_dia(filename)
			# filename = bytearray(filename, 'ANSI').decode()
			# logger.warning("XXX " +  pdffullname)
			
			pdffullname = pdfpath0 +  filename + '.pdf'
			if os.path.isfile(pdffullname):
				#logger.warning("2 " +  pdffullname)
				############### print(pdffullname)
				retval = pdffullname
	if retval != 'NA':				
		# pdfpath = pdfpath0.replace(PATHBASEINDB, WEBTOPDIR)
		# pdfpath = pdfpath.replace('\\', '/')
		# retval = pdfpath + filename + ".pdf"
		retval = retval.replace(PATHBASEINDB, WEBTOPDIR)
		retval = retval.replace('\\', '/')
	else:
		logger_pdf.error('Chýba ' + pdfpath0 + filename + '.pdf')
	return retval
	

GOODROWCOUNT = 0
ALLROWCOUNT = 0

def CSVReader(topdir):
    '''Najde kazdy vrt.csv pod topdir, vytiahne data, doplni o hpv, pdf, JTSK a ulozi do resultfile.csv
    ziskanie hpv z vrtdat csv je niekedy problematick0
    '''
    global GOODROWCOUNT 
    global ALLROWCOUNT

    retval = _utils.Subdirs(topdir, True) #all dirs under TOPDIR
    for  dir in retval:
        #print (dir)
        #todo test for existence
        if not os.path.isfile(dir+VRTCSV):
            logger.warning (f"Warning: file {dir+VRTCSV} does not exist")
            pass
        else:
            #privrav si dictionary s hladinami hpv = { CVRT1 : (hpvn, hpvu), CVRT2 : ...}
            hpvlist = oneVrtdatReader(dir+VRTDATCSV)
            with open(dir+VRTCSV, encoding='cp1250') as csvfile:
            #    data = csvfile.read()
            #    csvfile = re.sub('\n.*?^[^\\s]','', data,re.M )    
                try:
                    # print(VRTCSV)
                    row = next(csvfile) #skip header
                    # print(row)
                    vrtreader = csv.reader(csvfile, delimiter=';')
                    for row in vrtreader:
                        ALLROWCOUNT += 1
                        if (len(row) >= 13): #skip not parseable rows - niektoré položky sú na viac riadkov napr. 11756
                            # row = [x.encode('ANSI').decode('cp1250') for x in row]
                            x = row[9].replace(',', '.') #JTSK
                            y = row[10].replace(',', '.')
                            if x == '': x = '0'
                            if y == '': y = '0'
                            if y < x: 
                                x, y = y, x
                                row[9], row[10] = row[10],row[9]
                            
                            JTSK = proj4.JTSK_to_WGS(x,y) #pridaj JTSK
                            JTSK =  map(str, JTSK) #urob z toho stringy
                            row.extend(JTSK)
                            #vyčisti hĺbku
                            row[22] = row[22].strip(' ').strip('m').strip(' ').replace(',','.').replace('vrtu ','')
                            #pridaj hpv ak existuje
                            key = row[0]
                            if key in hpvlist:
                                hpvresult = hpvlist[key]     #cislo vrtu
                            else: 
                                hpvresult=('NA')
                                # logger.warning(f'hpv error: {key} {row}')
                            hpvresult =  map(str, hpvresult) #urob z toho stringy
                            row.extend(hpvresult)
                            pdfname = adjust_pdf(dir, row[0])
                            row.extend([pdfname])
                            row = [s.strip().replace('"','') for s in row] #niektore mali leading spaces
                        #    logger.info('; '.join((map(str, row)))+ ';')
                            resultfile.write('; '.join((map(str, row)))+ ';\n')
                            ##### print('; '.join((map(str, row)))+ ';\n')
                            GOODROWCOUNT += 1
                        else:
                            logger.exception("Málo položiek v zozname:" + dir + '/' + row[0])
                except Exception as err:
                    logger.exception ('CSV-READER: ' + dir + '/' + row[0] + f'{err=}, {type(err)=}')
        
def oneVrtdatReader(vrtfn):
    '''fn načíta názov súboru vrtdat.vrt a pripraví list v tvare hpv = { CVRT1 : (hpvn, hpvu), CVRT2 : ...}
    tento spôsob je výhodnejší oproti viacnásobnému načítavaniu a parsovaniu vrtddat.vrt
    veľká zmena 20250909
    doteraz sa vrtdat delil na základe EOL a nasledovným začiatkom riadku bez bodkočiarky. V niektorých prípadoch, napr 11747 to
    nefungovalo. Skúsime to deliť na základe tých istých parametrov, ale v konkrétnom riadku musí byť aj meno súboru.
    '''
    VRTREPLACE1 = re.compile(r'(?ms)Vzorky.*?Podz', re.M)  #\01900\1900097\IGI-1.pdf
    VRTREPLACE2 = re.compile(r'(?ms)Vzorky.*?námka', re.M) #nefunguje Lupca 
    # VRTSPLIT0 = re.compile(r'\n(?=[^;\s])', re.M) #lookahead EOL not followed by semicolon rozdelí na jednotlivé vrty
    # VRTSPLIT00 = re.compile(r'\n(?=[^;])', re.M) #lookahead EOL not followed by semicolon rozdelí na jednotlivé vrty
    # VRTSPLIT = re.compile(r'\n(?=^[^;].*?;c:\\Shares)', re.M) #lookahead EOL not followed by semicolon rozdelí na jednotlivé vrty
    
    # lookahead EOL not followed by semicolon rozdelí na jednotlivé vrty 
    # VRTSPLIT = re.compile(r'\n(?=[^;].*?;'+ re.escape(vrtfn[:-13]) + ')', re.M) 
    VRTSPLIT = re.compile(r'\n(?=[^;].*?;)', re.M) 
 
    vrtfn
    vrtfn
    # print(VRTSPLIT, vrtdat[:-13], vrtdat)
    if os.path.isfile(vrtfn):
        with open(vrtfn, 'r', encoding='cp1250' ) as vrtdat:
            dict_hpv = {}
            data_full =  vrtdat.read()
                
            #print(data_full)
            data_split = re.split(VRTSPLIT, data_full)
            for vrt in data_split:
                # print('-----' * 3, '\n')
                # print('vrt:>',vrt,'<')
                if re.search(VRTREPLACE1, data_full):
                    data_full = re.sub(VRTREPLACE1,r';', data_full) #preco
                elif re.search(VRTREPLACE2, data_full):
                    data_full = re.sub(VRTREPLACE2,r';', data_full) #preco
            
                # print('vrt:>',vrt,'<')
                if len(vrt) > 50:
                    dict_hpv.update(get_hpv(vrt)) #update rozbalí list2
                else:
                    logger.info('len vrt {len(vrt)}')
    else:
        dict_hpv={}    
    # print(dict_hpv)
    return(dict_hpv)



def get_hpv(vrt):
    '''fn dostane blok '''
    try: 
        [vrtname, vrtfile,dummy] = re.split('[\n;]', vrt, maxsplit = 2 )
        #print(vrtfile, vrtname, vrtname == 'S-1')
        vrt = vrt.strip('\n')
    except Exception as err:
        logger.exception(f'err get_hpv1: {vrtname} {vrtfile} {err=}, {type(err)=}')  #je to trochu riziko
        return {}
    try:    
        if not vrt.endswith('Ustálená;') and vrt.find('Ustálená;') > 0:   #niektoré vrty nemajú ani hpv
            [dummy,pv] = re.split('Ustálená;\n', vrt, maxsplit=2)
            #pv=pv.strip('\n')
            #print(pv,'---', pv.strip(';'))
            if pv != '':
                hpv = pv.split('\n')
                for n, vrstva in enumerate(hpv):
                    hpv[n] = vrstva.replace('\n', '').strip(';').replace(';','-') #vyhod EOL, okrajove ; a daj rozsah
                #    print (n,vrtname, hpv[n])
                hpvn = hpv
                hpvu = 'NA0'
            else:
                hpvn = hpvu = 'NA1'    
        else:
            hpvn = hpvu = 'NA2'
    except Exception as err:
        logger.error('err get_hpv2: %s %s %s %s', vrtname, vrtfile, err, type(err))  #je to trochu riziko
        hpvn = hpvu = 'NA3'
    # print({vrtname : (hpvn, hpvu)})
    return{vrtname : (hpvn, hpvu)}

def main():
    # VRTDAT = 'c:\\Shares\\vrty\\vrty3\\python\\Vrty_202509\\10744\\vrtdat.csv'
    # res = oneVrtdatReader(VRTDAT)
    # print(res)
    # exit(0)
    # # print('Started')
    resultfile.write('''Vrt;File;Uloha;Priloha;Ucel;Firma;Lokalita;Okres;Kraj;JTSKX;\
JTSKY;Hteren;Hpaznica;Dielo;Etapa;Obstaravatel;Vrtal;Suprava;Vrtmajster;Doba;\
Geolog;Mierka;Hlbka;void;Lat;Lon;HPV;Na;PDF;\n''')
    CSVReader(TOPDIR)
    resultfile.close()
    print(f'vrty - done all={ALLROWCOUNT} good={GOODROWCOUNT}  diff={ALLROWCOUNT - GOODROWCOUNT}')

if __name__ == '__main__':
    main()

#  testovacia suita nepotrebne
#oneVrtdatReader(r'c:\Users\pp\program\python\vrty\TESTVRTDIR\10450\vrtdat1.csv')
def test_headers(topdir = TOPDIR, csvfn='vrty.csv'):
    ''' prejde podadresáre pod TOPDIR, nájde v nich súbory vrty.csv
    zozbiera UNIQUE headers a vytlačí ich'''
    headers=[]
    retvalFiles = _utils.dirEntries(topdir, True, 'csv')
    for file in retvalFiles:
        #print (file, csvfn)
        if file.find(csvfn) != -1:
            try:
                with open(file, encoding='cp1250') as csvfile:
                    vrtreader = csv.reader(csvfile, delimiter=';' )
                    row = next(vrtreader)
                    # row = [x.encode('ANSI').decode('cp1250') for x in row]
                    # print(row)
                    if row not in headers:
                        headers.append(row)
            except Exception as err:
                logger.error("test_headers chyba: %s %s %s", csvfile, err, type(err))
                print("test_headers chyba: %s %s %s", csvfile, err, type(err))
                
    for header in headers:
        #print(header)
        pass

#test_headers(csvfn='vrty.csv')
#exit(0)

def testDictReader():
    '''načítanie VRTCSV cez knižnicu csv, ktorá vlastne namiesto listu
    urobí z riadku dictionary s keys z headra. Nmá to význam, lebo
    v prípade týchto súborov sú headre variabilné.'''
    retval = _utils.Subdirs(TOPDIR, True)
    for dir in retval:
        print (dir)
        with open(dir+VRTCSV, encoding='ANSI') as csvfile:
            vrtreader = csv.DictReader(csvfile, delimiter=';')
            for row in vrtreader:
                #row = [x.encode('ANSI').decode('1250') for x in row]
                #print(row['Súradnice Y'].encode('ANSI').decode('1250'))
                #print(row[0].encode('ANSI').decode('1250')) #err
                #print(', '.join(row))
                pass

def testVrtdatReader():
    '''načítanie VRTCSV štandardným fileIO pythonu riadok po riadku'''
    retval = _utils.Subdirs(TOPDIR, True)
    VRTCSV='vrtdat.csv'
    for  dir in retval:
        print (dir)
        with open(dir+VRTCSV, encoding='ANSI') as csvfile:
            vrtreader = csv.reader(csvfile, delimiter=';')
            for row in vrtreader:
                # row = [x.encode('ANSI').decode('cp1250') for x in row]
                # print(row[1:5])
                # print(', '.join(row.encode('UTF8','replace').decode()))
                pass


