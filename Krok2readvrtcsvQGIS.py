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

# TOPDIR = r'f:\aaa\PROGRAM\python\vrty2\Vrty_2025'
# VRTCSV = r'\vrty.csv'
# VRTDATCSV = r'\vrtdat.csv'
# PATHBASEINDB = r'f:\aaa\PROGRAM\python\vrty2\Vrty_2025'
# WEBTOPDIR = r'http://172.16.0.2/dokumenty/Vrty_2025'
# PATHBASEINDB = TOPDIR

VRTCSV = r'\\' + VRTCSV
VRTDATCSV = r'\\' + VRTDATCSV


logging.basicConfig(filename = KROK2LOGFILE, level=logging.INFO)
logger=logging.getLogger()
resultfile = open(VRTCSVQGIS, 'w') # do resultfile zapisuje len CVSReader a main a uzatvara ho main 

def adjust_pdf(row):
	'''dostane kompletny riadok vrtu, v poli 0 je cislo vrtu
	v poli 1 je cesta ku suboru vrt a vráti názov pdf'''
	pdfpath0 = os.path.dirname(row[1].strip()) + '\\'
	filename = row[0]
	
	retval = 'NA'
	pdffullname = pdfpath0+ filename + '.pdf'
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
				print(pdffullname)
				retval = pdffullname
	if retval != 'NA':				
		# pdfpath = pdfpath0.replace(PATHBASEINDB, WEBTOPDIR)
		# pdfpath = pdfpath.replace('\\', '/')
		# retval = pdfpath + filename + ".pdf"
		retval = retval.replace(PATHBASEINDB, WEBTOPDIR)
		retval = retval.replace('\\', '/')
	else:
		logger.error(row[0] + ' : ' + pdfpath0 + filename + '.pdf')
		#print(row[0],retval)	
	return retval
	



def CSVReader(topdir):
    retval = _utils.Subdirs(topdir, True) #all dirs under TOPDIR
    for  dir in retval:
        #print (dir)
        #todo test for existence
        if not os.path.isfile(dir+VRTCSV):
            #print ("Warning: file {} does not exist", dir+VRTCSV)
            pass
        else:
            #privrav si dictionary s hladinami hpv = { CVRT1 : (hpvn, hpvu), CVRT2 : ...}
            hpvlist = oneVrtdatReader(dir+VRTDATCSV)
            with open(dir+VRTCSV, encoding='cp1250') as csvfile:
            #    data = csvfile.read()
            #    csvfile = re.sub('\n.*?^[^\\s]','', data,re.M )    
                try:
                    print(VRTCSV)
                    row = next(csvfile) #skip header
                    print(row)
                    vrtreader = csv.reader(csvfile, delimiter=';')
                    for row in vrtreader:
                        if (len(row) > 13): #skip not parseable rows - niektoré položky sú na viac riadkov napr. 11756
                            # row = [x.encode('ANSI').decode('cp1250') for x in row]
                            x = row[9].replace(',', '.') #JTSK
                            y = row[10].replace(',', '.')
                            if x == '': x = '0'
                            if y == '': y = '0'
                            
                            JTSK = proj4.JTSK_to_WGS(x,y) #pridaj JTSK
                            JTSK =  map(str, JTSK) #urob z toho stringy
                            row.extend(JTSK)
                            #vyčisti hĺbku
                            row[22] = row[22].strip(' ').strip('m').strip(' ').replace(',','.').replace('vrtu ','')
                            #pridaj hpv ak existuje
                            hpvresult = hpvlist[row[0]]     #cislo vrtu
                            if hpvresult == (): 
                                hpvresult=('NA')
                            hpvresult =  map(str, hpvresult) #urob z toho stringy
                            row.extend(hpvresult)
                            pdfname = adjust_pdf(row)
                            row.extend([pdfname])
                            row = [s.strip().replace('"','') for s in row] #niektore mali leading spaces
                        #    logger.info('; '.join((map(str, row)))+ ';')
                            resultfile.write('; '.join((map(str, row)))+ ';\n')
                        else:
                            logging.error("Málo položiek v zozname:" + dir + '/' + row[0])
                except Exception as err:
                     logging.error ('CSV-READER: ' + dir + '/' + row[0] + f'{err=}, {type(err)=}')
        
#sekcia vrtdat.vrt - Zatial len HPV
def oneVrtdatReader(vrtdat):
    '''fn načíta názov súboru vrtdat.vrt a pripraví list v tvare hpv = { CVRT1 : (hpvn, hpvu), CVRT2 : ...}
    tento spôsob je výhodnejší oproti viacnásobnému načítavaniu a parsovaniu vrtddat.vrt'''
    VRTREPLACE1 = re.compile(r'(?ms)Vzorky.*?Podz', re.M)  #\01900\1900097\IGI-1.pdf
    VRTREPLACE2 = re.compile(r'(?ms)Vzorky.*?námka', re.M) #nefunguje Lupca 
    VRTSPLIT = re.compile(r'\n(?=[^;\s])', re.M) #lookahead EOL not followed by semicolon rozdelí na jednotlivé vrty
    VRTSPLIT = re.compile(r'\n(?=[^;])', re.M) #lookahead EOL not followed by semicolon rozdelí na jednotlivé vrty
    if os.path.isfile(vrtdat):
        with open(vrtdat, 'r', encoding='cp1250' ) as vrtdat:
            dict_hpv = {}
            data_full =  vrtdat.read()
            #print(data_full)
            if re.search(VRTREPLACE1, data_full):
                data_full = re.sub(VRTREPLACE1,r';', data_full) #preco
            elif re.search(VRTREPLACE2, data_full):
                data_full = re.sub(VRTREPLACE2,r';', data_full) #preco
                
            #print(data_full)
            data_split = re.split(VRTSPLIT, data_full)
            for vrt in data_split:
                #print(vrt)
                dict_hpv.update(get_hpv(vrt)) #update rozbalí list2
    else:
        dict_hpv={}    
 #   print(dict_hpv)
    return(dict_hpv)



def get_hpv(vrt):
    '''fn dostane blok '''
    [vrtname, vrtfile,dummy] = re.split('[\n;]', vrt,2)
    #print(vrtfile, vrtname, vrtname == 'S-1')
    vrt = vrt.strip('\n')
    try: 
        if not vrt.endswith('Ustálená;') and vrt.find('Ustálená;') > 0:   #niektoré vrty nemajú ani hpv
            [dummy,pv] = re.split('Ustálená;\n',vrt,2)
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
        print('get_hpv: ',vrtname, vrtfile,f"ERR {err=}, {type(err)=}")  #je to trochu riziko
        hpvn = hpvu = 'NA3'
    #print(hpvn, hpvu)
    return{vrtname : (hpvn, hpvu)}

def main():
    
    print('Started')
    resultfile.write('''Vrt;File;Uloha;Priloha;Ucel;Firma;Lokalita;Okres;Kraj;JTSKX;\
JTSKY;Hteren;Hpaznica;Dielo;Etapa;Obstaravatel;Vrtal;Suprava;Vrtmajster;Doba;\
Geolog;Mierka;Hlbka;void;Lat;Lon;HPV;Na;PDF\n''')
    CSVReader(TOPDIR)
    resultfile.close()
    print ('vrty - done')
if __name__ == '__main__':
    main()

#testovacia suita
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
                print("test_headers err:", csvfile, f"ERR {err=}, {type(err)=}, err") 
    for header in headers:
        #print(header)
        pass

#test_headers(csvfn='vrty.csv')
#exit(0)

#--------------NOT USED --- YET
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


#testDictReader()
