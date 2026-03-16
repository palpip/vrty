from _settings import *
import pandas as pd
print(TOPDIR)
#delimiter je SK, bad_lines vypíše a skipne, index_col=False - neberie prvý stĺpec ako index
df = pd.read_csv(VRTCSVQGIS, delimiter=';', on_bad_lines='warn', index_col=False)
pd.set_option('display.max_colwidth', 1000)
pd.set_option('display.max_rows', None)
#tu je problem, lebo neviem zobrazit kompletny riadok 10053
dupl = df[df.duplicated(subset=["Vrt", "Uloha", "JTSKX", "JTSKY"], keep='first')].sort_values(by=["Vrt", "File"]).loc[:,["Vrt", "File", "JTSKX", "JTSKY"]]
print(dupl)
