from loguru import logger
from embedding import Embedding
from tokenizer import Tokenizer
import numpy as np

class Vectorizer(object):
    
    em = Embedding()
    WEM = em.get_embedding()
    EMBEDDING_DIM = em.get_embedding_dim()
    
    @staticmethod
    def vectorize_tokens(tokens):
        return Vectorizer.WEM.query(tokens)
        
    @staticmethod
    def vectorize_sents(sents):
        ret_sents = []
        for each in sents:
            ret_sents.append(Vectorizer.vectorize_sent(each))
        return ret_sents
    
    @staticmethod
    def vectorize_sent(sent, get_tokens=False):
        sent_vec = np.zeros(Vectorizer.EMBEDDING_DIM)
        sent_token = Tokenizer.tokenize(sent) if isinstance(sent, str) else []

        if not sent_token:
            return sent_vec

        numw = 0
        for w in sent_token:
            try:
                sent_vec = np.add(sent_vec, Vectorizer.WEM.query(w))
                numw+=1
            except:
                pass

        vect = sent_vec / np.sqrt(sent_vec.dot(sent_vec))

        if get_tokens:
            return vect, sent_token
        else:
            return vect