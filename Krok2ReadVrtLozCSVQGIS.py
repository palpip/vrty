''' Utilita načíta v každom podadresári TOPDIR
csv súbory vty.csv '''
import csv
import re #parsovanie vrtdat
import _utils
import proj4
import os.path
import logging
from _funcs import chkdirs
from _settings import *
chkdirs()

VRTLOZCSV = r'\\' + VRTLOZCSV
VRTLOZDATCSV = r'\\' + VRTLOZDATCSV 


logger=logging.getLogger('vrt')
logger.addHandler(logging.FileHandler(KROK2LOGFILE, mode='a'))
logger.addHandler(logging.StreamHandler())
logger_pdf = logging.getLogger('pdf')
logger_pdf.addHandler(logging.StreamHandler())
logger_pdf.addHandler(logging.FileHandler(KROK2PDF, mode='a'))
resultfile = open(VRTLOZCSVQGIS, 'w') # do resultfile zapisuje len CVSReader a main a uzatvara ho main 

def adjust_pdf(dir, filename):
	'''dostane kompletny riadok vrtu, v poli 0 je cislo vrtu
	v poli 1 je cesta ku suboru vrt a vráti názov pdf'''
	pdfpath0 = dir + '\\'
	retval = 'NA'
	pdffullname = pdfpath0+ filename + '.pdf'
	if os.path.isfile(pdffullname): 
		#logger.warning("0 " + pdffullname)
	#	print(pdfullname)
		retval = pdffullname
	else:
		filename = 	filename.replace(' ','').replace('/','_').replace('.','_')
		pdffullname = pdfpath0 +  filename + '.pdf'
		if os.path.isfile(pdffullname):
			#logger.warning("1 " + pdffullname)
	#		print(pdfullname)
			retval = pdffullname
		else:
			filename = 	_utils.remove_dia(filename)
			pdffullname = pdfpath0 +  filename + '.pdf'
			if os.path.isfile(pdffullname):
				#logger.warning("2 " +  pdffullname)
				print(pdffullname)
				retval = pdffullname
	if retval == 'NA':				
		retval = pdfpath0 + filename + '.pdf'
		logger_pdf.error(f'{retval}  nenajdene, polozka pripravena')

	retval = retval.replace(PATHBASEINDB, WEBTOPDIR)
	retval = retval.replace('\\', '/')
	return retval

GOODROWCOUNT = 0
ALLROWCOUNT = 0

def CSVReader(topdir):

    global GOODROWCOUNT 
    global ALLROWCOUNT

    retval = _utils.Subdirs(topdir, True) #all dirs under TOPDIR
    for  dir in retval:
        print (dir)
        #todo test for existence
        if not os.path.isfile(dir+VRTLOZCSV):
            pass
        elif os.path.getsize(dir+VRTLOZCSV) == 0 :
            logger.error("Warning: Súbor %s má nulovú veľkosť", dir+VRTLOZCSV)
        else:
            #privrav si dictionary s hladinami hpv = { CVRT1 : (hpvn, hpvu), CVRT2 : ...}
            hpvlist = oneVrtdatReader(dir+VRTLOZDATCSV)
            with open(dir+VRTLOZCSV, encoding='cp1250') as csvfile:
            #    data = csvfile.read()
            #    csvfile = re.sub('\n.*?^[^\\s]','', data,re.M )    
                try:
                    row = next(csvfile) #skip header
                    vrtreader = csv.reader(csvfile, delimiter=';')
                    for row in vrtreader:
                        ALLROWCOUNT += 1
                        if (len(row) > 13): #skip not parseable rows - niektoré položky sú na viac riadkov napr. 11756
                            # row = [x.encode('ANSI').decode('cp1250') for x in row]
                            x = row[10].replace(',', '.') #JTSK
                            y = row[11].replace(',', '.')
                            if x == '': x = '0'
                            if y == '': y = '0'
                            if y < x: 
                                x, y = y, x
                                row[11], row[10] = row[10],row[11]
                            
                            JTSK = proj4.JTSK_to_WGS(x,y) #pridaj JTSK
                            JTSK =  map(str, JTSK) #urob z toho stringy
                            row.extend(JTSK)
                            # OPRAVA
                            # pdfname = adjust_pdf(row)
                            pdfname = adjust_pdf(dir, row[0])
                            
                            row.extend([pdfname])
                            resultfile.write('; '.join((map(str, row)))+ ';\n')
                            GOODROWCOUNT += 1
                        else:
                            print("Málo položiek v zozname:", dir, row)
                            logger.error("Málo položiek v zozname:", dir, row)
                except Exception as err:
                    logger.error("READER csv Exception:%s %s %s ", dir , err, type(err))
                    print("READER csv Exception:", dir,  f"{err=}, {type(err)=}")
#sekcia vrtdat.vrt - Zatial len HPV
def oneVrtdatReader(vrtdat):
    '''fn načíta názov súboru vrtdat.vrt a pripraví list v tvare hpv = { CVRT1 : (hpvn, hpvu), CVRT2 : ...}
    tento spôsob je výhodnejší oproti viacnásobnému načítavaniu a parsovaniu vrtddat.vrt'''
    VRTREPLACE1 = re.compile(r'(?ms)Vzorky.*?Podz', re.M)  
    VRTSPLIT = re.compile(r'\n(?=[^;\s])', re.M) #lookahead EOL not followed by semicolon rozdelí na jednotlivé vrty
    VRTSPLIT = re.compile(r'\n(?=[^;])', re.M) #lookahead EOL not followed by semicolon rozdelí na jednotlivé vrty
    if os.path.isfile(vrtdat):
        with open(vrtdat, 'r', encoding='cp1250' ) as vrtd:
            dict_hpv = {}
            try:
                data_full =  vrtd.read()
                #print(data_full)
                data_full = re.sub(VRTREPLACE1,r';', data_full)
                #print(data_full)
                data_split = re.split(VRTSPLIT, data_full)
                for vrt in data_split:
                    dict_hpv.update(get_hpv(vrt)) #update rozbalí list2
            except Exception as err:
                logger.error("Exception: %s %s %s", vrtdat, err, type(err))
    
    else:
        dict_hpv={}    
    return(dict_hpv)



def get_hpv(vrt):
    '''fn dostane blok '''
    if vrt == '':
         return {}
    try:
        [vrtname, vrtfile,dummy] = re.split('[\n;]', vrt, maxsplit = 2)
    except Exception as err:
        logger.error('get_hpv: ', vrt, f"ERR {err=}, {type(err)=}")  #je to trochu riziko
    
    try: 
        if not vrt.endswith('Ustálená;') and vrt.find('Ustálená;') > 0:   #niektoré vrty nemajú ani hpv
            [dummy,pv] = re.split('Ustálená;\n',vrt,2)
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
        logger.error('get_hpv: ',vrtname, vrtfile,f"ERR {err=}, {type(err)=}")  #je to trochu riziko
        hpvn = hpvu = 'NA3'
    #print(hpvn, hpvu)
    return{vrtname : (hpvn, hpvu)}

def main():
    
    print('Started')
    resultfile.write('''Vrt;File;Uloha;CUloha;Firma;Lokalita;Kataster;Okres;Kraj;\
Listmapy;JTSKX;JTSKY;Hteren;PocvaJTSKX;PocvaJTSKY;HPocva;DobaOd;DobaDo;Hlbka;Druhvrtu;\
SposobReal;Uklon;Smer;Vrtal;Mierka;NA;Lat;Lon;PDF;\n''')
    CSVReader(TOPDIR)
    resultfile.close()
    print(f'lozvrty - done all={ALLROWCOUNT} good={GOODROWCOUNT}  diff={ALLROWCOUNT - GOODROWCOUNT}')

    print ('lozvrty - done')
if __name__ == '__main__':
    main()

