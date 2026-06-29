
.\.venv\scripts\python Krok1Prepare.py
@echo "spustenie krokov 1 - 5 - teda až po spojenie a vygenerovanie spojeného xls a kml"
@echo "exportovan0 údaje zo súborov *vrt a vrl v dávke"
rem @pause


.\.venv\scripts\python Krok2ReadGeo5.py
.\.venv\scripts\python Krok2readvrtcsvQGIS.py
.\.venv\scripts\python Krok2ReadVrtLozCSVQGIS.py
@echo "vytvorené 3 súbory csv z dávky pre jednotlivé typy vrtov, umiestnené v TOPDIR"
rem @pause

.\.venv\scripts\python Krok3importcsvPandas.py
@echo "spojené 3 csv z dávky do jediného xls, umiestnené v TOPDIR a jeho kópia v joindir"
rem @pause
.\.venv\scripts\python Krok4CreateKML.py
@echo "zo spojeného xls vytvorené kml dávky v TOPDIR"
rem @pause
.\.venv\scripts\python Krok5Joinxls.py
@echo "zo xlsx súborov dávok v joindir vytvorené spojené xlsx a spojené kml"
@echo "v pripravte pdf súbory v http serveri a spustite test - krok6"
@pause
.\.venv\scripts\python Krok6TestKML.py

