import pandas as pd
import logging
import datetime as dt
from _settings import *
import os

def create_logger(logname):
    '''Create and return a logger with the specified name'''
    logger = logging.getLogger(logname)
    logger.addHandler(logging.FileHandler(TOPDIR + f"{dt.datetime.now().strftime('%H-%M')}-{logname}.log", mode='w'))
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)
    logger.setLevel(logging.DEBUG)
    return logger

def print_log_error(logger, msg):
    print(msg)
    logger.error(msg)

def clean_duplicates(df, typ):
    if df.shape[0]:
        if typ == SHGEO5: sortby = 'Vrt'
        elif typ == SHVRT or typ == SHVRTLOZ: sortby = 'File'
        df_dup = df.sort_values(by=sortby,ascending=True).drop_duplicates(subset=["Vrt", "JTSKX", "JTSKY"], keep='last')
        return df_dup
    else:
        return pd.DataFrame()


def bad_coordinates_df(df):
    return df[(df.JTSKY >= 595000) | (df.JTSKY <= 160000) | (df.JTSKX >= 1340000) | (df.JTSKX <= 1128000) ] # bad values
    # return df[~( 160000 < df.JTSKY < 595000) & (1128000 < df.JTSKX < 1340000)] # negate good values
 
def good_coordinates_df(df):
    return df[(df.JTSKY < 595000) & (df.JTSKY > 160000) & (df.JTSKX < 1340000) & (df.JTSKX > 1128000) ] # good values
    # return df[( 160000 < df.JTSKY < 595000) & (1128000 < df.JTSKX < 1340000)] # good values
 
def to_num(df, cols):
    '''prevedie stlpce cols na numeric'''
    for col in cols:
        df[col] = pd.to_numeric(df[col], errors='coerce', dtype_backend='numpy_nullable').astype('Float32')
        #memory usage 60347 vs 80255 bytes
        #df[col] = pd.to_numeric(df[col], errors='coerce', dtype_backend='pyarrow' ).astype(pd.ArrowDtype(pa.float64())) 
    return df


def chkdirs():
    if not os.path.exists(TOPDIR):
        print(f'FATAL TOPDIR adresar {TOPDIR} neexistuje, nepokracujem...')
        exit(-1)


