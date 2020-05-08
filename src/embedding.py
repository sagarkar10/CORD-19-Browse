from pymagnitude import *
import configparser
from loguru import logger


class Embedding(object):
    def __init__(self, config_path="config.cfg"):
        self.config_path = config_path
        config = configparser.ConfigParser()
        config.read(self.config_path)
        self.EMBEDING_FILE = config.get("DATA", "EMBEDING_FILE")
        self.EMBEDDING_DIM = config.getint("DATA", "EMBEDING_DIM")
        try:
            self._load_embedding()
        except:
            raise ValueError(f"Model File Not found: {self.EMBEDING_FILE}")

    def __str__(self):
        return f"config_path:{self.config_path}, embedding_file_path:{self.EMBEDING_FILE}, embedding_dimension:{self.EMBEDDING_DIM}, length:{self.WEM.length}"

    def __repr__(self):
        return self.__str__()

    def _load_embedding(self):
        logger.info(f"Loading Embeddings from: {self.EMBEDING_FILE}")
        self.WEM = Magnitude(self.EMBEDING_FILE)

    def get_embedding(self):
        return self.WEM

    def get_embedding_dim(self):
        return self.EMBEDDING_DIM
