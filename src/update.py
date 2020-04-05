import urllib
import configparser
import datetime as dt
from loguru import logger
import pandas as pd
import os
import pickle

from vectorizer import Vectorizer

def _process_data(df):
    df = df.fillna(" ")
    df = df.assign(title_vect=Vectorizer.vectorize_sents(df["title"].values))
    return df

def _update_config(config, value):
    config.set("STATUS", "LAST_UPDATED", value=value) 
    with open("../config.cfg", "w+") as fp:
        config.write(fp)
        
def update():
    config = configparser.ConfigParser()
    config.read("../config.cfg")
    url = config.get("DATA", "META_DATA_URL")
    data_dir = config.get("DATA", "DATA_DIR")
    last_updated = dt.datetime.strptime(config.get("STATUS", "LAST_UPDATED"), '%d-%m-%Y').date()
    date_now = dt.datetime.now().date()
    
    if (date_now==last_updated) and os.path.exists(data_dir+"/metadata.csv"):
        logger.info("Data Already Updated Today, no need to update again, Relaoding Instead!")
    else:
        logger.info('Downloading Data... Please Wait')
        f_name, htm = urllib.request.urlretrieve(url, f"{data_dir}/metadata.csv")
        logger.info(f'Data Downloaded!\n {htm.items()}')
        
        logger.info('Processing Data... Please Wait')
        df = pd.read_csv(f_name)
        df = df[["title", "abstract", "publish_time", "authors", "journal", "source_x", "url"]].fillna(" ")
        df = _process_data(df)
        with open(data_dir+"/processed_metadata.pickle", "wb") as f:
            pickle.dump(df, f)
        logger.info(f'Data Processed\n')
        _update_config(config, date_now.strftime('%d-%m-%Y'))
        logger.info("Updating Config")
        logger.info("Updated Processed File Created!")
    

        
    