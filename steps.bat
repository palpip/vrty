
@echo "spustenie krokov 1 - 5 - teda až po spojenie a vygenerovanie spojeného xls a kml"
@echo "exportujem údaje zo súborov *vrt a vrl v dávke"
.\.venv\scripts\python Krok1Prepare.py
@echo "vytvrímam csv dávky pre jednotlivé typy vrtov a umiestnim ich do TOPDIR"
@pause

.\.venv\scripts\python Krok2ReadGeo5.py
.\.venv\scripts\python Krok2readvrtcsvQGIS.py
.\.venv\scripts\python Krok2ReadVrtLozCSVQGIS.py
@echo "vytvorrím spojím csv dávky do jediného xls a umiestnim ho do TOPDIR a jeho kópiu do joindir"
@pause
.\.venv\scripts\python Krok3importcsvPandas.py
@echo "zo spojeného xls vytvorím kml dávky"
@pause
.\.venv\scripts\python Krok4CreateKML.py
@echo "zo xlsx súborov dávok v joindir vytvorím spojené xlsx a spojené kml"
@pause
.\.venv\scripts\python Krok5Joinxls.py
@echo "hotovo"
