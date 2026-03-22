rem .\.venv\scripts\activate.bat
rem nacita surove data z Geo5, Vrt, VrtLoz a vytvori csv
.\.venv\scripts\python Krok2ReadGeo5.py
.\.venv\scripts\python Krok2readvrtcsvQGIS.py
.\.venv\scripts\python Krok2ReadVrtLozCSVQGIS.py
pause
rem vytvori vrty.xlsx
.\.venv\scripts\python Krok3importcsv.py
pause
rem z xlsx vytvori kml.kml
.\.venv\scripts\python Krok4CreateKML.py


