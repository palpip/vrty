'''Testovaci modul na pyproj'''
import pyproj 
testData = [
    [-409182.98979439994, -1222029.386833282],
    [409182.98979439994, 1222029.386833282],
    [-409182.98979439994, 1222029.386833282],
    [1222029.386833282,-409182.98979439994],
    [-1222029.386833282,-409182.98979439994],
    [1222029.386833282,409182.98979439994],
]
testDataSKPOS =[
    [401732.137,1216049.224,48.8578747,19.3512488],
    [401732.127,1216049.224,48.8578747,19.3512488]
]

transform5514ToWGS = pyproj.Transformer.from_crs(5514,4326) 
  
def test():
    transformer = pyproj.Transformer.from_crs(4326, 5514) 
    print(transformer.transform(48.7994, 19.2559))
    transform5514ToWGS = pyproj.Transformer.from_crs(5514,4326) 
    print(transform5514ToWGS.transform(-409182.98979439994, -1222029.386833282))


def get_crs_list(): 
    crs_info_list = pyproj.database.query_crs_info(auth_name=None, pj_types=None) 
    crs_list = ["EPSG:" + info[1] for info in crs_info_list] 
    print(crs_list) 
    return sorted(crs_list) 

def JTSK_to_WGS(x, y):
    '''input string x a y v JTSK. Funkcia otestuje formát, pridá záporné hodnoty ak treba a prehodí poradie
    fn nastaví formáty pre ESPG5514, ak treba ESPG5513, treba urobiť swap alebo '''
    #niektoré súradnice majú koncoku ' m'. Odstrániť
    #print(y)
    if x == '': x = 0
    if y == '': y = 0
    x = x.replace(' m', '')
    y = y.replace(' m', '')
     
    x = abs(float(x))
    y = abs(float(y))
    xret = yret = 0
    if 1.0e6 < x < 1.5e6: yret = -x
    if 1.7e5 < y < 7e5: xret = -y
    if 1.0e6 < y < 1.5e6: yret = -y
    if 1.7e5 < x < 7e5: xret = - x
    #print (x, y, xret, yret, transform5514ToWGS.transform(xret,yret))
    return(transform5514ToWGS.transform(xret,yret))  

for test in testData:
    #JTSK_to_WGS(test[0], test[1])
    JTSK_to_WGS(str(test[0]), str(test[1]))
    #JTSK_to_WGS(test[0], test[1])

#obmedzenia 10e6-13e6
#get_crs_list()