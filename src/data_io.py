import pandas as pd
import configparser
import json
import glob
import os
from loguru import logger
from vectorizer import Vectorizer
import pickle
import urllib
import re


class DataIO(object):
    def __init__(self, config_path="config.cfg", autoload=True):
        self.config_path = config_path
        self.autoload = autoload
        
        config = configparser.ConfigParser()
        config.read(config_path)
        self.DATA_DIR = config.get("DATA", "DATA_DIR")
        
        self.df = pd.DataFrame()
        if autoload:
            self._load_metadata()
            
        
    def __str__(self):
        return f"DATA_DIR:{self.DATA_DIR}, df_loaded:{not self.df.empty}, df_shape:{self.df.shape}, autoload:{self.autoload}, config_path:{self.config_path}"
    
    def __repr__(self):
        return self.__str__()
    
    def _get_new_url(self):
        d = urllib.request.urlopen(url="https://pages.semanticscholar.org/coronavirus-research") 
        if d.status==200:
            con = d.read()
            return re.findall('<a href="(https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/.{10}/metadata.csv)">', str(con))[0]
        else:
            return None
    
    def update(self):
        url = self._get_new_url()
        if url:
            logger.info('Downloading Data... Please Wait')
            f_name, htm = urllib.request.urlretrieve(url, f"{self.DATA_DIR}/metadata.csv")
            logger.info(f'Data Downloaded!\n {htm.items()}')

            logger.info('Processing Data... Please Wait')
            df = pd.read_csv(f_name)
            df = df[["title", "abstract", "publish_time", "authors", "journal", "source_x", "url"]].fillna(" ")
            self.df = self.get_data()
            df = self.df[~self.df["title"].isin(df["title"])]
            if df.empty:
                logger.info("No New data to update")
            else:
                logger.info(f"New Data after last run: {df.shape}")
                df["title_vect"] = df["title"].apply(Vectorizer.vectorize_sent)
                self.df = pd.concat([self.df, df],ignore_index=True)
                logger.info(f'Data Processed\n')
                self._write_pickle(filename=self.DATA_DIR+"/processed_metadata.pickle")
                logger.info("Updated Processed File Created!")
            return self.df
        else:
            logger.warning("Update Failed")
            return pd.DataFrame()
    
    def load_sample(self):
        df = pd.read_csv(f"{self.DATA_DIR}/sample_metadata.csv")
        df = df[["title", "abstract", "publish_time", "authors", "journal", "source_x", "url"]].fillna(" ")
        df["title_vect"] = df["title"].apply(Vectorizer.vectorize_sent)
        self.df = df
        return self.df
        
    def _write_pickle(self, filename):
        logger.info("Writing Pickle Data to disk")
        with open(filename, "wb") as f:
            pickle.dump(self.df, f)
    
    def _load_pickle(self, filename):
        with open(filename, "rb") as fp:
                self.df = pickle.load(fp)
        return self.df
    
#     def _process_data(self):
#         self.df = self.df.fillna(" ")
#         self.df = self.df.assign(title_vect=Vectorizer.vectorize_sents(self.df["title"].values))
#         return self.df
        
#     def _load_data_v1(self):
#         logger.info(f"Loading json data from {self.DATA_DIR}")
#         fl = glob.glob(os.path.join(self.DATA_DIR, "*"))
#         aggregator = []
#         for each in fl:
#             with open(each, "r") as fr:
#                 data = json.load(fr)
#                 paper_id = data.get("paper_id")
#                 title = data.get("metadata").get("title")
#                 abstract = ''.join([x.get("text") for x in data.get("abstract")])
#                 # abstract paragraphs may not be in order, ignoring that fact.
#                 aggregator.append({"paper_id":paper_id, "title":title, "abstract":abstract})
#         df = pd.DataFrame(aggregator)
        
#         if df.empty:
#             logger.warning("DataFrame is empty! Not loading")
#             return None
#         else:
#             self.df = df
#             self._process_data()
#             return self.df
    
    def _load_metadata(self):
        if os.path.exists(f"{self.DATA_DIR}/processed_metadata.pickle"):
            logger.info(f"Loading {self.DATA_DIR}/processed_metadata.pickle ")
            self._load_pickle(filename=f"{self.DATA_DIR}/processed_metadata.pickle")
        elif os.path.exists(f"{self.DATA_DIR}/sample_metadata.csv"):
            logger.info(f"Loading {self.DATA_DIR}/sample_metadata.csv")
            return self.load_sample()
        else:
            return self.update()
            
        if self.df.empty:
            logger.warning("DataFrame is empty! Not loading")
            return None
        else:
            return self.df
        
    def get_data(self):
        if not self.df.empty:
            return self.df
        else:
            return self._load_metadata()
    
