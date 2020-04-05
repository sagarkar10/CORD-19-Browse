import pandas as pd
import configparser
import json
import glob
import os
from loguru import logger
from vectorizer import Vectorizer
import pickle

class DataIO(object):
    def __init__(self, config_path="../config.cfg", autoload=True):
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
        logger.info(f"Loading processed_metadata from {self.DATA_DIR}")
        
        with open(f"{self.DATA_DIR}/processed_metadata.pickle", "rb") as fp:
            df = pickle.load(fp)
        
        if df.empty:
            logger.warning("DataFrame is empty! Not loading")
            return None
        else:
            self.df = df
            return self.df
        
    def get_data(self):
        if not self.df.empty:
            return self.df
        else:
            return self._load_metadata()
    
