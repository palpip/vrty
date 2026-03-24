#from openpyxl import load_workbook
import os
import openpyxl as op
import simplekml
import csv
import logging
from pykml import parser
# from proj4 import JTSK_to_WGS
# from _utils import dirEntries
from _settings import *

logging.basicConfig(filename = KROK4LOGFILE, level=logging.INFO, filemode='w')
logger=logging.getLogger()
_KML = '' #global variable initialized in main


# Source - https://stackoverflow.com/a/68086563
# Posted by Lenormju
# Retrieved 2026-03-24, License - CC BY-SA 4.0

import xml.etree.ElementTree as ET
from pathlib import Path


kml_file_path = Path(r'c:\Shares\vrty\vrty3\python\joindir\kml.kml')
tree = ET.parse(kml_file_path)
root = tree.getroot()
print(root.tag)  # kml
# for placemark_node in root.findall("Document/Folder/Folder/Placemark"):
# for placemark_node in root.findall("{http://www.opengis.net/kml/2.2}Folder"):
# for placemark_node in root:    
for ch in root:
    print(ch.attrib)
    print("Placemark =====")
    for ch1 in ch:
        print("L1 ", ch1.tag,":::", ch1.text)
        for ch2 in ch1:
            print("   L2", ch2.tag,":::", ch2.text)
        for ch3 in ch2:
            print("     L3", ch3.tag,":::", ch3.text)
            for ch4 in ch3:
                print("       L4", ch4.tag,":::", ch4.text)
print(root.tag, '   ', root.text)  # kml
            
for coor in root.findall("Placemark}"):
    print(" ", coor.tag,":::", coor.text, coor)

exit(0)



with open(r'c:\Shares\vrty\vrty3\python\joindir\KML.kml', 'r', encoding="utf-8") as f:
   root = parser.parse(f).getroot()

places = []
for place in root.Document.Folder.Placemark:
    data = {item.get("name"): item.text for item in
            place.ExtendedData.SchemaData.SimpleData}
    coords = place.Polygon.outerBoundaryIs.LinearRing.coordinates.text.strip()
    data["Coordinates"] = coords
    places.append(data)
df = pd.DataFrame(places)
print(df) 